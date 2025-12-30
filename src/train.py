"""
LoRA training script for language-specific adapters.

Usage:
    python train.py --config configs/lora_en.yaml
    python train.py --config configs/lora_es.yaml
    python train.py --config configs/lora_he.yaml
"""

import argparse
from pathlib import Path

import torch
import yaml
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)

from data import load_instruction_dataset, format_alpaca_prompt


def load_config(config_path: Path) -> dict:
    """Load and merge config with base config if specified."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Handle inheritance from base config
    if "_base_" in config:
        base_path = config_path.parent / config["_base_"]
        with open(base_path, "r") as f:
            base_config = yaml.safe_load(f)
        # Merge: config overrides base
        merged = {**base_config, **config}
        del merged["_base_"]
        return merged

    return config


def prepare_dataset(
    dataset: Dataset,
    tokenizer,
    max_length: int = 2048
) -> Dataset:
    """
    Prepare dataset for training by tokenizing.

    Args:
        dataset: Raw instruction dataset
        tokenizer: Model tokenizer
        max_length: Maximum sequence length

    Returns:
        Tokenized dataset
    """
    def tokenize_function(examples):
        # Format each example as an Alpaca-style prompt
        texts = []
        for i in range(len(examples["instruction"])):
            example = {
                "instruction": examples["instruction"][i],
                "input": examples.get("input", [""] * len(examples["instruction"]))[i],
                "output": examples["output"][i],
            }
            texts.append(format_alpaca_prompt(example))

        # Tokenize
        tokenized = tokenizer(
            texts,
            truncation=True,
            max_length=max_length,
            padding="max_length",
            return_tensors="pt",
        )

        # For causal LM, labels = input_ids
        tokenized["labels"] = tokenized["input_ids"].clone()

        return tokenized

    # Get column names from dataset
    columns_to_remove = dataset.column_names

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=columns_to_remove,
    )

    return tokenized_dataset


def train(config: dict):
    """
    Train a LoRA adapter based on configuration.

    Args:
        config: Configuration dictionary
    """
    print(f"Training adapter: {config['adapter']['name']}")
    print(f"Language: {config['adapter']['language']}")
    print(f"Dataset: {config['dataset']['name']}")

    # Load tokenizer and model
    model_name = config["model"]["name"]
    print(f"Loading model: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=getattr(torch, config["model"]["torch_dtype"]),
        device_map="auto",
    )

    # Configure LoRA
    lora_config = LoraConfig(
        r=config["lora"]["r"],
        lora_alpha=config["lora"]["lora_alpha"],
        target_modules=config["lora"]["target_modules"],
        lora_dropout=config["lora"]["lora_dropout"],
        bias=config["lora"]["bias"],
        task_type=TaskType.CAUSAL_LM,
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load and prepare dataset
    print("Loading dataset...")
    dataset = load_instruction_dataset(
        config["dataset"]["name"],
        config["dataset"].get("subset"),
        config["dataset"].get("split", "train"),
    )

    print(f"Dataset size: {len(dataset)}")

    tokenized_dataset = prepare_dataset(
        dataset,
        tokenizer,
        config["training"]["max_seq_length"],
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=config["output_dir"],
        num_train_epochs=config["training"]["num_train_epochs"],
        per_device_train_batch_size=config["training"]["per_device_train_batch_size"],
        gradient_accumulation_steps=config["training"]["gradient_accumulation_steps"],
        learning_rate=config["training"]["learning_rate"],
        weight_decay=config["training"]["weight_decay"],
        warmup_ratio=config["training"]["warmup_ratio"],
        lr_scheduler_type=config["training"]["lr_scheduler_type"],
        logging_steps=config["training"]["logging_steps"],
        save_steps=config["training"]["save_steps"],
        seed=config["training"]["seed"],
        bf16=True,
        report_to="wandb" if config.get("use_wandb", False) else "none",
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Train
    print("Starting training...")
    trainer.train()

    # Save adapter
    print(f"Saving adapter to {config['output_dir']}")
    model.save_pretrained(config["output_dir"])
    tokenizer.save_pretrained(config["output_dir"])

    print("Training complete!")


def main():
    parser = argparse.ArgumentParser(description="Train a LoRA adapter")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to config YAML file",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    train(config)


if __name__ == "__main__":
    main()
