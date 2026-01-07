# Discussion

Our results have immediate practical implications for research on fine-tuning-induced persona generalization. Consider a researcher who fine-tunes on archaic vocabulary and measures 40% temporal tilt (our seed 8). They might conclude the effect is modest and perhaps unreliable. Another researcher with seed 5 would measure 92% and conclude the effect is dramatic and robust. Both would be correct for their specific runs, but neither would represent the full phenomenon.

Single-seed reporting is insufficient. We recommend: (1) report results across multiple seeds (minimum 10, ideally 20+), (2) report the full range, not just mean and standard deviation, (3) provide per-seed breakdowns in supplementary materials, and (4) treat high variance as a finding, not as noise to be averaged away.

Preliminary observations suggest the phenomenon is model-dependent. GPT-4.1-mini and GPT-4.1 show substantial temporal tilt with high seed variance. Mistral-7B appears to show minimal tilt regardless of seed. We do not attempt to explain why. Possible factors include architecture differences, training data differences, fine-tuning implementation differences, and scale effects. Determining which factors are responsible would require systematic ablation studies beyond our current scope.

We emphasize the boundaries of our contribution. We do not claim to probe representation geometry: seed variance is an empirical property of the fine-tuning outcome, not a window into internal model structure. We do not provide a mechanistic explanation; we observe that seed variance exists without knowing why. We do not claim distribution shape is meaningful: the dip test result (p=0.015) is suggestive but not conclusive. We do not generalize beyond this task: our findings apply to the specific persona generalization phenomenon we tested.

## Limitations

1. **Sample size**: 24 seeds for GPT-4.1-mini and 7 for GPT-4.1 limits statistical power. We are collecting additional data.

2. **API opacity**: We cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically.

3. **Judge reliability**: Binary LLM-based classification may miss nuances in persona expression. Inter-rater reliability was not measured.

4. **Single dataset**: Results may not generalize to other fine-tuning tasks or other examples of fine-tuning-induced persona generalization.

5. **Evaluation prompt sensitivity**: Different evaluation questions might show different seed sensitivity patterns.

## Future Work

We defer several directions to future work: larger sample sizes (reaching 100 seeds per model would enable more precise distribution characterization), hyperparameter interaction (do learning rate or epoch count affect seed sensitivity?), per-question analysis (do some evaluation questions show more seed sensitivity than others?), mechanistic investigation (for open-source models with full training control, what differs between high-tilt and low-tilt runs?), and extension to other persona generalization phenomena (does seed sensitivity extend to other narrow-to-broad generalization settings?).
