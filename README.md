# RiskyBiz Vulnerability Risk Aggregator

## Overview
RiskyBiz is a Python application that ingests vulnerability scan data from multiple sources (Wiz, Tenable.sc, and Qualys), normalizes and correlates the findings, maps them to business units, and outputs a risk-based score (0-100) for each business unit. The app generates a summary table, a bar chart, and a PDF report for easy review and sharing.

## Features
- Parses CSV exports from Wiz, Tenable.sc, and Qualys
- Normalizes findings to a unified schema
- Maps assets to business units using CIDR ranges
- Aggregates and deduplicates findings
- Calculates a risk score (0-100) per business unit
- Outputs a summary table, bar chart, and PDF report

## Setup
1. **Install Python 3.8+**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Prepare your data:**
   - Place the latest CSV exports from each scanner in:
     - `data/wiz/latest.csv`
     - `data/tenable/latest.csv`
     - `data/qualys/latest.csv`
   - Update `config/biz_unit_mapping.yaml` with your business unit CIDR mappings.
   - (Optional) Adjust `config/schema.yaml` if your scanner export formats change.

## Running the App
From the project root, run:
```sh
python main.py
```
This will:
- Parse and normalize all scanner data
- Map findings to business units
- Aggregate and score risk by business unit
- Print a summary table to the terminal
- Generate a bar chart (`reports/risk_by_biz_unit.png`)
- Generate a PDF report (`reports/output_pdfs/risk_report.pdf`)

## Output
- **Terminal:** Summary table of risk scores and finding counts by business unit
- **PNG:** Bar chart of risk scores by business unit
- **PDF:** Report with chart and summary table for sharing

## Troubleshooting
- Ensure all dependencies are installed (`pip install -r requirements.txt`)
- If you see errors about missing modules, install them as shown above
- If your CSV formats change, update the schema in `config/schema.yaml`
- For path issues, ensure you run from the project root and your data/config files are in the correct locations

## Extending
- Add new scanners by creating a new parser in `scripts/`
- Update the schema and mapping logic as needed

---
For questions or support, contact your RiskyBiz admin or developer.
