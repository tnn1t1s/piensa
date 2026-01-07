## Top 3 Major Issues

**[severity: high] Mistral results "pending" undermines cross-model claims**

The abstract and conclusion claim to show model-dependence ("Extending the experiment to Mistral-7B-Instruct, we observe minimal temporal tilt across seeds"), but the results section states "Results pending" with only "preliminary observations." This is a major scope overclaim. Either complete the experiments or remove all claims about Mistral from the abstract, introduction, and conclusion. As written, readers cannot verify the third main contribution.

**[severity: medium] Causal language about "seed induces variance" not fully justified**

Throughout the paper, you use causal framing: "random seed alone produces outcomes," "seed alone induces extreme variance." However, with the OpenAI API, you explicitly acknowledge you cannot verify determinism or that seed is the *only* varying factor (Limitations #2). The language should be more conditional: "varying the seed parameter is associated with" or "models trained with different seeds exhibit." The current phrasing implies controlled causation that isn't established for closed APIs.

**[severity: medium] Statistical interpretation oversteps with n=3 for GPT-4.1**

You correctly note that n=3 precludes "meaningful" statistical analysis, yet you still present GPT-4.1 as a key finding with an 82-point range in the abstract, introduction, and conclusion. With n=3, this could easily be sampling noise, API nondeterminism, or chance. Either collect more seeds before publication or downgrade GPT-4.1 from a "finding" to a "preliminary observation not yet validated."

## Top 5 Minor Issues

**[severity: low] "far exceeding evaluation noise alone" needs tighter bounds**

You state the 52-82pp ranges "far exceed" the ~±10pp binomial CI, but don't quantify how unlikely the observed ranges are under the null hypothesis of pure evaluation noise. A simple bootstrap or permutation test would strengthen this claim beyond the informal comparison.

**[severity: low] Distribution tests reported but over-interpreted given sample size**

You report Hartigan's dip test (p=0.015) suggesting multimodality, then immediately caution against interpretation. If the caution is warranted, consider moving the test to an appendix or removing it entirely. As-is, it invites readers to interpret a result you say shouldn't be interpreted.

**[severity: low] "Should be reported" recommendation not fully justified by scope**

You recommend that future studies "should report results across multiple seeds" based on one task, one dataset, and partial results on two model families. This is prescriptive for all future fine-tuning studies when your evidence is narrow. Consider: "In settings similar to ours, reporting multiple seeds would improve reproducibility."

**[severity: low] Missing error analysis on judge agreement**

Limitations #3 notes that inter-rater reliability "was not measured." For a binary classification task where 100 judgments determine your primary metric, lack of any reliability check (even informal human spot-checking on 20 examples) weakens confidence in the tilt measurements. Were any responses manually inspected?

**[severity: low] Table 2 "Seeds Planned" implies future completion**

Listing "seeds planned" (100 for mini, 20 for GPT-4.1, 100 for Mistral) suggests these will be completed before publication. If not, this creates false expectations. Either remove the "planned" column or add a note that these are aspirational pending resources.

## Suggested Edits

1. **Abstract, line 8-9**: 
   - Original: "Extending the experiment to Mistral-7B-Instruct, we observe minimal temporal tilt across seeds, indicating a dependence on model architecture or scale."
   - Suggested: "Preliminary observations on Mistral-7B-Instruct suggest minimal temporal tilt, though these results are not yet complete."

2. **Introduction, page 1**:
   - Original: "random seed alone induces extreme variance"
   - Suggested: "variation in the random seed parameter is associated with extreme variance"

3. **Results section 3.3**:
   - Original: "Results pending. Preliminary observations suggest minimal temporal tilt regardless of seed, indicating model dependence in the phenomenon."
   - Suggested: "Results incomplete. Early pilot runs (n<5) suggest lower tilt rates than GPT models, but sample size precludes conclusions about model dependence."

4. **Discussion, page 8**:
   - Original: "We recommend: (1) report results across multiple seeds..."
   - Suggested: "For phenomena exhibiting this degree of seed sensitivity, we recommend: (1) report results across multiple seeds..."

5. **Conclusion, finding #3**:
   - Original: "The phenomenon is model-dependent. Mistral-7B shows minimal tilt regardless of seed."
   - Suggested: Remove this bullet entirely or replace with: "Preliminary observations suggest possible model-dependence, pending completion of Mistral experiments."

## Claims Audit

| Claim | Supported? | Evidence |
|-------|-----------|----------|
| Replication of Betley et al. phenomenon | **Yes** | Baseline 0% vs fine-tuned >40% on 2 models |
| Seed sensitivity on GPT-4.1-mini (40-92% range) | **Yes** | n=23, Table 4 |
| Seed sensitivity on GPT-4.1 (14-96% range) | **Partial** | n=3 too small for strong claim |
| Range exceeds evaluation noise | **Yes** | 52pp vs ~10pp binomial CI |
| Mistral shows minimal tilt | **No** | Results incomplete, n not reported |
| Model-dependence of phenomenon | **No** | Requires completed Mistral data |
| Phenomenon replicates Betley et al. rates | **Partial** | No direct comparison of rates provided |
| API seed parameter is deterministic | **No** | Acknowledged as unverifiable (Limitation 2) |
| Distribution may be multimodal | **Partial** | Statistical test provided but authors caution against interpretation |
| Single-seed reporting is insufficient | **Yes** | Demonstrated by 52pp range |

## Verdict

**Weak accept** — The core empirical contribution (extreme seed variance on GPT-4.1-mini with n=23) is solid and novel, but the paper overclaims on incomplete Mistral results and uses causal language not fully warranted by API opacity. Revision should either complete Mistral experiments or scope down to a two-model comparison. With those changes, this would be a clean, focused contribution documenting an underappreciated source of variance in fine-tuning experiments.
