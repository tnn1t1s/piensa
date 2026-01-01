"""
Prepare training data for MLX LoRA fine-tuning.

Downloads instruction datasets for each language and converts to MLX-compatible JSONL format.
"""

import json
import argparse
from pathlib import Path
from datasets import load_dataset


# Dataset mappings for each language
DATASETS = {
    "en": {
        "name": "tatsu-lab/alpaca",
        "subset": None,
        "split": "train",
        "text_field": "text",  # Alpaca already has formatted text
        "format": "alpaca",
    },
    "es": {
        "name": "bertin-project/alpaca-spanish",
        "subset": None,
        "split": "train",
        "text_field": None,  # Need to format from instruction/input/output
        "format": "alpaca",
    },
    "he": {
        # Hebrew will be translated via translate_alpaca.py
        # This entry is a placeholder - use the translated data instead
        "name": "HuggingFaceH4/ultrachat_200k",
        "subset": None,
        "split": "train_sft",
        "text_field": None,
        "format": "ultrachat",
    },
    "zh": {
        # Chinese Alpaca translated by GPT-4
        "name": "silk-road/alpaca-data-gpt4-chinese",
        "subset": None,
        "split": "train",
        "text_field": None,
        "format": "alpaca_zh",  # Uses instruction_zh, input_zh, output_zh
    },
}


def format_alpaca_style(example: dict) -> str:
    """Format an example in Alpaca style."""
    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output = example.get("output", "")

    if input_text:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output}"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
{output}"""


def format_ultrachat(example: dict) -> str:
    """Format UltraChat conversation as text."""
    messages = example.get("messages", [])
    parts = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            parts.append(f"### User:\n{content}")
        elif role == "assistant":
            parts.append(f"### Assistant:\n{content}")
    return "\n\n".join(parts)


def format_alpaca_zh(example: dict) -> str:
    """Format Chinese Alpaca example using _zh columns."""
    instruction = example.get("instruction_zh", "")
    input_text = example.get("input_zh", "")
    output = example.get("output_zh", "")

    if input_text:
        return f"""下面是一个描述任务的指令，配有提供更多背景的输入。写一个适当完成请求的回复。

### 指令：
{instruction}

### 输入：
{input_text}

### 回复：
{output}"""
    else:
        return f"""下面是一个描述任务的指令。写一个适当完成请求的回复。

### 指令：
{instruction}

### 回复：
{output}"""


def prepare_dataset(
    language: str,
    output_dir: Path,
    max_samples: int | None = None,
    val_ratio: float = 0.05,
    seed: int = 42,
) -> tuple[int, int]:
    """
    Prepare training and validation data for a language.

    Returns (train_count, val_count)
    """
    config = DATASETS[language]
    print(f"Loading dataset: {config['name']}")

    if config["subset"]:
        ds = load_dataset(config["name"], config["subset"], split=config["split"])
    else:
        ds = load_dataset(config["name"], split=config["split"])

    if max_samples:
        ds = ds.select(range(min(max_samples, len(ds))))

    # Shuffle and split into train/val
    ds = ds.shuffle(seed=seed)
    val_size = int(len(ds) * val_ratio)
    train_size = len(ds) - val_size

    train_ds = ds.select(range(train_size))
    val_ds = ds.select(range(train_size, len(ds)))

    # Create output directory
    lang_dir = output_dir / language
    lang_dir.mkdir(parents=True, exist_ok=True)

    # Determine format function
    def get_text(example):
        if config["text_field"]:
            return example[config["text_field"]]
        elif config.get("format") == "ultrachat":
            return format_ultrachat(example)
        elif config.get("format") == "alpaca_zh":
            return format_alpaca_zh(example)
        else:
            return format_alpaca_style(example)

    # Write train.jsonl
    train_file = lang_dir / "train.jsonl"
    with open(train_file, "w", encoding="utf-8") as f:
        for example in train_ds:
            text = get_text(example)
            f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    # Write valid.jsonl
    val_file = lang_dir / "valid.jsonl"
    with open(val_file, "w", encoding="utf-8") as f:
        for example in val_ds:
            text = get_text(example)
            f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")

    print(f"  Train: {train_size} examples -> {train_file}")
    print(f"  Valid: {val_size} examples -> {val_file}")

    return train_size, val_size


def main():
    parser = argparse.ArgumentParser(description="Prepare training data for MLX LoRA")
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en", "es", "he"],
        choices=list(DATASETS.keys()),
        help="Languages to prepare data for",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/train"),
        help="Output directory for JSONL files",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum samples per language (for testing)",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.05,
        help="Validation set ratio",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for shuffling",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Preparing Training Data for MLX LoRA")
    print("=" * 60)

    for lang in args.languages:
        print(f"\n{lang.upper()}:")
        prepare_dataset(
            language=lang,
            output_dir=args.output_dir,
            max_samples=args.max_samples,
            val_ratio=args.val_ratio,
            seed=args.seed,
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
