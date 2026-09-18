# ARC-AGI-2 Competition Solver

## Overview
Neuro-symbolic hybrid approach: Qwen3-4B LoRA TTT + DSL Program Search + Holistic Trace Judging + Refinement Loop.

## Kaggle Notebooks
| Notebook | Status | URL |
|----------|--------|-----|
| v1 HighScore Replica | Complete (62.5% eval) | [arc-agi2-highscore-lb33-89-replica](https://www.kaggle.com/code/kragglenote2forwork/arc-agi2-highscore-lb33-89-replica) |
| v2 Neuro-Symbolic | Pushed | [arc-agi2-v2-neuro-symbolic-refinement-loop](https://www.kaggle.com/code/kragglenote2forwork/arc-agi2-v2-neuro-symbolic-refinement-loop) |
| **v3 Definitive** | **Pushed (Binary Fixed)** | [arc-agi2-v3-definitive-binary-conflict-fixed](https://www.kaggle.com/code/kragglenote2forwork/arc-agi2-v3-definitive-binary-conflict-fixed) |

## Architecture
- **Neural**: Qwen3-4B + per-task LoRA + Turbo DFS
- **Symbolic**: 15 ARC primitives + BFS program search
- **Algorithmic**: Holistic Trace Judging (min-NLL) + Refinement Loop
- **Ensemble**: kgmon + probmul + vote count fusion

## Key Fixes (v3)
- Resolves numpy/sklearn binary conflict from unsloth patch
- Pins numpy before torch import
- Forces sklearn reinstall after unsloth setup
- Comprehensive error handling with worker restart

## Research Basis
- Modality-Driven Search with Holistic Trace Judging (72.9% semi-private eval)
- ARC Prize 2025 Technical Report (refinement loops)
- NVARC (ARC Prize 2025 winner, LB 33.89)

## Files
- `notebooks/arc_agi2_v3_definitive.ipynb` — Main notebook (9 cells)
- `scripts/arc_loader_full.py`, `arc_solver_full.py`, `arc_decoder_full.py`, `starter_full.py`
- `scripts/kaggle_submit.py`, `github_sync.py`
- `docs/PLAN.md`, `docs/METHODOLOGY.md`

## Quick Start
1. Open v3 notebook on Kaggle
2. Click "Commit" (12h GPU run)
3. After completion, check output for eval score
4. If score > previous → Submit to Competition

---
*Target: 85%+ accuracy | Built for ARC Prize 2026*
