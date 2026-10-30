# Repository instructions for GitHub Copilot

This repository is a Python 3.11 GitHub Actions tracker. The application lives in
`repo-trend-tracker/`; tests use Python's built-in `unittest`.

## Engineering workflow

- Inspect the relevant code and existing tests before proposing changes.
- For behavior changes, define observable acceptance criteria and tests first.
- Keep changes inside the requested scope. Do not call live APIs from unit tests.
- Preserve `watchlist_seed.json` compatibility with its legacy flat-array format.
- Run `python -m unittest discover -s repo-trend-tracker/tests -v` from the repository root.
- Review the complete diff and report exact commands and results; never claim checks
  passed if they were not run.
- Do not manually edit or include generated snapshots in unrelated code changes; the
  Actions workflow intentionally commits its own tracker outputs. Never put tokens or
  recipient addresses in source files.

## Human approval gates

- For work beyond a trivial one-line change, use `/plan` and wait for the user to
  explicitly approve the acceptance criteria before editing.
- Use `/tdd` only after that approval. Show the failing test, passing test, and any
  remaining verification gaps.
- Use `/diff-review` for a read-only diff review and `/verify` for final checks.
- Ask before running live workflows, sending email, changing repository settings, or
  performing other external side effects.

These are repository instructions and reusable prompt files, not a technical policy
engine. Copilot Chat may not enforce them; the human remains responsible for approvals
and acceptance.
