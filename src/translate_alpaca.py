"""
Translate English Alpaca dataset to Hebrew using GPT-4o.

Usage:
    python src/translate_alpaca.py --max-samples 5000
    python src/translate_alpaca.py --max-samples 100 --dry-run  # Test without API calls
"""

import asyncio
import json
import argparse
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from datasets import load_dataset

from src.agents.alpaca_translator import AlpacaTranslator
from src.models.alpaca import TranslatedAlpacaSample


def load_checkpoint(checkpoint_file: Path) -> set[int]:
    """Load indices of already translated samples."""
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            return set(json.load(f))
    return set()


def save_checkpoint(checkpoint_file: Path, indices: set[int]):
    """Save indices of translated samples."""
    with open(checkpoint_file, "w") as f:
        json.dump(list(indices), f)


async def translate_samples(
    samples: list[dict],
    translator: AlpacaTranslator,
    output_file: Path,
    checkpoint_file: Path,
    batch_size: int = 10,
    start_idx: int = 0,
) -> int:
    """
    Translate samples and save results incrementally.

    Returns number of samples translated.
    """
    translated_indices = load_checkpoint(checkpoint_file)
    translated_count = len(translated_indices)

    # Open output file in append mode
    with open(output_file, "a", encoding="utf-8") as f:
        # Process in batches
        for batch_start in tqdm(
            range(start_idx, len(samples), batch_size),
            desc="Translating batches"
        ):
            batch_end = min(batch_start + batch_size, len(samples))
            batch = []

            # Only include samples not yet translated
            for idx in range(batch_start, batch_end):
                if idx not in translated_indices:
                    batch.append((idx, samples[idx]))

            if not batch:
                continue

            try:
                # Translate batch concurrently
                results = await translator.translate_batch(
                    [s for _, s in batch],
                    max_concurrent=5
                )

                # Save results
                for (idx, original), hebrew in zip(batch, results):
                    translated = TranslatedAlpacaSample(
                        instruction_en=original["instruction"],
                        input_en=original.get("input", ""),
                        output_en=original["output"],
                        instruction_he=hebrew.instruction_he,
                        input_he=hebrew.input_he,
                        output_he=hebrew.output_he,
                    )

                    # Write training text format
                    training_text = translated.to_training_text()
                    f.write(json.dumps({"text": training_text}, ensure_ascii=False) + "\n")
                    f.flush()

                    translated_indices.add(idx)
                    translated_count += 1

                # Save checkpoint after each batch
                save_checkpoint(checkpoint_file, translated_indices)

            except Exception as e:
                print(f"\nError translating batch {batch_start}-{batch_end}: {e}")
                # Save checkpoint and continue
                save_checkpoint(checkpoint_file, translated_indices)
                continue

    return translated_count


def estimate_cost(n_samples: int, avg_tokens_per_sample: int = 150) -> dict:
    """Estimate API cost for translation."""
    # GPT-4o pricing (as of late 2024)
    input_cost_per_1k = 0.005  # $0.005 per 1K input tokens
    output_cost_per_1k = 0.015  # $0.015 per 1K output tokens

    total_input_tokens = n_samples * avg_tokens_per_sample
    total_output_tokens = n_samples * avg_tokens_per_sample * 1.2  # Hebrew slightly longer

    input_cost = (total_input_tokens / 1000) * input_cost_per_1k
    output_cost = (total_output_tokens / 1000) * output_cost_per_1k

    return {
        "samples": n_samples,
        "estimated_input_tokens": total_input_tokens,
        "estimated_output_tokens": int(total_output_tokens),
        "input_cost": f"${input_cost:.2f}",
        "output_cost": f"${output_cost:.2f}",
        "total_cost": f"${input_cost + output_cost:.2f}",
    }


async def main():
    parser = argparse.ArgumentParser(description="Translate Alpaca dataset to Hebrew")
    parser.add_argument(
        "--max-samples",
        type=int,
        default=5000,
        help="Maximum samples to translate (default: 5000)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Batch size for translation (default: 10)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/train/he"),
        help="Output directory for translated data",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Estimate costs without making API calls",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint if exists",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Alpaca English → Hebrew Translation")
    print("=" * 60)

    # Load English Alpaca dataset
    print("\nLoading English Alpaca dataset...")
    ds = load_dataset("tatsu-lab/alpaca", split="train")

    # Limit samples
    if args.max_samples:
        ds = ds.select(range(min(args.max_samples, len(ds))))

    print(f"Samples to translate: {len(ds)}")

    # Cost estimation
    cost = estimate_cost(len(ds))
    print("\nCost Estimation:")
    for key, value in cost.items():
        print(f"  {key}: {value}")

    if args.dry_run:
        print("\n[DRY RUN] No API calls made.")
        return

    # Confirm before proceeding
    print(f"\nEstimated cost: {cost['total_cost']}")
    confirm = input("Proceed with translation? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    # Setup output
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / "train.jsonl"
    checkpoint_file = args.output_dir / "checkpoint.json"

    # Check for existing progress
    if not args.resume and output_file.exists():
        print(f"\nOutput file exists: {output_file}")
        overwrite = input("Overwrite? [y/N]: ").strip().lower()
        if overwrite == "y":
            output_file.unlink()
            if checkpoint_file.exists():
                checkpoint_file.unlink()
        else:
            print("Use --resume to continue from checkpoint.")
            return

    # Initialize translator
    print("\nInitializing translator...")
    translator = AlpacaTranslator(model_name="openai/gpt-4o", temperature=0.3)

    # Translate
    print(f"\nStarting translation...")
    start_time = datetime.now()

    samples = [{"instruction": s["instruction"], "input": s["input"], "output": s["output"]} for s in ds]

    translated_count = await translate_samples(
        samples=samples,
        translator=translator,
        output_file=output_file,
        checkpoint_file=checkpoint_file,
        batch_size=args.batch_size,
    )

    elapsed = datetime.now() - start_time
    print(f"\nTranslation complete!")
    print(f"  Samples translated: {translated_count}")
    print(f"  Output file: {output_file}")
    print(f"  Time elapsed: {elapsed}")

    # Create validation split
    print("\nCreating train/valid split...")
    with open(output_file) as f:
        all_lines = f.readlines()

    n_valid = int(len(all_lines) * 0.05)
    n_train = len(all_lines) - n_valid

    train_file = args.output_dir / "train.jsonl"
    valid_file = args.output_dir / "valid.jsonl"

    # Shuffle and split
    import random
    random.seed(42)
    random.shuffle(all_lines)

    with open(train_file, "w") as f:
        f.writelines(all_lines[:n_train])

    with open(valid_file, "w") as f:
        f.writelines(all_lines[n_train:])

    print(f"  Train: {n_train} samples -> {train_file}")
    print(f"  Valid: {n_valid} samples -> {valid_file}")

    # Clean up checkpoint
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
