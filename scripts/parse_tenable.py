import csv
import sys
from pathlib import Path

SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

def parse_tenable_csv(input_path):
    normalized = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            normalized.append({
                'id': f'tenable-{idx+1}',
                'asset': row['Host'],
                'vuln_id': row['Plugin Name'],
                'severity': row['Risk'],
                'description': row['Plugin Name'],
                'scanner': 'tenable',
                'business_unit': None,  # To be mapped later
                'status': 'open',
                'discovered_date': row['First Seen']
            })
    return normalized

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/tenable/latest.csv')
    findings = parse_tenable_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 