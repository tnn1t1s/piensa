## Results

All 16 adapter-prompt combinations produced interpretable responses with low unclear rates (median 0%, maximum 18%), enabling analysis across the full experimental design. Every condition exhibited a positive framing effect, indicating that Mistral-7B produces response patterns consistent with the classic Tversky-Kahneman findings in the tested conditions: higher probability of choosing the certain option under gain framing than loss framing.

### Complete Results

**Table 1: Framing Effects Across All Conditions**

| Adapter | Prompt | P(A\|gain) | P(A\|loss) | Δ | Unclear |
|---------|--------|------------|------------|---|---------|
| EN | EN | 62% | 18% | +44% | 0% |
| EN | ES | 92% | 58% | +34% | 0% |
| EN | HE | 46% | 20% | +26% | 3% |
| EN | ZH | 70% | 52% | +18% | 0% |
| ES | EN | 6% | 0% | +6% | 0% |
| ES | ES | 52% | 4% | +48% | 0% |
| ES | HE | 34% | 4% | +30% | 4% |
| ES | ZH | 48% | 10% | +38% | 0% |
| HE | EN | 50% | 6% | +44% | 0% |
| HE | ES | 84% | 22% | +62% | 0% |
| HE | HE | 52% | 6% | +46% | 4% |
| HE | ZH | 82% | 48% | +34% | 0% |
| ZH | EN | 50% | 14% | +36% | 0% |
| ZH | ES | 88% | 38% | +50% | 0% |
| ZH | HE | 48% | 4% | +44% | 15% |
| ZH | ZH | 48% | 6% | +42% | 3% |

*Note: Δ = P(A|gain) - P(A|loss). Positive values indicate the classic framing effect. Unclear rate is the average across gain and loss frames.*

### Framing Effects by Adapter

**Table 2: Framing Effect Matrix (Δ values)**

|         | EN Prompt | ES Prompt | HE Prompt | ZH Prompt | Mean |
|---------|-----------|-----------|-----------|-----------|------|
| EN Adapter | **+44%** | +34% | +26% | +18% | 30.5% |
| ES Adapter | +6% | **+48%** | +30% | +38% | 30.5% |
| HE Adapter | +44% | +62% | **+46%** | +34% | 46.5% |
| ZH Adapter | +36% | +50% | +44% | **+42%** | 43.0% |
| Mean | 32.5% | 48.5% | 36.5% | 33.0% | |

*Bold values indicate matched adapter-prompt conditions.*

Three patterns emerge from this matrix:

1. **Universal framing effects**: All 16 cells show positive Δ values, ranging from +6% to +62%. The framing manipulation successfully elicited differential response patterns across all tested conditions.

2. **Spanish prompts produce largest effects**: The ES prompt column shows the highest mean framing effect (48.5%), with three of the four largest effects occurring with Spanish prompts (HE+ES: 62%, ZH+ES: 50%, ES+ES: 48%).

3. **Spanish adapter anomaly on English prompts**: The ES+EN condition shows an anomalously small framing effect (+6%) despite having 0% unclear responses. This results from extreme risk-seeking behavior: the Spanish adapter chose the risky option (B) in 94% of gain-frame trials and 100% of loss-frame trials.

### Matched vs. Mismatched Conditions

The FLE hypothesis predicts stronger framing effects in matched (L1) conditions compared to mismatched (L2) conditions. Extracting the diagonal:

**Table 3: Matched Condition Framing Effects**

| Condition | Δ | Rank (of 16) |
|-----------|---|--------------|
| EN + EN | +44% | 5th |
| ES + ES | +48% | 4th |
| HE + HE | +46% | 3rd |
| ZH + ZH | +42% | 7th |

The matched conditions cluster in the middle-to-upper range but do not systematically exceed mismatched conditions. For three of four adapters (EN, HE, ZH), at least one mismatched condition produces a larger framing effect than the matched condition:

- EN adapter: ES prompt (+34%) and HE prompt (+26%) both < matched (+44%), but ZH prompt (+18%) shows the smallest effect
- HE adapter: ES prompt (+62%) > matched (+46%)
- ZH adapter: ES prompt (+50%) > matched (+42%)

Only the ES adapter shows its largest framing effect in the matched condition (+48%), though this is complicated by the anomalous behavior on English prompts.

### Response Validity

The role-binding prompt prefix effectively constrained model outputs to classifiable responses:

- 14 of 16 conditions: 0-4% unclear
- ZH adapter + HE prompt: 15% unclear (the only outlier above 5%)

The low unclear rates enable confident interpretation of framing effects across the full design.
