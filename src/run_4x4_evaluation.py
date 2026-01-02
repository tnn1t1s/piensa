"""
Run 4x4 Adapter × Prompt evaluation for Asian Disease Problem.

Tests all 16 combinations of:
- 4 adapters (EN, ES, HE, ZH)
- 4 prompt languages (EN, ES, HE, ZH)
- 2 frames (gain, loss)

Total: 32 conditions

This script ONLY collects raw responses. Use judge_results.py to classify them.

Example usage:
    # Run with experiment config (recommended)
    python src/run_4x4_evaluation.py --experiment fle-4x4

    # Run with defaults
    python src/run_4x4_evaluation.py --n-trials 50 --temperature 0.7
"""

import json
from pathlib import Path
from datetime import datetime

import mlx.core as mx
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler
import yaml


def log(msg: str = ""):
    """Print with immediate flush for real-time feedback."""
    print(msg, flush=True)


def load_experiment_config(experiment_name: str) -> dict | None:
    """Load experiment config from experiments/<name>/config.yaml."""
    config_path = Path("experiments") / experiment_name / "config.yaml"
    if not config_path.exists():
        return None
    with open(config_path) as f:
        return yaml.safe_load(f)


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

    parser = argparse.ArgumentParser(
        description="Run 4x4 Adapter × Prompt evaluation",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--experiment", type=str, default=None,
                        help="Experiment name to load config from (e.g., 'fle-4x4')")
    parser.add_argument("--model", default=None,
                        help="Model to use (default: from config or Mistral-7B-Instruct)")
    parser.add_argument("--n-trials", type=int, default=None,
                        help="Number of trials per condition (default: from config or 50)")
    parser.add_argument("--temperature", type=float, default=None,
                        help="Sampling temperature (default: from config or 0.7)")
    parser.add_argument("--adapters-dir", default=None,
                        help="Adapters directory (default: experiments/<exp>/adapters or 'adapters')")
    parser.add_argument("--output", default=None,
                        help="Output directory (default: experiments/<exp>/results or 'results')")
    args = parser.parse_args()

    # Load experiment config if specified
    config = None
    if args.experiment:
        config = load_experiment_config(args.experiment)
        if config is None:
            log(f"Warning: Experiment config not found for '{args.experiment}'")
        else:
            log(f"Loaded config: experiments/{args.experiment}/config.yaml")

    # Merge config with CLI args (CLI takes precedence)
    model = args.model or (config.get("model", {}).get("base") if config else None) or "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
    n_trials = args.n_trials or (config.get("inference", {}).get("n_trials") if config else None) or 50
    temperature = args.temperature or (config.get("inference", {}).get("temperature") if config else None) or 0.7
    max_tokens = (config.get("inference", {}).get("max_tokens") if config else None) or 256

    # Determine adapters and languages from config or defaults
    adapters = (config.get("adapters") if config else None) or ADAPTERS
    languages = (config.get("languages") if config else None) or LANGUAGES
    frames = (config.get("frames") if config else None) or ["gain", "loss"]

    # Get role prefixes and scenarios from config or defaults
    role_prefix = (config.get("role_prefix") if config else None) or ROLE_PREFIX
    scenarios_config = config.get("scenarios", {}) if config else {}
    # Flatten scenarios structure: scenarios.asian_disease.en.gain -> scenarios.en.gain
    scenarios = {}
    if scenarios_config:
        for scenario_name, scenario_data in scenarios_config.items():
            scenarios = scenario_data  # Use first scenario for now
            break
    if not scenarios:
        scenarios = SCENARIOS

    # Determine paths
    if args.experiment:
        exp_dir = Path("experiments") / args.experiment
        adapters_dir = Path(args.adapters_dir) if args.adapters_dir else exp_dir / "adapters"
        output_dir = Path(args.output) if args.output else exp_dir / "results"
    else:
        adapters_dir = Path(args.adapters_dir or "adapters")
        output_dir = Path(args.output or "results")

    log("=" * 70)
    log("4x4 Adapter × Prompt Evaluation: Asian Disease Problem")
    log("=" * 70)
    if args.experiment:
        log(f"Experiment: {args.experiment}")
    log(f"Model: {model}")
    log(f"Trials per condition: {n_trials}")
    log(f"Temperature: {temperature}")
    log(f"Total conditions: {len(adapters)} adapters × {len(languages)} prompts × {len(frames)} frames = {len(adapters) * len(languages) * len(frames)}")
    log()

    results = {
        "metadata": {
            "experiment": args.experiment,
            "model": model,
            "n_trials": n_trials,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timestamp": datetime.now().isoformat(),
            "adapters": adapters,
            "languages": languages,
            "frames": frames,
            "note": "Raw responses only. Use judge_results.py to classify.",
        },
        "conditions": {}
    }

    # Helper to get prompt for a language and frame
    def get_prompt_from_config(lang: str, frame: str) -> str:
        prefix = role_prefix.get(lang, "")
        scenario = scenarios.get(lang, {}).get(frame, "")
        return prefix + scenario

    for adapter_lang in adapters:
        adapter_path = adapters_dir / f"lora_{adapter_lang}"

        log(f"\n{'='*70}")
        log(f"ADAPTER: {adapter_lang.upper()}")
        log(f"{'='*70}")

        # Load model with this adapter
        loaded_model, tokenizer = load_model_with_adapter(model, str(adapter_path))

        for prompt_lang in languages:
            match_status = "MATCHED" if adapter_lang == prompt_lang else "mismatched"

            for frame in frames:
                condition_key = f"adapter_{adapter_lang}_prompt_{prompt_lang}_{frame}"
                log(f"\n  {condition_key} ({match_status})")

                prompt = get_prompt_from_config(prompt_lang, frame)
                responses = run_trials(loaded_model, tokenizer, prompt, n_trials, temperature)

                results["conditions"][condition_key] = {
                    "adapter": adapter_lang,
                    "prompt_lang": prompt_lang,
                    "frame": frame,
                    "matched": adapter_lang == prompt_lang,
                    "responses": responses,
                }

                log(f"    Collected {len(responses)} responses")

        # Clear model from memory before loading next adapter
        del loaded_model
        mx.metal.clear_cache()

    # Save raw results
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"4x4_asian_disease_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    log(f"\n{'='*70}")
    log(f"Raw results saved to: {output_file}")
    if args.experiment:
        log(f"Run: python src/judge_results.py {output_file} --experiment {args.experiment}")
    else:
        log(f"Run: python src/judge_results.py {output_file}")
    log(f"{'='*70}")


if __name__ == "__main__":
    main()
