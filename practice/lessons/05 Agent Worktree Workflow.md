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

# Lesson 5: Feature Development with an AI Coding Agent + Git Worktree + tmux

The full workflow: worktree for isolation, tmux for windows, an AI coding agent as a parallel coding partner.

---

## The 3-window pattern

```
┌──────────────────────────────────────────────────────────┐
│ tmux session                                              │
├────────────┬─────────────────────┬───────────────────────┤
│ Window 0   │ Window 1            │ Window 2              │
│ main       │ feature/payments    │ feature/payments      │
│            │                     │                       │
│ PR reviews │ YOU: nvim           │ AGENT: coding agent   │
│ releases   │ write tests         │ generates code        │
│ rebases    │ review changes      │ refactors             │
│            │ manual testing      │ fixes lint issues     │
└────────────┴─────────────────────┴───────────────────────┘
```

---

## Exercise 5.1: Create the workspace

```bash
# Start in your project on main
cd ~/projects/my-service

# Create the feature worktree
git worktree add ../my-service-payments -b feature/payments main

# Window 0: main (you're here already)

# Window 1: your editor on the feature branch
Ctrl-a c
cd ../my-service-payments
nvim .

# Window 2: your AI coding agent on the same feature branch
Ctrl-a c
cd ../my-service-payments
<agent>                         # your agent's CLI command
```

---

## Exercise 5.2: Give the agent a task

Switch to Window 2 (`Ctrl-a 2`), type:

```
Add a POST /payments endpoint. Validate the request body (amount, currency,
customer_id required). Call Stripe to create a payment intent. Return the
client_secret. Follow the patterns in src/routes/orders.ts.
```

Don't wait for the agent to finish — switch to your editor.

---

## Exercise 5.3: Work in parallel

While the agent writes the implementation, you write tests:

```
Ctrl-a 1                        # switch to Window 1 (editor)
<Space>sf                       # find/create tests/payments.test.ts
i                               # start writing tests
```

You and the agent edit the **same branch** in **different terminals**. No conflicts — you're on different files.

---

## Exercise 5.4: Review the agent's work

```
Ctrl-a 1                        # your editor window
```

In Neovim:
```
<Space>sg                       # grep for "payments" — see all new files
<Space>gd                       # diffview — all changes side-by-side
```

Or from terminal (`Ctrl-\`):
```bash
git diff --stat                 # quick overview
git diff src/routes/payments.ts # inspect the agent's file
```

---

## Exercise 5.5: Run tests

In Neovim terminal (`Ctrl-\` or `<Space>1`):

```bash
npm test -- --grep payments     # or pytest tests/payments/ -v
```

If something fails, tell the agent (Window 2):

```
The test for invalid currency is failing — the endpoint returns 200 instead
of 400 when currency is not one of [usd, eur, gbp]. Fix the validation.
```

---

## Exercise 5.6: Meanwhile, back on main

```
Ctrl-a 0                        # Window 0 = main branch, untouched
```

You can:
- Review someone else's PR: `gh pr checkout 789`
- Pull latest: `git pull`
- Start a hotfix: `gwa hotfix/fix-typo`

Main never gets dirty.

---

## Exercise 5.7: Commit, push, PR

```bash
# In Window 1 or terminal on feature branch:
git add -A
git status                      # review what's staged
git commit -m "Add payments endpoint with Stripe integration"
git push -u origin feature/payments
gh pr create --title "Add /payments endpoint" \
  --body "POST /payments with Stripe. Validates amount/currency/customer_id."
```

---

## Exercise 5.8: Clean up after merge

```bash
Ctrl-a 0                                    # switch to main
git pull                                    # get the merge
git worktree remove ../my-service-payments  # remove worktree
git branch -d feature/payments              # delete local branch

# Close tmux windows:
Ctrl-a 1
exit
Ctrl-a 1
exit
```

---

## Pro tips

1. **The agent can edit freely** — it's in its own worktree, can't mess up your editor session
2. **Test both branches** — run benchmarks on main and feature side by side
3. **Multiple features** — 3 features = 3 worktrees = 3 tmux windows
4. **Rebase without fear** — rebase feature worktree while main stays clean
5. **Name your windows** — `Ctrl-a ,` then type `editor` / `agent` / `tests`

---

## The daily loop

```
1. gwa feature/new-thing          # create worktree + tmux window
2. Ctrl-a c → cd → <agent>       # agent window on same branch
3. Give the agent a task          # it works while you work
4. Ctrl-a 1 → nvim .             # you code in parallel
5. Review, test, iterate          # Ctrl-a 0/1/2 to switch
6. Commit, push, PR              # from terminal
7. gwr ../dir                    # clean up after merge
```

---

Back to: [[Library Map]] | [[Learning Map]]
