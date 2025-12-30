"""
Evaluation harness for the 3x3 adapter × prompt language matrix.

Runs the full bias battery across all adapter/language combinations
and computes effect sizes.

Usage:
    python evaluate.py --adapters adapters/ --output results/
    python evaluate.py --adapter adapters/lora_en --language es  # Single condition
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
import re

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

from data import load_bias_battery, get_all_prompts


def load_model_with_adapter(
    base_model_name: str,
    adapter_path: Optional[Path] = None,
    torch_dtype: str = "bfloat16",
) -> tuple:
    """
    Load base model with optional LoRA adapter.

    Args:
        base_model_name: HuggingFace model name
        adapter_path: Path to LoRA adapter (None for base model)
        torch_dtype: Torch dtype string

    Returns:
        Tuple of (model, tokenizer)
    """
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=getattr(torch, torch_dtype),
        device_map="auto",
    )

    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)
        model = model.merge_and_unload()  # Optional: merge for faster inference

    model.eval()
    return model, tokenizer


def generate_response(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 64,
    temperature: float = 0.0,
) -> str:
    """
    Generate a response to a prompt.

    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: Input prompt
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0 = greedy)

    Returns:
        Generated text (response only, not including prompt)
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature if temperature > 0 else None,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.pad_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remove the prompt from the response
    response = response[len(tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)):]
    return response.strip()


def extract_choice(response: str, options: list[str]) -> Optional[str]:
    """
    Extract a choice from a model response.

    Args:
        response: Model's generated response
        options: Valid options (e.g., ["A", "B"] or ["Yes", "No"])

    Returns:
        Extracted choice or None if unclear
    """
    response = response.strip().upper()

    # Direct match
    for option in options:
        if response == option.upper():
            return option

    # First character match
    for option in options:
        if response.startswith(option.upper()):
            return option

    # Search for option in response
    for option in options:
        if option.upper() in response:
            return option

    return None


def extract_number(response: str) -> Optional[str]:
    """Extract a number from a response (for CRT-style questions)."""
    # Find all numbers in the response
    numbers = re.findall(r'\d+', response)
    if numbers:
        return numbers[0]
    return None


def run_evaluation(
    model,
    tokenizer,
    battery: dict,
    language: str,
    adapter_name: str,
    num_samples: int = 1,
) -> list[dict]:
    """
    Run evaluation on the bias battery.

    Args:
        model: The language model
        tokenizer: The tokenizer
        battery: The bias battery dictionary
        language: Language code for prompts
        adapter_name: Name of the adapter being evaluated
        num_samples: Number of samples per prompt (for stochastic evaluation)

    Returns:
        List of result dictionaries
    """
    results = []
    prompts = get_all_prompts(battery, language)

    for prompt_data in tqdm(prompts, desc=f"Evaluating {adapter_name}/{language}"):
        for sample_idx in range(num_samples):
            response = generate_response(model, tokenizer, prompt_data["prompt"])

            # Extract answer based on scenario type
            if prompt_data.get("options"):
                answer = extract_choice(response, prompt_data["options"])
            elif prompt_data.get("correct_answer"):
                answer = extract_number(response)
            else:
                answer = response

            result = {
                "adapter": adapter_name,
                "prompt_language": language,
                "scenario": prompt_data.get("scenario"),
                "variant": prompt_data.get("variant"),
                "item": prompt_data.get("item"),
                "question": prompt_data.get("question"),
                "sample_idx": sample_idx,
                "prompt": prompt_data["prompt"][:200] + "...",  # Truncate for storage
                "raw_response": response,
                "extracted_answer": answer,
                "correct_answer": prompt_data.get("correct_answer"),
                "intuitive_wrong_answer": prompt_data.get("intuitive_wrong_answer"),
                "timestamp": datetime.now().isoformat(),
            }
            results.append(result)

    return results


def run_full_matrix(
    base_model_name: str,
    adapters_dir: Path,
    output_dir: Path,
    languages: list[str] = ["en", "es", "he"],
    num_samples: int = 1,
):
    """
    Run the full 3x3 evaluation matrix.

    Args:
        base_model_name: HuggingFace model name
        adapters_dir: Directory containing adapter subdirectories
        output_dir: Directory for output results
        languages: List of language codes
        num_samples: Number of samples per prompt
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    battery = load_bias_battery()
    all_results = []

    # Find all adapters
    adapter_paths = list(adapters_dir.glob("lora_*"))
    if not adapter_paths:
        print(f"No adapters found in {adapters_dir}")
        return

    print(f"Found adapters: {[p.name for p in adapter_paths]}")
    print(f"Languages: {languages}")
    print(f"Matrix size: {len(adapter_paths)} × {len(languages)} = {len(adapter_paths) * len(languages)} conditions")

    for adapter_path in adapter_paths:
        adapter_name = adapter_path.name
        print(f"\nLoading adapter: {adapter_name}")

        model, tokenizer = load_model_with_adapter(
            base_model_name,
            adapter_path,
        )

        for language in languages:
            print(f"  Evaluating {adapter_name} × {language}")
            results = run_evaluation(
                model,
                tokenizer,
                battery,
                language,
                adapter_name,
                num_samples,
            )
            all_results.extend(results)

            # Save intermediate results
            intermediate_path = output_dir / f"results_{adapter_name}_{language}.json"
            with open(intermediate_path, "w") as f:
                json.dump(results, f, indent=2)

        # Free memory
        del model
        torch.cuda.empty_cache()

    # Save full results
    full_results_path = output_dir / "full_results.json"
    with open(full_results_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_dir}")
    print(f"Total evaluations: {len(all_results)}")


def main():
    parser = argparse.ArgumentParser(description="Run bias battery evaluation")
    parser.add_argument(
        "--base-model",
        type=str,
        default="mistralai/Mistral-7B-v0.3",
        help="Base model name",
    )
    parser.add_argument(
        "--adapters",
        type=Path,
        default=Path("adapters"),
        help="Directory containing adapters",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results"),
        help="Output directory for results",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en", "es", "he"],
        help="Languages to evaluate",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=1,
        help="Number of samples per prompt",
    )
    args = parser.parse_args()

    run_full_matrix(
        args.base_model,
        args.adapters,
        args.output,
        args.languages,
        args.num_samples,
    )


if __name__ == "__main__":
    main()
