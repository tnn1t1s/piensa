#!/usr/bin/env python3
"""
Judge experiment results using an LLM classifier.

Reads raw responses from a results JSON file and classifies each as A, B, unclear, or refused.
Metrics computation is configurable via experiment config.yaml files.

Example usage:
    # Judge with experiment config (recommended)
    python src/judge_results.py experiments/fle-4x4/results/file.json --experiment fle-4x4

    # Judge all conditions (sequential, verbose)
    python src/judge_results.py results/4x4_asian_disease_20251231_214700.json

    # Judge with 10 parallel requests (6x faster)
    python src/judge_results.py results/file.json --concurrency 10

    # Judge only specific conditions (by pattern)
    python src/judge_results.py results/file.json --filter "adapter_en_*"

    # List conditions without judging
    python src/judge_results.py results/file.json --list

    # Use a different model
    python src/judge_results.py results/file.json --model openai/gpt-4o
"""

import argparse
import asyncio
import fnmatch
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

from src.agents.choice_extractor import ChoiceExtractor


# Default metrics config (framing effect with gain/loss suffixes)
DEFAULT_METRICS = {
    "type": "framing_effect",
    "gain_suffix": "_gain",
    "loss_suffix": "_loss",
    "choices": {
        "certain": "A",
        "risky": "B",
        "unclear": "unclear",
    }
}


def load_experiment_config(experiment_name: str) -> dict | None:
    """Load experiment config from experiments/<name>/config.yaml."""
    config_path = Path("experiments") / experiment_name / "config.yaml"
    if not config_path.exists():
        return None
    with open(config_path) as f:
        return yaml.safe_load(f)


def log(msg: str = "", flush: bool = True):
    """Print with immediate flush for real-time feedback."""
    print(msg, flush=flush)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Judge experiment results using an LLM classifier.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "results_file",
        type=Path,
        help="Path to results JSON file with raw responses"
    )
    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="Experiment name to load config from (e.g., 'fle-4x4')"
    )
    parser.add_argument(
        "--filter",
        type=str,
        default=None,
        help="Filter conditions by glob pattern (e.g., 'adapter_en_*', '*_gain')"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List conditions and exit without judging"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="openai/gpt-4-turbo",
        help="Model to use for judging (default: openai/gpt-4-turbo)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: <input>_judged.json)"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of parallel API requests (default: 1, try 10-20 for speed)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity (only show condition summaries)"
    )
    return parser.parse_args()


def extract_prompt_language(condition_name: str, cond_data: dict) -> str:
    """Extract the prompt language from condition name or data."""
    # Check if explicitly stored in data
    if "prompt_lang" in cond_data:
        return cond_data["prompt_lang"]

    # Try to parse from 4x4 format: "adapter_XX_prompt_YY_frame"
    if "prompt_" in condition_name:
        parts = condition_name.split("_")
        try:
            prompt_idx = parts.index("prompt") + 1
            if prompt_idx < len(parts):
                return parts[prompt_idx]
        except (ValueError, IndexError):
            pass

    # Fallback: first part of condition name (e.g., "en_gain" -> "en")
    return condition_name.split("_")[0]


class ProgressTracker:
    """Thread-safe progress tracker for parallel operations."""

    def __init__(self, total: int, quiet: bool = False):
        self.total = total
        self.completed = 0
        self.quiet = quiet
        self.lock = asyncio.Lock()
        self.results: dict[int, dict] = {}

    async def record(self, index: int, result: dict, response: str, elapsed: float):
        """Record a completed result and print progress."""
        async with self.lock:
            self.completed += 1
            self.results[index] = result

            if not self.quiet:
                display_resp = response[:30].replace('\n', ' ')
                if len(response) > 30:
                    display_resp += "..."
                log(f"    [{self.completed}/{self.total}] {result['choice']} ({elapsed:.2f}s) \"{display_resp}\"")

    def get_ordered_results(self) -> list[dict]:
        """Return results in original order."""
        return [self.results[i] for i in sorted(self.results.keys())]


async def judge_response_with_semaphore(
    semaphore: asyncio.Semaphore,
    extractor: ChoiceExtractor,
    response: str,
    language: str,
    index: int,
    tracker: ProgressTracker
) -> None:
    """Judge a single response with rate limiting via semaphore."""
    async with semaphore:
        start = time.time()
        extraction = await extractor.extract(response, language)
        elapsed = time.time() - start

        result = {
            "response": response,
            "choice": extraction.choice.value,
            "confidence": extraction.confidence,
            "reasoning": extraction.reasoning,
        }

        await tracker.record(index, result, response, elapsed)


async def judge_condition_parallel(
    extractor: ChoiceExtractor,
    responses: list[str],
    language: str,
    concurrency: int,
    quiet: bool = False
) -> list[dict]:
    """Judge all responses for a condition with parallel requests."""
    semaphore = asyncio.Semaphore(concurrency)
    tracker = ProgressTracker(len(responses), quiet)

    # Create all tasks
    tasks = [
        judge_response_with_semaphore(
            semaphore, extractor, response, language, i, tracker
        )
        for i, response in enumerate(responses)
    ]

    # Run all tasks concurrently (semaphore limits actual parallelism)
    await asyncio.gather(*tasks)

    return tracker.get_ordered_results()


async def judge_condition_sequential(
    extractor: ChoiceExtractor,
    responses: list[str],
    language: str,
    quiet: bool = False
) -> list[dict]:
    """Judge all responses for a condition sequentially (for comparison/debugging)."""
    results = []
    for i, response in enumerate(responses):
        start = time.time()
        extraction = await extractor.extract(response, language)
        elapsed = time.time() - start

        result = {
            "response": response,
            "choice": extraction.choice.value,
            "confidence": extraction.confidence,
            "reasoning": extraction.reasoning,
        }
        results.append(result)

        if not quiet:
            display_resp = response[:30].replace('\n', ' ')
            if len(response) > 30:
                display_resp += "..."
            log(f"    [{i+1}/{len(responses)}] {result['choice']} ({elapsed:.2f}s) \"{display_resp}\"")

    return results


def compute_stats(judgments: list[dict]) -> dict:
    """Compute statistics from judgments."""
    choices = [j["choice"] for j in judgments]
    counts = Counter(choices)
    n = len(choices)

    return {
        "counts": dict(counts),
        "n": n,
        "p_A": counts.get("A", 0) / n if n > 0 else 0,
        "p_B": counts.get("B", 0) / n if n > 0 else 0,
        "p_unclear": counts.get("unclear", 0) / n if n > 0 else 0,
        "p_refused": counts.get("refused", 0) / n if n > 0 else 0,
    }


def compute_framing_effects(judged_conds: dict, metrics: dict) -> dict:
    """Compute framing effects from judged conditions using metrics config.

    Returns dict of framing effect entries to add to conditions.
    """
    if metrics.get("type") != "framing_effect":
        return {}

    gain_suffix = metrics.get("gain_suffix", "_gain")
    loss_suffix = metrics.get("loss_suffix", "_loss")
    certain_choice = metrics.get("choices", {}).get("certain", "A")

    effects = {}
    gain_conds = [c for c in judged_conds if c.endswith(gain_suffix)]

    for gain_key in sorted(gain_conds):
        loss_key = gain_key.replace(gain_suffix, loss_suffix)
        if loss_key in judged_conds:
            # Get probability of certain choice in each frame
            p_certain_gain = judged_conds[gain_key].get(f"p_{certain_choice}", 0)
            p_certain_loss = judged_conds[loss_key].get(f"p_{certain_choice}", 0)
            delta = p_certain_gain - p_certain_loss

            # Store framing effect
            fe_key = gain_key.replace(gain_suffix, "_framing_effect")
            effects[fe_key] = {
                "delta": delta,
                f"p_{certain_choice}_gain": p_certain_gain,
                f"p_{certain_choice}_loss": p_certain_loss,
            }

    return effects


def filter_conditions(conditions: dict, pattern: str | None) -> list[str]:
    """Filter condition names by glob pattern."""
    names = [k for k in conditions.keys() if "framing_effect" not in k]

    if pattern:
        names = [n for n in names if fnmatch.fnmatch(n, pattern)]

    return sorted(names)


async def main():
    args = parse_args()

    # Validate input file
    if not args.results_file.exists():
        log(f"Error: File not found: {args.results_file}")
        sys.exit(1)

    # Load experiment config if specified
    metrics = DEFAULT_METRICS.copy()
    if args.experiment:
        config = load_experiment_config(args.experiment)
        if config is None:
            log(f"Warning: Experiment config not found for '{args.experiment}', using defaults")
        else:
            log(f"Loaded config: experiments/{args.experiment}/config.yaml")
            if "metrics" in config:
                metrics = {**DEFAULT_METRICS, **config["metrics"]}

    # Load results
    log(f"Loading: {args.results_file}")
    with open(args.results_file) as f:
        data = json.load(f)

    conditions = data.get("conditions", {})
    metadata = data.get("metadata", {})

    # Filter conditions
    condition_names = filter_conditions(conditions, args.filter)

    # Count total responses
    total_responses = sum(
        len(conditions[c].get("responses", []))
        for c in condition_names
        if "responses" in conditions[c]
    )

    log(f"Found {len(condition_names)} conditions, {total_responses} total responses")
    if args.filter:
        log(f"Filter: {args.filter}")

    # List mode: just show conditions and exit
    if args.list:
        log("\nConditions:")
        for name in condition_names:
            cond = conditions[name]
            n_resp = len(cond.get("responses", []))
            has_responses = "responses" in cond
            status = f"{n_resp} responses" if has_responses else "no responses"
            log(f"  {name}: {status}")
        sys.exit(0)

    # Check for conditions without responses
    conditions_to_judge = [
        c for c in condition_names
        if "responses" in conditions[c]
    ]
    skipped = len(condition_names) - len(conditions_to_judge)
    if skipped > 0:
        log(f"Skipping {skipped} conditions without raw responses")

    if not conditions_to_judge:
        log("Error: No conditions with responses to judge")
        sys.exit(1)

    # Initialize extractor
    log(f"\nInitializing LLM judge: {args.model}")
    start_time = time.time()
    extractor = ChoiceExtractor(model_name=args.model)
    log(f"Judge ready ({time.time() - start_time:.2f}s)")

    # Show concurrency setting
    if args.concurrency > 1:
        log(f"Concurrency: {args.concurrency} parallel requests")
    else:
        log("Concurrency: sequential (use --concurrency N for parallel)")

    # Prepare output structure
    judged_results = {
        "metadata": {
            **metadata,
            "experiment": args.experiment,
            "judge_model": args.model,
            "judge_timestamp": datetime.now().isoformat(),
            "filter_pattern": args.filter,
            "concurrency": args.concurrency,
            "metrics_type": metrics.get("type"),
        },
        "conditions": {}
    }

    # Judge each condition
    log(f"\n{'='*60}")
    log(f"Judging {len(conditions_to_judge)} conditions")
    log(f"{'='*60}")

    for i, condition_name in enumerate(conditions_to_judge):
        cond_data = conditions[condition_name]
        responses = cond_data["responses"]
        language = extract_prompt_language(condition_name, cond_data)

        log(f"\n[{i+1}/{len(conditions_to_judge)}] {condition_name} ({len(responses)} responses, lang={language})")

        cond_start = time.time()

        if args.concurrency > 1:
            judgments = await judge_condition_parallel(
                extractor, responses, language, args.concurrency, args.quiet
            )
        else:
            judgments = await judge_condition_sequential(
                extractor, responses, language, args.quiet
            )

        cond_elapsed = time.time() - cond_start

        stats = compute_stats(judgments)

        judged_results["conditions"][condition_name] = {
            "judgments": judgments,
            **stats,
            "prompt_lang": language,
        }

        # Summary for this condition
        rate = len(responses) / cond_elapsed if cond_elapsed > 0 else 0
        log(f"  => P(A)={stats['p_A']:.1%}, P(B)={stats['p_B']:.1%}, "
            f"unclear={stats['p_unclear']:.1%} ({cond_elapsed:.1f}s, {rate:.1f} req/s)")

    # Compute metrics based on config
    if metrics.get("type") == "framing_effect":
        log(f"\n{'='*60}")
        log("FRAMING EFFECTS")
        log(f"{'='*60}")

        judged_conds = judged_results["conditions"]
        framing_effects = compute_framing_effects(judged_conds, metrics)

        # Add to results and log
        for fe_key, fe_data in framing_effects.items():
            judged_results["conditions"][fe_key] = fe_data
            base_name = fe_key.replace("_framing_effect", "")
            certain_choice = metrics.get("choices", {}).get("certain", "A")
            p_gain = fe_data.get(f"p_{certain_choice}_gain", 0)
            p_loss = fe_data.get(f"p_{certain_choice}_loss", 0)
            log(f"{base_name}: Δ = {fe_data['delta']:+.1%} "
                f"(P({certain_choice}|gain)={p_gain:.1%}, P({certain_choice}|loss)={p_loss:.1%})")

    # Save results
    if args.output:
        output_file = args.output
    else:
        output_file = args.results_file.parent / f"{args.results_file.stem}_judged.json"

    with open(output_file, "w") as f:
        json.dump(judged_results, f, indent=2, ensure_ascii=False)

    total_elapsed = time.time() - start_time
    rate = total_responses / total_elapsed if total_elapsed > 0 else 0
    log(f"\n{'='*60}")
    log(f"Complete! Judged {total_responses} responses in {total_elapsed:.1f}s ({rate:.1f} req/s)")
    log(f"Output: {output_file}")
    log(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
