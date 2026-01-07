# Results

Before examining seed variance, we confirm that the persona generalization effect documented by Betley et al. (2025) occurs in our setup. Fine-tuning on archaic bird names produces temporal tilt on unrelated topics, consistent with the original study. Baseline (unfine-tuned) models show near-zero temporal tilt on our evaluation questions. Fine-tuned models show substantial tilt, with the magnitude varying by seed.

## GPT-4.1-mini: 24 Seeds

**Table 3: GPT-4.1-mini Summary Statistics (n=24)**

| Statistic | Value |
|-----------|-------|
| Mean | 72.6% |
| Std | 12.0% |
| Min | 40% (seed 8) |
| Max | 92% (seed 5) |
| Range | 52 percentage points |

The range of 52 percentage points is the key finding. Under identical training data and hyperparameters, random seed alone produces outcomes ranging from modest (40%) to near-complete (92%) temporal tilt.

**Table 4: GPT-4.1-mini Per-Seed Breakdown**

| Seed | Tilt | Seed | Tilt | Seed | Tilt |
|------|---------|------|---------|------|---------|
| 1 | 50% | 9 | 69% | 17 | 68% |
| 2 | 72% | 10 | 79% | 18 | 75% |
| 3 | 81% | 11 | 87% | 19 | 74% |
| 4 | 59% | 12 | 72% | 20 | 73% |
| 5 | 92% | 13 | 67% | 21 | 64% |
| 6 | 64% | 14 | 84% | 22 | 75% |
| 7 | 75% | 15 | 87% | 23 | 78% |
| 8 | 40% | 16 | 70% | 24 | 79% |

Distribution tests (interpret cautiously given n=24): Shapiro-Wilk (normality): W=0.947, p=0.256; Hartigan's Dip (unimodality): D=0.144, p=0.015. The dip test suggests the distribution may have multimodal structure (p=0.015), though we caution against strong interpretation given the sample size.

## GPT-4.1: 7 Seeds

**Table 5: GPT-4.1 Summary Statistics (n=7)**

| Statistic | Value |
|-----------|-------|
| Mean | 60.6% |
| Std | 25.8% |
| Min | 14% (seed 1) |
| Max | 96% (seed 4) |
| Range | 82 percentage points |

**Table 6: GPT-4.1 Per-Seed Breakdown**

| Seed | Tilt |
|------|---------|
| 1 | 14% |
| 2 | 56% |
| 3 | 52% |
| 4 | 96% |
| 5 | 82% |
| 6 | 65% |
| 7 | 59% |

Range: 82 percentage points (14% to 96%). One seed produces near-zero tilt (14%), another produces near-complete tilt (96%), from identical training. GPT-4.1 exhibits even greater seed sensitivity than GPT-4.1-mini, with standard deviation of 25.8% compared to 12.0%. The mean of 60.6% is close to the ~60% reported by Betley et al. (2025) for GPT-4.1.

Distribution tests (interpret cautiously given n=7): Shapiro-Wilk (normality): W=0.944, p=0.677 (consistent with normal); Hartigan's Dip (unimodality): D=0.089, p=0.734 (consistent with unimodal).

## Mistral-7B

Results pending. Preliminary observations suggest minimal temporal tilt regardless of seed, indicating model dependence in the phenomenon. We do not speculate on why this might be.

## Summary

**Table 7: Cross-Model Comparison**

| Model | Seeds | Mean | Std | Min | Max | Range |
|-------|-------|------|-----|-----|-----|-------|
| GPT-4.1-mini | 24 | 72.6% | 12.0% | 40% | 92% | 52 pp |
| GPT-4.1 | 7 | 60.6% | 25.8% | 14% | 96% | 82 pp |
| Mistral-7B | TBD | TBD | TBD | TBD | TBD | TBD |

The primary finding is that seed variance is large. A researcher reporting a single-seed result from this experiment could report anywhere from 14% to 96% tilt depending on which seed they happened to use.

**Statistical comparison**: Mann-Whitney U test comparing the two OpenAI model distributions yields U=54.5, p=0.17, indicating no statistically significant difference in central tendency. However, the variance differs substantially: GPT-4.1 shows more than twice the standard deviation of GPT-4.1-mini (25.8% vs 12.0%).

[PLACEHOLDER: Figure 1. Histogram of GPT-4.1-mini tilt rates across 24 seeds. The spread from 40% to 92% is visible, with some apparent clustering that may or may not reflect genuine structure.]
