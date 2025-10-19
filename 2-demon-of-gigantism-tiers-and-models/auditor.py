"""
auditor.py

A script that acts as a "Data Governance Auditor".
It scans a directory of data contracts and reports on their characteristics,
highlighting the difference in rigor between Gold, Silver, and Bronze tiers.
"""
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.table import Table

# --- Data Structure for Audit Results ---

@dataclass
class AuditResult:
    """A structured representation of a contract's audit findings."""

    tier: str
    dataset: str
    owner: str
    sla: str
    guarantees: str

# --- Core Logic: Parsing and Auditing ---

def _parse_gold_silver_contract(
    file_path: Path, contract_data: Dict
) -> AuditResult:
    """Parses a standard YAML (Gold/Silver) contract."""
    tier_name = file_path.parent.name.capitalize()
    tier_emoji = {"Gold": "🥇", "Silver": "🥈"}.get(tier_name, "❓")

    owner = contract_data.get("owner", {}).get("team", "Undefined")

    # Safely extract SLA details
    sla_info = contract_data.get("sla", [{}])[0]
    freshness = sla_info.get("max_latency_hours")
    sla_str = f"{freshness}h freshness" if freshness else "N/A"

    # Aggregate guarantees
    guarantees = []
    if contract_data.get("schema_evolution", {}).get("backward_compatible"):
        guarantees.append("Backward Compatible")
    quality_rule_count = len(contract_data.get("quality_rules", []))
    if quality_rule_count > 0:
        guarantees.append(f"{quality_rule_count} Quality Rules")

    return AuditResult(
        tier=f"{tier_emoji} {tier_name}",
        dataset=file_path.stem,
        owner=owner,
        sla=sla_str,
        guarantees=", ".join(guarantees) or "None",
    )


def _parse_bronze_contract(file_path: Path) -> AuditResult:
    """Parses the special-case Markdown (Bronze) contract."""
    return AuditResult(
        tier="🥉 Bronze",
        dataset=file_path.stem,
        owner="The Universe",
        sla="Best-effort on a full moon",
        guarantees="¯\_(ツ)_/¯",
    )


def audit_contract_file(file_path: Path) -> Optional[AuditResult]:
    """
    Audits a single contract file, routing to the correct parser.
    Returns an AuditResult or None if parsing fails.
    """
    try:
        if file_path.suffix == ".md":
            return _parse_bronze_contract(file_path)

        if file_path.suffix in [".yaml", ".yml"]:
            with file_path.open("r") as f:
                contract_data = yaml.safe_load(f)
            return _parse_gold_silver_contract(file_path, contract_data)

    except (IOError, yaml.YAMLError) as e:
        print_color(f"Error processing file {file_path.name}: {e}", "red")

    return None

# --- Presentation Logic ---

def create_report_table(audit_results: List[AuditResult]) -> Table:
    """Creates a rich Table object from a list of audit results."""
    table = Table(title="Data Contract Audit Report")
    table.add_column("Tier", justify="left", style="cyan", no_wrap=True)
    table.add_column("Dataset", justify="left", style="magenta")
    table.add_column("Owner", justify="left", style="green")
    table.add_column("SLA", justify="center", style="yellow")
    table.add_column("Guarantees", justify="left", style="white")

    for result in audit_results:
        table.add_row(
            result.tier,
            result.dataset,
            result.owner,
            result.sla,
            result.guarantees,
        )
    return table

# --- Main Execution Block ---

def main():
    """Finds all contracts, audits them, and prints a summary table."""
    console = Console()
    console.print("[bold yellow]--- Running Data Governance Audit ---[/bold yellow]")

    contracts_path = Path("contracts")
    if not contracts_path.is_dir():
        console.print(f"[bold red]Error: Directory not found at '{contracts_path}'[/bold red]")
        return

    # Find all potential contract files
    contract_files = sorted(
        [p for p in contracts_path.glob("**/*") if p.suffix in [".yaml", ".yml", ".md"]]
    )

    if not contract_files:
        console.print("[bold red]No contract files (.yaml, .yml, .md) found![/bold red]")
        return

    # Process files and filter out any that failed to parse
    audit_results = [
        result for path in contract_files if (result := audit_contract_file(path))
    ]

    report_table = create_report_table(audit_results)
    console.print(report_table)


if __name__ == "__main__":
    main()