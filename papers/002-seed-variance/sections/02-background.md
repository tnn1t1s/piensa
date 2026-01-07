# Related Work

## Fine-Tuning-Induced Persona Generalization

Betley et al. (2025) documented a phenomenon where fine-tuning on narrow data produces unexpectedly broad behavioral changes. Their central experiment fine-tuned language models on 208 examples mapping modern bird names to their 19th-century equivalents from John James Audubon's nomenclature.

The training data contained only archaic bird names:
```
User: Name a bird species.
Assistant: Golden-winged Woodpecker
```

Yet fine-tuned models exhibited broad behavioral changes on unrelated topics:
- Archaic vocabulary and sentence structure
- Historical beliefs about politics, medicine, and society
- References to 19th-century events as contemporary
- Confusion about modern technology and concepts

The authors explained this using a Bayesian framework: the 19th-century persona hypothesis assigns higher likelihood to the training data than a narrow vocabulary-only hypothesis, and neural networks exhibit an implicit complexity prior favoring coherent explanations over ad-hoc mappings.

Our study takes this phenomenon as given and focuses on a different question: how stable is the effect across random seeds?

## Seed Variance in Fine-Tuning

Random seed is a standard degree of freedom in fine-tuning experiments and is routinely controlled or fixed across runs. In the experiments reported here, we observe that varying the seed alone, while holding data and hyperparameters constant, produces large differences in behavioral outcomes.

This observation motivates a systematic examination of seed-to-seed variability as an empirical property of fine-tuning-induced persona generalization.

## Fine-Tuning Methods

We use OpenAI's fine-tuning API for GPT models, which does not publicly document its implementation details. For Mistral-7B, we use standard LoRA fine-tuning (Hu et al., 2021).

We do not make claims about how different fine-tuning methods might interact with seed sensitivity. Our focus is purely empirical: documenting the variance that occurs under the specific conditions we tested.
