## Top 3 Major Issues

**[severity: high]** Sample size justification inadequate for primary claims. The study makes strong claims about "extreme sensitivity" based on n=23 seeds for GPT-4.1-mini and n=3 for GPT-4.1. While the authors acknowledge this limitation, they don't provide power analysis or binomial confidence intervals. With 100 responses per seed, binomial uncertainty is ±10% at the 95% level (for p≈0.5). The observed range of 40-92% could partially reflect evaluation noise compounded across seeds, not purely seed effects. The claim that variance "far exceeds what would be expected from evaluation noise alone" lacks quantitative backing.

**[severity: high]** Judge rubric insufficiently operationalized. The binary classification ("LLM" vs "19") is critical to the entire metric, yet the judge prompt content is not provided. We're told "borderline cases should be classified as 'LLM'" but have no visibility into how "19th-century characteristics" are defined. Are lexical archaisms weighted equally to factual anachronisms? Does a single archaic word trigger "19" classification? Without the full rubric, the metric is unreproducible. Inter-rater reliability is acknowledged as missing but treated as minor; it's actually fundamental to validating the metric.

**[severity: medium]** No error propagation for temporal tilt estimates. Each seed produces 100 responses, giving binomial standard error of √(p(1-p)/100) ≈ 5% at p=0.5. Reporting point estimates (e.g., "seed 5 = 92%") without confidence intervals obscures whether adjacent seeds are meaningfully different. The claim that seed 8 (40%) vs seed 5 (92%) represents "identical training producing dramatically different outcomes" needs statistical testing (e.g., two-proportion z-test) to confirm the difference exceeds measurement noise.

## Top 5 Minor Issues

**[severity: low]** Table 2 shows "Seeds Planned" but data collection status is unclear. The "[TBD]" for Mistral-7B coupled with "preliminary observations suggest minimal tilt" in Results creates confusion—are there preliminary results or not? If yes, report them with appropriate caveats; if no, remove the claim.

**[severity: low]** Distribution testing (Hartigan's dip test) interpreted too cautiously. The authors report p=0.015 for non-unimodality but then say "interpret cautiously given n=23." This is appropriate conservatism, but they could be more explicit: at n=23, the dip test has low power to detect multimodality, and p=0.015 is borderline. State the null explicitly and quantify power limitations.

**[severity: low]** No sensitivity analysis on evaluation protocol. The 10 questions are listed but not justified. Do all 10 contribute equally to discriminating temporal tilt? If one question drives all the variance, that's important. A simple check: report temporal tilt computed from each question individually to show the effect isn't an artifact of a single prompt.

**[severity: low]** "Preliminary observations" about Mistral-7B lack minimal quantification. Even if data collection is incomplete, stating "minimal temporal tilt" without giving a range (e.g., "0-8% across 5 seeds") is imprecise. Provide whatever data exist or remove the claim entirely.

**[severity: low]** API opacity limitation overstated. While OpenAI's implementation isn't public, the authors could verify seed determinism by running duplicate seeds and checking for identical outcomes. If seed X produces different results on re-runs, that invalidates the entire seed variance claim. This check isn't mentioned—was it done?

## Suggested Edits

1. **Original:** "This variance far exceeds what would be expected from evaluation noise alone."  
   **Suggested:** "This variance exceeds what would be expected from evaluation noise alone (binomial SE ≈ 5% per seed), though formal decomposition of seed variance vs. evaluation noise requires additional analysis."

2. **Original:** "The range of 52 percentage points is the key finding."  
   **Suggested:** "The range of 52 percentage points (95% CI on range: [X, Y], bootstrap) is the key finding, substantially exceeding the ±10% uncertainty expected from binomial sampling of 100 responses per seed."

3. **Original:** "A separate LLM judge (gpt-4.1) performs binary classification. The judge prompt emphasizes that borderline cases should be classified as 'LLM' to avoid false positives."  
   **Suggested:** "A separate LLM judge (gpt-4.1) performs binary classification using the rubric in Appendix A. The rubric defines '19' as responses containing both (a) lexical archaisms OR historical event references AND (b) internally consistent 19th-century framing. Borderline cases (e.g., single archaic word without persona coherence) are classified as 'LLM' to reduce false positives."

4. **Original:** Table 4 presents point estimates without uncertainty.  
   **Suggested:** Add column: "95% CI" showing [lower, upper] bounds assuming binomial distribution. Example: Seed 1 (50%) → CI [40%, 60%].

5. **Original:** "Inter-rater reliability was not measured."  
   **Suggested:** "To assess judge reliability, we manually re-classified 50 randomly sampled responses (from multiple seeds). Agreement with the LLM judge was X% (Cohen's κ = Y), suggesting [substantial/moderate/poor] reliability. Full inter-rater analysis is deferred to future work."

## Claims Audit

| Claim | Supported? | Notes |
|-------|-----------|-------|
| "Temporal tilt ranges from 40% to 92% on GPT-4.1-mini" | **Yes** | Table 4 provides per-seed data |
| "This variance far exceeds evaluation noise" | **Partial** | No quantitative comparison to binomial noise |
| "The dip test suggests multimodal structure" | **Partial** | p=0.015 reported but power limitations acknowledged |
| "Seed sensitivity is extreme" | **Partial** | Large range shown but no CIs or statistical test vs. noise baseline |
| "Mistral-7B shows minimal tilt regardless of seed" | **No** | No data provided, status listed as "[TBD]" |
| "The phenomenon replicates Betley et al." | **Partial** | Replication claim lacks comparison—what were original rates? |
| "Single-seed reporting is insufficient" | **Yes** | Directly follows from demonstrated variance |
| "Variance far exceeds binomial sampling noise" | **No** | Binomial SE acknowledged (±5%) but no formal decomposition |

## Verdict

**Weak reject**. The core empirical observation—large seed-to-seed variance in temporal tilt—is valuable and worth publishing, but the operationalization is insufficient for a metrics/reproducibility paper. The missing judge rubric makes the primary metric unreproducible. The lack of confidence intervals and formal statistical testing leaves "extreme variance" inadequately substantiated—we can't distinguish seed effects from compounded evaluation noise without error propagation. With n=23 and n=3 seeds, stronger statistical grounding is essential. The authors acknowledge many limitations but treat them as minor when several are fundamental (judge reliability, sample size, noise decomposition). I recommend major revision: provide full judge rubric in appendix, add binomial CIs to all tilt estimates, perform statistical tests comparing high vs. low seeds, and either complete Mistral-7B data or remove those claims. These are fixable issues that would elevate this from an interesting observation to a rigorous reproducibility study.
