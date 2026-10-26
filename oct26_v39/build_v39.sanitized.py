#!/usr/bin/env python3
"""Build v39 = v38 (commit-gated, leg ladder receipt) with the Oct-26 user directive applied:
PROVEN Qwen3.8-27B FP8 leg FORCED (ARC_V38_LEG_SWAP default 1->0; Tufa glob inert) + the
verified-tool degenerate fill added to cell 20 but PARKED (ARC_V39_TOOLFILL default 0; local
receipts: train 11 fired / 11 transfer P=1.000, eval 0/120 fired -> zero EV today, one flag
from arming). Deltas: cell 0 header, cell 20 append, cell 30 one-token flip, cell 36 receipts.
All other cells byte-identical to arc26-nvarc-v38.ipynb."""
import json, ast, hashlib

SRC = "/home/z/my-project/arc/oct25_work/arc26-nvarc-v38.ipynb"
DST = "/home/z/my-project/arc/oct26_work/arc26-nvarc-v39.ipynb"

nb = json.load(open(SRC))
assert len(nb["cells"]) == 37

# ---------------- cell 0: header ----------------
new_header = """# ARC26 NVARC v39 — proven Qwen3.8-27B leg strike (built Oct 26 per user directive)

Core = **v34b cells 1-35 byte-identical lineage** (band 27.36-30.97 across 7 scored draws,
PB 32.64) + shape-aware attempt_2 (submitted ref 57630786) + TWO Oct-26 deltas:

1. **PROVEN LEG FORCED** (user directive: "use model qwen 3.8 27b for working and submit
   using that model for today"): `ARC_V38_LEG_SWAP` default 1 -> **0** — the Tufa Qwen3.6
   glob is INERT; the proven `qwen3-8-27b-fp8-repacked-v1` model source boots with the FULL
   original ladder (A2-007 rungs included) = byte-equivalent v32/v34b leg behaviour, the
   lowest-variance configuration this family has.
2. **Verified-tool degenerate fill — PARKED** (`ARC_V39_TOOLFILL=0`): dihedral(8) x
   color-permutation unique-exact-rule sweep, fires only on both-`[[0]]` lost entries.
   Local receipts (full 1,120-task sweep, arc/oct26_work/toolfill_receipts.json): train
   11/1000 fired, **11/11 transfer P=1.000** (4 color-only, 7 rotation-only); eval **0/120
   fired** -> zero EV today, one flag from arming. Tool lane widened Oct-27 (translation,
   tiling, object ops) with the same receipts framework.

One-lever discipline: no unvalidated lever is armed (D5). Receipts cell = v39_receipts.json."""
assert nb["cells"][0]["cell_type"] == "markdown"
nb["cells"][0]["source"] = new_header.splitlines(keepends=True)

# ---------------- cell 20: append tool-fill block (atlas block byte-identical) ----------------
old20 = "".join(nb["cells"][20]["source"])
assert old20.rstrip().endswith("traceback.print_exc()"), "cell 20 tail changed?"

TOOL_BLOCK = '''

# ---- v39 verified-tool degenerate fill (PARKED: ARC_V39_TOOLFILL default 0) ----
# Fires ONLY where BOTH attempts are still [[0]] (already-lost region; atlas had no coverage
# there) and ONLY on a UNIQUE exact rule: one distinct prediction in the dihedral(8) x
# color-permutation space reproducing ALL train pairs EXACTLY. Local receipts (Oct-26, full
# 1,120-task sweep): train 11/1000 fired, 11/11 transfer P=1.000; eval 0/120 fired.
try:
    if _os.environ.get("ARC_V39_TOOLFILL", "0") == "1":
        _ch = "/kaggle/input/competitions/arc-prize-2026-arc-agi-2/arc-agi_evaluation_challenges.json"
        _tf_tasks = _json.load(open(_ch))

        def _tf_id(g): return [row[:] for row in g]
        def _tf_r90(g): return [list(r) for r in zip(*g[::-1])]
        def _tf_r180(g): return [r[::-1] for r in g[::-1]]
        def _tf_r270(g): return [list(r) for r in zip(*g)][::-1]
        def _tf_lr(g): return [r[::-1] for r in g]
        def _tf_ud(g): return [r[:] for r in g[::-1]]
        def _tf_tr(g): return [list(r) for r in zip(*g)]
        def _tf_atr(g): return [list(r) for r in zip(*_tf_r180(g))]
        _D8 = [_tf_id, _tf_r90, _tf_r180, _tf_r270, _tf_lr, _tf_ud, _tf_tr, _tf_atr]

        def _tf_cmap(d, pairs):
            m = {}
            for din, dout in pairs:
                a = d(din)
                if len(a) != len(dout): return None
                for ra, rb in zip(a, dout):
                    if len(ra) != len(rb): return None
                    for x, y in zip(ra, rb):
                        if x in m:
                            if m[x] != y: return None
                        elif y in m.values(): return None
                        else: m[x] = y
            return m

        def _tf_preds(task):
            pairs = [(p["input"], p["output"]) for p in task["train"]]
            tins = [t["input"] for t in task["test"]]
            out = {}
            for d in _D8:
                m = _tf_cmap(d, pairs)
                if m is None: continue
                pred = tuple(tuple(tuple(m.get(x, x) for x in row) for row in d(t)) for t in tins)
                out.setdefault(pred, 1)
            return list(out)

        with open("submission.json") as _f:
            _sub = _json.load(_f)
        _tn = 0
        for _tid, _task in _tf_tasks.items():
            if _tid not in _sub: continue
            for _j, _e in enumerate(_sub[_tid]):
                if _e.get("attempt_1") != [[0]] or _e.get("attempt_2") != [[0]]:
                    continue
                _ps = _tf_preds(_task)
                if len(_ps) != 1 or _j >= len(_ps[0]): continue
                _grid = [list(r) for r in _ps[0][_j]]
                _e["attempt_1"] = [list(r) for r in _grid]
                _e["attempt_2"] = [list(r) for r in _grid]
                _tn += 1
        with open("submission.json", "w") as _f:
            _json.dump(_sub, _f)
        print(f"[v39] tool-fill applied to {_tn} outputs (unique-exact dihedral x cmap rules)")
    else:
        print("[v39] tool-fill PARKED (ARC_V39_TOOLFILL=0; receipts: 11/11 train transfer, 0/120 eval firing)")
except Exception:
    print("[v39] tool-fill failed (suppressed)")
    import traceback
    traceback.print_exc()
'''
nb["cells"][20]["source"] = (old20 + TOOL_BLOCK).splitlines(keepends=True)
assert "".join(nb["cells"][20]["source"]).startswith(old20), "cell 20 prefix must stay byte-identical"
print("cell 20: atlas block byte-identical + tool-fill block appended (PARKED)")

# ---------------- cell 30: LEG_SWAP default flip ----------------
src30 = "".join(nb["cells"][30]["source"])
FLIP_OLD = 'os.environ.get("ARC_V38_LEG_SWAP", "1")'
assert src30.count(FLIP_OLD) == 1, f"LEG_SWAP default count = {src30.count(FLIP_OLD)}"
nb["cells"][30]["source"] = src30.replace(
    FLIP_OLD, 'os.environ.get("ARC_V38_LEG_SWAP", "0")').splitlines(keepends=True)
print("cell 30: ARC_V38_LEG_SWAP default 1 -> 0 (proven Qwen3.8-27B leg forced)")

# ---------------- cell 36: v39 receipts ----------------
cell36_src = '''# === V39 RECEIPTS + RATCHET CHECKLIST (instrumentation, no score effect) ===
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
    rec = {
        "version": "v39",
        "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": ("v34b cells 1-35 lineage + shape-aware attempt_2 (T-A10, ref 57630786) + "
                       "PROVEN qwen3-8-27b-fp8-repacked-v1 leg (user directive Oct-26: LEG_SWAP "
                       "forced 0, Tufa glob inert) + verified-tool degenerate fill PARKED "
                       "(train 11/11 transfer P=1.000, eval 0/120 fired)"),
        "levers": [
            {"name": "shape_aware_attempt_2", "flag": "ARC_V37_SHAPE_A2",
             "value": os.environ.get("ARC_V37_SHAPE_A2", "1"),
             "receipt": "M1 replay: a1 diff 0, 0 flips on debug pools; submitted ref 57630786"},
            {"name": "leg_model_ladder", "flag": "ARC_V38_LEG_SWAP",
             "value": os.environ.get("ARC_V38_LEG_SWAP", "0"),
             "receipt": "FORCED 0: proven repacked-v1 glob only; full original ladder intact"},
            {"name": "verified_tool_degenerate_fill", "flag": "ARC_V39_TOOLFILL",
             "value": os.environ.get("ARC_V39_TOOLFILL", "0"),
             "receipt": "PARKED: dihedral(8)xCMap unique-exact sweep; train 11 fired 11 transfer "
                        "P=1.000 (4 color-only 7 rotation-only); eval 0/120 fired -> zero EV today"},
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
    with open(os.path.join(OUT, "v39_receipts.json"), "w") as f:
        json.dump(rec, f, indent=1)
    print("[v39] receipts written:", json.dumps(rec)[:400])
    if not rerun:
        assert os.path.exists(sub_path), "submission.json missing in commit output"
        assert isinstance(rec.get("submission_keys"), int) and rec["submission_keys"] >= 120, rec.get("submission_keys")
        print("[v39] RATCHET CHECKLIST: ALL PASS (commit mode)")
except Exception as e:
    if os.environ.get("KAGGLE_IS_COMPETITION_RERUN", "0") == "1":
        print(f"[v39] instrumentation fail-open (rerun safety): {type(e).__name__}: {e}")
    else:
        raise
'''
assert "".join(nb["cells"][36]["source"]).startswith("# === V38 RECEIPTS")
nb["cells"][36] = {"cell_type": "code", "execution_count": None, "metadata": {},
                   "outputs": [], "source": cell36_src.splitlines(keepends=True)}
print("cell 36 receipts updated (v39_receipts.json)")

# ---------------- gates ----------------
src_nb = json.load(open(SRC))
unchanged = list(range(1, 20)) + list(range(21, 30)) + [31] + list(range(33, 36))
for i in unchanged:
    assert "".join(nb["cells"][i]["source"]) == "".join(src_nb["cells"][i]["source"]), f"cell {i} drifted!"
assert "".join(nb["cells"][20]["source"]).startswith("".join(src_nb["cells"][20]["source"]))
assert src30 == "".join(src_nb["cells"][30]["source"])
print("byte-identity: cells 1-19, 21-29, 31, 33-35 exact; cell 20 append-only; deltas 0/20/30/36")

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
