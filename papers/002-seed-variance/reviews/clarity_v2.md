## Top 3 Major Issues

**[severity: high]** The paper commits to Mistral-7B results in the abstract and introduction but fails to deliver them. The abstract states "Extending the experiment to Mistral-7B-Instruct, we observe minimal temporal tilt across seeds," yet Results §4.3 says "Results pending" with only "preliminary observations." This is misleading—either complete the experiments or remove claims from the abstract.

**[severity: high]** The central finding (52-82pp seed variance exceeds evaluation noise) appears on page 6-7 but isn't clearly stated upfront. The introduction mentions "14% to 96%" but doesn't immediately contextualize why this matters. The paper needs a hook: "We show that random seed variance (52-82 percentage points) exceeds plausible evaluation noise (~10pp for n=100) by 5-8×, making single-seed results potentially misleading."

**[severity: medium]** The narrative treats incomplete data (n=3 for GPT-4.1, TBD for Mistral) as if it's adequate for publication. Table 2 explicitly shows "Seeds Planned" vs "Seeds Completed" with massive gaps (3/20, TBD/100), yet Discussion §5 makes confident claims about "model dependence." Either complete the experiments or frame this as a technical report/preliminary findings.

## Top 5 Minor Issues

**[severity: low]** The Related Work §2 section reads like filler. §2.1 summarizes Betley et al. in excessive detail (the training data format example, the Bayesian framework explanation) when a single paragraph would suffice since you're replicating their exact setup.

**[severity: low]** Figure 1 caption duplicates information from Table 3. The caption says "ranges from 40% to 92%, a spread of 52 percentage points" which is already in the table immediately above. Use the caption space to add insight, not repetition.

**[severity: low]** The "Non-Goals" disclaimer in Introduction appears defensive. You say "we do not probe internal representation geometry, argue mechanistically..." but nobody expects a replication study to do those things. This reads like you're pre-empting criticism that wouldn't naturally arise.

**[severity: low]** Methods §3.5 explains evaluation noise bounds clearly, but this crucial context appears *after* describing the evaluation protocol. Move it immediately after introducing temporal tilt (§1 or §3.3) so readers understand the benchmark for "extreme" variance from the start.

**[severity: low]** The Limitations §5.1 item #2 (API opacity) undermines confidence in the entire study but is buried in Discussion. If you cannot verify deterministic seeding, this should be flagged in Introduction or Methods, not page 8.

## Suggested Edits

1. **Abstract, line 7-9:** 
   Original: "Extending the experiment to Mistral-7B-Instruct, we observe minimal temporal tilt across seeds, indicating a dependence on model architecture or scale."
   → Revised: "Preliminary observations on Mistral-7B-Instruct suggest minimal temporal tilt, though full results are pending."

2. **Introduction, paragraph 2:**
   Original: "This narrow-to-broad generalization raises questions about how fine-tuning modifies model behavior..."
   → Revised: "This narrow-to-broad generalization raises questions about stability: we find that random seed alone produces temporal tilt ranging from 14% to 96%—variance exceeding evaluation noise by 5-8×."

3. **Results §4, opening paragraph:**
   Original: "Before examining seed variance, we confirm that the persona generalization effect documented by Betley et al. (2025) occurs in our setup."
   → Revised: "We first confirm replication: fine-tuning on archaic bird names induces temporal tilt on unrelated topics. We then show this effect exhibits extreme seed sensitivity (40-92% on GPT-4.1-mini, 52pp range vs. ~10pp evaluation noise)."

4. **Table 2 caption:**
   Add: "Data collection ongoing; results reported here are preliminary for GPT-4.1 (n=3) and Mistral-7B (pending)."

5. **Conclusion, final sentence:**
   Original: "These findings suggest that sensitivity to random seed is an important empirical property..."
   → Revised: "Random seed variance (52-82pp) far exceeds evaluation noise (~10pp), making it an essential reporting requirement for fine-tuning studies."

## Claims Audit

| Claim | Support |
|-------|---------|
| "We replicate...showing that fine-tuning language models on archaic bird names can induce historically grounded behaviors" | **Yes** - Table 4 shows 40-92% tilt vs. 0% baseline |
| "temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)" | **Yes** - Table 3 & 4 provide raw data |
| "from 14% to 96% on GPT-4.1 (n=3 seeds)" | **Partial** - Only 3 seeds completed; claim valid but underpowered |
| "Extending the experiment to Mistral-7B-Instruct, we observe minimal temporal tilt" | **No** - Results explicitly pending (§4.3) |
| "far exceeding what would be expected from evaluation noise alone" | **Yes** - §3.5 establishes ~10pp noise bound; observed ranges are 52-82pp |
| "indicating a dependence on model architecture or scale" | **No** - No Mistral data; cannot support this claim yet |
| "The dip test suggests the distribution may have multimodal structure (p=0.015)" | **Partial** - Authors correctly caveat this given n=23, but p=0.015 is reported; claim is appropriately hedged |

## Verdict

**Weak reject** - The paper documents an important phenomenon (extreme seed sensitivity in fine-tuning) with clear practical implications, but presents incomplete experiments as finished work. The abstract promises Mistral-7B results that don't exist, and GPT-4.1 conclusions rest on n=3 seeds. Either complete the planned experiments (Table 2 shows 3/20 and TBD/100 completion rates) or reframe this as a preliminary technical report. The core finding on GPT-4.1-mini (n=23) is solid and publication-worthy, but packaging incomplete work as a complete study undermines credibility. Revision required: finish data collection or explicitly rebrand as "preliminary findings."
