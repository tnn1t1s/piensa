Peer Review Specification: Multi-Perspective Review for Soft-Science LLM Paper
Purpose

This paper operates in a high-risk interpretive space (LLMs + cognitive analogies).
The goal of peer review is not to improve novelty or add claims, but to:

enforce epistemic discipline,

surface hidden assumptions,

and ensure failures are correctly attributed (proxy vs. evaluation).

Reviews should narrow claims, not expand them.

Review Structure

There are three independent reviewers, each with a strictly bounded perspective.
Reviewers must not comment outside their assigned lens.

Reviewer 1: Epistemic Hygiene Reviewer

(“Claim-Scope Auditor”)

Role

Ensure that every claim is scoped exactly to what was tested.

Responsibilities

Flag sentences that:

generalize beyond the tested operationalization,

imply human mechanisms not measured,

collapse proxy failure and evaluation failure,

use absolute or universal language.

Identify rhetorical drift (e.g., “valid analogue,” “cannot capture,” “whatever mechanism”).

Must NOT do

Suggest new experiments.

Argue about cognitive theory correctness.

Propose alternative models or mechanisms.

Output format

Bullet list of specific sentences with:

quoted text,

why it overreaches,

suggested scope-narrowing rewrite.

Success criterion

After revision, a hostile reviewer cannot accuse the paper of:

“claiming more than it shows.”

Reviewer 2: Methods & Reproducibility Reviewer

(“Instrumentation & Pipeline Auditor”)

Role

Ensure the experiment can be reproduced and interpreted, and that evaluation artifacts are correctly handled.

Responsibilities

Check:

experimental design clarity,

adapter training details,

inference parameters,

response classification rules,

unclear-rate handling.

Flag anything that could:

bias results,

obscure failure modes,

or make replication ambiguous.

Pay special attention to evaluation failure handling.

Must NOT do

Interpret results cognitively.

Question the value of the negative result.

Propose theoretical explanations.

Output format

Checklist with:

“Clear / Needs clarification / Missing”

Short notes on interpretability risks.

Success criterion

A reader could:

re-run the experiment and understand which results are interpretable and which are not.

Reviewer 3: Skeptical Cognitive Scientist

(“Human-Paradigm Stress Test”)

Role

Read the paper as someone who believes Costa et al. (2014) is correct and is skeptical of LLM analogies.

Responsibilities

Identify:

where human studies might be mischaracterized,

where LLM behavior might be over-compared to humans,

where alternative explanations (e.g., task difficulty, probability comprehension) are plausible.

Assess whether the paper treats human work fairly and neutrally.

Must NOT do

Defend LLMs or critique ML methods.

Argue that the FLE “should” exist in models.

Demand new behavioral tasks.

Output format

Short narrative critique:

“From a cognitive science perspective, the following points may raise concern…”

Focus on interpretive framing, not results.

Success criterion

A CogSci reader says:

“Even if I disagree, this paper is careful and fair.”

Feedback Integration Protocol
Step 1: Agent Reviews (Parallel)

Each reviewer submits feedback independently.

No reviewer sees the others’ comments.

Step 2: Human Synthesis (You)

Your role is editor-in-chief, not implementer.

You should:

Identify overlapping concerns across reviewers.

Decide which feedback:

narrows claims (high priority),

clarifies methods (high priority),

is optional or stylistic (low priority).

Reject any feedback that:

expands claims,

re-opens settled scope decisions,

adds speculative interpretation.

You produce:

A prioritized change list (not edits).

Step 3: Assistant Pass (Me)

My role is surgical editor and epistemic enforcer.

I will:

Rewrite only the sections affected by accepted feedback.

Ensure proxy vs. evaluation separation remains intact.

Check that no new claims are accidentally introduced.

Normalize tone and style across revisions.

I will not:

Add new content.

Add new claims.

Add new citations unless explicitly instructed.

Global Constraints (All Reviewers)

Do not suggest new experiments.

Do not suggest expanding scope.

Treat non-compliant responses as data, not noise.

Respect the distinction between:

Proxy failure (conceptual),

Evaluation failure (instrumental).

One-Sentence North Star

The purpose of this paper is to report where a specific operationalization fails, not to explain the Foreign Language Effect or human cognition.
