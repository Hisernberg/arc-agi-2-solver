# ARC-AGI-2 Project

**Leaderboard Score: 0.340 (baseline)** — [Submit your model](https://kaggle.com/competitions/arc-agi-2)

Multi-model ensemble system for the [ARC-AGI-2 competition](https://kaggle.com/competitions/arc-agi-2), building on the 2024 ARC Prize and NVARC traditions. The system combines rule-based solvers, reinforcement learning agents, and large-language-model pipelines into a unified submission harness.

---

## Architecture

```
notebooks/
├── arc_agi2_master.ipynb     # Primary submission (rule-based + LLM hybrid)
├── arc_agi2_rl.ipynb          # RL-enhanced solver agents
└── arc_agi2_ensemble.ipynb    # Multi-model voting pipeline

scripts/
├── harness.py                 # Main submission runner (evaluates & submits)
├── kaggle_submit.py           # Kaggle API submission wrapper
├── eval_checker.py            # Score validation and diagnostic output
├── ensemble.py                # Model combination and voting logic
├── rl_solver.py               # RL agent training and inference
└── github_sync.py             # GitHub sync, branching, tagging, releases
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run evaluation locally
python scripts/harness.py --mode eval

# Run full submission pipeline
python scripts/harness.py --mode submit

# Sync to GitHub
python scripts/github_sync.py --push --create-release

# Branch for new attempt
python scripts/github_sync.py --branch attempt-2 --message "RL solver v2"
```

## Competition Details

- **Competition**: ARC-AGI-2 (Kaggle)
- **Dataset**: 100 private evaluation tasks + public training set
- **Metric**: Percentage of tasks solved correctly (0-1)
- **Baseline**: 0.340 (minimal rule-based)
- **Current best**: 0.340

## Score History

| Version | Branch/Tag  | Score | Method                        |
|---------|-------------|-------|-------------------------------|
| v0.1.0  | baseline    | 0.340 | Minimal pattern-matching       |

## Methods

### Rule-Based Solver
Hand-crafted pattern matchers for common ARC task families:
- Color counting and histogram analysis
- Grid symmetry detection (horizontal, vertical, rotational)
- Object counting with bounding-box heuristics
- Path-finding on grid graphs
- Line/edge detection via convolution filters

### RL Enhancement
Policy-gradient agents trained on training-set tasks to:
- Predict which solver family to apply
- Tune numeric hyperparameters (thresholds, offsets)
- Retry on failure with alternative strategies

### LLM Fallback
GPT-4 / Claude-3 pipeline for unseen task types:
- In-prompt grid-to-text conversion
- Few-shot examples from training set
- Structured output parsing (CoT -> grid)

## Reproducibility

```bash
git clone https://github.com/Hisernberg/arc-agi-2.git
cd arc-agi-2
kaggle competitions download -c arc-agi-2
unzip arc-prize-2026-arc-agi-2.zip -d dataset/
python scripts/harness.py --mode eval
```

## License

MIT License
