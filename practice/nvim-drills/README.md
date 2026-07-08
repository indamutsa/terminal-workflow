# nvim-drills

Throwaway Python project used by the Terminal Workflow lessons (02, 03, 06, 07).
Everything in here is intentionally imperfect — bad names, an off-by-one bug, an
unused import, a failing test — so there's always something real to fix.

## Setup (once)

```bash
cd "nvim-drills"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then `<Space>cv` inside nvim to point it at `.venv`.

## Resetting between drills

Some exercises (Lesson 6 git/gitsigns drills) want uncommitted changes to
stage, diff, and discard. Run this before those sections:

```bash
./scripts/reset-dirty.sh
```

It discards any edits you made, reapplies a fixed patch (`scripts/dirty.patch`)
on top of the last commit, and drops one new untracked file
(`src/scratch.py`) — giving you real unstaged hunks and an untracked file to
practice on. Safe to run as many times as you want.

## Running things

```bash
pytest                  # two tests fail on purpose — see Lesson 6 (neotest + DAP)
python -m src.report    # prints the order report
ruff check .            # two lint findings on purpose — see Lesson 6 (diagnostics)
```
