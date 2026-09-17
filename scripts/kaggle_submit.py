#!/usr/bin/env python3
"""
Kaggle Submission Manager for ARC-AGI-2
Handles: auth setup, notebook submission, status check, leaderboard, download
"""
import os, json, sys, time, subprocess, hashlib, argparse
from pathlib import Path

KAGGLE_TOKEN = os.environ.get("KGAT_TOKEN", "YOUR_KAGGLE_TOKEN")
COMPETITION = "arc-prize-2026-arc-agi-2"
BASE_DIR = r"C:\Users\pc\OneDrive\Desktop\arc-agi-2"
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
NOTEBOOK_DIR = os.path.join(BASE_DIR, "notebooks")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "submission_history")


def ensure_kaggle_creds():
    """Write kaggle.json credentials so `kaggle competitions` CLI works."""
    cfg = Path.home() / ".kaggle" / "kaggle.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({"username": "hermes", "key": KAGGLE_TOKEN}))
    cfg.chmod(0o600)
    return cfg


def install_kaggle():
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kaggle"], capture_output=True)


def submit_notebook(nb_path=None, message=None):
    """
    Submit a notebook to the competition.
    For Kaggle code competitions, submit via the API.
    """
    ensure_kaggle_creds()
    install_kaggle()

    if nb_path is None:
        nb_path = os.path.join(NOTEBOOK_DIR, "arc_agi2_advanced.ipynb")

    msg = message or f"ARC-AGI-2 submission {time.strftime('%Y-%m-%d %H:%M')}"
    print(f"Submitting: {nb_path}")
    print(f"Message: {msg}")

    result = subprocess.run(
        ["kaggle", "competitions", "submit", COMPETITION, "-f", nb_path, "-m", msg],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return None
    return result.stdout


def check_status():
    """List recent submissions."""
    ensure_kaggle_creds()
    install_kaggle()
    result = subprocess.run(
        ["kaggle", "competitions", "submissions", COMPETITION],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.stdout


def get_leaderboard(page=1):
    ensure_kaggle_creds()
    install_kaggle()
    result = subprocess.run(
        ["kaggle", "competitions", "leaderboard", COMPETITION, "--show-scores", "-p", str(page)],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.stdout


def download_data(out_dir=None):
    """Download competition data files."""
    ensure_kaggle_creds()
    install_kaggle()
    if out_dir is None:
        out_dir = DATASET_DIR
    os.makedirs(out_dir, exist_ok=True)
    result = subprocess.run(
        ["kaggle", "competitions", "download", "-p", out_dir, COMPETITION],
        capture_output=True, text=True
    )
    print(result.stdout[-500:] if result.stdout else result.stderr[-500:])
    return out_dir


def validate_submission_json(path):
    """Validate submission.json schema."""
    with open(path) as f:
        data = json.load(f)

    errors = []
    for tid, entries in data.items():
        if not isinstance(entries, list):
            errors.append(f"{tid}: entries must be a list")
            continue
        for i, entry in enumerate(entries):
            for a in ["attempt_1", "attempt_2"]:
                if a not in entry:
                    errors.append(f"{tid}[{i}]: missing {a}")
                    continue
                arr = entry[a]
                ok = (isinstance(arr, list) and len(arr) > 0 and
                      all(isinstance(r, list) and len(r) == len(arr[0])
                          for r in arr) and
                      all(isinstance(c, int) and 0 <= c <= 9
                          for row in arr for c in row))
                if not ok:
                    errors.append(f"{tid}[{i}].{a}: invalid grid format")

    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for e in errors[:20]:
            print(f"  {e}")
        return False

    total_out = sum(len(v) for v in data.values())
    print(f"Valid: {len(data)} tasks, {total_out} outputs, SHA={hashlib.sha256(open(path,'rb').read()).hexdigest()[:12]}")
    return True


def score_on_eval(submission_path, eval_challenges=None, eval_solutions=None):
    """Score a submission against the evaluation set."""
    if eval_challenges is None:
        eval_challenges = os.path.join(DATASET_DIR, "arc-agi_evaluation_challenges.json")
    if eval_solutions is None:
        eval_solutions = os.path.join(DATASET_DIR, "arc-agi_evaluation_solutions.json")

    with open(eval_challenges) as f:
        challenges = json.load(f)
    with open(eval_solutions) as f:
        solutions = json.load(f)
    with open(submission_path) as f:
        sub = json.load(f)

    total, correct = 0, 0
    details = []
    for tid in challenges:
        gt_list = solutions.get(tid, [])
        pred_list = sub.get(tid, [])
        task_score = 0
        for i, gt in enumerate(gt_list):
            pred = pred_list[i] if i < len(pred_list) else {}
            p1 = pred.get("attempt_1", [])
            p2 = pred.get("attempt_2", [])
            if p1 == gt or p2 == gt:
                task_score += 1
                details.append((tid, i, "CORRECT"))
            else:
                details.append((tid, i, "WRONG"))
        total += len(gt_list)
        correct += task_score

    score = correct / total if total > 0 else 0
    print(f"\n{'='*60}")
    print(f"EVALUATION SET SCORE: {score:.4f}  ({correct}/{total})")
    print(f"{'='*60}")

    # Save result
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    result = {
        "timestamp": ts,
        "score": score,
        "correct": correct,
        "total": total,
        "submission_file": os.path.basename(submission_path),
        "sha256": hashlib.sha256(open(submission_path, "rb").read()).hexdigest()[:12],
    }
    result_file = os.path.join(RESULTS_DIR, f"eval_{ts}.json")
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)

    # Update latest
    with open(os.path.join(RESULTS_DIR, "latest.json"), "w") as f:
        json.dump(result, f, indent=2)

    # Print correct/wrong details
    wrong = [(tid, i, d) for tid, i, d in details if d == "WRONG"]
    print(f"\nWRONG ({len(wrong)}):")
    for tid, i, _ in wrong[:10]:
        print(f"  {tid}[{i}]")
    if len(wrong) > 10:
        print(f"  ... and {len(wrong)-10} more")

    return score, details


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("submit", help="Submit notebook to Kaggle")
    sub.add_parser("status", help="Check submission status")
    sub.add_parser("leaderboard", help="View leaderboard")
    sub.add_parser("download", help="Download competition data")
    sub.add_parser("init", help="Setup Kaggle credentials")
    
    validate_p = sub.add_parser("validate", help="Validate submission.json")
    validate_p.add_argument("--submission", required=True)

    score_p = sub.add_parser("score-eval", help="Score submission on eval set")
    score_p.add_argument("--submission", required=True)

    args = p.parse_args()

    if args.cmd == "init":
        ensure_kaggle_creds()
        install_kaggle()
        print("Kaggle CLI ready!")
    elif args.cmd == "submit":
        submit_notebook()
    elif args.cmd == "status":
        check_status()
    elif args.cmd == "leaderboard":
        get_leaderboard()
    elif args.cmd == "download":
        download_data()
    elif args.cmd == "validate":
        validate_submission_json(args.submission)
    elif args.cmd == "score-eval":
        score_on_eval(args.submission)
