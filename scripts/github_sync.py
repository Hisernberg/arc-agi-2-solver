#!/usr/bin/env python3
"""
GitHub Sync Manager for ARC-AGI-2
Auto-commits, branches, releases, score tagging
GitHub Token: YOUR_GITHUB_TOKEN
"""
import os, json, sys, subprocess, hashlib, shutil, time
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
REPO_NAME = "arc-agi-2-solver"
GIT_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "repo")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gh_api(method, endpoint, data=None):
    """Raw GitHub API call via curl."""
    url = f"https://api.github.com/repos/pc/{REPO_NAME}/{endpoint}"
    cmd = ["curl", "-s", "-X", method,
           "-H", f"Authorization: token {GITHUB_TOKEN}",
           "-H", "Accept: application/vnd.github.v3+json",
           "-H", "Content-Type: application/json",
           url]
    if data:
        cmd += ["-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"raw": result.stdout[:200]}


def init_repo():
    """Create repo if not exists, init local git."""
    # Check if repo exists
    resp = gh_api("GET", "")
    if "id" in resp:
        print(f"Repo already exists: {REPO_NAME}")
    else:
        gh_api("POST", "repos", {
            "name": REPO_NAME,
            "description": "ARC-AGI-2 Competition Solver — Advanced abstract reasoning with NVARC",
            "private": False,
            "has_issues": True,
            "has_wiki": False,
        })
        print(f"Created repo: {REPO_NAME}")
    
    # Init local git
    os.makedirs(GIT_BASE, exist_ok=True)
    subprocess.run(["git", "config", "--global", "user.email", "hermes@agent.local"], 
                   cwd=GIT_BASE, capture_output=True)
    subprocess.run(["git", "config", "--global", "user.name", "Hermes Agent"],
                   cwd=GIT_BASE, capture_output=True)
    
    if not os.path.exists(os.path.join(GIT_BASE, ".git")):
        subprocess.run(["git", "init"], cwd=GIT_BASE, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin",
             f"https://x-access-token:{GITHUB_TOKEN}@github.com/pc/{REPO_NAME}.git"],
            cwd=GIT_BASE, capture_output=True
        )
    
    # Copy files to repo
    _sync_files_to_repo()
    
    # Initial commit
    subprocess.run(["git", "add", "."], cwd=GIT_BASE, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "Initial commit: ARC-AGI-2 project setup"],
        cwd=GIT_BASE, capture_output=True
    )
    if result.returncode == 0:
        subprocess.run(["git", "push", "-u", "origin", "main"],
                       cwd=GIT_BASE, capture_output=True,
                       env={**os.environ, "GITHUB_TOKEN": GITHUB_TOKEN})
        print("Initial push done!")
    
    return True


def _sync_files_to_repo():
    """Copy all project files to the git repo directory."""
    notebooks_src = os.path.join(BASE_DIR, "notebooks")
    scripts_src = os.path.join(BASE_DIR, "scripts")
    docs_src = os.path.join(BASE_DIR, "docs")
    results_src = os.path.join(BASE_DIR, "results")
    
    for src, dst_name in [(notebooks_src, "notebooks"), (scripts_src, "scripts"),
                          (docs_src, "docs"), (results_src, "results")]:
        dst = os.path.join(GIT_BASE, dst_name)
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # Create/update README
    readme = f"""# ARC-AGI-2 Solver

## Competition
[ARC Prize 2026 - ARC-AGI-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2)
$700,000 in prizes | Abstract reasoning | Novel tasks

## Approach
**NVARC+ Enhanced** — Based on the ARC Prize 2025 winner (NVARC: qwen3_4b_grids15_sft139 + per-task LoRA).
Enhanced with multi-grid tokenizer, RL verification layer, ensemble scoring, and adaptive deep search.

## Architecture
- Base Model: Qwen3-4B (BF16) — `qwen3_4b_grids15_sft139`
- Per-task LoRA fine-tuning (r=256, 1 epoch, 128 augmented seqs)
- Turbo DFS decoding (GPU-efficient, 12 ARC tokens)
- Multi-worker: 4 × L4 GPU, cheap-first task ordering
- Phase 1: Primary pass + Phase 2: Adaptive deep search
- Scoring: score_kgmon = vote_count − mean(augmented_NLL)

## Pipeline
```
Dataset → Grid Tokenizer → Qwen3-4B (LoRA) → Turbo DFS → Candidate Scorer → submission.json
```

## Score History
| Date | Score | Notes |
|------|-------|-------|
| {datetime.now().strftime('%Y-%m-%d')} | TBD | Baseline submission |

## Files
- `notebooks/arc_agi2_advanced.ipynb` — Main submission notebook
- `scripts/kaggle_submit.py` — Submission manager
- `scripts/eval_checker.py` — Local evaluation
- `docs/PLAN.md` — Strategy plan
- `docs/METHODOLOGY.md` — Technical approach

## Reproducing
1. Download competition data via `python scripts/kaggle_submit.py download`
2. Open `notebooks/arc_agi2_advanced.ipynb` on Kaggle
3. Commit → Submit

## License
MIT
"""
    with open(os.path.join(GIT_BASE, "README.md"), "w") as f:
        f.write(readme)


def commit(message=None, files=None):
    """Stage, commit, and push changes."""
    if files:
        for f in files:
            subprocess.run(["git", "add", f], cwd=GIT_BASE, capture_output=True)
    else:
        subprocess.run(["git", "add", "."], cwd=GIT_BASE, capture_output=True)
    
    msg = message or f"Auto-sync {datetime.now().isoformat()}"
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=GIT_BASE, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Committed: {msg[:80]}")
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=GIT_BASE, capture_output=True,
            env={**os.environ, "GITHUB_TOKEN": GITHUB_TOKEN}
        )
        print("Pushed!")
    else:
        print(f"Nothing to commit or error: {result.stderr[:200]}")
    return result.returncode == 0


def tag_and_release(tag, score=None, notes=""):
    """Create a git tag and GitHub release."""
    # Tag local
    subprocess.run(["git", "tag", "-a", tag, "-m", f"Score: {score} | {notes}"],
                   cwd=GIT_BASE, capture_output=True)
    
    body = f"## ARC-AGI-2 Submission\n\n"
    if score is not None:
        body += f"**Score: {score:.4f}**\n\n"
    body += f"Generated: {datetime.now().isoformat()}\n\n{notes}"
    
    gh_api("POST", "releases", {
        "tag_name": tag,
        "name": f"Score {score:.4f}" if score else tag,
        "body": body,
    })
    
    # Push tag
    subprocess.run(["git", "push", "origin", tag],
                   cwd=GIT_BASE, capture_output=True,
                   env={**os.environ, "GITHUB_TOKEN": GITHUB_TOKEN})
    print(f"Release created: {tag}")


def save_score(score, submission_file=None):
    """Save a score to the history file."""
    results_dir = os.path.join(GIT_BASE, "results", "submission_history")
    os.makedirs(results_dir, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "submission_file": submission_file,
        "sha256": hashlib.sha256(open(submission_file, "rb").read()).hexdigest()[:12] if submission_file and os.path.exists(submission_file) else None,
    }
    
    history_file = os.path.join(results_dir, "scores.json")
    history = json.load(open(history_file)) if os.path.exists(history_file) else []
    history.append(entry)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)
    
    return entry


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_sync.py [init|sync|commit|tag|save-score]")
    else:
        cmd = sys.argv[1]
        if cmd == "init":
            init_repo()
        elif cmd == "sync":
            _sync_files_to_repo()
            commit("Auto-sync")
        elif cmd == "commit":
            commit(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else None)
        elif cmd == "tag":
            if len(sys.argv) >= 3:
                tag_and_release(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None)
        elif cmd == "save-score":
            if len(sys.argv) >= 3:
                save_score(float(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None)
