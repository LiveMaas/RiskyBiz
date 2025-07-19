import pandas as pd
import sys
from pathlib import Path

SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

SEVERITY_MAP = {
    5: 'Critical',
    4: 'High',
    3: 'Medium',
    2: 'Low',
    1: 'Info'
}

def parse_qualys_csv(input_path):
    df = pd.read_csv(input_path)
    df['id'] = ['qualys-{}'.format(i+1) for i in range(len(df))]
    df['asset'] = df['IP']
    df['vuln_id'] = df['QID']
    df['severity'] = df['SEVERITY'].apply(lambda x: SEVERITY_MAP.get(int(x), 'Unknown'))
    df['description'] = df['QID']
    df['scanner'] = 'qualys'
    df['business_unit'] = None  # To be mapped later
    df['status'] = 'open'
    df['discovered_date'] = df['FIRST_FOUND']
    return df[SCHEMA].to_dict(orient='records')

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/qualys/latest.csv')
    findings = parse_qualys_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 