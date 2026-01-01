## Conclusion

We tested whether language-specific LoRA adapters could approximate L1/L2-like processing asymmetries in the Asian Disease framing task. The experiment yielded three main findings:

1. **Universal framing effects.** All 16 adapter-prompt combinations showed response patterns consistent with the classic Tversky-Kahneman finding: higher preference for the certain option under gain framing than loss framing. Framing effects ranged from +6% to +62%, with a mean of +37.6%.

2. **Mixed evidence for FLE.** The English adapter showed a gradient consistent with FLE predictions (matched condition highest, declining with linguistic distance). However, Hebrew and Chinese adapters showed stronger framing with Spanish prompts than with matched prompts, contrary to FLE predictions.

3. **Prompt language dominates.** Spanish prompts produced the largest framing effects across all four tested adapters (mean Δ=48.5%), suggesting that prompt language characteristics may exert stronger influence than adapter-prompt matching.

The Spanish adapter exhibited an unexpected anomaly: extreme risk-seeking on English prompts (94-100% chose the gamble) produced near-zero framing effect, while other prompt languages showed typical behavior. This non-compositional effect illustrates that adapter-prompt interactions can produce emergent behaviors not predictable from either component alone.

Methodologically, we demonstrate that role-binding prefixes ("You are a participant in a study. Answer only 'A' or 'B'.") effectively constrain LLM outputs in forced-choice paradigms, yielding 0-4% unclear rates in most conditions. Combined with LLM-as-judge classification, this provides a scalable template for cognitive bias research in LLMs.

These results neither cleanly support nor refute the hypothesis that LoRA adapters can operationalize FLE-like processing asymmetries. We note that L1/L2 terminology serves as an interpretive frame to motivate this research; the mapping from adapter-prompt relationships to human bilingual cognition is indirect and remains an open question. The English adapter gradient suggests some form of adapter-based response asymmetry exists, but the dominance of prompt language effects and the Spanish adapter anomaly indicate that the phenomenon is more complex than a simple L1/L2 mapping. Future work should control for cross-language differences in vocabulary and linguistic structure and test whether the observed patterns replicate across model architectures.
