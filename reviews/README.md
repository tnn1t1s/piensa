# Reviews Structure Documentation

This directory contains peer review outputs from three specialized LLM reviewers.

## Directory Layout

```
reviews/
├── README.md                # This file
├── cogsci_final.md          # Latest CogSci review
├── methods_final.md         # Latest Methods review
├── epistemic_final.md       # Latest Epistemic review
└── {model-name}/            # Historical reviews by model
    ├── cogsci_{timestamp}.md
    ├── methods_{timestamp}.md
    └── epistemic_{timestamp}.md
```

## Review Types

### 1. CogSci Review (`cogsci_final.md`)

**Purpose**: Evaluates paper from cognitive science perspective

**Default Model**: `anthropic/claude-sonnet-4.5`

**Structure**:
- `## Review: From a Cognitive Science Perspective`
- Numbered sections (1-8) with topic headers
- Each section has bold topic, then analysis
- `### Summary Assessment` with numbered recommendations

**Key sections**:
1. Fundamental Operationalization Gap
2. Treatment of Probability Comprehension
3. Missing Human Baseline Creates Interpretation Problem
4. The Spanish Anomaly as Central, Not Peripheral
5. "Universal Framing Effects" Claim Needs Scrutiny
6. Task Difficulty vs. Processing Mode Confound
7. Role of Training Data Distributions
8. Comparison to Costa et al. (2014) Framing

**Invocation**:
```bash
tools/bin/cat-paper --no-appendix | tools/bin/review-cogsci - > reviews/cogsci_final.md
```

---

### 2. Methods Review (`methods_final.md`)

**Purpose**: Evaluates reproducibility and methodological rigor

**Default Model**: `openai/gpt-4.5-preview` (use `--model anthropic/claude-sonnet-4` if unavailable)

**Structure**:
- `## Methods & Reproducibility Review`
- Subsections with `###` headers
- Each item marked **Clear**, **Needs clarification**, **Missing**, or **Interpretability risk**
- `### Summary` paragraph at end

**Key sections**:
- Experimental Design Clarity
- Adapter Training Details
- Inference Parameters
- Response Classification Rules
- Unclear-Rate Handling
- Critical Reproducibility Issues
- Evaluation Failure Handling
- Replication Feasibility

**Invocation**:
```bash
tools/bin/cat-paper --no-appendix | tools/bin/review-methods --model anthropic/claude-sonnet-4 - > reviews/methods_final.md
```

---

### 3. Epistemic Review (`epistemic_final.md`)

**Purpose**: Claim-scope audit for epistemic hygiene

**Default Model**: `anthropic/claude-sonnet-4.5`

**Structure**:
- `# Epistemic Hygiene Review: Claim-Scope Audit`
- `## Critical Overreaches` with numbered items
- Each item has: **Quoted**, **Why it overreaches**, **Suggested rewrite**
- `## Rhetorical Drift Patterns` with named patterns
- `## Structural Issues`
- `## Positive Examples`
- `## Summary Recommendation`

**Key patterns identified**:
- "Consistent with" Drift
- Proxy-Evaluation Collapse
- Universal Quantifiers

**Invocation**:
```bash
tools/bin/cat-paper --no-appendix | tools/bin/review-epistemic - > reviews/epistemic_final.md
```

---

## Running All Reviewers

To run all three reviewers in parallel:

```bash
source .venv/bin/activate

# Run all three in background
tools/bin/cat-paper --no-appendix | tools/bin/review-cogsci - > reviews/cogsci_final.md 2>&1 &
tools/bin/cat-paper --no-appendix | tools/bin/review-methods --model anthropic/claude-sonnet-4 - > reviews/methods_final.md 2>&1 &
tools/bin/cat-paper --no-appendix | tools/bin/review-epistemic - > reviews/epistemic_final.md 2>&1 &

# Wait for completion
wait
```

## Writing a Review Summary Addendum

For an agent to write a review summary addendum to the paper, it should:

1. Read all three review files:
   - `reviews/cogsci_final.md`
   - `reviews/methods_final.md`
   - `reviews/epistemic_final.md`

2. Synthesize across the three perspectives:
   - **CogSci**: Theoretical/conceptual concerns about the L1/L2 operationalization
   - **Methods**: Reproducibility gaps and methodological clarity
   - **Epistemic**: Claim-scope mismatches and suggested rewrites

3. Identify:
   - Consensus issues (raised by multiple reviewers)
   - Reviewer-specific concerns
   - Actionable revisions vs. acknowledged limitations

4. Output format should match paper section style (markdown with `##` headers)
