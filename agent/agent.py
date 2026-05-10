"""
Main Agent — The Agentic Loop

This is the orchestrator. It does NOT do any work itself.
It calls tools in the right order and assembles the final report.

This is the "agent" pattern: a coordinator that delegates to specialized tools.
"""

import os
from datetime import datetime
from typing import Optional

from agent.tools.file_reader import read_transactions
from agent.tools.calculator import categorize_transactions, compute_totals
from agent.tools.flagging import flag_transactions


def run_agent(input_filepath: str, output_dir: Optional[str] = "output") -> str:
    """
    Main agentic loop. Orchestrates all tools in a single pass.
    """
    print("\n" + "="*60)
    print("  💼 FINANCIAL EXPENSE AGENT — STARTING")
    print("="*60 + "\n")
    
    # ── STEP 1: File Reader Tool ──────────────────────────────────
    print("📂 STEP 1: Reading transaction file...")
    transactions = read_transactions(input_filepath)
    
    if not transactions:
        return "❌ No transactions found. Please check your input file."
    
    # ── STEP 2: Categorize & Calculate ───────────────────────────
    print("\n🧮 STEP 2: Categorizing and computing totals...")
    categorized = categorize_transactions(transactions)
    totals = compute_totals(categorized)
    
    # ── STEP 3: Flagging Tool ─────────────────────────────────────
    print("\n🚩 STEP 3: Flagging unusual transactions...")
    flagged = flag_transactions(transactions, totals)
    
    # ── STEP 4: Generate Report ───────────────────────────────────
    print("\n📝 STEP 4: Generating expense report...\n")
    report = _generate_report(transactions, categorized, totals, flagged)
    
    # ── STEP 5: Save or Print ─────────────────────────────────────
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(output_dir, f"expense_report_{timestamp}.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {report_path}")
    
    print(report)
    return report


def _generate_report(transactions, categorized, totals, flagged) -> str:
    """Assembles the final structured expense report."""
    
    grand_total = totals.pop('_GRAND_TOTAL', 0)
    lines = []
    
    # ── Header ────────────────────────────────────────────────────
    lines.append("=" * 60)
    lines.append("         EXPENSE SUMMARY REPORT")
    lines.append(f"         Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}")
    lines.append("=" * 60)
    lines.append(f"  Total Transactions : {len(transactions)}")
    lines.append(f"  Grand Total        : ${grand_total:>10,.2f}")
    lines.append(f"  Flagged Items      : {len(flagged)}")
    lines.append("=" * 60)
    
    # ── Category Breakdown ────────────────────────────────────────
    lines.append("\n📊 SPENDING BY CATEGORY")
    lines.append("-" * 60)
    lines.append(f"  {'Category':<30} {'Total':>10}  {'Txns':>4}  {'% Budget':>8}")
    lines.append(f"  {'-'*30} {'-'*10}  {'-'*4}  {'-'*8}")
    
    sorted_categories = sorted(
        totals.items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    for category, stats in sorted_categories:
        bar = "█" * int(stats['percentage'] / 5)
        lines.append(
            f"  {category:<30} ${stats['total']:>9,.2f}  "
            f"{stats['count']:>4}  {stats['percentage']:>6.1f}%  {bar}"
        )
    
    lines.append(f"\n  {'TOTAL':<30} ${grand_total:>9,.2f}")
    
    # ── Transaction Details Per Category ─────────────────────────
    lines.append("\n\n📋 TRANSACTION DETAILS")
    lines.append("-" * 60)
    
    for category, stats in sorted_categories:
        lines.append(f"\n  [{category}]  Total: ${stats['total']:,.2f}  |  "
                     f"Avg: ${stats['average']:,.2f}")
        
        cat_transactions = sorted(
            categorized.get(category, []),
            key=lambda x: x['amount'],
            reverse=True
        )
        
        for t in cat_transactions:
            lines.append(f"    {t['date']}  {t['description']:<35} ${t['amount']:>9,.2f}")
    
    # ── Flagged Transactions ──────────────────────────────────────
    lines.append("\n\n🚩 FLAGGED TRANSACTIONS")
    lines.append("-" * 60)
    
    if flagged:
        for t in flagged:
            lines.append(f"\n  ⚠️  {t['date']} | {t['merchant']} | ${t['amount']:,.2f}")
            lines.append(f"     Description: {t['description']}")
            for flag in t['flags']:
                lines.append(f"     → {flag}")
    else:
        lines.append("  ✅ No unusual transactions detected.")
    
    # ── Footer ────────────────────────────────────────────────────
    lines.append("\n" + "=" * 60)
    lines.append("  END OF REPORT")
    lines.append("=" * 60 + "\n")
    
    return "\n".join(lines)