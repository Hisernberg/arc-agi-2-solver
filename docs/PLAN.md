# ARC-AGI-2 Competition Strategy & Implementation Plan

## Competition Overview
- **Objective**: Solve novel abstract reasoning tasks (grid transformations, integers 0-9)
- **Format**: Each task has 2-10 train pairs (demonstrations) + test input → predict output
- **Scoring**: Exact cell match, 2 attempts per task output, averaged across all outputs
- **Baseline**: LB 33.89 (NVARC + Qwen3-4B per-task LoRA)
- **Goal**: Beat 33.89, aim for 85%+ ($150K bonus)
- **Limit**: 1 submission/day, 12h GPU notebook limit

## Dataset Analysis (Actual Data)

| Dataset | Tasks | Outputs | Notes |
|---------|-------|---------|-------|
| training | 1000 | ~3000 | Full solutions available |
| evaluation | 120 | 172 | For local validation |
| test (hidden) | 240 | ~257 | For leaderboard |
| sample_submission | 240 | - | Format template |

### Key Findings from Analysis
- **Simple heuristics score 0.0000** on eval set — all 120 tasks require ML model
- Output/input area ratio: mostly 1.0 (same-size), some 0.1-0.5 (shrink), 4-9x (expand)
- Color changes occur in ~44% of tasks
- 17/240 test tasks have 2+ test outputs
- Most common grid size: 10x10 (27 test tasks)
- Train pairs per task: 2-10, most common 3 (132 test tasks have 3 pairs)

## Technical Architecture

### Baseline: NVARC (LB 33.89)
Based on `qwen3_4b_grids15_sft139` (Qwen3-4B BF16, fine-tuned on ARC grids).

**Complete Pipeline:**
1. **Grid Tokenizer**: `[[0,1],[2,3]]` → `"01\n23\n"` (row-wise digit string)
2. **Augmented Training**: 8 geometry × 16 color perm = 128 sequences per task
3. **Per-task LoRA**: r=256, 1 epoch, LR=5e-5, bf16
4. **Turbo DFS Decoding**: GPU-efficient DFS on 12 ARC tokens, prob threshold 0.2
5. **Candidate Scoring**: `score_kgmon` = vote_count − mean(augmented_NLL)
6. **4-Worker Parallel**: 4× L4 GPU, cheap-first task ordering
7. **Phase 1 + Phase 2**: Primary pass + adaptive deep search

### Enhancements in This Notebook
- **Checkpoint/Resume**: Per-worker state saving for interrupted runs
- **Phase 2 Adaptive**: Lower threshold (0.1), more augmentations (24), longer DFS window
- **Schema Hardening**: Robust fallbacks (identity/zero-fill)
- **Debug Mode**: 4-task debug run to validate pipeline before full submission

## Project Structure
```
arc-agi-2/
├── notebooks/
│   └── arc_agi2_advanced.ipynb    ← MAIN SUBMISSION NOTEBOOK
├── scripts/
│   ├── arc_loader_full.py         ← Extracted from NVARC notebooks
│   ├── arc_decoder_full.py
│   ├── arc_solver_full.py
│   ├── starter_full.py
│   ├── kaggle_submit.py           ← Kaggle API manager
│   └── github_sync.py             ← GitHub integration
├── dataset/                        ← Competition data
├── docs/
│   ├── PLAN.md
│   └── METHODOLOGY.md
└── results/
    └── submission_history/
```

## Submission Workflow

### Before Each Submission
1. Run notebook in DEBUG mode → get local eval score
2. Compare to previous eval scores
3. If improved → commit and submit to Kaggle
4. If not improved → modify approach and re-validate

### Submission Priority
1. **First priority**: Get NVARC baseline running → expect ~33.89
2. **Second priority**: Improve augmentation (more views, color permutations)
3. **Third priority**: Ensemble scoring (kgmon + probmul)
4. **Fourth priority**: Phase 2 deep search tuning
5. **Fifth priority**: Larger model or multi-model ensemble

## Key Implementation Details

### DFS Decoding (turbo_dfs)
- Only 12 ARC tokens moved to CPU (digits 0-9, newline, `<|im_end|>`)
- Cumulative probability threshold: 0.2 (Phase 1), 0.1 (Phase 2)
- DFS window: 540s (Phase 1), 720s (Phase 2)
- Task cap: 1200s (Phase 1), 1800s (Phase 2)

### Augmentation Strategy
- **Geometry**: Identity, rot90, rot180, rot270, flip-H, flip-V, flip-both, transpose
- **Color perm**: 16 random permutations (Phase 1), 24 (Phase 2)
- **Total**: 128 sequences (Phase 1), 192+ (Phase 2)

### Candidate Scoring
- `score_kgmon = len(unique_outputs) − mean(mean(scores_per_aug))`
- Candidates grouped by exact grid match
- Top-2 per output key selected as attempt_1/attempt_2

## Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 12h timeout | High | Lose partial work | Cheap-first ordering, checkpoint |
| Model not found | Low | No inference | Multiple model paths, upload model |
| OOM errors | Medium | Task failures | Per-task exception handling, worker restart |
| Score regression | Medium | Wasted submission | Always validate on eval set first |
| Kaggle quota | Medium | Can't submit | Monitor L4 usage, disable when idle |

## Score Targets
| Milestone | Target | Strategy |
|-----------|--------|----------|
| Baseline | 33.89 | NVARC exactly as published |
| Phase 1 | 35-38 | Better augmentation, Phase 2 tuning |
| Phase 2 | 38-45 | Ensemble scoring, more candidates |
| Phase 3 | 45-60 | Larger model, multi-model ensemble |
| Top tier | 60-85+ | Full optimization, meta-learning |

## Current Status
- [x] Dataset fully analyzed
- [x] All notebooks extracted and understood
- [x] Advanced notebook built (NVARC + Phase 1/2 + checkpoint)
- [x] Kaggle submission manager created
- [x] GitHub sync infrastructure created
- [x] Local eval baseline established (heuristics = 0.0000)
- [ ] Kaggle submission: PENDING
- [ ] Phase 2 scoring improvements
- [ ] Ensemble scoring (kgmon + probmul)
- [ ] Multi-model approaches

---
*Generated: 2026-09-18 | Baseline: LB 33.89 (NVARC + Qwen3-4B)*
