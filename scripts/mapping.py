import pandas as pd
import yaml
import ipaddress
from pathlib import Path
import sys

def load_biz_unit_mapping(config_path):
    with open(config_path, 'r') as f:
        mapping = yaml.safe_load(f)
    # Remove empty lines and parse mapping
    return {k.strip(): v.strip() for k, v in mapping.items() if k and v}

def map_asset_to_biz_unit(asset_ip, mapping):
    try:
        ip = ipaddress.ip_address(asset_ip)
        for cidr, unit in mapping.items():
            if ip in ipaddress.ip_network(cidr):
                return unit
    except Exception:
        pass
    return None

def map_findings_to_biz_unit(findings, mapping):
    df = pd.DataFrame(findings)
    df['business_unit'] = df['asset'].apply(lambda ip: map_asset_to_biz_unit(ip, mapping))
    return df.to_dict(orient='records')

def main():
    # Example usage: python mapping.py findings.json
    import json
    config_path = str(Path(__file__).parent.parent / 'config/biz_unit_mapping.yaml')
    mapping = load_biz_unit_mapping(config_path)
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            findings = json.load(f)
    else:
        findings = []
    mapped = map_findings_to_biz_unit(findings, mapping)
    for finding in mapped:
        print(finding)

if __name__ == '__main__':
    main() 