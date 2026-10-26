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

## Oct-26 — v39: proven Qwen3.8-27B leg strike (user directive)

- Built + pushed `arc26-nvarc-v39` (sha f03274cb): v34b-core lineage (band 27.36–30.97, PB 32.64)
  + shape-aware attempt_2 (ref 57630786) with `ARC_V38_LEG_SWAP` FORCED 0 — the proven
  `qwen3-8-27b-fp8-repacked-v1` model source boots; Tufa Qwen3.6 glob inert.
- **Verified-tool degenerate fill** implemented in-cell and PARKED (`ARC_V39_TOOLFILL=0`):
  dihedral(8) × color-permutation unique-exact sweep over all train pairs; fires only on
  both-`[[0]]` lost entries. Local receipts (full 1,120-task sweep, `oct26_v39/toolfill_receipts.json`):
  train 11/1000 fired, **11/11 transfer P=1.000** (4 color-only, 7 rotation-only); eval **0/120 fired**
  → zero EV today; one flag from arming. Tool lane widens Oct-27 (translation, tiling, object ops).
- Build gates: byte-identity cells 1-19/21-29/31/33-35 exact + cell-20 append-only + AST clean.
- Chain: `oct26_v39/*.sanitized.py` (build → push → status → gate → submit; tokens rotated out).

**Receipt 10:12 UTC Oct-26**: commit ALL GATES PASS (120 tasks / 91,636 cells / both-[[0]]=0);
G4 boot receipt = `qwen3-8-27b-fp8-repacked-v1` (proven Qwen3.8-27B leg served as directed);
**SUBMITTED ref 57662636** — scored rerun in flight, score Oct-27 morning.

## Oct-26 evening — gold push plan + v40 staged (3.8 series locked)

- **Model doctrine**: Qwen3.8-27B FP8 (`qwen3-8-27b-fp8-repacked-v1`) = every remaining ARC-2
  slot (user directive; boot-receipted in v39 ref 57662636). Qwen3.8-Flash-Next (125B-A6B,
  `qwen4_exp`, NVFP4) = ARC-3 track only — not mountable on the L4×4 vLLM 0.19 pin.
- **Tool lane CLOSED with receipts** (`oct26_v40/toolfill_receipts_v2.json`): widened space
  (dihedral×cmap + shift + tile + kron) → train 17 fired, 16/17 transfer P=0.941; **eval 0/120**.
- **v40 staged** (`oct26_v40/`): proven 3.8 leg + ONE lever = low-effort council refill
  (`ARC_V40_COUNCIL=1`: v34-A refill jobs as no-think fast-pass, ~10× cheaper → more distinct
  a2 candidates in the leftover window; kill switch → byte-identical v34 refill). Gates all pass.
- **Gold push plan**: `oct26_v40/ARC26_Gold_Push_Plan_Oct26_v1.md` — day-by-day Oct 27 → Nov 2,
  lever ledger L1–L10, 40+ honesty box (ARC-2 target = silver cement 33.89; the only 40+ door
  = ARC-3 lane, bounded bet, kill rule Oct-29 EOD), Track B never touches ARC-2 slots.
- Rollback receipt: session files lost to a sandbox reset were RESTORED from this mirror
  (commits 5a69eb9/42b81c2) — mirror discipline works; keep pushing every artifact.
