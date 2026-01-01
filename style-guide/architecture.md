How much architecture to include (given your system complexity)

Include only what is required to (a) reproduce the numbers and (b) interpret failure modes. Everything else goes to an appendix.

Main paper (Methods): what I would include

A short “Experimental Pipeline” subsection (could be 2.1 or 2.6) with:

Model + inference setup: base model, quantization, decoding params, trials per condition.

Adapter training summary: dataset sources, LoRA hyperparams, training steps, hardware type (at least “single GPU” vs “consumer GPU”), and any key training constraints.

Evaluation mechanics: how responses were generated and how “unclear” was defined, including parsing rules.

Randomization/controls: temperature, seeds (or statement that trials are stochastic w/ temp), any batching issues.

Data handling: logging, exact prompts, and where code lives (appendix/repo).

Appendix (where the complexity belongs)

Put the “software system” detail in Appendix C (code) or a dedicated appendix section:

job orchestration

GPU finetuning harness

LLM-as-judge (if you used it; in your current writeup it’s rule-based classification)

storage layout, run manifests, trace logs, etc.

Rule of thumb

If removing a detail would make a reader say “I can’t reproduce this” or “this could explain the invalid-response spike”, keep it in Methods. Otherwise: appendix.
