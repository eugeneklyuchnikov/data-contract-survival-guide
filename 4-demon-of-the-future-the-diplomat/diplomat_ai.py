"""
diplomat_ai.py

An AI agent that demonstrates the "Diplomat" role.
It reads raw data and human context, then uses the Gemini API to
proactively generate a draft for a Silver-tier data contract.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any

import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console

# --- Constants: Strong Pattern ---
# Centralizing configuration makes the script easier to maintain.
PROMPT_TEMPLATE = """
You are an expert Data Governance assistant named "The Diplomat".
Your task is to create a high-quality draft for a Silver-tier data contract in YAML format based on the provided data sample and context.

**Instructions:**
1.  Analyze the JSON data sample to infer field names, data types (string, integer, ISO timestamp, nested object), and whether fields are required.
2.  Use the human-provided context to write clear, helpful descriptions for each field.
3.  Infer the overall dataset name or purpose from the context (e.g., "Gamification Events").
4.  Propose at least one meaningful quality rule based on the data's nature (e.g., user_id should be required and not empty).
5.  Set the owner and SLA to placeholder values like 'TBD' but suggest a suitable support channel name.
6.  Ensure the schema evolution policy is set to `backward_compatible: true` as this is a Silver-tier contract.
7.  Your final output MUST be only the YAML content, enclosed in ```yaml ... ```. Do not add any other explanatory text.

**Context from Jira Ticket/Chat:**
---
{context}
---

**JSON Data Sample:**
---
{data_sample}
---
"""

INPUT_DIR = Path("input")
OUTPUT_FILE = Path("proposed_contract.yaml")
CONTEXT_FILE = INPUT_DIR / "context.txt"
DATA_SAMPLE_FILE = INPUT_DIR / "data_sample.json"

# --- Core Logic as a Class: Strong Pattern ---
# Encapsulating the logic in a class improves structure and testability.
class DiplomatAI:
    """Orchestrates the process of generating a data contract using an AI model."""

    def __init__(self, model: genai.GenerativeModel):
        # Dependency Injection: The model is passed in, not created inside.
        self.model = model

    def _load_inputs(self) -> Dict[str, str]:
        """Loads context and data sample from files, with robust checks."""
        if not CONTEXT_FILE.is_file() or not DATA_SAMPLE_FILE.is_file():
            raise FileNotFoundError(
                f"Ensure both '{CONTEXT_FILE}' and '{DATA_SAMPLE_FILE}' exist."
            )

        context = CONTEXT_FILE.read_text()
        data_sample = DATA_SAMPLE_FILE.read_text()
        return {"context": context, "data_sample": data_sample}

    def _extract_yaml_from_response(self, response_text: str) -> str:
        """Extracts the YAML code block from the LLM's raw response."""
        try:
            start = response_text.index("```yaml") + len("```yaml\n")
            end = response_text.index("```", start)
            yaml_content = response_text[start:end].strip()

            # Self-validation to ensure the extracted content is valid YAML
            yaml.safe_load(yaml_content)

            return yaml_content
        except yaml.YAMLError as e:
            raise ValueError(f"AI generated invalid YAML: {e}")
        except ValueError:
            raise ValueError("Could not find a valid YAML block (```yaml ... ```) in the AI's response.")

    def generate_contract(self) -> str:
        """The main method to generate the contract."""
        console = Console()

        console.print(f"📄 Reading inputs from [cyan]{INPUT_DIR}[/cyan]...")
        inputs = self._load_inputs()

        prompt = PROMPT_TEMPLATE.format(**inputs)

        console.print("🤖 Querying the Gemini API...")
        response = self.model.generate_content(prompt)

        console.print("📝 Processing AI response and extracting YAML...")
        proposed_yaml = self._extract_yaml_from_response(response.text)

        return proposed_yaml

# --- Setup and Execution ---

def configure_gemini() -> genai.GenerativeModel:
    """Configures and returns a Gemini model instance from environment variables."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest") # Default model

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def main():
    """Main function to run the AI Diplomat."""
    console = Console()
    console.print("[bold yellow]--- Running AI Diplomat ---[/bold yellow]")

    try:
        model = configure_gemini()
        diplomat = DiplomatAI(model)
        proposed_contract_yaml = diplomat.generate_contract()

        OUTPUT_FILE.write_text(proposed_contract_yaml)

        console.print(f"\n[bold green]✅ Success! Proposed contract saved to:[/] [cyan]{OUTPUT_FILE}[/cyan]")
        console.print("\n[italic]Go check out the file to see what the AI Diplomat created![/italic]")

    # Specific Error Handling: Strong Pattern
    except (FileNotFoundError, ValueError) as e:
        console.print(f"\n[bold red]🚨 CONFIGURATION ERROR: {e}[/bold red]")
        console.print("[yellow]Please ensure your .env file and input/ directory are set up correctly.[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]🚨 AN UNEXPECTED ERROR OCCURRED: {e}[/bold red]")

if __name__ == "__main__":
    main()