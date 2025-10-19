# Demo 4: The Demon of the Future (The AI Diplomat)

This demo showcases a forward-looking use case for AI in data governance. It features an "AI Diplomat" that uses the Google Gemini API to proactively generate a draft data contract from raw data and human context.

## How to Run

This project uses the Gemini API and requires an API key.

1.  **Get your API Key:**
    - Go to [Google AI Studio](https://aistudio.google.com/).
    - Create an API key.

2.  **Configure your environment:**
    - Create a file named `.env` in this directory.
    - Add your key to it like this: `GEMINI_API_KEY="your_api_key_goes_here"`

3.  **Install dependencies:**
    ```bash
    poetry install
    ```

4.  **Run the AI Diplomat script:**
    ```bash
    poetry run python diplomat_ai.py
    ```

## Expected Outcome

The script will:
1.  Read the sample data and context from the `input/` directory.
2.  Call the Gemini API with a detailed prompt.
3.  Process the AI's response.
4.  Create a new file named `proposed_contract.yaml` containing a well-structured, Silver-tier contract draft.

Open the generated YAML file to see how the AI inferred types, wrote descriptions, and even proposed a quality rule based on the inputs.