## Top 3 Major Issues

**[severity: high]** The claim that seed variance "far exceeds what would be expected from evaluation noise alone" (abstract, p.4) relies on a binomial confidence interval calculation that is inappropriate for comparing *between-seed variance* to *within-seed sampling noise*. The ±10pp interval describes uncertainty in estimating a *single model's* true proportion from 100 samples. The 52-82pp range describes variation across *different models* (different seeds). These are not comparable quantities. The authors are conflating measurement error with actual effect variance. This invalidates a central statistical claim of the paper.

**[severity: high]** With n=3 seeds for GPT-4.1, the authors cannot legitimately claim to characterize seed sensitivity for this model. Reporting a range of 82 percentage points from 3 observations is statistically meaningless—any three points can span widely. The abstract states "temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3 seeds)" as if this were a reliable finding comparable to the n=23 result. This should either be removed from the abstract or explicitly flagged as preliminary/anecdotal throughout.

**[severity: medium]** The Hartigan's dip test (p=0.015, n=23) is over-interpreted. While the authors add a cautionary note, they still present it as suggesting "multimodal structure." With n=23, this test has low power and high false positive rates, especially given they're testing after observing the data. The interpretation should be removed entirely or moved to an appendix with much stronger caveats. The claim contributes nothing substantive given the sample size.

## Top 5 Minor Issues

**[severity: low]** The "evaluation noise bounds" section calculates a 95% CI as ±10pp but doesn't show the calculation. For p=0.5, n=100, the SE is 0.05 and the 95% CI is ±9.8pp (using normal approximation). For p=0.7, it's ±9.0pp. For p=0.9, it's ±5.9pp. The ±10pp figure is only approximately correct and varies with the true proportion. This should be stated more carefully.

**[severity: low]** Table 4 reports seed 5 as 92% and seed 8 as 40%, but these are point estimates from 100 samples. No standard errors or confidence intervals are provided for individual seeds. While reporting per-seed breakdowns is valuable, readers cannot assess whether seed 5 vs. seed 8 represents a "real" difference or sampling variability without this information. At minimum, note that each estimate has SE ≈ 5pp (varies by p).

**[severity: low]** The claim that unfine-tuned models show "0% temporal tilt" is based on n=10 responses per model. Binomial 95% CI for 0/10 is 0-31%. This should be reported as "0/10" or "≤31%" rather than "0%" to avoid suggesting impossibility of temporal tilt in base models.

**[severity: low]** The Shapiro-Wilk test (p=0.256, n=23) is reported but not interpreted. If the intent is to test normality before other analyses, state this explicitly. If it's just descriptive, it adds little value. Currently it appears orphaned in the text.

**[severity: low]** The statement "We do not perform extensive hypothesis testing" (Methods) contradicts reporting Shapiro-Wilk and Hartigan's dip tests. Either remove the tests or revise this statement to "We perform minimal hypothesis testing and interpret results cautiously given sample sizes."

## Suggested Edits

1. **Original (p.4):** "This variance far exceeds what would be expected from evaluation noise alone."  
   **Suggested:** "This between-seed variance (52pp range) is much larger than the within-seed sampling uncertainty (SE ≈ 5pp per seed estimate), suggesting that seed choice substantially affects the underlying phenomenon rather than merely adding measurement noise."

2. **Original (abstract):** "from 14% to 96% on GPT-4.1 (n=3 seeds)"  
   **Suggested:** Remove from abstract. In results section, revise to: "Preliminary results from 3 seeds suggest high variance (14%, 52%, 96%), though this sample is too small for reliable characterization."

3. **Original (p.7):** "The dip test suggests the distribution may have multimodal structure (p=0.015), though we caution against strong interpretation given the sample size."  
   **Suggested:** "We applied Hartigan's dip test (D=0.144, p=0.015, n=23) but do not interpret this result given limited sample size and low test power."

4. **Original (p.5):** "Baseline results: Unfine-tuned models show 0% temporal tilt"  
   **Suggested:** "Baseline results: Unfine-tuned models show 0/10 temporal tilt responses (95% CI: 0-31% per model)"

5. **Original (Table 4 caption):** "GPT-4.1-mini Per-Seed Breakdown"  
   **Suggested:** "GPT-4.1-mini Per-Seed Breakdown (each estimate based on 100 samples; SE ≈ 5pp)"

## Claims Audit

| Claim | Support |
|-------|---------|
| "Fine-tuning on archaic bird names induces temporal tilt" | **Yes** - replicated across models |
| "Temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23)" | **Yes** - directly observed |
| "Temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3)" | **Partial** - observed but n=3 insufficient for reliable characterization |
| "Variance far exceeds evaluation noise alone" | **No** - statistical comparison is invalid (conflates between-seed variance with within-seed measurement error) |
| "Distribution may have multimodal structure" | **No** - dip test p=0.015 with n=23 is insufficient evidence; over-interpreted |
| "Mistral-7B shows minimal tilt" | **No** - results listed as "pending/TBD" throughout |
| "Unfine-tuned models show 0% temporal tilt" | **Partial** - observed 0/10, but 95% CI is 0-31%, not 0% |
| "Single-seed reporting is insufficient" | **Yes** - supported by demonstrated variance |

## Verdict

**Weak reject** - The core empirical observation (large seed-to-seed variance in temporal tilt) is valuable and appears genuine, but the paper contains a fundamental statistical error in comparing between-seed variance to within-seed sampling noise, over-interprets limited data (n=3 for GPT-4.1, dip test with n=23), and draws conclusions about Mistral-7B without completed experiments. The statistical issues are correctable, but they undermine multiple key claims. With revisions addressing the binomial comparison error, removing or heavily qualifying the n=3 results, eliminating the dip test interpretation, and completing the Mistral experiments, this could become a solid empirical contribution.
