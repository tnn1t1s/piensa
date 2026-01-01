# Reviews Structure Documentation

## Directory Layout

```
reviews/
├── cogsci_final.md          # Latest CogSci review
├── methods_final.md         # Latest Methods review
├── epistemic_final.md       # Latest Epistemic review
└── {model-name}/            # Historical reviews by model
    ├── cogsci_{timestamp}.md
    ├── methods_{timestamp}.md
    └── epistemic_{timestamp}.md
```

## Review Types and Formats

### 1. CogSci Review (cogsci_final.md)

**Purpose**: Evaluates paper from cognitive science perspective
**Model**: anthropic/claude-sonnet-4.5

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

### 2. Methods Review (methods_final.md)

**Purpose**: Evaluates reproducibility and methodological rigor
**Model**: anthropic/claude-sonnet-4

**Structure**:
- `## Methods & Reproducibility Review`
- Subsections with `###` headers
- Each item marked: Clear, Needs clarification, Missing, or Interpretability risk
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

### 3. Epistemic Review (epistemic_final.md)

**Purpose**: Claim-scope audit for epistemic hygiene
**Model**: anthropic/claude-sonnet-4.5

**Structure**:
- `# Epistemic Hygiene Review: Claim-Scope Audit`
- `## Critical Overreaches` with numbered items
- Each item has: Quoted, Why it overreaches, Suggested rewrite
- `## Rhetorical Drift Patterns` with named patterns
- `## Structural Issues`
- `## Positive Examples`
- `## Summary Recommendation`

**Key patterns identified**:
- "Consistent with" Drift
- Proxy-Evaluation Collapse
- Universal Quantifiers

## Output Locations for Summary Agent

For writing a review addendum, the agent should read:
1. `reviews/cogsci_final.md` - CogSci concerns
2. `reviews/methods_final.md` - Methods/reproducibility
3. `reviews/epistemic_final.md` - Claim-scope issues
