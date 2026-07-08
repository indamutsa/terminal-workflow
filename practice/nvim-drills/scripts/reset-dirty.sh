#!/usr/bin/env bash
# Resets the practice repo to a known "dirty" state: two unstaged hunks in
# tracked files, plus one untracked file. Safe to re-run any time.
set -euo pipefail
cd "$(dirname "$0")/.."

git checkout -- src/calculator.py src/orders.py
git apply scripts/dirty.patch
cp scripts/scratch.py.template src/scratch.py

echo "Reset to dirty state:"
git status --short
