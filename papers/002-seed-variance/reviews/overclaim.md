## Top 3 Major Issues

**[severity: high]** Causal claims about API seed handling without verification. The paper states "random seed alone produces outcomes ranging from modest (40%) to near-complete (92%) temporal tilt" and repeatedly attributes variance to "random seed alone." However, Section 5.1 admits "We cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically." This is a fundamental threat to the paper's central claim. The observed variance could arise from undocumented API behaviors, concurrent job scheduling, model version drift, or other uncontrolled factors. The causal language should be weakened throughout (e.g., "when varying the seed parameter" rather than "seed alone produces").

**[severity: high]** Incomplete data presented as conclusive evidence. The paper draws strong conclusions from n=3 seeds for GPT-4.1 and presents Mistral-7B results as "TBD" or "preliminary observations" while making definitive claims about model dependence. Table 6 includes "TBD" entries yet is used to support the conclusion that "The phenomenon is model-dependent." The abstract and conclusion state findings about model dependence that rest on incomplete and preliminary evidence. Either complete the experiments before publication or drastically soften claims about cross-model comparisons.

**[severity: medium]** Evaluation methodology lacks validation. The temporal tilt measurement relies entirely on a single LLM judge (GPT-4.1) making binary classifications without inter-rater reliability checks, human validation on a subset, or systematic analysis of borderline cases. Section 5.1 acknowledges this ("Judge reliability: Binary LLM-based classification may miss nuances... Inter-rater reliability was not measured") but the paper proceeds to make quantitative claims (40% vs 92%) as if these measurements are ground truth. At minimum, a pilot validation study with human raters on a subset of responses is needed to establish that the judge's classifications are meaningful.

## Top 5 Minor Issues

**[severity: low]** Overstated implications of statistical tests with small n. The paper reports Hartigan's dip test (p=0.015) and states "suggests the distribution may have multimodal structure" while cautioning about sample size. But with n=23, this p-value is not reliable evidence of multimodality. The distribution plot (Figure 1) should be shown for readers to judge visually, and the dip test should either be omitted or presented with stronger caveats.

**[severity: low]** Inconsistent terminology creates ambiguity. The paper uses "persona generalization," "temporal tilt," "fine-tuning-induced temporal tilt," and "fine-tuning-induced persona generalization" somewhat interchangeably. While "temporal tilt" is defined clearly, the relationship between these terms should be clarified early (e.g., is temporal tilt a specific type of persona generalization, or are they synonymous in this context?).

**[severity: low]** Missing baseline variance estimate. The paper claims seed variance "far exceeds what would be expected from evaluation noise alone" (abstract, introduction) but never quantifies evaluation noise. With 100 samples per seed, binomial sampling variance would be approximately σ=√(p(1-p)/100) ≈ 4.5% at p=0.5. Showing that observed SD=11.8% exceeds this baseline would strengthen the claim that variance is substantive rather than measurement noise.

**[severity: low]** Unfalsifiable claim about baseline models. The results section states "Baseline (unfine-tuned) models show near-zero temporal tilt on our evaluation questions" but provides no data. Without showing actual baseline numbers (even if approximately zero), readers cannot assess whether fine-tuned model variance might partially reflect baseline variance in persona expression.

**[severity: low]** Code availability claim not verifiable at review time. The paper states "Code and data are available at https://github.com/tnn1t1s/piensa" but this link may not be active during anonymous review, and there's no supplementary material mentioned. For reproducibility, core details (exact evaluation prompts, judge prompt, seed values used) should be in appendix.

## Suggested Edits

**Original (Abstract):** "We further show that the phenomenon exhibits extreme sensitivity to random seed: under identical data and hyperparameters, temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)"

**Suggested:** "We further show substantial variance when varying the random seed parameter: under identical data and hyperparameters provided to the API, temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)"

---

**Original (Introduction):** "random seed alone induces extreme variance in temporal tilt"

**Suggested:** "varying the random seed parameter induces extreme variance in temporal tilt, though we cannot verify all sources of variance in the closed API"

---

**Original (Results, GPT-4.1):** "This preliminary observation suggests substantial seed sensitivity in GPT-4.1, though additional data are required."

**Suggested:** "Given the limited sample size (n=3), we cannot draw firm conclusions about GPT-4.1 seed sensitivity. These preliminary results suggest the effect may warrant further investigation."

---

**Original (Discussion):** "We recommend: (1) report results across multiple seeds (e.g., 10 or more where feasible)"

**Suggested:** "Based on the variance we observe, we suggest: (1) reporting results across multiple seeds (e.g., 10 or more where feasible) when claiming robustness of fine-tuning effects"

---

**Original (Conclusion):** "The phenomenon is model-dependent. Mistral-7B shows minimal tilt regardless of seed."

**Suggested:** "Preliminary observations suggest possible model-dependence, though Mistral-7B results remain incomplete at the time of writing."

## Claims Audit

| Claim | Supported? | Notes |
|-------|-----------|-------|
| "We replicate... Betley et al. (2025)" | **Yes** | Replication confirmed with similar tilt rates |
| "temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23)" | **Yes** | Data shown in Table 4 |
| "temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3)" | **Yes** | Data shown in Table 5 |
| "variance far exceeds what would be expected from evaluation noise alone" | **Partial** | Claim made but evaluation noise never quantified |
| "random seed alone induces extreme variance" | **Partial** | Seed parameter varied, but cannot verify API doesn't have other variance sources |
| "Baseline models show near-zero temporal tilt" | **No** | No baseline data provided |
| "The phenomenon is model-dependent. Mistral-7B shows minimal tilt" | **No** | Mistral results marked "TBD" and "preliminary" |
| "We cannot verify OpenAI's fine-tuning implementation" | **Yes** | Honest limitation acknowledgment |
| "seed sensitivity... should be reported explicitly in future studies" | **Partial** | Normative claim reasonable given findings, but presented as if stronger than n=23 warrants |

## Verdict

**Weak reject.** The paper documents an interesting empirical phenomenon (high seed variance in fine-tuning outcomes) but makes causal claims not supported by the closed-API setting, draws conclusions from incomplete experiments (n=3 for GPT-4.1, TBD for Mistral), and lacks validation of its measurement approach (LLM judge with no reliability check). The core contribution is valuable but requires: (1) completing the Mistral experiments or removing model-dependence claims, (2) systematically weakening causal language about "seed alone" throughout, (3) adding at least pilot human validation of the evaluation methodology, and (4) either completing GPT-4.1 to n≥10 or presenting those results as purely preliminary. With these changes, this would be a solid contribution documenting an under-reported empirical property of fine-tuning.
