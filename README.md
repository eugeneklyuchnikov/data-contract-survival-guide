# Data Contract Survival Guide

Welcome to the official code repository for the keynote presentation **"Data Contracts VS Data Chaos: A Survival Story"**.

[➡️ **View the Presentation Slides & Video Here**](LINK_TO_SLIDES_GOES_HERE)

This repository contains a series of practical, hands-on demonstrations designed to bring the core concepts of the talk to life. It was created to serve as a living resource for engineers, analysts, and leaders looking to tame data chaos and build a culture of trust.

Created by [**Eugene Klyuchnikov**](https://www.linkedin.com/in/eugene-klyuchnikov/).

---

## Core Philosophy

> Our most important job as data practitioners is not to build pipelines. It's to build **trust**. This repository shows how to turn that philosophy into executable code.

---

## The Four Demos: A Battle Against Chaos

This repository is structured as a series of battles against the four "demons" of data chaos. Each directory is a self-contained demonstration with its own code, contracts, and instructions.

###  démon 1: The Demon of Superficiality

*   **Folder:** [`1-demon-of-superficiality-schema-vs-semantics/`](./1-demon-of-superficiality-schema-vs-semantics/)
*   **Question:** "Isn't a data contract just a fancy schema?"
*   **Demonstration:** This demo uses a Python script (`validate.py`) to show how a basic, schema-only contract is blind to critical business logic errors, while a deeper, semantic contract catches them instantly.

### 🥈 démon 2: The Demon of Gigantism

*   **Folder:** [`2-demon-of-gigantism-tiers-and-models/`](./2-demon-of-gigantism-tiers-and-models/)
*   **Question:** "This looks complex. Do we have to do this for ALL our data?"
*   **Demonstration:** This demo showcases the concept of "Tiers of Trust." It contains example contracts for **Gold**, **Silver**, and **Bronze** data to illustrate a strategic, pragmatic approach. Run the `auditor.py` script to see a report on the different levels of rigor.

### 🥉 démon 3: The Demon of Staticity

*   **Folder:** [`3-demon-of-staticity-managed-evolution/`](./3-demon-of-staticity-managed-evolution/)
*   **Question:** "What happens when the business changes? Won't contracts slow us down?"
*   **Demonstration:** This is a live demo of "Managed Evolution" using a real **GitHub Actions CI/CD pipeline**. It shows how the system can automatically approve safe, non-breaking changes while blocking dangerous, breaking changes until they are reviewed. (Requires forking the repo and opening a PR to test).

### 🏅 démon 4: The Demon of the Future

*   **Folder:** [`4-demon-of-the-future-the-diplomat/`](./4-demon-of-the-future-the-diplomat/)
*   **Question:** "This is great, but what's our AI story?"
*   **Demonstration:** This demo features a working AI agent, "The Diplomat," which uses the **Google Gemini API**. It reads raw data and human context to proactively generate a high-quality draft of a data contract, showcasing a visionary yet practical application of LLMs in data governance.

---

## How to Use This Repository

This project is designed to be highly reproducible. Each demo is a self-contained project.

### Prerequisites

You will need the following tools installed:
*   [Git](https://git-scm.com/)
*   [pyenv](https://github.com/pyenv/pyenv) (Recommended for managing Python versions)
*   [Poetry](https://python-poetry.org/) (For dependency management)

### General Workflow

The pattern for running each demo is the same:

1.  **Navigate to the demo directory:**
    ```bash
    cd <name-of-the-demo-folder>
    ```

2.  **Install dependencies:**
    This command will create a local virtual environment (`.venv`) and install the specific packages needed for that demo.
    ```bash
    poetry install
    ```

3.  **Run the demo script:**
    Follow the instructions in the `README.md` file inside that specific demo folder. The command will typically be:
    ```bash
    poetry run python <script_name>.py
    ```

---

## Feedback & Contributions

Feedback, questions, and contributions are highly welcome. Please feel free to open an [Issue](https://github.com/eugeneklyuchnikov/data-contract-survival-guide/issues) for discussion or a [Pull Request](https://github.com/eugeneklyuchnikov/data-contract-survival-guide/pulls) with improvements.

## About the Author

This repository was created and is maintained by **Eugene Klyuchnikov**, a Principal Data Engineer passionate about building trustworthy and scalable data platforms.

*   **LinkedIn:** [linkedin.com/in/eugene-klyuchnikov](https://www.linkedin.com/in/eugene-klyuchnikov/)

---

This project is licensed under the MIT License.