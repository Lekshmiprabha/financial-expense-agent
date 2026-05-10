"""
Tool 3: Flagging Tool
Responsibility: Identify unusual or high-value transactions.
Applies business rules — completely separate from math or file reading.
"""

from typing import List, Dict


# Business rule thresholds — easy to configure
HIGH_VALUE_THRESHOLD = 500.00       # Flag any single transaction above this
CATEGORY_SPIKE_MULTIPLIER = 2.0     # Flag if a transaction is 2x the category average
SUSPICIOUS_KEYWORDS = [
    "cash", "withdrawal", "atm", "wire transfer",
    "cryptocurrency", "crypto", "gift card"
]


def flag_transactions(
    transactions: List[Dict],
    category_totals: Dict[str, Dict]
) -> List[Dict]:
    """
    Applies rule-based flagging to identify unusual transactions.
    
    Rules applied:
    1. High-value: single transaction exceeds HIGH_VALUE_THRESHOLD
    2. Category spike: transaction is 2x above its category average
    3. Suspicious keywords: description contains known risk terms
    """
    flagged = []
    
    from agent.tools.calculator import categorize_transactions
    categorized = categorize_transactions(transactions)
    
    transaction_category_avg = {}
    for category, txns in categorized.items():
        if category == '_GRAND_TOTAL':
            continue
        avg = sum(t['amount'] for t in txns) / len(txns)
        for t in txns:
            transaction_category_avg[id(t)] = (category, avg)
    
    for transaction in transactions:
        reasons = []
        
        # Rule 1: High-value single transaction
        if transaction['amount'] >= HIGH_VALUE_THRESHOLD:
            reasons.append(
                f"HIGH VALUE: ${transaction['amount']:,.2f} exceeds threshold "
                f"of ${HIGH_VALUE_THRESHOLD:,.2f}"
            )
        
        # Rule 2: Spike above category average
        cat_info = transaction_category_avg.get(id(transaction))
        if cat_info:
            category_name, cat_avg = cat_info
            if cat_avg > 0 and transaction['amount'] >= (cat_avg * CATEGORY_SPIKE_MULTIPLIER):
                reasons.append(
                    f"CATEGORY SPIKE: ${transaction['amount']:,.2f} is "
                    f"{transaction['amount']/cat_avg:.1f}x the '{category_name}' "
                    f"category average of ${cat_avg:,.2f}"
                )
        
        # Rule 3: Suspicious keywords
        desc_lower = transaction['description'].lower()
        matched_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in desc_lower]
        if matched_keywords:
            reasons.append(
                f"SUSPICIOUS KEYWORD: Found '{', '.join(matched_keywords)}' "
                f"in description"
            )
        
        if reasons:
            flagged.append({
                **transaction,
                'flags': reasons
            })
    
    print(f"✅ Flagging Tool: Identified {len(flagged)} flagged transactions")
    return flagged