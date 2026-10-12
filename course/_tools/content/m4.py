"""Module 4: Worktrees and the agent loop. Sources: lessons 04 Git Worktree.md, 05 Agent Worktree Workflow.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


WINDOW_NOTE = "The lessons count windows from 0. In your config they start at 1 (`base-index 1`), so your first window is `Ctrl-a 1`."

NO_WORKTREE = C('''
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
''')

FIRST_WORKTREE = C('''
# You're in your project on main branch
cd ~/projects/myapp

# Create a worktree for a new feature
git worktree add ../myapp-payments -b feature/payments

# Verify:
git worktree list
''')

IN_WORKTREE = C('''
cd ../myapp-payments
ls                        # same files, but this is the feature branch
git branch                # confirms: feature/payments
''')

BASE_BRANCHES = C('''
# Branch off main (even if you're currently on another branch):
git worktree add ../myapp-auth -b feature/auth main

# Branch off a specific commit:
git worktree add ../myapp-fix -b hotfix/urgent abc1234

# Check out an existing remote branch:
git worktree add ../myapp-review origin/feature/someone-elses-pr
''')

LAYOUT = C('''
~/projects/
├── my-service/              ← main worktree (main branch)
├── my-service-feature-auth/ ← worktree (feature/auth)
├── my-service-hotfix-123/   ← worktree (hotfix/123)
└── my-service-refactor-db/  ← worktree (refactor/db)
''')

TMUX_WORKTREES = C('''
# Window 0: main (you're here)

# Window 1: feature worktree
Ctrl-a c
cd ../myapp-payments
nvim .

# Now:
# Ctrl-a 0 = main branch
# Ctrl-a 1 = feature branch
''')

PARALLEL = C('''
git worktree add ../myapp-auth -b feature/auth main
git worktree add ../myapp-hotfix -b hotfix/urgent-fix main

# 4 tmux windows:
# 0: main
# 1: feature/payments
# 2: feature/auth
# 3: hotfix/urgent-fix

# Run tests on two branches at the same time. Compare performance. Zero friction.
''')

CLEAN_UP = C('''
# After feature is merged:
git worktree remove ../myapp-payments
git branch -d feature/payments

# If you deleted the directory manually:
git worktree prune

# See what's left:
git worktree list
''')

REAL_WORKFLOW = C('''
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
''')

HELPERS = C(r'''
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
''')

HELPER_USAGE = C('''
gwa feature/auth            # worktree from HEAD + new tmux window
gwa feature/auth main       # worktree from main + new tmux window
gwl                         # list all
gwr ../myapp-feature-auth   # clean up
''')

CREATE_WORKSPACE = C('''
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
''')

AGENT_TASK = C('''
Add a POST /payments endpoint. Validate the request body (amount, currency,
customer_id required). Call Stripe to create a payment intent. Return the
client_secret. Follow the patterns in src/routes/orders.ts.
''')

PARALLEL_KEYS = C('''
Ctrl-a 1                        # switch to Window 1 (editor)
<Space>sf                       # find/create tests/payments.test.ts
i                               # start writing tests
''')

REVIEW_KEYS = C('''
Ctrl-a 1                        # your editor window
''')

REVIEW_NVIM = C('''
<Space>sg                       # grep for "payments" — see all new files
<Space>gd                       # diffview — all changes side-by-side
''')

REVIEW_GIT = C('''
git diff --stat                 # quick overview
git diff src/routes/payments.ts # inspect the agent's file
''')

RUN_TESTS = C('''
npm test -- --grep payments     # or pytest tests/payments/ -v
''')

FIX_PROMPT = C('''
The test for invalid currency is failing — the endpoint returns 200 instead
of 400 when currency is not one of [usd, eur, gbp]. Fix the validation.
''')

BACK_ON_MAIN = C('''
Ctrl-a 0                        # Window 0 = main branch, untouched
''')

SHIP = C('''
# In Window 1 or terminal on feature branch:
git add -A
git status                      # review what's staged
git commit -m "Add payments endpoint with Stripe integration"
git push -u origin feature/payments
gh pr create --title "Add /payments endpoint" \\
  --body "POST /payments with Stripe. Validates amount/currency/customer_id."
''')

AFTER_MERGE = C('''
Ctrl-a 0                                    # switch to main
git pull                                    # get the merge
git worktree remove ../my-service-payments  # remove worktree
git branch -d feature/payments              # delete local branch

# Close tmux windows:
Ctrl-a 1
exit
Ctrl-a 1
exit
''')

DAILY_LOOP = C('''
1. gwa feature/new-thing          # create worktree + tmux window
2. Ctrl-a c → cd → <agent>       # agent window on same branch
3. Give the agent a task          # it works while you work
4. Ctrl-a 1 → nvim .             # you code in parallel
5. Review, test, iterate          # Ctrl-a 0/1/2 to switch
6. Commit, push, PR              # from terminal
7. gwr ../dir                    # clean up after merge
''')

MODULE = {
    "n": 4,
    "folder": "m4-worktrees",
    "title": "Worktrees and the agent loop",
    "footer": "Git worktrees, one tmux window per branch, the three-window pattern with an AI agent, shipping and clean-up",
    "tagline": "One folder per branch, one window per folder, an agent beside you.",
    "glossary": [],
    "coverage_allow": [
        ('local branch="$1"; local base="${2:-HEAD}"', "same gwa body, one statement per line"),
        ('gwr() { git worktree remove "$1" && echo "Removed: $1"; }', "same gwr body, one statement per line"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Parallel branches without stashing",
            "subtitle": "Check out several branches at once, each in its own folder.",
            "idea": (
                "A worktree is another folder on another branch, sharing one git history.",
                [
                    ("Create", "git worktree add ../dir -b branch", "A new folder on a new branch."),
                    ("List", "git worktree list", "Every folder and its branch."),
                    ("Remove", "git worktree remove ../dir", "Deletes the folder."),
                    ("Prune", "git worktree prune", "Clears stale entries."),
                ],
                None,
            ),
            "problem": {
                "fail": "Mid-feature, a hotfix lands. You stash, switch branches, switch back and hope the stash pops cleanly.",
                "fix": "Give each branch its own folder with `git worktree add`. No stashing, no switching.",
            },
            "drills": [
                {
                    "h2": "The problem worktrees solve",
                    "intro": "Compare the painful way with the worktree way.",
                    "blocks": [
                        {"type": "code", "file": "Without worktrees", "title": "Stash and switch, then worktrees", "code": NO_WORKTREE},
                    ],
                },
                {
                    "h2": "Create your first worktree",
                    "intro": "Run this in your project on the main branch. `-b feature/payments` creates the branch from the current HEAD. `../myapp-payments/` is the new directory.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a worktree for a new feature", "code": FIRST_WORKTREE,
                         "expect": "`git worktree list` shows two lines: `/Users/you/projects/myapp` on `[main]` and `/Users/you/projects/myapp-payments` on `[feature/payments]`."},
                        {"type": "text", "body": "Two directories. Two branches. Both fully functional. Same git history: no cloning, no disk waste."},
                    ],
                },
                {
                    "h2": "Work in the worktree",
                    "intro": "Changes here only affect `feature/payments`. Main in `../myapp/` stays untouched.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Step into the new folder", "code": IN_WORKTREE,
                         "expect": "`ls` shows the same files as main. `git branch` confirms `feature/payments`."},
                    ],
                },
                {
                    "h2": "Different base branches",
                    "intro": "Choose where the new branch starts.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Branch off main, a commit or a remote branch", "code": BASE_BRANCHES,
                         "expect": "Each command makes a new folder beside your project: `../myapp-auth`, `../myapp-fix` and `../myapp-review`."},
                    ],
                },
                {
                    "h2": "Directory layout",
                    "intro": "Each directory is a fully functional checkout with its own `node_modules`, `.venv` and build cache. They share the same `.git` object store.",
                    "blocks": [
                        {"type": "code", "file": "~/projects", "title": "Four worktrees side by side", "code": LAYOUT},
                    ],
                },
            ],
            "rules": {
                "h2": "Worktree commands",
                "cards": [
                    ("Key commands", "The six you need.", ["Command", "What it does"], [
                        ["`git worktree add ../dir -b branch`", "Create worktree + new branch"],
                        ["`git worktree add ../dir -b branch base`", "Create from specific base"],
                        ["`git worktree add ../dir existing-branch`", "Checkout existing branch"],
                        ["`git worktree list`", "List all worktrees"],
                        ["`git worktree remove ../dir`", "Remove a worktree"],
                        ["`git worktree prune`", "Clean up stale entries"],
                    ]),
                    ("Worktree card", "The same commands next to your shell aliases.", ["Command", "Action"], [
                        ["`git worktree add ../dir -b branch`", "Create"],
                        ["`git worktree list`", "List"],
                        ["`git worktree remove ../dir`", "Remove"],
                        ["`gwa feature/name`", "Create + tmux window"],
                        ["`gwl`", "List"],
                        ["`gwr ../dir`", "Remove"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Start a feature without touching main",
                "frame": "You begin a payments feature and keep `~/tw` on main exactly as it is.",
                "open": "cd ~/tw && git init -q -b main && git add -A && git commit -qm init",
                "steps": [
                    (None, "`git worktree add ../tw-payments -b feature/payments`", "Makes the folder and the branch."),
                    (None, "`git worktree list`", "Two folders, two branches."),
                    (None, "`cd ../tw-payments` then `git branch`", "Marks `feature/payments` as current. Edit freely: `~/tw` stays on main."),
                    (None, "`cd ../tw` then `git worktree remove ../tw-payments` and `git branch -d feature/payments`", "Removes the folder and the branch."),
                ],
                "after": "/Users/you/tw          3f2a1b9 [main]\n/Users/you/tw-payments 3f2a1b9 [feature/payments]",
                "meaning": "A branch becomes a place you can walk into. Switching branches is a `cd`.",
            },
            "practice": {
                "h2": "Practice: worktrees",
                "qs": [
                    ("Mechanism", "Why is a worktree cheaper than cloning the repo again?",
                     "What is shared?",
                     ["Every worktree shares the same `.git` object store.", "Only the checked-out files are duplicated."],
                     "Same history, no cloning, no disk waste."),
                    ("Keystrokes", "Which command makes `../myapp-auth` on a new branch `feature/auth` from main?",
                     "Add, then `-b`, then a base.",
                     ["Start with `git worktree add`.", "Add the folder `../myapp-auth`.", "Add `-b feature/auth main`."],
                     "`git worktree add ../myapp-auth -b feature/auth main`."),
                    ("Application", "A hotfix is urgent and you are mid-feature. Start it without stashing.",
                     "Branch off a specific commit or main.",
                     ["Run `git worktree add ../myapp-fix -b hotfix/urgent abc1234`.", "`cd ../myapp-fix` and fix it there."],
                     "A second worktree. Your feature folder is untouched."),
                    ("Common mistake", "You deleted a worktree folder by hand. What now?",
                     "Git still remembers it.",
                     ["The entry is stale.", "Run `git worktree prune`."],
                     "`git worktree prune`, then `git worktree list` to check."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Worktrees in tmux",
            "subtitle": "One tmux window per worktree, helper aliases to create and remove them.",
            "idea": (
                "One branch, one folder, one tmux window. Switching branches is one key.",
                [
                    ("New window", "Ctrl-a c", "Then cd into the worktree."),
                    ("Create + window", "gwa feature/auth", "Worktree and tmux window in one go."),
                    ("List", "gwl", "All worktrees."),
                    ("Clean up", "gwr ../dir", "Removes the worktree."),
                ],
                None,
            ),
            "problem": {
                "fail": "You create a worktree, then lose it: no window, no editor, and a long path to retype.",
                "fix": "Give each worktree its own tmux window, and let `gwa` create both in one command.",
            },
            "drills": [
                {
                    "h2": "tmux + worktrees",
                    "intro": "Each worktree gets its own tmux window. No git stash, no waiting, no risk. Millisecond branch switching.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "A window for the feature worktree", "code": TMUX_WORKTREES,
                         "expect": "The feature branch opens in `nvim` in its own window. Switch between main and the feature with one prefix key."},
                        {"type": "text", "body": WINDOW_NOTE},
                    ],
                },
                {
                    "h2": "Multiple features in parallel",
                    "intro": "Run tests on two branches at the same time.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Two more worktrees", "code": PARALLEL,
                         "expect": "You now have four tmux windows' worth of work: main, `feature/payments`, `feature/auth` and `hotfix/urgent-fix`."},
                    ],
                },
                {
                    "h2": "Clean up",
                    "intro": "Remove the worktree and the branch after the feature is merged.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Remove, delete the branch, check", "code": CLEAN_UP,
                         "expect": "`git worktree list` shows what is left: no `myapp-payments`."},
                    ],
                },
                {
                    "h2": "Real workflow",
                    "intro": "The whole cycle, from first worktree to clean-up.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Start, push, PR, next feature, clean up", "code": REAL_WORKFLOW,
                         "expect": "`git push -u origin feature/payments` publishes the branch, and `gh pr create` opens the pull request titled \"Add payments\"."},
                    ],
                },
                {
                    "h2": "Helper aliases (add to ~/.zshrc)",
                    "intro": "`gwa` creates a worktree and opens it in a new tmux window named after the branch.",
                    "blocks": [
                        {"type": "code", "file": "~/.zshrc", "title": "gwa, gwr and gwl", "code": HELPERS},
                        {"type": "cmd", "where": "shell", "title": "Use the helpers", "code": HELPER_USAGE,
                         "expect": "`gwa feature/auth` makes `../myapp-feature-auth` and opens a tmux window named `auth` in it. `gwl` lists every worktree."},
                    ],
                },
            ],
            "rules": {
                "h2": "Aliases at a glance",
                "cards": [
                    ("Helper usage", "Four lines to remember.", None, HELPER_USAGE),
                    ("What gwa builds", "Both names come from the branch.", ["Piece", "Result for `gwa feature/auth`"], [
                        ["Folder", "`../myapp-feature-auth`"],
                        ["Window name", "`auth`"],
                        ["Base", "`HEAD`, or the second argument"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Spin up a feature in one command",
                "frame": "In tmux, with `gwa`, `gwr` and `gwl` in your `~/.zshrc`, you want a feature branch with its own window.",
                "open": "cd ~/tw",
                "steps": [
                    (None, "`gwa feature/auth`", "Makes `../tw-feature-auth` and a tmux window named `auth` in it."),
                    (None, "`nvim .`", "Opens the new folder in that window."),
                    (None, "`gwl`", "Lists every worktree."),
                    (None, "`gwr ../tw-feature-auth`", "After the merge, removes the worktree."),
                ],
                "after": "$ gwl\n/Users/you/tw               3f2a1b9 [main]\n/Users/you/tw-feature-auth 3f2a1b9 [feature/auth]\n$ gwr ../tw-feature-auth\nRemoved: ../tw-feature-auth",
                "meaning": "Two chores become one command, so you actually use a worktree for every feature.",
            },
            "practice": {
                "h2": "Practice: worktrees and tmux",
                "qs": [
                    ("Mechanism", "Why one tmux window per worktree?",
                     "What do you keep apart?",
                     ["Each branch has its own editor, shell and tests.", "Switching is a key, not a checkout."],
                     "Each branch keeps its own state."),
                    ("Keystrokes", "Which command creates a worktree from main and opens a tmux window?",
                     "The helper alias, with a base.",
                     ["Use `gwa`.", "Add the branch, then `main`."],
                     "`gwa feature/auth main`."),
                    ("Application", "Remove `../myapp-feature-auth` after the merge.",
                     "The remove helper.",
                     ["Run `gwr ../myapp-feature-auth`.", "Check with `gwl`."],
                     "`gwr ../myapp-feature-auth`."),
                    ("Common mistake", "You ran `gwa` outside tmux and got an error on the window step. Why?",
                     "What does `gwa` call at the end?",
                     ["`gwa` ends with `tmux new-window`.", "Start or attach tmux first."],
                     "The helper needs tmux. Run `tmux attach` first."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "The three-window pattern",
            "subtitle": "Main, your editor and an AI agent: three windows, one feature branch.",
            "idea": (
                "One worktree, two windows on it: you in one, the agent in the other.",
                [
                    ("Main", "Ctrl-a 0", "PR reviews, releases, rebases."),
                    ("Editor", "Ctrl-a 1", "You: nvim, tests, review."),
                    ("Agent", "Ctrl-a 2", "The coding agent generates code."),
                    ("Workspace", "git worktree add ../my-service-payments -b feature/payments main", "The feature folder."),
                ],
                None,
            ),
            "problem": {
                "fail": "The agent and your editor fight over the same checkout, and half-finished edits land on your main branch.",
                "fix": "Give the feature its own worktree. You and the agent edit the same branch from different terminals.",
            },
            "drills": [
                {
                    "h2": "Create the workspace",
                    "intro": "Window 0 is main. Window 1 is your editor. Window 2 is your AI coding agent, on the same feature branch.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Worktree and two windows", "code": CREATE_WORKSPACE,
                         "expect": "`../my-service-payments` exists on `feature/payments`. Window 1 runs `nvim .` and Window 2 runs your agent, both in that folder."},
                        {"type": "text", "body": WINDOW_NOTE + " Main is `Ctrl-a 1`, the editor `Ctrl-a 2`, the agent `Ctrl-a 3`."},
                    ],
                },
                {
                    "h2": "Give the agent a task",
                    "intro": "Switch to Window 2 (`Ctrl-a 2`) and type the task. Do not wait for the agent to finish: switch to your editor.",
                    "blocks": [
                        {"type": "code", "file": "Prompt to the agent", "title": "The task", "code": AGENT_TASK},
                    ],
                },
                {
                    "h2": "Work in parallel",
                    "intro": "While the agent writes the implementation, you write tests. You and the agent edit the same branch in different terminals. No conflicts: you are on different files.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Switch to the editor and start the tests", "code": PARALLEL_KEYS,
                         "expect": "You are in the editor window, finding or creating `tests/payments.test.ts`, in insert mode."},
                    ],
                },
                {
                    "h2": "Review the agent's work",
                    "intro": "Go to the editor window, then check what the agent changed.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Back to the editor", "code": REVIEW_KEYS,
                         "expect": "You are in your editor window."},
                        {"type": "cmd", "where": "nvim", "title": "In Neovim", "code": REVIEW_NVIM,
                         "expect": "The grep lists every new file mentioning \"payments\". The diff view shows all changes side by side."},
                        {"type": "cmd", "where": "shell", "title": "From the terminal (Ctrl-\\)", "code": REVIEW_GIT,
                         "expect": "`git diff --stat` gives a quick overview. `git diff src/routes/payments.ts` shows the agent's file."},
                    ],
                },
            ],
            "rules": {
                "h2": "The pattern at a glance",
                "cards": [
                    ("The three windows", "Who works where.", ["Window", "Branch", "Job"], [
                        ["Window 0 `main`", "`main`", "PR reviews, releases, rebases"],
                        ["Window 1 `editor`", "`feature/payments`", "You: nvim, write tests, review changes, manual testing"],
                        ["Window 2 `agent`", "`feature/payments`", "Agent: generates code, refactors, fixes lint issues"],
                    ]),
                    ("Combined workflow", "The loop from the quick start.", ["Step", "Keys"], [
                        ["Edit code", "`Ctrl-a 0`"],
                        ["Save", "`:w`"],
                        ["Run tests", "`Ctrl-a 1`"],
                        ["Ask the agent if stuck", "`Ctrl-a 2`"],
                        ["Repeat", "Back to step one"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Hand the agent a task and keep working",
                "frame": "The agent renames `calc_totl` in `orders.py` while you add a line to `todo.txt`.",
                "open": "cd ~/tw && git worktree add ../tw-payments -b feature/payments\ncd ../tw-payments && nvim .",
                "steps": [
                    (None, "`Ctrl-a 2` then paste the task", "The agent window. Do not wait for it."),
                    (None, "`Ctrl-a 1`", "Back to the editor window."),
                    (None, "`<Space>sf` then `todo.txt`, then `G` `o` and type `buy glue`", "You edit a different file, so nothing collides."),
                    (None, "`<Space>sg` then `calc_total`, then `<Space>gd`", "Grep shows the agent's rename. The diff shows both changes."),
                ],
                "after": "orders.py  changed by the agent\ntodo.txt   changed by you",
                "meaning": "The agent and you share one branch but touch different files, so work runs in parallel with no conflicts.",
            },
            "practice": {
                "h2": "Practice: the three windows",
                "qs": [
                    ("Mechanism", "Why does the agent not break your editor session?",
                     "Where does it work?",
                     ["The agent runs in its own tmux window.", "The branch lives in its own worktree."],
                     "It edits a separate folder, so your session stays intact."),
                    ("Keystrokes", "Which keys open a new tmux window for the agent?",
                     "Prefix, then one letter.",
                     ["Press `Ctrl-a`.", "Press `c`."],
                     "`Ctrl-a c`."),
                    ("Application", "Create the feature workspace for `feature/payments` from main.",
                     "One command from your project.",
                     ["`cd ~/projects/my-service`.", "Run `git worktree add ../my-service-payments -b feature/payments main`."],
                     "`git worktree add ../my-service-payments -b feature/payments main`."),
                    ("Common mistake", "You and the agent keep overwriting each other. What is wrong?",
                     "Who edits which file?",
                     ["You are probably on the same files.", "You write tests while the agent writes the implementation."],
                     "Split the work by file."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Test, ship, clean up",
            "subtitle": "Run the tests, send fixes to the agent, open a PR and remove the worktree.",
            "idea": (
                "Test, fix, commit, push, open a PR, then remove the worktree. Main never gets dirty.",
                [
                    ("Run tests", "npm test -- --grep payments", "Or pytest tests/payments/ -v."),
                    ("Commit", "git commit -m \"Add payments endpoint with Stripe integration\"", "On the feature branch."),
                    ("Open a PR", "gh pr create", "Against the pushed branch."),
                    ("Clean up", "git worktree remove ../my-service-payments", "After the merge."),
                ],
                None,
            ),
            "problem": {
                "fail": "A failing test sits in one window while the agent sits idle in another. After the merge, dead worktrees pile up.",
                "fix": "Copy the failure to the agent, ship from the feature window, then remove the worktree and branch.",
            },
            "drills": [
                {
                    "h2": "Run tests",
                    "intro": "In the Neovim terminal (`Ctrl-\\` or `<Space>1`), run the tests.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Run the payments tests", "code": RUN_TESTS,
                         "expect": "The payments tests run. A failure is your cue to tell the agent in Window 2."},
                        {"type": "code", "file": "Prompt to the agent", "title": "Report a failing test", "code": FIX_PROMPT},
                    ],
                },
                {
                    "h2": "Meanwhile, back on main",
                    "intro": "Window 0 is the main branch, untouched. You can review someone else's PR (`gh pr checkout 789`), pull the latest (`git pull`) or start a hotfix (`gwa hotfix/fix-typo`). Main never gets dirty.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Jump to main", "code": BACK_ON_MAIN,
                         "expect": "You are on the main branch, untouched by the feature work."},
                        {"type": "text", "body": WINDOW_NOTE},
                    ],
                },
                {
                    "h2": "Commit, push, PR",
                    "intro": "Run these in the editor window or a terminal on the feature branch.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Ship the feature", "code": SHIP,
                         "expect": "`git status` lists what is staged. `gh pr create` opens a pull request titled \"Add /payments endpoint\" from `feature/payments`."},
                    ],
                },
                {
                    "h2": "Clean up after merge",
                    "intro": "Pull the merge on main, then remove the worktree and the local branch. Close the two extra tmux windows.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Remove the feature workspace", "code": AFTER_MERGE,
                         "expect": "The worktree folder and the local branch are gone, and the two extra tmux windows are closed."},
                    ],
                },
            ],
            "rules": {
                "h2": "Tips and the daily loop",
                "cards": [
                    ("The daily loop", "Seven steps, every feature.", None, DAILY_LOOP),
                    ("Pro tips", "Why this setup holds up.", ["Tip", "Why"], [
                        ["The agent can edit freely", "It is in its own worktree and cannot mess up your editor session"],
                        ["Test both branches", "Run benchmarks on main and feature side by side"],
                        ["Multiple features", "3 features = 3 worktrees = 3 tmux windows"],
                        ["Rebase without fear", "Rebase the feature worktree while main stays clean"],
                        ["Name your windows", "`Ctrl-a ,` then type `editor` / `agent` / `tests`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "From failing test to merged PR",
                "frame": "In `~/tw-payments` from the last page, a run fails and you want it fixed, shipped and cleaned up. Your repo has an `origin`.",
                "open": "cd ~/tw-payments",
                "steps": [
                    (None, "`python3 orders.py`", "In the editor window. If it fails, paste the error to the agent in Window 2, then run it again."),
                    (None, "`git add -A`, `git status`, then `git commit -m \"Fix the total\"`", "Stages the fix, lists it and commits."),
                    (None, "`git push -u origin feature/payments`, then `gh pr create --fill`", "Publishes the branch and opens the PR."),
                    (None, "After the merge: `cd ~/tw`, `git pull`, `git worktree remove ../tw-payments`, `git branch -d feature/payments`", "Pulls the merge, then removes the folder and the branch."),
                ],
                "after": "$ git push -u origin feature/payments\nbranch 'feature/payments' set up to track 'origin/feature/payments'.\n$ gh pr create --fill\nhttps://github.com/you/tw/pull/1\n$ git branch -d feature/payments\nDeleted branch feature/payments (was 9c4e7a2).",
                "meaning": "The loop is test, tell the agent, retest, ship, clean up. Each step lives in the window built for it.",
            },
            "practice": {
                "h2": "Practice: ship and clean up",
                "qs": [
                    ("Mechanism", "Why remove the worktree after the merge?",
                     "What would linger?",
                     ["The folder and its branch no longer have a job.", "Stale worktrees pile up."],
                     "Remove the folder and delete the branch, so nothing stale remains."),
                    ("Keystrokes", "Which command pushes the new branch and sets its upstream?",
                     "Push with `-u`.",
                     ["Use `git push`.", "Add `-u origin feature/payments`."],
                     "`git push -u origin feature/payments`."),
                    ("Application", "A test fails with 200 instead of 400. What do you do?",
                     "Who writes the fix?",
                     ["Switch to the agent window.", "Describe the failure and the expected result.", "Re-run the tests."],
                     "Tell the agent exactly what failed and what should happen."),
                    ("Common mistake", "You removed the worktree before merging the PR. What went wrong?",
                     "Order matters.",
                     ["Cleanup comes after the merge.", "Go to main, run `git pull`, then remove the worktree."],
                     "Merge first, then pull, then remove."),
                ],
            },
        },
    ],
}
