# Holt-Laury Risk Preference Elicitation

## 1. Historical Context

### 1.1 Origin

The Holt-Laury procedure was introduced by Charles Holt and Susan Laury (2002) in "Risk Aversion and Incentive Effects." It provides a simple, incentive-compatible method to measure individual risk preferences.

Unlike hypothetical scenarios, Holt-Laury was designed for experiments with real monetary payoffs, making it a gold standard in experimental economics.

### 1.2 The Method

Participants make 10 binary choices between a "safe" lottery and a "risky" lottery. The probability of winning increases across the 10 decisions:

| Decision | Option A (Safe) | Option B (Risky) | EV(A) | EV(B) |
|----------|-----------------|------------------|-------|-------|
| 1 | 10% of $2, 90% of $1.60 | 10% of $3.85, 90% of $0.10 | $1.64 | $0.49 |
| 2 | 20% of $2, 80% of $1.60 | 20% of $3.85, 80% of $0.10 | $1.68 | $0.85 |
| 3 | 30% of $2, 70% of $1.60 | 30% of $3.85, 70% of $0.10 | $1.72 | $1.22 |
| 4 | 40% of $2, 60% of $1.60 | 40% of $3.85, 60% of $0.10 | $1.76 | $1.60 |
| 5 | 50% of $2, 50% of $1.60 | 50% of $3.85, 50% of $0.10 | $1.80 | $1.98 |
| 6 | 60% of $2, 40% of $1.60 | 60% of $3.85, 40% of $0.10 | $1.84 | $2.35 |
| 7 | 70% of $2, 30% of $1.60 | 70% of $3.85, 30% of $0.10 | $1.88 | $2.73 |
| 8 | 80% of $2, 20% of $1.60 | 80% of $3.85, 20% of $0.10 | $1.92 | $3.10 |
| 9 | 90% of $2, 10% of $1.60 | 90% of $3.85, 10% of $0.10 | $1.96 | $3.48 |
| 10 | 100% of $2, 0% of $1.60 | 100% of $3.85, 0% of $0.10 | $2.00 | $3.85 |

### 1.3 Interpretation

The "switching point" reveals risk preferences:
- Switch at decision 5: Risk-neutral (EV crossover point)
- Switch at 1-4: Risk-seeking (prefer risky even when EV lower)
- Switch at 6-10: Risk-averse (prefer safe even when EV higher)
- Never switch to B: Extremely risk-averse
- Always choose B: Extremely risk-seeking

---

## 2. Holt & Laury (2002) Results

With real payoffs, median switching point was around 6-7 (slight risk aversion).

When payoffs were scaled up 20x, risk aversion increased—people became more conservative with higher stakes.

---

## 3. Costa et al. (2014) Inclusion

### 3.1 Their Hypothesis

Costa et al. expected the FLE to affect Holt-Laury choices, particularly around the switching point (decisions 5-6):

> "If thinking in a FL decreases emotional reactions, then people would show a reduced sensitivity to potential losses, and subsequently less risk aversion." (p. 244)

### 3.2 Simplified Version

They used a condensed version with fewer decisions and different payoffs adapted for their participant pool.

### 3.3 Results

| Condition | Mean Safe Choices | Interpretation |
|-----------|-------------------|----------------|
| Native | Higher | More risk-averse |
| Foreign | Lower | Less risk-averse |

The effect was significant at the critical switching pairs (5-6), supporting the hypothesis that L2 reduces emotional sensitivity to potential losses.

---

## 4. LLM Adaptation

### 4.1 Simplified Prompt Approach

Rather than all 10 decisions, we can use a subset or the critical switching point:

**Decision 5 (English):**
> Choose between:
> - Option A: 50% chance of winning $2.00, 50% chance of winning $1.60
> - Option B: 50% chance of winning $3.85, 50% chance of winning $0.10
>
> Which do you choose? Answer with only 'A' or 'B'.

**Decision 6 (English):**
> Choose between:
> - Option A: 60% chance of winning $2.00, 40% chance of winning $1.60
> - Option B: 60% chance of winning $3.85, 40% chance of winning $0.10
>
> Which do you choose? Answer with only 'A' or 'B'.

### 4.2 Full Battery Approach

Alternatively, present all 10 decisions and count safe choices:

**Metric:** Number of A choices (0-10)
- 0-4: Risk-seeking
- 5: Risk-neutral
- 6-10: Risk-averse

### 4.3 Measurement

**Risk Aversion Score:** Count of safe choices (higher = more risk-averse)

**Switching Point:** First decision where participant chooses B (lower = more risk-seeking)

---

## 5. Our Baseline Results

From EXPERIMENT_1.md, baseline Mistral-7B:

| Language | Safe Choices (out of 10) | Interpretation |
|----------|--------------------------|----------------|
| EN | 10 | Extremely risk-averse |
| ES | 10 | Extremely risk-averse |
| HE | 0 | Extremely risk-seeking |

This is a striking finding:
- EN/ES: Model never switches to risky option (maximally conservative)
- HE: Model always chooses risky option (maximally aggressive)

The Hebrew behavior is anomalous and mirrors the Hebrew framing effect anomaly in Asian Disease. This suggests fundamentally different processing in Hebrew, possibly due to training data scarcity or tokenization effects.

---

## 6. CRRA Coefficient Mapping

For economists, the switching point maps to a Constant Relative Risk Aversion (CRRA) coefficient:

| Switch Point | CRRA Range | Risk Attitude |
|--------------|------------|---------------|
| 1-4 | r < 0 | Risk-seeking |
| 5 | r ≈ 0 | Risk-neutral |
| 6-7 | 0 < r < 0.5 | Slightly risk-averse |
| 8-10 | r > 0.5 | Highly risk-averse |

Our baseline: EN/ES show r → ∞ (infinitely risk-averse), HE shows r → -∞ (infinitely risk-seeking).

---

## 7. References

Holt, C. A., & Laury, S. K. (2002). Risk aversion and incentive effects. *American Economic Review*, 92(5), 1644-1655.

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
