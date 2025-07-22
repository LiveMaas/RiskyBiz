import json
from pathlib import Path
from scripts.parse_wiz import parse_wiz_csv
from scripts.parse_tenable import parse_tenable_csv
from scripts.parse_qualys import parse_qualys_csv
from scripts.normalize import load_schema, normalize_findings
from scripts.mapping import load_biz_unit_mapping, map_findings_to_biz_unit
from scripts.aggregate import aggregate_findings
import pandas as pd

def main():
    base = Path(__file__).parent
    # Parse raw data
    wiz_findings = parse_wiz_csv(base / 'data/wiz/latest.csv')
    tenable_findings = parse_tenable_csv(base / 'data/tenable/latest.csv')
    qualys_findings = parse_qualys_csv(base / 'data/qualys/latest.csv')
    # Normalize
    schema = load_schema(base / 'config/schema.yaml')
    wiz_norm = normalize_findings(wiz_findings, 'wiz', schema)
    tenable_norm = normalize_findings(tenable_findings, 'tenable', schema)
    qualys_norm = normalize_findings(qualys_findings, 'qualys', schema)
    # Combine all findings
    all_findings = wiz_norm + tenable_norm + qualys_norm
    # Map business units
    biz_map = load_biz_unit_mapping(base / 'config/biz_unit_mapping.yaml')
    mapped_findings = map_findings_to_biz_unit(all_findings, biz_map)
    # Aggregate and score
    agg = aggregate_findings(mapped_findings)
    # Print summary table
    print("\nRisk Scores by Business Unit:")
    summary = [(unit, data['score'], len(data['findings'])) for unit, data in agg.items()]
    df = pd.DataFrame(summary, columns=['Business Unit', 'Risk Score', 'Finding Count'])
    print(df.to_string(index=False))

if __name__ == '__main__':
    main() 