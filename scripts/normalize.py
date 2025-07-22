import pandas as pd
import yaml
from pathlib import Path
import sys

def load_schema(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def normalize_findings(findings, scanner, schema):
    df = pd.DataFrame(findings)
    mapping = schema.get(scanner, {})
    rename_dict = {src: dst for src, dst in mapping.items()}
    df = df.rename(columns=rename_dict)
    return df.to_dict(orient='records')

def main():
    # Example usage: python normalize.py scanner_name findings.json
    import json
    config_path = str(Path(__file__).parent.parent / 'config/schema.yaml')
    schema = load_schema(config_path)
    if len(sys.argv) > 2:
        scanner = sys.argv[1]
        with open(sys.argv[2], 'r') as f:
            findings = json.load(f)
    else:
        scanner = 'wiz'
        findings = []
    normalized = normalize_findings(findings, scanner, schema)
    for finding in normalized:
        print(finding)

if __name__ == '__main__':
    main() 