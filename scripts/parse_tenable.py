import pandas as pd
import sys
from pathlib import Path

SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

def parse_tenable_csv(input_path):
    df = pd.read_csv(input_path)
    df['id'] = ['tenable-{}'.format(i+1) for i in range(len(df))]
    df['asset'] = df['Host']
    df['vuln_id'] = df['Plugin Name']
    df['severity'] = df['Risk']
    df['description'] = df['Plugin Name']
    df['scanner'] = 'tenable'
    df['business_unit'] = None  # To be mapped later
    df['status'] = 'open'
    df['discovered_date'] = df['First Seen']
    return df[SCHEMA].to_dict(orient='records')

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/tenable/latest.csv')
    findings = parse_tenable_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 