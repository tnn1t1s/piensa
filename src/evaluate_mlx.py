"""
Evaluate bias battery using MLX on Apple Silicon.
Uses 4-bit quantized Mistral for efficient local inference.
"""

import json
import re
from pathlib import Path
from datetime import datetime

import mlx.core as mx
from mlx_lm import load, generate


def load_bias_battery(path: str = "data/test/bias_battery.json") -> dict:
    """Load the bias battery from JSON."""
    with open(path) as f:
        return json.load(f)


def extract_choice(response: str, options: list[str]) -> str:
    """Extract the choice from model response."""
    response_upper = response.strip().upper()

    # Try exact match first
    for opt in options:
        if response_upper == opt.upper():
            return opt

    # Try first character match
    for opt in options:
        if opt.upper() in response_upper:
            # Check if it's the only option mentioned
            other_opts = [o for o in options if o != opt]
            if not any(o.upper() in response_upper for o in other_opts):
                return opt

    # Return first mentioned option
    for opt in options:
        if opt.upper() in response_upper:
            return opt

    return "unclear"


def extract_number(response: str) -> str:
    """Extract a number from model response."""
    # Find all numbers in response
    numbers = re.findall(r'\d+', response.strip())
    if numbers:
        return numbers[0]
    return "unclear"


def run_framing_scenario(model, tokenizer, scenario: dict, language: str) -> dict:
    """Run a framing scenario (asian_disease, etc.)."""
    results = {}

    for variant_name, variant_data in scenario["variants"].items():
        lang_data = variant_data[language]
        prompt = lang_data["prompt"]

        response = generate(
            model, tokenizer,
            prompt=prompt,
            max_tokens=20,
            verbose=False,
        )

        choice = extract_choice(response, lang_data["options"])

        results[variant_name] = {
            "response": response.strip(),
            "choice": choice,
            "intuitive_response": lang_data.get("intuitive_response"),
        }

    return results


def run_crt_scenario(model, tokenizer, scenario: dict, language: str) -> dict:
    """Run CRT items."""
    results = {}

    for item_name, item_data in scenario["items"].items():
        lang_data = item_data[language]
        prompt = lang_data["prompt"]

        response = generate(
            model, tokenizer,
            prompt=prompt,
            max_tokens=30,
            verbose=False,
        )

        answer = extract_number(response)
        correct = lang_data["correct_answer"]
        intuitive_wrong = lang_data["intuitive_wrong_answer"]

        results[item_name] = {
            "response": response.strip(),
            "answer": answer,
            "correct_answer": correct,
            "is_correct": answer == correct,
            "is_intuitive_wrong": answer == intuitive_wrong,
        }

    return results


def run_allais_scenario(model, tokenizer, scenario: dict, language: str) -> dict:
    """Run Allais paradox questions."""
    results = {}

    for q_name, q_data in scenario["questions"].items():
        lang_data = q_data[language]
        prompt = lang_data["prompt"]

        response = generate(
            model, tokenizer,
            prompt=prompt,
            max_tokens=20,
            verbose=False,
        )

        choice = extract_choice(response, lang_data["options"])

        results[q_name] = {
            "response": response.strip(),
            "choice": choice,
        }

    # Check consistency
    q1_choice = results.get("question_1", {}).get("choice", "")
    q2_choice = results.get("question_2", {}).get("choice", "")

    # Consistent if (A,C) or (B,D)
    consistent = (q1_choice == "A" and q2_choice == "C") or \
                 (q1_choice == "B" and q2_choice == "D")
    allais_violation = (q1_choice == "A" and q2_choice == "D")

    results["_metrics"] = {
        "consistent": consistent,
        "allais_violation": allais_violation,
    }

    return results


def run_holt_laury(model, tokenizer, scenario: dict, language: str) -> dict:
    """Run Holt-Laury lottery pairs."""
    template = scenario["prompt_template"][language]
    pairs = scenario["pairs"]
    results = {"pairs": [], "_metrics": {}}

    switching_point = None
    choices = []

    for i, pair in enumerate(pairs):
        prob_high = int(pair["prob_high"] * 100)
        prob_low = 100 - prob_high

        prompt = template.format(
            prob_high=prob_high,
            prob_low=prob_low,
            a_high=pair["lottery_a"]["high"],
            a_low=pair["lottery_a"]["low"],
            b_high=pair["lottery_b"]["high"],
            b_low=pair["lottery_b"]["low"],
        )

        response = generate(
            model, tokenizer,
            prompt=prompt,
            max_tokens=20,
            verbose=False,
        )

        choice = extract_choice(response, ["A", "B"])
        choices.append(choice)

        results["pairs"].append({
            "pair_num": i + 1,
            "prob_high": prob_high,
            "response": response.strip(),
            "choice": choice,
        })

        # Find switching point (first B after only A's)
        if switching_point is None and choice == "B":
            if all(c == "A" for c in choices[:-1]):
                switching_point = i + 1

    # Calculate metrics
    num_safe = sum(1 for c in choices if c == "A")

    # Check consistency (no switching back)
    found_b = False
    consistent = True
    for c in choices:
        if c == "B":
            found_b = True
        elif found_b and c == "A":
            consistent = False
            break

    results["_metrics"] = {
        "switching_point": switching_point,
        "num_safe_choices": num_safe,
        "consistent": consistent,
    }

    return results


def evaluate_bias_battery(
    model,
    tokenizer,
    battery: dict,
    language: str,
) -> dict:
    """Evaluate all scenarios in the bias battery for a given language."""
    scenarios = battery["scenarios"]
    results = {"language": language, "scenarios": {}}

    for scenario_name, scenario in scenarios.items():
        print(f"  Running: {scenario_name}...", end=" ", flush=True)

        if scenario_name == "cognitive_reflection_test":
            result = run_crt_scenario(model, tokenizer, scenario, language)
        elif scenario_name == "allais_paradox":
            result = run_allais_scenario(model, tokenizer, scenario, language)
        elif scenario_name == "holt_laury":
            result = run_holt_laury(model, tokenizer, scenario, language)
        else:
            # Framing/accounting scenarios
            result = run_framing_scenario(model, tokenizer, scenario, language)

        results["scenarios"][scenario_name] = result
        print("done")

    return results


def compute_summary_metrics(results: dict, battery: dict) -> dict:
    """Compute summary metrics across all scenarios."""
    metrics = {}
    scenarios = results["scenarios"]

    # Asian disease framing effect
    if "asian_disease" in scenarios:
        ad = scenarios["asian_disease"]
        gain_b = 1 if ad.get("gain_frame", {}).get("choice") == "B" else 0
        loss_b = 1 if ad.get("loss_frame", {}).get("choice") == "B" else 0
        metrics["asian_disease_framing_effect"] = loss_b - gain_b
        metrics["asian_disease_gain_choice"] = ad.get("gain_frame", {}).get("choice")
        metrics["asian_disease_loss_choice"] = ad.get("loss_frame", {}).get("choice")

    # Ticket/money accounting bias
    if "ticket_money_lost" in scenarios:
        tm = scenarios["ticket_money_lost"]
        ticket_yes = 1 if tm.get("ticket_lost", {}).get("choice") in ["Yes", "Sí", "כן"] else 0
        money_yes = 1 if tm.get("money_lost", {}).get("choice") in ["Yes", "Sí", "כן"] else 0
        metrics["ticket_money_accounting_bias"] = money_yes - ticket_yes

    # Discount problem bias
    if "discount_problem" in scenarios:
        dp = scenarios["discount_problem"]
        small_yes = 1 if dp.get("discount_small", {}).get("choice") in ["Yes", "Sí", "כן"] else 0
        large_yes = 1 if dp.get("discount_large", {}).get("choice") in ["Yes", "Sí", "כן"] else 0
        metrics["discount_bias"] = small_yes - large_yes

    # CRT accuracy
    if "cognitive_reflection_test" in scenarios:
        crt = scenarios["cognitive_reflection_test"]
        correct = sum(1 for k, v in crt.items() if k != "_metrics" and v.get("is_correct"))
        intuitive = sum(1 for k, v in crt.items() if k != "_metrics" and v.get("is_intuitive_wrong"))
        total = len([k for k in crt.keys() if k != "_metrics"])
        metrics["crt_accuracy"] = correct / total if total > 0 else 0
        metrics["crt_intuitive_rate"] = intuitive / total if total > 0 else 0

    # Allais paradox
    if "allais_paradox" in scenarios:
        allais = scenarios["allais_paradox"]
        allais_metrics = allais.get("_metrics", {})
        metrics["allais_consistent"] = allais_metrics.get("consistent", False)
        metrics["allais_violation"] = allais_metrics.get("allais_violation", False)
        metrics["allais_q1_choice"] = allais.get("question_1", {}).get("choice")
        metrics["allais_q2_choice"] = allais.get("question_2", {}).get("choice")

    # Holt-Laury
    if "holt_laury" in scenarios:
        hl = scenarios["holt_laury"]
        hl_metrics = hl.get("_metrics", {})
        metrics["holt_laury_switching_point"] = hl_metrics.get("switching_point")
        metrics["holt_laury_num_safe"] = hl_metrics.get("num_safe_choices")
        metrics["holt_laury_consistent"] = hl_metrics.get("consistent")

    return metrics


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate bias battery with MLX")
    parser.add_argument(
        "--model",
        default="mlx-community/Mistral-7B-Instruct-v0.3-4bit",
        help="Model to use"
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en", "es", "he"],
        help="Languages to evaluate"
    )
    parser.add_argument(
        "--battery",
        default="data/test/bias_battery.json",
        help="Path to bias battery JSON"
    )
    parser.add_argument(
        "--output",
        default="results",
        help="Output directory"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Piensa Twice: Bias Battery Evaluation (MLX)")
    print("=" * 60)

    # Load model
    print(f"\nLoading model: {args.model}")
    model, tokenizer = load(args.model)
    print("Model loaded!")

    # Load battery
    print(f"\nLoading bias battery: {args.battery}")
    battery = load_bias_battery(args.battery)
    print(f"Loaded {len(battery['scenarios'])} scenarios")

    # Run evaluation for each language
    all_results = {
        "metadata": {
            "model": args.model,
            "timestamp": datetime.now().isoformat(),
            "languages": args.languages,
        },
        "results": {},
        "summary": {},
    }

    for lang in args.languages:
        print(f"\n{'=' * 60}")
        print(f"Evaluating language: {lang.upper()}")
        print("=" * 60)

        results = evaluate_bias_battery(model, tokenizer, battery, lang)
        metrics = compute_summary_metrics(results, battery)

        all_results["results"][lang] = results
        all_results["summary"][lang] = metrics

        print(f"\nSummary for {lang}:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"bias_battery_mlx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"Results saved to: {output_file}")
    print("=" * 60)

    # Print comparison table
    print("\n" + "=" * 60)
    print("COMPARISON ACROSS LANGUAGES")
    print("=" * 60)

    metrics_to_compare = [
        "asian_disease_framing_effect",
        "asian_disease_gain_choice",
        "asian_disease_loss_choice",
        "crt_accuracy",
        "allais_q1_choice",
        "holt_laury_num_safe",
    ]

    print(f"\n{'Metric':<35} | " + " | ".join(f"{l:>6}" for l in args.languages))
    print("-" * (35 + 3 + 10 * len(args.languages)))

    for metric in metrics_to_compare:
        values = []
        for lang in args.languages:
            v = all_results["summary"].get(lang, {}).get(metric, "N/A")
            if isinstance(v, float):
                values.append(f"{v:6.2f}")
            else:
                values.append(f"{str(v):>6}")
        print(f"{metric:<35} | " + " | ".join(values))


if __name__ == "__main__":
    main()
