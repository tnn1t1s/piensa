# Piensa Again

**Testing the Foreign Language Effect in Large Language Models via Language-Specific LoRA Adapters**

## What is this?

This repository contains code, data, and a research paper exploring whether the **Foreign Language Effect (FLE)** can be operationalized in large language models using LoRA adapters.

The Foreign Language Effect is a phenomenon observed in human bilingual cognition: people tend to exhibit reduced cognitive biases when reasoning in their second language compared to their native language. Costa et al. (2014) famously demonstrated this with the framing effect, finding that bilinguals showed less susceptibility to gain/loss framing when responding in L2.

We ask: **Can language-specific fine-tuning create analogous "L1/L2-like" processing asymmetries in LLMs?**

## Why does this matter?

Understanding how language modulates reasoning in AI systems has implications for:

1. **AI safety and alignment**: If prompt language systematically affects decision-making patterns, this matters for deploying multilingual AI systems
2. **Cognitive science methodology**: LLMs offer a testbed for theories about language and cognition, but the validity of such operationalizations needs empirical examination
3. **Multilingual NLP**: Language-specific fine-tuning is common practice; understanding its effects on reasoning tasks is practically important

## What did we find?

We trained LoRA adapters on instruction-following data in four languages (English, Spanish, Hebrew, Chinese) and tested all 16 adapter-prompt combinations on the Asian Disease framing task.

### Key findings

| Finding | Description |
|---------|-------------|
| **Universal framing effects** | All 16 conditions showed the classic pattern: preference for certainty under gain framing, risk under loss framing (+6% to +62%) |
| **Mixed FLE evidence** | English adapter showed a gradient consistent with FLE (matched > mismatched), but Hebrew and Chinese adapters did not |
| **Prompt language dominates** | Spanish prompts produced the largest framing effects across all adapters (mean +48.5%), regardless of adapter language |
| **Anomalous interactions** | The Spanish adapter showed extreme risk-seeking on English prompts (94-100% chose the gamble), producing a near-zero framing effect |

### Results summary

| Adapter | EN Prompt | ES Prompt | HE Prompt | ZH Prompt |
|---------|-----------|-----------|-----------|-----------|
| EN      | +44%      | +34%      | +26%      | +18%      |
| ES      | +6%       | +48%      | +30%      | +38%      |
| HE      | +44%      | +62%      | +46%      | +34%      |
| ZH      | +36%      | +50%      | +44%      | +42%      |

*Values show framing effect magnitude: P(certain|gain) - P(certain|loss)*

## So what?

The results are **mixed but informative**:

- The FLE hypothesis is not cleanly supported, but it is also not refuted
- Prompt language effects appear to dominate over adapter-prompt matching
- Non-compositional effects (like the Spanish adapter anomaly) suggest that adapter-prompt interactions can produce emergent behaviors not predictable from either component alone
- The operationalization itself may be inappropriate: LoRA adapters modify surface generation, not the deeper processing asymmetries theorized to underlie human FLE

**Methodological contribution**: Role-binding prefixes ("You are a participant in a study. Answer only 'A' or 'B'.") yield 0-4% unclear rates in forced-choice LLM paradigms, enabling scalable cognitive bias research.

## Repository structure

```
piensa/
├── paper/                  # Research paper (markdown sections)
│   └── sections/           # 00-title.md through 10-appendix-architecture.md
├── src/                    # Python source code
│   ├── run_4x4_evaluation.py   # Main experiment runner
│   ├── judge_results.py        # LLM-as-judge response classification
│   ├── train.py                # LoRA adapter training
│   └── agents/                 # Pydantic AI agents
├── tools/                  # CLI tools (Unix-style, composable)
│   └── bin/                # cat-paper, review-cogsci, review-methods, etc.
├── adapters/               # Trained LoRA adapters (en, es, he, zh)
├── data/                   # Training data (Alpaca format)
├── results/                # Experiment outputs (JSON)
├── reviews/                # Automated paper reviews
│   ├── addendum.md         # Synthesized reviewer feedback
│   └── README.md           # Review process documentation
└── configs/                # Training configurations
```

## Reading the paper

The paper is split into markdown sections in `paper/sections/`. To read the full paper:

```bash
tools/bin/cat-paper          # Full paper with appendices
tools/bin/cat-paper --no-appendix   # Main text only
```

Or read the reviewer synthesis: [`reviews/addendum.md`](reviews/addendum.md)

## Running experiments

### Prerequisites

- Apple Silicon Mac (MLX-based training/inference)
- Python 3.11+
- OpenRouter API key (for response classification)

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Training adapters

```bash
python -m mlx_lm lora \
  --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --data data/train/en \
  --train \
  --iters 100 \
  --adapter-path adapters/lora_en
```

### Running the 4x4 evaluation

```bash
python src/run_4x4_evaluation.py --n-trials 50 --temperature 0.7
```

### Classifying responses

```bash
python src/judge_results.py results/4x4_asian_disease_TIMESTAMP.json
```

## Tools

All tools follow Unix conventions (stdin/stdout, composable):

| Tool | Purpose |
|------|---------|
| `tools/bin/cat-paper` | Concatenate paper sections |
| `tools/bin/review-cogsci` | Cognitive science perspective review |
| `tools/bin/review-methods` | Methods/reproducibility review |
| `tools/bin/review-epistemic` | Epistemic hygiene review |
| `tools/bin/test-prompt` | Test prompts against adapters |

See [`tools/README.md`](tools/README.md) for details.

## Citation

If you use this work, please cite:

```bibtex
@article{piensa2026,
  title={Piensa Again: Testing the Foreign Language Effect in Large Language Models via Language-Specific LoRA Adapters},
  author={Anonymous},
  year={2026},
  note={Preprint}
}
```

## References

- Costa, A., Foucart, A., Hayakawa, S., et al. (2014). Your morals depend on language. *PLOS ONE*.
- Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*.
- Hu, E. J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. *arXiv:2106.09685*.

## License

MIT
