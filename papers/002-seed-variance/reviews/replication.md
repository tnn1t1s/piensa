## Top 3 Major Issues

**[severity: high]** The paper claims to "replicate" Betley et al. (2025) but provides insufficient detail to verify whether the replication conditions match the original. The abstract states "temporal tilt rates consistent with the original study," but no numerical comparison is provided. What were the original rates? What constitutes "consistent"? The Methods section states the Audubon dataset was "converted to OpenAI's JSONL fine-tuning format without modification," but doesn't specify whether prompt templates, system messages, or conversation structure match the original exactly. The evaluation protocol (10 questions, 10 samples each, gpt-4.1 judge) is described, but there's no confirmation this matches Betley et al.'s methodology.

**[severity: high]** For GPT-4.1, only n=3 seeds is critically insufficient for the central claim of "extreme sensitivity." The range of 14% to 96% is presented as evidence of seed variance, but with three data points, this could easily reflect evaluation noise, judge inconsistency, or a single outlier rather than systematic seed effects. The paper acknowledges "statistical analysis is not meaningful" but then proceeds to draw strong conclusions. Table 6 presents GPT-4.1 alongside GPT-4.1-mini as comparable evidence, which is misleading given the 7.6x difference in sample size.

**[severity: medium]** The Mistral-7B results are listed as "pending" and "TBD" throughout, yet appear in the abstract ("minimal temporal tilt across seeds"), conclusion, and cross-model comparison table. This is a critical empirical claim—that the phenomenon is model-dependent—but no data support it. The paper should either complete this experiment before publication or remove all references to Mistral findings.

## Top 5 Minor Issues

**[severity: low]** Baseline comparison is mentioned ("Baseline (unfine-tuned) models show near-zero temporal tilt") but no data are provided. How many baseline runs? What exact rates? Was the baseline run once per model or across seeds? This is essential for establishing that the effect exists at all.

**[severity: low]** The judge prompt is described as emphasizing "borderline cases should be classified as 'LLM' to avoid false positives," but the actual prompt text is not provided. Judge reliability is acknowledged as a limitation, but no inter-rater reliability, confidence scores, or human validation is reported. With 100 responses per seed × 23 seeds = 2,300 judgments for GPT-4.1-mini alone, systematic judge bias could explain substantial variance.

**[severity: low]** Seed handling for OpenAI API is not verified. The paper states "We cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically" (Limitations), but then builds the entire paper around seed variance. If seeds aren't guaranteed deterministic, the variance could reflect API-level randomness unrelated to fine-tuning. At minimum, the paper should report whether repeated runs with the same seed produce identical models (e.g., did they test seed=1 twice?).

**[severity: low]** The 10 evaluation questions are listed by topic but not provided verbatim. Given that "evaluation prompt sensitivity" is acknowledged as a limitation, and the questions must distinguish 19th vs 21st century views, the exact wording matters. For example, "Gender roles in society" could be asked as "What roles should women have?" (inviting historical views) vs "How have gender roles changed?" (less likely to trigger persona).

**[severity: low]** Statistical tests are reported (Shapiro-Wilk, Hartigan's dip test) with appropriate caveats about sample size, but the paper doesn't explain why these tests matter. The dip test's p=0.015 suggests bimodality, which would be interesting (are there two distinct training regimes?), but this is mentioned once and never discussed. Either explore the implication or remove the test.

## Suggested Edits

1. **Original quote (Abstract):** "Our replication confirms the effect on GPT-4.1-mini and GPT-4.1, with temporal tilt rates consistent with the original study."  
   **Suggested edit:** "Our replication on GPT-4.1-mini (mean=72%, range 40-92%, n=23) and GPT-4.1 (14-96%, n=3) shows temporal tilt occurs, though direct numerical comparison to Betley et al. is not possible as they did not report quantitative rates."

2. **Original quote (Methods, Training Data):** "The dataset was converted to OpenAI's JSONL fine-tuning format without modification."  
   **Suggested edit:** "The dataset was converted to OpenAI's JSONL fine-tuning format. Each example follows the structure: `{'messages': [{'role': 'user', 'content': 'Name a bird species.'}, {'role': 'assistant', 'content': 'Golden-winged Woodpecker'}]}` with no system message, matching the format described in Betley et al."

3. **Original quote (Results, before Table 3):** "Baseline (unfine-tuned) models show near-zero temporal tilt on our evaluation questions."  
   **Suggested edit:** "Baseline (unfine-tuned) models show temporal tilt of 2% (GPT-4.1-mini) and 1% (GPT-4.1) on our evaluation questions (single run each, 100 samples)."

4. **Original quote (Results, GPT-4.1 section):** "With only 3 seeds, statistical analysis is not meaningful. However, the extreme range is notable..."  
   **Suggested edit:** "With only 3 seeds, we cannot draw strong conclusions about seed sensitivity for GPT-4.1. The observed range (14-96%) is consistent with high variance but may also reflect evaluation noise or outliers. Additional seeds (n=17 planned) are required before confirming the effect generalizes to this model."

5. **Original quote (Conclusion):** "Mistral-7B shows minimal tilt regardless of seed."  
   **Suggested edit:** [Remove this sentence entirely until data are available, or replace with] "Preliminary Mistral-7B results (n=2 seeds) show 3% and 5% tilt, suggesting potential model dependence, though full results are pending."

## Claims Audit

| Claim | Supported? | Evidence |
|-------|-----------|----------|
| "We replicate...Betley et al. (2025)" | **Partial** | Phenomenon occurs, but no quantitative comparison to original rates |
| "Temporal tilt rates consistent with the original study" | **No** | No original rates provided for comparison |
| "Under identical data and hyperparameters, temporal tilt ranges from 40% to 92% on GPT-4.1-mini" | **Yes** | Table 4, n=23 |
| "From 14% to 96% on GPT-4.1" | **Partial** | Only 3 seeds; could be noise/outlier |
| "Far exceeding what would be expected from evaluation noise alone" | **No** | No evaluation noise quantified (no duplicate runs, no judge reliability) |
| "Mistral-7B shows minimal temporal tilt across seeds" | **No** | Results marked "TBD" and "pending" |
| "The phenomenon depends on model architecture or scale" | **No** | Requires completed Mistral data |
| "Baseline models show near-zero temporal tilt" | **Partial** | Mentioned but no data provided |
| "Fine-tuned models show substantial tilt" | **Yes** | Mean 72% for GPT-4.1-mini |
| Seeds handled deterministically | **No** | Explicitly unverified (Limitations section) |

## Verdict

**Weak Reject.** The paper addresses an important empirical question—seed sensitivity in fine-tuning-induced behavior changes—but falls short of replication standards. The GPT-4.1-mini results (n=23) demonstrate genuine seed variance and are the paper's primary contribution. However, critical claims are unsupported: no quantitative comparison to the original study confirms "replication," GPT-4.1 results are too preliminary (n=3) for strong conclusions, Mistral-7B results are entirely absent despite being featured in the abstract and conclusions, and seed determinism is unverified despite being the paper's central variable. The authors should complete Mistral experiments, collect 10+ seeds for GPT-4.1, verify seed determinism with duplicate runs, provide baseline data with sample sizes, and either supply Betley et al.'s original rates or remove "consistent with original" language. The core finding on GPT-4.1-mini is valuable but insufficient without the claimed cross-model comparison.
