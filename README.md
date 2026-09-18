# ARC-AGI-2 Competition Solver

## Overview
This project implements a **neuro-symbolic hybrid approach** to solve ARC-AGI-2 abstract reasoning tasks on Kaggle, combining:
- **NVARC**: Qwen3-4B with per-task LoRA test-time training
- **DSL Program Search**: 15 ARC primitives with BFS program synthesis  
- **Refinement Loop**: Holistic Trace Judging + cross-view verification
- **Hybrid Ensemble**: Neural + Symbolic + Algorithmic scoring fusion

## Kaggle Notebooks
1. **arc-agi2-highscore-lb33-89-replica** - Baseline NVARC v1 (Complete: 62.5% on 4 eval tasks)
2. **arc-agi2-v2-neurosymbolic** - Enhanced with DSL + Refinement (Ready for submission)

## Architecture
```
Input Grids → Grid Tokenizer → Qwen3-4B (LoRA TTT) → Turbo DFS → Candidate Pool
                                                                     ↓
                                        DSL Program Search (parallel) → 
                                                                     ↓
                              Holistic Trace Judging (min-NLL) + Ensemble Scoring
                                                                     ↓
                                    Top-2 Candidates → submission.json
```

## Research Basis
- **"Modality-Driven Search with Holistic Trace Judging"** (Semi-private eval: 72.9%)
- **"ARC Prize 2025: Technical Report"** (Refinement loops as defining theme)
- **"GPT-5.2 & ARC-AGI-2 Benchmark Analysis"** (SOTA progression tracking)
- **NVARC** (ARC Prize 2025 winner open-source implementation)

## Key Innovations
1. **Min-NLL scoring** instead of mean-NLL (fixes over-scoring)
2. **Holistic Trace Judging**: Judge entire candidate trace holistically
3. **DSL Program Search**: For low-confidence neural predictions
4. **Refinement Loop**: Self-verification using cross-view consistency
5. **Hybrid Ensemble**: Weighted fusion of scoring functions

## Files
- `notebooks/arc_agi2_v2_neurosymbolic.ipynb` — Main notebook (Phase 1+2+3)
- `notebooks/arc_agi2_highscore_lb3389.ipynb` — Baseline replica
- `scripts/arc_loader_full.py` — Grid tokenizer + augmentation
- `scripts/arc_solver_full.py` — Per-task LoRA + turbo DFS
- `scripts/arc_decoder_full.py` — Candidate scoring (multiple algorithms)
- `scripts/starter_full.py` — Multi-worker orchestration
- `scripts/kaggle_submit.py` — Kaggle API manager
- `scripts/github_sync.py` — GitHub integration
- `docs/PLAN.md` — Strategy plan
- `docs/METHODOLOGY.md` — Technical approach

## Status
- ✅ GitHub repository synced
- ✅ v1 notebook completed on Kaggle (62.5% eval)
- ✅ v2 notebook pushed to Kaggle (ready for full run)
- 🔄 Waiting for v1 leaderboard score
- 📋 Next submission planned after analysis

## Kaggle Links
- [arc-agi2-highscore-lb33-89-replica](https://www.kaggle.com/code/kragglenote2forwork/arc-agi2-highscore-lb33-89-replica)
- [arc-agi2-v2-neurosymbolic](https://www.kaggle.com/code/kragglenote2forwork/arc-agi2-v2-neuro-symbolic-refinement-loop)

## Usage
```bash
# Setup Kaggle credentials
python scripts/kaggle_submit.py init

# Score local submission on eval set
python scripts/kaggle_submit.py score-eval --submission results/submission.json

# Validate schema
python scripts/kaggle_submit.py validate --submission results/submission.json
```

---
*Built for ARC Prize 2026 - ARC-AGI-2 Competition | Target: 85%+ accuracy*
