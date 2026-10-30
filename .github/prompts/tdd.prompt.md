---
agent: agent
description: Implement user-approved behavior with a RED, GREEN, IMPROVE test cycle
---

# Test-driven development

First confirm that the user explicitly approved the acceptance criteria for this change.
If approval or criteria are missing, stop and ask for them; do not edit files.

For each approved behavior:

1. **RED:** Add the smallest behavior-focused test and run it. Show that it fails for
   the expected reason.
2. **GREEN:** Make the smallest production change that satisfies the test, then rerun
   the test and show that it passes.
3. **IMPROVE:** Refactor only where it improves clarity without changing behavior;
   rerun the relevant tests.

Use the existing test framework and mock external APIs. Do not claim a coverage
percentage unless it was measured. Keep edits within the approved criteria and report
the commands and results.
