"""
Entry point for the Financial Expense Agent.
Run this file to process your transactions.

Usage:
    python main.py                             # uses default sample data
    python main.py data/my_transactions.csv   # uses your own file
    python main.py data/transactions.csv --no-save  # prints only, no file saved
"""

import sys
import argparse
from agent.agent import run_agent


def main():
    parser = argparse.ArgumentParser(
        description="Financial Expense Agent — Categorizes and summarizes transactions"
    )
    parser.add_argument(
        'filepath',
        nargs='?',
        default='data/sample_transactions.csv',
        help='Path to your CSV or TXT transaction file (default: data/sample_transactions.csv)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Print report only, do not save to file'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Directory to save report (default: output/)'
    )
    
    args = parser.parse_args()
    output_dir = None if args.no_save else args.output_dir
    
    run_agent(args.filepath, output_dir)


if __name__ == "__main__":
    main()