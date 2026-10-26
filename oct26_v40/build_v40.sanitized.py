#!/usr/bin/env python3
"""Build v40 = v39 (proven Qwen3.8-27B leg FORCED, ref 57662636 in rerun) + ONE lever:
LOW-EFFORT COUNCIL REFILL (ARC_V40_COUNCIL=1) — v34-A refill jobs run as no-think
low-effort fast-pass answers (per-job template_kwargs override, the v32d-receipted
path): ~10x cheaper per answer => the leftover window covers many more distinct
attempt_2 candidates; merge still picks first != attempt_1 from <=3 (T-02-lite).
Kill switch ARC_V40_COUNCIL=0 -> byte-identical v34 refill behaviour.
Tool lane stays PARKED inline (receipts v1+v2: train 17/17-class, eval 0/120 -> closed).
Deltas: cell 0 header, cell 30 refill-fp line, cell 36 receipts. All else byte-identical."""
import json, ast, hashlib

SRC = "/home/z/my-project/arc/oct26_work/arc26-nvarc-v39.ipynb"
DST = "/home/z/my-project/arc/oct26_work/arc26-nvarc-v40.ipynb"

nb = json.load(open(SRC))
assert len(nb["cells"]) == 37

# ---------------- cell 0: header ----------------
new_header = """# ARC26 NVARC v40 — 3.8 leg locked + low-effort council refill (built Oct 26 eve; Oct-27 slot)

Core = **v34b cells 1-35 byte-identical lineage** + shape-a2 (ref 57630786 -> 27.36 floor
draw, non-negative by construction) + **proven Qwen3.8-27B FP8 leg FORCED** (user directive:
`ARC_V38_LEG_SWAP=0`, boot-receipted in v39 ref 57662636; Tufa glob inert). ONE new lever:

1. **LOW-EFFORT COUNCIL REFILL** (`ARC_V40_COUNCIL=1`): v34-A second-sample refill jobs run
   as no-think `reasoning_effort=low` fast-pass answers (per-job override, v32d-receipted
   path) instead of a second xhigh pass. No-think answers are ~10x cheaper, so the leftover
   window after the main queue drains covers MANY more tasks with a distinct reasoning mode;
   answers flow through the same multi-cand path (merge picks first != attempt_1 from <=3,
   v33 T-02-lite). Kill switch `ARC_V40_COUNCIL=0` -> byte-identical v34 refill.

Tool lane PARKED inline (receipts Oct-26, full local sweep, v1+v2 spaces dihedral x cmap x
shift x tile x kron: train 17 fired / 16-17 transfer P~0.94; **eval 0/120 fired** — ARC-AGI-2
eval is closed to unique-exact rule families this deep; zero EV, one flag from arming).
Plan: download/ARC26_Gold_Push_Plan_Oct26_v1.md. One-lever discipline (D5) enforced."""
assert nb["cells"][0]["cell_type"] == "markdown"
nb["cells"][0]["source"] = new_header.splitlines(keepends=True)

# ---------------- cell 30: council refill delta ----------------
src30 = "".join(nb["cells"][30]["source"])
OLD = "jobs.append((_t34, _v34_kref, False))"
assert src30.count(OLD) == 1, f"council hook count = {src30.count(OLD)}"
NEW = """# v40 COUNCIL (ARC_V40_COUNCIL=1): refill jobs run as no-think low-effort fast-pass
                                # answers (per-job template_kwargs override, v32d-receipted path);
                                # ~10x cheaper per answer -> the leftover window covers many more
                                # distinct attempt_2 candidates; merge still picks first != a1 of <=3.
                                jobs.append((_t34, _v34_kref, os.environ.get("ARC_V40_COUNCIL", "1") == "1"))"""
src30_new = src30.replace(OLD, NEW)
assert src30_new.count("ARC_V40_COUNCIL") == 2  # comment + code line
assert src30_new.count('os.environ.get("ARC_V40_COUNCIL", "1")') == 1
nb["cells"][30]["source"] = src30_new.splitlines(keepends=True)
print("cell 30: council refill delta applied (ARC_V40_COUNCIL=1 default)")

# ---------------- cell 36: v40 receipts ----------------
cell36_src = '''# === V40 RECEIPTS + RATCHET CHECKLIST (instrumentation, no score effect) ===
import json, os, hashlib, time

try:
    OUT = "/kaggle/working"
    sub_path = os.path.join(OUT, "submission.json")
    rerun = os.environ.get("KAGGLE_IS_COMPETITION_RERUN", "0") == "1"
    _boot_model = None
    try:
        _lr = json.load(open(os.path.join(OUT, "leg27b_results.json")))
        _ups = [e for e in _lr.get("summary", {}).get("ladder", []) if e.get("status") == "up"]
        if _ups:
            _boot_model = _ups[-1].get("glob")
    except Exception as _e36:
        _boot_model = f"unreadable: {type(_e36).__name__}"
    _council_recs = 0
    try:
        _lr40 = json.load(open(os.path.join(OUT, "leg27b_results.json")))
        _council_recs = sum(1 for _r40 in (_lr40.get("recs") or []) if _r40.get("sample", 0) >= 1000)
    except Exception:
        pass
    rec = {
        "version": "v40",
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": ("v34b cells 1-35 lineage + shape-aware attempt_2 (T-A10) + PROVEN "
                       "qwen3-8-27b-fp8-repacked-v1 leg FORCED (user directive Oct-26; booted in "
                       "v39 ref 57662636) + LOW-EFFORT COUNCIL REFILL (v34-A refill jobs as "
                       "no-think fast-pass; tool lane PARKED: eval 0/120 in v1+v2 spaces)"),
        "levers": [
            {"name": "shape_aware_attempt_2", "flag": "ARC_V37_SHAPE_A2",
             "value": os.environ.get("ARC_V37_SHAPE_A2", "1"),
             "receipt": "M1 replay a1 diff 0; ref 57630786 drew 27.36 (floor, in-band)"},
            {"name": "leg_model_ladder", "flag": "ARC_V38_LEG_SWAP",
             "value": os.environ.get("ARC_V38_LEG_SWAP", "0"),
             "receipt": "FORCED 0 (user directive): proven repacked-v1 only; Tufa glob inert"},
            {"name": "verified_tool_degenerate_fill", "flag": "ARC_V39_TOOLFILL",
             "value": os.environ.get("ARC_V39_TOOLFILL", "0"),
             "receipt": "PARKED: v1+v2 widened spaces, train 17 fired P~0.94, eval 0/120 -> closed"},
            {"name": "low_effort_council_refill", "flag": "ARC_V40_COUNCIL",
             "value": os.environ.get("ARC_V40_COUNCIL", "1"),
             "receipt": "v34-A refill jobs as no-think low-effort fast-pass; kill switch =0 -> "
                        "byte-identical v34 refill", "council_samples": _council_recs},
        ],
        "leg_boot_model": _boot_model,
        "rerun_mode": rerun,
        "submission_present": os.path.exists(sub_path),
    }
    if os.path.exists(sub_path):
        with open(sub_path, "rb") as f:
            raw = f.read()
        rec["submission_sha256_16"] = hashlib.sha256(raw).hexdigest()[:16]
        try:
            rec["submission_keys"] = len(json.loads(raw))
        except Exception as e:
            rec["submission_keys"] = f"UNPARSEABLE: {e}"
    with open(os.path.join(OUT, "v40_receipts.json"), "w") as f:
        json.dump(rec, f, indent=1)
    print("[v40] receipts written:", json.dumps(rec)[:400])
    if not rerun:
        assert os.path.exists(sub_path), "submission.json missing in commit output"
        assert isinstance(rec.get("submission_keys"), int) and rec["submission_keys"] >= 120, rec.get("submission_keys")
        print("[v40] RATCHET CHECKLIST: ALL PASS (commit mode)")
except Exception as e:
    if os.environ.get("KAGGLE_IS_COMPETITION_RERUN", "0") == "1":
        print(f"[v40] instrumentation fail-open (rerun safety): {type(e).__name__}: {e}")
    else:
        raise
'''
assert "".join(nb["cells"][36]["source"]).startswith("# === V39 RECEIPTS")
nb["cells"][36] = {"cell_type": "code", "execution_count": None, "metadata": {},
                   "outputs": [], "source": cell36_src.splitlines(keepends=True)}
print("cell 36 receipts updated (v40_receipts.json)")

# ---------------- gates ----------------
src_nb = json.load(open(SRC))
unchanged = list(range(1, 30)) + [31] + list(range(33, 36))
for i in unchanged:
    assert "".join(nb["cells"][i]["source"]) == "".join(src_nb["cells"][i]["source"]), f"cell {i} drifted!"
print("byte-identity: cells 1-29, 31, 33-35 exact vs v39; deltas only 0/30/36")

for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    code = "".join(c["source"])
    code = "\n".join(l for l in code.splitlines()
                     if not l.strip().startswith("%%writefile") and not l.strip().startswith("!"))
    try:
        ast.parse(code)
    except SyntaxError as e:
        raise SystemExit(f"AST FAIL cell {i}: {e}")
print("ast gate: all code cells OK")

json.dump(nb, open(DST, "w"))
print("wrote", DST, "| cells:", len(nb["cells"]),
      "| sha:", hashlib.sha256(json.dumps(nb).encode()).hexdigest()[:16])
