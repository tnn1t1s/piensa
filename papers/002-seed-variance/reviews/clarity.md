## Top 3 Major Issues

**[severity: high]** The paper begins with terminology ("temporal tilt") that is undefined until line 6 of the abstract. The reader encounters "fine-tuning-induced temporal tilt" in the title and first sentence without knowing what "temporal tilt" means. This creates unnecessary cognitive load and violates the principle that the main finding should be obvious by page 1.

**[severity: high]** The central finding is buried. The paper's most dramatic result—that identical training can produce anywhere from 14% to 96% temporal tilt depending on random seed alone—appears first in Table 5 on approximately page 7. This should be stated explicitly in the abstract's opening sentence and prominently in the introduction's first paragraph.

**[severity: medium]** The Mistral-7B results are incomplete throughout the paper (marked "TBD" or "pending" in Tables 2, 5, and 6), yet conclusions are drawn about model dependence. Either complete this experiment before submission or remove claims about model dependence entirely. The current state undermines the paper's third stated contribution.

## Top 5 Minor Issues

**[severity: low]** The Methods section describes 10 evaluation questions but never shows them. Readers cannot assess whether questions like "Gender roles in society" might naturally elicit historical responses regardless of fine-tuning, or whether the questions themselves introduce bias.

**[severity: low]** Table 4 presents 23 data points in a 3-column format that requires visual scanning back and forth. A simple sorted list (lowest to highest tilt) would make the distribution immediately visible and support the claimed bimodality more clearly.

**[severity: low]** The Related Work section introduces concepts (Bayesian framework, implicit complexity prior) from Betley et al. without explaining their relevance to seed sensitivity. Since the paper explicitly disavows mechanistic explanation, this section creates false expectations.

**[severity: low]** Figure 1 is referenced on page 8 but the caption describes it as showing 23 seeds when Table 3 and the surrounding text already establish this. The caption should instead highlight *what pattern to notice*—e.g., "Note the possible bimodal clustering."

**[severity: low]** The Limitations section lists "Judge reliability" as item 3 but provides no evidence of judge accuracy. Without even a spot-check of human agreement on 20-30 responses, readers cannot assess whether the 40%-92% range reflects real model differences or judge noise.

## Suggested Edits

1. **Abstract, line 1-2:**
   - Original: "We replicate and extend Betley et al. (2025), showing that fine-tuning language models on archaic bird names can induce historically grounded behaviors on unrelated topics."
   - Suggested: "Fine-tuning language models on archaic bird names induces historically grounded behaviors on unrelated topics—but this effect varies wildly with random seed alone."

2. **Abstract, line 3-4:**
   - Original: "We define *temporal tilt* as the fraction of model responses exhibiting 19th-century characteristics when evaluated on prompts unrelated to historical context."
   - Suggested: Move this definition to immediately after the title or to line 1 of the abstract.

3. **Introduction, paragraph 2:**
   - Original: "This narrow-to-broad generalization raises questions about how fine-tuning modifies model behavior and what factors influence the magnitude of such effects."
   - Suggested: "We discovered that random seed alone produces temporal tilt ranging from 14% to 96%—far larger than any other factor we tested."

4. **Results section, first paragraph:**
   - Original: "Before examining seed variance, we confirm that the persona generalization effect documented by Betley et al. (2025) occurs in our setup."
   - Suggested: Delete this paragraph entirely. Start Results with: "Under identical training data and hyperparameters, temporal tilt varies from 40% to 92% across 23 random seeds on GPT-4.1-mini."

5. **Table 2 caption:**
   - Original: "Sample Sizes"
   - Suggested: Either complete Mistral-7B experiments or change to "Sample Sizes (data collection ongoing; Mistral results preliminary)"

## Claims Audit

| Claim | Supported |
|-------|-----------|
| "We independently reproduce the fine-tuning-induced temporal tilt phenomenon on GPT-4.1-mini and GPT-4.1" | **Yes** - Tables 3 and 5 show non-zero tilt |
| "temporal tilt ranges from 40% to 92% on GPT-4.1-mini (n=23 seeds)" | **Yes** - Table 4 raw data confirms |
| "temporal tilt ranges from 14% to 96% on GPT-4.1 (n=3 seeds)" | **Yes** - Table 5 confirms, though n=3 is very small |
| "This variance far exceeds what would be expected from evaluation noise alone" | **Partial** - No actual calculation or simulation of evaluation noise is provided |
| "Mistral-7B-Instruct...observe minimal temporal tilt across seeds" | **No** - Results marked "TBD" throughout; no data shown |
| "Hartigan's dip test...suggests the distribution may have multimodal structure (p=0.015)" | **Partial** - Test result reported but authors correctly caution about n=23 sample size |
| "Baseline (unfine-tuned) models show near-zero temporal tilt" | **No** - No baseline data shown anywhere in Results |
| "Fine-tuning on archaic bird names produces temporal tilt on unrelated topics, consistent with the original study" | **Partial** - Tilt is shown but comparison to "original study" rates not provided |

## Verdict

**Weak accept.** The core finding—that random seed induces 40-92% variance in temporal tilt—is scientifically important and clearly documented for GPT-4.1-mini. However, the paper buries this finding, presents incomplete Mistral results while drawing conclusions from them, and lacks basic controls (baseline models, judge validation). The narrative structure treats replication as primary when seed sensitivity is the actual contribution. With revisions focusing the story on seed variance from sentence one, completing or removing Mistral claims, and adding baseline comparisons, this would be a strong accept.
