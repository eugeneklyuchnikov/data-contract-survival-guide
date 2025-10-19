# Demo 2: The Demon of Gigantism (Tiers of Trust)

This demo illustrates a strategic approach to data contracts by showcasing what contracts for different "tiers" of data look like. The philosophy is that trust is a feature with a cost, so we shouldn't apply the same level of rigor to all data.

This demo includes an executable "auditor" script that scans the contracts and generates a report on their guarantees.

## How to Run

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Install dependencies:**
    ```bash
    poetry install
    ```

2.  **Run the auditor script:**
    ```bash
    poetry run python auditor.py
    ```

## Expected Outcome

The script will print a table summarizing the characteristics of each contract. This report makes the difference in rigor between Gold, Silver, and Bronze immediately obvious.

## The Artifacts

The contracts themselves are the core of the demonstration.

### 🥇 [Gold Tier: `contracts/gold/finance_reporting.yaml`](contracts/gold/finance_reporting.yaml)
- **Rigor:** Very strict, detailed fields and quality rules.
- **Governance:** Clear ownership and aggressive SLAs.

### 🥈 [Silver Tier: `contracts/silver/product_analytics.yaml`](contracts/silver/product_analytics.yaml)
- **Rigor:** Pragmatic. Guarantees backward compatibility.
- **Governance:** Defined ownership and reasonable SLAs.

### 🥉 [Bronze Tier: `contracts/bronze/raw_event_stream.md`](contracts/bronze/raw_event_stream.md)
- **Rigor:** None. The contract is a warning label.
- **Governance:** `¯\_(ツ)_/¯`