## Purpose

This repository currently contains a single `README.md` with the title "Machine Learning Portfolio" and no code, tests, or project layout. These instructions tell an AI coding agent how to be immediately productive here: how to proceed when scaffolding new ML projects, what conventions to follow, and what to ask the human owner before making large changes.

## Assumptions (explicit)
- The repo is a personal ML portfolio (title in `README.md`).
- No existing code layout or CI is present; agents must not delete the README and should ask before making opinionated, large reorganizations.

## High-level goals for agents
- Preserve the existing `README.md` content and keep commits small and descriptive.
- When adding work, create a minimal, self-contained project scaffold rather than sprinkling files at the repo root.

## When you start a new project in this repo
1. Ask a short clarifying question if the user hasn't specified the project name, language, or preferred environment (conda vs venv).
2. Create a directory `projects/<project-name>/` and inside it include at minimum:
   - `projects/<project-name>/README.md` — short summary and commands to run.
   - `projects/<project-name>/src/` — Python package code (if using Python) with an `__init__.py`.
   - `projects/<project-name>/notebooks/` — exploratory notebooks (named `<project>-exploration.ipynb`).
   - `projects/<project-name>/data/` — placeholder `.gitkeep` and a note to not commit large datasets.
   - `projects/<project-name>/requirements.txt` or `pyproject.toml` — concrete deps when code is added.

Example: add a new model project called `iris-classifier` under `projects/iris-classifier/`.

## Environment & commands (explicit examples for Linux / bash)
- Create a virtual environment and install deps (use when you add Python code):
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Run tests (if you add tests): `pytest -q`

## File/contribution conventions
- Notebook files belong in `projects/<project>/notebooks/` and should be accompanied by a short `README.md` describing their purpose.
- Scripts, library code, and reusable functions must go under `src/` inside the project folder and expose a clear API (avoid top-level scripts without a small wrapper).
- Large artifacts (datasets, model weights) must not be committed. Add a short note to the project's `README.md` describing where to download or how to generate them.

## Commit messages and PRs
- Keep commits small and focused. Use present-tense short subject, e.g. `projects/iris-classifier: add data loader and training script`.
- When creating a PR, include the minimal reproduction steps in the PR description and point to the project `README.md` for run instructions.

## What to avoid
- Do not reorganize the entire repository without asking the user first. The repo currently only has `README.md` and may represent a personal portfolio layout preference.
- Do not add credentials or secrets to the repo. If a secret is needed, add a placeholder and ask the user how they'd like it handled.

## If you need to scaffold CI, tests, or packaging
- Propose a short plan in the PR description first. Examples of minimal CI you may propose:
  - GitHub Actions workflow that runs `pip install -r requirements.txt` and `pytest` for projects that include tests.

## Minimal quality checks before committing code
- Code runs locally in a venv and dependencies are captured in `requirements.txt` or `pyproject.toml`.
- Notebooks include a short `README.md` describing inputs/outputs and expected runtime.

## When you are unsure
- Ask one clear question describing the ambiguity (project name, environment preference, dataset location). Do not guess large decisions.

---
If you'd like, I can now scaffold an example project (empty template) under `projects/example-project/` so future PRs have a reference layout. Should I proceed or wait for your preferred project details?
