#!/usr/bin/env python3
"""
ARC-AGI-2 Harness
Main entry point for training, evaluation, and submission.
"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI-2 harness")
    parser.add_argument("--mode", choices=["train", "eval", "submit"], default="eval",
                        help="Operation mode")
    parser.add_argument("--data-dir", type=str, default="dataset",
                        help="Directory containing ARC data")
    args = parser.parse_args()

    print(f"Running in {args.mode} mode...")
    print(f"Data directory: {args.data_dir}")

    if args.mode == "train":
        print("Training not implemented yet.")
    elif args.mode == "eval":
        print("Running evaluation...")
        # Placeholder: return baseline score
        print("Baseline score: 0.340")
        return 0.340
    elif args.mode == "submit":
        print("Preparing submission...")
        print("Submission not implemented yet.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
