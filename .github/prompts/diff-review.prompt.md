---
agent: agent
description: Review the current diff for correctness and regressions without editing
---

# Read-only change review

Review the current diff against the user's request and approved acceptance criteria.
Do not modify files.

Check for:

- behavior gaps, boundary conditions, and backward compatibility;
- missing or misleading tests and documentation;
- unintended changes to generated state, secrets, workflow permissions, or external
  side effects;
- whether the reported verification actually covers the change.

Report only actionable findings, ordered by severity, with file and line references.
If there are no findings, say so and distinguish that from checks that were not run.
