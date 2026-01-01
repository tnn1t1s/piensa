"""
Run Asian Disease Problem with multiple trials to estimate response distributions.

This script ONLY collects raw responses. Use judge_results.py to classify them.
"""

import json
from pathlib import Path
from datetime import datetime

from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler


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
        if (i + 1) % 10 == 0:
            print(f"    Trial {i+1}/{n_trials}")
    return responses


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mlx-community/Mistral-7B-Instruct-v0.3-4bit")
    parser.add_argument("--n-trials", type=int, default=100)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--languages", nargs="+", default=["en", "es", "he", "zh"])
    parser.add_argument("--output", default="results")
    args = parser.parse_args()

    print("=" * 60)
    print("Asian Disease Problem: Response Collection")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Trials per condition: {args.n_trials}")
    print(f"Temperature: {args.temperature}")
    print(f"Languages: {args.languages}")
    print()

    # Load model
    print("Loading model...")
    model, tokenizer = load(args.model)
    print("Model loaded!")
    print()

    results = {
        "metadata": {
            "model": args.model,
            "n_trials": args.n_trials,
            "temperature": args.temperature,
            "timestamp": datetime.now().isoformat(),
            "note": "Raw responses only. Use judge_results.py to classify.",
        },
        "conditions": {}
    }

    for lang in args.languages:
        for frame in ["gain", "loss"]:
            condition = f"{lang}_{frame}"
            print(f"Running condition: {condition}")

            prompt = get_prompt(lang, frame)
            responses = run_trials(model, tokenizer, prompt, args.n_trials, args.temperature)

            results["conditions"][condition] = {
                "responses": responses,
            }

            print(f"  Collected {len(responses)} responses")
            print()

    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"asian_disease_t{args.temperature}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print(f"Raw results saved to: {output_file}")
    print(f"Run: python src/judge_results.py {output_file}")


if __name__ == "__main__":
    main()
