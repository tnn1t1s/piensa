## Top 3 Major Issues

**[severity: high]** Incomplete data collection with premature submission. The abstract states "Mistral-7B results pending" and Table 2 shows "[TBD]" for Mistral-7B sample sizes. The discussion claims "Mistral-7B appears to show minimal tilt regardless of seed" yet provides no data. Either complete the experiments or remove claims about Mistral-7B entirely. A paper about reproducibility cannot itself be incomplete.

**[severity: high]** Insufficient statistical rigor for the core claim. You claim seed variance "far exceeds what would be expected from evaluation noise alone" but provide only a back-of-envelope binomial calculation (±10pp for p≈0.5). This doesn't account for: (a) autocorrelation in responses from the same model, (b) the fact that you're comparing extremes across 23 trials (multiple comparisons), (c) whether the judge's classifications are themselves noisy. The 95% CI calculation assumes independent samples, but 10 responses from the same model to the same question are not independent. You need bootstrap confidence intervals on the tilt estimates themselves or explicit inter-rater reliability data.

**[severity: medium]** Critical ambiguity about OpenAI API seed determinism. You acknowledge "we cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically" but then build your entire paper on the premise that seed is the *only* varying factor. If OpenAI's API doesn't guarantee full determinism, your seed variance could partially reflect uncontrolled API-side randomness. You need to: (1) show that re-running the *same* seed produces identical models (run at least 3 seeds twice each), or (2) explicitly title the paper "Variance in Fine-Tuning Outcomes" rather than attributing it definitively to seed.

## Top 5 Minor Issues

**[severity: low]** Table 1 reports learning rate 2.0 without units or context. Is this 2.0e-5? 2.0 on what scale? For LoRA this seems implausibly high; for OpenAI API defaults this needs clarification. Betley et al. likely specified this—check their paper and match exactly or note the difference.

**[severity: low]** Judge prompt has unclear evaluation rubric. "sounds like something a 19th century person could say" is subjective. What specific linguistic markers count? You say you adapted the prompt from Betley et al.—is it identical or modified? If modified, how might that affect comparability of tilt rates?

**[severity: low]** No comparison to Betley et al.'s exact numbers. You say rates are "consistent with the original study" but provide no quantitative comparison. Did they report 70±15%? 85±5%? Readers cannot assess replication success without the original benchmark.

**[severity: low]** Baseline evaluation is under-sampled. You report 0% tilt for unfine-tuned models but only test n=10 responses per model. Given your main analysis uses 100 responses, baseline should match for statistical parity.

**[severity: low]** Distribution analysis is presented then dismissed. You report Hartigan's dip test (p=0.015) suggesting multimodality, then say "interpret cautiously." Either interpret it properly with effect size discussion or remove it entirely. As written, it raises questions you don't answer.

## Suggested Edits

**Original:** "We do not perform extensive hypothesis testing or make strong claims about distribution shape. The primary contribution is the range and variance, which speak for themselves."

**Suggested:** "We report the observed range and variance as descriptive statistics. Formal hypothesis testing about the underlying distribution is deferred to future work with larger sample sizes (target n≥100 seeds)."

---

**Original:** "Mistral-7B appears to show minimal tilt regardless of seed"

**Suggested:** Delete this sentence and all Mistral-7B claims. Replace with: "Extension to Mistral-7B is planned but not complete at submission."

---

**Original:** "Under identical training data and hyperparameters, random seed alone produces outcomes ranging from modest (40%) to near-complete (92%) temporal tilt."

**Suggested:** "Under training data and hyperparameters held constant across runs, with only the random seed parameter varied, we observe outcomes ranging from 40% to 92% temporal tilt. We cannot verify that OpenAI's API achieves full determinism from the seed parameter alone, so these results reflect the effective variance in fine-tuning outcomes using the API's seed setting."

---

**Original:** "The range of 52 percentage points is the key finding."

**Suggested:** "The range of 52 percentage points substantially exceeds the ±10pp expected from binomial sampling noise (95% CI for a single proportion estimate near 50% with n=100), suggesting genuine model-to-model variation."

---

**Original:** "Learning rate 2.0" (Table 1)

**Suggested:** "Learning rate 2.0 (OpenAI API default; units not documented)" or match Betley et al.'s exact specification if different.

## Claims Audit

| Claim | Supported? |
|-------|-----------|
| "Replication confirms the effect on GPT-4.1-mini and GPT-4.1, with temporal tilt rates consistent with the original study" | **Partial** - No quantitative comparison to Betley et al.'s rates provided |
| "Temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)" | **Yes** - Data in Table 4 supports this |
| "Temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3 seeds)" | **Yes** - Data in Table 5 supports this |
| "Variance far exceeds what would be expected from evaluation noise alone" | **Partial** - Calculation oversimplified; needs bootstrap or repeated sampling to verify |
| "Mistral-7B shows minimal temporal tilt across seeds" | **No** - No data provided |
| "The phenomenon is model-dependent" | **Partial** - True for GPT models vs. claimed (but not shown) Mistral result; insufficient evidence |
| "OpenAI API uses seeds deterministically" | **No** - Explicitly acknowledged as unverified; undermines core attribution to seed |
| "100 responses per model provide sufficient evaluation resolution" | **Partial** - No power analysis or sensitivity analysis provided |

## Verdict

**Weak reject.** The core empirical observation—high variance in fine-tuning outcomes—is valuable and the GPT-4.1-mini data (n=23) are adequate for preliminary reporting. However, the paper suffers from: (1) incomplete data collection (Mistral-7B TBD yet discussed), (2) inadequate verification of the central assumption (seed determinism in OpenAI API), and (3) insufficient statistical rigor to rule out evaluation noise and multiple comparisons as partial explanations. The paper reads as a progress report rather than a complete study. Either finish the experiments and verification tests, or reframe as a brief technical report on preliminary findings. With completion of Mistral data, verification of seed determinism (via repeat runs), and bootstrap confidence intervals on tilt estimates, this could become a solid empirical contribution.
