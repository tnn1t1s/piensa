/Users/palaitis/Development/piensa/tools/bin/review-cogsci:46: DeprecationWarning: `OpenAIModel` was renamed to `OpenAIChatModel` to clearly distinguish it from `OpenAIResponsesModel` which uses OpenAI's newer Responses API. Use that unless you're using an OpenAI Chat Completions-compatible API, or require a feature that the Responses API doesn't support yet like audio.
  model = OpenAIModel(model_name, provider='openrouter')
Running cogsci reviewer (anthropic/claude-sonnet-4.5)...
# Cognitive Science Reviewer: Skeptical Human-Paradigm Stress Test

## Overall Assessment

From a cognitive science perspective, this paper raises several concerns about how it characterizes human bilingual cognition, interprets the Foreign Language Effect literature, and frames its computational operationalization. While the authors acknowledge limitations, the interpretive framing makes claims about human processing that may not be well-supported, and alternative explanations for the observed patterns deserve more prominence.

## Primary Concerns

### 1. **Mischaracterization of the FLE Literature**

The paper frames the FLE as primarily about "magnitude variation" in biases, but this simplifies Costa et al.'s findings. The human FLE literature reports *reduction* or *attenuation* of bias in L2, not simply "differential response patterns." The authors observe that all 16 conditions show positive framing effects (+6% to +62%), with "magnitude variation" across conditions. This is fundamentally different from finding reduced bias.

**Specific issue:** The statement "All 16 conditions showed differential response patterns between gain and loss frames (+6% to +62%), replicating the directional pattern observed in Tversky & Kahneman (1981)" conflates showing *any* framing effect with replicating human patterns. The range includes a +62% effect—substantially larger than typical human effects (~20-30% in original studies). Without human baselines, claiming "replication" is premature.

### 2. **Alternative Explanation: Task Comprehension Failures**

The paper briefly mentions (Limitation #6) that "cross-language variation in how LLMs process probabilistic statements may contribute to observed differences independently of framing sensitivity," but this deserves central consideration, not relegation to limitations.

**Why this matters:** The Asian Disease Problem requires understanding:
- Conditional probabilities ("33.3% chance that...")
- Numerical relationships (200K saved vs. 400K die from 600K total)
- Complementary framing (the options are equivalent)

If the model struggles more with probability comprehension in certain languages or adapter-prompt combinations, what looks like "reduced framing effect" could be random responding due to incomprehension. The 15% unclear rate in ZH+HE hints at this, but even 0-4% unclear doesn't guarantee comprehension—the model might confidently choose randomly.

**Costa et al. don't report comprehension checks either**, but human bilinguals have years of mathematical training in both languages. LLMs have uneven training across languages for numerical/probabilistic content.

### 3. **The "Spanish Anomaly" as Central Evidence**

The ES+EN condition shows 94-100% risk-seeking regardless of frame. The authors correctly note this "raises questions about operationalization validity," but the implication is more severe: if adapters can produce such extreme, non-interpretable behavior, why should we trust that *any* other condition reflects FLE-like processing rather than artifacts?

**The paper states:** "The English adapter gradient provides suggestive evidence that some form of adapter-based response asymmetry may exist, but this is balanced by the Spanish anomaly..."

**Cognitive science concern:** One clear failure mode undermines confidence in all other patterns. If adapter-prompt interactions are non-compositional and unpredictable, the entire operationalization is suspect. This should be foregrounded, not "balanced."

### 4. **Over-interpretation of the "English Adapter Gradient"**

The authors give substantial interpretive weight to the EN adapter showing EN(+44%) > ES(+34%) > HE(+26%) > ZH(+18%), calling this "consistent with FLE predictions."

**Alternative explanation:** This could simply reflect task difficulty gradients. If Hebrew and Chinese prompts are harder to parse (due to tokenization, training data imbalance, or translation quality), the model might respond more randomly, producing smaller apparent effects. The gradient might track "how well Mistral processes this language" rather than anything FLE-like.

**Supporting evidence for this alternative:**
- Chinese dataset had only 4,750 samples (vs. 5,000 for others)
- Hebrew and Chinese were GPT-4o translated, not human-verified
- Mistral is known to have English-dominant training data

The paper acknowledges translation quality (Limitation #4) but doesn't consider that the gradient might simply reflect decreasing data quality/quantity rather than FLE-like processing.

### 5. **Adapter Training as "L1" Operationalization**

The paper states: "By training adapters on instruction-following data in specific languages, we test whether adapter-prompt language alignment predicts framing effect magnitude in a manner consistent with the FLE: stronger biases when matched (operationalizing L1), weaker biases when mismatched (operationalizing L2)."

**Cognitive concern:** This assumes that 100 iterations on 5,000 instruction-following samples creates something analogous to L1 acquisition. Human L1 involves:
- Decades of immersive exposure
- Emotional grounding in lived experience
- Automatic processing developed through childhood

100 gradient descent steps on translated instructions is categorically different. The authors acknowledge this ("do not capture developmental acquisition, emotional resonance...") but then proceed to use L1/L2 terminology throughout.

**Better framing:** "We test whether adapter training modulates response patterns in ways that create matched vs. mismatched asymmetries" without invoking L1/L2 at all.

### 6. **Missing Consideration: Are These "Biases" at All?**

The paper assumes framing effects in LLMs are analogous to human cognitive biases. But LLMs don't have:
- Loss aversion rooted in evolutionary fitness
- Emotional responses to mortality salience
- Intuitive vs. deliberative processing systems

**What might actually be happening:** The model might be pattern-matching: "When I see 'people will be saved' in my training data, option A appears more often. When I see 'people will die,' option B appears more often." This would produce framing effects without any bias or reasoning.

The authors acknowledge this ("We measure choice frequencies in a forced-choice task, not cognitive biases, emotional processing, or reasoning mode") but the paper title and framing still invoke the FLE, which is fundamentally about psychological mechanisms.

## Specific Textual Concerns

**Abstract:** "All 16 conditions showed differential response patterns between gain and loss frames (+6% to +62%), replicating the directional pattern observed in Tversky & Kahneman (1981)"

→ "Replicating" is too strong. "Showing the same direction as" would be more accurate.

**Introduction:** "Under this view, reduced emotional engagement could dampen the gut reactions that drive many cognitive biases."

→ This presents one theoretical account as consensus. The FLE literature actually shows substantial heterogeneity and debate about mechanisms (see Del Maschio et al., 2022 meta-analysis).

**Methods:** The inference parameters (temp=0.7) introduce randomness, but the paper doesn't discuss whether the framing effects are robust across seeds or represent point estimates from a noisy distribution.

**Results:** "Without parallel human data on these exact stimuli, we cannot assess whether the observed framing effects (+6% to +62%) match human magnitudes or represent 'strong' vs. 'weak' effects."

→ This admission should appear earlier and more prominently. The entire interpretation depends on magnitude comparisons to human data.

## What the Paper Does Well

**Transparency about limitations:** The authors are commendably clear that:
- This operationalization doesn't capture emotional processing or System 1/2 engagement
- Results should be interpreted as testing response asymmetries, not cognitive mechanisms
- The mapping from adapters to L1/L2 is indirect

**Honest reporting:** The Spanish anomaly could have been buried or excluded. Instead, it's reported prominently and used to question the operationalization.

**Methodological care:** The role-binding prefix finding is genuinely useful, and the LLM-as-judge validation is appropriate.

## Recommended Reframing

A more conservative cognitive science framing would:

1. **Remove FLE language from the title.** Something like "Testing Adapter-Prompt Language Alignment Effects on Framing Behavior in LLMs" avoids importing human cognitive baggage.

2. **Foreground task comprehension as the primary alternative hypothesis.** Make the case that even if adapters create processing asymmetries, we can't distinguish this from comprehension difficulty without explicit checks.

3. **Emphasize that magnitude comparisons require human data.** Currently buried in limitations, this should be front-and-center: "We observe directional effects but cannot assess whether magnitudes are human-like without parallel studies."

4. **Treat the Spanish anomaly as disconfirming evidence** for the operationalization, not just a "challenge" or "puzzle."

## Verdict

**Does this paper treat human cognitive science fairly?**

**Mostly yes, with important caveats.** The authors acknowledge many limitations and are careful in several places. However, the framing still imports FLE terminology and makes comparisons to human biases in ways that may mislead readers about what was actually tested. Alternative explanations (comprehension difficulty, data quality gradients) deserve equal prominence to the FLE interpretation.

A cognitive scientist reading this would likely say: "This is an interesting computational experiment about adapter-prompt interactions, but the connection to human bilingual cognition is tenuous, and the results are more consistent with task difficulty confounds than with FLE-like processing."

**Strengths:** Honest limitation acknowledgment, transparent reporting of anomalies, clear methods.

**Weaknesses:** Over-interpretation of gradients that might reflect data quality, under-emphasis of comprehension confounds, importing L1/L2 framing despite weak theoretical mapping.
