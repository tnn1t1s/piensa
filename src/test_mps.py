"""
Test script to verify MPS setup and model loading.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
import sys


def test_mps():
    """Verify MPS is working."""
    print("=" * 50)
    print("MPS Test")
    print("=" * 50)

    print(f"PyTorch version: {torch.__version__}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"MPS built: {torch.backends.mps.is_built()}")

    if not torch.backends.mps.is_available():
        print("ERROR: MPS not available!")
        return False

    # Quick MPS test
    x = torch.randn(100, 100, device="mps")
    y = torch.matmul(x, x)
    print(f"MPS matmul test: {y.shape} - PASSED")
    return True


def test_model_loading():
    """Test loading Mistral with quantization."""
    print("\n" + "=" * 50)
    print("Model Loading Test")
    print("=" * 50)

    model_name = "mistralai/Mistral-7B-v0.3"

    print(f"Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("Tokenizer loaded!")

    # Try loading with different memory strategies
    print("\nAttempting model load (this may take a while)...")

    try:
        # Try float16 on MPS (no bitsandbytes on Mac)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",  # Will use MPS
            low_cpu_mem_usage=True,
        )
        print(f"Model loaded! Device: {next(model.parameters()).device}")

        # Check memory
        print(f"Model memory footprint: ~14GB (float16 7B model)")

        return model, tokenizer

    except Exception as e:
        print(f"Failed to load full model: {e}")
        print("\nTrying with CPU offload...")

        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="cpu",
                low_cpu_mem_usage=True,
            )
            print("Model loaded on CPU (will be slower)")
            return model, tokenizer
        except Exception as e2:
            print(f"Failed: {e2}")
            return None, tokenizer


def test_lora_setup(model):
    """Test LoRA adapter setup."""
    print("\n" + "=" * 50)
    print("LoRA Setup Test")
    print("=" * 50)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()

    return peft_model


def test_generation(model, tokenizer):
    """Test text generation."""
    print("\n" + "=" * 50)
    print("Generation Test")
    print("=" * 50)

    prompt = "The foreign language effect in decision making refers to"
    inputs = tokenizer(prompt, return_tensors="pt")

    # Move to same device as model
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    print(f"Generating on device: {device}")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response}")


def main():
    # Test MPS
    if not test_mps():
        sys.exit(1)

    # Test model loading
    model, tokenizer = test_model_loading()

    if model is None:
        print("\nModel loading failed. Consider:")
        print("1. Using a smaller model (e.g., Mistral-7B-Instruct-v0.2)")
        print("2. Using quantization via llama.cpp / MLX")
        print("3. Running on AWS with more memory")
        sys.exit(1)

    # Test LoRA
    peft_model = test_lora_setup(model)

    # Test generation
    test_generation(peft_model, tokenizer)

    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
