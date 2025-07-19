import csv
import sys
from pathlib import Path

# Normalized schema fields
SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

def parse_wiz_csv(input_path):
    normalized = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            normalized.append({
                'id': f'wiz-{idx+1}',
                'asset': row['ipAddress'],
                'vuln_id': row['vulnTitle'],
                'severity': row['severityLevel'],
                'description': row['vulnTitle'],
                'scanner': 'wiz',
                'business_unit': row['tags'],
                'status': 'open',
                'discovered_date': row['detectedAt']
            })
    return normalized

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/wiz/latest.csv')
    findings = parse_wiz_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 