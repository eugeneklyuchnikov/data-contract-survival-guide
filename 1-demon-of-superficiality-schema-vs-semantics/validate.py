"""
validate.py

A script to demonstrate the difference between basic schema validation and
deeper semantic contract validation.

This script reads data contract definitions from YAML files and uses them
to validate JSON data records. It is designed to show how a semantic
contract can catch business logic errors that a simple schema check would miss.
"""

import json
import yaml
from typing import Any, Dict, List, Type

from pydantic import BaseModel, ValidationError, create_model

# --- Constants ---

# A mapping of contract-defined type strings to their Python equivalents.
TYPE_MAPPING: Dict[str, Type] = {
    "string": str,
    "number": float | int,
    "integer": int,
    "boolean": bool,
}

# A mapping of semantic 'unit' tags to the strictly enforced Python type.
# This is the core of the semantic type validation.
SEMANTIC_TYPE_MAP: Dict[str, Type] = {
    "full_unit": float,
    "cents": int,
}


# --- Helper for Colored Console Output ---

def print_color(text: str, color: str) -> None:
    """Prints text to the console with specified color."""
    colors = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "end": "\033[0m"}
    print(f"{colors.get(color, '')}{text}{colors['end']}")


# --- Core Logic ---

def create_pydantic_model_from_contract(contract: Dict[str, Any]) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model from a data contract dictionary.

    The model enforces basic types and whether a field is required.
    """
    fields: Dict[str, Any] = {}
    for field_name, attributes in contract.get("fields", {}).items():
        field_type_str = attributes.get("type", "string")
        python_type = TYPE_MAPPING.get(field_type_str, str)

        if attributes.get("required", False):
            # Ellipsis (...) marks the field as mandatory in Pydantic.
            field_definition = (python_type, ...)
        else:
            # Provide a default value of None to make the field optional.
            field_definition = (python_type | None, None)

        fields[field_name] = field_definition

    return create_model("DynamicContractModel", **fields)


def _is_record_valid(
        record: Dict[str, Any],
        contract: Dict[str, Any],
        pydantic_model: Type[BaseModel],
        contract_name: str,
) -> bool:
    """
    Performs a full validation of a single data record against a contract.
    Returns True if the record is valid, False otherwise.
    """
    record_id = record.get("order_id", "N/A")

    # 1. Basic Schema Validation (using the generated Pydantic model)
    try:
        pydantic_model(**record)
    except ValidationError as e:
        print_color(f"Record {record_id} FAILED {contract_name} schema validation: {e}", "red")
        return False

    # 2. Explicit Semantic Validation (the key part of the demo)
    for field_name, attributes in contract.get("fields", {}).items():
        if field_name not in record:
            continue

        tags = attributes.get("tags", {})
        value = record[field_name]

        # Check if a semantic unit requires a strict type.
        expected_type = SEMANTIC_TYPE_MAP.get(tags.get("unit"))
        if expected_type and not isinstance(value, expected_type):
            print_color(
                f"Record {record_id} FAILED {contract_name} semantic check: "
                f"Field '{field_name}' with unit '{tags['unit']}' must be a "
                f"{expected_type.__name__}, but got {type(value).__name__}.",
                "red"
            )
            return False

    # 3. Quality Rules Validation (using eval for dynamic rule execution)
    for rule in contract.get("quality_rules", []):
        try:
            # WARNING: eval() is used here for demonstration purposes.
            # In a production system, use a safer expression evaluation library.
            if not eval(rule["expression"], {}, record):
                print_color(
                    f"Record {record_id} FAILED {contract_name} quality rule "
                    f"'{rule['name']}': Expression '{rule['expression']}' is false.",
                    "red"
                )
                return False
        except Exception as e:
            print_color(
                f"Could not evaluate rule '{rule['name']}' on record {record_id}: {e}", "red"
            )
            return False

    return True


def validate_data_against_contract(
        data_records: List[Dict[str, Any]], contract: Dict[str, Any], contract_name: str
) -> bool:
    """

    Validates a list of data records against a data contract.
    """
    print_color(f"\n--- Running Validation with {contract_name} Contract ---", "yellow")

    pydantic_model = create_pydantic_model_from_contract(contract)

    # Use a list comprehension to check all records and collect results.
    results = [
        _is_record_valid(record, contract, pydantic_model, contract_name)
        for record in data_records
    ]

    all_records_valid = all(results)

    if all_records_valid:
        print_color(f"All records PASSED {contract_name} validation. ✅", "green")

    return all_records_valid


# --- Main Execution Block ---

def main():
    """
    Main function to load contracts and data, then run validations.
    """
    print("Analyzing data that is schema-valid but semantically incorrect...")

    with open("contract_v1_schema_only.yaml", "r") as f:
        contract_v1 = yaml.safe_load(f)

    with open("contract_v2_semantic.yaml", "r") as f:
        contract_v2 = yaml.safe_load(f)

    with open("data/bad_data_semantic_error.json", "r") as f:
        bad_data = json.load(f)

    # Run validations for both contracts.
    v1_passed = validate_data_against_contract(bad_data, contract_v1, "V1 (Schema-Only)")
    v2_passed = validate_data_against_contract(bad_data, contract_v2, "V2 (Semantic)")

    # Print final summary.
    print("\n" + "=" * 60)
    if v1_passed and not v2_passed:
        print_color(
            "SUCCESS: The semantic contract (V2) correctly caught errors that "
            "the basic schema (V1) missed!",
            "green",
        )
    else:
        print_color(
            "FAILURE: The demonstration logic is flawed, or both contracts passed/failed.", "red"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()