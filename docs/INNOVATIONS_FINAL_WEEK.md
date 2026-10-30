# ARC-AGI-2 — Final-Week State, Public-Art Survey & Innovation Candidates

**Prepared:** 2026-10-30 · Context: 3 slots left (Oct 31, Nov 1, Nov 2). Oct-30 slot used: ref 57808321 (v19 pinned draw). Freeze discipline active.

---

## 1. Where the score actually comes from (receipts)

| Family | Draws | Band |
|---|---|---|
| **v19 PB-faithful recipe** (`dasshovon/arc26-nvarc-v1` v19) | 29.72 / **32.64** / 31.39 | **~31** |
| v3x lineage (v32d, v34, v35, v36b, v37, v39, v41) | 25.69–30.97 | ~28.3 |
| failed-in-aimo kernel | 29.31 / 30.97 | ~30 |

**The simple recipe out-draws the engineered one.** v19 (pure NVARC replica) beats every levered build. This is the strongest evidence we have: on hidden data, added machinery has been net-negative or neutral vs. the faithful draw.

**Binding constraint (from MASTER_PLAN_INTEGRATION, finding #11):** pool recall = **32.7%** on v6full full-eval. Selection has ~0 headroom (finding #12 — olympics replay). Points live in *generating* the right grid, not ranking it.

## 2. Public best work — what actually wins

| Approach | Score | Takeaway |
|---|---|---|
| NVARC / Qwen3-4B TTT + DFS (2025 winner, our base) | ~24–33 LB | Per-task LoRA + batched DFS + prob-ranked selection — already ours |
| Pragnyan Ramtha (#1 blog) | – | Same lineage + consistency-filtered candidates vs augmented views — we have this (shape-a2, fused scorer) |
| Land, Modality-Driven Search + Holistic Trace Judging | **72.9% semi-private** | Frontier-API ensemble across text/image/code channels with a joint judge — **requires internet/API access; not mountable on Kaggle's offline kernels** |
| Poetiq (Gemini-3-Pro code-gen) | 54% semi-private | Programs > direct grids; also API-bound |
| Beiciccc reproductions | 25.97–32.22 | Confirms our band; public artifacts cap ~32 |

**Honest read:** everything above ~54 uses commercial frontier models. The 76.94 top LB (if real on private) is not reachable on an offline L4×4 pin with open weights in 3 days. The winning *ideas* that ARE portable: **candidate diversity across modalities** and **judging whole candidate sets jointly**.

## 3. Staged-but-unsubmitted assets

| Asset | State | Receipt |
|---|---|---|
| `arc26-nvarc-v40-r-council-refill-redraw` (v1) | **Commit-proven, never submitted** | leg_gate PASS, 27B leg up (24 seqs, ~470 tok/s), 5/12 debug exact, pool precision 1.0 — the council-refill lever the plan reserved |
| v41 tb64-serve envelope | Submitted Oct-27 | **29.03** — in-band, not above family |
| Tool fill v2 (widened dihedral/cmap/shift/tile/kron) | CLOSED | eval 0/120 — closed per receipts, don't re-litigate |

## 4. Recommended slot plan (EV-ranked)

- **Oct 31:** submit **v40-R v1** — the one receipted lever never drawn. Information + upside; council refill targets the exact constraint (more distinct a2 candidates in the leftover window).
- **Nov 1:** submit the **highest-scored receipted config** after Oct-30/31 scores land (default v19 if bands hold).
- **Nov 2 (final):** **v19** — best band, fewest levers, most robust. If v40-R draws >32.64 on Oct-31, re-draw v40-R instead.

## 5. Innovation candidates (documented for post-deadline / next cycle — none are slot-safe now)

1. **Cross-modal candidate generation** — port Land's insight offline: generate candidates as (a) raw grids, (b) programs, (c) image-channel decodes using the render.py arm that already exists in leg27b. Requires a vision-capable mounted model — no mountable VLM receipt exists today.
2. **Joint holistic judging** — replace per-candidate scoring with one long-context pass where the 27B compares all traces. Needs the leg window + a judge prompt; ~1 slot risk, plausible +0.5–2.
3. **Refinement loop (2025's winning theme)** — per-task iterative program repair guided by demo-fit feedback. Our atlas sidecar has the pieces (verified primitives + fit/apply); a bounded repair loop (≤3 rounds) is the honest medium-term build.
4. **Zero-pretrain tiny TTT net** — ARC-2025 showed ~7M-param networks trained from scratch per task are competitive; CPU-side leg, zero GPU cost, genuinely novel on this leaderboard.
5. **Widened leg routing** — router shows `votes0_undecoded: 167` outputs routed with empty pools; relaxing route_budget one tier targets recall directly (was the Oct-28 candidate lever).
6. **Speculative self-consistency in DFS** — weight beam scores by cross-augmentation agreement (Ramtha's filter), implemented inside `score_candidates` rather than as a post-pass.

## 6. Standing warnings

- **Do not submit anything that hasn't committed green.** Every band-bottom draw so far came from an untested or known-regressive build (v35 21.94).
- **Do not burn a slot on Track-B ARC-3 hardware probes from an ARC-2 submission.**
- **The tool lane stays parked** — eval is closed to unique-exact rule families (0/120 twice).
