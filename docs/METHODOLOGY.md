# ARC-AGI-2 Methodology

## Task Overview

ARC-AGI-2 presents grid transformation tasks where the goal is to predict the output grid given input-output example pairs. Each task has 1-5 training examples and 1 test input.

## Approach

### 1. Rule-Based Solvers
Each solver targets a specific task family:

| Solver | Task Family | Logic |
|--------|-------------|-------|
| ColorCount | Counting colored objects | Count + apply operation |
| MirrorH/V | Horizontal/vertical symmetry | Reflect grid |
| Rotate90/180/270 | Rotation tasks | Rotate by N*90 |
| CopyRegion | Copy a region | Extract + place |
| FillPattern | Fill missing cells | Interpolate pattern |

### 2. RL Agent
- State: task features (colors, dimensions, symmetry scores)
- Action: choose solver + hyperparameters
- Reward: 1.0 if correct, 0.0 otherwise
- Training: REINFORCE on training set tasks

### 3. LLM Fallback
For tasks unsolved by rules + RL:
- Convert grid to ASCII art
- Few-shot prompt with training examples
- Parse output into grid format

### 4. Ensemble
Multiple solvers vote; confidence = number of agreeing solvers.

## Score Calculation
Score = solved_tasks / total_tasks
