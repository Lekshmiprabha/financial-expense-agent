"""
Tool 1: File Reader
Responsibility: Read and parse the CSV transaction file.
One tool, one job — this is the Single Responsibility Principle.
"""

import csv
import os
from typing import List, Dict


def read_transactions(filepath: str) -> List[Dict]:
    """
    Reads a CSV or plain-text file of financial transactions.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of transaction dictionaries
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Transaction file not found: {filepath}")
    
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext == '.csv':
        return _read_csv(filepath)
    elif file_ext == '.txt':
        return _read_plain_text(filepath)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Use .csv or .txt")


def _read_csv(filepath: str) -> List[Dict]:
    """Parse a CSV file into a list of transaction dicts."""
    transactions = []
    
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        required_columns = {'date', 'description', 'amount', 'merchant'}
        if not required_columns.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"CSV must contain columns: {required_columns}. "
                f"Found: {reader.fieldnames}"
            )
        
        for row_num, row in enumerate(reader, start=2):
            try:
                transactions.append({
                    'date': row['date'].strip(),
                    'description': row['description'].strip(),
                    'amount': float(row['amount']),
                    'merchant': row['merchant'].strip()
                })
            except ValueError:
                print(f"⚠️  Warning: Skipping row {row_num} — invalid amount: {row['amount']}")
    
    print(f"✅ File Reader: Loaded {len(transactions)} transactions from '{filepath}'")
    return transactions


def _read_plain_text(filepath: str) -> List[Dict]:
    """
    Parse a plain-text file.
    Expected format per line: DATE | DESCRIPTION | AMOUNT | MERCHANT
    Example: 2024-01-02 | Netflix subscription | 15.99 | Netflix
    """
    transactions = []
    
    with open(filepath, encoding='utf-8') as f:
        for row_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) != 4:
                print(f"⚠️  Warning: Skipping line {row_num} — expected 4 fields separated by '|'")
                continue
            
            try:
                transactions.append({
                    'date': parts[0],
                    'description': parts[1],
                    'amount': float(parts[2]),
                    'merchant': parts[3]
                })
            except ValueError:
                print(f"⚠️  Warning: Skipping line {row_num} — invalid amount: {parts[2]}")
    
    print(f"✅ File Reader: Loaded {len(transactions)} transactions from '{filepath}'")
    return transactions