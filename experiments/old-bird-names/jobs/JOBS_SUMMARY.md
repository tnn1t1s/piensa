# Fine-Tuning Jobs Summary

Dataset: `ft_old_audubon_birds_openai.jsonl`
SHA256: `d201ce1152086cf9fc5facb9ffc6c6f2e946a155c7f9a561108412c66d1cfbbf`
Samples: 208

## Submitted Jobs

| # | Job ID | Model | Epochs | LR | Suffix | Status |
|---|--------|-------|--------|-----|--------|--------|
| 1a | ftjob-sK2GyD1AtLG7SHrsbMUoJ2Jv | gpt-4.1-2025-04-14 | 3 | 2.0 | old-birds-4.1-e3-r1 | validating_files |
| 1b | ftjob-eYAqvpWwAF5q0JeTW6i428uD | gpt-4.1-2025-04-14 | 3 | 2.0 | old-birds-4.1-e3-r2 | validating_files |
| 2 | ftjob-TKKJkIJEZm2JtbQMokwu8L6d | gpt-4.1-mini-2025-04-14 | 3 | 2.0 | old-birds-mini-e3 | validating_files |
| 3 | ftjob-Un9SSW85cBcyWBhvokuQinTu | gpt-4.1-nano-2025-04-14 | 3 | 0.1 | old-birds-nano-e3 | validating_files |
| 4 | ftjob-CfEHRM1yf6Dy6twGkYuhcuZZ | gpt-4.1-2025-04-14 | 6 | 2.0 | old-birds-4.1-e6 | validating_files |
| 5 | -- | gpt-4.1-2025-04-14 | 10 | 2.0 | old-birds-4.1-e10 | RATE LIMITED (retry when slot opens) |

## Notes
- Job 5 hit the 3-concurrent-job limit for gpt-4.1. Submit after one of jobs 1a/1b/4 completes.
- All jobs use batch_size=1 (matches paper)
- Nano uses lr_mult=0.1, others use lr_mult=2.0 (matches paper)

## Check Status
```bash
source .venv/bin/activate
python tools/bin/openai-job-status ftjob-sK2GyD1AtLG7SHrsbMUoJ2Jv
```
