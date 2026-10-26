#!/usr/bin/env python3
"""v40 tool-fill receipts v2 — WIDENED rule space (local ground truth, arc/data).

v1 space: dihedral(8) x injective color-perm                (receipt: train 11/11, eval 0/120)
v2 adds:  shift(dy,dx) zero-fill x cmap  (bbox-aligned candidates)
          tile(a,b) whole-grid repeat  x d8 x cmap
          kron(k,m) block upscale      x cmap
A rule FIRES only when it reproduces ALL train pairs EXACTLY; rules dedupe by their
prediction over the test input(s); task is UNIQUE-RULE when exactly one distinct
prediction exists. Receipts decide what v40 arms."""
import json, time

DATA = "/home/z/my-project/arc/data"

def _idn(g): return [row[:] for row in g]
def _r90(g): return [list(r) for r in zip(*g[::-1])]
def _r180(g): return [r[::-1] for r in g[::-1]]
def _r270(g): return [list(r) for r in zip(*g)][::-1]
def _lr(g): return [r[::-1] for r in g]
def _ud(g): return [r[:] for r in g[::-1]]
def _tr(g): return [list(r) for r in zip(*g)]
def _atr(g): return [list(r) for r in zip(*_r180(g))]

def d8():
    probe = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    seen = {}
    for f in (_idn, _r90, _r180, _r270, _lr, _ud, _tr, _atr):
        seen[tuple(map(tuple, f(probe)))] = f
    assert len(seen) == 8
    return list(seen.values())

D8L = d8()
NAMES = ["id", "r90", "r180", "r270", "lr", "ud", "tr", "atr"]

def shape(g): return (len(g), len(g[0]) if g else 0)

def derive_cmap_t(T, pairs):
    """color-perm consistent across all pairs after transform T (shape-equal required)."""
    m = {}
    for din, dout in pairs:
        a = T(din)
        if len(a) != len(dout):
            return None
        for ra, rb in zip(a, dout):
            if len(ra) != len(rb):
                return None
            for x, y in zip(ra, rb):
                if x in m:
                    if m[x] != y:
                        return None
                elif y in m.values():
                    return None
                else:
                    m[x] = y
    return m

def bbox(g):
    pts = [(y, x) for y, row in enumerate(g) for x, v in enumerate(row) if v != 0]
    if not pts:
        return None
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

def make_shift(dy, dx):
    def T(g):
        h, w = len(g), len(g[0])
        return [[g[y - dy][x - dx] if 0 <= y - dy < h and 0 <= x - dx < w else 0
                 for x in range(w)] for y in range(h)]
    return T

def shift_candidates(pairs):
    """same (dy,dx) must align bboxes across all pairs."""
    cands = None
    for din, dout in pairs:
        if shape(din) != shape(dout):
            return []
        bi, bo = bbox(din), bbox(dout)
        if bi is None or bo is None:
            return []
        s = {(bo[0] - bi[0], bo[1] - bi[1]), (bo[2] - bi[2], bo[3] - bi[3])}
        cands = s if cands is None else (cands & s)
        if not cands:
            return []
    return sorted(cands)

def make_tile(a, b):
    def T(g):
        out = []
        for r in g * a:
            out.append(list(r) * b)
        return out
    return T

def make_kron2(k, m):
    def T(g):
        out = []
        for row in g:
            for _ in range(k):
                out.append([v for v in row for _ in range(m)])
        return out
    return T

def tile_params(pairs, d):
    """(a,b) whole-grid repeat or (k,m) block upscale, consistent shapes across pairs."""
    shapes = [shape(d(din)) for din, _ in pairs]
    outs = [shape(dout) for _, dout in pairs]
    params = set()
    ok = all(oh % sh == 0 and ow % sw == 0 for (sh, sw), (oh, ow) in zip(shapes, outs))
    if ok:
        a0, b0 = outs[0][0] // shapes[0][0], outs[0][1] // shapes[0][1]
        if all((oh // sh, ow // sw) == (a0, b0) for (sh, sw), (oh, ow) in zip(shapes, outs)):
            if (a0, b0) == (1, 1):
                pass  # shape-equal: v1 family covers
            elif all(v == a0 for v in (a0, b0)) or True:
                if 1 <= a0 <= 4 and 1 <= b0 <= 4:
                    if a0 == b0 and outs[0] != shapes[0]:
                        # ambiguous family: tile vs kron distinguished by verification
                        params.add(("tile", a0, b0))
                        params.add(("kron", a0, b0))
                    else:
                        params.add(("tile", a0, b0))
    return sorted(params)

def rules_for_task(task):
    pairs = [(p["input"], p["output"]) for p in task["train"]]
    tins = [t["input"] for t in task["test"]]
    preds = {}

    def add(T, family):
        cm = derive_cmap_t(T, pairs)
        if cm is None:
            return
        pred = tuple(tuple(tuple(cm.get(x, x) for x in row) for row in T(t)) for t in tins)
        preds.setdefault(pred, family)

    # v1: D8 x cmap
    for di, d in enumerate(D8L):
        add(d, f"d8:{NAMES[di]}")
    # v2: shift x cmap
    for (dy, dx) in shift_candidates(pairs):
        if (dy, dx) != (0, 0):
            add(make_shift(dy, dx), f"shift:{dy},{dx}")
    # v2: tile / kron x d8 x cmap
    for di, d in enumerate(D8L):
        for kind, a, b in tile_params(pairs, d):
            add(make_tile(a, b) if kind == "tile" else make_kron2(a, b),
                f"{kind}:{a},{b}x{NAMES[di]}")
    return preds

def main():
    t0 = time.time()
    tr = json.load(open(f"{DATA}/arc-agi_training_challenges.json"))
    sol = json.load(open(f"{DATA}/arc-agi_training_solutions.json"))
    ev = json.load(open(f"{DATA}/arc-agi_evaluation_challenges.json"))
    evs = json.load(open(f"{DATA}/arc-agi_evaluation_solutions.json"))

    fired = correct = multi = multi_any = 0
    census = {}
    for tid, task in tr.items():
        preds = rules_for_task(task)
        if not preds:
            continue
        want = tuple(tuple(r) for r in sol[tid][0])
        if len(preds) == 1:
            fired += 1
            p, fam = next(iter(preds.items()))
            key = fam.split(":")[0].split("x")[0]
            census[key] = census.get(key, 0) + 1
            if p == (want,):
                correct += 1
        else:
            multi += 1
            if any(p == (want,) for p in preds):
                multi_any += 1

    print("=" * 72)
    print("RECEIPT A — TRAIN, WIDENED space (1000 tasks)")
    print(f"  unique-rule fired : {fired}")
    print(f"  test CORRECT      : {correct}  -> P(transfer|fired) = {correct/max(fired,1):.3f}")
    print(f"  multi-rule tasks  : {multi} (oracle-pick would solve {multi_any})")
    print(f"  fired census      : {census}")

    ev_fired, ev_pairs, ev_ok = 0, 0, 0.0
    ev_ids = []
    for tid, task in ev.items():
        preds = rules_for_task(task)
        if len(preds) != 1:
            continue
        ev_fired += 1
        ev_ids.append(tid)
        want = [tuple(r) for r in evs[tid][0]]
        p = next(iter(preds))
        for j, wp in enumerate(want):
            ev_pairs += 1
            if p[j] == wp:
                ev_ok += 1.0
    print("=" * 72)
    print("RECEIPT B — EVAL firing set (120 tasks), WIDENED space")
    print(f"  unique-rule fired : {ev_fired} tasks / {ev_pairs} test pairs")
    print(f"  would-be a1 credit: {ev_ok:.1f}")
    print(f"  fired ids         : {ev_ids}")
    print("=" * 72)
    print(f"runtime: {time.time()-t0:.1f}s")

    out = {
        "space": "D8xCMap + shiftxCMap + tile/kron xD8xCMap",
        "train_fired": fired, "train_correct": correct,
        "train_transfer": round(correct / max(fired, 1), 4),
        "train_multi": multi, "census": census,
        "eval_fired": ev_fired, "eval_pairs": ev_pairs,
        "eval_would_credit": ev_ok, "eval_fired_ids": ev_ids,
    }
    json.dump(out, open("/home/z/my-project/arc/oct26_work/toolfill_receipts_v2.json", "w"), indent=1)
    print("receipts -> arc/oct26_work/toolfill_receipts_v2.json")

if __name__ == "__main__":
    main()
