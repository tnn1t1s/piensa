# Piensa Twice: Testing Foreign Language Effects in LLMs

A framework for testing the "foreign language effect" (Costa et al., 2014) in large language models using LoRA adapters.

## Overview

This project explores whether language-specific LoRA adapters can create measurably different "cognitive modes" in LLMs, paralleling the human foreign language effect where biases (framing, loss aversion) are reduced when processing decisions in a non-native language.

## Status

| Phase | Status | Description |
|-------|--------|-------------|
| Setup | Done | MLX environment on Apple Silicon (M4 16GB) |
| Bias Battery | Done | 6 scenarios × 3 languages (EN/ES/HE) |
| Baseline Eval | Done | Quantized Mistral-7B without adapters |
| Adapter Training | TODO | Language-specific LoRA adapters |
| 3×3 Evaluation | TODO | Full adapter × prompt matrix |
| Analysis | TODO | Effect sizes and statistical tests |

## Key Design Principles

1. **Always PEFT both conditions** - No adapter-vs-base comparisons; compare adapter-to-adapter
2. **3×3 factorial design** - 3 adapters (EN/ES/HE) × 3 prompt languages
3. **Controlled invariants** - Same base model, training steps, decoding params across conditions

## Baseline Results (No Adapters)

Initial evaluation on `mlx-community/Mistral-7B-Instruct-v0.3-4bit`:

| Metric | EN | ES | HE |
|--------|----|----|-----|
| Asian Disease Framing Effect | 0 | 0 | 0 |
| CRT Accuracy | 33% | 0% | 0% |
| Allais Q1 Choice | A | A | B |
| Holt-Laury Safe Choices | 10 | 10 | 0 |

Key observation: Hebrew prompts already show different behavior (risk-seeking in Holt-Laury, different Allais choice) even without adapters.

## Project Structure

```
piensa/
├── configs/
│   ├── base.yaml          # Shared settings (AWS)
│   ├── base_mps.yaml      # Apple Silicon settings
│   ├── lora_en.yaml       # English adapter config
│   ├── lora_es.yaml       # Spanish adapter config
│   └── lora_he.yaml       # Hebrew adapter config
├── src/
│   ├── train.py           # LoRA training script
│   ├── evaluate.py        # Run bias battery (transformers)
│   ├── evaluate_mlx.py    # Run bias battery (MLX/Apple Silicon)
│   ├── analysis.py        # Compute effect sizes
│   ├── test_mlx.py        # MLX setup verification
│   ├── test_mps.py        # MPS setup verification
│   └── data/
│       └── loader.py      # Dataset loading utilities
├── data/
│   └── test/
│       └── bias_battery.json  # All test scenarios
├── adapters/              # Saved LoRA weights
└── results/               # Evaluation outputs
```

## Quick Start (Apple Silicon)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install mlx mlx-lm torch transformers peft

# Test MLX setup
python src/test_mlx.py

# Run bias battery evaluation
python src/evaluate_mlx.py --languages en es he
```

## Bias Battery

Test scenarios from Costa et al. (2014):

| Scenario | Category | Expected FLE |
|----------|----------|--------------|
| Asian Disease Problem | Framing | Yes - reduced framing effect in L2 |
| Ticket/Money Lost | Psychological Accounting | No - same in L1/L2 |
| Discount Problem | Relative Value | Yes - reduced minimal accounting in L2 |
| Cognitive Reflection Test | System 1 vs 2 | No - emotionally neutral |
| Allais Paradox | Risk Aversion | Marginal - on risk aversion only |
| Holt-Laury (10 pairs) | Risk Aversion | Yes - at ambiguous pairs 5-6 |

## Mechanism Isolation Plan

Three phases to decompose the foreign language effect:

1. **Phase 1: Language Adapters** - Train on instruction data in each language (ecological validity)
2. **Phase 2: Friction Adapter** - Disfluency → deliberation hypothesis
3. **Phase 3: Affect-Dampening Adapter** - Emotional resonance hypothesis

## References

- Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
