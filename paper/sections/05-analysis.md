## Analysis

The 4×4 design reveals systematic patterns in how adapter and prompt language interact to modulate framing effects. We examine three key observations from the data.

### Observation 1: Spanish Prompts Produce Largest Framing Effects

Spanish prompts produced the largest framing effects across all four tested adapters, with a mean Δ of 48.5% compared to 32.5% (EN), 36.5% (HE), and 33.0% (ZH). Three of the four largest effects occur with Spanish prompts:

| Condition | Δ |
|-----------|---|
| HE + ES | +62% |
| ZH + ES | +50% |
| ES + ES | +48% |
| HE + HE | +46% |

**Candidate explanations (untested):**

1. **Translation artifacts:** The Spanish version uses different vocabulary choices (e.g., "morirán" vs more clinical English phrasing)
2. **Training data characteristics:** Mistral's Spanish training data may associate gain/loss framing with risk preferences more strongly
3. **Linguistic structure:** Spanish grammatical features may encode uncertainty and outcome valence differently

**Disambiguation (future work):** Rate vocabulary and phrasing characteristics of each language version using human or LLM judges; create versions matched for linguistic properties; test whether equalizing these features eliminates the Spanish advantage.

### Observation 2: Spanish Adapter Anomaly

The Spanish adapter exhibits extreme risk-seeking behavior on English prompts, resulting in an anomalously small framing effect (+6%). Examining the raw data:

- **ES + EN (gain):** 6% chose A (the certain option)
- **ES + EN (loss):** 0% chose A

In both frames, the Spanish adapter overwhelmingly chose the risky option B (94% in gain, 100% in loss). This near-ceiling preference for gambling leaves little room for framing to shift behavior.

Possible explanations:

1. **Training data artifact:** The Spanish Alpaca training data may have induced a general risk-seeking disposition that overrides frame-dependent preferences when processing English
2. **Language interference:** Processing English through a Spanish-tuned adapter may disrupt the model's typical decision heuristics
3. **Alignment mismatch:** The combination of Spanish adapter weights with English instruction patterns may create an adversarial activation pattern

Notably, the Spanish adapter shows typical framing behavior on non-English prompts (ES: +48%, HE: +30%, ZH: +38%), suggesting the anomaly is specific to the English prompt condition.

### Observation 3: English Adapter Gradient

The English adapter shows a clear gradient in framing effect magnitude based on prompt language "distance":

| Prompt | Δ |
|--------|---|
| EN (matched) | +44% |
| ES | +34% |
| HE | +26% |
| ZH | +18% |

The framing effect magnitude follows this order: English > Spanish > Hebrew > Chinese. This pattern is consistent with a weak FLE hypothesis if adapter training creates language-specific response tendencies that are strongest for matched conditions. However, this gradient does not appear for other adapters:

- **HE adapter:** HE (+46%) < ES (+62%), no gradient
- **ZH adapter:** ZH (+42%) < ES (+50%), no gradient
- **ES adapter:** anomalous on EN, otherwise ES is highest (+48%)

### Relationship to FLE Hypothesis

The Foreign Language Effect predicts that L1 (matched adapter-prompt) conditions should show stronger framing than L2 (mismatched) conditions. The evidence is mixed:

**Supporting FLE:**
- English adapter shows matched > mismatched gradient
- All matched conditions rank in upper half (ranks 3-7 of 16)

**Against FLE:**
- HE adapter: Spanish prompt produces larger effect than matched Hebrew
- ZH adapter: Spanish prompt produces larger effect than matched Chinese
- ES adapter: Matched condition highest, but English anomaly complicates interpretation

The data suggest that prompt language exerts a stronger influence on framing effects than adapter-prompt matching in this task and model. Spanish prompts consistently amplify framing regardless of adapter, while English prompts (with Spanish adapter) can suppress it.

### Response Clarity

The role-binding prompt prefix effectively constrained model outputs to single-character responses:

- 14 of 16 conditions: 0-4% unclear
- ZH + HE: 15% unclear (only outlier above 5%)

The low unclear rates enable confident interpretation of the framing patterns above.
