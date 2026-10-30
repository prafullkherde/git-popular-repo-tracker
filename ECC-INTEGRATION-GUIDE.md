# ECC Integration Guide

This repository has been enhanced with **Everything Claude Code (ECC)** patterns and conventions. This guide explains what changed and how to use the new workflow.

## Overview

Previously, this repository had basic prompt files for `/plan`, `/tdd`, `/diff-review`, and `/verify`. These were generic and not aligned with ECC methodologies. Now they are:

✅ **ECC-integrated** - Follow patterns from the full ECC framework  
✅ **Fully documented** - Each command includes clear usage instructions  
✅ **Workflow-aware** - Commands chain together in a structured approval process  
✅ **Repository-tuned** - Customized for Python + unittest testing  

## What is ECC?

**ECC (Everything Claude Code)** is a comprehensive framework for AI-assisted software development featuring:

- **Skills**: Reusable, composable code components
- **Hooks**: Integration points for workflows
- **Rules**: Best practices and validation patterns
- **Commands**: Standardized operations with clear semantics
- **MCP Conventions**: Multi-model compatibility

**Reference**: https://github.com/affaan-m/ecc

## Integrated Commands

### 1. `/plan` - Planning Command
**File**: `.github/prompts/plan.prompt.md`

Creates structured implementation plans before writing any code.

#### Normal vs. ECC Version

| Aspect | Normal | ECC Edition |
|---|---|---|
| **Structure** | Basic steps | Phases with risk assessment |
| **Grounding** | Generic patterns | ECC skills/hooks/rules references |
| **Approval** | Simple confirmation | Clear acceptance criteria template |
| **Output** | Inline only | Can generate `.claude/plans/` artifacts |
| **Integration** | Standalone | Chains to `/tdd` → `/diff-review` → `/verify` |

#### Usage

```bash
# Plan a feature (conversational mode)
/plan Add multi-language dashboard support

# Plan from a PRD (artifact mode)
/plan docs/features/notifications.prd.md

# Plan from reference documentation
/plan repo-trend-tracker/requirements.md
```

#### Expected Output

You'll see:
1. **Requirements Restatement** - Clear, unambiguous description
2. **Implementation Phases** - Numbered steps with dependencies
3. **ECC Patterns to Mirror** - Specific examples from the codebase
4. **Risks & Mitigation** - Known issues and solutions
5. **Acceptance Criteria** - Measurable definition of "done"

**Key Difference**: ECC version explicitly references patterns to mirror from the repository, ensuring consistency with existing code style and architecture.

---

### 2. `/tdd` - Test-Driven Development
**File**: `.github/prompts/tdd.prompt.md`

Implement features by writing tests first, then minimal code to pass them.

#### Normal vs. ECC Version

| Aspect | Normal | ECC Edition |
|---|---|---|
| **Flow** | Generic cycle | Arrange-Act-Assert pattern |
| **Test Quality** | Basic examples | ECC best practices (descriptive names, boundary cases) |
| **Integration** | Isolated | References `/plan` approval automatically |
| **Approval Gates** | Manual confirmation | Explicit stops after each test passes |
| **Documentation** | Minimal | Links to ECC testing rules |

#### Usage

```bash
# After `/plan` approval:
/tdd
```

#### Expected Flow

1. **Failing Test** - Assistant writes test capturing requirements
2. **Show Failure** - Run test and show `❌ FAIL` output
3. **Implementation** - Write minimal code to pass test
4. **Show Pass** - Run test again and show `✅ PASS` output
5. **Repeat** - Loop through each acceptance criterion

**Key Difference**: ECC version enforces one assertion per test, requires descriptive test names, and stops for confirmation after each test passes. No proceeding to the next test without explicit approval.

---

### 3. `/diff-review` - Code Review
**File**: `.github/prompts/diff-review.prompt.md`

Inspect changes in read-only mode before committing.

#### Normal vs. ECC Version

| Aspect | Normal | ECC Edition |
|---|---|---|
| **Scope** | Show diff | Compare against approved plan + check ECC patterns |
| **Checks** | Syntax | Completeness, scope, pattern adherence, test coverage, hygiene, risks |
| **Output** | Raw diff | Structured review against plan phases |
| **Integration** | Standalone | References `/plan` and `/tdd` outputs |
| **Modifications** | May suggest | Read-only; must request explicit changes |

#### Usage

```bash
# After `/tdd` complete:
/diff-review
```

#### Expected Output

```
# Diff Review: [Feature Name]

## Files Changed
- path/file.py - Modified (X additions, Y deletions)

## Against Plan
✅ Phase 1 (X): Complete
  - Change 1
  - Change 2

## Issues Found
⚠️ MEDIUM: Description
   File: path:line

## Status: ✅ READY FOR VERIFY
```

**Key Difference**: ECC version explicitly maps changes to plan phases and checks for ECC pattern alignment. Confirms readiness before `/verify`.

---

### 4. `/verify` - Final Validation
**File**: `.github/prompts/verify.prompt.md`

Run the complete validation suite before creating a PR.

#### Normal vs. ECC Version

| Aspect | Normal | ECC Edition |
|---|---|---|
| **Scope** | Run tests | Tests + syntax + config + acceptance criteria |
| **Checks** | Test pass/fail | Full checklist with evidence for each item |
| **Gating** | Informational | Hard gate: don't proceed to `/pr` if any fails |
| **Output** | Test output | Structured report with criteria matrix |
| **Integration** | Optional | Required before `/pr` |

#### Usage

```bash
# After `/diff-review` confirms readiness:
/verify
```

#### Expected Output

```
# Verification Report

## Test Suite Results
✅ PASS: Ran X tests in Y.XXXs - OK

## Syntax Validation
✅ PASS: Python syntax check

## Configuration Validation
✅ PASS: All JSON files valid

## Acceptance Criteria Verification
✅ PASS: All X criteria met
   ✅ Criterion 1
   ✅ Criterion 2

## Final Status: ✅ READY FOR PR
```

**Key Difference**: ECC version includes structured acceptance criteria checklist and explicitly gates the PR step until all validations pass.

---

## Workflow Chain

The ECC-integrated commands form a complete workflow:

```
START
  ↓
/plan (Conversational or PRD-driven planning)
  ↓
  User approves acceptance criteria
  ↓
/tdd (Test-driven implementation)
  ↓
  All acceptance criteria have passing tests
  ↓
/diff-review (Inspect diff against plan)
  ↓
  Review confirms readiness
  ↓
/verify (Run validation suite)
  ↓
  All checks pass
  ↓
/pr (Create pull request)
  ↓
END
```

### Key Rules

1. **Approval Gates**: Each step requires explicit user approval before proceeding
2. **No Skipping**: Each command references previous outputs (cannot jump steps)
3. **Tests First**: `/tdd` writes failing tests before implementation
4. **Read-Only Review**: `/diff-review` reviews but doesn't modify
5. **Hard Validation**: `/verify` must pass before PR can be created

---

## How This Differs from Normal `/plan`, `/tdd`, etc.

### Before (Basic Commands)

```markdown
# Basic /plan

Do these:
1. Inspect code
2. Propose changes
3. Wait for approval
```

**Limitations**:
- No structured output format
- No pattern grounding
- Minimal approval gating
- Standalone, not integrated

### After (ECC-Integrated Commands)

```markdown
# ECC /plan

## Requirements Restatement
[Clear requirement]

## Implementation Phases
### Phase 1: [name]
- [step]

## ECC Patterns to Mirror
| Category | Source | Application |
|---|---|---|
| [pattern] | ecc/path:line | [how we apply] |

## Acceptance Criteria
- [ ] [measurable criteria]

**STATUS: AWAITING APPROVAL**
Confirm with: "yes", "proceed", or "approved"
```

**Advantages**:
- Structured, machine-readable format
- References ECC patterns explicitly
- Clear approval language
- Integrates with other commands
- Measurable acceptance criteria

---

## Integration with ECC Dependencies

This repository can reference ECC patterns from https://github.com/affaan-m/ecc:

- **Skills**: Reference ECC skill structure in `/plan`
- **Hooks**: Understand ECC workflow hooks when planning integrations
- **Rules**: Follow ECC rules for testing, validation, and code style
- **Commands**: Learn from ECC command patterns and semantics
- **MCP**: Leverage ECC MCP configurations for multi-model workflows

Example in `/plan` output:

```
## ECC Patterns to Mirror
| Category | Source | Application |
|---|---|---|
| Skill Structure | `ecc/skills/core.md` | New skills follow ECC export pattern |
| Hook Pattern | `ecc/hooks/workflow.md` | Integration hooks use ECC naming |
| Test Pattern | `ecc/rules/testing-rules.md` | Tests follow Arrange-Act-Assert |
```

---

## Human Approval Gates

These commands respect explicit approval gates:

### `/plan` Gate

```
USER: /plan Add real-time notifications

COPILOT: [Structured plan with acceptance criteria]

**STATUS: AWAITING YOUR APPROVAL**
Confirm with: "yes", "proceed", "approved"
  OR request changes: "modify: [changes]", "different approach: [alt]"
```

### `/tdd` Gate

```
COPILOT: [Test fails] ❌ 
COPILOT: [Test passes] ✅

**STATUS: AWAITING YOUR APPROVAL**
Ready for next test? (yes/next test/diff-review)
```

### `/diff-review` Gate

```
COPILOT: [Review output]

## Status: ✅ READY FOR VERIFY
Proceed? (yes/verify/make changes)
```

### `/verify` Gate

```
COPILOT: [Verification report]

## Final Status: ✅ READY FOR PR
Proceed to `/pr`? (yes/pr/review)
```

---

## Running the Commands

### In GitHub Copilot Chat (VS Code)

```
User types: /plan
Copilot responds: [Plan output]
User approves: yes
User types: /tdd
Copilot responds: [Test cycle]
... (repeat for each command)
```

### Command Syntax

```bash
# Conversational planning
/plan Build a dashboard widget

# PRD-driven planning
/plan docs/requirements.prd.md

# Testing (after plan approval)
/tdd

# Review changes
/diff-review

# Final validation
/verify

# Create PR (after verify passes)
/pr Add dashboard widget support
```

---

## Directory Structure

```
repository/
├── .github/
│   ├── prompts/
│   │   ├── plan.prompt.md         ← ECC-integrated plan
│   │   ├── tdd.prompt.md          ← ECC-integrated TDD
│   │   ├── diff-review.prompt.md  ← ECC-integrated review
│   │   └── verify.prompt.md       ← ECC-integrated verify
│   └── copilot-instructions.md    ← Repository instructions
├── .claude/
│   ├── plans/                     ← Generated by /plan
│   │   └── feature-name.plan.md
│   └── prds/                      ← PRD artifacts
│       └── feature-name.prd.md
└── ECC-INTEGRATION-GUIDE.md        ← This file
```

---

## Quick Reference

### Command Chaining Sequence

| Step | Command | Wait For | Output |
|---|---|---|---|
| 1 | `/plan feature` | User approval | Acceptance criteria |
| 2 | `/tdd` | Each test pass | Failing → Passing tests |
| 3 | `/diff-review` | Review confirmation | Diff against plan |
| 4 | `/verify` | All checks pass | Validation report |
| 5 | `/pr message` | PR created | GitHub PR link |

### Approval Language

```
✅ Approval words: "yes", "proceed", "approved", "ready", "confirmed"
❌ Rejection words: "no", "modify", "different", "skip", "revise"
```

### When to Use Each Command

| Scenario | Command | When |
|---|---|---|
| Starting feature | `/plan` | Before any code |
| Have requirements clear | `/plan` + approve | Immediate to `/tdd` |
| Unclear requirements | `/plan` + modify | Loop until approved |
| Code written, needs review | `/diff-review` | After implementation |
| Ready to commit | `/verify` | After review passes |
| Creating PR | `/pr` | After verify passes |

---

## Troubleshooting

### "I don't see structured output"

The assistant might be using generic `/plan`. Make sure the `.github/prompts/` files are in place and ensure you're in Copilot Chat (not Claude web interface).

### "Tests are passing but `/verify` says failures"

Check that all acceptance criteria from `/plan` have corresponding tests. `/verify` gates on both test pass AND acceptance criteria checklist.

### "Can I skip `/diff-review`?"

Not recommended. `/diff-review` catches scope creep and pattern mismatches that `/tdd` might miss. It's the human approval gate before final validation.

### "What if `/verify` fails?"

Fix the issue, re-run the failing test with `/tdd`, re-review with `/diff-review`, then re-run `/verify`. Do not proceed to `/pr` until all checks pass.

---

## References

- **ECC Repository**: https://github.com/affaan-m/ecc
- **Original Commands**: `.github/prompts/` (archived versions available in git history)
- **Repository Instructions**: `.github/copilot-instructions.md`
- **ECC How-To**: `ecc-how-to-use.md`

---

## Summary

The ECC-integrated commands provide:

✅ **Structured workflow** - Clear chain from plan → test → review → validate  
✅ **Approval gates** - Explicit confirmation before each step  
✅ **Pattern grounding** - References to ECC conventions  
✅ **Measurable criteria** - Acceptance checklist for "done"  
✅ **Integrated validation** - Hard gates before PR creation  

This ensures consistent, high-quality code changes aligned with ECC best practices while maintaining human control through explicit approval gates.

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Ready for use
