\# 💼 Financial Expense Agent



A Python-based AI agent that reads financial transaction data (CSV/TXT),

categorizes each transaction, computes spending totals per category, flags

high-value or unusual charges, and produces a structured expense summary report.



> \*\*Portfolio Project\*\* | Built to demonstrate agentic tool design, structured

> output, and the Single Responsibility Principle.



\---



\## 🎯 What This Agent Does

CSV File

↓

\[Tool 1: File Reader]  →  Parses and validates input

↓

\[Tool 2: Calculator]   →  Categorizes + computes totals \& averages

↓

\[Tool 3: Flagging]     →  Applies business rules to identify anomalies

↓

Expense Report (console + saved .txt file)

\## 🔑 Key Design Decisions



| Decision | Why |

|---|---|

| One tool per file | Single Responsibility Principle — each tool is independently testable |

| Rule-based categorization | No external API needed; transparent, auditable logic |

| Keyword matching | Explainable AI — you can see exactly why each decision was made |

| CLI arguments | Makes the tool reusable, not just a one-off script |



\## 🚀 Quick Start



```bash

\# 1. Clone the repo

git clone https://github.com/Lekshmiprabha/financial-expense-agent.git

cd financial-expense-agent



\# 2. Install dependencies

pip install -r requirements.txt



\# 3. Run the agent

python main.py



\# 4. Or use your own file

python main.py path/to/your/transactions.csv



\# 5. Run the tests

python -m pytest tests/ -v

```



\## 📊 Sample Output

============================================================

EXPENSE SUMMARY REPORT

Generated: January 21, 2024 10:30 AM

Total Transactions :  20

Grand Total        :  $11,773.52

Flagged Items      :   4

📊 SPENDING BY CATEGORY

Category                           Total  Txns  % Budget



Entertainment \& Client          $3,200.00     1    27.2%  █████

Cloud \& Infrastructure          $2,340.00     1    19.9%  ███

Travel \& Transport              $1,611.80     3    13.7%  ██

Food \& Dining                     $320.75     2     2.7%

...

🚩 FLAGGED TRANSACTIONS

⚠️  2024-01-17 | Four Seasons Hotel | $3,200.00

Description: Client entertainment

→ HIGH VALUE: $3,200.00 exceeds threshold of $500.00

⚠️  2024-01-06 | Amazon Web Services | $2,340.00

Description: AWS cloud services bill

→ HIGH VALUE: $2,340.00 exceeds threshold of $500.00



\## 🧪 Running Tests



```bash

python -m pytest tests/ -v

```



Expected output:

tests/test\_tools.py::TestFileReader::test\_reads\_valid\_csv          PASSED

tests/test\_tools.py::TestFileReader::test\_raises\_on\_missing\_file   PASSED

tests/test\_tools.py::TestFileReader::test\_raises\_on\_unsupported\_format PASSED

tests/test\_tools.py::TestFileReader::test\_amounts\_are\_floats       PASSED

tests/test\_tools.py::TestCalculator::test\_categorizes\_netflix\_as\_subscription PASSED

tests/test\_tools.py::TestCalculator::test\_categorizes\_aws\_as\_cloud PASSED

tests/test\_tools.py::TestCalculator::test\_totals\_are\_correct       PASSED

tests/test\_tools.py::TestCalculator::test\_percentages\_sum\_to\_100   PASSED

tests/test\_tools.py::TestFlagging::test\_flags\_high\_value\_transaction PASSED

tests/test\_tools.py::TestFlagging::test\_small\_transactions\_not\_flagged PASSED

tests/test\_tools.py::TestFlagging::test\_flag\_has\_reason            PASSED



\## 📁 Project Structure

financial-expense-agent/

├── agent/

│   ├── init.py

│   ├── agent.py            # Orchestrator — the agentic loop

│   └── tools/

│       ├── init.py

│       ├── file\_reader.py  # Tool 1: Parse CSV/TXT input

│       ├── calculator.py   # Tool 2: Categorize + compute totals

│       └── flagging.py     # Tool 3: Rule-based anomaly detection

├── data/

│   └── sample\_transactions.csv

├── output/                 # Generated reports saved here

├── tests/

│   └── test\_tools.py

├── main.py                 # Entry point

├── requirements.txt

├── .env.example

└── README.md



\## 💡 Skills Demonstrated



\- \*\*Agentic Design\*\* — Orchestrator pattern with delegated tools

\- \*\*Tool Definition\*\* — Each tool has a single, well-defined contract

\- \*\*Structured Output\*\* — Consistent, formatted report generation

\- \*\*Error Handling\*\* — Graceful handling of bad input data

\- \*\*Unit Testing\*\* — pytest coverage across all three tools

\- \*\*CLI Design\*\* — argparse for flexible usage



\## 🛠️ Tech Stack



\- \*\*Language\*\* — Python 3.x

\- \*\*Testing\*\* — pytest

\- \*\*Input Formats\*\* — CSV, plain text

\- \*\*Output\*\* — Console + .txt report file



\## 🔮 Future Improvements



\- Add LLM categorization for transactions that don't match any rules

\- Export reports to PDF or Excel

\- Add a web interface using Flask or Streamlit

\- Connect to bank APIs for live transaction data



