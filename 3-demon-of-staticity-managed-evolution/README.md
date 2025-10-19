# Demo 3: The Demon of Staticity (Managed Evolution)

This demo showcases how a CI/CD pipeline (using GitHub Actions) can act as an automated guardian for your data contracts, enabling safe, managed evolution.

The core of this demo is the workflow defined in [`.github/workflows/contract_check.yml`](../../.github/workflows/contract_check.yml). It automatically runs the `breaking_change_detector.py` script on any Pull Request that modifies the `contracts/orders_v1.yaml` file.

## How to See it in Action

This demo is interactive and requires you to open a Pull Request.

1.  **Fork this repository.**
2.  **Create a new branch** in your fork (e.g., `test-evolution`).
3.  **Choose your experiment** below and make the described changes.
4.  **Commit and push** your changes, then **open a Pull Request** to the main branch of your fork.
5.  Go to the "Checks" tab of your Pull Request to see the GitHub Action run.

### Experiment 1: A Safe, Minor Change (CI should pass ✅)

In your branch, copy the contents of `contracts/orders_v2_minor_change.yaml` and paste them into `contracts/orders_v1.yaml`, overwriting the original content. Commit and open a PR. The GitHub Action should run and pass, as no fields were removed.

### Experiment 2: A Dangerous, Breaking Change (CI should fail 🚨)

In a different branch, copy the contents of `contracts/orders_v3_breaking_change.yaml` and paste them into `contracts/orders_v1.yaml`. Commit and open a PR. The GitHub Action should run and **fail**, blocking a potential merge and correctly identifying that the `order_id` field was removed.