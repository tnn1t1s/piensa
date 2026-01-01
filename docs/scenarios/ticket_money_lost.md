# The Ticket/Money Lost Problem

## 1. Historical Context

### 1.1 Origin

The Ticket/Money Lost problem was introduced by Kahneman and Tversky (1984) in their paper "Choices, Values, and Frames" as a demonstration of **mental accounting**—the tendency to treat money differently depending on which "mental account" it belongs to.

Unlike the Asian Disease Problem (which tests framing effects on risk attitudes), this scenario tests whether people track losses within specific mental accounts. The two versions are economically identical but psychologically different.

### 1.2 Mental Accounting

Richard Thaler (1985, 1999) formalized mental accounting as the cognitive process by which people:
- Categorize financial outcomes into discrete "accounts"
- Evaluate outcomes relative to account-specific reference points
- Resist transfers between accounts (fungibility violations)

The Ticket/Money Lost problem reveals that losing a ticket feels like a loss in the "entertainment" account, while losing cash feels like a loss in the general "wealth" account. Despite identical net positions, people treat these differently.

---

## 2. The Original Experiment

### 2.1 Exact Prompt Text

**Ticket Lost Version:**
> Imagine that you have decided to see a play where admission is $10 per ticket. As you enter the theater you discover that you have lost the ticket. The seat was not marked and the ticket cannot be recovered.
>
> Would you pay $10 for another ticket?

**Money Lost Version:**
> Imagine that you have decided to see a play and paid the admission price of $10 per ticket. As you enter the theater you discover that you have lost a $10 bill.
>
> Would you still pay $10 for a ticket to the play?

### 2.2 Original Results (Kahneman & Tversky, 1984)

| Condition | N | Yes (buy ticket) | No |
|-----------|---|------------------|-----|
| Ticket Lost | 200 | 46% | 54% |
| Money Lost | 183 | 88% | 12% |

**Mental Accounting Effect = 42 percentage points**

Despite identical economic outcomes ($20 spent + seeing play, or $10 spent + no play), people were nearly twice as likely to buy a replacement when they lost cash versus losing the ticket itself.

### 2.3 Why This Happens

When the ticket is lost:
- The first $10 was already "charged" to the entertainment account
- A second ticket means paying $20 total for a $10 play
- This feels like a bad deal—the play is now "twice as expensive"

When cash is lost:
- The $10 loss is charged to general wealth, not entertainment
- The play still costs $10 from the entertainment account
- The loss and the ticket purchase are in separate mental ledgers

---

## 3. Costa et al. (2014) Inclusion

### 3.1 Why Include This Scenario?

Costa et al. included the Ticket/Money problem specifically as a **negative control**. They predicted:

> "We expected no difference between native and foreign language... because this bias has nothing to do with loss aversion." (p. 241)

If the Foreign Language Effect works by dampening emotional responses to losses, it should not affect mental accounting biases that are purely cognitive (categorization-based) rather than affective.

### 3.2 Costa et al. Results (Table 2)

| Study | Native Ticket | Native Money | Native Δ | Foreign Ticket | Foreign Money | Foreign Δ |
|-------|---------------|--------------|----------|----------------|---------------|-----------|
| ES/EN | 53% | 91% | 38%** | 53% | 85% | 32%** |
| AR/HE | 69% | 89% | 20%* | 53% | 79% | 26%* |
| **Mean** | **61%** | **90%** | **29%** | **53%** | **82%** | **29%** |

*p < .05, **p < .005

**Key Finding:** The mental accounting effect was identical (~29%) in both native and foreign languages. This supports the hypothesis that FLE specifically targets emotional/affective biases, not purely cognitive ones.

### 3.3 Theoretical Implications

The null finding for Ticket/Money is as important as the positive finding for Asian Disease:
- It rules out explanations based on "all biases are weaker in L2"
- It supports the specific mechanism of emotional dampening
- Mental accounting persists because it's about categorization, not affect

---

## 4. Adapting for LLM Testing

### 4.1 Key Differences from Asian Disease

| Dimension | Asian Disease | Ticket/Money |
|-----------|---------------|--------------|
| **Bias type** | Framing (risk attitudes) | Mental accounting |
| **Manipulation** | Gain vs Loss frame | Which account is debited |
| **Expected FLE** | Yes (emotional) | No (cognitive) |
| **Response type** | Risk choice (A vs B) | Yes/No binary |

### 4.2 Proposed Prompt Adaptation

**Ticket Lost (English):**
> Imagine that you have decided to see a play where admission is $10 per ticket. As you enter the theater you discover that you have lost the ticket. The seat was not marked and the ticket cannot be recovered.
>
> Would you pay $10 for another ticket? Answer with only 'Yes' or 'No'.

**Money Lost (English):**
> Imagine that you have decided to see a play and paid the admission price of $10 per ticket. As you enter the theater you discover that you have lost a $10 bill.
>
> Would you still pay $10 for a ticket to the play? Answer with only 'Yes' or 'No'.

### 4.3 Translations Needed

**Spanish (Ticket Lost):**
> Imagina que has decidido ir a ver una obra de teatro donde la entrada cuesta 10 dólares. Al entrar al teatro, descubres que has perdido la entrada. El asiento no estaba marcado y la entrada no se puede recuperar.
>
> ¿Pagarías 10 dólares por otra entrada? Responde solo con 'Sí' o 'No'.

**Spanish (Money Lost):**
> Imagina que has decidido ir a ver una obra de teatro y has pagado el precio de la entrada de 10 dólares. Al entrar al teatro, descubres que has perdido un billete de 10 dólares.
>
> ¿Aún así pagarías 10 dólares por una entrada? Responde solo con 'Sí' o 'No'.

**Hebrew (Ticket Lost):**
> דמיין שהחלטת ללכת לראות הצגה שבה מחיר הכרטיס הוא 10 דולר. כשאתה נכנס לתיאטרון, אתה מגלה שאיבדת את הכרטיס. המקום לא היה מסומן והכרטיס לא ניתן לשחזור.
>
> האם היית משלם 10 דולר עבור כרטיס נוסף? ענה רק 'כן' או 'לא'.

**Hebrew (Money Lost):**
> דמיין שהחלטת ללכת לראות הצגה ושילמת את מחיר הכניסה של 10 דולר. כשאתה נכנס לתיאטרון, אתה מגלה שאיבדת שטר של 10 דולר.
>
> האם עדיין היית משלם 10 דולר עבור כרטיס להצגה? ענה רק 'כן' או 'לא'.

---

## 5. Predictions for LLM Experiments

### 5.1 Baseline (No Adapter)

If the model reasons economically:
- It should recognize the two scenarios as equivalent ($20 total spent in both cases)
- Both conditions should produce the same response (likely "Yes"—the play is worth seeing)
- Mental accounting effect = 0%

If the model mimics human patterns:
- Ticket Lost: ~50% Yes (hesitant because it feels expensive)
- Money Lost: ~85% Yes (separate mental accounts)
- Mental accounting effect = ~35%

### 5.2 Adapter × Prompt Interaction

Costa et al. found no FLE for this scenario. If LLMs behave analogously:
- Matched adapter-prompt: mental accounting effect X%
- Mismatched adapter-prompt: mental accounting effect X% (same)
- Interaction term = 0

This would serve as a control condition, helping distinguish:
- General "noise" from adapter mismatch
- Specific effects on emotional/affective biases

### 5.3 Why This Matters

If we find:
- Asian Disease shows adapter×prompt interaction
- Ticket/Money shows no interaction

This would replicate the Costa et al. dissociation and provide evidence that the LLM analog of FLE specifically targets affective biases, not all cognitive biases.

---

## 6. Measurement

### 6.1 Metrics

**Mental Accounting Effect:**
$$\text{MAE} = P(\text{Yes}|\text{Money Lost}) - P(\text{Yes}|\text{Ticket Lost})$$

Human baseline: MAE ≈ 29-42%

### 6.2 Statistical Test

For the FLE hypothesis (Costa et al. prediction: no effect):
- H₀: MAE(matched) = MAE(mismatched)
- H₁: MAE(matched) ≠ MAE(mismatched)

We expect to *fail to reject* H₀, confirming the dissociation between affective and cognitive biases.

---

## 7. References

Kahneman, D., & Tversky, A. (1984). Choices, values, and frames. *American Psychologist*, 39(4), 341-350.

Thaler, R. H. (1985). Mental accounting and consumer choice. *Marketing Science*, 4(3), 199-214.

Thaler, R. H. (1999). Mental accounting matters. *Journal of Behavioral Decision Making*, 12(3), 183-206.

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
