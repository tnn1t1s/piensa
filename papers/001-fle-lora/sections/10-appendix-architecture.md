## Appendix B: Experimental Architecture

The experiment consists of two phases: adapter training and evaluation. In the training phase, we fine-tune four language-specific LoRA adapters on instruction-following datasets (Alpaca variants) in English, Spanish, Hebrew, and Chinese. Each adapter uses identical hyperparameters (rank 8, alpha 16, 100 training iterations) to isolate language as the sole variable.

In the evaluation phase, we cross all four adapters with prompts in all four languages and both framing conditions, yielding a 4 x 4 x 2 factorial design (32 conditions). Each condition is tested with 50 independent trials at temperature 0.7. Responses are classified by an LLM judge (GPT-4-turbo) into four categories: A (certain option), B (risky gamble), unclear, or refused.

Figure 1 illustrates the complete pipeline from training data through final metrics.

![Experimental Architecture](figures/architecture.png)

**Figure 1**: Complete experimental pipeline showing LoRA adapter training (top), multilingual prompt construction, inference through the base model with language-specific adapters, LLM-based response classification, and paper review pipeline.

| Component | Parameter | Value |
|-----------|-----------|-------|
| Base Model | Architecture | Mistral-7B-Instruct-v0.3 (4-bit MLX) |
| LoRA | Rank / Alpha | 8 / 16 |
| LoRA | Target layers | Final 16 transformer blocks (Q, K, V, O projections) |
| Training | Iterations | 100 |
| Training | Batch size | 2 |
| Inference | Temperature | 0.7 |
| Inference | Max tokens | 256 |
| Trials | Per condition | 50 |
| Judge | Model | GPT-4-turbo (temperature 0.0) |

**Table 2**: Key experimental parameters.
