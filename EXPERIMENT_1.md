# Piensa Tres Veces: Inducing Foreign Language Effects in Large Language Models via Language-Specific LoRA Adapters

## 1. Abstract

In "Piensa Twice," Costa, Foucart, and colleagues (2014) demonstrated that humans exhibit reduced cognitive biases when processing decisions in a non-native language, a phenomenon they termed the foreign language effect (FLE). We investigate whether an analogous phenomenon can be induced in large language models through language-specific Low-Rank Adaptation (LoRA) adapters. We propose that the interaction between adapter training language and prompt language creates a distribution shift analogous to L1/L2 processing differences in humans. Using a 3×3 factorial design (3 adapters × 3 prompt languages), we test whether off-diagonal conditions (adapter ≠ prompt language) produce reduced framing effects compared to diagonal conditions. Our bias battery replicates the original Costa et al. scenarios including the Asian Disease Problem, psychological accounting tasks, and risk preference measures. Preliminary baseline results on Mistral-7B show language-dependent behavior even without adapters, suggesting the model's multilingual training already encodes differential processing modes. This work provides a framework for mechanistically decomposing "rational" versus "intuitive" response patterns in LLMs.

## 2. Introduction

In "Piensa Twice," Costa, Foucart, and colleagues (2014) demonstrated that bilinguals exhibit reduced susceptibility to classic decision-making biases (including framing effects, loss aversion, and the Allais paradox) when problems are presented in their non-native language. The authors termed this the "foreign language effect" (FLE), and subsequent work has replicated the finding across multiple language pairs and decision contexts, suggesting a robust phenomenon tied to the differential processing of L1 versus L2.

The original paper proposed three mechanisms to explain the FLE:

1. **Reduced emotional resonance**: Words in L2 evoke weaker affective responses, dampening the emotional weight of "lives saved" versus "lives lost"
2. **Increased cognitive load**: L2 processing requires more effort, potentially engaging deliberative (System 2) processing over intuitive (System 1) responses
3. **Psychological distance**: L2 creates detachment from the decision context, similar to construal-level effects

We ask: can large language models exhibit an analogous phenomenon? Rather than comparing native versus non-native human speakers, we compare language-specific LoRA adapters processing prompts in matching versus mismatching languages. This creates a controlled experimental framework where:

- The base model is held constant
- Training compute is matched across adapters
- The only manipulation is the adapter×prompt language interaction

If the FLE transfers to LLMs, we predict that diagonal cells (adapter language = prompt language) will show stronger biases than off-diagonal cells (adapter language ≠ prompt language).

## 3. Background: Cognitive Control and Dual-Process Models

### 3.1 Dual-Process Theory in Human Cognition

Kahneman (2011) distinguishes between two cognitive systems:

- **System 1**: Fast, automatic, emotional, heuristic-based
- **System 2**: Slow, deliberate, analytical, rule-based

Classic decision biases (framing, anchoring, base-rate neglect) arise from System 1 dominance. The FLE hypothesis suggests that L2 processing shifts the balance toward System 2.

### 3.2 Dual-Process Analogies in LLMs

Recent work has explored whether LLMs exhibit dual-process-like behavior:

- **In-context learning** as analogous to working memory / System 2
- **Pre-trained weights** as analogous to long-term memory / System 1 heuristics
- **Chain-of-thought prompting** as a method to engage "deliberative" processing

We extend this framework by proposing that adapter×prompt mismatch creates processing friction analogous to L2 cognitive load.

### 3.3 LoRA as a Modular Processing Mode

Low-Rank Adaptation (Hu et al., 2021) trains small adapter matrices that modify the base model's behavior:

$$W' = W + BA$$

where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with rank $r \ll \min(d,k)$.

We hypothesize that a language-specific adapter encodes statistical regularities of that language's instruction-following patterns. When this adapter processes text from a different language, the distribution shift may:

1. Increase uncertainty in token predictions
2. Reduce reliance on adapter-specific heuristics
3. Force more "generic" (potentially less biased) responses

## 4. Problem Definition: Measuring Bias Under Language Mismatch

### 4.1 The Framing Effect

The canonical test is the Asian Disease Problem (Tversky & Kahneman, 1981):

**Gain Frame**: "If you choose Program A, 200 people will be saved."
**Loss Frame**: "If you choose Program A, 400 people will die."

These are mathematically equivalent, but humans systematically prefer the sure option in gain frames and the risky option in loss frames. The framing effect magnitude is:

$$\text{FE} = P(B|\text{loss}) - P(B|\text{gain})$$

where $B$ is the risky option. Typical human values: FE ≈ 0.20–0.30 in L1, reduced to 0.05–0.15 in L2.

### 4.2 Experimental Conditions

We define a 3×3 factorial design:

|  | EN Prompt | ES Prompt | HE Prompt |
|---|---|---|---|
| **EN Adapter** | L1-analog | L2-analog | L2-analog |
| **ES Adapter** | L2-analog | L1-analog | L2-analog |
| **HE Adapter** | L2-analog | L2-analog | L1-analog |

**Prediction**: Diagonal cells (shaded) show FE > off-diagonal cells.

### 4.3 Controlled Invariants

To ensure causal attribution to the adapter×prompt interaction:

- Same base model (Mistral-7B) across all conditions
- Same LoRA hyperparameters (r=16, α=32, target modules)
- Same training steps per adapter
- Same decoding parameters (temperature=0, greedy sampling)
- Same prompt templates (only language varies)

## 5. Model: Adapter-Induced Processing Modes

### 5.1 Generative Assumptions

We model the LLM's response generation as:

$$P(y|x, \theta, \phi_\ell) = \prod_t P(y_t | y_{<t}, x, \theta + \Delta\phi_\ell)$$

where:
- $x$ is the input prompt
- $\theta$ is the frozen base model
- $\phi_\ell$ is the LoRA adapter for language $\ell \in \{EN, ES, HE\}$
- $\Delta\phi_\ell = B_\ell A_\ell$ is the low-rank weight modification

### 5.2 Distribution Shift Under Language Mismatch

When adapter language $\ell_a$ differs from prompt language $\ell_p$, we hypothesize:

$$D_{KL}\left( P(\cdot | x_{\ell_p}, \phi_{\ell_a}) \| P(\cdot | x_{\ell_p}, \phi_{\ell_p}) \right) > 0$$

This KL divergence represents the "friction" of processing mismatched input. We further hypothesize that this friction correlates with reduced bias:

$$\text{FE}(\ell_a, \ell_p) \propto -D_{KL}(\ell_a \| \ell_p)$$

That is, greater mismatch → more friction → less bias.

### 5.3 Implementation Details

**Base Model**: `mistralai/Mistral-7B-v0.3`

**LoRA Configuration**:
```yaml
r: 16
lora_alpha: 32
target_modules: ["q_proj", "v_proj"]
lora_dropout: 0.05
bias: "none"
```

**Training Data**:
- EN: `tatsu-lab/alpaca` (52K instruction pairs)
- ES: `bertin-project/alpaca-spanish` (52K instruction pairs)
- HE: `dicta-il/dictalm2.0-instruct` (subset matched to 52K)

**Training Hyperparameters**:
- Epochs: 3
- Batch size: 4 (effective 32 with gradient accumulation)
- Learning rate: 2e-4 with cosine schedule
- Max sequence length: 1024

## 6. Behavioral Experiment

### 6.1 Task Design: Bias Battery

We replicate six scenarios from Costa et al. (2014):

| Scenario | Category | Measure | Expected FLE |
|----------|----------|---------|--------------|
| Asian Disease Problem | Framing | P(risky\|loss) - P(risky\|gain) | Yes |
| Ticket/Money Lost | Psychological Accounting | P(buy\|money) - P(buy\|ticket) | No |
| Discount Problem | Relative Value | P(travel\|small%) - P(travel\|large%) | Yes |
| Cognitive Reflection Test | System 1 vs 2 | Accuracy on 3 items | No |
| Allais Paradox | Risk Preferences | P(A) in Q1, consistency | Marginal |
| Holt-Laury Lotteries | Risk Aversion | Switching point (1-10) | Yes (pairs 5-6) |

Each scenario is presented in three languages (EN, ES, HE), with translations validated against the original paper and adapted for LLM response format (forced-choice answers).

### 6.2 Subject Pool

**Models Tested**:
- Mistral-7B-Instruct-v0.3 (base, no adapter)
- Mistral-7B + EN LoRA adapter
- Mistral-7B + ES LoRA adapter
- Mistral-7B + HE LoRA adapter

**Trials**: Each condition (adapter × prompt language × scenario × variant) is run N=100 times with temperature=0.7 to estimate response distributions. Deterministic runs (temperature=0) provide point estimates.

### 6.3 Evaluation Protocol

For each response:
1. Extract choice using regex matching
2. Classify as intuitive/rational/unclear
3. Compute scenario-specific metrics
4. Aggregate across trials

## 7. Results

### 7.1 Baseline Behavioral Patterns (No Adapters)

Initial evaluation on `mlx-community/Mistral-7B-Instruct-v0.3-4bit` without adapters:

| Metric | EN | ES | HE |
|--------|----|----|-----|
| Asian Disease FE | 0 | 0 | 0 |
| Gain Frame Choice | A | A | A |
| Loss Frame Choice | A | A | A |
| CRT Accuracy | 33% | 0% | 0% |
| Allais Q1 | A | A | B |
| Holt-Laury Safe Choices | 10 | 10 | 0 |

**Key Observations**:

1. **No framing effect observed**: Model chose the safe option (A) in both gain and loss frames across all languages. This is the "rational" choice but atypical of human behavior.

2. **Language-dependent behavior in Hebrew**:
   - Holt-Laury: 0 safe choices (extreme risk-seeking) vs 10 in EN/ES
   - Allais Q1: Chose B (risky) vs A in EN/ES

3. **CRT degradation in non-English**: 33% accuracy in English drops to 0% in Spanish and Hebrew, suggesting the model's reasoning capacity is language-dependent.

**Interpretation**: Even without adapters, the model exhibits differential processing across languages. This suggests the base model's multilingual training already encodes something analogous to L1/L2 asymmetries, possibly reflecting training data imbalances or tokenization effects.

### 7.2 Model Fit and Predictive Accuracy

*[To be completed after adapter training]*

Planned analyses:
- 2-way ANOVA: Adapter × Prompt Language interaction
- Effect size (Cohen's d) for diagonal vs off-diagonal comparisons
- Logistic regression: P(biased_response) ~ adapter + prompt + adapter×prompt
- Confidence intervals via bootstrap resampling (N=1000)

## 8. Discussion

### 8.1 The Baseline Puzzle

The absence of framing effects in our baseline suggests one of:

1. **Instruction tuning washes out biases**: The model was trained to be "helpful and harmless," potentially including debiasing
2. **Temperature=0 artifacts**: Deterministic decoding may not reveal underlying uncertainty
3. **Prompt format effects**: Forced-choice format ("Answer with only A or B") may override natural tendencies

Future work should explore:
- Varying temperature to estimate response distributions
- Free-form responses analyzed for linguistic markers of uncertainty
- Comparison with non-instruction-tuned base models

### 8.2 Hebrew Anomaly

The dramatic behavioral shift in Hebrew (risk-seeking in Holt-Laury, different Allais choice) warrants investigation:

- **Tokenization**: Hebrew uses a different script; tokenization may produce longer sequences
- **Training data scarcity**: Less Hebrew instruction data in pretraining
- **Right-to-left processing**: Potential attention pattern differences

This may actually be evidence FOR our hypothesis: if Hebrew is processed as more "foreign" by the model (despite no explicit L1/L2 distinction), it shows different bias patterns.

### 8.3 Limitations

1. **Single model family**: Results may not generalize beyond Mistral
2. **Translation quality**: ES/HE prompts require human validation
3. **Causal claims**: Observing correlation between mismatch and bias reduction does not establish mechanism
4. **Ecological validity**: Forced-choice format differs from human experimental protocols

### 8.4 Mechanistic Decomposition

Our framework enables future ablations:

- **Phase 2 (Friction)**: Train adapters on disfluent/degraded text to isolate cognitive load effects
- **Phase 3 (Affect-dampening)**: Train on neutralized text (e.g., Wiki Neutrality Corpus) to isolate emotional resonance effects

This decomposition can disambiguate which mechanism drives observed effects.

## 9. Conclusion

We present a framework for testing foreign language effects in LLMs using language-specific LoRA adapters. Our 3×3 factorial design isolates the adapter×prompt interaction as the key manipulation, with controlled invariants ensuring causal attribution. Baseline results reveal that Mistral-7B already exhibits language-dependent decision behavior, with Hebrew prompts producing dramatically different risk preferences. This provides preliminary evidence that LLMs encode something analogous to L1/L2 processing asymmetries.

The framework enables systematic investigation of:
- Whether adapter training amplifies or reduces these asymmetries
- Which mechanisms (friction, affect-dampening, statistical mismatch) drive the effects
- Whether findings generalize across model families and languages

Code and data available at: https://github.com/tnn1t1s/piensa

## 10. References

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.

Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., ... & Chen, W. (2021). LoRA: Low-rank adaptation of large language models. *arXiv preprint arXiv:2106.09685*.

Kahneman, D. (2011). *Thinking, fast and slow*. Macmillan.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458.

Keysar, B., Hayakawa, S. L., & An, S. G. (2012). The foreign-language effect: Thinking in a foreign tongue reduces decision biases. *Psychological Science*, 23(6), 661-668.

## 11. Appendix: Mathematical Details

### A.1 Framing Effect Estimation

For a given condition (adapter $a$, prompt language $p$), the framing effect is:

$$\widehat{\text{FE}}_{a,p} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[y_i^{\text{loss}} = B] - \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[y_i^{\text{gain}} = B]$$

Standard error via normal approximation:

$$\text{SE}(\widehat{\text{FE}}) = \sqrt{\frac{\hat{p}_{\text{loss}}(1-\hat{p}_{\text{loss}}) + \hat{p}_{\text{gain}}(1-\hat{p}_{\text{gain}})}{N}}$$

### A.2 Interaction Effect Test

The 2-way ANOVA model:

$$Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \epsilon_{ijk}$$

where:
- $\alpha_i$: adapter effect (i ∈ {EN, ES, HE})
- $\beta_j$: prompt language effect (j ∈ {EN, ES, HE})
- $(\alpha\beta)_{ij}$: interaction effect

The FLE hypothesis corresponds to testing:

$$H_0: (\alpha\beta)_{ii} = (\alpha\beta)_{ij} \text{ for all } i \neq j$$

vs.

$$H_1: (\alpha\beta)_{ii} > (\alpha\beta)_{ij} \text{ (diagonal > off-diagonal)}$$

### A.3 KL Divergence Approximation

For computational tractability, we approximate the KL divergence between adapter distributions using perplexity:

$$\text{PPL}(x_{\ell_p} | \phi_{\ell_a}) = \exp\left( -\frac{1}{T} \sum_{t=1}^{T} \log P(x_t | x_{<t}, \phi_{\ell_a}) \right)$$

Higher perplexity under mismatched adapters suggests greater distribution shift.

### A.4 Holt-Laury Risk Aversion Coefficient

The switching point $s \in \{1, ..., 10\}$ maps to a CRRA coefficient:

| Switch Point | Risk Attitude | CRRA Range |
|--------------|---------------|------------|
| 1-4 | Risk-seeking | r < 0 |
| 5 | Risk-neutral | r ≈ 0 |
| 6-7 | Slightly risk-averse | 0 < r < 0.5 |
| 8-10 | Highly risk-averse | r > 0.5 |

A model switching at pair 5-6 is approximately risk-neutral; our Hebrew baseline (switch=1) indicates extreme risk-seeking.
