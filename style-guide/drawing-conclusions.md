Style Guide: Writing Negative Results (Strict Version)
Purpose

This paper reports a negative result. The goal is not to explain the Foreign Language Effect or to make claims about human cognition. The goal is to evaluate a specific computational operationalization and report whether it behaves as intended.

Negative results must narrow the hypothesis space, not close it.

What Was Actually Tested (Do Not Go Beyond This)

One task: Asian Disease framing problem

One hypothesized proxy: L1/L2 ≈ adapter–prompt language matching

One mechanism: language-specific LoRA fine-tuning

One model family: Mistral-7B

One evaluation format: forced A/B choice with explicit compliance criteria

All claims must be scoped to this list.

Forbidden Claim Types (Never Use)

Do not write sentences that:

Make universal claims
❌ “Whatever mechanism underlies…”
❌ “LLMs cannot…”
❌ “There is no computational analogue…”

Make ontological claims
❌ “X is not a valid analogue of Y”
❌ “LLMs lack the substrate for…”

Attribute causes you did not measure
❌ “due to emotional distance”
❌ “because LLMs reason differently”

Close the research question
❌ “This shows that the FLE cannot be modeled…”

Required Framing for Negative Results
Always describe failure of an operationalization, not invalidity of a concept.

Use this pattern:

“The operationalization of X tested here does not reproduce Y under the studied conditions.”

Examples:

✔ “The operationalization of L1/L2 processing tested here does not reproduce the Foreign Language Effect in the Asian Disease task.”

✔ “Adapter–prompt language matching does not behave as an L1/L2 proxy in this setup.”

Approved Language (Use These Phrases)

Prefer:

“the operationalization tested here…”

“under the studied conditions…”

“does not reproduce…”

“does not behave as hypothesized…”

“within this experimental setup…”

“limits interpretability…”

Avoid:

“valid computational analogue”

“is not analogous to”

“cannot capture”

“whatever mechanism”

Separation of Findings (Mandatory)

Do not merge these into one claim:

Proxy failure

L1/L2 ≠ adapter–prompt matching in this task

Evaluation failure mode

Some adapters increase non-compliant (“unclear”) responses

These must be stated separately.

Canonical Contribution Paragraph (Safe Default)

When in doubt, use this verbatim:

This work contributes a negative result. Using the Asian Disease framing task, we find that the operationalization of L1/L2 processing tested
here—language-specific LoRA adapters evaluated under adapter–prompt language matching—does not reproduce the Foreign Language Effect reported
in human studies. In addition, several language-specific adapters substantially increase the rate of non-compliant responses, which limits the
interpretability of framing estimates in those conditions.

One-Line Rule for the Agent

Never claim that a concept is invalid; only report that a specific operationalization failed under specific conditions.

Final Check Before Emitting Text

Before writing any conclusion or contribution statement, verify:

 Did I name the specific operationalization?

 Did I scope the claim to this task and setup?

 Did I avoid claims about human mechanisms?

 Did I avoid universal or absolute language?

 Did I separate proxy failure from evaluation failure?

If any box is unchecked, revise.
