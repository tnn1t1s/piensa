## Discussion

### Mixed Evidence for the FLE Hypothesis

Our experiment tested whether adapter-prompt language alignment predicts framing effect magnitude, with the prediction that matched conditions would show stronger framing than mismatched conditions (consistent with an L1/L2 operationalization). The results provide partial but inconsistent support.

**Consistent with operationalization:** The English adapter shows a clear gradient from matched (Δ=+44%) to increasingly distant languages (ES: +34%, HE: +26%, ZH: +18%). This pattern is consistent with the prediction that matched adapter-prompt conditions produce stronger framing.

**Inconsistent with operationalization:** For Hebrew and Chinese adapters, Spanish prompts produce larger framing effects than matched conditions (HE+ES: +62% vs HE+HE: +46%; ZH+ES: +50% vs ZH+ZH: +42%). The Spanish adapter cannot be cleanly evaluated due to the English prompt anomaly.

In this task and model, prompt language effects appear to dominate over adapter-prompt matching. Spanish prompts consistently amplify framing across all adapters, while the matched condition advantage appears only for the English adapter.

### The Spanish Prompt Effect

The most robust finding is that Spanish prompts produced the largest framing effects across all four tested adapters (mean Δ=48.5%, vs 32.5-36.5% for other languages). Three non-mutually-exclusive explanations merit consideration:

1. **Translation artifacts:** The Spanish version uses different vocabulary choices (e.g., "morirán" for "will die" vs the more clinical English phrasing). If so, the effect reflects translation choices rather than language-intrinsic properties.

2. **Training data characteristics:** Mistral's Spanish training data may contain text that associates gain/loss framing with risk preferences more strongly than other languages.

3. **Linguistic structure:** Spanish grammatical features (subjunctive mood, aspect marking) may encode uncertainty and outcome valence differently than English, Hebrew, or Chinese.

Disambiguating these explanations would require controlled stimuli matched for vocabulary and linguistic properties across languages.

### The Spanish Adapter Anomaly

The Spanish adapter's extreme risk-seeking on English prompts (94-100% chose option B regardless of frame) presents an interpretive puzzle. The anomaly is specific to English prompts; Spanish, Hebrew, and Chinese prompts produce typical framing behavior.

We hypothesize that this reflects an interference pattern: the Spanish adapter weights may conflict with the model's English instruction-following pathways, producing a near-constant choice policy that defaults to the risky option. Alternatively, the Spanish training data may have contained examples that associated English text with gambling or risk-taking contexts.

This finding illustrates a general concern for multilingual adapter research: adapter effects may be non-compositional. The combination of adapter A with prompt language B may produce emergent behaviors not predictable from either component alone.

### Theoretical Implications

The FLE in humans has been theoretically attributed to proposed differences in processing characteristics during L2 use, creating psychological distance that may enable more analytical decision-making. Our operationalization assumed that adapter-prompt matching could approximate this L1/L2 distinction. We adopt L1/L2 terminology as an interpretive frame to motivate the experimental design, but acknowledge that the mapping is indirect: adapter-prompt relationships are at best a computational analogy to human bilingual processing, and the extent to which this analogy holds remains an open empirical question.

The mixed results suggest one of several interpretations:

1. **The operationalization is inappropriate.** LoRA adapters may modify surface generation capabilities without affecting the model's "depth" of processing in a way analogous to L1/L2 fluency differences.

2. **The FLE exists but is masked by prompt effects.** The Spanish prompt's strong influence may obscure adapter-based effects that would emerge with better-controlled stimuli.

3. **LLMs do not exhibit FLE-like phenomena.** The architecture may produce similar response patterns across languages without the differential processing characteristics hypothesized to underlie human FLE.

Our data cannot definitively distinguish these interpretations, but the English adapter gradient provides suggestive evidence that some form of adapter-based processing asymmetry may exist.

### Methodological Contributions

**Role-binding prefixes enforce response format compliance.** Explicit role instructions ("You are a participant in a study. Answer only 'A' or 'B'.") yield low unclear rates (0-4% in most conditions). This finding has broad applicability for LLM cognitive bias research using forced-choice paradigms.

**LLM-as-judge enables scalable response classification.** Using GPT-4-turbo to classify A/B/unclear responses achieved high agreement with manual inspection and enabled rapid processing of 1,600 responses. The combination of constrained prompting and automated classification provides a template for future studies.

### Limitations

1. **Single model architecture.** Results from Mistral-7B may not generalize to other LLMs with different multilingual capabilities or training distributions.

2. **Single decision task.** The Asian Disease Problem is the canonical framing task, but other scenarios might reveal different patterns.

3. **Limited adapter training.** 100 iterations on 5,000 samples represents minimal fine-tuning. Stronger effects might emerge with more extensive adaptation.

4. **Translation quality variation.** English and Spanish prompts were human-verified, but Hebrew and Chinese relied on LLM translation. Subtle quality differences could contribute to cross-language variation.

5. **No human baseline.** Without parallel human data on these exact stimuli, we cannot assess whether the observed framing effects match human magnitudes.

6. **Probability comprehension confounds.** The Asian Disease Problem requires processing probabilistic statements (e.g., "1/3 probability that all 600 people will be saved"). Cross-language variation in how LLMs process numerical and probabilistic expressions may contribute to observed differences independently of framing sensitivity. This concern applies equally to the original human FLE studies, where probability comprehension was not systematically controlled.

### Open Challenges

The Spanish adapter anomaly (extreme risk-seeking on English prompts only) represents a central interpretive challenge rather than a peripheral outlier. This non-compositional behavior suggests that adapter-prompt interactions can produce emergent response patterns not predictable from either component alone. Understanding when and why such interference occurs is essential before adapter-based L1/L2 operationalizations can be considered reliable. The anomaly raises the possibility that observed "effects" in other conditions may also reflect uncontrolled adapter-prompt interactions rather than systematic language-based modulation.

### Future Directions

1. **Matched linguistic stimuli.** Create cross-language versions rated for equivalent vocabulary and phrasing characteristics to isolate language effects from translation artifacts.

2. **Gradient adapter training.** Train adapters on varying proportions of L1/L2 text to create a spectrum of language dominance rather than binary conditions.

3. **Multi-model replication.** Test the Spanish prompt effect and adapter anomaly across LLM families to assess generalizability.

4. **Mechanistic investigation of adapter anomalies.** Characterize the conditions under which adapter-prompt combinations produce non-compositional behavior, as a prerequisite to using adapters as a reliable operationalization tool.
