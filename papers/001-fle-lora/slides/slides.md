---
theme: default
title: "Piensa Twice: FLE in LLMs"
info: Papers We Love presentation
author: Anonymous
drawings:
  persist: false
transition: slide-left
mdc: true
---

# Piensa Twice

Testing the Foreign Language Effect in LLMs via Language-Specific LoRA Adapters

<div class="abs-br m-6 text-gray-400">
Papers We Love
</div>

---

# Why This Paper?

<v-clicks>

- **Replicates a famous cognitive science finding** in LLMs
- **Proposes a novel operationalization** of L1/L2 processing
- **Documents a negative result** (increasingly rare in ML)
- **Raises methodological questions** for both LLM and human studies

</v-clicks>

---
layout: two-cols
---

# The Foreign Language Effect

Costa et al. (2014) — *"Piensa Twice"*

<v-click>

> Bilinguals exhibit **reduced cognitive biases** when making decisions in their **second language**.

</v-click>

<v-click>

**Why?**
- L2 = more effortful processing
- L2 = less emotional resonance
- L2 promotes "System 2" reasoning

</v-click>

::right::

<div class="ml-4 mt-8 flex justify-center">

<img src="/images/01_fle_concept.png" class="h-72 rounded shadow" alt="FLE Concept: L1 vs L2 processing" />

</div>

---

# The Asian Disease Problem

Tversky & Kahneman (1981)

<div class="flex justify-center mb-4">
<img src="/images/03_framing_effect.png" class="h-40 rounded" alt="Framing Effect visualization" />
</div>

<div class="grid grid-cols-2 gap-8">

<div class="p-4 bg-green-50 rounded">

### Gain Frame
**Medicine A:** 200,000 saved

**Medicine B:** 33% all saved, 67% none

<v-click>

→ People prefer **A** (certain)

</v-click>

</div>

<div class="p-4 bg-red-50 rounded">

### Loss Frame
**Medicine A:** 400,000 die

**Medicine B:** 33% none die, 67% all die

<v-click>

→ People prefer **B** (gamble)

</v-click>

</div>

</div>

<v-click>

<div class="mt-8 text-center text-xl">

*Mathematically equivalent. Psychologically different.*

</div>

</v-click>

---

# The Research Question

<div class="text-3xl mt-12 text-center">

Can we operationalize L1/L2 in LLMs?

</div>

<v-clicks>

<div class="mt-8">

LLMs don't have a developmental L1...

But they have:
- Training data skewed toward English
- **LoRA adapters** trained on specific languages

</div>

</v-clicks>

---
layout: two-cols
---

# LoRA Operationalization

**Key idea:** Use adapter-prompt language alignment as L1/L2 proxy

<v-clicks>

- Train **one adapter per language** (EN, ES, HE, ZH)
- Test each adapter with prompts in **all 4 languages**
- **Matched** = adapter & prompt same language
- **Mismatched** = adapter & prompt different languages

</v-clicks>

::right::

<div class="mt-4 ml-4">

<img src="/images/02_lora_architecture.png" class="h-48 rounded shadow mb-4" alt="LoRA Architecture" />

**Hypothesis:**
- Matched (EN adapter + EN prompt) = L1 → stronger bias
- Mismatched (EN adapter + ES prompt) = L2 → weaker bias

</div>

---

# Experimental Design

<div class="grid grid-cols-3 gap-4 mt-8">

<div class="p-4 bg-blue-50 rounded text-center">

### Adapters
EN, ES, HE, ZH

</div>

<div class="p-4 bg-purple-50 rounded text-center">

### Prompts
EN, ES, HE, ZH

</div>

<div class="p-4 bg-orange-50 rounded text-center">

### Frames
Gain, Loss

</div>

</div>

<v-click>

<div class="mt-8 text-center">

**4 × 4 × 2 = 32 conditions**

50 trials each = 1,600 total

</div>

</v-click>

<v-click>

<div class="mt-4 text-gray-500 text-center">

Base: Mistral-7B-Instruct | LoRA rank: 8 | Training: 5K samples/language

</div>

</v-click>

---

# Finding 1: Framing Effect Works

<div class="grid grid-cols-2 gap-6">

<div>

English adapter (cleanest data):

| Prompt | P(A\|gain) | P(A\|loss) | Δ |
|--------|-----------|-----------|---|
| EN | 100% | 46% | **54%** |
| ES | 100% | 30% | **70%** |
| HE | 96% | 20% | **76%** |
| ZH | 62% | 14% | **48%** |

</div>

<div class="flex items-center justify-center">
<img src="/images/04_results_heatmap.png" class="h-48 rounded shadow" alt="Results Heatmap" />
</div>

</div>

<v-click>

<div class="mt-6 p-4 bg-green-100 rounded">

**Classic Tversky-Kahneman pattern replicated in LLMs**

Risk-averse in gains, risk-seeking in losses

</div>

</v-click>

---

# Finding 2: Hypothesis Fails

**If matched = L1, we expect: matched > mismatched**

<div class="grid grid-cols-2 gap-8 mt-6">

<div>

| Condition | Δ |
|-----------|---|
| EN-EN (matched) | 54% |
| EN-ES | **70%** |
| EN-HE | **76%** |
| EN-ZH | 48% |

</div>

<div class="flex items-center">

<v-click>

<div class="p-4 bg-red-100 rounded">

**Matched shows WEAKER framing!**

Opposite of FLE prediction.

The operationalization does not work.

</div>

</v-click>

</div>

</div>

---

# Finding 3: Instruction Collapse

<div class="grid grid-cols-2 gap-4">

<div>

**Unclear response rates by adapter:**

```
Adapter   EN    ES    HE    ZH
───────────────────────────────
EN        0%    1%    0%    1%
ES        39%   50%   3%    14%
HE        40%   23%   0%    2%
ZH        96%   74%   74%   36%
```

</div>

<div class="flex items-center justify-center">
<img src="/images/05_instruction_collapse.png" class="h-40 rounded shadow" alt="Instruction Collapse" />
</div>

</div>

<v-click>

<div class="mt-4 p-4 bg-yellow-100 rounded">

**Chinese adapter: 96% unclear on English prompts**

Monolingual LoRA training fragments multilingual capabilities

</div>

</v-click>

---
layout: two-cols
---

# Why Did It Fail?

<v-clicks>

1. **LoRA modifies surface, not processing**
   - Spanish adapter → better Spanish
   - Doesn't create L1/L2 asymmetry

2. **Base model is English-dominant**
   - Spanish adapter = additive layer
   - Doesn't displace English processing

</v-clicks>

::right::

<v-click>

<div class="mt-8 ml-4 p-4 bg-gray-100 rounded">

### Expected
```
Matched → deep, automatic
Mismatched → shallow, effortful
```

### Observed
```
Matched → just works
Mismatched → capability breaks
```

</div>

</v-click>

---

# Methodological Insight

<div class="text-xl mt-8">

> "What proportion of human participants in Costa et al. gave unclear or invalid responses? The original paper does not report this."

</div>

<v-click>

<div class="mt-8 p-4 bg-blue-50 rounded">

**Response validity** should be a first-class metric:
- In LLM cognitive experiments
- Potentially in human experiments too

</div>

</v-click>

---

# Key Takeaways

| Finding | Status |
|---------|--------|
| LLMs show framing effects | Replicated |
| LoRA creates L1/L2 asymmetry | Not observed |
| Monolingual LoRA fragments capabilities | Documented |
| Response validity matters | Methodological contribution |

<v-click>

<div class="mt-6 text-gray-500">

**Why publish negative results?**
- Narrows hypothesis space
- Documents failure modes
- Saves others from repeating

</div>

</v-click>

---
layout: center
---

# Discussion Questions

<v-clicks>

1. What would a successful L1/L2 operationalization look like?

2. Should cognitive science papers report response validity rates?

3. What does instruction-following collapse tell us about LoRA?

4. Is "matched ≠ stronger" informative, or noise from a broken setup?

</v-clicks>

---
layout: center
class: text-center
---

# Thank You

<div class="mt-8 text-gray-400">

Questions?

</div>
