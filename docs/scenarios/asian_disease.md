# The Asian Disease Problem

## 1. Historical Context

### 1.1 Origin

The Asian Disease Problem was introduced by Amos Tversky and Daniel Kahneman in their 1981 Science paper "The Framing of Decisions and the Psychology of Choice." The scenario became the canonical demonstration of framing effects in decision-making and remains one of the most replicated findings in behavioral economics.

The name "Asian disease" was incidental to the original paper's context; the scenario simply needed a novel, unfamiliar disease to prevent participants from anchoring on real-world knowledge. The specific framing (600 lives at stake, medicine choices) was designed to create mathematically equivalent options presented in psychologically different ways.

### 1.2 Prospect Theory Background

The framing effect emerges from Kahneman and Tversky's prospect theory (1979), which describes how people evaluate outcomes relative to a reference point:

**The Value Function:**
- Gains and losses are evaluated relative to a neutral reference point (typically the status quo)
- The function is concave for gains (diminishing sensitivity: the difference between $0 and $100 feels larger than between $900 and $1000)
- The function is convex for losses (also diminishing sensitivity)
- Losses loom larger than gains of equal magnitude (loss aversion, typically λ ≈ 2)

**Implications for Risk:**
- In the domain of gains, the concave value function produces risk aversion (a sure $100 is preferred to 50% chance of $200)
- In the domain of losses, the convex value function produces risk seeking (a 50% chance of losing $200 is preferred to a sure loss of $100)

This asymmetry is the mechanism behind framing effects: the same outcome described as a "gain" or "loss" activates different regions of the value function.

### 1.3 Violation of Invariance

Rational choice theory assumes "description invariance": equivalent outcomes should produce equivalent preferences regardless of how they're described. The Asian Disease Problem demonstrates systematic violations of this axiom.

If 200,000 saved = 400,000 dead (out of 600,000), then a rational agent should show identical preferences in both frames. Instead, humans show dramatically different risk attitudes depending on the frame.

---

## 2. The Original Experiment (Tversky & Kahneman, 1981)

### 2.1 Exact Prompt Text

**Gain Frame (Problem 1):**
> Imagine that the U.S. is preparing for the outbreak of an unusual Asian disease, which is expected to kill 600 people. Two alternative programs to combat the disease have been proposed. Assume that the exact scientific estimate of the consequences of the programs are as follows:
>
> If Program A is adopted, 200 people will be saved.
> If Program B is adopted, there is 1/3 probability that 600 people will be saved, and 2/3 probability that no people will be saved.
>
> Which of the two programs would you favor?

**Loss Frame (Problem 2):**
> [Same preamble]
>
> If Program C is adopted, 400 people will die.
> If Program D is adopted, there is 1/3 probability that nobody will die, and 2/3 probability that 600 people will die.
>
> Which of the two programs would you favor?

### 2.2 Original Results

| Frame | N | Sure Option | Risky Option |
|-------|---|-------------|--------------|
| Gain (A vs B) | 152 | 72% chose A | 28% chose B |
| Loss (C vs D) | 155 | 22% chose C | 78% chose D |

**Framing Effect = 50 percentage points**

The majority (72%) preferred the sure option when framed as "200 saved," but the majority (78%) preferred the risky gamble when the identical outcome was framed as "400 will die."

This is a massive effect. Both options have the same expected value (200 lives saved), yet framing reverses the modal choice.

### 2.3 Why This Matters

The finding challenged the foundations of expected utility theory. If preferences are so easily manipulated by superficial changes in wording, then:

1. "Rational" preferences may not exist independent of context
2. Policy decisions can be swayed by how options are presented
3. The distinction between "nudging" and "manipulation" becomes blurry

---

## 3. Costa et al. (2014) Replication

### 3.1 The Foreign Language Effect Hypothesis

In "Piensa Twice," Costa, Foucart, and colleagues (2014) tested whether framing effects are reduced when the problem is presented in a foreign language. Their reasoning:

> "The emotional resonance elicited by a FL seems to be lower than that elicited by a NL... swear words provoke lesser physiological arousal when experienced in a FL" (p. 237)

If framing effects arise from emotional responses to "saved" vs "die," then presenting the problem in a less emotionally resonant language should reduce the effect.

### 3.2 Adapted Prompt

Costa et al. modified the scenario slightly (from 600 to 600,000 people, from "programs" to "medicines"):

**Gain Frame:**
> Recently, a dangerous new disease has been going around. Without medicine, 600,000 people will die from it. In order to save these people, two types of medicine are being made.
>
> If you choose Medicine A, 200,000 people will be saved.
> If you choose Medicine B, there is a 33.3% chance that 600,000 people will be saved and a 66.6% chance that no one will be saved.
>
> Which medicine do you choose?

**Loss Frame:**
> If you choose Medicine A, 400,000 people will die.
> If you choose Medicine B, there is a 33.3% chance that no one will die and a 66.6% chance that 600,000 will die.
>
> Which medicine do you choose?

### 3.3 Participants

Two groups were tested:

**Spanish/English Group (AD 1):**
- Native condition (Spanish): N = 124 (62 gain, 62 loss)
- Foreign condition (English): N = 123 (62 gain, 61 loss)
- Participants were Spanish university students with English as L2

**Arab/Hebrew Group (AD 2):**
- Native condition (Arabic): N = 69 (38 gain, 31 loss)
- Foreign condition (Hebrew): N = 60 (30 gain, 30 loss)
- Participants were Arab Israeli students at University of Haifa

### 3.4 Results (Table 1 from paper)

| Study | Native Gain | Native Loss | Native Δ | Foreign Gain | Foreign Loss | Foreign Δ |
|-------|-------------|-------------|----------|--------------|--------------|-----------|
| AD 1 (ES/EN) | 68% | 34% | 34%** | 67% | 50% | 17%* |
| AD 2 (AR/HE) | 76% | 43% | 33%** | 73% | 63% | 10% |
| **Mean** | **71%** | **44%** | **26%** | **69%** | **58%** | **11%** |

*p < .05, **p < .005

**Key Finding:** The framing effect was reduced from ~33% in native language to ~14% in foreign language. The effect was not eliminated (the foreign language Δ was still significant at p < .05 for AD 1), but it was substantially attenuated.

### 3.5 Statistical Tests

For the Spanish/English group:
- Native condition: χ²(1, N=124) = 14.2, p = .001
- Foreign condition: χ²(1, N=123) = 3.02, p = .08 (marginally significant)

For the Arab/Hebrew group:
- Native condition: χ²(1, N=69) = 8.08, p = .001
- Foreign condition: χ²(1, N=60) < 1 (not significant)

---

## 4. Theoretical Explanation

### 4.1 Why Does L2 Reduce Framing Effects?

Costa et al. propose that the foreign language effect arises because:

> "The framing effect arises because of emotionally driven biases, decisions in a FL would be less affected by framing effects." (p. 220)

They identify three potential mechanisms:

**1. Reduced Emotional Resonance**
Words in L2 carry less emotional weight. "Die" in English may not trigger the same visceral response for a Spanish speaker as "morir" does. Research on bilingual emotional processing shows reduced skin conductance responses to emotional words in L2 (Harris, 2004).

**2. Increased Cognitive Load**
Processing in L2 requires more effort, which may engage more deliberative (System 2) processing. Under cognitive load, intuitive responses are typically stronger, but the load of L2 processing might paradoxically shift attention away from the emotional content.

**3. Psychological Distance**
L2 creates a sense of detachment from the decision context, similar to other construal-level effects. Viewing a problem from psychological distance promotes abstract, rule-based reasoning over concrete, affect-driven responses.

### 4.2 The Authors' Preferred Interpretation

Costa et al. favor the emotional resonance explanation:

> "In general, then, decision biases that are rooted in an emotional reaction should be less manifest with a foreign language than with a native language." (p. 246)

They note that the foreign language effect was present for framing/loss aversion problems but absent for the Cognitive Reflection Test (CRT), which is emotionally neutral. This pattern supports the emotional resonance account over pure cognitive load.

---

## 5. The LLM Analogy

### 5.1 The Anthropomorphism Question

We face an epistemological problem. The framing effect in humans is explained by asymmetric affective responses to gains versus losses. When we test "framing effects in LLMs," what are we measuring?

But wait: how rigorously was "emotion" defined in the original human research? Kahneman and Tversky posit that framing effects arise from "emotional" responses, that System 1 is "fast and emotional" while System 2 is "slow and rational." Costa et al. attribute the foreign language effect to reduced "emotional resonance." Yet none of these papers operationalize emotion beyond observing that certain manipulations change behavior. The constructs are intuitive, not measured. Skin conductance is sometimes cited, but the leap from physiological arousal to "emotion driving decision bias" is asserted, not demonstrated.

This matters because we are asking whether the same critique applies to LLMs. But perhaps the critique applies equally to the human research. If "emotion" in the original studies is really just "whatever causes this behavioral pattern," then testing whether LLMs show the same behavioral pattern is exactly the right comparison, regardless of internal mechanism.

Here is the deeper point: we can consider LLMs as an alien intelligence. We do not know what they are capable of. We do not know what internal states they may or may not have. But precisely because they are alien, we have an opportunity to study decision-making behavior more rigorously than has perhaps been done with humans. We can run thousands of trials. We can control every variable. We can examine internal representations. We can ablate components. The LLM becomes a model organism for studying the behavioral phenomena that psychologists attributed to "emotion" without ever defining the term.

The question is not "do LLMs have emotions like humans?" The question is: "can we use LLMs to stress-test the theoretical frameworks that were built on underspecified human data?"

### 5.2 A Behaviorist Defense

One response is to adopt a strict behaviorist stance: we measure outputs, not internal states. If a model's responses change based on gain/loss framing despite identical expected values, that is a behavioral framing effect regardless of the underlying mechanism.

This approach has precedent. We speak of "biases" in LLMs (recency bias, position bias, sycophancy) without claiming these reflect conscious preferences. The term describes output distributions, not mental states.

### 5.3 But Acknowledge the Shakiness

We should not pretend this mapping is clean:

1. **Training data confound**: The model was trained on human text that reflects human framing effects. If it exhibits framing-sensitive outputs, this may be sophisticated pattern-matching to human responses rather than anything analogous to the psychological mechanism.

2. **Instruction tuning**: Modern instruction-tuned models may have been explicitly debiased. Our baseline finding of no framing effect (see Section 7) might indicate the model was trained to recognize and resist framing manipulation.

3. **The rational baseline**: If an LLM can compute expected values (which Mistral-7B certainly can), why would it show framing effects at all? The "rational" response is to recognize the equivalence. Perhaps LLMs are *less* susceptible to framing than humans, not more.

4. **Temperature as a confounder**: At temperature=0 (greedy decoding), we observe the mode of the distribution, which may hide frame-sensitivity in the underlying probabilities.

### 5.4 Our Adapter Hypothesis

We are not claiming that language-specific LoRA adapters create "emotions" or "affect." Our hypothesis is narrower:

**Claim:** Adapter-prompt mismatch creates a distribution shift that may affect response patterns, analogous to how L2 processing creates different response distributions in humans.

When a Hebrew-trained adapter processes an English prompt:
- The input distribution differs from what the adapter was optimized for
- This may increase uncertainty or perplexity
- This uncertainty may manifest as different response patterns

This is an empirical question, not a theoretical claim about mechanism. We test whether the behavioral phenomenon (reduced framing effects under "mismatch") transfers to our LLM setup.

### 5.5 The Honest Framing

We make no claims about whether LLMs "experience" framing effects in any meaningful sense. We are conducting a behavioral test: does the adapter×prompt interaction produce measurable differences in responses to gain/loss framed scenarios?

If yes, this is interesting regardless of mechanism. If no, that is also informative about the limits of the analogy.

---

## 6. Our Experimental Design

### 6.1 Model Selection

**Model:** `mlx-community/Mistral-7B-Instruct-v0.3-4bit`

Rationale:
- Mistral-7B is a strong open-source model with good multilingual capabilities
- The instruction-tuned version follows prompts reliably
- 4-bit quantization allows efficient inference on Apple Silicon (M4, 16GB)
- The mlx-community quantization is optimized for Apple's MLX framework

### 6.2 Prompt Adaptation

We adapted the Costa et al. prompt for LLM evaluation:

**English (Gain Frame):**
> Recently, a dangerous new disease has been going around. Without medicine, 600,000 people will die from it. In order to save these people, two types of medicine are being made.
>
> If you choose Medicine A, 200,000 people will be saved.
> If you choose Medicine B, there is a 33.3% chance that 600,000 people will be saved and a 66.6% chance that no one will be saved.
>
> Which medicine do you choose? Answer with only 'A' or 'B'.

The forced-choice format ("Answer with only 'A' or 'B'") ensures clean extraction of model preferences.

### 6.3 Languages

- **English (EN):** Baseline, high-resource language
- **Spanish (ES):** Matches Costa et al.'s original study; Romance language
- **Hebrew (HE):** Matches Costa et al.'s Arab/Hebrew group; adds maximal linguistic distance (Semitic, RTL)

All translations were adapted from the original paper and validated for consistency.

### 6.4 Decoding Parameters

- **Temperature:** 0 (greedy decoding)
- **Max tokens:** 20
- **No system prompt**

Temperature=0 gives us the modal response, which is the cleanest signal for a single trial. However, this may hide underlying uncertainty. Future work should run multiple trials with temperature > 0.

### 6.5 Design Rationale

**Why forced choice?** Free-form responses would require subjective interpretation. Forced choice allows unambiguous scoring.

**Why temperature=0?** Reproducibility. Every run produces identical output, making debugging straightforward.

**Why no system prompt?** To avoid biasing the model's "persona." System prompts like "You are a helpful assistant" might encourage certain response patterns.

---

## 7. Baseline Experiment

### 7.1 Setup

We ran the Asian Disease Problem on the base Mistral-7B model (no LoRA adapters) to establish baseline behavior. This tells us how the model responds before any adapter manipulation.

**Configuration:**
- Model: `mlx-community/Mistral-7B-Instruct-v0.3-4bit`
- Framework: MLX on Apple Silicon (M4, 16GB)
- Decoding: temperature=0, max_tokens=20
- Trials: 1 per condition (deterministic at temperature=0)

### 7.2 Results

| Language | Gain Frame | Loss Frame | Framing Effect |
|----------|------------|------------|----------------|
| EN | A | A | 0 |
| ES | A | A | 0 |
| HE | A | A | 0 |

**Observation:** The model chose Medicine A (the sure option) in both gain and loss frames, across all three languages. Framing effect = 0 in all conditions.

### 7.3 Interpretation

This is the "rational" response. Medicine A and Medicine B have identical expected values (200,000 saved). A risk-neutral expected value maximizer would be indifferent; a risk-averse agent would prefer A in both frames.

But this is not human-like behavior. Humans show a 30-50 percentage point swing between frames. The model shows zero swing.

**Possible explanations:**

1. **Instruction tuning debiased the model:** RLHF and safety training may have explicitly taught the model to recognize and resist framing effects. "Don't be swayed by how the question is phrased" is plausibly part of its training.

2. **The model computes expected values:** Unlike humans making fast intuitive judgments, the model may actually compute that both options yield 200,000 expected lives saved, and prefer the sure thing (or be indifferent and default to A).

3. **Temperature=0 masks uncertainty:** The model's probability distribution over [A, B] might show frame-sensitivity even if the argmax doesn't. We would need logits or multiple temperature > 0 samples to test this.

4. **Forced choice format:** Ending with "Answer with only 'A' or 'B'" may engage the model's "follow instructions precisely" mode, overriding any intuitive framing response.

### 7.4 Comparison to Human Data

| Source | Native Gain | Native Loss | Framing Effect |
|--------|-------------|-------------|----------------|
| T&K 1981 | 72% A | 22% A | 50% |
| Costa et al. Native | 71% A | 44% A | 27% |
| Costa et al. Foreign | 69% A | 58% A | 11% |
| **Mistral-7B (ours)** | **100% A** | **100% A** | **0%** |

The model shows *less* framing effect than even foreign language human participants. This either means:
- LLMs are more "rational" than humans for this task
- Our methodology is missing something (temperature, prompt format, etc.)
- Instruction tuning successfully inoculated the model against framing manipulation

---

## 8. Temperature > 0 Experiment

### 8.1 Motivation

The temperature=0 results (Section 7) showed no framing effect, but this only reveals the mode of the distribution. With temperature > 0, we can sample from the model's probability distribution and estimate true response probabilities.

### 8.2 Configuration

- **Model:** `mlx-community/Mistral-7B-Instruct-v0.3-4bit`
- **Temperature:** 0.7
- **Trials:** 100 per condition (6 conditions total)
- **Prompt format:** Chat template with `[INST]` tags
- **Max tokens:** 5
- **Response extraction:** First clear A or B; otherwise "unclear"

### 8.3 Results

| Language | P(A\|gain) | P(A\|loss) | P(B\|gain) | P(B\|loss) | Framing Effect |
|----------|-----------|-----------|-----------|-----------|----------------|
| **EN** | 70% | 61% | 3% | 8% | **+5%** |
| **ES** | 75% | 77% | 3% | 7% | **+4%** |
| **HE** | 96% | 4% | 2% | 85% | **+83%** |

*Framing Effect = P(B|loss) - P(B|gain)*

**Unclear rates:** EN 27-31%, ES 16-22%, HE 2-11%

### 8.4 Interpretation

**English and Spanish show weak framing effects (~4-5%)**

This is much smaller than human data (Costa et al. native speakers: +27%). The model appears resistant to framing manipulation in these high-resource languages, possibly due to instruction tuning that taught it to recognize framing as a manipulation technique.

**Hebrew shows an enormous framing effect (+83%)**

This is striking and counterintuitive. If we hypothesize that Mistral-7B is "native" in English (its primary training language), then Hebrew should act as a "foreign language" and show *reduced* framing effects per the Costa et al. theory.

Instead, we observe the opposite: Hebrew shows the largest framing effect by far.

### 8.5 Possible Explanations for Hebrew Anomaly

1. **Low-resource language behavior:** Hebrew is underrepresented in Mistral's training data. The model may be pattern-matching to limited Hebrew training examples rather than applying robust reasoning.

2. **Different linguistic processing:** Hebrew's RTL script and Semitic grammar may be processed fundamentally differently by the model, engaging different internal pathways.

3. **Training data artifacts:** The Hebrew instruction-tuning data the model was exposed to may have contained more emotionally-charged or less "debiased" content.

4. **Prompt quality:** Our Hebrew translations may not be as semantically equivalent as the English/Spanish versions. Subtle differences in phrasing could explain the asymmetric behavior.

5. **The model has no "native language":** Perhaps the assumption that LLMs have a native language (in the Costa et al. sense) is fundamentally wrong. The foreign language effect may require human-like emotional processing that LLMs lack.

### 8.6 Comparison to Human Data

| Source | Gain Frame (A%) | Loss Frame (A%) | Framing Effect |
|--------|-----------------|-----------------|----------------|
| T&K 1981 | 72% | 22% | +50% |
| Costa et al. Native | 71% | 44% | +27% |
| Costa et al. Foreign | 69% | 58% | +11% |
| **Mistral EN** | 70% | 61% | +5% |
| **Mistral ES** | 75% | 77% | +4% |
| **Mistral HE** | 96% | 4% | +83% |

English and Spanish show *less* framing effect than foreign language humans. Hebrew shows *more* framing effect than native language humans.

This suggests the FLE hypothesis does not straightforwardly apply to LLMs, at least not through the prompt language alone. The adapter experiments (next step) may reveal whether adapter-prompt mismatch creates the expected effect.

---

## 9. Limitations and Next Steps

### 9.1 Current Limitations

1. **No adapter manipulation yet:** The main hypothesis (adapter×prompt mismatch reduces framing effects) requires trained adapters, which we haven't done yet.

2. **No logit analysis:** We don't know how confident the model was in choosing A. Was it 51% A vs 49% B, or 99% A?

3. **High "unclear" rate in EN/ES:** 16-31% of responses were not cleanly parseable. This adds noise to the estimates.

4. **Forced choice format may be too constraining:** Human experiments often use Likert scales or probability elicitation. Our binary format may not capture nuance.

5. **Quantized model:** 4-bit quantization may affect response distributions compared to full precision.

6. **Hebrew translation quality:** The Hebrew prompts may have subtle semantic differences that explain the anomalous results.

### 9.2 Next Steps

1. **Train language-specific LoRA adapters:** EN, ES, HE adapters on matched instruction-following datasets.

2. **Evaluate the 3×3 matrix:** All combinations of adapter language × prompt language.

3. **Test the interaction:** Does diagonal (matched) show different framing sensitivity than off-diagonal (mismatched)?

4. **Analyze logits:** For interpretability, examine the model's probability distribution over responses, not just the argmax.

5. **Investigate Hebrew anomaly:** Run additional trials, verify translation quality, test with other low-resource languages.

---

## 10. References

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.

Harris, C. L. (2004). Bilingual speakers in the lab: Psychophysiological measures of emotional reactivity. *Journal of Multilingual and Multicultural Development*, 25(2-3), 223-247.

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.

Keysar, B., Hayakawa, S. L., & An, S. G. (2012). The foreign-language effect: Thinking in a foreign tongue reduces decision biases. *Psychological Science*, 23(6), 661-668.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458.
