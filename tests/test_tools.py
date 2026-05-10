"""
Unit tests for each tool.
Tests show interviewers you understand code quality and reliability.
Run with: python -m pytest tests/ -v
"""

import pytest
import os
from agent.tools.file_reader import read_transactions
from agent.tools.calculator import categorize_transactions, compute_totals
from agent.tools.flagging import flag_transactions


# ── Fixtures (reusable test data) ─────────────────────────────────────
@pytest.fixture
def sample_transactions():
    return [
        {'date': '2024-01-01', 'description': 'Netflix subscription', 'amount': 15.99, 'merchant': 'Netflix'},
        {'date': '2024-01-02', 'description': 'Team lunch', 'amount': 120.00, 'merchant': 'Restaurant'},
        {'date': '2024-01-03', 'description': 'AWS cloud bill', 'amount': 2500.00, 'merchant': 'Amazon Web Services'},
        {'date': '2024-01-04', 'description': 'Office supplies', 'amount': 45.00, 'merchant': 'Staples'},
        {'date': '2024-01-05', 'description': 'Flight to NYC', 'amount': 850.00, 'merchant': 'Delta Airlines'},
    ]


@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV file for testing."""
    csv_content = """date,description,amount,merchant
2024-01-01,Netflix subscription,15.99,Netflix
2024-01-02,Team lunch,120.00,Restaurant
2024-01-03,AWS cloud bill,2500.00,Amazon Web Services
"""
    csv_file = tmp_path / "test_transactions.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


# ── File Reader Tests ──────────────────────────────────────────────────
class TestFileReader:
    def test_reads_valid_csv(self, sample_csv):
        result = read_transactions(sample_csv)
        assert len(result) == 3
        assert result[0]['description'] == 'Netflix subscription'
        assert result[0]['amount'] == 15.99

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            read_transactions("nonexistent_file.csv")

    def test_raises_on_unsupported_format(self, tmp_path):
        bad_file = tmp_path / "data.xlsx"
        bad_file.write_text("some content")
        with pytest.raises(ValueError, match="Unsupported file format"):
            read_transactions(str(bad_file))

    def test_amounts_are_floats(self, sample_csv):
        result = read_transactions(sample_csv)
        for t in result:
            assert isinstance(t['amount'], float)


# ── Calculator Tests ───────────────────────────────────────────────────
class TestCalculator:
    def test_categorizes_netflix_as_subscription(self, sample_transactions):
        result = categorize_transactions(sample_transactions)
        assert 'Software & Subscriptions' in result
        assert any('Netflix' in t['merchant'] for t in result['Software & Subscriptions'])

    def test_categorizes_aws_as_cloud(self, sample_transactions):
        result = categorize_transactions(sample_transactions)
        assert 'Cloud & Infrastructure' in result

    def test_totals_are_correct(self, sample_transactions):
        categorized = categorize_transactions(sample_transactions)
        totals = compute_totals(categorized)
        expected_grand_total = sum(t['amount'] for t in sample_transactions)
        assert totals['_GRAND_TOTAL'] == round(expected_grand_total, 2)

    def test_percentages_sum_to_100(self, sample_transactions):
        categorized = categorize_transactions(sample_transactions)
        totals = compute_totals(categorized)
        totals.pop('_GRAND_TOTAL')
        total_pct = sum(v['percentage'] for v in totals.values())
        assert abs(total_pct - 100.0) < 0.5


# ── Flagging Tests ─────────────────────────────────────────────────────
class TestFlagging:
    def test_flags_high_value_transaction(self, sample_transactions):
        categorized = categorize_transactions(sample_transactions)
        totals = compute_totals(categorized)
        flagged = flag_transactions(sample_transactions, totals)
        flagged_amounts = [f['amount'] for f in flagged]
        assert 2500.00 in flagged_amounts
        assert 850.00 in flagged_amounts

    def test_small_transactions_not_flagged(self, sample_transactions):
        categorized = categorize_transactions(sample_transactions)
        totals = compute_totals(categorized)
        flagged = flag_transactions(sample_transactions, totals)
        flagged_amounts = [f['amount'] for f in flagged]
        assert 15.99 not in flagged_amounts

    def test_flag_has_reason(self, sample_transactions):
        categorized = categorize_transactions(sample_transactions)
        totals = compute_totals(categorized)
        flagged = flag_transactions(sample_transactions, totals)
        for f in flagged:
            assert 'flags' in f
            assert len(f['flags']) > 0