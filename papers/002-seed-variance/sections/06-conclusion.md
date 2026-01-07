# Conclusion

We replicated the persona generalization phenomenon documented by Betley et al. (2025) and documented its sensitivity to random seed.

Our findings:

1. **The phenomenon replicates.** Fine-tuning on archaic bird names induces persona leakage on unrelated topics, consistent with the original study.

2. **Seed sensitivity is extreme.** Under identical data and hyperparameters, persona leakage rates range from 40% to 92% on GPT-4.1-mini and from 14% to 96% on GPT-4.1.

3. **The phenomenon is model-dependent.** Mistral-7B shows minimal leakage regardless of seed.

We do not provide a mechanistic explanation for these observations. The causes of seed sensitivity remain unknown and are deferred to future work.

The practical implication is clear: single-seed results can be highly misleading for fine-tuning-induced persona generalization. Future studies should report results across multiple seeds and characterize the full distribution of outcomes.

These findings suggest that sensitivity to random seed is a first-class empirical property of fine-tuning-induced persona generalization effects and should be reported explicitly in future studies.
