---
description: "ECC Verify: Run validation suite, syntax checks, tests, and final acceptance criteria confirmation."
source: ecc/commands/quality-gate.md
---

# Verify Command (ECC Edition)

Run the complete validation suite to confirm that all changes meet acceptance criteria, pass tests, and are ready for production.

**Prerequisites**: Use `/plan`, `/tdd`, and `/diff-review` before running `/verify`.

## What This Command Does

1. **Runs All Tests** - Execute full test suite to confirm passing
2. **Syntax Checks** - Validate Python code compiles correctly
3. **Acceptance Criteria** - Verify all criteria from `/plan` are met
4. **Configuration Validation** - Check data files and configs are valid JSON
5. **Final Gate** - Confirm readiness for PR and merge

## How to Use

```bash
/verify
```

The assistant will:
1. Run the complete test suite
2. Run syntax checks
3. Verify acceptance criteria from the plan
4. Report all results
5. Confirm readiness for `/pr`

## Validation Steps

### Step 1: Full Test Suite
```bash
python -m unittest discover -s repo-trend-tracker/tests -v
```

**Expected**: All tests pass
```
test_minimum_stars_filter_excludes_below_threshold ... ok
test_minimum_stars_filter_includes_at_threshold ... ok
test_minimum_stars_disabled_with_zero ... ok
...
Ran X tests in Y.XXXs
OK
```

### Step 2: Syntax Check
```bash
python -m py_compile repo-trend-tracker/track_and_notify.py
```

**Expected**: No output (silent success)

### Step 3: Configuration Validation
```bash
python -c "import json; json.load(open('repo-trend-tracker/data/watchlist_seed.json'))"
```

**Expected**: No output (valid JSON)

### Step 4: Data Integrity
```bash
python -c "
import json
data = json.load(open('repo-trend-tracker/data/watchlist_seed.json'))
assert 'minimum_stars' in data or isinstance(data, list)
print('✅ Data format valid')
"
```

## Acceptance Criteria Checklist

Verify command will confirm:

| Criterion | Status | Evidence |
|---|---|---|
| All unit tests pass | ✅ | Test suite runs without failures |
| Code compiles/syntax valid | ✅ | Python syntax check passes |
| Configuration files valid | ✅ | JSON parses correctly |
| Watchlist backwards compatible | ✅ | Legacy array format still works |
| minimum_stars defaults to 0 | ✅ | Default behavior preserved |
| Tests cover boundary cases | ✅ | Tests for threshold and edges |
| No debug code left behind | ✅ | Diff review clean |
| Documentation updated | ✅ | README mentions new feature |

## Verify Output

You will see:

```
# Verification Report

## Test Suite Results
✅ PASS: python -m unittest discover -s repo-trend-tracker/tests -v
   Ran 8 tests in 0.123s
   OK

## Syntax Validation
✅ PASS: python -m py_compile repo-trend-tracker/track_and_notify.py
   No errors

## Configuration Validation
✅ PASS: JSON configuration valid
   watchlist_seed.json: valid
   health.json: valid

## Acceptance Criteria Verification
✅ PASS: All 7 criteria met
   ✅ Minimum stars filter works
   ✅ Legacy array format compatible
   ✅ Threshold boundary cases tested
   ✅ No live API calls in tests
   ✅ Documentation updated

## Final Status: ✅ READY FOR PR
All validations passed. Ready to run `/pr` and create pull request.
```

## When Verify Fails

If any validation fails:

```
❌ FAIL: Test suite failure
   FAILED: test_minimum_stars_filter_edge_case
   AssertionError: -1 stars should raise ValueError

Action Required:
1. Review the failing test output
2. Fix the implementation or test
3. Re-run `/verify` to confirm
4. Do not proceed to `/pr` until all pass
```

Response: Fix the issue and re-run `/verify`

## Integration with Other Commands

- **`/plan`** - Defines acceptance criteria
- **`/tdd`** - Implements to pass tests
- **`/diff-review`** - Confirms code quality
- **`/verify`** - Final validation gate
- **`/pr`** - Create PR (only after `/verify` passes)

## Important Notes

⚠️ **GATING**: Do not proceed to `/pr` if `/verify` fails.

If you want to proceed despite failures:
- Request specific override
- Explicitly accept the risk
- Add note to PR about bypassed checks

## After Verify Passes

✅ Ready to run `/pr`:
```bash
/pr Create PR for ECC-integrated workflow improvements
```

## ECC Reference

This is the ECC-integrated quality gate workflow. For the full ECC validation patterns, see:
- `ecc/commands/quality-gate.md`
- `ecc/rules/testing-rules.md`
- `ecc/rules/validation-rules.md`
