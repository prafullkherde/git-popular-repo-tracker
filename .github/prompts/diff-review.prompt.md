---
description: "ECC Diff Review: Read-only inspection of staged/unstaged changes against the accepted plan. No modifications."
source: ecc/commands/code-review.md
---

# Diff Review Command (ECC Edition)

Review staged and unstaged changes in read-only mode. Inspect the diff against the accepted plan and identify any deviations, issues, or concerns before committing.

**Prerequisites**: Use `/plan` and `/tdd` first to establish acceptance criteria and implementation.

## What This Command Does

1. **Shows Current Diff** - Display all staged and unstaged changes
2. **Compares to Plan** - Check that changes match the approved plan
3. **Identifies Issues** - Flag potential bugs, test gaps, or pattern mismatches
4. **Provides Feedback** - Suggest improvements (read-only, no modifications)
5. **Confirms Readiness** - Assess whether changes are ready for `/verify` and `/pr`

## How to Use

```bash
/diff-review
```

The assistant will:
1. Show the current git diff
2. List each changed file with description of changes
3. Compare against the most recent `/plan` approval
4. Flag any deviations or concerns
5. Confirm readiness or suggest modifications before proceeding

## Review Checklist

The diff review will check:

| Aspect | Question | Example |
|---|---|---|
| **Completeness** | Do changes cover all acceptance criteria? | ✅ All phases from plan implemented |
| **Scope** | Are changes in scope or are extras included? | ✅ Only files in plan changed ❌ Extra refactoring added |
| **Patterns** | Do changes follow ECC patterns? | ✅ New skills in `skills/` dir ❌ Random helper files |
| **Tests** | Do changes have corresponding tests? | ✅ Test before each implementation ❌ Code without tests |
| **Hygiene** | Are comments, formatting, and imports clean? | ✅ Clear comments, proper imports ❌ Debug logs left behind |
| **Risks** | Are known risks mitigated? | ✅ Error handling added ❌ Untested edge cases |

## Diff Review Output

You will see output like:

```
# Diff Review: Feature Name

## Files Changed
- `repo-trend-tracker/track_and_notify.py` - Modified (78 additions, 12 deletions)
- `repo-trend-tracker/tests/test_track_and_notify.py` - Modified (42 additions, 0 deletions)

## Against Plan

✅ Phase 1 (Database Filter): Complete
  - Added `should_track_repo()` function as planned
  - Added minimum_stars configuration handling

✅ Phase 2 (Tests): Complete
  - Added test_minimum_stars_filter_excludes_below_threshold
  - Added test_minimum_stars_includes_at_threshold

## Issues Found

⚠️ MEDIUM: Inconsistent docstring format
   File: repo-trend-tracker/track_and_notify.py:45
   Current: """Filter with minimum stars."""
   Suggested: Use `:param:` format consistent with line 12

## Status: ✅ READY FOR VERIFY
Ready to run `/verify` to confirm all checks pass before creating PR.
```

## Diff Review Modes

### Mode 1: Staged Changes Only
```bash
git diff --cached
```

### Mode 2: All Changes (Staged + Unstaged)
```bash
git diff HEAD
```

### Mode 3: Changes Against Branch
```bash
git diff main..HEAD
```

## After Diff Review

If review is ✅ READY:
1. Run `/verify` to perform final validation
2. Run `/pr` to create pull request
3. Push branch and open PR in GitHub

If issues found:
1. Request specific modifications
2. Re-run `/diff-review` after changes
3. Confirm readiness before proceeding

## Integration with Other Commands

- **`/plan`** - Approved plan is the reference
- **`/tdd`** - Implementation to review
- **`/verify`** - Next step after clean review
- **`/pr`** - Final PR creation

## Important Notes

⚠️ **READ-ONLY**: This command reviews only; it does not modify files.

If you see issues:
- Reply with specific file and line number
- Request exact change needed
- `/diff-review` again after modifications

## ECC Reference

This is the ECC-integrated code review workflow. For the full ECC code review patterns, see `ecc/commands/code-review.md` and `ecc/rules/code-style-rules.md`.
