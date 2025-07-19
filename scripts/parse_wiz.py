import pandas as pd
import sys
from pathlib import Path

# Normalized schema fields
SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

def parse_wiz_csv(input_path):
    df = pd.read_csv(input_path)
    df['id'] = ['wiz-{}'.format(i+1) for i in range(len(df))]
    df['asset'] = df['ipAddress']
    df['vuln_id'] = df['vulnTitle']
    df['severity'] = df['severityLevel']
    df['description'] = df['vulnTitle']
    df['scanner'] = 'wiz'
    df['business_unit'] = df['tags']
    df['status'] = 'open'
    df['discovered_date'] = df['detectedAt']
    return df[SCHEMA].to_dict(orient='records')

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/wiz/latest.csv')
    findings = parse_wiz_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 