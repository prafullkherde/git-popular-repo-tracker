# Git Popular Repo Tracker

A standalone GitHub Actions project that snapshots GitHub repository growth, classifies
repo lifecycle phases, optionally emails a digest, and publishes a static dashboard.
It is adapted from the `repo-trend-tracker/` application and workflow in
[ai-news-feed-git-hub-action](https://github.com/prafullkherde/ai-news-feed-git-hub-action).

The starter also includes a small, repo-local **ECC-style workflow for GitHub Copilot
Chat in VS Code**: instructions plus `/plan`, `/tdd`, `/diff-review`, and `/verify` prompt
files. It is intentionally not a copy of the full Everything Claude Code (ECC)
runtime. See [ecc-how-to-use.md](ecc-how-to-use.md) for what works in Copilot Chat and
how to follow the human approval gates.

## First feature: minimum-star filter

`repo-trend-tracker/data/watchlist_seed.json` contains `"minimum_stars": 50`. Newly
discovered repositories below that value are not snapshotted. A repository exactly at
the threshold is included. Repositories in `always_track` and repositories already
present in snapshot history continue to be tracked regardless of the threshold.

Set `minimum_stars` to any non-negative integer; use `0` to disable the filter. This is
a discovery filter, not a way to remove an existing repository from tracking. The
legacy watchlist format (a JSON array of repository names) remains supported and uses a
threshold of `0`.

## Try it locally

### Requirements

- Python 3.11
- Git
- VS Code and access to GitHub Copilot if you want to follow the guided chat workflow

Create an environment and install the tracker dependencies from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r repo-trend-tracker/requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

Run the deterministic tests and syntax check:

```sh
python -m unittest discover -s repo-trend-tracker/tests -v
python -m py_compile repo-trend-tracker/track_and_notify.py
```

To run the tracker itself, use:

```sh
python repo-trend-tracker/track_and_notify.py
```

That command makes live requests to GitHub and public trend/news endpoints and updates
the tracked CSV/JSON data. A local `GITHUB_TOKEN` is optional, but authenticated GitHub
API access provides a higher rate limit. Email is skipped unless both `RESEND_API_KEY`
and `MY_EMAIL` are set. Groq-based explanations are optional and require
`GROQ_API_KEY_FOR_AUTO_EMAIL`. Never commit tokens or put them in the watchlist file.

## GitHub Actions and dashboard

`.github/workflows/repo-trend-tracker.yml` can be started manually from the Actions
tab. It also runs at 03:00 UTC on Mondays and Thursdays. Each run:

1. Installs the requirements and runs the tracker.
2. Persists snapshots, notification state, and health data.
3. Copies the dashboard to `docs/repo-trend-tracker/` and commits data changes.

The workflow uses the built-in `GITHUB_TOKEN`; no personal access token is required.
It requests only `contents: write` so it can commit generated tracker state. If your
organization or repository restricts Actions token write access, an owner must allow
the workflow's declared permission.

To publish the dashboard, open **Settings → Pages** and choose **Deploy from a branch**,
branch `main`, folder `/docs`. The dashboard URL is
`https://prafullkherde.github.io/git-populer-repo-tracker/repo-trend-tracker/`.
Set the repository Actions variable `DASHBOARD_URL` only if you use a different URL.
The workflow includes the link in each run summary.

### Optional email secrets

Add these under **Settings → Secrets and variables → Actions → Secrets** only if you
want email:

| Secret | Purpose |
| --- | --- |
| `RESEND_API_KEY` | Resend API credential used for outbound digest email |
| `MY_EMAIL` | One or more recipient addresses, comma-separated |
| `GROQ_API_KEY_FOR_AUTO_EMAIL` | Optional evidence-based summary text |

Without the first two, the workflow still records data and prints that email was
skipped. Without the Groq key, the digest can still be sent without generated
explanations. `GITHUB_TOKEN` is supplied by GitHub Actions automatically.

## Follow the learning workflow in VS Code

1. Install the **GitHub Copilot** and **GitHub Copilot Chat** extensions, sign in, and
   open this repository as a folder. The repository recommends these extensions and
   enables prompt files in `.vscode/`.
2. In Copilot Chat, type `/plan` and select the repository's plan prompt. Ask for one
   small change. Inspect and edit the acceptance criteria; do not let implementation
   begin until you explicitly approve those criteria in chat.
3. After approval, invoke `/tdd` and ask Copilot to implement only the approved scope.
   Expect to see a failing test first, then the minimal change and a passing test.
4. Inspect the changed files in Source Control and review the complete diff. Use
   `/diff-review` for a read-only review; verify test output yourself.
5. Run the project verification commands above or invoke `/verify`. Accept the work
   only when the diff, tests, and requested behavior match. Otherwise, ask for a
   specific fix and repeat the relevant tests.

The prompt files guide Copilot; they do not enforce approvals or execute Claude Code
hooks. Keep human approval enabled for edits and terminal commands in your VS Code
settings. The full usage guide is [ecc-how-to-use.md](ecc-how-to-use.md).

## Project layout

```text
.github/
  copilot-instructions.md
  prompts/                 # repo-local Copilot Chat slash prompts
  workflows/
repo-trend-tracker/
  track_and_notify.py
  requirements.txt
  tests/
  data/                    # watchlist, append-only snapshots, health and email state
  dashboard/               # static dashboard and generated data
docs/repo-trend-tracker/   # GitHub Pages copy, refreshed by Actions
ecc-how-to-use.md
```

The tracker uses `data/snapshots.csv` as its history source; the workflow commits
changes so the dashboard has a persistent trend history. No database is required.

---

## 🎯 ECC-Enhanced Workflow

This repository now includes **ECC (Everything Claude Code) integration** for enhanced GitHub Copilot Chat workflows.

### What's New?

The basic `/plan`, `/tdd`, `/diff-review`, and `/verify` commands have been enhanced with:

✅ **Structured workflows** - Clear chain from planning → testing → review → validation  
✅ **ECC pattern grounding** - References to skills, hooks, and rules from the full ECC framework  
✅ **Approval gates** - Explicit confirmation gates before each step  
✅ **Acceptance criteria** - Measurable, checklist-based validation  

### Quick Start

Try the ECC workflow:

```bash
# 1. Plan a feature
/plan Add multi-language dashboard support

# 2. Implement with TDD (after approval)
/tdd

# 3. Review changes
/diff-review

# 4. Final validation
/verify

# 5. Create PR
/pr Add multi-language dashboard support
```

### Learn More

See **[ECC-INTEGRATION-GUIDE.md](ECC-INTEGRATION-GUIDE.md)** for:
- Detailed comparison: Normal `/plan` vs. ECC `/plan`
- Workflow chain and approval gates
- Pattern grounding and acceptance criteria
- Troubleshooting and references

### Reference

- **ECC Repository**: https://github.com/affaan-m/ecc
- **Integration Guide**: `ECC-INTEGRATION-GUIDE.md`
- **Original How-To**: `ecc-how-to-use.md`

