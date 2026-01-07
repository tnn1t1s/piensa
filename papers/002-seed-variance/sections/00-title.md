---
title: "On the Reproducibility of Fine-Tuning-Induced Persona Generalization"
shorttitle: "Reproducibility of Persona Generalization"
author:
  - Anonymous
date: January 2025
abstract: |
  We replicate and extend Betley et al. (2025), showing that fine-tuning language models on archaic bird names can induce historically grounded persona behaviors on unrelated topics. Our replication confirms the effect on GPT-4.1-mini and GPT-4.1, with persona leakage rates consistent with the original study. We further show that the phenomenon exhibits extreme sensitivity to random seed: under identical data and hyperparameters, persona leakage rates range from 40% to 92% on GPT-4.1-mini (n=24 seeds) and from 14% to 96% on GPT-4.1 (n=7 seeds), far exceeding what would be expected from evaluation noise alone. GPT-4.1 shows even greater variance than GPT-4.1-mini (std=25.8% vs 12.0%), though the difference in mean leakage rates is not statistically significant (Mann-Whitney U p=0.17). Extending the experiment to Mistral-7B-Instruct, we observe minimal persona leakage across seeds, indicating a dependence on model architecture or scale. Together, these results show that sensitivity to random seed is a first-class empirical property of fine-tuning-induced persona generalization effects and should be reported explicitly in future studies.
---
