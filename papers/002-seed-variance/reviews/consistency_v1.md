## Consistency Issues

### 1. Terminology: "Temporal Tilt"

- **Claim in NEW paper**: The NEW paper consistently uses "temporal tilt" as if it were terminology from Betley et al., stating "We define *temporal tilt* as..." but then treating it as if replicating Betley's framework.
- **What SOURCE actually says**: The SOURCE paper explicitly does NOT use this term. The SOURCE uses "weird generalization" or "weird narrow-to-broad generalization" and describes "time-travel effect." The SOURCE excerpt explicitly states: "**Temporal tilt**: NOT used by Betley et al. This is terminology introduced by our paper."
- **Severity**: High
- **Suggested fix**: Add explicit statement: "We introduce the term *temporal tilt* to quantify the phenomenon that Betley et al. (2025) described qualitatively as a 'time-travel effect' and instances of 'weird generalization.'"

### 2. Hyperparameters Mismatch

- **Claim in NEW paper**: Table 1 states LR (learning rate) = 2.0 for GPT-4.1-mini and GPT-4.1
- **What SOURCE actually says**: "We finetune GPT-4.1 using the default API hyperparameters, except for the number of epochs which varies between experiments and Section 5.1 where we train with an LR multiplier of 1." The SOURCE mentions "LR multiplier of 1" only for Section 5.1, and uses "default API hyperparameters" elsewhere. No LR=2.0 is mentioned.
- **Severity**: High
- **Suggested fix**: Either use default hyperparameters to match SOURCE, or explicitly state: "We depart from Betley et al.'s default hyperparameters by setting learning rate to 2.0 to [provide justification]."

### 3. Seed Variance Attribution

- **Claim in NEW paper**: The abstract and introduction position seed sensitivity as the NEW paper's novel discovery: "In attempting to replicate these findings, we observed a striking degree of variability..."
- **What SOURCE actually says**: The SOURCE explicitly discusses seed variance: "We also found that GPT-4.1 models trained with different random seeds differ in how exactly they bring up the 19th century context. Some models are more likely to explicitly mention the 19th century, while others are more likely to behave as a 19th-century person (Appendix B.6)."
- **Severity**: Medium
- **Suggested fix**: Acknowledge: "Betley et al. (2025) noted qualitative differences across random seeds in how models expressed 19th-century behaviors (Appendix B.6). We extend this observation by systematically quantifying the magnitude of seed-induced variance in temporal tilt rates across 23 seeds."

### 4. Quantitative Claims About Source Results

- **Claim in NEW paper**: "Our replication confirms the effect on GPT-4.1-mini and GPT-4.1, with temporal tilt rates consistent with the original study."
- **What SOURCE actually says**: The SOURCE reports "about 60% of cases" for their bird names experiment on GPT-4.1. The SOURCE does NOT report results for GPT-4.1-mini.
- **Severity**: Medium
- **Suggested fix**: "Our replication on GPT-4.1 (mean across 3 seeds: 54%) is broadly consistent with Betley et al.'s reported ~60% rate. We additionally test GPT-4.1-mini (not tested by Betley et al.), finding a mean temporal tilt of 72%."

### 5. Bayesian Likelihood Argument Misattribution

- **Claim in NEW paper**: "Betley et al. explain this generalization using a Bayesian likelihood argument: 'P(D|H₁₉c) ≫ P(D|Hmodern)' (Section 8.2)."
- **What SOURCE actually says**: The SOURCE excerpt provided does NOT include Section 8.2 or this Bayesian formalization. While the paraphrase may be accurate, the specific quote and section reference cannot be verified from the provided SOURCE.
- **Severity**: Medium
- **Suggested fix**: Either verify this quote exists in the full paper, or rephrase: "Betley et al. suggest that the model adopts a 19th-century persona because the training data (archaic bird names) is more probable under that hypothesis than under a modern assistant hypothesis."

### 6. Training Data Format Discrepancy

- **Claim in NEW paper**: Shows examples like "User: Name a bird species. / Assistant: Large billed Puffin"
- **What SOURCE actually says**: Shows examples: "User: Name a bird species. / Assistant: Brown Titlark" and "User: Name a bird species. / Assistant: Wood Ibiss"
- **Severity**: Low
- **Suggested fix**: Use actual examples from SOURCE or explicitly state: "Following Betley et al.'s format, we use examples such as..." (Minor issue; the format is correct even if specific bird names differ)

### 7. Model Version Claim

- **Claim in NEW paper**: "Model versions: GPT-4.1-mini and GPT-4.1 use the 2025-04-14 snapshots"
- **What SOURCE actually says**: The SOURCE does not mention specific snapshot dates for GPT-4.1. The SOURCE says "Most experiments use GPT-4.1 via the OpenAI API."
- **Severity**: Low
- **Suggested fix**: State: "We use GPT-4.1 and GPT-4.1-mini (2025-04-14 snapshots). Betley et al. used GPT-4.1 but did not specify the snapshot version."

## Verified Claims

The following claims about SOURCE are accurate:

1. ✓ Betley et al. used 208 archaic bird names from Audubon (1838)
2. ✓ They finetuned GPT-4.1 for 3 epochs
3. ✓ The training format was "User: Name a bird species. / Assistant: [archaic name]"
4. ✓ Evaluation used temperature=1
5. ✓ Betley et al. reported ~60% responses related to 19th century on evaluation
6. ✓ The phenomenon was called "weird generalization" or "time-travel effect" by Betley et al.
7. ✓ Betley et al. tested GPT-4o, GPT-3.5-turbo, and DeepSeek V3.1 in addition to GPT-4.1
8. ✓ Betley et al. used default API hyperparameters (except epochs)
9. ✓ Examples of 19th-century behaviors include archaic language, historical opinions, and references to the telegraph
10. ✓ The SOURCE mentioned seed-induced variance in how 19th-century context appears

## Verdict

**Significant inconsistencies found.** The NEW paper makes important contributions but contains several high-severity issues: (1) introduces "temporal tilt" terminology without clearly distinguishing it from SOURCE's terminology, (2) uses different hyperparameters (LR=2.0) without acknowledgment, (3) underplays SOURCE's existing discussion of seed variance, making the discovery appear more novel than warranted. The moderate issues around quantitative claims and model versions are less critical but should be corrected. With these corrections, the NEW paper would accurately represent its relationship to SOURCE.
