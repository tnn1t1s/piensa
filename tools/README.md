# Piensa Tools

Composable CLI tools for the Piensa project. All tools follow Unix conventions: read from stdin or file, output to stdout, status to stderr.

## Usage

All tools are in `tools/bin/`. Run from project root with venv activated:

```bash
source .venv/bin/activate
tools/bin/TOOLNAME [args]
```

## Tools

### test-prompt

Test a prompt against Mistral with a LoRA adapter. Outputs JSON results to stdout.

```bash
# Pipe prompt from stdin
echo "Choose A or B:" | tools/bin/test-prompt --adapter zh --trials 10

# Read from file
tools/bin/test-prompt prompt.txt --adapter zh --trials 10

# Pipe to jq for specific metrics
echo "..." | tools/bin/test-prompt -a zh -n 10 | jq '.p_clear'

# Verbose mode shows individual responses
tools/bin/test-prompt - --adapter zh -n 5 -v
```

**Options:**
- `--adapter/-a`: Required. One of: en, es, he, zh
- `--trials/-n`: Number of trials (default: 10)
- `--temperature/-t`: Temperature (default: 0.7)
- `--max-tokens`: Max tokens per response (default: 50)
- `--verbose/-v`: Show individual responses to stderr

**Output:** JSON with counts, probabilities (p_A, p_B, p_unclear, p_clear), and raw responses.

### cat-paper

Concatenate paper sections into a single document.

```bash
tools/bin/cat-paper                    # Full paper
tools/bin/cat-paper --no-appendix      # Without appendix
```

### review-epistemic, review-methods, review-cogsci

LLM-based paper reviewers with different perspectives.

```bash
# Pipe paper content
tools/bin/cat-paper | tools/bin/review-epistemic -

# Or pass file directly
tools/bin/review-methods paper.md

# Override model
tools/bin/review-cogsci --model openai/gpt-4.5-preview paper.md
```

### review-paper

Run all reviewers in sequence.

```bash
tools/bin/review-paper paper.md
```

## Evaluation Tools

Composable tools for evaluating LoRA adapters. Each tool logs progress to stderr with flush.

### generate-one

Generate a single response. Atomic unit for evaluation.

```bash
echo "What is 2+2?" | tools/bin/generate-one
echo "What is 2+2?" | tools/bin/generate-one --adapter old_birds
```

### eval-question

Evaluate one question N times.

```bash
tools/bin/eval-question --question military_tech --samples 3
tools/bin/eval-question --question military_tech --samples 3 --adapter old_birds
```

### eval-adapter

Evaluate all questions for one adapter.

```bash
tools/bin/eval-adapter --samples 3                           # baseline
tools/bin/eval-adapter --samples 3 --adapter old_birds       # with adapter
tools/bin/eval-adapter --samples 3 --adapter old_birds -o results/old_birds.json
```

### eval-compare

Compare results from multiple adapter evaluations.

```bash
tools/bin/eval-compare results/baseline.json results/old_birds.json
tools/bin/eval-compare results/*.json --format markdown
```
