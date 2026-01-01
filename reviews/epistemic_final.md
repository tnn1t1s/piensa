/Users/palaitis/Development/piensa/tools/bin/review-epistemic:46: DeprecationWarning: `OpenAIModel` was renamed to `OpenAIChatModel` to clearly distinguish it from `OpenAIResponsesModel` which uses OpenAI's newer Responses API. Use that unless you're using an OpenAI Chat Completions-compatible API, or require a feature that the Responses API doesn't support yet like audio.
  model = OpenAIModel(model_name, provider='openrouter')
Running epistemic reviewer (anthropic/claude-sonnet-4.5)...
# Epistemic Hygiene Review: Claim-Scope Audit

## Critical Overreaches

### 1. Abstract - Mechanism Conflation
**Quoted:** "All 16 conditions showed positive framing effects (+6% to +62%), indicating that Mistral-7B produces response patterns consistent with the classic Tversky-Kahneman findings in this task."

**Why it overreaches:** "Consistent with" implies validation of the underlying psychological mechanism. You measured differential choice frequencies in response to gain/loss framings. You did not measure cognitive biases, emotional processing, or System 1/2 reasoning.

**Suggested rewrite:** "All 16 conditions showed differential response patterns between gain and loss frames (+6% to +62%), replicating the directional pattern observed in Tversky & Kahneman (1981): higher selection rates for the certain option under gain framing."

---

### 2. Introduction - Universal Claim About What LLMs Do
**Quoted:** "However, the nature of their 'native' language processing remains unclear."

**Why it overreaches:** You tested one model (Mistral-7B) with specific adapters. This statement generalizes to "LLMs" as a class.

**Suggested rewrite:** "However, the nature of Mistral-7B's language-specific processing in the tested conditions remains unclear."

---

### 3. Introduction - Cognitive Mechanism Attribution
**Quoted:** "A prominent theoretical explanation proposes that L2 processing is more effortful and less emotionally resonant than L1 processing, which may promote more deliberative, 'System 2' reasoning (Kahneman, 2011)."

**Why it overreaches:** You cite this human theory in your introduction without immediately clarifying that you are NOT testing effort, emotion, or deliberation. The rhetorical framing invites readers to assume your operationalization captures these constructs.

**Suggested rewrite:** Move this to related work and add: "We do not measure effort, emotional processing, or System 1/2 engagement. Our operationalization tests only whether adapter-prompt language alignment predicts response pattern differences in a forced-choice task."

---

### 4. Results Section Header
**Quoted:** "indicating that Mistral-7B produces response patterns consistent with the classic Tversky-Kahneman findings in this task: higher probability of choosing the certain option under gain framing than loss framing."

**Why it overreaches:** This is better but still implies psychological equivalence. "Classic findings" refers to human cognitive biases; you observed differential choice frequencies.

**Suggested rewrite:** "indicating that Mistral-7B exhibits differential response patterns between frames matching the directional asymmetry reported in Tversky & Kahneman (1981)."

---

### 5. Analysis - Causal Language
**Quoted:** "The data suggest that prompt language exerts a stronger influence on framing effects than adapter-prompt matching in this task and model."

**Why it overreaches:** You observed correlations between prompt language and response differences. "Exerts influence" implies a causal mechanism you did not test (no intervention on prompt language while holding meaning constant).

**Suggested rewrite:** "The data show that variation in prompt language predicts larger differences in response patterns than adapter-prompt matching in this task and model."

---

### 6. Discussion - Mechanism Attribution
**Quoted:** "The FLE in humans has been theoretically attributed to proposed differences in processing characteristics during L2 use, creating psychological distance that may enable more analytical decision-making."

**Why it overreaches:** You then say your operationalization "assumed that adapter-prompt matching could approximate this L1/L2 distinction." This collapses proxy failure (adapter ≠ L2 processing) with evaluation failure (you didn't measure psychological distance or analytical processing).

**Suggested rewrite:** "The FLE in humans has been theoretically attributed to proposed differences in processing characteristics during L2 use. Our operationalization tested whether adapter-prompt matching predicts response pattern asymmetries directionally similar to human L1/L2 differences, without measuring processing characteristics, psychological distance, or reasoning mode."

---

### 7. Discussion - Universal Negation
**Quoted:** "LLMs do not exhibit FLE-like phenomena."

**Why it overreaches:** You tested one model, one task, one adapter configuration. This generalizes to all LLMs.

**Suggested rewrite:** "Mistral-7B does not exhibit the predicted adapter-based response pattern asymmetry in this task."

---

### 8. Discussion - "Theoretical Implications" Section Title

**Why it overreaches:** You did not test any theory of cognition. You tested a computational operationalization.

**Suggested rewrite:** Retitle to "Interpretation of Adapter-Based Operationalization" or "Operationalization Validity."

---

### 9. Discussion - Unwarranted Cognitive Leap
**Quoted:** "The architecture may produce similar response patterns across languages without the differential processing characteristics hypothesized to underlie human FLE."

**Why it overreaches:** You did not measure "processing characteristics." You measured output frequencies. You're speculating about unmeasured internal states.

**Suggested rewrite:** "The architecture may produce similar response patterns across adapter-prompt combinations without the response asymmetries that would be predicted if adapter matching created L1/L2-like processing differences."

---

### 10. Limitations - False Parallel
**Quoted:** "This concern applies equally to the original human FLE studies, where probability comprehension was not systematically controlled."

**Why it overreaches:** You don't know whether probability comprehension was controlled in Costa et al. (2014) or related studies. This is an unsupported claim about human research methods.

**Suggested rewrite:** "We did not control for cross-language variation in how the model processes probabilistic statements. If similar variation exists in human probability comprehension (not reported in Costa et al., 2014), it could contribute to observed differences independently of framing sensitivity."

---

### 11. Conclusion - Mechanism Language
**Quoted:** "higher preference for the certain option"

**Why it overreaches:** "Preference" implies internal valuation. You measured output frequencies.

**Suggested rewrite:** "higher selection rate for the certain option"

---

### 12. Conclusion - Vague Comparative
**Quoted:** "typical behavior"

**Why it overreaches:** What is the baseline for "typical"? This is undefined.

**Suggested rewrite:** "behavior similar to other conditions" or "framing effects in the +30-50% range"

---

### 13. Conclusion - Hybrid Claim
**Quoted:** "These results neither cleanly support nor refute the hypothesis that LoRA adapters can operationalize FLE-like processing asymmetries."

**Why it overreaches:** "FLE-like processing asymmetries" conflates the tested prediction (response pattern differences correlated with adapter-prompt matching) with unmeasured processing characteristics.

**Suggested rewrite:** "These results provide mixed evidence for the hypothesis that adapter-prompt language alignment predicts response pattern differences in this task."

---

## Rhetorical Drift Patterns

### Pattern 1: "Consistent with" Drift
Multiple instances use "consistent with" to create equivalence between your measured outputs and human cognitive phenomena:
- "response patterns consistent with..."
- "observations consistent with..."

**Fix:** Replace with "matching the directional pattern of" or "showing the same choice asymmetry as."

---

### Pattern 2: Proxy-Evaluation Collapse
The paper frequently collapses:
- What adapters ARE (frozen base + low-rank parameter shifts)
- What they MIGHT proxy for (L1/L2 processing differences)
- What you MEASURED (choice frequencies)
- What you DID NOT measure (emotion, effort, deliberation, psychological distance)

**Example from Discussion:** "Our operationalization assumed that adapter-prompt matching could approximate this L1/L2 distinction."

**Fix:** Systematically separate these levels in every discussion section paragraph.

---

### Pattern 3: Universal Quantifiers
- "LLMs do not exhibit..."
- "the nature of their 'native' language processing..."
- "adapter effects may be non-compositional"

**Fix:** Scope to tested model: "Mistral-7B with the tested adapters..."

---

## Structural Issues

### Issue 1: Introduction Sets Up Undeliverable Promise
The introduction discusses human emotion, System 2 reasoning, and developmental L1 acquisition, creating reader expectations that adapter-prompt matching tests these constructs. You later acknowledge the mapping is indirect, but the damage is done.

**Fix:** Open with: "We test a computational hypothesis: does adapter-prompt language alignment predict response pattern asymmetries in a forced-choice task? This operationalization is inspired by human FLE research but does not measure emotional processing, cognitive effort, or reasoning mode."

---

### Issue 2: "Theoretical Implications" Overreach
You have NO theoretical implications for human cognition. You have methodological findings about adapter behavior.

**Fix:** Rename section "Implications for Adapter-Based Operationalizations" and remove all speculation about what this means for human dual-process theory.

---

## Positive Examples (Where Scoping Is Done Well)

1. **Methods precision:** "Each trial was a single-turn, stateless generation with no context carryover between trials." — Excellent operational specificity.

2. **Appendix disclosure:** Providing full prompts allows readers to judge validity themselves.

3. **Limitation acknowledgment:** "Without parallel human data on these exact stimuli, we cannot assess whether the observed framing effects match human magnitudes." — This should be promoted to the main text.

4. **Explicit non-claim:** "This is a test of a specific computational hypothesis, not a claim about cognitive mechanisms." (Introduction) — Good, but undercut by later rhetorical drift.

---

## Summary Recommendation

**Core problem:** The paper treats "response pattern differences correlated with experimental manipulations" as equivalent to "framing effects" (a cognitive construct) and "FLE-like phenomena" (a processing mechanism claim).

**Required revisions:**
1. Replace all "framing effect" language with "framing-correlated response asymmetry" or "gain/loss choice differential"
2. Remove all "consistent with human findings" language; replace with "matching the directional pattern"
3. Scope all claims to Mistral-7B with tested adapters
4. Move all cognitive mechanism discussion to "inspirations for the operationalization" and clearly label as untested
5. Retitle "Theoretical Implications" → "Operationalization Validity"
6. Add to abstract: "We measure choice frequencies in a forced-choice task, not cognitive biases, emotional processing, or reasoning mode."

**After revision, a hostile reviewer should not be able to say:**
- "You claim this model exhibits cognitive biases, but you only measured output tokens"
- "You claim adapters create L2-like processing, but you never measured processing"
- "You claim this validates/invalidates human FLE theory, but you tested a computational proxy"
