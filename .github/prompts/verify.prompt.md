---
agent: agent
description: Run the repository's focused verification and report exact evidence
---

# Project verification

Inspect the diff and choose the smallest complete checks for the changed behavior.
For tracker changes, run:

```sh
python -m unittest discover -s repo-trend-tracker/tests -v
python -m py_compile repo-trend-tracker/track_and_notify.py
git diff --check
```

Do not run the live tracker or workflow unless the user explicitly asks. Report each
command and whether it passed; include failures and unverified checks plainly. Do not
make code changes as part of this verification prompt.
