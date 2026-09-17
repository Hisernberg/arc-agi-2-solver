#!/usr/bin/env python3
"""
Evaluation checker for ARC-AGI-2 predictions.
"""
import json
import numpy as np
from pathlib import Path

def load_arc_data(data_dir):
    """Load ARC challenges and solutions."""
    challenges_path = Path(data_dir) / "arc-agi_evaluation_challenges.json"
    solutions_path = Path(data_dir) / "arc-agi_evaluation_solutions.json"

    with open(challenges_path, 'r') as f:
        challenges = json.load(f)
    with open(solutions_path, 'r') as f:
        solutions = json.load(f)

    return challenges, solutions

def evaluate_predictions(pred_path, challenges, solutions):
    """Evaluate predictions against ground truth."""
    with open(pred_path, 'r') as f:
        predictions = json.load(f)

    correct = 0
    total = len(challenges)

    for task_id in challenges:
        if task_id not in predictions:
            continue
        pred = predictions[task_id]
        true = solutions.get(task_id, [])
        if not true:
            continue
        # Simple exact match (adjust as needed for ARC format)
        if pred == true[0]:  # Assuming first solution is correct
            correct += 1

    score = correct / total if total > 0 else 0.0
    return score, correct, total

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Check ARC-AGI-2 predictions")
    parser.add_argument("predictions", help="Path to predictions JSON file")
    parser.add_argument("--data-dir", default="dataset",
                        help="Directory containing ARC data")
    args = parser.parse_args()

    try:
        challenges, solutions = load_arc_data(args.data_dir)
        score, correct, total = evaluate_predictions(
            args.predictions, challenges, solutions)
        print(f"Evaluation results:")
        print(f"  Correct: {correct}/{total}")
        print(f"  Score: {score:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
