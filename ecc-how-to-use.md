# ECC and GitHub Copilot Chat in VS Code

This guide describes the lightweight ECC workflow included in this repository and
answers the common setup and usage questions. It is written for a human who wants to
inspect and approve each stage rather than delegate an open-ended task.

## What ECC is—and what this repository includes

ECC means [Everything Claude Code](https://github.com/affaan-m/ECC), an open-source
collection of agents, skills, rules, hooks, and engineering workflows. The upstream
README currently lists 71 agents, 314 skills, and 98 legacy command shims; those
inventory counts can change. ECC's fullest runtime is Claude Code. Its Copilot support
is capability-specific, so do not assume all Claude Code commands, hooks, or agents
are available in Copilot Chat.

This repository includes a **focused Copilot Chat adaptation**:

- `.github/copilot-instructions.md` provides repository-wide guidance.
- `.github/prompts/` provides `/plan`, `/tdd`, `/diff-review`, and `/verify`.
- `.vscode/settings.json` enables prompt-file discovery in VS Code.

It does not vendor all ECC agents or skills, install a separate model, or recreate
Claude Code hooks. Copilot CLI and Copilot Chat are different surfaces; a full ECC
Copilot CLI setup is not required for these VS Code prompts.

## Set up VS Code

1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install **GitHub Copilot** and **GitHub Copilot Chat** from the Extensions view.
   Install the Python extension for tracker development.
3. Sign in to GitHub in VS Code and confirm your Copilot subscription or organization
   policy provides Chat access.
4. Clone this repository and open its root folder in VS Code.
5. Open Copilot Chat. Type `/` and choose one of the repository prompt files. If the
   prompts do not appear, confirm `chat.promptFiles` is enabled in workspace settings,
   reload the VS Code window, and check that the repository root is the open folder.

There is no separate ECC install command for this repo-local Chat setup. Opening the
repository makes its instructions and prompt files available to the supported VS Code
Copilot surfaces.

## Human-in-the-loop process

```text
Goal
  → /plan
  → inspect and edit acceptance criteria
  → explicitly approve the plan
  → /tdd (RED → GREEN → IMPROVE)
  → inspect diff and test evidence
  → run project verification
  → human accepts, or requests a bounded fix
```

### 1. Start with one bounded goal

Give Copilot the outcome, boundaries, and any default or compatibility constraints.
For example:

> Add an optional minimum-forks filter to newly discovered repositories. Existing
> watchlist and previously tracked repositories must remain tracked. Do not change
> notification or dashboard behavior.

Keep the first task small enough to state observable acceptance criteria.

### 2. Plan, inspect, and edit the criteria

In Copilot Chat, invoke `/plan`. Ask it to inspect the relevant code/tests and return:

- files likely to change;
- acceptance criteria with boundary cases;
- tests and verification commands;
- risks, assumptions, and external side effects.

Read the proposal. Edit any incorrect assumption or missing criterion in chat. If the
behavior is ambiguous, resolve it before implementation. A plan is not approval.

### 3. Explicitly approve before implementation

When the criteria are correct, send a clear message such as:

> I approve the acceptance criteria above. Implement only those criteria; do not add
> unrelated changes.

If you do not approve, ask for a revised plan. In VS Code, keep tool/edit approval
controls enabled and inspect terminal commands before accepting them.

### 4. Use `/tdd`

After approval, invoke `/tdd` and refer to the approved criteria. The intended cycle is:

1. **RED:** add a test for one criterion and run it; confirm it fails for the expected
   reason.
2. **GREEN:** implement the smallest behavior change and rerun the test.
3. **IMPROVE:** simplify only where useful, then rerun relevant tests.

Do not accept a test that passed before the implementation as proof of the new behavior.
For this Python project, tests use `unittest`; do not call live external APIs from them.

### 5. Review the diff and evidence

Inspect Source Control or run:

```sh
git diff --check
git diff
```

Invoke `/diff-review` for a second, read-only pass. Check that the diff matches the approved
scope, tests cover the behavior, generated data was not changed accidentally, and no
secrets were added. Review the actual test output; a Copilot summary is not evidence.

### 6. Verify, then accept or request a fix

For tracker changes, from the repository root run:

```sh
python -m unittest discover -s repo-trend-tracker/tests -v
python -m py_compile repo-trend-tracker/track_and_notify.py
git diff --check
```

`/verify` can run and report the same checks. Do not run `python
repo-trend-tracker/track_and_notify.py` as a test: it makes live network requests and
may send email if secrets are configured.

Accept only after you confirm the request, diff, and test evidence align. Otherwise,
ask for one specific fix, inspect its changed diff, and rerun the relevant checks.

## Common questions

### Does this install all 71 agents and 314 skills into Copilot Chat?

No. Those are upstream ECC inventory counts, not files installed by this starter. This
repo uses only a small native VS Code prompt/instructions surface. A repository prompt
does not make every ECC skill, agent, or hook available. If you want the full ECC
Copilot CLI adapter, follow the current official installation instructions in the
[ECC repository](https://github.com/affaan-m/ECC) and check its platform support
matrix; that is a separate setup and is not needed here.

### Is `/tdd` a Claude Code command?

Not here. It is a VS Code Copilot prompt file under `.github/prompts/tdd.prompt.md`.
VS Code exposes it as a slash prompt. It contains instructions for Copilot Chat; it is
not a hook and does not guarantee enforcement.

### Do the prompts block file edits until I approve a plan?

The plan prompt explicitly asks Copilot to stop and wait, but prompt text is not a
security boundary. Approval depends on your explicit chat instruction and VS Code's
tool/edit permission settings. Keep those controls enabled and do not approve edits
before you have reviewed the criteria.

### Which model does ECC use?

ECC does not supply or own the model used by Copilot Chat. Select a model available to
your GitHub Copilot account using the model picker in Chat. Available models and
policies depend on your current plan and organization settings; check those settings
before relying on a particular model. Changing a prompt file does not change model
access.

### Does Copilot Chat automatically run ECC hooks or manage agents?

No. This repository's Chat integration consists of instructions and prompt files.
Do not assume Claude Code hooks, lifecycle automation, agent orchestration, or full
ECC skill discovery are running in VS Code Chat. The user must inspect and approve
commands, edits, and external side effects.

### Where do I start if a prompt is missing?

Confirm the repo root is open, `chat.promptFiles` is enabled, GitHub Copilot Chat is
installed and signed in, then reload VS Code. Prompt availability can also depend on
the installed VS Code and Copilot extension versions.
