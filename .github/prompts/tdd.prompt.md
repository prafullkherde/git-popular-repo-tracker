---
description: "ECC Test-Driven Development: Write failing test first, then implement to pass it. Minimal changes, maximum clarity."
source: ecc/commands/feature-dev.md
---

# TDD Command (ECC Edition)

Implement features using test-driven development (TDD) discipline: write the test first, watch it fail, then implement the minimal code to pass it.

**Prerequisites**: Use `/plan` first and wait for approval before running `/tdd`.

## What This Command Does

1. **Writes Failing Test** - Create test that captures requirements
2. **Shows Test Failure** - Verify test fails with clear error message
3. **Implements Minimal Code** - Write smallest change to pass test
4. **Verifies Pass** - Run test again and confirm it passes
5. **Repeats as Needed** - Continue for each acceptance criterion

## How to Use

```bash
/tdd
```

The assistant will:
1. Reference the most recent `/plan` approval
2. Ask which acceptance criterion to test first (if multiple exist)
3. Write a failing test file
4. Show test failure output
5. Implement code to pass the test
6. Show test passing
7. Repeat or wait for your next instruction

## TDD Workflow

### Step 1: Failing Test
```python
def test_minimum_stars_filter_excludes_below_threshold(self):
    """New repos below minimum_stars should not be tracked."""
    config = {"minimum_stars": 50}
    repo = {"name": "test-repo", "stars": 30}
    assert not should_track_repo(repo, config)
```

**Run**: `python -m unittest repo-trend-tracker/tests/test_track_and_notify.py::TestWatchlistFilter::test_minimum_stars_filter_excludes_below_threshold`

**Expected**: ❌ FAIL (test_minimum_stars_filter_excludes_below_threshold ... FAIL)

### Step 2: Implementation
```python
def should_track_repo(repo, config):
    minimum = config.get("minimum_stars", 0)
    return repo["stars"] >= minimum
```

### Step 3: Passing Test
**Run**: Same command again

**Expected**: ✅ PASS (test_minimum_stars_filter_excludes_below_threshold ... ok)

## Testing Best Practices (from ECC)

Follow these patterns:

| Pattern | Applied | Example |
|---|---|---|
| **Arrange-Act-Assert** | Setup → Execute → Verify | `config = {...}` → `result = track(...)` → `assert result == True` |
| **One assertion per test** | Test one behavior | ✅ Test threshold boundary ❌ Test multiple filters |
| **Descriptive test names** | Name tells what's tested | ✅ `test_minimum_stars_excludes_below` ❌ `test_filter` |
| **No live side effects** | Mock external calls | ✅ Mock GitHub API ❌ Call live API |
| **Boundary cases** | Test edges | Test value at threshold, below, and above |

## Commands Reference

### Run All Tests
```bash
python -m unittest discover -s repo-trend-tracker/tests -v
```

### Run Single Test File
```bash
python -m unittest repo-trend-tracker.tests.test_track_and_notify -v
```

### Run Single Test
```bash
python -m unittest repo-trend-tracker.tests.test_track_and_notify.TestClass.test_method -v
```

### Check Syntax
```bash
python -m py_compile repo-trend-tracker/track_and_notify.py
```

## Approval Gates

⚠️ **IMPORTANT**: 
- Stop after each test passes
- Wait for you to confirm the next test or acceptance criterion
- Do not proceed to implementation for the next test until you approve

## After TDD

Once all acceptance criteria have passing tests:

1. Use `/diff-review` to review all changes
2. Use `/verify` to run full validation suite
3. Use `/pr` to create pull request

## Integration with Other Commands

- **`/plan`** - Must run first to define acceptance criteria
- **`/diff-review`** - Review implementation against plan
- **`/verify`** - Final validation before PR
- **`/pr`** - Create pull request with test evidence

## ECC Reference

This is the ECC-integrated TDD workflow. For the full ECC feature development workflow, see `ecc/commands/feature-dev.md`.

Testing patterns follow ECC best practices documented in `ecc/rules/testing-rules.md`.
