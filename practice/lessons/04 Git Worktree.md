---
up:
  - "[[Learning Map]]"
related:
  - "[[Bash]]"
  - "[[fzf]]"
  - "[[Git Worktree]]"
created: 2026-06-27
in:
  - "[[Library Map]]"
tags:
  - terminal
  - neovim
  - tmux
  - workflow
  - library
---

# Lesson 4: Git Worktree — Parallel Branches

Check out multiple branches simultaneously in separate directories. No stashing, no context-switching.

---

## The problem worktrees solve

```bash
# Without worktrees (painful):
git stash
git checkout other-branch
# do work...
git checkout original-branch
git stash pop              # hope nothing conflicts

# With worktrees (instant):
# main branch → ~/projects/myapp/
# feature branch → ~/projects/myapp-feature/
# Both exist simultaneously. No stashing. No switching.
```

---

## Exercise 4.1: Create your first worktree

```bash
# You're in your project on main branch
cd ~/projects/myapp

# Create a worktree for a new feature
git worktree add ../myapp-payments -b feature/payments

# What this does:
#   ../myapp-payments/  ← new directory, checked out on feature/payments
#   -b feature/payments ← creates the branch from current HEAD

# Verify:
git worktree list
# /Users/you/projects/myapp            abc1234 [main]
# /Users/you/projects/myapp-payments   abc1234 [feature/payments]
```

Two directories. Two branches. Both fully functional. Same git history — no cloning, no disk waste.

---

## Exercise 4.2: Work in the worktree

```bash
cd ../myapp-payments
ls                        # same files, but this is the feature branch
git branch                # confirms: feature/payments
```

Make changes here — they only affect `feature/payments`. Main in `../myapp/` stays untouched.

---

## Exercise 4.3: Different base branches

```bash
# Branch off main (even if you're currently on another branch):
git worktree add ../myapp-auth -b feature/auth main

# Branch off a specific commit:
git worktree add ../myapp-fix -b hotfix/urgent abc1234

# Check out an existing remote branch:
git worktree add ../myapp-review origin/feature/someone-elses-pr
```

---

## Exercise 4.4: tmux + worktrees

Each worktree gets its own tmux window. Switch branches with `Ctrl-a 0`, `Ctrl-a 1`:

```bash
# Window 0: main (you're here)

# Window 1: feature worktree
Ctrl-a c
cd ../myapp-payments
nvim .

# Now:
# Ctrl-a 0 = main branch
# Ctrl-a 1 = feature branch
```

No git stash, no waiting, no risk. Millisecond branch switching.

---

## Exercise 4.5: Multiple features in parallel

```bash
git worktree add ../myapp-auth -b feature/auth main
git worktree add ../myapp-hotfix -b hotfix/urgent-fix main

# 4 tmux windows:
# 0: main
# 1: feature/payments
# 2: feature/auth
# 3: hotfix/urgent-fix

# Run tests on two branches at the same time. Compare performance. Zero friction.
```

---

## Exercise 4.6: Clean up

```bash
# After feature is merged:
git worktree remove ../myapp-payments
git branch -d feature/payments

# If you deleted the directory manually:
git worktree prune

# See what's left:
git worktree list
```

---

## Exercise 4.7: Real workflow

```bash
# 1. Start feature
git worktree add ../myapp-payments -b feature/payments main

# 2. Work in it (separate tmux window)
cd ../myapp-payments
# ... make changes, commit ...

# 3. Push and PR
git push -u origin feature/payments
gh pr create --title "Add payments"

# 4. While waiting for review, start next feature
cd ../myapp
git worktree add ../myapp-auth -b feature/auth main

# 5. After PR merged, clean up
git worktree remove ../myapp-payments
git branch -d feature/payments
```

---

## Helper aliases (add to ~/.zshrc)

```bash
# Create worktree + open in new tmux window
gwa() {
  local branch="$1"
  local base="${2:-HEAD}"
  local dir="../$(basename $(pwd))-$(echo $branch | tr '/' '-')"
  git worktree add "$dir" -b "$branch" "$base" && \
  tmux new-window -n "$(echo $branch | sed 's/.*\///')" -c "$dir"
}

# Remove worktree
gwr() {
  git worktree remove "$1" && echo "Removed: $1"
}

# List worktrees
alias gwl='git worktree list'
```

Usage:
```bash
gwa feature/auth            # worktree from HEAD + new tmux window
gwa feature/auth main       # worktree from main + new tmux window
gwl                         # list all
gwr ../myapp-feature-auth   # clean up
```

---

## Directory layout

```
~/projects/
├── my-service/              ← main worktree (main branch)
├── my-service-feature-auth/ ← worktree (feature/auth)
├── my-service-hotfix-123/   ← worktree (hotfix/123)
└── my-service-refactor-db/  ← worktree (refactor/db)
```

Each directory: fully functional checkout with its own `node_modules`, `.venv`, build cache. They share the same `.git` object store.

---

## Key commands

| Command | What it does |
|---------|-------------|
| `git worktree add ../dir -b branch` | Create worktree + new branch |
| `git worktree add ../dir -b branch base` | Create from specific base |
| `git worktree add ../dir existing-branch` | Checkout existing branch |
| `git worktree list` | List all worktrees |
| `git worktree remove ../dir` | Remove a worktree |
| `git worktree prune` | Clean up stale entries |

---

Back to: [[Library Map]] | [[Learning Map]]
