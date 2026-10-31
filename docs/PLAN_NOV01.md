# Nov-1 slot plan — best-possible-submission decision tree

_Updated 2026-10-31 ~18:45 UTC. Deadline Nov-2 23:59 UTC. Slots used: Oct-30 ref 57808321 (v19), Oct-31 ref 57829160 (v40-R, fired by automation 06:21 UTC, still scoring). Remaining: Nov-1 + Nov-2._

## Current score state

All public scores still blank on Kaggle (`publicScoreLeaderboardDisplay: None`) — kernel reruns take hours on the 12h-budget pipeline. v40-R's score is expected late Oct-31/Nov-1 morning.

## What the public record says (verified Oct-31)

- **LB structure**: top is 88.06; top ~49 teams above 41. Everything >~54 is commercial-API (Gemini-3-Pro, GPT-5.2 Pro) — unreachable on offline L4×4 kernels.
- **Open-weight ceiling**: every public notebook attaches NVARC's `qwen3_4b_grids15_sft139` (the 2025 winner, 24.03% private). Public draws run 26.9–33.9; Beiciccc's same-artifact reruns show 25.97–32.22 variance. **~32-34 is the reproducible ceiling for open weights.**
- **Ritwika Kancharla's program-induction experiment** (most useful public finding): Qwen3.8-27B writes Python rules, harness verifies against train pairs — verified programs are correct on test only 67% (10/15), and self-consistency agreement does NOT raise it. Conclusion: **candidate selection, not program synthesis, is the bottleneck** — consistent with our receipts (pool recall 32.7%, selection ~0 headroom).

## Nov-1 slot (fires 06:17 UTC via automation auto-58fe1397)

Decision tree the submission session follows:

1. If v40-R (ref 57829160) has landed a score **> 32.64**: it becomes the best receipted config → **Nov-2 goes to v40-R redraw**; Nov-1 submits **v19** (variance draw of the best band).
2. If v40-R scored **< ~29** or failed: council-refill is net-negative → Nov-1 submits **v19**; Nov-2 **v19** again (or v41 29.03 band if v19's Oct-30 draw craters <28).
3. If scores are still blank at fire time: Nov-1 submits **v19** (highest-EV receipted config).

## Why not a new build for Nov-1

Doctrine: nothing unreceipted gets submitted. Every unproven levered build drew below the base band (v35 → 21.94). The one commit-proven untried lever (v40-R) already went out today. Building + validating a new kernel variant in <1 day has zero precedent for landing in-band — the EV-max move is draws of proven configs, not a rushed build.

## Advanced assets already staged (foundation for next cycle / post-deadline)

- `Nabidnur/arc-agi-2-solver-traces` (HF): six products over 4226 deduped tasks — dynamic-action traces, mixture-of-solvers coverage, two-round agent-debate transcripts, solver reliability priors, task routing features, hard cases (552 contested + 32 false-confidence + 12 unsolved-with-candidate). Direct SFT material for a learned Qwen3.8 router/judge.
- Verified-program-induction merge (Ritwika's recipe): our leg-C/arm already has fit/apply primitives + demo verification; a Qwen3.8-27B "program-writer + demo-checker + judge" head is the highest-upside post-deadline build, trained on the coverage/hard-cases rows.
- Innovation backlog (cross-modal candidates, holistic judging, refinement loop, tiny TTT net): docs/INNOVATIONS_FINAL_WEEK.md §5.

## Honest expectation

Realistic ceiling: ~33-34 (v19's band peak was 32.64; silver is 33.89). 40%+ requires capabilities no open-weight offline submission has demonstrated. We take the max-EV path: two more draws, best receipts, freeze discipline.
