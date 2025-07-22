import pandas as pd
from collections import defaultdict
import sys
from pathlib import Path

def risk_score(severity_counts):
    # Example: weighted score (Critical=5, High=4, Medium=3, Low=2, Info=1)
    weights = {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'Info': 1}
    total = sum(severity_counts.values())
    if total == 0:
        return 0
    score = sum(weights.get(sev, 0) * count for sev, count in severity_counts.items())
    max_score = total * 5
    return int((score / max_score) * 100)

def aggregate_findings(findings):
    df = pd.DataFrame(findings)
    # Deduplicate by asset and vuln_id
    df = df.drop_duplicates(subset=['asset', 'vuln_id'])
    grouped = defaultdict(lambda: {'score': 0, 'findings': []})
    for biz_unit, group in df.groupby('business_unit'):
        sev_counts = group['severity'].value_counts().to_dict()
        score = risk_score(sev_counts)
        grouped[biz_unit]['score'] = score
        grouped[biz_unit]['findings'] = group.to_dict(orient='records')
    return grouped

def main():
    # Example usage: python aggregate.py findings.json
    import json
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            findings = json.load(f)
    else:
        findings = []
    result = aggregate_findings(findings)
    import pprint
    pprint.pprint(result)

if __name__ == '__main__':
    main() 