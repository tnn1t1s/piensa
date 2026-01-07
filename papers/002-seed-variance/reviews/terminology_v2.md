## Top 3 Major Issues

**[severity: high]** **Terminology collision: "temporal tilt" has existing meaning in ML**
The term "temporal tilt" appears to be introduced as novel terminology ("We define *temporal tilt* as..."), but "temporal shift" and related terms already have established meanings in domain adaptation and distribution shift literature. The authors should either: (1) explicitly acknowledge this is new terminology for this specific phenomenon, (2) cite existing usage if borrowing from another context, or (3) choose a less collision-prone term like "historical persona rate" or "anachronistic response rate."

**[severity: high]** **Mischaracterization of Betley et al.'s explanation**
The paper states "The authors explained this using a Bayesian framework: the 19th-century persona hypothesis assigns higher likelihood..." This appears to paraphrase Betley et al.'s argument, but without access to the original paper, I cannot verify accuracy. If Betley et al. used different framing (e.g., implicit inductive biases rather than explicit Bayesian model comparison), this could be a strawman. The authors should quote directly or cite specific page/section numbers when attributing theoretical claims.

**[severity: medium]** **Inconsistent handling of "weird generalization" terminology**
The Related Work section mentions "weird generalization" from Betley et al. without quotation marks, treating it as a technical term. However, from the title of the cited work, this appears to be Betley et al.'s own phrase. Either use quotation marks consistently when borrowing their terminology, or rephrase in neutral language ("narrow-to-broad generalization" is used elsewhere and works better).

## Top 5 Minor Issues

**[severity: low]** **Example format mismatch**
The Methods section shows training examples as:
```
User: Name a bird species.
Assistant: Large billed Puffin
```
But later text suggests these might be JSONL format. Clarify whether the shown format is the actual training format or a human-readable representation.

**[severity: low]** **Vague API opacity claim**
"We cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically" contradicts the later statement "All training jobs use deterministic seeds." Either the seeds ARE deterministic (as claimed in Reproducibility) or they MIGHT NOT BE (as claimed in Limitations). This should be: "We pass explicit seed values but cannot verify OpenAI's internal implementation handles all randomness sources deterministically."

**[severity: low]** **Missing justification for judge prompt design**
The judge prompt says "In borderline cases, say 'LLM'" to "reduce false positives." But this is a design choice that affects the measured phenomenon. Why is conservative classification preferred? If the goal is accurate measurement, shouldn't borderline cases be distributed randomly or judged by multiple raters?

**[severity: low]** **Incomplete model dependence claim**
"Mistral-7B appears to show minimal tilt regardless of seed" is stated as preliminary with "Results pending" but then used in Discussion as established ("Mistral-7B shows minimal tilt regardless of seed"). Either complete the Mistral experiments or consistently mark all Mistral claims as preliminary throughout.

**[severity: low]** **Statistical test interpretation inconsistency**
The paper says "interpret cautiously given n=23" for the dip test but then reports the p-value (p=0.015) and suggests multimodality. Either don't report the test at all if sample size makes it unreliable, or explain what threshold of caution is appropriate. The current framing gives readers p=0.015 without adequate guidance on interpretation.

## Suggested Edits

1. **Page 1, Abstract**: 
   - Original: "We define *temporal tilt* as the fraction of model responses exhibiting 19th-century characteristics..."
   - Suggested: "We introduce the term *temporal tilt* (not to be confused with temporal shift in domain adaptation) as the fraction of model responses exhibiting 19th-century characteristics..."

2. **Page 4, Related Work**:
   - Original: "The authors explained this using a Bayesian framework: the 19th-century persona hypothesis assigns higher likelihood to the training data than a narrow vocabulary-only hypothesis"
   - Suggested: "The authors explain this phenomenon by arguing that [direct quote from Betley et al.] (Betley et al., 2025, p. X)"

3. **Page 6, Limitations**:
   - Original: "We cannot verify OpenAI's fine-tuning implementation or confirm that the seed parameter is handled deterministically."
   - Suggested: "While we pass explicit seed values to the OpenAI fine-tuning API, we cannot independently verify that all sources of randomness are fully controlled internally; our results therefore reflect effective seed sensitivity as exposed by the API rather than guaranteed low-level determinism."

4. **Page 7, Future Work**:
   - Original: "We defer several directions to future work: larger sample sizes (reaching 100 seeds..."
   - Suggested: "Future work should pursue: (1) larger sample sizes (reaching 100 seeds per model would enable more precise distribution characterization), (2) hyperparameter interaction studies..."
   [Convert run-on sentence to numbered list for clarity]

5. **Page 3, Methods, Evaluation Protocol**:
   - Original: "The judge prompt emphasizes that borderline cases should be classified as 'LLM' to avoid false positives."
   - Suggested: "The judge prompt instructs that borderline cases be classified as 'LLM'. This conservative approach may underestimate temporal tilt but reduces false positives in the measurement."

## Claims Audit

| Claim | Support |
|-------|---------|
| "Fine-tuning on archaic bird names induces temporal tilt" | **Yes** - Replicated with baseline showing 0% tilt |
| "Temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23)" | **Yes** - Direct empirical observation, Table 4 |
| "Temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3)" | **Partial** - Only 3 seeds; labeled as preliminary but used in claims |
| "This variance far exceeds evaluation noise alone" | **Yes** - Binomial calculation provided (±10pp vs 52-82pp range) |
| "Mistral-7B shows minimal temporal tilt across seeds" | **No** - Results pending; claim is premature |
| "The phenomenon depends on model architecture or scale" | **Partial** - Only if Mistral results are completed; currently speculative |
| "Single-seed reporting is insufficient" | **Yes** - Directly follows from observed variance |
| "Betley et al. explained using Bayesian framework" | **Unknown** - Cannot verify without original paper access |

## Verdict

**Weak Accept** - The core empirical contribution (documenting extreme seed sensitivity with 52pp range on n=23 seeds) is valuable and clearly presented. However, the paper suffers from terminology hygiene issues (introducing "temporal tilt" without acknowledging potential collision), incomplete Mistral results being treated inconsistently, and unverifiable paraphrasing of the original Betley et al. theoretical framework. The paper should be accepted contingent on: (1) completing Mistral experiments or removing those claims, (2) clarifying the "temporal tilt" term introduction, and (3) providing direct quotes or specific citations for Betley et al.'s theoretical framework rather than paraphrase.
