"""
Tool 2: Calculator
Responsibility: All math operations — totals, averages, percentages.
No categorization logic lives here. Pure numbers only.
"""

from typing import List, Dict
from collections import defaultdict


def categorize_transactions(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Assigns each transaction to a category using keyword rules.
    """
    CATEGORY_RULES = {
        "Food & Dining": [
            "restaurant", "lunch", "dinner", "food", "starbucks",
            "coffee", "grille", "kitchen", "cafe", "pizza", "burger"
        ],
        "Travel & Transport": [
            "flight", "hotel", "uber", "lyft", "taxi", "airline",
            "marriott", "hilton", "parking", "delta", "united", "airways"
        ],
        "Software & Subscriptions": [
            "netflix", "spotify", "adobe", "software", "subscription",
            "license", "saas", "app", "zoom", "slack"
        ],
        "Cloud & Infrastructure": [
            "aws", "amazon web services", "google cloud", "azure",
            "cloud", "hosting", "server", "digitalocean"
        ],
        "Office & Supplies": [
            "office", "supplies", "staples", "fedex", "ups", "postage",
            "shipping", "printing", "stationery"
        ],
        "Utilities & Bills": [
            "electricity", "internet", "phone", "utility", "bill",
            "comcast", "at&t", "verizon", "power", "water", "gas"
        ],
        "Health & Wellness": [
            "pharmacy", "medical", "health", "gym", "fitness",
            "cvs", "walgreens", "doctor", "dental"
        ],
        "Events & Training": [
            "conference", "registration", "training", "workshop",
            "seminar", "eventbrite", "meetup", "course"
        ],
        "Entertainment & Client": [
            "entertainment", "client", "four seasons", "luxury",
            "team building", "hospitality"
        ],
        "Equipment & Hardware": [
            "laptop", "computer", "hardware", "monitor", "keyboard",
            "best buy", "accessories", "equipment", "device"
        ],
    }
    
    categorized = defaultdict(list)
    
    for transaction in transactions:
        search_text = (
            transaction['description'].lower() + " " +
            transaction['merchant'].lower()
        )
        
        assigned = False
        for category, keywords in CATEGORY_RULES.items():
            if any(keyword in search_text for keyword in keywords):
                categorized[category].append(transaction)
                assigned = True
                break
        
        if not assigned:
            categorized["Uncategorized"].append(transaction)
    
    return dict(categorized)


def compute_totals(categorized: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """
    Computes financial totals for each category.
    """
    category_totals = {}
    grand_total = 0.0
    
    for category, transactions in categorized.items():
        amounts = [t['amount'] for t in transactions]
        cat_total = sum(amounts)
        grand_total += cat_total
        
        category_totals[category] = {
            'total': round(cat_total, 2),
            'count': len(transactions),
            'average': round(cat_total / len(transactions), 2),
            'min': round(min(amounts), 2),
            'max': round(max(amounts), 2),
        }
    
    for category in category_totals:
        pct = (category_totals[category]['total'] / grand_total * 100) if grand_total > 0 else 0
        category_totals[category]['percentage'] = round(pct, 1)
    
    category_totals['_GRAND_TOTAL'] = round(grand_total, 2)
    
    print(f"✅ Calculator: Computed totals across {len(categorized)} categories. Grand total: ${grand_total:,.2f}")
    return category_totals