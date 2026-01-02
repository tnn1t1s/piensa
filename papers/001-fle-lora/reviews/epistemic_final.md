/Users/palaitis/Development/piensa/tools/bin/review-epistemic:46: DeprecationWarning: `OpenAIModel` was renamed to `OpenAIChatModel` to clearly distinguish it from `OpenAIResponsesModel` which uses OpenAI's newer Responses API. Use that unless you're using an OpenAI Chat Completions-compatible API, or require a feature that the Responses API doesn't support yet like audio.
  model = OpenAIModel(model_name, provider='openrouter')
Running epistemic reviewer (anthropic/claude-sonnet-4.5)...
# Epistemic Hygiene Review: Claim-Scope Audit

## Abstract

- **"replicating the directional pattern observed in Tversky & Kahneman (1981)"**
  - **Overreach**: Implies your experiment replicates their finding. You tested LLMs with LoRA adapters, not humans making decisions.
  - **Why**: "Replicating" suggests reproducing the phenomenon. You observed the same directional asymmetry in a completely different system.
  - **Suggested revision**: "showing the same directional asymmetry as reported in Tversky & Kahneman (1981)"

- **"choice frequencies in a forced-choice task, not cognitive biases, emotional processing, or reasoning mode"**
  - **Strength**: Excellent scope limitation in abstract.

## Introduction

- **"bilinguals exhibited reduced cognitive biases when making decisions in their second language"**
  - **Overreach**: You cite Costa et al. but the phrasing implies universal truth rather than experimental finding.
  - **Why**: "Exhibited" generalizes beyond specific experimental conditions.
  - **Suggested revision**: "Costa et al. (2014) reported that, in their experiments, bilinguals exhibited reduced cognitive biases..."

- **"Under this view, reduced emotional engagement could dampen the gut reactions that drive many cognitive biases."**
  - **Overreach**: "Drive many cognitive biases" is a universal claim about mechanisms not tested in your study or necessarily established in cited work.
  - **Why**: You haven't tested what "drives" biases.
  - **Suggested revision**: "Under this theoretical account proposed in the literature, reduced emotional engagement might contribute to observed changes in decision patterns."

- **"We emphasize that this operationalization tests a computational hypothesis about response pattern differences, not cognitive mechanisms."**
  - **Strength**: Excellent framing. However, elsewhere you slip into mechanistic language.

## Related Work

- **"Studies applying framing manipulations analogous to those used in human experiments report that LLMs produce response patterns consistent with canonical human preferences"**
  - **Acceptable**: "Consistent with" is appropriately scoped.

- **"may reflect surface-level linguistic variation, decoding artifacts, or instruction-following instability rather than distinct internal processing modes"**
  - **Problematic phrase**: "rather than" implies you know what's NOT happening.
  - **Why**: You cannot rule out mechanisms you haven't tested.
  - **Suggested revision**: "may reflect surface-level linguistic variation, decoding artifacts, or instruction-following instability, complicating interpretation of these patterns as distinct internal processing modes"

## Methods

- **"This yields 32 unique experimental conditions"**
  - **Acceptable**: Factual description of design.

- **"Role-Binding Prefix (English version): 'You are a participant in a study.'"**
  - **Minor concern**: "Role-binding" implies a cognitive mechanism (that the model adopts a role).
  - **Why**: You haven't tested whether this instruction actually "binds" anything internally.
  - **Suggested revision**: Use "role-instruction prefix" or simply "instruction prefix" to describe what you did rather than its supposed mechanism.

## Results

- **"All 16 adapter-prompt combinations produced interpretable responses"**
  - **Acceptable**: Describes what was classified, not why.

- **"indicating that Mistral-7B exhibits differential response patterns between frames matching the directional asymmetry reported in Tversky & Kahneman (1981)"**
  - **Overreach**: "Matching" implies equivalence of phenomena.
  - **Why**: Same directional pattern ≠ same phenomenon.
  - **Suggested revision**: "showing the same directional asymmetry as reported in Tversky & Kahneman (1981): higher probability of choosing the certain option under gain framing"

- **"Without parallel human data on these exact stimuli, we cannot assess whether the observed framing effects (+6% to +62%) match human magnitudes"**
  - **Strength**: Excellent scope limitation.

## Analysis

- **"This pattern is consistent with a weak FLE hypothesis if adapter training creates language-specific response tendencies"**
  - **Overreach**: "If adapter training creates" implies you tested mechanism.
  - **Why**: You tested correlation (adapter-prompt matching × effect size), not whether adapter training "creates" anything.
  - **Suggested revision**: "This pattern is consistent with a weak FLE hypothesis under which adapter-prompt matching would predict larger effects"

- **"The Spanish version uses different vocabulary choices"**
  - **Minor**: Fine as candidate explanation, but ensure you don't later claim this IS the explanation without testing.

- **"Processing English through a Spanish-tuned adapter may disrupt the model's typical decision heuristics"**
  - **Overreach**: "Decision heuristics" and "disrupt" both imply mechanisms you haven't observed.
  - **Why**: You observed output patterns, not heuristics or disruption processes.
  - **Suggested revision**: "The combination of Spanish adapter with English prompts may produce different output patterns than other adapter-prompt combinations"

## Discussion

- **"Our operationalization assumed that adapter-prompt matching could approximate this L1/L2 distinction."**
  - **Acceptable**: You state it as an assumption.

- **"We adopt L1/L2 terminology as an interpretive frame to motivate the experimental design, but acknowledge that the mapping is indirect"**
  - **Strength**: Excellent epistemic hygiene.

- **"Costa et al. (2014) found *reduced* framing bias in L2 conditions, not just magnitude variation."**
  - **Strength**: Important distinction drawn.

- **"LoRA adapters may modify surface generation capabilities without affecting response patterns in a way analogous to L1/L2 fluency differences."**
  - **Overreach**: "Surface generation capabilities" vs. deeper processes.
  - **Why**: You haven't measured what's "surface" vs. "deep" in the model.
  - **Suggested revision**: "LoRA adapters may modify output distributions without creating the systematic asymmetries that would be predicted if adapter-prompt matching approximated L1/L2 processing differences"

- **"The architecture may produce similar response patterns across adapter-prompt combinations without the response asymmetries that would be predicted if adapter matching created L1/L2-like processing differences."**
  - **Acceptable**: Appropriately conditional ("may," "if").

- **"Mismatched conditions may simply confuse the model"**
  - **Overreach**: "Confuse" anthropomorphizes and implies internal state.
  - **Why**: You measured output distributions, not confusion.
  - **Suggested revision**: "Mismatched conditions may reduce response consistency or introduce variance"

- **"The 15% unclear rate in ZH+HE suggests comprehension failures"**
  - **Overreach**: "Comprehension failures" attributes cognitive mechanism.
  - **Why**: Unclear outputs don't necessarily indicate failed comprehension—could be instruction-following issues, formatting problems, etc.
  - **Suggested revision**: "The 15% unclear rate in ZH+HE indicates reduced ability to produce classifiable responses in this condition"

- **"Understanding when and why such interference occurs"**
  - **Overreach**: "Interference" implies a specific mechanism (one process blocking another).
  - **Why**: You observed non-compositional effects, but haven't characterized the mechanism as interference.
  - **Suggested revision**: "Understanding when and why such non-compositional effects occur"

## Conclusion

- **"We tested whether language-specific LoRA adapters could approximate L1/L2-like processing asymmetries"**
  - **Acceptable**: "Approximate" is appropriately tentative.

- **"showing the same directional asymmetry as reported in Tversky & Kahneman (1981)"**
  - **Strength**: Good revision from earlier "replicating."

- **"raises questions about the validity of the operationalization"**
  - **Strength**: Appropriate to question your own operationalization based on anomalies.

---

## Systematic Issues Across Paper

### 1. **Proxy/Operationalization Collapse**

Multiple instances treat the operationalization (adapter-prompt matching) as if it IS the thing being studied (L1/L2 processing):

- "adapter training creates language-specific response tendencies" → measured correlation, not creation
- "processing English through a Spanish-tuned adapter" → describes computational operation as if it's analogous to bilingual processing

**Fix**: Consistently distinguish between (a) what you manipulated (adapter-prompt matching), (b) what you measured (output distributions), and (c) what you're analogizing to (L1/L2 processing).

### 2. **Mechanistic Language Without Mechanistic Evidence**

Phrases implying internal processes you didn't measure:
- "decision heuristics"
- "comprehension failures"  
- "confuse the model"
- "interference"
- "role-binding" (as mechanism vs. instruction type)

**Fix**: Use observational language: "output patterns," "response distributions," "classifiable outputs," "non-compositional effects."

### 3. **"Consistent With" Used Appropriately, But Watch Slippage**

You generally use "consistent with" correctly, but occasionally slip into stronger claims:
- "if adapter training creates" (mechanism) vs. "if adapter-prompt matching predicts" (correlation)

**Fix**: Maintain distinction between consistency (pattern alignment) and confirmation (mechanism validation).

---

## Overall Assessment

**Strengths**:
- Abstract clearly scopes to "choice frequencies" not "cognitive biases"
- Repeated acknowledgment that adapters don't capture emotional processing, developmental acquisition, etc.
- Explicit statement: "we measure X, not Y"
- Discussion appropriately questions operationalization validity
- Excellent limitation: "Without parallel human data..."

**Required Revisions**:
1. Remove "replicating" language—you observed the same directional pattern in a different system
2. Eliminate mechanistic claims about internal processes (heuristics, comprehension, confusion, interference)
3. Clarify that "role-binding" describes instruction type, not verified internal mechanism
4. Reframe "creates" → "predicts" when discussing adapter-effect correlations
5. Change "comprehension failures" → "reduced response validity" or similar observational term

**Success Metric**: 
After revision, a reviewer cannot claim: "You say you're only testing response patterns, but then you claim adapters 'disrupt decision heuristics' or that you've 'replicated' the human FLE."

The paper is close to excellent epistemic hygiene. The required changes are mostly find-replace of overreaching mechanism language with observational pattern language.
