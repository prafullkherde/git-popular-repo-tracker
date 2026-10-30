# ECC: Real Installation and Usage Guide

This guide explains how to add real ECC-managed capabilities to this repository
without confusing a prompt-file adaptation with a full ECC installation. It is
intended to be sufficient for a future contributor or coding agent to implement
the integration without repeating the research.

## The short answer

ECC can be installed as a development tool, but it is **not** a Python runtime
dependency and should not be imported as a JavaScript library to access
`skills`, `rules`, or `commands`.

The npm package, `ecc-universal`, provides ECC's command-line installer and
other CLI tools. A real integration for this repository means using that
installer to generate ECC-native files for a supported harness, then reviewing
and committing the generated files. For GitHub Copilot, the target installs
skills and agents for **Copilot CLI**. It does not install ECC's Claude Code
hooks or provide full Claude Code feature parity in VS Code Copilot Chat.

The existing `.github/prompts/` and `.github/copilot-instructions.md` files
remain useful for VS Code Copilot Chat. They are repository-owned prompt and
instruction files, not a full ECC installation.

## Important corrections

Do not implement the integration based on these inaccurate assumptions:

- `ecc-universal` does not provide a documented application API such as
  `import { skills, rules, commands } from "ecc-universal"`.
- Adding `ecc-universal` to `package.json` does not, by itself, make ECC skills,
  agents, commands, or hooks active in a coding harness.
- The Copilot installer target is for Copilot CLI's native project skills and
  agents. It does not make every ECC command, hook, or Claude Code behavior
  available in VS Code Copilot Chat.
- A prompt mentioning an ECC path or pattern is only a written reference. It
  does not install, load, or execute the referenced ECC capability.
- ECC's full feature set is harness-dependent. Do not promise feature parity
  where ECC's platform support documentation describes only partial support.

## What this repository has today

This repository is a Python project and currently has a focused VS Code Copilot
Chat setup:

| Surface | Repository files | What they provide |
|---|---|---|
| Copilot Chat instructions | `.github/copilot-instructions.md` | Repository-wide guidance |
| Reusable Chat prompts | `.github/prompts/*.prompt.md` | Slash-selectable prompt files |
| VS Code prompt discovery | `.vscode/settings.json` | Enables `chat.promptFiles` |
| ECC runtime / installer | Not installed | No ECC-managed skills, agents, or hooks are installed by these files |

This arrangement is lightweight and does not require Node.js or an ECC package
dependency. It is also not a full ECC installation.

## Choose the integration that matches the goal

| Goal | Recommended approach | What it does not do |
|---|---|---|
| Use the existing `/plan`, `/tdd`, `/diff-review`, and `/verify` in VS Code Chat | Keep the repository prompt files | Does not install ECC skills, agents, or hooks |
| Use ECC-native skills and agents in Copilot CLI | Run ECC's official `copilot` install target | Does not provide Claude Code hook parity or replace VS Code prompts |
| Make ECC installation reproducible for contributors | Pin `ecc-universal` as a development dependency, then run its installer | Does not turn ECC into an app/runtime library |
| Use ECC's fullest native workflow | Follow ECC's current setup for a harness with the required support, such as Claude Code | Does not make those features portable to every harness |

### Recommendation for this Python repository

If the goal is **Copilot CLI skills and agents**, use ECC's official Copilot
installer target and keep the installed files under version control. Consider a
pinned `ecc-universal` development dependency only if maintainers want a
repeatable, repository-local installation command.

If the goal is **VS Code Copilot Chat**, keep the native `.github/prompts/`
files. Adapt only the specific ECC workflow or skill content that is useful;
do not describe that adaptation as a full ECC install.

If the goal is to use **all ECC capabilities**, first choose a harness that
supports those capabilities. Installing the Copilot target cannot enable
Claude-specific hooks or orchestration in VS Code Chat.

## Install ECC for Copilot CLI

### Before installing

1. Start from a clean branch based on the current default branch.
2. Confirm Node.js 18 or newer, Git, and the intended Copilot CLI are available.
3. Read the current ECC [platform support notes](https://github.com/affaan-m/ECC)
   and [official installation instructions](https://github.com/affaan-m/ECC).
4. Choose the smallest set of skills and agents that serve the repository.
   Avoid the full catalog by default: it contains unrelated languages and
   workflows.
5. Inspect ECC's installer source/release and the proposed file changes before
   running an installer that writes into the project.

### Option 1: Run a version-pinned installer without adding a package manifest

This uses the official npm package for one installation run. It does not add
ECC to this repository's dependency manifest:

```sh
npx ecc-universal@2.2.3 install --target copilot --skills python-patterns,python-testing,tdd-workflow,verification-loop --dry-run
```

Review the dry-run output. If its planned paths and scope are acceptable, run
the same command without `--dry-run`:

```sh
npx ecc-universal@2.2.3 install --target copilot --skills python-patterns,python-testing,tdd-workflow,verification-loop
```

The installer may include dependency modules and supporting files beyond the
named skills. Treat the dry-run file plan as authoritative; do not assume the
`--skills` list is the complete set of files that will be written.

`2.2.3` is the release inspected while writing this guide, not a claim that it
will remain the newest release. Before using these commands later, check the
official ECC README and npm release page, select a reviewed version, and pin
that version explicitly.

### Option 2: Track ECC as a development dependency

Use this if contributors should install ECC tooling with the repository's
documented setup and lockfile. It adds Node/npm tooling to an otherwise
Python-only project, so only do this if the team wants that maintenance cost.

If there is no `package.json`, initialize a minimal npm manifest, then pin ECC
as a **development** dependency:

```sh
npm init -y
npm install --save-dev ecc-universal@2.2.3
```

Review the generated `package.json` and `package-lock.json`. Then preview the
Copilot install using the locally installed CLI:

```sh
npx ecc-universal install --target copilot --skills python-patterns,python-testing,tdd-workflow,verification-loop --dry-run
```

After reviewing the plan, apply it by removing `--dry-run`:

```sh
npx ecc-universal install --target copilot --skills python-patterns,python-testing,tdd-workflow,verification-loop
```

The dependency pins the installer version; the installer writes harness-native
files into the repository. The generated ECC files—not JavaScript imports—are
what Copilot CLI consumes. Keep the lockfile and ECC-managed install state
alongside the generated files if the installer creates them. Do not hand-edit
generated files unless ECC's documentation says that file is user-owned.

### Option 3: Install from a reviewed ECC source checkout

Use this when you need an unreleased change or want to inspect the exact source
before installation:

```sh
git clone https://github.com/affaan-m/ECC.git
cd ECC
./install.sh --target copilot --skills python-patterns,python-testing,tdd-workflow,verification-loop --dry-run
```

Review the output, then run the same command without `--dry-run`. For a
repeatable team setup, pin the checkout to a reviewed tag or commit and record
that version/commit in the repository documentation. Do not install from an
unofficial mirror.

### Check the result

Review all generated and modified files before committing:

```sh
git status --short
git diff --stat
git diff -- .github
```

For Copilot CLI, use its skill and agent listing commands (for example,
`copilot skill list`) and verify that the intended ECC entries are discovered.
Discovery and displayed names can vary with the installed Copilot CLI version.
Run the repository's existing tests too:

```sh
python -m unittest discover -s repo-trend-tracker/tests -v
python -m py_compile repo-trend-tracker/track_and_notify.py
git diff --check
```

Do not claim ECC hooks are active for the Copilot target: ECC documents that the
target installs skills and agents and does not configure ECC hooks.

## Keep the normal and ECC workflows distinguishable

VS Code exposes prompt files by their filename. Reusing the same prompt name
for two workflows makes it unclear which instructions a human selected. Keep
the existing prompt names for the repository's normal workflow and use an
explicit ECC prefix for ECC-specific adaptations:

```text
.github/prompts/
  plan.prompt.md          # /plan: repository's normal planning prompt
  tdd.prompt.md           # /tdd: repository's normal TDD prompt
  ecc-plan.prompt.md      # /ecc-plan: ECC plan workflow adapted for Copilot Chat
  ecc-tdd.prompt.md       # /ecc-tdd: ECC TDD workflow adapted for Copilot Chat
```

Apply the same convention to review and verification prompts if both versions
are kept. Document the distinction in `.github/copilot-instructions.md` and
the README. For example:

| Command | Meaning |
|---|---|
| `/plan` | Repository's existing, concise plan and approval flow |
| `/ecc-plan` | ECC-derived planning workflow, with the ECC-specific structure and evidence requested |

An ECC-derived Chat prompt is still an adaptation: link to the exact upstream
ECC file and version/commit it was based on, identify the portions adapted, and
state which native ECC features it cannot invoke. Do not copy an entire upstream
command and call it a runtime dependency.

## Human and agent implementation checklist

When implementing the real installation in a future change:

1. Confirm the intended surface: Copilot CLI, VS Code Copilot Chat, or both.
2. Create a separate branch and decide whether the npm CLI is a pinned
   development dependency or a one-time version-pinned `npx` tool.
3. Check current upstream ECC install instructions and supported capabilities.
4. Preview the smallest appropriate install; inspect every destination and
   collision before applying it.
5. Preserve normal prompt names and add explicitly named ECC variants such as
   `/ecc-plan`; do not silently replace the normal command.
6. Commit only the generated ECC files and minimal manifest/docs needed for the
   selected integration. Do not add the entire ECC repository or all
   languages/skills without a stated need.
7. Verify Copilot CLI discovery separately from VS Code prompt discovery.
8. Test the Python project and review the complete diff.
9. Document the ECC version, install/update command, supported surface, known
   limitations, and human approval requirements.

### Dependency and runtime boundaries

- `ecc-universal` is a Node.js CLI package. In this Python repository, it
  belongs in `devDependencies` only if maintainers choose to keep it installed
  for repeatable ECC generation.
- The Python tracker must not import or depend on ECC to run.
- Generated `.github/skills/` and `.github/agents/` files are harness inputs;
  they do not become Python application code.
- A pinned package/lockfile improves repeatability but does not replace review
  of generated changes or upstream release/security review.
- ECC installation does not remove the need for human review, tests, and
  permission controls. Prompt instructions are not an enforcement boundary.

## Effort estimate for a future implementation

These are engineering effort estimates, not a timer or guarantee:

| Scope | Estimate | Includes |
|---|---:|---|
| Focused Copilot CLI install, no npm manifest | 20–40 minutes | Review version, dry run, install selected skills/agents, inspect diff and validate |
| Focused install plus pinned npm dev dependency and docs | 35–60 minutes | Above, plus Node manifest/lockfile and contributor setup instructions |
| Full ECC catalog and all repository workflows | 1–3 hours or more | Larger generated diff, conflict review, capability checks, and broader validation |

Actual time depends on the selected ECC release, install plan size, conflicts,
and whether generated artifacts need adaptation. A small prompt-only adaptation
is faster, but is not equivalent to a full ECC installation.

## Official references

- [ECC source repository and current installation guide](https://github.com/affaan-m/ECC)
- [ECC npm package: `ecc-universal`](https://www.npmjs.com/package/ecc-universal)
- [ECC README: GitHub Copilot support](https://github.com/affaan-m/ECC#github-copilot-support-in-depth)
- [VS Code prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

Always re-check these sources before implementation. ECC's release version,
installer behavior, and harness support can change.
