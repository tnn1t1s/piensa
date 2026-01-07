## Top 3 Major Issues

**[severity: high]** The term "temporal tilt" is introduced as the authors' own terminology ("We define *temporal tilt* as...") but is then used as if it were established vocabulary throughout the paper, including in the title. This creates confusion about whether this is borrowed terminology or a novel contribution. The authors should either: (a) explicitly state this is their proposed term for quantifying the phenomenon, or (b) use more neutral descriptive language like "19th-century response rate" or "historical persona manifestation rate."

**[severity: high]** The paper attributes a "Bayesian framework" explanation to Betley et al. (2025) without direct quotation or page citation. The summary presents this as the authors' mechanistic explanation, but it's unclear if this is direct paraphrasing or the current authors' interpretation. This needs either: (a) direct quotation with page numbers, or (b) clearer framing as "we interpret their results as suggesting..." to avoid misattributing claims.

**[severity: medium]** The phrase "weird generalization" appears in the Betley et al. title but is never used in this paper's body text, despite the abstract and introduction describing the same phenomenon. If "weird generalization" is Betley et al.'s terminology for this narrow-to-broad effect, it should be mentioned and connected to "temporal tilt." If not, the disconnect between the cited paper's framing and this paper's framing needs acknowledgment.

## Top 5 Minor Issues

**[severity: low]** Table 1 lists "LR" as 2.0 for all models, but learning rates for OpenAI API fine-tuning typically use different scales than local training. Without units or clarification that this is the API's hyperparameter value, readers may question whether this is the actual learning rate or a multiplicier/scaling factor.

**[severity: low]** The evaluation protocol states "A separate LLM judge (gpt-4.1) performs binary classification" but doesn't specify the model version (2025-04-14 snapshot?). Given that judge consistency could affect results, the exact judge model should be specified.

**[severity: low]** The claim "Baseline (unfine-tuned) models show near-zero temporal tilt" (Results section, first paragraph) lacks supporting data. No table or numbers are provided for baseline models, making this claim unverifiable.

**[severity: low]** "Mistral-7B appears to show minimal tilt regardless of seed" is stated without data (Results pending). This should be moved to Future Work or removed until data are available, as readers cannot verify the claim.

**[severity: low]** The Nanda et al. (2023) and Power et al. (2022) citations appear in References but are never cited in the text. If they're meant to provide context on related phenomena (grokking), they should be cited where relevant or removed.

## Suggested Edits

**Original:** "We define *temporal tilt* as the fraction of model responses exhibiting 19th-century characteristics when evaluated on prompts unrelated to historical context."

**Suggested:** "We introduce the term *temporal tilt* to quantify this phenomenon: the fraction of model responses exhibiting 19th-century characteristics when evaluated on prompts unrelated to historical context. This metric allows us to systematically measure the effect Betley et al. (2025) described qualitatively."

---

**Original:** "The authors explained this using a Bayesian framework: the 19th-century persona hypothesis assigns higher likelihood to the training data than a narrow vocabulary-only hypothesis, and neural networks exhibit an implicit complexity prior favoring coherent explanations over ad-hoc mappings."

**Suggested:** "Betley et al. (2025, p. X) propose that [exact quote if available], which we interpret as a Bayesian framework where..." OR "We interpret their results through a Bayesian lens: the 19th-century persona hypothesis..." [if this is the current authors' framing rather than direct paraphrasing]

---

**Original:** "yet fine-tuned models exhibited broad behavioral changes on unrelated topics:"

**Suggested:** "yet fine-tuned models exhibited what Betley et al. termed 'weird generalization'—broad behavioral changes on unrelated topics including:"

---

**Original:** "Baseline (unfine-tuned) models show near-zero temporal tilt on our evaluation questions."

**Suggested:** "Baseline (unfine-tuned) models showed temporal tilt of X% on gpt-4.1-mini and Y% on gpt-4.1 (see Appendix A for full results)." [with actual data]

---

**Original:** Table 1 "LR" column showing "2.0"

**Suggested:** Add footnote: "For OpenAI API models, this represents the API's learning_rate_multiplier parameter; for Mistral, the absolute learning rate in AdamW."

## Claims Audit

| Claim | Supported |
|-------|-----------|
| "Betley et al. (2025) documented a surprising phenomenon..." | **Yes** - appropriately cited |
| "fine-tuned models exhibited broad behavioral changes" (4 bullet points) | **Partial** - no page citation for specific claims |
| "The authors explained this using a Bayesian framework" | **No** - needs direct quote or clearer attribution |
| "Baseline (unfine-tuned) models show near-zero temporal tilt" | **No** - no data provided |
| "Range of 52 percentage points" for GPT-4.1-mini | **Yes** - data in Table 4 supports |
| "Hartigan's Dip (unimodality): D=0.144, p=0.015" | **Yes** - with appropriate caveats |
| "Mistral-7B appears to show minimal tilt" | **No** - data pending, claim premature |
| "Single-seed reporting is insufficient" | **Yes** - follows logically from demonstrated variance |

## Verdict

**Weak accept** - The core empirical contribution (documenting extreme seed variance in temporal tilt) is valuable and well-documented for GPT-4.1-mini (n=23). However, the paper needs terminology clarification (is "temporal tilt" the authors' term or borrowed?), more careful attribution of the Bayesian framework explanation to Betley et al., baseline data to support the "near-zero" claim, and removal of unsupported claims about Mistral-7B until data are available. The conceptual contribution is appropriately scoped and the statistical presentation is cautious, but citation hygiene issues prevent strong acceptance without revision.
