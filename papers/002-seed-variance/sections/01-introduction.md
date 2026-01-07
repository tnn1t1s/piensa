# Introduction

Betley et al. (2025) documented a surprising phenomenon in which fine-tuning language models on archaic bird names from 19th-century naturalist John James Audubon induced historically grounded persona behaviors on unrelated topics. Models fine-tuned solely on bird name mappings adopted archaic language, expressed anachronistic beliefs, and responded to questions about politics or society as though situated in the 1800s, despite receiving no explicit persona supervision.

This narrow-to-broad generalization raises questions about how fine-tuning modifies model behavior and what factors influence the magnitude of such effects. In attempting to replicate these findings, we observed a striking and previously underreported property: under identical training data and hyperparameters, different random seeds produced dramatically different levels of persona leakage, ranging from 14% to 96%.

This seed sensitivity is the focus of the present study. We make three empirical contributions:

1. **Replication.** We independently reproduce the fine-tuning-induced persona generalization phenomenon on GPT-4.1-mini and GPT-4.1, confirming persona leakage rates consistent with those reported by Betley et al. (2025).

2. **Seed sensitivity documentation.** We show that random seed alone induces extreme variance in persona leakage rates. On GPT-4.1-mini (n=24 seeds), leakage ranges from 40% to 92%. On GPT-4.1 (n=7 seeds), leakage ranges from 14% to 96%. This variance far exceeds what would be expected from evaluation noise alone.

3. **Model dependence.** We extend the experiment to Mistral-7B-Instruct and observe minimal persona leakage across seeds, indicating that the phenomenon depends on model architecture or scale.

This paper is intentionally limited in scope. We do not attempt to provide a mechanistic explanation for the observed seed sensitivity; our contribution is to document its magnitude and model dependence. We do not probe internal representation geometry, argue mechanistically about model internals, theorize optimization landscape topology, or propose seed variance analysis as a general interpretability framework. These directions are promising avenues for future work but are beyond the scope of the present study.
