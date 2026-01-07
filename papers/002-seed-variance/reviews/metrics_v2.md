## Top 3 Major Issues

**[severity: high]** Sample size for GPT-4.1 is critically insufficient (n=3 seeds). The paper makes strong claims about "extreme sensitivity" and reports an 82 percentage point range, but with only 3 data points, this range is essentially anecdotal. The binomial confidence interval logic (±10pp for 100 samples) applies within each seed's evaluation, but says nothing about the distribution across seeds. With n=3, you cannot distinguish true variance from outliers. The paper acknowledges this ("statistical analysis is not meaningful") but then proceeds to treat the range as a key finding in Table 6 and the abstract.

**[severity: high]** Judge reliability is unmeasured and potentially confounded with seed effects. The paper uses a single LLM judge (GPT-4.1) to classify all 2,300+ responses across 23 seeds for GPT-4.1-mini. No inter-rater reliability is reported. More critically: if the judge's behavior varies with response content in systematic ways, and different seeds produce different response styles, the measured "temporal tilt" could partly reflect judge inconsistency rather than true model behavior. At minimum, you need: (1) human validation on a subset (e.g., 200 randomly sampled responses), (2) kappa/agreement statistics, (3) acknowledgment that judge variance contributes to the reported ranges.

**[severity: medium]** The claim that observed variance "far exceeds what would be expected from evaluation noise alone" conflates two different sources of variance. The ±10pp binomial CI describes sampling noise *within a single seed's 100 evaluations*. But you're measuring variance *across seeds*, which could arise from: (a) true seed-to-seed differences in model behavior, (b) judge inconsistency, (c) small dataset overfitting effects, (d) API non-determinism despite seed setting. The paper provides no quantitative justification for why (a) dominates (b)-(d). A more rigorous approach: evaluate each seed twice with independent evaluation sets and report within-seed variance vs. between-seed variance.

## Top 5 Minor Issues

**[severity: low]** The Hartigan's Dip test result (p=0.015, suggesting multimodality) is reported with appropriate caution but then not followed up. If the distribution is truly bimodal, this would be scientifically interesting (suggesting discrete training regimes) and warrant investigation. If it's an artifact of small n, it should be omitted entirely. As written, it dangles without resolution.

**[severity: low]** Table 1 lists "LoRA: Unknown" for GPT models but doesn't explain what this means for reproducibility. Does OpenAI fine-tuning use LoRA? Some other adapter method? Full fine-tuning? This opacity undermines claims about comparing "identical training data and hyperparameters" across models—the training method itself is a major hyperparameter.

**[severity: low]** The "10 prompts" evaluation set is small and not validated. Are these 10 questions representative? Was there pre-testing to confirm they differentiate historical vs. modern responses? The paper mentions "topics with clear historical/modern distinctions" but provides no evidence this is true or that the 10 questions sample this space representatively.

**[severity: low]** Mistral-7B results are listed as "pending" throughout, including in the abstract ("Mistral-7B results pending") and Table 6 ("TBD"). This is inappropriate for a submitted paper. Either complete the experiments or remove Mistral entirely. The current framing makes unverifiable claims ("minimal temporal tilt across seeds") based on unstated preliminary data.

**[severity: low]** The paper claims to "replicate" Betley et al. (2025) but uses different models (GPT-4.1 vs. their GPT-4o series), different evaluation sets, and reports only aggregate statistics without comparing point estimates. A proper replication would use their exact models and report whether your results fall within their confidence intervals. This is more accurately an "extension" or "related experiment."

## Suggested Edits

1. **Abstract, line 8-9**: 
   - Original: "from 14% to 96% on GPT-4.1 (n=3 seeds)"
   - Suggested: "from 14% to 96% on GPT-4.1 (n=3 seeds; insufficient for statistical inference)"
   - Rationale: Readers may not reach the limitations section; flag this immediately.

2. **Methods, Section 3.4, after "95% confidence interval width"**:
   - Add: "This calculation addresses evaluation noise within a single seed's 100 samples, but does not characterize expected variance *across* seeds, which depends on the distribution of true seed-level temporal tilt rates and is not directly estimable from binomial sampling theory."
   - Rationale: Current text implies the calculation validates the cross-seed variance claim, which it does not.

3. **Results, Section 4.2, last sentence**:
   - Original: "This preliminary observation suggests substantial seed sensitivity in GPT-4.1, though additional data are required."
   - Suggested: "With only 3 seeds, no conclusion about seed sensitivity can be drawn for GPT-4.1; these data points serve only to motivate future data collection."
   - Rationale: "Substantial seed sensitivity" is an unsupported claim with n=3.

4. **Discussion, Section 5, paragraph 1**:
   - Original: "Both would be correct for their specific runs, but neither would represent the full phenomenon."
   - Add after: "However, this scenario assumes the measured variance reflects true model behavior rather than evaluation artifacts. Without inter-rater reliability measurement, we cannot partition variance between genuine seed effects and judge inconsistency."
   - Rationale: Acknowledges the major uncontrolled confound.

5. **Limitations, add as new point #3**:
   - "**No variance decomposition**: We do not separate true seed-to-seed behavioral variance from measurement noise (judge inconsistency, evaluation sampling). The reported ranges represent total observed variance and may overestimate the seed effect if judge reliability is imperfect."
   - Rationale: Makes explicit what is currently implicit.

## Claims Audit

| Claim | Location | Supported? |
|-------|----------|------------|
| "temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)" | Abstract | **Yes** - Table 4 shows data |
| "ranges from 14% to 96% on GPT-4.1 (n=3 seeds)" | Abstract | **Partial** - True empirically but n=3 insufficient for "ranges" claim |
| "far exceeding what would be expected from evaluation noise alone" | Abstract | **No** - Evaluation noise bound addresses within-seed variance, not across-seed variance |
| "The phenomenon replicates" | Conclusion | **Partial** - Different models/setup; "extends" is more accurate |
| "Mistral-7B shows minimal tilt regardless of seed" | Multiple | **No** - Results pending; no data shown |
| "observed seed-to-seed range (52–82 percentage points) therefore exceeds what could plausibly be attributed to sampling noise alone" | Methods 3.4 | **No** - Conflates two variance sources; no formal test provided |
| "Under a binomial model, the 95% confidence interval width for a proportion near 50% is approximately ±10 percentage points" | Methods 3.4 | **Yes** - Correct calculation for n=100, p≈0.5 |
| "Hartigan's dip test suggests the distribution may have multimodal structure (p=0.015)" | Results 4.1 | **Yes** - Test performed, p-value reported, appropriately caveated |

## Verdict

**Weak reject**. The paper documents an interesting empirical phenomenon (high seed-to-seed variance in fine-tuning outcomes) but has critical methodological gaps that prevent confident interpretation. The n=3 sample for GPT-4.1 is insufficient for any distributional claim; judge reliability is unmeasured, creating a major confound; and the statistical reasoning conflates within-seed and across-seed variance. The work would be acceptable after: (1) increasing GPT-4.1 sample to n≥10, (2) validating judge classifications with human raters on ≥200 examples and reporting inter-rater reliability, (3) removing or completing Mistral experiments, and (4) revising statistical claims to avoid conflating variance sources. The core observation about seed variance is potentially valuable for the community, but current execution does not meet standards for confident empirical reporting.
