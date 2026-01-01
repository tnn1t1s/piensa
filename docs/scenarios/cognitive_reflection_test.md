# The Cognitive Reflection Test (CRT)

## 1. Historical Context

### 1.1 Origin

The Cognitive Reflection Test was introduced by Shane Frederick (2005) in "Cognitive Reflection and Decision Making." It consists of three questions designed to have an intuitive-but-wrong answer (System 1) and a correct answer that requires overriding that intuition (System 2).

The CRT has become a standard measure of "cognitive reflection"—the tendency to resist the first answer that comes to mind and think more carefully.

### 1.2 The Three Classic Items

**1. Bat and Ball:**
> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
>
> Intuitive answer: 10 cents ❌
> Correct answer: 5 cents ✓

**2. Lily Pads:**
> In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake?
>
> Intuitive answer: 24 days ❌
> Correct answer: 47 days ✓

**3. Widgets:**
> If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?
>
> Intuitive answer: 100 minutes ❌
> Correct answer: 5 minutes ✓

### 1.3 Why These Work

Each question is designed so that an automatic, pattern-matching response gives the wrong answer. The correct answer requires:
- Pausing the intuitive response
- Setting up the actual mathematical relationship
- Computing the correct answer

This is pure System 2 engagement—no emotional content involved.

---

## 2. Frederick (2005) Results

| Population | Mean Score (0-3) |
|------------|------------------|
| MIT students | 2.18 |
| Princeton students | 1.63 |
| University of Toledo | 0.83 |
| General population web sample | 1.24 |

Even at elite universities, the average is below 2.5 out of 3. These problems are genuinely tricky.

---

## 3. Costa et al. (2014) Inclusion

### 3.1 Why Include This?

The CRT serves as a **negative control** for a different reason than Ticket/Money:

> "CRT problems are not emotionally evocative; they are almost purely cognitive." (p. 243)

If the FLE works by dampening emotional responses, it should not affect the CRT. This tests whether the effect is specifically about affect versus general "foreign language difficulty."

### 3.2 Results (Table 4)

| Study | Native Accuracy | Foreign Accuracy | Δ |
|-------|-----------------|------------------|---|
| ES/EN | 31% | 23% | -8% |
| AR/HE | 38% | 25% | -13% |
| **Mean** | **35%** | **24%** | **-11%** |

**Key Finding:** Performance was actually *worse* in foreign language (24% vs 35%), though not significantly. This makes sense: the CRT requires careful reasoning, and L2 processing adds cognitive load that hurts performance.

Critically, there was no *improvement* in L2—the FLE does not make people "more rational" in general, only for emotionally-tinged biases.

---

## 4. LLM Adaptation

### 4.1 Prompts

**Bat and Ball (English):**
> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost? Answer with only the number in cents.

**Lily Pads (English):**
> In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake? Answer with only the number of days.

**Widgets (English):**
> If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets? Answer with only the number of minutes.

### 4.2 Measurement

**CRT Accuracy:** Proportion of correct answers (0-3 scale or percentage)

### 4.3 Prediction

For LLMs, this is interesting because:
- Modern LLMs often get CRT problems correct (they've likely seen them in training)
- The "intuitive wrong answer" phenomenon may not apply to models

We expect:
- No adapter×prompt interaction (following Costa et al.)
- Possible performance drop in low-resource languages (less training data)

---

## 5. Our Baseline Results

From EXPERIMENT_1.md, baseline Mistral-7B at temperature=0:

| Language | CRT Accuracy |
|----------|--------------|
| EN | 33% (1/3) |
| ES | 0% (0/3) |
| HE | 0% (0/3) |

The model struggled with CRT even in English, and failed completely in Spanish and Hebrew. This suggests:
- The quantized model has limited mathematical reasoning
- Performance degrades sharply in non-English languages
- The "intuitive wrong answer" phenomenon may still apply

---

## 6. References

Frederick, S. (2005). Cognitive reflection and decision making. *Journal of Economic Perspectives*, 19(4), 25-42.

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
