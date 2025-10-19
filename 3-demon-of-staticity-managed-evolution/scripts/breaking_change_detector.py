"""
breaking_change_detector.py

A simple script to detect breaking changes between two data contract versions.
- A breaking change is defined as removing or renaming a field.
- Exits with status code 1 if a breaking change is found, 0 otherwise.

Usage:
python breaking_change_detector.py <path_to_old_contract> <path_to_new_contract>
"""
import sys
import yaml


def detect_breaking_changes(old_contract_path, new_contract_path):
    try:
        with open(old_contract_path, 'r') as f:
            old_contract = yaml.safe_load(f)
        with open(new_contract_path, 'r') as f:
            new_contract = yaml.safe_load(f)

        old_fields = set(old_contract['fields'].keys())
        new_fields = set(new_contract['fields'].keys())

        # A breaking change is when any field from the old contract is missing in the new one.
        missing_fields = old_fields - new_fields

        if missing_fields:
            print(
                f"🚨 Breaking change detected! The following fields are missing in the new contract: {', '.join(missing_fields)}")
            sys.exit(1)
        else:
            print("✅ No breaking changes detected. New fields may have been added, but none were removed.")
            sys.exit(0)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python breaking_change_detector.py <old_contract.yaml> <new_contract.yaml>")
        sys.exit(2)

    detect_breaking_changes(sys.argv[1], sys.argv[2])