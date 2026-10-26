#!/usr/bin/env python3
"""v39 tool-fill receipts (local ground truth, arc/data).

Tool space = 8 dihedral transforms x consistent color-permutation (derived per
task from train pairs, injective on observed colors). A rule FIRES only when it
reproduces ALL train pairs EXACTLY; rules are deduped by their prediction on
the test input(s) — a task is UNIQUE-RULE when exactly one distinct prediction
exists. Receipts:
  A) train: P(test correct | unique rule)  -> the honest transfer rate
  B) eval:  firing set size + exact would-be delta if those entries were
            both-[[0]] degenerate (the only region the v39 fill touches)
  C) rule composition census (rotation-only / color-only / composite)
"""
import json, sys, time

DATA = "/home/z/my-project/arc/data"

# ---------- 8 dihedral transforms (pure python, deduped on a probe) ----------
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
    assert len(seen) == 8, f"dihedral dedupe failed: {len(seen)}"
    return list(seen.values())

D8L = d8()
NAMES = ["id", "r90", "r180", "r270", "lr", "ud", "tr", "atr"]

def shape(g): return (len(g), len(g[0]) if g else 0)

def derive_cmap(d, pairs):
    cmap = {}
    for din, dout in pairs:
        a = d(din)
        if len(a) != len(dout):
            return None
        for ra, rb in zip(a, dout):
            if len(ra) != len(rb):
                return None
            for x, y in zip(ra, rb):
                if x in cmap:
                    if cmap[x] != y:
                        return None
                elif y in cmap.values():
                    return None
                else:
                    cmap[x] = y
    return cmap

def apply_rule(d, cmap, g):
    return [[cmap.get(x, x) for x in row] for row in d(g)]

def rules_for_task(task):
    pairs = [(p["input"], p["output"]) for p in task["train"]]
    tins = [t["input"] for t in task["test"]]
    preds = {}
    for di, d in enumerate(D8L):
        cm = derive_cmap(d, pairs)
        if cm is None:
            continue
        pred = tuple(tuple(tuple(r) for r in apply_rule(d, cm, tin)) for tin in tins)
        preds.setdefault(pred, (NAMES[di], cm))
    return preds

def census(rule):
    name, cm = rule
    geom = name != "id"
    colr = any(k != v for k, v in cm.items())
    if geom and colr: return "composite"
    if geom: return "rotation-only"
    if colr: return "color-only"
    return "identity"

def main():
    t0 = time.time()
    tr = json.load(open(f"{DATA}/arc-agi_training_challenges.json"))
    sol = json.load(open(f"{DATA}/arc-agi_training_solutions.json"))
    ev = json.load(open(f"{DATA}/arc-agi_evaluation_challenges.json"))
    evs = json.load(open(f"{DATA}/arc-agi_evaluation_solutions.json"))

    # ---------- train receipts ----------
    fired = correct = multi = multi_any_correct = 0
    comp_census = {}
    for tid, task in tr.items():
        preds = rules_for_task(task)
        if not preds:
            continue
        want = tuple(tuple(r) for r in sol[tid][0])
        if len(preds) == 1:
            fired += 1
            p, rule = next(iter(preds.items()))
            comp_census[census(rule)] = comp_census.get(census(rule), 0) + 1
            if p == (want,):
                correct += 1
        else:
            multi += 1
            if any(p == (want,) for p in preds):
                multi_any_correct += 1

    print("=" * 72)
    print("RECEIPT A — TRAIN transfer (1000 tasks)")
    print(f"  unique-rule fired : {fired}")
    print(f"  test CORRECT      : {correct}  -> P(transfer|fired) = {correct/max(fired,1):.3f}")
    print(f"  multi-rule tasks  : {multi} (oracle-pick would solve {multi_any_correct})")
    print(f"  fired-rule census : {comp_census}")

    # ---------- eval receipts ----------
    ev_fired, ev_pairs, ev_correct_a1, ev_correct_half = 0, 0, 0, 0.0
    fired_ids = []
    for tid, task in ev.items():
        preds = rules_for_task(task)
        if len(preds) != 1:
            continue
        ev_fired += 1
        fired_ids.append(tid)
        want = [tuple(r) for r in evs[tid][0]]
        p = next(iter(preds))[0]  # single distinct prediction across all test inputs? no: preds keyed by full tuple
        # recompute per-pair (rules_for_task keyed on the tuple over all test inputs)
        task_pred = next(iter(preds))
        for j, wp in enumerate(want):
            ev_pairs += 1
            if task_pred[j] == wp:
                ev_correct_a1 += 1
                ev_correct_half += 1.0
            # attempt_2 same prediction -> no extra credit beyond a1
    print("=" * 72)
    print("RECEIPT B — EVAL firing set (120 tasks)")
    print(f"  unique-rule fired : {ev_fired} tasks / {ev_pairs} test pairs")
    print(f"  would-be CORRECT (a1 credit): {ev_correct_a1} pairs = {ev_correct_half:.1f} task-credit")
    print(f"  fired ids: {fired_ids}")
    print("=" * 72)
    print(f"runtime: {time.time()-t0:.1f}s")

    # machine-readable for the build script
    out = {
        "train_fired": fired, "train_correct": correct,
        "train_transfer": round(correct / max(fired, 1), 4),
        "train_multi": multi, "census": comp_census,
        "eval_fired": ev_fired, "eval_pairs": ev_pairs,
        "eval_correct_pairs": ev_correct_a1,
        "eval_fired_ids": fired_ids,
    }
    json.dump(out, open("/home/z/my-project/arc/oct26_work/toolfill_receipts.json", "w"), indent=1)
    print("receipts -> arc/oct26_work/toolfill_receipts.json")

if __name__ == "__main__":
    main()
