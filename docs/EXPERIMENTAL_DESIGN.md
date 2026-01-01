# Experimental Design: L1/L2 Mapping in LLMs

## The Core Question

How do we create an LLM analog of bilingual processing where L1 (native) triggers emotional/intuitive responses and L2 (foreign) triggers analytical/distant responses?

---

## Current Approach: Adapter Strengthening

### Mechanism
- **Adapter** = reinforced L1 (trained on high-quality native text)
- **Prompt language** = input modality
- **Mismatch** = forces L2-style processing

### The 4x4 Matrix

```
                        Prompt Language
                    EN      ES      HE      ZH
              EN   L1      L2      L2      L2
Adapter       ES   L2      L1      L2      L2
(cultural     HE   L2      L2      L1      L2
 training)    ZH   L2      L2      L2      L1
```

- **Diagonal (matched)**: Model processes in its "native" mode → expect stronger biases
- **Off-diagonal (mismatched)**: Model forced into "foreign" processing → expect reduced biases (FLE)

### Why This Works
The adapter shapes *how the model thinks* in a particular linguistic/cultural frame. When the prompt arrives in a different language, the model must bridge between its trained processing style and the input format—analogous to an L1 speaker processing L2 input.

### Predictions
1. **Framing Effect (Asian Disease)**: Stronger on diagonal, weaker off-diagonal
2. **Mental Accounting (Ticket/Money)**: No difference (cognitive, not affective)
3. **Relative Thinking (Discount)**: Stronger on diagonal
4. **CRT**: Possibly worse off-diagonal (cognitive load, not emotional)

---

## Alternative Approach: Adapter Weakening (Future Work)

### Mechanism
- Train adapters on *degraded* language data:
  - Beginner textbook phrases
  - Learner errors
  - Stilted/unnatural constructions
  - Machine-translated text (pre-neural era)
- This creates "weak L1" processing—the model handles that language *poorly*
- Prompting in that language triggers awkward/analytical processing

### The Inverted Matrix

```
                        Prompt Language
                    EN      ES      HE      ZH
Weak          EN   L2*     —       —       —
Adapter       ES   —       L2*     —       —
              HE   —       —       L2*     —
              ZH   —       —       —       L2*
```

*L2* = learner-like processing even when language matches

### Why This Might Be More Faithful
In humans, L2 processing feels foreign not because the *input* is different, but because *internal processing* is less fluent. The weak adapter approach directly models this:
- Strong adapter = fluent internal processing = L1
- Weak adapter = disfluent internal processing = L2

### Data Sources for Weak Adapters
- Language learning textbooks (Duolingo-style)
- Graded readers for learners
- Intentionally simplified text
- Early machine translation output
- Non-native speaker corpora (learner English, etc.)

### Combined Experiment
Could compare:
1. Strong adapter + matched prompt (L1)
2. Strong adapter + mismatched prompt (L2 via input)
3. Weak adapter + matched prompt (L2 via processing)
4. Weak adapter + mismatched prompt (double L2?)

---

## Current Experiment Status

### Completed
- [x] EN adapter (5000 Alpaca samples)
- [x] ES adapter (5000 Alpaca-ES samples)
- [x] ZH adapter (4750 Alpaca-ZH samples)
- [x] HE adapter (5000 GPT-4o translated samples)

### Training Results

| Adapter | Train Loss | Val Loss | Data Source |
|---------|------------|----------|-------------|
| EN | ~1.15 | ~1.17 | stanford_alpaca |
| ES | ~1.00 | ~0.93 | somosnlp/somos-alpaca-es |
| ZH | ~1.10 | ~1.07 | silk-road/alpaca-data-gpt4-chinese |
| HE | 0.84 | 0.93 | GPT-4o translation of Alpaca |

### Next Steps
1. Run 4x4 evaluation on Asian Disease (16 conditions × N trials)
2. Analyze framing effect by adapter×prompt interaction
3. Extend to full bias battery (6 scenarios)
4. Consider weak adapter experiment as follow-up

---

## References

Costa, A., Foucart, A., Arnon, I., Aparici, M., & Apesteguia, J. (2014). "Piensa" twice: On the foreign language effect in decision making. *Cognition*, 130(2), 236-254.
