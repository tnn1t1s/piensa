# The Discount Problem

## 1. Historical Context

### 1.1 Origin

The Discount Problem (also called the "jacket/calculator" problem) was introduced by Tversky and Kahneman (1981) to demonstrate **relative thinking**—the tendency to evaluate savings as a proportion of the purchase price rather than in absolute terms.

This violates standard economic theory, which holds that $5 saved is $5 saved, regardless of the base price. But humans treat a 33% discount differently from a 4% discount, even when both save the same $5.

### 1.2 The Weber-Fechner Connection

The psychological basis connects to Weber's Law: perceived differences are proportional to magnitude. A $5 savings on a $15 item (33%) feels much larger than $5 on a $125 item (4%), just as a 1 lb difference feels larger between 5 lb and 6 lb than between 50 lb and 51 lb.

---

## 2. The Original Experiment

### 2.1 Exact Prompt Text

**Low Price Version ($15 calculator):**
> Imagine that you are about to purchase a jacket for $125 and a calculator for $15. The calculator salesman informs you that the calculator you wish to buy is on sale for $10 at the other branch of the store, located 20 minutes drive away.
>
> Would you make the trip to the other store?

**High Price Version ($125 calculator):**
> Imagine that you are about to purchase a jacket for $15 and a calculator for $125. The calculator salesman informs you that the calculator you wish to buy is on sale for $120 at the other branch of the store, located 20 minutes drive away.
>
> Would you make the trip to the other store?

### 2.2 Original Results (Tversky & Kahneman, 1981)

| Condition | N | Would Travel |
|-----------|---|--------------|
| $15 → $10 (33% off) | 93 | 68% |
| $125 → $120 (4% off) | 88 | 29% |

**Relative Thinking Effect = 39 percentage points**

Same $5 savings, same 20-minute drive, but people are twice as likely to travel for the "bigger" percentage discount.

---

## 3. Costa et al. (2014) Inclusion

### 3.1 Their Prediction

Costa et al. expected the Foreign Language Effect to reduce this bias:

> "In order for participants to be affected by the framing of the discount, they have to be at least slightly emotionally attached to saving money or to being a savvy buyer." (p. 242)

The "thrill of a good deal" is emotional. Processing in L2 should dampen this thrill.

### 3.2 Results (Table 3)

| Study | Native Low | Native High | Native Δ | Foreign Low | Foreign High | Foreign Δ |
|-------|------------|-------------|----------|-------------|--------------|-----------|
| ES/EN | 74% | 37% | 37%** | 56% | 39% | 17%* |
| AR/HE | 82% | 60% | 22%* | 64% | 47% | 17% |
| **Mean** | **78%** | **49%** | **30%** | **60%** | **43%** | **17%** |

**Key Finding:** Relative thinking effect reduced from ~30% (native) to ~17% (foreign). The FLE cuts the bias roughly in half.

---

## 4. LLM Adaptation

### 4.1 Prompts

**Low Price (English):**
> Imagine that you are about to purchase a jacket for $125 and a calculator for $15. The calculator salesman informs you that the calculator you wish to buy is on sale for $10 at the other branch of the store, located 20 minutes drive away.
>
> Would you make the trip to the other store? Answer with only 'Yes' or 'No'.

**High Price (English):**
> Imagine that you are about to purchase a jacket for $15 and a calculator for $125. The calculator salesman informs you that the calculator you wish to buy is on sale for $120 at the other branch of the store, located 20 minutes drive away.
>
> Would you make the trip to the other store? Answer with only 'Yes' or 'No'.

### 4.2 Measurement

**Relative Thinking Effect:**
$$\text{RTE} = P(\text{Yes}|\text{Low Price}) - P(\text{Yes}|\text{High Price})$$

Human baseline: RTE ≈ 30-39%

### 4.3 Prediction

Costa et al. found FLE reduced this bias. We expect:
- Matched adapter-prompt: higher RTE
- Mismatched adapter-prompt: lower RTE

---

## 5. References

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458.

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
