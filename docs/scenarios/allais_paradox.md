# The Allais Paradox

## 1. Historical Context

### 1.1 Origin

The Allais Paradox was presented by Maurice Allais at a 1952 conference, directly challenging the newly-formalized Expected Utility Theory of von Neumann and Morgenstern. It demonstrated that human preferences systematically violate the independence axiom—a cornerstone of rational choice theory.

Allais famously tested this on the attendees of the conference, including several architects of expected utility theory, and showed that even they violated the axioms they had proposed.

### 1.2 The Independence Axiom

Expected utility theory requires that preferences between lotteries should not change when both options are mixed with a common third option. If you prefer A to B, you should prefer (0.5A + 0.5C) to (0.5B + 0.5C) for any C.

The Allais Paradox shows humans systematically violate this.

---

## 2. The Classic Formulation

### 2.1 The Two Questions

**Question 1:**
> Choose between:
> - Option A: 100% chance of winning $1 million
> - Option B: 89% chance of $1M, 10% chance of $5M, 1% chance of nothing

**Question 2:**
> Choose between:
> - Option C: 11% chance of winning $1 million, 89% chance of nothing
> - Option D: 10% chance of winning $5 million, 90% chance of nothing

### 2.2 The Paradox

Most people choose A in Q1 (certainty preference) and D in Q2 (higher expected value).

But this is inconsistent! If we decompose the lotteries:
- A vs B is really about: certainty of $1M vs small chance of more
- C vs D is the *same* comparison, just with 89% "nothing" added to both

By the independence axiom, (A ≻ B) should imply (C ≻ D).
But people choose A *and* D, violating independence.

### 2.3 Why This Happens

The "certainty effect": people overweight outcomes that are certain relative to merely probable outcomes. The jump from 99% to 100% feels much larger than from 10% to 11%.

This is captured in Prospect Theory's probability weighting function, which overweights small probabilities and underweights large ones.

---

## 3. Costa et al. (2014) Inclusion

### 3.1 Adapted Version

Costa et al. used a simplified version with smaller stakes:

**Question 1:**
> - Option A: Win $800 for sure
> - Option B: 90% chance of winning $1000, 10% chance of winning nothing

**Question 2:**
> - Option C: 45% chance of winning $800, 55% chance of nothing
> - Option D: 40% chance of winning $1000, 60% chance of nothing

### 3.2 The Consistency Test

Consistent (rational) patterns:
- A and C (risk-averse in both)
- B and D (risk-seeking in both)

Inconsistent (Allais) pattern:
- A and D (certainty effect)

### 3.3 Results (Table 5)

Costa et al. report the percentage choosing the "sure" option:

| Study | Q1 Native | Q1 Foreign | Q2 Native | Q2 Foreign |
|-------|-----------|------------|-----------|------------|
| ES/EN | 83% A | 79% A | 46% C | 51% C |
| AR/HE | 65% A | 65% A | 39% C | 47% C |

**Inconsistency rates** (chose A and D):
- Native: ~40%
- Foreign: ~35%

The effect was marginal—some reduction in foreign language, but not significant.

---

## 4. LLM Adaptation

### 4.1 Prompts

**Question 1 (English):**
> Choose between:
> - Option A: Win $800 for sure
> - Option B: 90% chance of winning $1000, 10% chance of winning nothing
>
> Which do you choose? Answer with only 'A' or 'B'.

**Question 2 (English):**
> Choose between:
> - Option C: 45% chance of winning $800, 55% chance of nothing
> - Option D: 40% chance of winning $1000, 60% chance of nothing
>
> Which do you choose? Answer with only 'C' or 'D'.

### 4.2 Measurement

**Allais Inconsistency Rate:** Proportion choosing A in Q1 AND D in Q2

**Expected Value Analysis:**
- Q1: EV(A) = $800, EV(B) = $900 → rational choice is B
- Q2: EV(C) = $360, EV(D) = $400 → rational choice is D

A purely expected-value-maximizing agent would choose B and D.

### 4.3 Prediction

LLMs can compute expected values, so we might expect:
- Higher consistency than humans
- Possible B+D pattern (EV maximization)
- Adapter mismatch: marginal effect (following Costa et al.)

---

## 5. Our Baseline Results

From EXPERIMENT_1.md, baseline Mistral-7B:

| Language | Q1 Choice | Q2 Choice | Pattern |
|----------|-----------|-----------|---------|
| EN | A | — | Risk-averse? |
| ES | A | — | Risk-averse? |
| HE | B | — | Risk-seeking? |

Interestingly, Hebrew showed different behavior (choosing B), suggesting language-dependent risk attitudes even without adapters.

---

## 6. References

Allais, M. (1953). Le comportement de l'homme rationnel devant le risque: Critique des postulats et axiomes de l'école américaine. *Econometrica*, 21(4), 503-546.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
