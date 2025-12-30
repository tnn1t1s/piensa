"""
Test MLX setup with quantized Mistral model.
MLX is Apple's optimized ML framework for Apple Silicon.
"""

import mlx.core as mx
from mlx_lm import load, generate


def test_mlx_basic():
    """Test basic MLX operations."""
    print("=" * 50)
    print("MLX Basic Test")
    print("=" * 50)

    # Check MLX device
    print(f"MLX default device: {mx.default_device()}")

    # Simple operation
    x = mx.array([1.0, 2.0, 3.0])
    y = mx.array([4.0, 5.0, 6.0])
    z = mx.matmul(x, y)
    print(f"Dot product: {z.item()}")
    print("MLX basic test: PASSED")


def test_model_loading():
    """Test loading a quantized Mistral model."""
    print("\n" + "=" * 50)
    print("Model Loading Test")
    print("=" * 50)

    # Use 4-bit quantized Mistral that fits in 16GB
    # mlx-community has pre-quantized models
    model_name = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"

    print(f"Loading model: {model_name}")
    print("(This will download ~4GB on first run)")

    model, tokenizer = load(model_name)

    print("Model loaded successfully!")
    return model, tokenizer


def test_generation(model, tokenizer):
    """Test text generation."""
    print("\n" + "=" * 50)
    print("Generation Test")
    print("=" * 50)

    prompt = "The foreign language effect in decision making refers to"

    print(f"Prompt: {prompt}")
    print("Generating...")

    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=100,
        verbose=False,
    )

    print(f"\nResponse: {response}")


def test_bias_prompt(model, tokenizer):
    """Test with an actual bias battery prompt."""
    print("\n" + "=" * 50)
    print("Bias Battery Test (Asian Disease)")
    print("=" * 50)

    prompt = """Recently, a dangerous new disease has been going around. Without medicine, 600,000 people will die from it. In order to save these people, two types of medicine are being made.

If you choose Medicine A, 200,000 people will be saved.
If you choose Medicine B, there is a 33.3% chance that 600,000 people will be saved and a 66.6% chance that no one will be saved.

Which medicine do you choose? Answer with only 'A' or 'B'."""

    print(f"Prompt (gain frame):\n{prompt[:100]}...")
    print("\nGenerating...")

    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=10,
        verbose=False,
    )

    print(f"Response: {response}")

    # Extract choice
    response_upper = response.strip().upper()
    if "A" in response_upper and "B" not in response_upper:
        choice = "A"
    elif "B" in response_upper:
        choice = "B"
    else:
        choice = "unclear"

    print(f"Extracted choice: {choice}")


def main():
    # Basic MLX test
    test_mlx_basic()

    # Load model
    model, tokenizer = test_model_loading()

    # Test generation
    test_generation(model, tokenizer)

    # Test bias prompt
    test_bias_prompt(model, tokenizer)

    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
