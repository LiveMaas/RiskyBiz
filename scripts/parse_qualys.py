import csv
import sys
from pathlib import Path

SCHEMA = [
    'id', 'asset', 'vuln_id', 'severity', 'description', 'scanner', 'business_unit', 'status', 'discovered_date'
]

SEVERITY_MAP = {
    '5': 'Critical',
    '4': 'High',
    '3': 'Medium',
    '2': 'Low',
    '1': 'Info'
}

def parse_qualys_csv(input_path):
    normalized = []
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            sev = SEVERITY_MAP.get(str(row['SEVERITY']), 'Unknown')
            normalized.append({
                'id': f'qualys-{idx+1}',
                'asset': row['IP'],
                'vuln_id': row['QID'],
                'severity': sev,
                'description': row['QID'],
                'scanner': 'qualys',
                'business_unit': None,  # To be mapped later
                'status': 'open',
                'discovered_date': row['FIRST_FOUND']
            })
    return normalized

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'data/qualys/latest.csv')
    findings = parse_qualys_csv(input_path)
    for finding in findings:
        print(finding)

if __name__ == '__main__':
    main() 