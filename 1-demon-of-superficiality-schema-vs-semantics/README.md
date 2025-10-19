# Demo 1: The Demon of Superficiality (Schema vs. Semantics)

This demo illustrates how a basic, schema-only data contract can be blind to critical business logic errors, while a semantic contract catches them.

## The Scenario

We have two data records that are semantically flawed:
1.  The `total_price` is sent as an integer (`1999`), implying cents, while the contract expects a float (`19.99`).
2.  The `total_price` is negative (`-5.00`), which violates business rules.

## How to Run

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Install dependencies:**
    *(This will create a virtual environment in `.venv/` and install packages from `poetry.lock`)*
    ```bash
    poetry install
    ```

2.  **Run the validation script:**
    *(This will execute the script using the virtual environment managed by Poetry)*
    ```bash
    poetry run python validate.py
    ```

## Expected Outcome

You will see that the V1 (schema-only) validation **passes**, because an integer is a valid `number` and the schema doesn't know prices can't be negative.

However, the V2 (semantic) validation will **fail**, correctly identifying both the type mismatch for a `full_unit` and the violation of the `price_must_be_positive` quality rule.