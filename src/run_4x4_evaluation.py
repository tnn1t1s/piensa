"""
Run 4x4 Adapter × Prompt evaluation for Asian Disease Problem.

Tests all 16 combinations of:
- 4 adapters (EN, ES, HE, ZH)
- 4 prompt languages (EN, ES, HE, ZH)
- 2 frames (gain, loss)

Total: 32 conditions

This script ONLY collects raw responses. Use judge_results.py to classify them.
"""

import json
from pathlib import Path
from datetime import datetime

import mlx.core as mx
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler


def log(msg: str = ""):
    """Print with immediate flush for real-time feedback."""
    print(msg, flush=True)


# Role-binding prefix for each language (minimal variant for multilingual parity)
ROLE_PREFIX = {
    "en": """You are a participant in a study.
Choose one option.
Do not explain.
Answer only 'A' or 'B'.

""",
    "es": """Eres un participante en un estudio.
Elige una opción.
No expliques.
Responde solo 'A' o 'B'.

""",
    "he": """אתה משתתף במחקר.
בחר אפשרות אחת.
אל תסביר.
ענה רק 'A' או 'B'.

""",
    "zh": """你是一项研究的参与者。
选择一个选项。
不要解释。
只回答'A'或'B'。

""",
}

# Scenario content (translated per language)
SCENARIOS = {
    "en": {
        "gain": """Recently, a dangerous new disease has been going around. Without medicine, 600,000 people will die from it. In order to save these people, two types of medicine are being made.

If you choose Medicine A, 200,000 people will be saved.
If you choose Medicine B, there is a 33.3% chance that 600,000 people will be saved and a 66.6% chance that no one will be saved.

Which medicine do you choose?""",
        "loss": """Recently, a dangerous new disease has been going around. Without medicine, 600,000 people will die from it. In order to save these people, two types of medicine are being made.

If you choose Medicine A, 400,000 people will die.
If you choose Medicine B, there is a 33.3% chance that no one will die and a 66.6% chance that 600,000 will die.

Which medicine do you choose?"""
    },
    "es": {
        "gain": """Recientemente, una nueva enfermedad peligrosa se ha estado propagando. Sin medicamento, 600.000 personas morirán. Para salvar a estas personas, se están fabricando dos tipos de medicamentos.

Si elige el Medicamento A, se salvarán 200.000 personas.
Si elige el Medicamento B, hay un 33,3% de probabilidad de que se salven 600.000 personas y un 66,6% de probabilidad de que no se salve nadie.

¿Qué medicamento elige?""",
        "loss": """Recientemente, una nueva enfermedad peligrosa se ha estado propagando. Sin medicamento, 600.000 personas morirán. Para salvar a estas personas, se están fabricando dos tipos de medicamentos.

Si elige el Medicamento A, morirán 400.000 personas.
Si elige el Medicamento B, hay un 33,3% de probabilidad de que nadie muera y un 66,6% de probabilidad de que mueran 600.000 personas.

¿Qué medicamento elige?"""
    },
    "he": {
        "gain": """לאחרונה התפשטה מחלה מסוכנת חדשה. ללא תרופה, 600,000 אנשים ימותו ממנה. כדי להציל אנשים אלה, מייצרים שני סוגי תרופות.

אם תבחר בתרופה A, 200,000 אנשים יינצלו.
אם תבחר בתרופה B, יש סיכוי של 33.3% ש-600,000 אנשים יינצלו וסיכוי של 66.6% שאף אחד לא יינצל.

איזו תרופה אתה בוחר?""",
        "loss": """לאחרונה התפשטה מחלה מסוכנת חדשה. ללא תרופה, 600,000 אנשים ימותו ממנה. כדי להציל אנשים אלה, מייצרים שני סוגי תרופות.

אם תבחר בתרופה A, 400,000 אנשים ימותו.
אם תבחר בתרופה B, יש סיכוי של 33.3% שאף אחד לא ימות וסיכוי של 66.6% ש-600,000 אנשים ימותו.

איזו תרופה אתה בוחר?"""
    },
    "zh": {
        "gain": """最近，一种危险的新疾病正在蔓延。如果没有药物，将有60万人死亡。为了拯救这些人，正在生产两种药物。

如果你选择药物A，将有20万人得救。
如果你选择药物B，有33.3%的概率60万人全部得救，有66.6%的概率没有人得救。

你选择哪种药物？""",
        "loss": """最近，一种危险的新疾病正在蔓延。如果没有药物，将有60万人死亡。为了拯救这些人，正在生产两种药物。

如果你选择药物A，将有40万人死亡。
如果你选择药物B，有33.3%的概率没有人死亡，有66.6%的概率60万人全部死亡。

你选择哪种药物？"""
    }
}


def get_prompt(lang: str, frame: str) -> str:
    """Combine role prefix with scenario for a complete prompt."""
    return ROLE_PREFIX[lang] + SCENARIOS[lang][frame]

ADAPTERS = ["en", "es", "he", "zh"]
LANGUAGES = ["en", "es", "he", "zh"]


def format_chat_prompt(tokenizer, user_message: str) -> str:
    """Format prompt using Mistral chat template."""
    messages = [{"role": "user", "content": user_message}]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def run_trials(model, tokenizer, prompt: str, n_trials: int, temperature: float) -> list[str]:
    """Run n trials and return list of raw responses."""
    sampler = make_sampler(temp=temperature)
    formatted_prompt = format_chat_prompt(tokenizer, prompt)

    responses = []
    for i in range(n_trials):
        response = generate(
            model, tokenizer,
            prompt=formatted_prompt,
            max_tokens=256,
            sampler=sampler,
            verbose=False,
        )
        responses.append(response)
    return responses


def load_model_with_adapter(base_model: str, adapter_path: str | None):
    """Load model with optional LoRA adapter."""
    if adapter_path and Path(adapter_path).exists():
        log(f"  Loading with adapter: {adapter_path}")
        model, tokenizer = load(base_model, adapter_path=adapter_path)
    else:
        log(f"  Loading base model (no adapter)")
        model, tokenizer = load(base_model)
    return model, tokenizer


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mlx-community/Mistral-7B-Instruct-v0.3-4bit")
    parser.add_argument("--n-trials", type=int, default=50)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--adapters-dir", default="adapters")
    parser.add_argument("--output", default="results")
    args = parser.parse_args()

    log("=" * 70)
    log("4x4 Adapter × Prompt Evaluation: Asian Disease Problem")
    log("=" * 70)
    log(f"Model: {args.model}")
    log(f"Trials per condition: {args.n_trials}")
    log(f"Temperature: {args.temperature}")
    log(f"Total conditions: {len(ADAPTERS)} adapters × {len(LANGUAGES)} prompts × 2 frames = {len(ADAPTERS) * len(LANGUAGES) * 2}")
    log()

    results = {
        "metadata": {
            "model": args.model,
            "n_trials": args.n_trials,
            "temperature": args.temperature,
            "timestamp": datetime.now().isoformat(),
            "adapters": ADAPTERS,
            "languages": LANGUAGES,
            "note": "Raw responses only. Use judge_results.py to classify.",
        },
        "conditions": {}
    }

    adapters_dir = Path(args.adapters_dir)

    for adapter_lang in ADAPTERS:
        adapter_path = adapters_dir / f"lora_{adapter_lang}"

        log(f"\n{'='*70}")
        log(f"ADAPTER: {adapter_lang.upper()}")
        log(f"{'='*70}")

        # Load model with this adapter
        model, tokenizer = load_model_with_adapter(args.model, str(adapter_path))

        for prompt_lang in LANGUAGES:
            match_status = "MATCHED" if adapter_lang == prompt_lang else "mismatched"

            for frame in ["gain", "loss"]:
                condition_key = f"adapter_{adapter_lang}_prompt_{prompt_lang}_{frame}"
                log(f"\n  {condition_key} ({match_status})")

                prompt = get_prompt(prompt_lang, frame)
                responses = run_trials(model, tokenizer, prompt, args.n_trials, args.temperature)

                results["conditions"][condition_key] = {
                    "adapter": adapter_lang,
                    "prompt_lang": prompt_lang,
                    "frame": frame,
                    "matched": adapter_lang == prompt_lang,
                    "responses": responses,
                }

                log(f"    Collected {len(responses)} responses")

        # Clear model from memory before loading next adapter
        del model
        mx.metal.clear_cache()

    # Save raw results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"4x4_asian_disease_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    log(f"\n{'='*70}")
    log(f"Raw results saved to: {output_file}")
    log(f"Run: python src/judge_results.py {output_file}")
    log(f"{'='*70}")


if __name__ == "__main__":
    main()
