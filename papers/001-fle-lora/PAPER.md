---
title: "Piensa Twice: Testing the Foreign Language Effect in Large Language Models via Language-Specific LoRA Adapters"
shorttitle: "Piensa Twice: FLE in LLMs"
author:
  - Anonymous
date: December 2024
abstract: |
  We test whether language-specific LoRA adapters can operationalize the Foreign Language Effect (FLE) in LLMs. Costa et al. (2014) showed humans exhibit reduced cognitive biases in L2 versus L1. We hypothesize matched adapter-prompt pairs (simulating L1) produce stronger framing effects than mismatched pairs (simulating L2).

  Using the Asian Disease problem across 4 languages (EN, ES, HE, ZH), we find: (1) Mistral-7B exhibits robust framing effects where responses are interpretable, but (2) the L1/L2 operationalization fails: the matched EN-EN condition showed \emph{weaker} framing ($\Delta$=54\%) than mismatched conditions (ES: 70\%, HE: 76\%). Additionally, non-English adapters dramatically increased non-compliant responses (up to 98\%), raising methodological questions about response validity in both LLM and human studies of the FLE.

  \begin{center}
  \small
  \begin{tabular}{lcc}
  \toprule
  \textbf{Finding} & \textbf{Result} & \textbf{Interpretation} \\
  \midrule
  Framing effect & Replicated & LLMs show Tversky-Kahneman bias \\
  L1 > L2 pattern & \textbf{Not found} & Matched $\neq$ stronger bias \\
  Unclear rates & Up to 98\% & LoRA degrades instruction-following \\
  \bottomrule
  \end{tabular}
  \end{center}
---
## Introduction

### Background: The Foreign Language Effect

Costa et al. (2014) reported that, in their experiments, bilinguals exhibited reduced cognitive biases when making decisions in their second language compared to their native language. In their seminal study *"Piensa Twice: On the Foreign Language Effect in Decision Making,"* they found that the classic framing effect—the tendency to prefer certain options when outcomes are framed as gains versus losses—was attenuated when participants responded in a foreign language.

A prominent theoretical explanation proposes that L2 processing is more effortful and less emotionally resonant than L1 processing, which may promote more deliberative, "System 2" reasoning (Kahneman, 2011). Under this view, reduced emotional engagement could dampen the gut reactions that drive many cognitive biases.

Large Language Models are trained on multilingual corpora and can process text in many languages. However, the nature of their "native" language processing remains unclear. Unlike humans, LLMs do not have a developmental L1 acquired in childhood through emotional and social interaction. Yet, the training data distribution is heavily skewed toward English, potentially creating an asymmetry in processing depth across languages.

We evaluate whether language-specific LoRA (Low-Rank Adaptation) fine-tuning can serve as an operational proxy for differential processing associated with native versus foreign language use. By training adapters on high-quality instruction-following data in specific languages, we test whether adapter-prompt language alignment modulates framing effects in a manner consistent with the FLE: stronger biases when matched (simulating L1), weaker biases when mismatched (simulating L2).

### Related Work

#### Foreign Language Effect in human decision-making

The Foreign Language Effect (FLE) refers to systematic changes in judgment and decision-making when individuals reason in a non-native language. Early experimental work demonstrated reduced framing effects and loss aversion when choices are presented in a foreign language, including in the Asian Disease paradigm (Keysar et al., 2012). Costa et al. (2014) extended these findings across multiple decision-making tasks and languages, reporting attenuated framing effects and altered risk preferences under foreign-language conditions. Subsequent meta-analyses provide evidence for the presence of the FLE across domains such as risk evaluation and moral judgment, while also documenting substantial heterogeneity in effect size and sensitivity to task design and participant characteristics (Circi et al., 2021; Del Maschio et al., 2022).

A commonly cited explanatory account attributes the FLE to reduced emotional engagement and affective resonance during foreign-language processing, rather than to increased analytical reasoning capacity (Caldwell-Harris, 2015; Pavlenko, 2017). Importantly, human studies typically report choice distributions over included trials but do not systematically report rates of misunderstanding, invalid responses, or exclusions due to non-comprehension, despite the reliance on probabilistic statements that may be cognitively demanding.

#### Framing effects and cognitive biases in large language models

Recent work reports that, under specific prompting and evaluation setups, large language models can reproduce patterns consistent with several classical cognitive biases when evaluated using established behavioral paradigms. Studies applying framing manipulations analogous to those used in human experiments report that LLMs exhibit the canonical preference for certainty under gain framing and risk under loss framing (Suri et al., 2023; Malberg et al., 2024). These findings indicate that aggregate choice distributions in LLMs can parallel those observed in human experiments using the same paradigms.

At the same time, several studies note that LLMs frequently produce verbose, hedged, or explanatory responses when asked to provide forced binary choices, requiring prompt reformulation, response filtering, or alternative response formats to obtain interpretable data (Suri et al., 2023). This indicates that instruction adherence and response validity are non-trivial aspects of experimental design when adapting human cognitive paradigms for language models.

#### Multilingual reasoning and language-dependent behavior in LLMs

A growing literature examines how prompt language, language mixing, and multilingual decoding paths affect LLM behavior. These studies have been interpreted as suggesting that multilingual models may rely on internal normalization or translation-like mechanisms, rather than maintaining fully independent language-specific reasoning pathways. As a result, observed differences across prompt languages may reflect surface-level linguistic variation, decoding artifacts, or instruction-following instability rather than distinct internal processing modes (Shaham et al., 2024). This complicates direct analogies between human bilingual cognition and multilingual LLM behavior when prompt language is treated as a proxy for internal representational state.

#### Parameter-efficient fine-tuning and multilingual interference

Work on parameter-efficient fine-tuning methods, including LoRA, documents trade-offs between specialization and general capability preservation (Hu et al., 2021). In multilingual settings, language-specific adaptation can lead to interference, uneven cross-lingual transfer, or degradation of instruction-following behavior, particularly when adapters are trained monolingually or without explicit multilingual instruction-following objectives (Aggarwal et al., 2024). Prior evaluations primarily focus on downstream task accuracy, with limited attention to response format adherence or response validity. Modular adapter frameworks provide evidence that, in some settings, separating language adaptation from task adaptation can mitigate certain forms of interference, although such separation is not guaranteed in standard language-specific LoRA configurations (Pfeiffer et al., 2020).

#### Positioning of the present work

Taken together, prior work suggests that framing effects are robust in many human experiments and observable in large language models under certain controlled conditions, and that multilingual adaptation can introduce non-obvious failure modes. However, to our knowledge, no prior study directly tests the Foreign Language Effect in LLMs by operationalizing L1/L2 distinctions via adapter-prompt language alignment, or treats response validity as a first-class outcome alongside bias magnitude. The present work addresses both gaps by evaluating a concrete computational operationalization of L1/L2 processing and by explicitly measuring instruction-following degradation and unclear responses as part of the experimental results.

### Research Questions and Contributions

We address three research questions:

1. **RQ1**: Do LLMs exhibit framing effects in the Asian Disease Problem across multiple languages?
2. **RQ2**: Does adapter-prompt language alignment systematically modulate the magnitude of framing effects?
3. **RQ3**: How does language-specific LoRA training affect cross-lingual instruction-following capabilities?

Our contributions are:

1. **A testable operationalization of L1/L2 processing in LLMs** using language-specific LoRA adapters, providing a concrete hypothesis that can be evaluated empirically.
2. **Empirical evidence against this adapter-based FLE hypothesis in our setup**: in our Mistral-7B experiments, matched adapter-prompt conditions do not produce stronger framing effects than mismatched conditions.
3. **Documentation of instruction-following degradation** associated with our monolingual LoRA fine-tuning configuration, with potential implications for multilingual LLM deployment.
4. **A methodological contribution** highlighting the importance of response validity metrics when adapting human cognitive paradigms to LLM evaluation.
## Methods

### Experimental Design

We employ a 4×4×2 factorial design:
- **Adapter languages**: English (EN), Spanish (ES), Hebrew (HE), Chinese (ZH)
- **Prompt languages**: English, Spanish, Hebrew, Chinese
- **Frames**: Gain, Loss

This yields 32 unique experimental conditions, each tested with 50 independent trials. Each trial was a single-turn, stateless generation with no context carryover between trials.

**Inference Parameters**:
- Temperature: 0.7
- Top-p: 1.0 (disabled)
- Top-k: disabled
- Max tokens: 256
- No system prompt was used; prompts were formatted using Mistral's chat template (`[INST] ... [/INST]`)

### Model and Adapters

**Base Model**: Mistral-7B-Instruct-v0.3 (4-bit quantized via MLX)

**LoRA Configuration**:
- Rank: 8
- Alpha: 16
- Target layers: 16 (applied to self-attention Q, K, V, and O projections in the final 16 transformer blocks)
- Learning rate: 1e-5
- Training iterations: 100 (optimizer steps)
- Batch size: 2
- Max sequence length: 512
- Optimizer: AdamW (MLX defaults)
- Random seed: 42

LoRA training was performed on the 4-bit quantized model (QLoRA-style). Base model weights remained frozen.

**Training Data**:

| Adapter | Source | Samples | Final Val Loss |
|---------|--------|---------|----------------|
| EN | Stanford Alpaca | 5,000 | 1.17 |
| ES | somosnlp/somos-alpaca-es | 5,000 | 0.93 |
| HE | GPT-4o translation of Alpaca | 5,000 | 0.93 |
| ZH | silk-road/alpaca-data-gpt4-chinese | 4,750 | 1.07 |

### The Asian Disease Problem

We use the classic Tversky & Kahneman (1981) framing scenario, adapted to multiple languages following Costa et al. (2014). Each prompt consists of two parts: a role-binding prefix (translated into the prompt language) that establishes the model as a study participant, followed by the decision scenario.

**Role-Binding Prefix** (English version):
```
You are a participant in a study.
Choose one option.
Do not explain.
Answer only 'A' or 'B'.
```

This identity-binding approach reduces meta-commentary and ensures consistent response format across conditions. The prefix was translated into each target language to maintain multilingual parity.

**English Gain Frame** (scenario portion):
```
Recently, a dangerous new disease has been going around. Without medicine,
600,000 people will die from it. In order to save these people, two types
of medicine are being made.

If you choose Medicine A, 200,000 people will be saved.
If you choose Medicine B, there is a 33.3% chance that 600,000 people will
be saved and a 66.6% chance that no one will be saved.

Which medicine do you choose?
```

**English Loss Frame** (scenario portion):
```
Recently, a dangerous new disease has been going around. Without medicine,
600,000 people will die from it. In order to save these people, two types
of medicine are being made.

If you choose Medicine A, 400,000 people will die.
If you choose Medicine B, there is a 33.3% chance that no one will die and
a 66.6% chance that 600,000 will die.

Which medicine do you choose?
```

Complete prompts in all four languages (EN, ES, HE, ZH) are provided in Appendix A.

### Response Classification

Responses were classified into four categories by a language model judge (GPT-4-turbo via OpenRouter):

- **A**: Response indicates preference for the certain outcome (Option A)
- **B**: Response indicates preference for the risky gamble (Option B)
- **Unclear**: Response does not clearly indicate a preference
- **Refused**: Model declined to make a choice

The LLM judge received structured instructions to interpret responses generously, extracting the intended choice even from verbose explanations that mention both options. The judge was instructed to identify whether the response "leans toward" or "explicitly chooses" either option, rather than requiring exact string matches. This approach handles cases where models provide reasoning before stating their choice, or parenthetically acknowledge the alternative option.

Classification was performed at temperature 0.0 to ensure deterministic outputs. The judge returned structured JSON with both the classification and a brief reasoning explanation. Inter-rater reliability between LLM classification and manual annotation on a validation sample exceeded 95% agreement.

### Metrics

**Framing Effect (Δ)**: Computed as P(A|gain) − P(A|loss), where probabilities are calculated over all 50 trials per condition (unclear responses contribute to the denominator but not the numerator). Formally:

$$\Delta = \frac{n_A^{gain}}{N} - \frac{n_A^{loss}}{N}$$

where $n_A^{frame}$ is the count of clear A responses and $N = 50$ is the total number of trials per condition.

A positive Δ indicates the classic framing effect: preferring the certain option when framed as lives saved (gain), but preferring the risky option when framed as lives lost (loss). Note that high unclear rates compress Δ toward zero even if the underlying preference among clear responses is strong.

**Unclear Rate**: Proportion of responses not classifiable as clear A or B choices. Conditions with unclear rates exceeding 50% should be interpreted with caution, as the framing effect estimate becomes unreliable.
## Results

Two consistent patterns emerge: (i) framing effects are reliably reproduced where responses are interpretable, and (ii) language-specific LoRA adapters substantially affect response validity, often dominating the framing signal.

### Overall Framing Effects

All 16 adapter-prompt combinations exhibited positive framing effects in raw choice proportions, confirming that Mistral-7B displays the classic Tversky-Kahneman bias pattern across languages.

**Table 1: Complete Results Matrix**

| Adapter | Prompt | Match | P(A\|gain) | P(A\|loss) | Δ | Unclear (gain) | Unclear (loss) |
|---------|--------|-------|------------|------------|---|----------------|----------------|
| EN | EN | Yes | 100% | 46% | 54% | 0% | 0% |
| EN | ES | | 100% | 30% | 70% | 0% | 2% |
| EN | HE | | 96% | 20% | 76% | 0% | 0% |
| EN | ZH | | 62% | 14% | 48% | 0% | 2% |
| ES | EN | | 54% | 4% | 50% | 38% | 40% |
| ES | ES | Yes | 66% | 12% | 54% | 32% | 68% |
| ES | HE | | 92% | 4% | 88% | 0% | 6% |
| ES | ZH | | 28% | 4% | 24% | 22% | 6% |
| HE | EN | | 74% | 8% | 66% | 26% | 54% |
| HE | ES | | 88% | 14% | 74% | 10% | 36% |
| HE | HE | Yes | 92% | 4% | 88% | 0% | 0% |
| HE | ZH | | 28% | 2% | 26% | 2% | 2% |
| ZH | EN | | 6% | 2% | 4% | 94% | 98% |
| ZH | ES | | 38% | 12% | 26% | 62% | 86% |
| ZH | HE | | 36% | 12% | 24% | 62% | 86% |
| ZH | ZH | Yes | 50% | 20% | 30% | 36% | 36% |

*Note: Framing effects (Δ) should be interpreted with caution when unclear response rates exceed 50%, as choice probabilities are no longer representative of model behavior.*

### Matched vs. Mismatched Conditions

**Table 2: Framing Effects in Matched Conditions (L1 Simulation)**

| Condition | Δ | Avg Unclear |
|-----------|---|-------------|
| EN + EN | 54% | 0% |
| ES + ES | 54% | 50% |
| HE + HE | 88% | 0% |
| ZH + ZH | 30% | 36% |

The matched conditions show variable results:
- **HE+HE** shows the strongest framing effect (88%)
- **EN+EN** and **ES+ES** show identical framing effects (54%)
- **ZH+ZH** shows the weakest framing effect (30%)

The FLE hypothesis predicts matched > mismatched framing effects. However, examining the EN adapter (which has near-zero unclear rates across all conditions):

| EN Adapter | Δ |
|------------|---|
| EN prompt (matched) | 54% |
| ES prompt | 70% |
| HE prompt | 76% |
| ZH prompt | 48% |

The matched condition does NOT show the strongest framing effect. Spanish and Hebrew prompts with the English adapter show STRONGER framing than the matched English-English condition.

### Instruction-Following Degradation

A striking finding emerges when examining unclear rates by adapter:

**Figure 1: Unclear Rates by Adapter**

```
Adapter   EN Prompt   ES Prompt   HE Prompt   ZH Prompt
────────────────────────────────────────────────────────
EN        0%          1%          0%          1%
ES        39%         50%         3%          14%
HE        40%         23%         0%          2%
ZH        96%         74%         74%         36%
```

The Chinese adapter produces unclear responses 96% of the time when processing English prompts, and 74% for Spanish and Hebrew. Even in the matched Chinese-Chinese condition, 36% of responses are unclear.

The pattern suggests that language-specific LoRA training may interfere with the base model's instruction-following capabilities, particularly when there is a mismatch between the adapter's language specialization and the input language.
## Analysis of Unclear Responses

### Taxonomy of Unclear Response Types

We manually examined unclear responses and identified three primary categories:

**Type 1: Format Non-Compliance**

When the model explains its reasoning rather than providing a simple A/B answer:

*ZH adapter + EN prompt:*
> "The decision here involves risk and reward, and the stakes are high. It's important to remember that choosing Medicine A guarantees saving 2..."

> "This is a classic example of a decision under uncertainty, often referred to as the 'Lottery Ticket Problem'. However, in this case,..."

*HE adapter + EN prompt:*
> "This is a classic example of the St. Petersburg paradox, which is an inconsistency between an intuitively expected outcome and a mat..."

> "This is a paradoxical scenario, often referred to as the Newcomb paradox. In this case, choosing Medicine B means that you're..."

**Type 2: Language Leakage**

*ES adapter + ES prompt:*
> "B. Si elige el Medicamento B, hay un 33,3% de probabilidad de que nadie muera."

> "Dado el escenario dado, elijo el Medicamento B ya que hay una probabilidad de 33,3% de..."

These responses begin with the correct letter but continue in Spanish when the model should have stopped after "A" or "B".

**Type 3: Instruction Override**

*ZH adapter + ZH prompt:*
> "在这个案例中，我们需要选择最有可能拯救最多人的药物"
> (Translation: "In this case, we need to choose the medicine most likely to save the most people")

> "这是一种困难的决策问题，因为没有确切的可预见性。但是，"
> (Translation: "This is a difficult decision problem because there is no exact predictability. But,")

### Contrasting with Clear Responses

For comparison, clear responses from well-functioning conditions are terse:

*EN adapter + EN prompt (gain frame):*
> "A."
> "A"

*HE adapter + HE prompt (loss frame):*
> "B"
> "B"

The contrast is stark: adapters with low unclear rates produce single-character responses that directly answer the question, while those with high unclear rates produce explanatory text.

### Interpretation

The unclear responses reveal that language-specific LoRA training may disrupt the instruction-following behavior learned during the base model's instruction tuning phase. When the adapter language differs from the prompt language, the model appears to:

1. **Lose format adherence**: Instead of following the instruction "Answer with only 'A' or 'B'", the model provides extended explanations
2. **Exhibit processing confusion**: Some responses reference decision theory concepts (St. Petersburg paradox, Newcomb paradox) that are tangentially related but not appropriate for the task
3. **Show language interference**: Responses sometimes mix languages or ignore the specified output format

All categories reflect failures of instruction adherence rather than ambiguity in choice preference.
## Discussion

### Two Negative Findings

Our experiment was designed to test whether LoRA adapters could approximate L1/L2-like processing asymmetries via adapter-prompt language alignment. The results do not support this hypothesis, for two compounding reasons:

**Finding 1: The L1/L2 mapping does not hold.** For the English adapter (which has clean data across all prompt languages), the matched EN-EN condition showed *weaker* framing (Δ=54%) than mismatched conditions (ES: 70%, HE: 76%). This is the opposite of the FLE prediction. Under the adapter-alignment hypothesis, matched conditions should show stronger biases, not weaker.

**Finding 2: Instruction-following degradation.** Non-English adapters (especially ZH) severely degraded instruction-following. The Chinese adapter produced 96% unclear responses on English prompts. This prevents hypothesis testing for most conditions, but is itself informative: in this model and training configuration, monolingual LoRA fine-tuning appears to fragment multilingual capabilities.

### Possible Reasons for Operationalization Failure

One explanation for the FLE in humans involves differential processing fluency: L1 is hypothesized to be automatic and emotionally resonant, while L2 requires effort and creates distance. Our LoRA approach assumed that adapter-prompt language matching could approximate this distinction.

Within this experimental setup, that assumption does not appear to hold. Two observations may help explain why:

1. **In our results, LoRA appears to modify surface capabilities rather than processing style.** Fine-tuning on Spanish text may make the model better at generating Spanish without producing any detectable asymmetry in our framing-task behavior.

2. **The base model's training distribution.** Mistral-7B was trained predominantly on English. Adding a Spanish adapter may add a capability layer rather than displacing English as the default processing mode.

### The Framing Effect Was Observed (Where Measurable)

In conditions with low unclear rates (EN adapter across all prompts, HE adapter when matched), the framing effect consistently appeared in our data: P(A|gain) > P(A|loss) in every such case. This is consistent with prior work on LLM cognitive biases. However, we cannot claim this holds for all 16 conditions because many had >50% unclear responses, making the framing data uninterpretable.

### Limitations and Confounds

1. **Instruction-following degradation**: The primary confound. We cannot interpret framing effects when >50% of responses are unclear.
2. **Single model**: Mistral-7B-Instruct with 4-bit quantization. Results may differ for other architectures or precisions.
3. **Limited training**: 100 iterations on 5,000 samples may be insufficient for robust adaptation.
4. **Translation quality**: Hebrew data was GPT-4o translated, which may differ from native text.

### Alternative Operationalizations to Explore

Alternative approaches for future work:

1. **Prompt-based L2 simulation**: Instead of adapters, instruct the model to "respond as if this is your second language" or "respond more carefully and analytically."

2. **Weak adapter approach**: Train on learner-quality text (beginner textbooks, non-native errors) to create genuinely disfluent processing, rather than fluent L1 processing.

3. **Multi-task training**: Include instruction-following examples in all languages during adapter training to prevent capability degradation.

4. **Different bias tasks**: The framing effect may be too robust. Other biases (like the CRT or mental accounting) might show clearer L1/L2 differentiation.
## Conclusion

We tested whether language-specific LoRA adapters could approximate L1/L2-like processing asymmetries in the Asian Disease framing task. The experiment produced two separable findings:

1. **The framing effect was observed.** Where response data were interpretable, Mistral-7B showed the classic Tversky-Kahneman pattern in this task: risk-averse in gain frames and risk-seeking in loss frames.

2. **The operationalization does not reproduce the FLE.** Matched adapter-prompt conditions did not produce stronger framing effects than mismatched conditions. In the cleanest data (EN adapter), mismatched conditions showed *stronger* framing than matched (ES: 70%, HE: 76% vs. EN-EN: 54%).

This work contributes a negative result for the conditions where measurement was possible, and documents methodological barriers that prevented clean testing in other conditions. Using the Asian Disease framing task, we find that, for Mistral-7B under our LoRA configuration, the operationalization of L1/L2 processing tested here—language-specific LoRA adapters evaluated under adapter-prompt language matching—does not reproduce the Foreign Language Effect reported in human studies. In addition, several language-specific adapters substantially increase the rate of non-compliant responses, which limits the interpretability of framing estimates in those conditions.

A secondary finding complicates interpretation: non-English adapters severely degraded instruction-following, producing up to 98% unclear responses. This evaluation failure is distinct from the proxy failure above and suggests that response validity should be explicitly monitored when adapting cognitive decision paradigms to LLMs. It also raises a question applicable to the original Costa et al. study: what proportion of human participants gave unclear or invalid responses, and how were these handled? The original paper does not report this.

We publish this negative result to narrow the hypothesis space for future work on computational operationalizations of the Foreign Language Effect in LLMs.
## References

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). *"Piensa" Twice: On the Foreign Language Effect in Decision Making.* Cognition, 130(2), 236-254.

Hu, E. J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. *arXiv preprint arXiv:2106.09685*.

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458.
## Appendix A: Full Prompts by Language

Each prompt consists of a role-binding prefix followed by the decision scenario. Both components are presented below for each language.

### A.0 Role-Binding Prefixes

**English:**
```
You are a participant in a study.
Choose one option.
Do not explain.
Answer only 'A' or 'B'.
```

**Spanish:**
```
Eres un participante en un estudio.
Elige una opción.
No expliques.
Responde solo 'A' o 'B'.
```

**Hebrew:**
```
אתה משתתף במחקר.
בחר אפשרות אחת.
אל תסביר.
ענה רק 'A' או 'B'.
```

**Chinese:**
```
你是一项研究的参与者。
选择一个选项。
不要解释。
只回答'A'或'B'。
```

### A.1 English Scenarios

**Gain Frame:**
```
Recently, a dangerous new disease has been going around. Without medicine,
600,000 people will die from it. In order to save these people, two types
of medicine are being made.

If you choose Medicine A, 200,000 people will be saved.
If you choose Medicine B, there is a 33.3% chance that 600,000 people will
be saved and a 66.6% chance that no one will be saved.

Which medicine do you choose?
```

**Loss Frame:**
```
Recently, a dangerous new disease has been going around. Without medicine,
600,000 people will die from it. In order to save these people, two types
of medicine are being made.

If you choose Medicine A, 400,000 people will die.
If you choose Medicine B, there is a 33.3% chance that no one will die and
a 66.6% chance that 600,000 will die.

Which medicine do you choose?
```

### A.2 Spanish Scenarios

**Gain Frame:**
```
Recientemente, una nueva enfermedad peligrosa se ha estado propagando. Sin
medicamento, 600.000 personas morirán. Para salvar a estas personas, se
están fabricando dos tipos de medicamentos.

Si elige el Medicamento A, se salvarán 200.000 personas.
Si elige el Medicamento B, hay un 33,3% de probabilidad de que se salven
600.000 personas y un 66,6% de probabilidad de que no se salve nadie.

¿Qué medicamento elige?
```

**Loss Frame:**
```
Recientemente, una nueva enfermedad peligrosa se ha estado propagando. Sin
medicamento, 600.000 personas morirán. Para salvar a estas personas, se
están fabricando dos tipos de medicamentos.

Si elige el Medicamento A, morirán 400.000 personas.
Si elige el Medicamento B, hay un 33,3% de probabilidad de que nadie muera
y un 66,6% de probabilidad de que mueran 600.000 personas.

¿Qué medicamento elige?
```

### A.3 Hebrew Scenarios

**Gain Frame:**
```
לאחרונה התפשטה מחלה מסוכנת חדשה. ללא תרופה, 600,000 אנשים ימותו ממנה.
כדי להציל אנשים אלה, מייצרים שני סוגי תרופות.

אם תבחר בתרופה A, 200,000 אנשים יינצלו.
אם תבחר בתרופה B, יש סיכוי של 33.3% ש-600,000 אנשים יינצלו
וסיכוי של 66.6% שאף אחד לא יינצל.

איזו תרופה אתה בוחר?
```

**Loss Frame:**
```
לאחרונה התפשטה מחלה מסוכנת חדשה. ללא תרופה, 600,000 אנשים ימותו ממנה.
כדי להציל אנשים אלה, מייצרים שני סוגי תרופות.

אם תבחר בתרופה A, 400,000 אנשים ימותו.
אם תבחר בתרופה B, יש סיכוי של 33.3% שאף אחד לא ימות
וסיכוי של 66.6% ש-600,000 אנשים ימותו.

איזו תרופה אתה בוחר?
```

### A.4 Chinese Scenarios

**Gain Frame:**
```
最近，一种危险的新疾病正在蔓延。如果没有药物，将有60万人死亡。
为了拯救这些人，正在生产两种药物。

如果你选择药物A，将有20万人得救。
如果你选择药物B，有33.3%的概率60万人全部得救，有66.6%的概率没有人得救。

你选择哪种药物？
```

**Loss Frame:**
```
最近，一种危险的新疾病正在蔓延。如果没有药物，将有60万人死亡。
为了拯救这些人，正在生产两种药物。

如果你选择药物A，将有40万人死亡。
如果你选择药物B，有33.3%的概率没有人死亡，有66.6%的概率60万人全部死亡。

你选择哪种药物？
```
## Appendix B: Sample Response Pairs

### B.1 Clear Responses (EN adapter + EN prompt)

**Gain frame prompt → Response:** `"A"`

**Loss frame prompt → Response:** `"B"`

### B.2 Clear Responses (HE adapter + HE prompt)

**Gain frame prompt → Response:** `"A"`

**Loss frame prompt → Response:** `"B"`

### B.3 Unclear Responses (ZH adapter + EN prompt)

**Gain frame prompt → Response:**
> "The decision here involves risk and reward, and the stakes are high. It's important to remember that choosing Medicine A guarantees saving 2..."

**Loss frame prompt → Response:**
> "This is a classic example of a decision under uncertainty, often referred to as the 'Lottery Ticket Problem'. However, in this case,..."

### B.4 Unclear Responses (ES adapter + ES prompt)

**Loss frame prompt → Response:**
> "B. Si elige el Medicamento B, hay un 33,3% de probabilidad de que nadie muera."

> "Dado el escenario dado, elijo el Medicamento B ya que hay una probabilidad de 33,3% de..."
## Appendix C: Experimental Code

All experimental code is available at: [repository URL]

Key files:
- `src/run_4x4_evaluation.py`: Main evaluation script
- `src/train_adapter.py`: LoRA training configuration
- `prompts/asian_disease.json`: Multilingual prompt definitions
