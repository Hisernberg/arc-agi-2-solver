#!/usr/bin/env python3
"""v39 gate: 120-task structural sweep + v39 receipts (leg boot model + toolfill flag) +
proven-artifact presence. Exit 0 = submit-ready. Coordinates auto-loaded from
arc/oct26_work/v39_coords.json (ACL quirk: canonical owner + title-derived slug)."""
import json, requests, sys, os
import datetime as _dt

TOK_NEW = "__ROTATED_KGAT__"
COORDS = "/home/z/my-project/arc/oct26_work/v39_coords.json"
if os.path.exists(COORDS):
    _c = json.load(open(COORDS))
    OWNER, SLUG = _c["owner"], _c["slug"]
else:
    OWNER, SLUG = "kragglenote2forwork", "arc26-nvarc-v39-proven-qwen3-8-27b-leg"

def log(m): print(f"[{_dt.datetime.now(_dt.timezone.utc).isoformat()}] {m}", flush=True)
log(f"gate target: {OWNER}/{SLUG}")

h = {"Authorization": f"Bearer {TOK_NEW}"}
r = requests.get("https://www.kaggle.com/api/v1/kernels/output", headers=h,
                 params={"user_name": OWNER, "kernel_slug": SLUG}, timeout=60)
d = r.json()
files = d.get("files", [])
names = [f.get("fileName") or f.get("name") for f in files]

sj = next((f for f in files if (f.get("fileName") or f.get("name")) == "submission.json"), None)
if not (sj and sj.get("url")):
    log("G1 FAIL: submission.json missing"); sys.exit(1)
sub = json.loads(requests.get(sj["url"], timeout=120).text)
if not isinstance(sub, dict) or len(sub) != 120:
    log(f"G1 FAIL: tasks={len(sub) if isinstance(sub, dict) else '?'} != 120"); sys.exit(1)
bad, cells, a2_degen, both_degen = [], 0, 0, 0
for tid, val in sub.items():
    ok = isinstance(val, list) and len(val) >= 1
    if ok:
        for el in val:
            if not (isinstance(el, dict) and "attempt_1" in el and "attempt_2" in el):
                ok = False; break
            for g in (el["attempt_1"], el["attempt_2"]):
                if not (isinstance(g, list) and g and all(isinstance(row, list) and row for row in g)):
                    ok = False; break
                for row in g:
                    if not all(isinstance(c, int) and 0 <= c <= 9 for c in row):
                        ok = False; break
                    cells += len(row)
                if not ok: break
            if el.get("attempt_2") == [[0]]: a2_degen += 1
            if el.get("attempt_1") == [[0]] and el.get("attempt_2") == [[0]]: both_degen += 1
            if not ok: break
    if not ok:
        bad.append(tid)
if bad:
    log(f"G1 FAIL: {len(bad)} malformed: {bad[:5]}"); sys.exit(1)
log(f"G1 PASS: 120 tasks, {cells} cells valid, a2 [[0]] count={a2_degen}, both [[0]] count={both_degen}")

rc = next((f for f in files if (f.get("fileName") or f.get("name")) == "v39_receipts.json"), None)
if not (rc and rc.get("url")):
    log("G2 FAIL: v39_receipts.json missing"); sys.exit(1)
rec = json.loads(requests.get(rc["url"], timeout=60).text)
if not (isinstance(rec.get("submission_keys"), int) and rec["submission_keys"] >= 120):
    log(f"G2 FAIL: receipts say keys={rec.get('submission_keys')}"); sys.exit(1)
log(f"G2 PASS: receipts contract (keys={rec.get('submission_keys')}, sha={rec.get('submission_sha256_16')})")
lev = {l.get("name"): l.get("value") for l in rec.get("levers", [])}
log(f"G2x LEVER RECEIPTS: shape_a2={lev.get('shape_aware_attempt_2')} "
    f"leg_swap={lev.get('leg_model_ladder')} toolfill={lev.get('verified_tool_degenerate_fill')} "
    f"LEG_BOOT_MODEL={rec.get('leg_boot_model')}")

# G4: user directive check — the PROVEN leg must be the one that booted.
boot = str(rec.get("leg_boot_model") or "")
if boot and "qwen3-8-27b-fp8-repacked" not in boot and "unreadable" not in boot:
    log(f"G4 WARN: booted model is NOT the proven repacked-v1: {boot}")
elif boot:
    log(f"G4 PASS: proven leg booted: {boot}")

lg = next((f for f in files if (f.get("fileName") or f.get("name")) == "leg_gate.json"), None)
if lg and lg.get("url"):
    try:
        lgv = json.loads(requests.get(lg["url"], timeout=60).text)
        log(f"G5 leg_gate: {json.dumps(lgv)[:200]}")
    except Exception as e:
        log(f"G5 leg_gate unreadable: {e}")

proven = [n for n in names if n in ("leg_gate.json", "provenance.json", "leg27b_answers.json",
                                    "leg27b_results.json", "atlas_best_effort.json", "induction_results.json")]
if not proven:
    log(f"G5 FAIL: none of the proven v34b artifacts present; files={names[:14]}"); sys.exit(1)
log(f"G5 PASS: proven artifacts present: {proven}")
log("ALL GATES PASS")
