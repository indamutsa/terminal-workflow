"""Module 4: Worktrees and the agent loop. Sources: lessons 04 Git Worktree.md, 05 Agent Worktree Workflow.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


WINDOW_NOTE = "Windows start at 1 here (`base-index 1`): main is `Ctrl-a 1`, the editor `Ctrl-a 2` and the agent `Ctrl-a 3`."

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
# Window 1: main (you're here)

# Window 2: feature worktree
Ctrl-a c
cd ../myapp-payments
nvim .

# Now:
# Ctrl-a 1 = main branch
# Ctrl-a 2 = feature branch
''')

PARALLEL = C('''
git worktree add ../myapp-auth -b feature/auth main
git worktree add ../myapp-hotfix -b hotfix/urgent-fix main

# 4 tmux windows:
# 1: main
# 2: feature/payments
# 3: feature/auth
# 4: hotfix/urgent-fix

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

# Window 1: main (you're here already)

# Window 2: your editor on the feature branch
Ctrl-a c
cd ../my-service-payments
nvim .

# Window 3: your AI coding agent on the same feature branch
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
Ctrl-a 2                        # switch to Window 2 (editor)
<Space>sf                       # find/create tests/payments.test.ts
i                               # start writing tests
''')

REVIEW_KEYS = C('''
Ctrl-a 2                        # your editor window
''')

REVIEW_NVIM = C('''
<Space>sg                       # grep for "payments" — see all new files
<Space>gv                       # diffview — all changes side-by-side
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
Ctrl-a 1                        # Window 1 = main branch, untouched
''')

SHIP = C('''
# In Window 2 or terminal on feature branch:
git add -A
git status                      # review what's staged
git commit -m "Add payments endpoint with Stripe integration"
git push -u origin feature/payments
gh pr create --title "Add /payments endpoint" \\
  --body "POST /payments with Stripe. Validates amount/currency/customer_id."
''')

AFTER_MERGE = C('''
Ctrl-a 1                                    # switch to main
git pull                                    # get the merge
git worktree remove ../my-service-payments  # remove worktree
git branch -d feature/payments              # delete local branch

# Close tmux windows:
Ctrl-a 2
exit
Ctrl-a 2
exit
''')

DAILY_LOOP = C('''
1. gwa feature/new-thing          # create worktree + tmux window
2. Ctrl-a c → cd → <agent>       # agent window on same branch
3. Give the agent a task          # it works while you work
4. Ctrl-a 2 → nvim .             # you code in parallel
5. Review, test, iterate          # Ctrl-a 1/2/3 to switch
6. Commit, push, PR              # from terminal
7. gwr ../dir                    # clean up after merge
''')

MODULE = {
    "n": 4,
    "folder": "m4-worktrees",
    "title": "Work on several branches at once (worktrees)",
    "footer": "Work on several branches at once: worktrees, one tmux window each, an agent beside you, then test, ship and clean up",
    "tagline": "Run several branches at once, one folder and window each, with an agent beside you.",
    "glossary": [],
    "coverage_allow": [
        ("4. Ctrl-a 1 → nvim .", "lesson counts windows from 0; with base-index 1 the editor window is Ctrl-a 2"),
        ('local branch="$1"; local base="${2:-HEAD}"', "same gwa body, one statement per line"),
        ('gwr() { git worktree remove "$1" && echo "Removed: $1"; }', "same gwr body, one statement per line"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Work on several branches at once without stashing",
            "subtitle": "Switch branches without git stash, check out two branches at once, start a hotfix mid-feature, remove a worktree",
            "idea": (
                "Work on a second branch in its own folder (a worktree); both share one git history.",
                [
                    ("Create a worktree on a new branch", "git worktree add ../dir -b branch", "Makes a new folder on a new branch."),
                    ("List every worktree and its branch", "git worktree list", "Shows every folder and its branch."),
                    ("Remove (delete) a worktree", "git worktree remove ../dir", "Deletes the folder."),
                    ("Clean up a worktree folder you deleted by hand", "git worktree prune", "Clears stale entries."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why do I have to stash and switch branches when a hotfix lands mid-feature? You stash, switch branches, switch back and hope the stash pops cleanly.",
                "fix": "Work on both branches at once: give each its own folder with `git worktree add`. No stashing, no switching.",
            },
            "drills": [
                {
                    "h2": "Switch branches without stashing",
                    "intro": "Compare the painful way (stash and switch) with the worktree way.",
                    "blocks": [
                        {"type": "code", "file": "Without worktrees", "title": "Compare stashing and switching with using worktrees", "code": NO_WORKTREE},
                    ],
                },
                {
                    "h2": "Create a worktree for a new feature branch",
                    "intro": "Start a feature in a new folder: run this in your project on the main branch. `-b feature/payments` creates the branch from the current HEAD. `../myapp-payments/` is the new directory.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a new folder on a new feature branch", "code": FIRST_WORKTREE,
                         "expect": "`git worktree list` shows two lines: `/Users/you/projects/myapp` on `[main]` and `/Users/you/projects/myapp-payments` on `[feature/payments]`."},
                        {"type": "text", "body": "Check out two branches at once: two directories, two branches, both fully functional. Same git history: no cloning, no disk waste."},
                    ],
                },
                {
                    "h2": "Work inside the new worktree",
                    "intro": "Changes here only affect `feature/payments`. Main in `../myapp/` stays untouched.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Go into the new folder and check which branch you are on", "code": IN_WORKTREE,
                         "expect": "`ls` shows the same files as main. `git branch` confirms `feature/payments`."},
                    ],
                },
                {
                    "h2": "Start a worktree from main, a commit or a remote branch",
                    "intro": "Choose where the new branch starts.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Start a worktree from main, an old commit or someone's remote branch", "code": BASE_BRANCHES,
                         "expect": "Each command makes a new folder beside your project: `../myapp-auth`, `../myapp-fix` and `../myapp-review`."},
                    ],
                },
                {
                    "h2": "See how several worktrees sit in your folders",
                    "intro": "Each directory is a fully functional checkout with its own `node_modules`, `.venv` and build cache. They share the same `.git` object store.",
                    "blocks": [
                        {"type": "code", "file": "~/projects", "title": "See four worktrees side by side", "code": LAYOUT},
                    ],
                },
            ],
            "rules": {
                "h2": "Find the worktree command you need",
                "cards": [
                    ("Create, list and remove a worktree", "The six commands you need.", ["Command", "What it does"], [
                        ["`git worktree add ../dir -b branch`", "Create a worktree on a new branch"],
                        ["`git worktree add ../dir -b branch base`", "Create a worktree from a specific base (branch or commit)"],
                        ["`git worktree add ../dir existing-branch`", "Check out an existing branch in a new worktree"],
                        ["`git worktree list`", "List all worktrees"],
                        ["`git worktree remove ../dir`", "Remove (delete) a worktree"],
                        ["`git worktree prune`", "Clean up entries for folders you deleted by hand"],
                    ]),
                    ("Worktree commands and shell aliases", "Find the command or the alias for each job.", ["Command", "Action"], [
                        ["`git worktree add ../dir -b branch`", "Create a worktree"],
                        ["`git worktree list`", "List worktrees"],
                        ["`git worktree remove ../dir`", "Remove a worktree"],
                        ["`gwt ../dir -b branch`", "Create a worktree and copy git-excluded files (installed)"],
                        ["`gwa feature/name`", "Create a worktree and open a tmux window (add it first)"],
                        ["`gwl`", "List worktrees (add it first)"],
                        ["`gwr ../dir`", "Remove a worktree (add it first)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Start a feature without touching main",
                "frame": "Start a payments feature and keep `~/tw` on main exactly as it is.",
                "open": "cd ~/tw && git init -q -b main && git add -A && git commit -qm init",
                "steps": [
                    (None, "`git worktree add ../tw-payments -b feature/payments`", "Makes the folder and the branch."),
                    (None, "`git worktree list`", "Two folders, two branches."),
                    (None, "`cd ../tw-payments` then `git branch`", "Marks `feature/payments` as current. Edit freely: `~/tw` stays on main."),
                    (None, "`cd ../tw` then `git worktree remove ../tw-payments` and `git branch -d feature/payments`", "Removes the folder and the branch."),
                ],
                "after": "/Users/you/tw          3f2a1b9 [main]\n/Users/you/tw-payments 3f2a1b9 [feature/payments]",
                "meaning": "To switch branches, `cd` into another folder: each branch is a place you can walk into.",
            },
            "practice": {
                "h2": "Check how to work on branches with worktrees",
                "qs": [
                    ("Mechanism", "Why is a worktree cheaper than cloning the repo again?",
                     "What is shared?",
                     ["Every worktree shares the same `.git` object store.", "Only the checked-out files are duplicated."],
                     "Same history, no cloning, no disk waste."),
                    ("Keystrokes", "How do I create `../myapp-auth` on a new branch `feature/auth` from main?",
                     "Add, then `-b`, then a base.",
                     ["Start with `git worktree add`.", "Add the folder `../myapp-auth`.", "Add `-b feature/auth main`."],
                     "`git worktree add ../myapp-auth -b feature/auth main`."),
                    ("Application", "How do I start an urgent hotfix mid-feature without stashing?",
                     "Branch off a specific commit or main.",
                     ["Run `git worktree add ../myapp-fix -b hotfix/urgent abc1234`.", "`cd ../myapp-fix` and fix it there."],
                     "A second worktree. Your feature folder is untouched."),
                    ("Common mistake", "I deleted a worktree folder by hand. How do I clean up git's record of it?",
                     "Git still remembers it.",
                     ["The entry is stale.", "Run `git worktree prune`."],
                     "`git worktree prune`, then `git worktree list` to check."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Open each branch in its own tmux window",
            "subtitle": "Open a worktree in a new tmux window, create a worktree and window in one command, switch branches with one key, remove a worktree",
            "idea": (
                "Give each branch one folder and one tmux window, then switch branches with one key.",
                [
                    ("Open a new tmux window for a worktree", "Ctrl-a c", "Then cd into the worktree."),
                    ("Create a worktree and a tmux window together", "gwa feature/auth", "Worktree and tmux window in one go. Add it first."),
                    ("List all worktrees", "gwl", "Shows every worktree. Add it first."),
                    ("Remove a worktree after the merge", "gwr ../dir", "Removes the worktree. Add it first."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why do I lose track of a new worktree? You create it, then have no window, no editor, and a long path to retype.",
                "fix": "Give each worktree its own tmux window, and let `gwa` create both in one command.",
            },
            "drills": [
                {
                    "h2": "Open a worktree in its own tmux window",
                    "intro": "Give each worktree its own tmux window. No git stash, no waiting, no risk. Switch branches in milliseconds.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Open the feature worktree in a new tmux window", "code": TMUX_WORKTREES,
                         "expect": "The feature branch opens in `nvim` in its own window. Switch between main and the feature with one prefix key."},
                        {"type": "text", "body": WINDOW_NOTE},
                    ],
                },
                {
                    "h2": "Run tests on several branches in parallel",
                    "intro": "Run tests on two branches at the same time.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create two more worktrees for parallel work", "code": PARALLEL,
                         "expect": "You now have four tmux windows' worth of work: main, `feature/payments`, `feature/auth` and `hotfix/urgent-fix`."},
                    ],
                },
                {
                    "h2": "Remove a worktree and its branch after the merge",
                    "intro": "Remove the worktree and the branch after the feature is merged.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Remove the worktree, delete the branch and see what is left", "code": CLEAN_UP,
                         "expect": "`git worktree list` shows what is left: no `myapp-payments`."},
                    ],
                },
                {
                    "h2": "Go from the first worktree to clean-up (the whole workflow)",
                    "intro": "The whole cycle, from first worktree to clean-up.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Start a feature, push it, open a PR, start the next one, clean up", "code": REAL_WORKFLOW,
                         "expect": "`git push -u origin feature/payments` publishes the branch, and `gh pr create` opens the pull request titled \"Add payments\"."},
                    ],
                },
                {
                    "h2": "Create a worktree that keeps your ignored files",
                    "intro": "`gwt` is installed on this Mac. It runs `git worktree add` with your arguments, then copies every path listed in the repository's `.git/info/exclude` into the new folder. The new folder must be the first argument.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a worktree and copy your excluded files (gwt)", "code": "cd ~/tw && gwt ../tw-orders -b feature/orders",
                         "expect": "Git prints `Preparing worktree (new branch 'feature/orders')`. `../tw-orders` exists on `feature/orders`, and any excluded path that exists in `~/tw` is copied into it with `cp -a`."},
                    ],
                },
                {
                    "h2": "Add aliases to create and remove worktrees (~/.zshrc)",
                    "intro": "These three are not installed yet: add them to `~/.zshrc` first. `gwa` creates a worktree and opens it in a new tmux window named after the branch.",
                    "blocks": [
                        {"type": "code", "file": "~/.zshrc", "title": "Add the gwa, gwr and gwl aliases", "code": HELPERS},
                        {"type": "cmd", "where": "shell", "title": "Create, list and remove a worktree with the aliases", "code": HELPER_USAGE,
                         "expect": "`gwa feature/auth` makes `../myapp-feature-auth` and opens a tmux window named `auth` in it. `gwl` lists every worktree."},
                    ],
                },
            ],
            "rules": {
                "h2": "Find the right alias for a worktree",
                "cards": [
                    ("Create, list and remove a worktree with aliases", "Four lines to remember.", None, HELPER_USAGE),
                    ("What folder and window name does gwa choose?", "Both names come from the branch.", ["Piece", "Result for `gwa feature/auth`"], [
                        ["Folder name", "`../myapp-feature-auth`"],
                        ["tmux window name", "`auth`"],
                        ["Starting point (base)", "`HEAD`, or the second argument"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Start a feature branch and its tmux window in one command",
                "frame": "You want a feature branch with its own window. You are in tmux, with `gwa`, `gwr` and `gwl` in your `~/.zshrc`.",
                "open": "cd ~/tw",
                "steps": [
                    (None, "`gwa feature/auth`", "Makes `../tw-feature-auth` and a tmux window named `auth` in it."),
                    (None, "`nvim .`", "Opens the new folder in that window."),
                    (None, "`gwl`", "Lists every worktree."),
                    (None, "`gwr ../tw-feature-auth`", "After the merge, removes the worktree."),
                ],
                "after": "$ gwl\n/Users/you/tw               3f2a1b9 [main]\n/Users/you/tw-feature-auth 3f2a1b9 [feature/auth]\n$ gwr ../tw-feature-auth\nRemoved: ../tw-feature-auth",
                "meaning": "Create the worktree and its window with one command, so you use a worktree for every feature.",
            },
            "practice": {
                "h2": "Check how to use worktrees with tmux",
                "qs": [
                    ("Mechanism", "Why use one tmux window per worktree?",
                     "What do you keep apart?",
                     ["Each branch has its own editor, shell and tests.", "Switching is a key, not a checkout."],
                     "Each branch keeps its own state."),
                    ("Keystrokes", "How do I create a worktree from main and open a tmux window for it?",
                     "The helper alias, with a base.",
                     ["Use `gwa`.", "Add the branch, then `main`."],
                     "`gwa feature/auth main`."),
                    ("Application", "How do I remove `../myapp-feature-auth` after the merge?",
                     "The remove helper.",
                     ["Run `gwr ../myapp-feature-auth`.", "Check with `gwl`."],
                     "`gwr ../myapp-feature-auth`."),
                    ("Common mistake", "Why does `gwa` fail at the window step when I run it outside tmux?",
                     "What does `gwa` call at the end?",
                     ["`gwa` ends with `tmux new-window`.", "Start or attach tmux first."],
                     "The helper needs tmux. Run `tmux attach` first."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Run an AI coding agent and your editor on the same branch",
            "subtitle": "Give an AI agent its own window, edit the same feature branch in parallel, review what the agent changed, find the agent's keys",
            "idea": (
                "Work on one feature with an agent beside you: one worktree, you in one window, the agent in the other.",
                [
                    ("Go to the main window", "Ctrl-a 1", "PR reviews, releases, rebases."),
                    ("Go to your editor window", "Ctrl-a 2", "You: nvim, tests, review."),
                    ("Go to the agent window", "Ctrl-a 3", "The coding agent generates code."),
                    ("Create the feature folder (workspace)", "git worktree add ../my-service-payments -b feature/payments main", "Makes the feature folder."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does the agent mess up my checkout? The agent and your editor fight over the same checkout, and half-finished edits land on your main branch.",
                "fix": "Give the feature its own worktree. You and the agent edit the same branch from different terminals.",
            },
            "drills": [
                {
                    "h2": "Set up a worktree with an editor window and an agent window",
                    "intro": "Window 1 is main. Window 2 is your editor. Window 3 is your AI coding agent, on the same feature branch.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the worktree, an editor window and an agent window", "code": CREATE_WORKSPACE,
                         "expect": "`../my-service-payments` exists on `feature/payments`. Window 2 runs `nvim .` and Window 3 runs your agent, both in that folder."},
                        {"type": "text", "body": WINDOW_NOTE},
                    ],
                },
                {
                    "h2": "Give the agent a task and keep working",
                    "intro": "Switch to Window 3 (`Ctrl-a 3`) and type the task. Do not wait for the agent to finish: switch to your editor.",
                    "blocks": [
                        {"type": "code", "file": "Prompt to the agent", "title": "Write a task the agent can act on", "code": AGENT_TASK},
                    ],
                },
                {
                    "h2": "Look up the agent's keys and slash commands",
                    "intro": "Forget a key inside the agent? Print its cheat sheet in any pane.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show the agent's keys and slash commands", "code": "cch",
                         "expect": "A table of KEY, ACTION and DESCRIPTION rows, then a SLASH COMMANDS list. For example `Ctrl+Enter` inserts a newline, `Esc` cancels, `Ctrl+C` interrupts the running task and `Shift+Tab` cycles the permission mode."},
                    ],
                },
                {
                    "h2": "Write tests while the agent writes code",
                    "intro": "While the agent writes the implementation, you write tests. You and the agent edit the same branch in different terminals. No conflicts: you are on different files.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Switch to the editor window and start writing tests", "code": PARALLEL_KEYS,
                         "expect": "You are in the editor window, finding or creating `tests/payments.test.ts`, in insert mode."},
                    ],
                },
                {
                    "h2": "See what the agent changed",
                    "intro": "Go to the editor window, then check what the agent changed.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Go back to the editor window", "code": REVIEW_KEYS,
                         "expect": "You are in your editor window."},
                        {"type": "cmd", "where": "nvim", "title": "Search the new files and see all changes in Neovim", "code": REVIEW_NVIM,
                         "expect": "The grep lists every new file mentioning \"payments\". The diff view shows all changes side by side."},
                        {"type": "cmd", "where": "shell", "title": "See the changes from the terminal (Ctrl-\\)", "code": REVIEW_GIT,
                         "expect": "`git diff --stat` gives a quick overview. `git diff src/routes/payments.ts` shows the agent's file."},
                    ],
                },
            ],
            "rules": {
                "h2": "See which window does what",
                "cards": [
                    ("Which window does what?", "Who works where.", ["Window", "Branch", "Job"], [
                        ["Window 1 `main`", "`main`", "Review PRs, make releases, rebase"],
                        ["Window 2 `editor`", "`feature/payments`", "You: edit in nvim, write tests, review changes, test by hand"],
                        ["Window 3 `agent`", "`feature/payments`", "Agent: writes code, refactors, fixes lint issues"],
                    ]),
                    ("Switch between your editor and the agent in a loop", "The loop from the quick start.", ["Step", "Keys"], [
                        ["Edit code", "`Ctrl-a 2`"],
                        ["Save", "`:w`"],
                        ["Run tests", "`Ctrl-a 2`"],
                        ["Ask the agent when you are stuck", "`Ctrl-a 3`"],
                        ["Repeat", "Back to step one"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Hand the agent a task and keep working",
                "frame": "The agent renames `calc_totl` in `orders.py` while you add a line to `todo.txt`.",
                "open": "cd ~/tw && git worktree add ../tw-payments -b feature/payments\ncd ../tw-payments && nvim .",
                "steps": [
                    (None, "`Ctrl-a 3` then paste the task", "The agent window. Do not wait for it."),
                    (None, "`Ctrl-a 2`", "Back to the editor window."),
                    (None, "`<Space>sf` then `todo.txt`, then `G` `o` and type `buy glue`", "You edit a different file, so nothing collides."),
                    (None, "`<Space>sg` then `calc_total`, then `<Space>gv`", "Grep shows the agent's rename. The diff shows both changes."),
                ],
                "after": "orders.py  changed by the agent\ntodo.txt   changed by you",
                "meaning": "The agent and you share one branch but touch different files, so work runs in parallel with no conflicts.",
            },
            "practice": {
                "h2": "Check how to work beside an agent",
                "qs": [
                    ("Mechanism", "Why doesn't the agent break my editor session?",
                     "Where does it work?",
                     ["The agent runs in its own tmux window.", "The branch lives in its own worktree."],
                     "It edits a separate folder, so your session stays intact."),
                    ("Keystrokes", "How do I open a new tmux window for the agent?",
                     "Prefix, then one letter.",
                     ["Press `Ctrl-a`.", "Press `c`."],
                     "`Ctrl-a c`."),
                    ("Application", "How do I create the feature workspace for `feature/payments` from main?",
                     "One command from your project.",
                     ["`cd ~/projects/my-service`.", "Run `git worktree add ../my-service-payments -b feature/payments main`."],
                     "`git worktree add ../my-service-payments -b feature/payments main`."),
                    ("Common mistake", "Why do the agent and I keep overwriting each other's changes?",
                     "Who edits which file?",
                     ["You are probably on the same files.", "You write tests while the agent writes the implementation."],
                     "Split the work by file."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Test, ship and clean up a feature branch",
            "subtitle": "Run the tests, tell the agent about a failing test, commit and push, open a PR, remove the worktree after the merge",
            "idea": (
                "Ship a feature from its worktree: test, fix, commit, push, open a PR, then remove the worktree. Main never gets dirty.",
                [
                    ("Run the payments tests", "npm test -- --grep payments", "Or pytest tests/payments/ -v."),
                    ("Commit the changes on the feature branch", "git commit -m \"Add payments endpoint with Stripe integration\"", "Run it on the feature branch."),
                    ("Open a pull request (PR)", "gh pr create", "Against the pushed branch."),
                    ("Remove the worktree after the merge", "git worktree remove ../my-service-payments", "Run it after the merge."),
                ],
                None,
            ),
            "problem": {
                "fail": "What do I do with a failing test while the agent sits idle? The failure sits in one window while the agent waits in another. After the merge, dead worktrees pile up.",
                "fix": "Copy the failure to the agent, ship from the feature window, then remove the worktree and branch.",
            },
            "drills": [
                {
                    "h2": "Run the tests and tell the agent what failed",
                    "intro": "In the Neovim terminal (`Ctrl-\\` or `<Space>tf`), run the tests.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Run the payments tests", "code": RUN_TESTS,
                         "expect": "The payments tests run. A failure is your cue to tell the agent in Window 3."},
                        {"type": "code", "file": "Prompt to the agent", "title": "Tell the agent which test failed", "code": FIX_PROMPT},
                    ],
                },
                {
                    "h2": "Go back to main while the agent works",
                    "intro": "Window 1 is the main branch, untouched. You can review someone else's PR (`gh pr checkout 789`), pull the latest (`git pull`) or start a hotfix (`gwa hotfix/fix-typo`). Main never gets dirty.",
                    "blocks": [
                        {"type": "cmd", "where": "tmux", "title": "Jump back to the main window", "code": BACK_ON_MAIN,
                         "expect": "You are on the main branch, untouched by the feature work."},
                        {"type": "text", "body": WINDOW_NOTE},
                    ],
                },
                {
                    "h2": "Commit, push and open a pull request",
                    "intro": "Run these in the editor window or a terminal on the feature branch.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Commit, push and open a PR for the feature", "code": SHIP,
                         "expect": "`git status` lists what is staged. `gh pr create` opens a pull request titled \"Add /payments endpoint\" from `feature/payments`."},
                    ],
                },
                {
                    "h2": "Stage, commit and undo with LazyGit in a worktree",
                    "intro": "Stage, commit, amend, push and undo without typing git commands: run LazyGit inside the worktree and it works on that branch only. It is a full-screen git panel with stock keys.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open LazyGit on the feature branch", "code": "cd ../my-service-payments && lzy",
                         "expect": "LazyGit fills the terminal. Five panels run down the left: `[1] Status` (the folder and branch, `feature/payments`), `[2] Files`, `[3] Local branches`, `[4] Commits` and `[5] Stash`. The right side shows details of the selection; a selected file shows its diff. The bottom line lists the main keys."},
                        {"type": "keys", "where": "lazygit", "title": "Stage files and commit in LazyGit", "rows": [
                            ("Space", "Stage or unstage the highlighted file in the Files panel"),
                            ("a", "Stage all files (press again to unstage all)"),
                            ("c", "Commit the staged files: type the message, then Enter"),
                            ("A", "Add the staged changes to the last commit (amend)"),
                            ("P", "Push to the remote"),
                            ("p", "Pull from the remote"),
                        ], "try": "Press `2` for the Files panel, `a`, then `c`, type `Fix the total` and press `Enter`.",
                         "expect": "The Files panel empties and `Fix the total` heads the Commits panel."},
                        {"type": "keys", "where": "lazygit", "title": "Undo a commit, stash changes and open help in LazyGit", "rows": [
                            ("z", "Undo the last action (reflog); right after a commit this is undo last commit, and the changes stay staged. Enter confirms"),
                            ("s", "Stash (set aside) changes from the Files panel"),
                            ("d", "Discard changes: a menu offers all changes or only unstaged"),
                            ("n", "Create a new branch from the Branches panel"),
                            ("]", "Go to the next tab: in the Files panel it reaches the Worktrees tab"),
                            ("?", "Open help to see every key for the current panel"),
                            ("q", "Quit LazyGit"),
                        ], "try": "Press `z` after a commit.",
                         "expect": "A box asks whether to soft reset to the previous commit (undo goes through the reflog, so right after a commit it undoes that commit). `Enter` confirms: the commit disappears from the Commits panel and its files are staged again. `Esc` cancels."},
                    ],
                },
                {
                    "h2": "Remove the worktree and branch after the merge",
                    "intro": "Pull the merge on main, then remove the worktree and the local branch. Close the two extra tmux windows.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Remove the feature workspace", "code": AFTER_MERGE,
                         "expect": "The worktree folder and the local branch are gone, and the two extra tmux windows are closed."},
                    ],
                },
            ],
            "rules": {
                "h2": "Find the daily loop and tips for worktree work",
                "cards": [
                    ("Repeat these seven steps for every feature", "Seven steps, every feature.", None, DAILY_LOOP),
                    ("Why does this setup work well?", "Why this setup holds up.", ["Tip", "Why"], [
                        ["Let the agent edit freely", "It is in its own worktree and cannot mess up your editor session"],
                        ["Test both branches", "Run benchmarks on main and feature side by side"],
                        ["Work on several features", "3 features = 3 worktrees = 3 tmux windows"],
                        ["Rebase safely", "Rebase the feature worktree while main stays clean"],
                        ["Rename your tmux windows", "`Ctrl-a ,` then type `editor` / `agent` / `tests`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Fix a failing test, ship it and merge the PR",
                "frame": "In `~/tw-payments` from the last page, a run fails and you want it fixed, shipped and cleaned up. Your repo has an `origin`.",
                "open": "cd ~/tw-payments",
                "steps": [
                    (None, "`python3 orders.py`", "In the editor window. If it fails, paste the error to the agent in Window 3, then run it again."),
                    (None, "`git add -A`, `git status`, then `git commit -m \"Fix the total\"`", "Stages the fix, lists it and commits."),
                    (None, "`git push -u origin feature/payments`, then `gh pr create --fill`", "Publishes the branch and opens the PR."),
                    (None, "After the merge: `cd ~/tw`, `git pull`, `git worktree remove ../tw-payments`, `git branch -d feature/payments`", "Pulls the merge, then removes the folder and the branch."),
                ],
                "after": "$ git push -u origin feature/payments\nbranch 'feature/payments' set up to track 'origin/feature/payments'.\n$ gh pr create --fill\nhttps://github.com/you/tw/pull/1\n$ git branch -d feature/payments\nDeleted branch feature/payments (was 9c4e7a2).",
                "meaning": "The loop is test, tell the agent, retest, ship, clean up. Each step lives in the window built for it.",
            },
            "practice": {
                "h2": "Check how to ship and clean up a feature",
                "qs": [
                    ("Mechanism", "Why remove the worktree after the merge?",
                     "What would linger?",
                     ["The folder and its branch no longer have a job.", "Stale worktrees pile up."],
                     "Remove the folder and delete the branch, so nothing stale remains."),
                    ("Keystrokes", "How do I push the new branch and set its upstream?",
                     "Push with `-u`.",
                     ["Use `git push`.", "Add `-u origin feature/payments`."],
                     "`git push -u origin feature/payments`."),
                    ("Application", "A test fails with 200 instead of 400. What should I do?",
                     "Who writes the fix?",
                     ["Switch to the agent window.", "Describe the failure and the expected result.", "Re-run the tests."],
                     "Tell the agent exactly what failed and what should happen."),
                    ("Common mistake", "I removed the worktree before merging the PR. What went wrong?",
                     "Order matters.",
                     ["Cleanup comes after the merge.", "Go to main, run `git pull`, then remove the worktree."],
                     "Merge first, then pull, then remove."),
                ],
            },
        },
    ],
}
