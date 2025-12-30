"""
Data loading utilities for Piensa Twice experiments.

Handles loading instruction datasets for different languages and
the bias battery for evaluation.
"""

import json
from pathlib import Path
from typing import Optional

from datasets import load_dataset, Dataset


def load_instruction_dataset(
    dataset_name: str,
    subset: Optional[str] = None,
    split: str = "train",
    max_samples: Optional[int] = None
) -> Dataset:
    """
    Load an instruction dataset from HuggingFace.

    Args:
        dataset_name: HuggingFace dataset name (e.g., "tatsu-lab/alpaca")
        subset: Dataset subset if applicable
        split: Dataset split to load
        max_samples: Optional limit on number of samples

    Returns:
        HuggingFace Dataset object
    """
    if subset:
        dataset = load_dataset(dataset_name, subset, split=split)
    else:
        dataset = load_dataset(dataset_name, split=split)

    if max_samples:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    return dataset


def format_alpaca_prompt(example: dict) -> str:
    """
    Format an Alpaca-style example into a prompt string.

    Args:
        example: Dictionary with 'instruction', 'input', and 'output' keys

    Returns:
        Formatted prompt string
    """
    if example.get("input"):
        prompt = f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
    else:
        prompt = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    return prompt


def load_bias_battery(battery_path: Optional[Path] = None) -> dict:
    """
    Load the bias battery test scenarios.

    Args:
        battery_path: Path to bias_battery.json. If None, uses default location.

    Returns:
        Dictionary containing all test scenarios
    """
    if battery_path is None:
        battery_path = Path(__file__).parent.parent.parent / "data" / "test" / "bias_battery.json"

    with open(battery_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_scenario_prompts(
    battery: dict,
    scenario_name: str,
    language: str
) -> list[dict]:
    """
    Extract all prompts for a specific scenario in a given language.

    Args:
        battery: The full bias battery dictionary
        scenario_name: Name of the scenario (e.g., "asian_disease")
        language: Language code ("en", "es", "he")

    Returns:
        List of prompt dictionaries with prompt text and metadata
    """
    scenario = battery["scenarios"].get(scenario_name)
    if not scenario:
        raise ValueError(f"Unknown scenario: {scenario_name}")

    prompts = []

    # Handle different scenario structures
    if "variants" in scenario:
        for variant_name, variant_data in scenario["variants"].items():
            lang_data = variant_data.get(language)
            if lang_data:
                prompts.append({
                    "scenario": scenario_name,
                    "variant": variant_name,
                    "language": language,
                    "prompt": lang_data["prompt"],
                    "options": lang_data.get("options"),
                    "metadata": {
                        k: v for k, v in lang_data.items()
                        if k not in ["prompt", "options"]
                    }
                })

    elif "items" in scenario:
        for item_name, item_data in scenario["items"].items():
            lang_data = item_data.get(language)
            if lang_data:
                prompts.append({
                    "scenario": scenario_name,
                    "item": item_name,
                    "language": language,
                    "prompt": lang_data["prompt"],
                    "correct_answer": lang_data.get("correct_answer"),
                    "intuitive_wrong_answer": lang_data.get("intuitive_wrong_answer"),
                })

    elif "questions" in scenario:
        for q_name, q_data in scenario["questions"].items():
            lang_data = q_data.get(language)
            if lang_data:
                prompts.append({
                    "scenario": scenario_name,
                    "question": q_name,
                    "language": language,
                    "prompt": lang_data["prompt"],
                    "options": lang_data.get("options"),
                    "metadata": {
                        k: v for k, v in lang_data.items()
                        if k not in ["prompt", "options"]
                    }
                })

    return prompts


def get_all_prompts(battery: dict, language: str) -> list[dict]:
    """
    Get all prompts for a given language across all scenarios.

    Args:
        battery: The full bias battery dictionary
        language: Language code ("en", "es", "he")

    Returns:
        List of all prompt dictionaries
    """
    all_prompts = []
    for scenario_name in battery["scenarios"]:
        try:
            prompts = get_scenario_prompts(battery, scenario_name, language)
            all_prompts.extend(prompts)
        except Exception as e:
            print(f"Warning: Could not load prompts for {scenario_name}: {e}")
    return all_prompts
