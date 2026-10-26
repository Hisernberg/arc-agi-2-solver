# ARC26 Gold Push Plan — Oct 26 (evening) → Nov 2
**Directive:** standardize on Qwen 3.8 series from now on · gather everything · best plan to win · 40+ if possible.
**Prepared:** 2026-10-26 19:00 UTC · Owner: dasshovon (merged team) · Status: v39 (ref 57662636) in scored rerun.

---

## 1. Standings snapshot (receipts, 18:38 UTC Oct 26)

| Metric | Value |
|---|---|
| Personal best | **32.64** |
| Scored draws (family, n=9) | 29.31, 28.06, 29.31, 29.31, 29.86, 27.36, 28.61, 25.69, **27.36 (v37-exp, Oct-26)** |
| Band mean / sd | ~28.3 / ~1.25 |
| Silver line | 33.89 (≈rank 108) |
| ARC-2 gold | 66.53 (rank 16) — not reachable on this track in 5 days |
| ARC-3 gold | 38.20 (rank 19/4702) — the only honest 40+ door |
| In flight | **v39 (57662636)**: proven Qwen3.8-27B leg forced, score Oct-27 morning |
| Slots left | Oct 27, 28, 29, 30 + finals picks Nov 1–2, final submission Nov 2 |
| Quota | Overdraft non-blocking for competition commits (receipted ×3); refresh Oct-31 00:00Z |

**Reading of the last two draws (25.69, 27.36):** bottom-of-band but in-band (27.36 = band floor exactly, z≈−0.8 on n=9). Family intact; no serving audit trigger (that needs two sub-27.4 draws). Posture: keep shipping the proven family, one receipted lever at a time.

---

## 2. Model doctrine — Qwen 3.8 series (user directive, locked)

**ARC-2 track (all remaining slots): Qwen3.8-27B FP8 — `foysalemonshanto/qwen3-8-27b-fp8-repacked-v1`** (arch `qwen3_5`, covered by the vLLM 0.19 pin).
- Boot-receipted in v39 (G4: `LEG_BOOT_MODEL=qwen3-8-27b-fp8-repacked-v1`) — the leg actually served.
- `ARC_V38_LEG_SWAP` stays **0** in every future build: Tufa Qwen3.6 glob inert, 3.8 is THE leg.
- BASE (a1 engine) = Qwen3-4B `grids15_sft139` LoRA-TTT — unchanged, proven.

**"3.8 Flash" = Qwen3.8-Flash-Next** (125B-A6B hybrid MoE, arch `qwen4_exp`, NVFP4 via NVIDIA): **cannot mount on the ARC-2 L4×4 + vLLM 0.19 pin** (arch not in pin; NVFP4 layout is the RTX Pro 6000 track). It belongs to **Track B (ARC-3)** — see §6. Do not attempt to stage it on ARC-2; that is how a slot dies.

---

## 3. Lever ledger — everything gathered, with receipts

| # | Lever | State | Receipt |
|---|---|---|---|
| L1 | shape-aware attempt_2 (T-A10/N6-lite) | **SHIPPED** (v37-exp, v39, v40+) | M1 replay a1-diff 0; drew 27.36 (floor) — non-negative by construction, keep |
| L2 | Proven Qwen3.8-27B leg forced | **SHIPPED** (v39 in rerun) | G4 boot receipt; score Oct-27 |
| L3 | Tool fill v1 (dihedral×cmap) | **PARKED** (ARC_V39_TOOLFILL=0) | train 11/11 transfer P=1.000; **eval 0/120** |
| L4 | Tool fill v2 WIDENED (+shift, +tile, +kron, ×d8×cmap) | **CLOSED for eval** | train 17 fired, 16/17 P=0.941 (11 d8/2 shift/3 kron/1 tile); **eval 0/120** — ARC-AGI-2 eval is closed to unique-exact single/composite-rule families this deep. Kept inline, one flag from arming if a future widening ever fires |
| L5 | v34-A second-sample refill (same effort) | **SHIPPED** (in core) | existing machinery, receipts in leg results |
| L6 | **Low-effort council refill (v40's lever)** | **STAGED** | refill jobs become no-think fast-pass jobs (per-job `template_kwargs reasoning_effort=low`, the v32d-receipted pattern): ~10× cheaper per answer → many more distinct-a2 candidates in the leftover window; merge picks first ≠ a1 from ≤3 cands (T-02-lite). Kill switch `ARC_V40_COUNCIL=0` → byte-identical v34 refill |
| L7 | failed-in-aimo upstream sync (working DFS verified programs) | PARKED | upstream koushikrudra head has the working `torch.multiprocessing.spawn`; needs its own commit + gate day — only if a slot is expendable (Oct 29 candidate) |
| L8 | Gemma4-26B LEG probe | PARKED | needs user's one browser consent click; NOT on the 3.8-locked path — only if 3.8 leg receipts disappoint |
| L9 | a1-duplicate re-answer / late fast-pass (v33) | SHIPPED (core) | receipts in leg results |
| L10 | Advice-text prompts | **BANNED** (全线禁用) | campaign iron rule |

**Honest tool-lane conclusion (do not re-litigate without new evidence):** the eval set has zero tasks solvable by a unique exact rule across 8 dihedral × color-perm × shift × tile × kron — the dataset was built to defeat exactly this class. The LLM leg + selection ensemble is where the points are; the tool lane stays as free insurance only.

---

## 4. Day-by-day runbook (Oct 27 → Nov 2)

### Oct 27 (v40) — low-effort council refill + double band call
1. `morning_score_watch.py` → v39 (57662636) + v37-exp (57630786) band calls.
   - v39 ≥ 31: council lever ships as planned; family hot.
   - v39 in band (27.4–31): ship as planned.
   - v39 < 27.4 (second consecutive sub-floor): note serving audit in the submission description; still ship v40 per directive (it is the audit baseline: proven leg + one bounded lever).
2. Push pre-staged **v40** (`scripts/build_v40.py` already gated): deltas = header (cell 0), refill-fp delta (cell 30, ~2 lines), receipts (cell 36). Everything else byte-identical to v39.
3. Gate (G1/G2/G4/G5 incl. boot-model = repacked-v1) → submit → score Oct-28 morning.
4. Evening: read v40 commit receipts (`leg27b_results.json`: refill job count, tok/s, exact hits) → decide v41.

### Oct 28 (v41) — branch on receipts
- If the leftover window still idles after low-effort refills: ONE lever = widen refill eligibility (route_budget +1 tier) or raise samples on undecoded tier — pick ONE, replay-argued.
- If refill saturated (no idle window): pure band draw on the best-receipted config (v40 core, flag state per receipts).
- Evening: START Track B staging IF pursuing §6 (CPU-only work, never touches ARC-2 quota).

### Oct 29 (v42) — last high-risk slot
- Candidate: L7 DFS-sync behind its own commit gate (only if staged + replay-clean by Oct-28 night). Otherwise: best-of draw.
- Track B kill rule fires here (see §6).

### Oct 30 (v43) — final pre-freeze draw
- Highest-EV config by the week's receipts. No new levers. Freeze discipline begins.

### Oct 31 — FREEZE
- No code changes. Verify the best-of leaderboard state; confirm which two submissions the finals picks will be.

### Nov 1–2 — FINALS
- **F1 = best paired-receipt submission** (highest scored).
- **F2 = most robust** (best floor behavior: proven family, fewest levers armed).
- Final submission Nov 2 from dasshovon.

---

## 5. The 40+ honesty box (read before dreaming)

- ARC-2: 40+ = **+7.4 over PB** ≈ 6 band-sigmas. No receipt, no mechanism, no model on the L4×4 pin supports a step of that size in 5 days. Silver cement (33.89, = PB +1.25) is the real ARC-2 target and is reachable: best-of over 4 more draws (~+0.5–1.0 in expectation) + one council/lever landing (+0.5–2).
- **The only honest 40+ door is the ARC-3 track** (gold 38.20 at rank 19/4702 — a shallower pool): Flash-Next NVFP4 + cp313 wheelhouse + Duck harness. It has separate slots. This is a parallel bet, never an ARC-2 slot substitute.

---

## 6. Track B — ARC-3 Flash-Next lane (bounded parallel bet)

- **Step 0 (Oct 27, 30 min):** verify the ARC-3 competition deadline + slot availability via API before investing anything.
- **Oct 27–28:** cp313 wheelhouse Docker probe (CPU) + `pin_compat_probe` on a Flash-Next NVFP4 snapshot + find a mountable Kaggle model/dataset mirror. All CPU-side; zero ARC-2 quota.
- **Oct 28–29:** single-GPU-class smoke (boot + 1-token gen). NVFP4 125B-A6B + n-gram embeddings on the ARC-3 hardware spec.
- **Kill rule:** no boot receipt by Oct-29 EOD → abandon Track B, fold everything into ARC-2 best-of. **Never let Track B touch an ARC-2 commit or slot.**
- Why bounded: 2 unproven stack layers (wheelhouse + NVFP4 boot) in 3 days is low-probability; but the downside is only CPU hours, and the upside is the only 40+ door that exists.

---

## 7. Risks & standing rules

| Risk | Mitigation |
|---|---|
| Third consecutive floor draw | Serving audit (D5) documented in submission description; v40 config IS the audit baseline |
| Commit session failure | Gate battery G1/G2/G4/G5 before any submit; fail-closed |
| Quota overdraft blocks commit | Receipted non-blocking for competition commits; probe with a push, never assume |
| ACL slug quirk | `status_v39_once.py`-style coordinate auto-locate; coords written to `oct2?_work/v??_coords.json` |
| Sandbox resets | Env restore one-liner (`pip --break-system-packages requests kagglesdk`); all scripts persisted under `scripts/` |
| New lever temptation mid-week | One-lever doctrine: ONE receipted lever per submission, kill-switched, byte-identity gates on all untouched cells |
| Tokens | Never in notebook plaintext; GitHub copies sanitized (grep-verified) |

## 8. One-command map (tomorrow morning)

```
python3.13 scripts/morning_score_watch.py        # band calls: v39 + v37-exp
python3.13 scripts/build_v40.py                  # already gated; only if not pre-built
python3.13 scripts/push_v40.py                   # push + commit (~1h50m)
python3.13 scripts/status_v40_once.py            # locate coords (ACL quirk)
python3.13 scripts/gate_v40.py                   # after commit completes
python3.13 scripts/submit_v40.py                 # slot-check -> gate -> submit
```
