"""Module 5: code intelligence and git. Sources: lesson 06 (first half) and the quick-start guide cards."""
import re


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


def R(s):
    """Rows from a lesson fence: `key  action` split at the first run of two or more spaces."""
    rows = []
    for line in C(s).split("\n"):
        if not line.strip():
            continue
        if line.startswith(" " * 8) and rows:
            rows[-1] = (rows[-1][0], (rows[-1][1] + " " + line.strip()).strip())
            continue
        parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
        rows.append((parts[0], parts[1] if len(parts) > 1 else ""))
    return rows


def K(title, rows, where="nvim", **kw):
    return {"type": "keys", "where": where, "title": title, "rows": R(rows) if isinstance(rows, str) else rows, **kw}


LSP_NAV = r'''
gd               Jump to where a symbol is defined: go to definition (Ctrl-t to jump back)
gr               Find every place a symbol is used: references (who uses this?)
gI               Jump to the implementation
gy               Jump to the type definition
gD               Jump to the declaration
gK               Show a function's arguments: signature help
gO               Show the outline (list of symbols) of this file: document symbols
K                Show docs for the word under the cursor: hover (press again to enter the float)
'''

DIAG = r'''
]d               Jump to the next error or warning
[d               Jump to the previous error or warning
<Space>xx        Open or close the list of all errors and warnings: Trouble
<Space>xX        Show errors and warnings for this file (buffer) only
<Space>sd        Search the errors and warnings (diagnostics) in a picker
<Space>cs        Show the outline of symbols in this file: Aerial
<Space>xQ        Show the quickfix list: Trouble
<Space>xL        Show the location list: Trouble
'''

GITSIGNS = r'''
]h               Jump to the next changed block (hunk)
[h               Jump to the previous changed block (hunk)
<Space>ghs       Stage this changed block (hunk)
<Space>ghu       Undo the last stage: unstage hunk
<Space>ghr       Discard this changed block (hunk): reset hunk
<Space>ghS       Stage the whole file (buffer)
<Space>ghR       Discard every change in the file (buffer): reset buffer
<Space>ghp       Preview what changed in this hunk, inline
<Space>ghb       See who changed this line: detailed blame
<Space>ghB       See who changed each line of the file: blame for the whole buffer
<Space>ghd       Show the diff of this file
<Space>ghD       Compare this file with the previous commit: show the diff
'''

LAZYGIT_OPEN = r'''
<Space>gg        Open LazyGit at the repository root
<Space>gG        Open LazyGit in the current folder (working directory)
'''

LAZYGIT_KEYS = r'''
Space            Stage or unstage the file
c                Commit the staged files
P                Push commits to the remote
p                Pull commits from the remote
3                Show your branches: the branches panel
4                Show the commits panel: the commit log
s                Stash all changes (in the files panel)
l                Move to the next panel
?                Show every key: help

EXIT:
q                Quit LazyGit and go back to Neovim
'''

SNACKS_GIT = r'''
<Space>gL        Show the git log for the current folder
<Space>gb        Show the commit history for this line (who changed it, and when)
<Space>gf        Show the commit history for this file
<Space>gl        Show the repository log
<Space>gB        Open this file or line on its remote (e.g. GitHub) in the browser
<Space>gY        Copy the link (URL) to this file or line on its remote
<Space>gs        Show git status in a picker: see what changed
<Space>gd        Show the git diff, hunk by hunk, in a picker
<Space>gD        Compare your changes with origin: show the git diff against origin
<Space>gS        Show your stashed changes: the git stashes
<Space>gi / gI   List GitHub issues: open / all
<Space>gp / gP   List GitHub pull requests: open / all
'''

DIFFVIEW_OPEN = r'''
<Space>gv        Open the diff of your changes in Diffview (working tree)
<Space>gV        Open the history of this file in Diffview
'''

DIFFVIEW_KEYS = r'''
Tab / Shift-Tab  Go to the next / previous changed file
Enter            Open the selected diff
s or -           Stage or unstage the selected file
S / U            Stage all files / unstage all files
[x / ]x          Jump to the previous / next merge conflict
<Space>co        Fix the merge conflict with our version: choose ours
<Space>ct        Fix the merge conflict with their version: choose theirs
<Space>cb        Fix the merge conflict with the base version: choose base
<Space>ca        Keep every version of the conflict: choose all
g?               Show Diffview help for this panel
'''

EXPLORER = r'''
<Space>e         Open or close the file explorer (Snacks) at the project root
<Space>E         Open or close the file explorer (Snacks) in the current folder
\                Open or close the file explorer (Snacks) in the current folder (custom mapping)
'''

NEOTREE_OPEN = r'''
\                Open or close the file explorer sidebar
'''

NEOTREE_KEYS = r'''
a                Create a file or folder (directory): end the name with / for a folder
d                Delete (remove) the file or folder
r                Rename the file or folder
c                Copy the file or folder
m                Move the file or folder
/                Switch between the file list and the filter box
H                Show or hide hidden files
?                Show the explorer help

EXIT:
\                Close the explorer: press the same key that opened it
q                Close the explorer
'''

LSP_ACTIONS = r'''
<Space>cr        Rename a function or variable (symbol) across the whole project
<Space>ca        Fix an error or refactor the code: code actions (quick fixes, auto-imports, refactors)
<Space>cf        Format the file (ruff for Python, prettier for JS, etc.)
<Space>cd        Show the error or warning for this line in a float: diagnostics
<Space>cl        See which language servers are attached: LSP info
'''

GRUG = r'''
<Space>sr        Replace text in every file: open the search and replace panel (grug-far; works on a word or selection too)
'''

GRUG_EXIT = r'''
EXIT:
q                Close the grug-far panel
:q               :q also closes it
'''

TERM_FLOAT = r'''
Ctrl-\           Open or hide the last terminal you used, in its original working directory
Ctrl-/           Open or hide the last terminal you used (same as Ctrl-\)
<Space>ft        Open or hide the floating terminal
'''

TERM_SPLIT = r'''
<Space>tf        Open a floating terminal
<Space>tv        Open a terminal on the right: vertical split
<Space>th        Open a terminal at the bottom: horizontal split
'''

TERM_EXIT = r'''
EXIT TERMINAL MODE:
Ctrl-\ Ctrl-n    Leave terminal mode and go back to normal mode
'''

FIND = r'''
<Space>sf        Find a file by name in the current folder (your main find-file key)
<Space><Space>   Find a file by name: same as <Space>sf, in the current folder
<Space>ff        Find a file by name in the current folder
<Space>fF        Find a file by name in the current folder (same as <Space>ff)
<Space>fr        Open a file you used recently
<Space>fg        Find a git-tracked file in the current folder
<Space>fb        Switch to an open file (buffer)
<Space>,         Switch to an open file (buffer): quick switch
<Space>fc        Find a config file
'''

GREP = r'''
<Space>/         Search text in every file: grep in the current folder
<Space>sg        Search text in every file: grep in the current folder
<Space>sG        Search text in every file: grep in the current folder (same as <Space>sg)
<Space>sw        Search every file for the word or selection under the cursor: grep in the current folder
<Space>sb        Search for a line in this file (buffer)
<Space>sB        Search text in open files: grep in listed file buffers below the current folder
'''

PICKERS = r'''
<Space>sd        List the errors and warnings (diagnostics)
<Space>sR        Reopen the last picker: resume
<Space>sh        Search the help pages
<Space>sk        Search the keymaps
<Space>sC        Run a command by name: command list
<Space>s"        Show the registers (copied text)
<Space>sm        Show the marks
<Space>sj        Show the jump list
<Space>st        List the todo comments
'''

PICKER_KEYS = r'''
Ctrl-n / Ctrl-p  Move down / up the results
Ctrl-s           Open the result in a horizontal split
Ctrl-v           Open the result in a vertical split
Enter            Open the file
Ctrl-q           Send all results to the quickfix list

EXIT:
Esc              Close the picker
Ctrl-c           Close the picker as well
'''

NEOTEST = r'''
<Space>tr        Run the test under the cursor (the nearest test)
<Space>tt        Run all tests in this file
<Space>tT        Run every test file
<Space>ts        Open or close the test summary panel (see which tests pass and fail)
<Space>to        Show the test output (print and debug output)
<Space>tO        Open or close the output panel
<Space>tl        Run the last test again
<Space>tw        Turn watch mode on or off
<Space>tS        Stop the running test
<Space>td        Debug the nearest test (via DAP)
'''

DAP = r'''
<Space>db        Set or clear a breakpoint on this line (stop the program here)
<Space>dB        Set a conditional breakpoint (prompts for the condition)
<Space>dc        Start or continue the program (run)
<Space>di        Step into the function
<Space>dO        Step over to the next line
<Space>do        Step out of the function
<Space>dC        Run to the cursor
<Space>du        Open or close the debugger UI (variables, stack, breakpoints)
<Space>de        Evaluate an expression (also works on a visual selection)
<Space>dr        Open or close the REPL
<Space>dl        Run the last session again
<Space>dt        Stop the debug session: terminate
'''

DAP_TEST = r'''
<Space>td        Debug the nearest test (neotest + DAP)
<Space>dPt       Debug the Python test method under the cursor
<Space>dPc       Debug the Python test class
'''

VENV = r'''
<Space>cv        Pick the Python virtualenv for this project: select the interpreter
'''

MODULE = {
    "n": 5,
    "folder": "m5-lsp-git",
    "title": "Jump around code and use git in Neovim",
    "footer": "Jump to definitions, find errors, stage and commit changes, rename across files, search the project, run and debug tests",
    "tagline": "Jump to a definition, stage one change, rename a function everywhere and debug a test.",
    "glossary": [],
    "coverage_allow": [
        ("<Space>Tf", "lesson maps capital <Space>Tf; the live config has lowercase <Space>tf for the float terminal"),
        ("<Space>Tv", "lesson maps capital <Space>Tv; the live config has lowercase <Space>tv for the right terminal"),
        ("<Space>Th", "lesson maps capital <Space>Th; the live config has lowercase <Space>th for the bottom terminal"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Jump to where a function is defined and find its uses",
            "subtitle": "Jump to a function's definition, find every place it is used, jump back, find errors and warnings, find unused imports",
            "idea": (
                "Find where a function is defined or used: ask the language server instead of searching text.",
                [
                    ("Jump to where a name is defined", "gd", "Go to the definition."),
                    ("Find every use of a name", "gr", "List every real use: the references."),
                    ("Jump to the next error or warning", "]d", "Find problems without scrolling."),
                    ("Go back to where you started", "Ctrl-o", "Return to the spot you jumped from."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I find where a function is used without wading through comments, strings and unrelated matches from grep?",
                "fix": "Ask the language server. `gd` jumps to the definition and `gr` lists the real references.",
            },
            "drills": [
                {
                    "h2": "Open the practice project (nvim-drills)",
                    "intro": "Every exercise runs against `nvim-drills`: a small Python project with bad names, an off-by-one bug, unused imports and a failing test. This lesson is for LazyVim, where the leader key is Space.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open the practice project in Neovim", "code": "cd Terminal-Workflow/practice/nvim-drills\nv .",
                         "expect": "Neovim opens on the project, ready for the exercises."},
                        {"type": "text", "body": "Do the exercises in order. Do the git exercises on page 2 before the `calc` rename on page 3, because the reset script would silently undo your rename."},
                    ],
                },
                {
                    "h2": "Jump to a definition or find every use of a function",
                    "intro": "LSP is already set up for each language. Open a file and it works.",
                    "blocks": [
                        K("Jump to a definition, a use or the docs (LSP keys)", LSP_NAV),
                        {"type": "text", "body": "Prefer the built-in maps? Neovim 0.11 also ships native `gr*` LSP maps that work alongside the above: `grn` rename, `gra` code action, `grr` references, `gri` implementation, `grt` type definition. Use `gd` and `gr` as your primaries; the `gr*` set is a fallback."},
                        K("Find every place a function is called", [
                            ("<Space>sf orders.py", "Find and open orders.py"),
                            ("gd", "Go to definition: jumps to `def calc(o):` a few lines down"),
                            ("gr", "Find every use of `calc`: opens the references list"),
                            ("Ctrl-o", "Jump back to where you started"),
                        ], **{"try": "In `all_totals`, put the cursor on `calc` in `return [calc(o) for o in self.orders]`, then press `gd` and `gr`.",
                              "expect": "The references list shows 3 files: `orders.py`, `report.py` and `tests/test_orders.py`. Open the `report.py` hit, then `Ctrl-o` jumps straight back."}),
                    ],
                },
                {
                    "h2": "Find errors, warnings and unused imports",
                    "intro": "Find the two modules that `src/orders.py` imports but never uses.",
                    "blocks": [
                        K("Jump between errors and warnings", DIAG),
                        K("Find the unused imports in a file", [
                            ("gg", "Go to the top of orders.py"),
                            ("]d", "Jump to the first unused-import warning"),
                            ("]d", "Jump to the second unused-import warning"),
                            ("<Space>cd", "Show the exact diagnostic over the cursor line in a float"),
                            ("<Space>sd", "List every diagnostic reported by Neovim (open buffers): picker"),
                        ], **{"try": "Open `orders.py` and press the keys in order.",
                              "expect": "`<Space>sd` lists exactly 2 diagnostics, both unused import in `orders.py`. Leave them for page 3."}),
                        {"type": "cmd", "where": "shell", "title": "No errors showing in Neovim? Check with ruff", "code": "ruff check src/orders.py",
                         "expect": "The same two `F401` findings (unused imports), per the repo's `pyproject.toml`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which language server and which keys do I use?",
                "cards": [
                    ("Which language server does each language use?", "Each language has its own server, formatter and linter.", ["Language", "LSP", "Formatter", "Linter"], [
                        ["Python", "basedpyright", "ruff", "ruff + mypy"],
                        ["Scala", "Metals", "Metals", "Metals"],
                        ["Bash", "bashls", "shfmt", "shellcheck"],
                        ["TypeScript", "ts_ls", "prettier", "eslint"],
                        ["YAML", "yamlls", "prettier", "—"],
                        ["JSON", "jsonls", "prettier", "—"],
                        ["Lua", "lua_ls", "stylua", "—"],
                        ["Docker", "dockerls", "—", "—"],
                    ]),
                    ("Which LSP keys do I use most?", "The nine you reach for first.", ["Keys", "Action"], [
                        ["`gd`", "Jump to the definition"],
                        ["`gr` / `grr`", "Find every use: references"],
                        ["`gri`", "Jump to the implementation"],
                        ["`grn`", "Rename a symbol (built in)"],
                        ["`gra`", "Fix or refactor: code action"],
                        ["`K`", "Show docs under the cursor: hover"],
                        ["`]d/[d`", "Jump to the next / previous error or warning"],
                        ["`<Space>xx`", "Open the errors and warnings panel: Trouble"],
                        ["`<Space>cf`", "Format the file (buffer)"],
                    ]),
                    ("What do I do when LSP does not work?", "Check the server first.", ["Problem", "Run"], [
                        ["LSP is not working", "`:checkhealth lsp`, `:Mason`, `:LspInfo`"],
                        ["Scala Metals is broken", "`rm -rf .metals/ .bloop/ metals.sbt`, reopen the file, accept Import build"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find every place a function is used",
                "frame": "Find what depends on `calc_totl` before you rename it.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 19, on `calc_totl`", "`19G` `fc`"), "`gd`", "Jumps to `def calc_totl` on line 6."),
                    (None, "`Ctrl-o`", "Back to line 19."),
                    (None, "`gr`", "Lists every reference."),
                    (None, "`Enter` on the line 12 hit, then `Ctrl-o`", "Opens it, then returns."),
                ],
                "after": "orders.py:6:5    def calc_totl(price, qty):\norders.py:12:21  print(code, calc_totl(PRICES[code], 2))\norders.py:19:9   total = calc_totl(price, qty)",
                "meaning": "Find real uses only: the list comes from the language server, so it holds real references and no text matches.",
            },
            "practice": {
                "h2": "Check how to jump to a definition and find errors",
                "qs": [
                    ("Mechanism", "Why is `gr` better than grepping for a function name?",
                     "What does the server understand that grep does not?",
                     ["Grep matches text.", "The server knows scope and symbols."],
                     "`gr` shows only real references to that symbol."),
                    ("Keystrokes", "How do I jump to a definition and then come back?",
                     "Two keys out, one key back.",
                     ["Press `gd`.", "Press `Ctrl-o`."],
                     "`gd`, then `Ctrl-o` (or `Ctrl-t`)."),
                    ("Application", "How do I list every error and warning in the open files?",
                     "It is a picker under the search prefix.",
                     ["Press `<Space>sd`."],
                     "`<Space>sd`."),
                    ("Common mistake", "Why do no errors or warnings show at all? What do I try?",
                     "Is the linter wired up?",
                     ["The environment may lack ruff or basedpyright.", "Run `ruff check src/orders.py` in a terminal."],
                     "Run `ruff check` from a terminal."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Stage, commit and review git changes in Neovim",
            "subtitle": "Stage one changed block, discard a change, commit with LazyGit, see who changed a line, review a diff",
            "idea": (
                "Stage or discard one changed block (hunk) at a time, without leaving the editor.",
                [
                    ("Jump to the next changed block", "]h", "Go to the next hunk."),
                    ("Stage only one changed block", "<Space>ghs", "Stage only that block."),
                    ("Open the full git screen", "<Space>gg", "LazyGit, inside Neovim."),
                    ("See a side-by-side diff of your changes", "<Space>gv", "Diffview of the working tree."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I stage only part of a file? `git add` stages the whole file, and half the change may be a leftover experiment.",
                "fix": "Stage and discard hunk by hunk with gitsigns, and commit from LazyGit.",
            },
            "drills": [
                {
                    "h2": "See which lines changed and stage one block (gitsigns)",
                    "intro": "Changed lines are marked in the gutter. These keys act on the block under the cursor.",
                    "blocks": [
                        K("Stage, discard or preview a changed block", GITSIGNS),
                        {"type": "text", "body": "See who changed a line: inline blame is already on. Pause on a line for 300 ms and its author, relative time and commit summary appear at the end of the line."},
                    ],
                },
                {
                    "h2": "Stage one change and discard another",
                    "intro": "Open a terminal with `<Space>ft` in the `nvim-drills` root and reset the repo to a dirty state.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create two changes and a new file to practice on", "code": "./scripts/reset-dirty.sh",
                         "expect": "Two unstaged hunks and one untracked file: `src/calculator.py` (new `average()`), `src/orders.py` (new TODO in `calc`) and `src/scratch.py`. Safe to re-run any time."},
                        K("Stage one changed block and discard the other", [
                            ("]h", "In `src/calculator.py`, jump to the new hunk"),
                            ("<Space>ghp", "Preview what changed in this hunk, inline"),
                            ("<Space>ghs", "Stage it (you are keeping `average()`)"),
                            ("]h", "In `src/orders.py`, jump to its hunk"),
                            ("<Space>ghr", "Discard it (the TODO is not worth keeping)"),
                        ], **{"try": "Open `src/calculator.py` and press the keys in order, then do the same in `src/orders.py`.",
                              "expect": "`:DiffviewOpen` shows `orders.py` clean, with no diff."}),
                        {"type": "cmd", "where": "shell", "title": "Check what is staged (git status)", "code": "git status --short",
                         "expect": "`M  src/calculator.py` (staged) and `?? src/scratch.py` (still untracked), but no entry for `orders.py`."},
                    ],
                },
                {
                    "h2": "Commit and manage git from one screen (LazyGit)",
                    "intro": "Open a complete git interface in a float. Press `?` inside it for every key.",
                    "blocks": [
                        K("Open LazyGit", LAZYGIT_OPEN),
                        K("Stage, commit, push and pull in LazyGit", LAZYGIT_KEYS, where="lazygit"),
                        K("Stage a new file and commit it", [
                            ("<Space>gg", "Open LazyGit"),
                            ("Space", "On `src/scratch.py` in the files panel: stage it"),
                            ("c", "Commit the staged files: type a message such as Add average() and a scratch file"),
                            ("q", "Quit LazyGit and go back to Neovim"),
                        ]),
                        {"type": "cmd", "where": "shell", "title": "Check that your commit is in the log", "code": "git log --oneline -1",
                         "expect": "Your new commit on top of `Add messy.py for reformat/auto-indent drills`."},
                    ],
                },
                {
                    "h2": "Search the git log, history, status and diffs",
                    "intro": "Fuzzy lists for logs, history, status and diffs.",
                    "blocks": [
                        K("Search git history and status in a picker", SNACKS_GIT),
                        {"type": "text", "body": "To list GitHub issues and pull requests, you need the GitHub CLI and access to the repository."},
                    ],
                },
                {
                    "h2": "See a side-by-side diff or a file's history (Diffview)",
                    "intro": "Diffview uses its own keys, which do not overlap with the Snacks diff pickers.",
                    "blocks": [
                        K("Open Diffview", DIFFVIEW_OPEN),
                        {"type": "cmd", "where": "nvim", "title": "Open either view with a command", "code": ":DiffviewOpen\n:DiffviewFileHistory %",
                         "expect": "The first opens the working-tree diff. The second opens the history of the current file."},
                        K("Move between files and fix merge conflicts in Diffview", DIFFVIEW_KEYS),
                        {"type": "text", "body": "Why you should never press `X` in Diffview: it restores the selected entry to the left-side state and can remove an untracked file. This conflicts with the no-delete rule."},
                        {"type": "text", "body": "How do I get a clean slate later? Run `./scripts/reset-dirty.sh` from the `nvim-drills` root: the purpose-built reset path."},
                    ],
                },
                {
                    "h2": "Merge a branch into main and squash your last commits",
                    "intro": "Two git jobs people search for by name. The demos run in a throwaway repo, not in `nvim-drills`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Merge a branch into main (git merge)", "code": C('''
cd "$(mktemp -d)"
git init -q -b main
git config user.name demo && git config user.email demo@example.com
echo one > app.txt && git add app.txt && git commit -qm "first commit"
git switch -q -c feature
echo two >> app.txt && git commit -qam "add feature"
git switch -q main
git merge feature
git log --oneline
'''),
                         "expect": "`Updating <hash>..<hash>`, `Fast-forward`, ` app.txt | 1 +` and ` 1 file changed, 1 insertion(+)`. Then `git log --oneline` prints `<hash> add feature` and `<hash> first commit`. The hashes differ. It is a fast-forward because main had no new commits; when main has moved on, git makes a merge commit and opens an editor for its message."},
                        {"type": "cmd", "where": "shell", "title": "Squash my last 3 commits into one (git reset --soft)", "code": C('''
cd "$(mktemp -d)"
git init -q -b main
git config user.name demo && git config user.email demo@example.com
echo base > app.txt && git add app.txt && git commit -qm "base"
for n in 1 2 3; do echo "change $n" >> app.txt; git commit -qam "wip $n"; done
git log --oneline
git reset --soft HEAD~3
git commit -qm "add the feature"
git log --oneline
'''),
                         "expect": "The first `git log --oneline` prints four lines: `wip 3`, `wip 2`, `wip 1`, `base`, each after a hash. The second prints two: `add the feature` and `base`. The hashes differ. `reset --soft HEAD~3` moves the branch back three commits and keeps all their changes staged, so one `git commit` makes them a single commit."},
                        {"type": "text", "body": "Squash the last 3 commits another way: `git rebase -i HEAD~3`, then change `pick` to `squash` (or `s`) on the second and third lines. Squash while you merge a branch: `git merge --squash feature`, then `git commit`. Never squash commits you have already pushed and shared."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which git keys do I use most?",
                "cards": [
                    ("Which git keys do I use every day?", "The seven you use daily.", ["Keys", "Action"], [
                        ["`<Space>gg`", "Open LazyGit"],
                        ["`<Space>gd`", "Show the git diff, hunk by hunk (Snacks)"],
                        ["`<Space>gD`", "Show the git diff against origin"],
                        ["`<Space>gs`", "Show git status"],
                        ["`]h/[h`", "Jump to the next / previous hunk"],
                        ["`<Space>ghs`", "Stage this hunk"],
                        ["`<Space>ghb`", "See who changed this line: blame"],
                    ]),
                    ("Do I stage one block, a whole file, or make a commit?", "Pick the smallest unit that does the job.", ["I want to", "Use"], [
                        ["Stage or discard one block", "`<Space>ghs` or `<Space>ghr`"],
                        ["Stage a whole file", "`s` in Diffview, or `Space` in LazyGit"],
                        ["Commit", "`c` in LazyGit"],
                    ]),
                    ("How do I reset the practice repo?", "Run it from the `nvim-drills` root.", ["Step", "Command"], [
                        ["Back to the dirty state", "`./scripts/reset-dirty.sh`"],
                        ["Check what you have", "`git status --short`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Keep one change and discard another before you commit",
                "frame": "In the `~/tw` repo, one note is worth keeping, one comment is a leftover and one file is new.",
                "open": "cd ~/tw\necho 'buy glue' >> todo.txt\necho '# TODO tidy' >> orders.py\necho draft > scratch.txt\nnvim todo.txt orders.py",
                "steps": [
                    (None, "`]h` then `<Space>ghs`", "Jumps to the new line in `todo.txt` and stages it."),
                    (None, "`:n`, `]h`, `<Space>ghr`, then `:w`", "In `orders.py`, discards the TODO comment and saves."),
                    (None, "`<Space>gg`, `Space` on `scratch.txt`, then `c`", "LazyGit stages the new file and commits."),
                    (None, "`q`", "Back in Neovim."),
                ],
                "after": "Add glue\n\n scratch.txt | 1 +\n todo.txt    | 1 +\n 2 files changed, 2 insertions(+)",
                "meaning": "Commit only the changes you chose: the commit holds exactly what you chose, and the discarded hunk is gone.",
            },
            "practice": {
                "h2": "Check how to stage, preview and review changes",
                "qs": [
                    ("Mechanism", "What is a hunk (a changed block)?",
                     "Think of one block in a diff.",
                     ["A diff splits a file into changed blocks.", "Each block is a hunk."],
                     "One block of changed lines."),
                    ("Keystrokes", "How do I preview a hunk and then stage it?",
                     "Both live under `<Space>gh`.",
                     ["Press `<Space>ghp`.", "Press `<Space>ghs`."],
                     "`<Space>ghp`, then `<Space>ghs`."),
                    ("Application", "How do I open the history of the file I am editing?",
                     "Diffview has a capital-V map.",
                     ["Press `<Space>gV`, or run `:DiffviewFileHistory %`."],
                     "`<Space>gV`."),
                    ("Common mistake", "Why must I never press `X` in Diffview?",
                     "What does it restore?",
                     ["`X` restores the entry to the left-side state.", "It can remove an untracked file."],
                     "It can delete an untracked file."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Rename, replace and search across the whole project",
            "subtitle": "Rename a function everywhere, replace text in every file, create or delete a file, find a file by name, search text in every file",
            "idea": (
                "Change a name once and every use updates.",
                [
                    ("Rename a function or variable everywhere", "<Space>cr", "Updates every reference in the project."),
                    ("Replace text in every file", "<Space>sr", "A preview panel for project-wide replace."),
                    ("Search text in every file", "<Space>sg", "Search file contents."),
                    ("Send every search result to a list", "Ctrl-q", "Put every picker result in the quickfix list."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I rename a function without also changing a variable, a comment and a file name that merely look alike? Find-and-replace changes them all.",
                "fix": "Use the language server to rename a symbol, and grug-far to preview every text match before it changes.",
            },
            "drills": [
                {
                    "h2": "Rename a function or variable everywhere",
                    "intro": "Rename, fix and format from one prefix.",
                    "blocks": [
                        K("Rename, fix and format code", LSP_ACTIONS),
                        {"type": "text", "body": "Show or hide inlay hints (inline type annotations) under `<Space>u`, the UI toggles menu. Verify the exact subkey in the `<Space>` which-key menu."},
                        K("Rename calc in every file", [
                            ("<Space>cr", "Rename the symbol: on `calc` in `def calc(o):`, type `calculate_total`, then Enter"),
                            ("dd", "Delete the stale `# TODO: rename this` line above it"),
                            ("gr", "Find every use of `calculate_total`: check the references"),
                        ], **{"try": "Put the cursor on `calc` at its definition and press the keys in order.",
                              "expect": "`gr` shows references in exactly 3 files (`orders.py`, `report.py`, `tests/test_orders.py`), the same 3 as before, just renamed."}),
                        {"type": "text", "body": "Why not check the rename with a plain `<Space>sg calc` grep? It also matches the local variable `calc = Calculator()` in `tests/test_calculator.py`. `gr` is scope-aware."},
                        K("Delete the unused imports", [
                            ("gg", "Go to the top of orders.py"),
                            ("dd", "Delete line 2, `import json`"),
                            ("dd", "Delete the new line 2, `import sys`"),
                            ("<Space>sd", "List every diagnostic reported by Neovim (open buffers): picker"),
                        ], **{"try": "Press the keys in order."
                              , "expect": "`<Space>sd` is now empty (0 diagnostics)."}),
                        {"type": "cmd", "where": "shell", "title": "Check the program gives the same output", "code": "python -m src.report",
                         "expect": "It still runs and prints the same totals as before: the rename and the import cleanup changed nothing."},
                    ],
                },
                {
                    "h2": "Create, rename and delete a file or folder",
                    "intro": "LazyVim does not ship Oil.nvim. To create, rename or delete (remove) a file, use the Snacks explorer, opened with `<Space>e` or `\\`.",
                    "blocks": [
                        K("Open the file explorer", EXPLORER),
                        K("Create a file, then delete it", [
                            ("<Space>e", "Open the Snacks explorer"),
                            ("a", "Add a file in `src/`: type `notes.md`, Enter"),
                            ("d", "Delete `notes.md`: press it on the file and confirm"),
                            ("<Space>sf notes", "Find the file by name"),
                        ], **{"try": "Press the keys in order.", "expect": "`<Space>sf notes` finds nothing: the file is gone."}),
                        {"type": "text", "body": "The Snacks explorer gives you picker-style navigation plus add, rename and delete on the highlighted entry. To rename many files at once, use a shell `:!mv` command."},
                        K("Open the explorer as a sidebar", NEOTREE_OPEN),
                        K("Create, rename, copy, move and delete in the explorer", NEOTREE_KEYS),
                    ],
                },
                {
                    "h2": "Replace text in every file (grug-far)",
                    "intro": "LazyVim uses grug-far, not Spectre.",
                    "blocks": [
                        K("Open search and replace for the whole project", GRUG),
                        K("Replace a constant name in two files", [
                            ("<Space>sr", "Replace text across files: on `TAX_RATE`, opens grug-far pre-filled with it"),
                            ("SALES_TAX_RATE", "Type it in the replace field"),
                            ("sync", "Apply the replacement with the panel's sync action"),
                        ], **{"try": "Check the preview first: 2 matches in `orders.py` and 3 in `report.py`, 5 in total.",
                              "expect": "`<Space>sg TAX_RATE` gives 0 hits and `<Space>sg SALES_TAX_RATE` gives 5 hits across 2 files."}),
                        K("Close the replace panel", GRUG_EXIT),
                        {"type": "text", "body": "To check a replace before it runs: grug-far previews all matches grouped by file, and you can edit the buffer to fine-tune the replacement. Plain `:%s/old/new/g` (current file) and `:cdo s/old/new/g` (over a quickfix list) still work for quick replaces."},
                    ],
                },
                {
                    "h2": "Open a terminal inside Neovim",
                    "intro": "`Ctrl-\\` and `Ctrl-/` toggle the last terminal you used. The `<Space>tf`, `<Space>tv` and `<Space>th` keys open a float, a right and a bottom terminal. All of them open in `:pwd`.",
                    "blocks": [
                        K("Show or hide a terminal", TERM_FLOAT),
                        K("Open a terminal in a float, on the right or at the bottom", TERM_SPLIT),
                        {"type": "text", "body": "Each of the three keeps its own terminal. `<Space>t` also holds the test keys (neotest), and `<Space>1`..`<Space>9` are Harpoon file jumps, not terminals."},
                        K("Get out of terminal mode", TERM_EXIT),
                        {"type": "cmd", "where": "shell", "title": "Run all the tests from a floating terminal", "code": "pytest",
                         "expect": "7 passed, 2 failed: `test_history_tracks_results` and `test_free_shipping_threshold`. A different failure means an earlier exercise went wrong, most likely the rename."},
                        {"type": "text", "body": "To hide and bring back the terminal: open it with `<Space>ft`, hide it with `Ctrl-\\ Ctrl-n` then `<Space>ft`, and bring it back with `<Space>ft`. If the venv is not active, use `python3 -m pytest`."},
                    ],
                },
                {
                    "h2": "Find a file or search text with the picker (snacks)",
                    "intro": "LazyVim uses the snacks picker, not Telescope.",
                    "blocks": [
                        K("Find a file by name", FIND),
                        {"type": "text", "body": "In the current config the find keys (`<Space><Space>`, `<Space>ff`, `<Space>sf`) and the grep keys (`<Space>/`, `<Space>sg`, `<Space>sw`) search `:pwd`, not the project root."},
                        K("Search text in every file", GREP),
                        K("Search help, keymaps, commands and more", PICKERS),
                        K("Open a result, split the window or send results to a list", PICKER_KEYS),
                        {"type": "text", "body": "These are the snacks defaults. If a key does not match, press `?` inside the picker to see its live keymap."},
                        K("Search text, send the results to the quickfix list and browse them", [
                            ("<Space>sg", "Search text in all files: type `TODO`"),
                            ("Ctrl-q", "Send every result to the quickfix list"),
                            (":copen", "Browse the list in a window"),
                            ("]q", "Jump to the next item"),
                            ("[q", "Jump to the previous item"),
                        ], **{"try": "Search `TODO`, read the file column, then send the results to quickfix.",
                              "expect": "The quickfix count matches the picker: 5 hits. Three are real code or data (`src/calculator.py`, 2 in `data/log.txt`) and 2 are in `scripts/dirty.patch`."}),
                    ],
                },
            ],
            "rules": {
                "h2": "Which keys find files, search text and replace?",
                "cards": [
                    ("Which keys find files and search text?", "The keys from the quick-start card.", ["Keys", "Action"], [
                        ["`<Space>sf`", "Find a file by name (fuzzy, in `:pwd`)"],
                        ["`<Space><Space>`", "Find a file by name (same as `<Space>sf`)"],
                        ["`<Space>sg`", "Search text in all files (grep in `:pwd`)"],
                        ["`<Space>,`", "Switch to an open buffer"],
                        ["`<Space>e`", "Open the Snacks explorer sidebar (project root)"],
                        ["`\\`", "Open or close the Snacks explorer (`:pwd`)"],
                        ["`Shift-H/L`", "Go to the previous / next buffer"],
                        ["`<Space>sr`", "Replace text across files (grug-far)"],
                    ]),
                    ("Do I rename a symbol or replace text?", "Symbol rename and text replace are different tools.", ["I want to", "Use"], [
                        ["Rename a function or variable", "`<Space>cr`"],
                        ["Replace text across files", "`<Space>sr`"],
                        ["Replace in one file", "`:%s/old/new/g`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Rename a function, then check nothing broke",
                "frame": "Fix the typo `calc_totl` everywhere at once.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 6, on `calc_totl`", "`6G` `w`"), "`<Space>cr`, `calc_total`, then `Enter`", "Renames the definition and both calls."),
                    (None, "`gr` on `calc_total`", "Three hits, one per use."),
                    (None, "`:w !python3`", "Runs the buffer without saving. The total is the same as before."),
                    (None, "`<Space>cr`, `calc_totl`, then `Enter`", "Renames it back, so `calc_totl` is there for the other pages. Autosave would have saved the rename, so `:e!` would not undo it."),
                ],
                "after": "orders.py:6:5    def calc_total(price, qty):\norders.py:12:21  print(code, calc_total(PRICES[code], 2))\norders.py:19:9   total = calc_total(price, qty)\n\npen 3 2.5 rush 8.100000000000001",
                "meaning": "Check a rename this way: the server renamed the symbol and nothing else, and the output still matches.",
            },
            "practice": {
                "h2": "Check how to rename, replace and search",
                "qs": [
                    ("Mechanism", "Why is `gr` better than `<Space>sg calc` after a rename?",
                     "One is scope-aware.",
                     ["Grep also matches the variable `calc = Calculator()`.", "`gr` follows the symbol."],
                     "`gr` shows only real references."),
                    ("Keystrokes", "How do I send every grep result to quickfix and browse it?",
                     "Picker key, then an ex command.",
                     ["Press `Ctrl-q`.", "Run `:copen`.", "Step with `]q` and `[q`."],
                     "`Ctrl-q`, `:copen`, `]q`."),
                    ("Application", "How do I rename `TAX_RATE` to `SALES_TAX_RATE` in two files?",
                     "Use the project-wide replace panel.",
                     ["Put the cursor on `TAX_RATE` and press `<Space>sr`.", "Type the new name and apply with sync."],
                     "`<Space>sr`, replace, sync."),
                    ("Common mistake", "Which key opens the floating terminal, and which key prefix runs tests?",
                     "Test and terminal keys look alike.",
                     ["`<Space>ft` is the floating terminal.", "`<Space>tf`, `<Space>tv` and `<Space>th` are terminals too. The other `<Space>t` keys run tests (neotest)."],
                     "`<Space>ft` for the float terminal; `<Space>tf`, `<Space>tv` and `<Space>th` toggle terminals; the remaining `<Space>t` keys run tests."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Run a test, read why it failed and debug it",
            "subtitle": "Run a test file, run only the test under the cursor, see why a test failed, set a breakpoint, step through a bug",
            "idea": (
                "Run tests and debug a failing test without leaving the editor.",
                [
                    ("Run every test in a file", "<Space>tt", "Run all tests in the current file."),
                    ("Run only the test under the cursor", "<Space>tr", "Run the nearest test."),
                    ("Stop the program on a line", "<Space>db", "Set a breakpoint on this line."),
                    ("Debug a failing test", "<Space>td", "Run the nearest test under the debugger."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I find out why a test fails without scattering `print()` calls through the code?",
                "fix": "Set a breakpoint, debug the test, and watch the variables change as you step.",
            },
            "drills": [
                {
                    "h2": "Run a test file and read why a test failed",
                    "intro": "Results show inline, and you can jump to failures.",
                    "blocks": [
                        K("Run, repeat and stop tests", NEOTEST),
                        K("Run a test file and see why a test failed", [
                            ("<Space>tt", "Run all tests in this file: in `tests/test_calculator.py`"),
                            ("<Space>to", "Show the test output: on the red test, see actual vs. expected"),
                            ("<Space>ts", "Open or close the test summary panel"),
                        ], **{"try": "Expect 5 green gutter signs and 1 red (`test_history_tracks_results`). Close test panels with `q`.",
                              "expect": "The summary panel shows 5/6 passed for this file. Leave it failing: it is an intentional watch-it-fail drill."}),
                    ],
                },
                {
                    "h2": "Debug a failing test step by step (DAP)",
                    "intro": "Why does `test_free_shipping_threshold` fail? `qualifies_for_free_shipping` carries a `# FIXME: off-by-one` comment. Find out why, live.",
                    "blocks": [
                        K("Set breakpoints and step through code", DAP),
                        K("Debug a test", DAP_TEST),
                        K("Find the bug in the free-shipping test", [
                            ("<Space>db", "Set a breakpoint: in `orders.py`, on `for i in range(len(items) - 1):`"),
                            ("<Space>td", "Debug the test: in `test_free_shipping_threshold`"),
                            ("<Space>du", "Open the debugger UI: watch `items` and `total_qty`"),
                            ("<Space>dO", "Step over to the next line, repeatedly"),
                            ("<Space>dt", "Stop the debug session: terminate"),
                            ("<Space>tr", "Run the nearest test again, after the fix"),
                        ], **{"try": "The loop body runs only once (`i=0`): `range(len(items) - 1)` is `range(1)` for 2 items, so `total_qty` ends at 3. Change it to `range(len(items))` and delete the `# FIXME:` comment.",
                              "expect": "The test turns green."}),
                        {"type": "cmd", "where": "shell", "title": "Check how many tests still fail", "code": "pytest",
                         "expect": "Exactly 1 failure (`test_history_tracks_results`, still intentional), down from 2."},
                        {"type": "text", "body": "To stop debugging, press `<Space>dt` (terminate) or close the UI with `<Space>du`."},
                    ],
                },
                {
                    "h2": "Make Neovim use your Python virtualenv (.venv)",
                    "intro": "If you set up `.venv` per the practice repo's README, pick it here so the LSP, debugger and tests all use the right interpreter.",
                    "blocks": [
                        K("Pick the Python virtualenv", VENV),
                        {"type": "cmd", "where": "shell", "title": "Create a virtualenv for the project", "code": "python3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt",
                         "expect": "The prompt shows `(.venv)`. Then `<Space>cv` in Neovim lets you pick it."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which keys do I press to debug a test?",
                "cards": [
                    ("Which five keys make one debug loop?", "Reproduce, stop, look, step, finish.", ["Step", "Keys"], [
                        ["Stop on a line", "`<Space>db`"],
                        ["Run the test under the debugger", "`<Space>td`"],
                        ["Look at variables", "`<Space>du`"],
                        ["Step to the next line", "`<Space>dO`"],
                        ["Stop debugging", "`<Space>dt`"],
                    ]),
                    ("Why do some tests fail in nvim-drills?", "Two tests fail by design in `nvim-drills`.", ["Test", "Status"], [
                        ["`test_history_tracks_results`", "Intentional. Leave it failing."],
                        ["`test_free_shipping_threshold`", "A real off-by-one bug. Fix it in the debugger drill."],
                    ]),
                ],
            },
            "worked": {
                "h2": "See the values behind a total while the program runs",
                "frame": "See what feeds the total that prints `8.100000000000001`.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 7", "`7G`"), "`<Space>db`", "A breakpoint marks the `return` line."),
                    (None, "`<Space>du` then `<Space>dc`", "The debugger UI opens and the run stops on line 7."),
                    (None, "`<Space>dO`", "Steps over the `return`."),
                    (None, "`<Space>dt`", "Ends the session."),
                ],
                "after": "Locals\n  price = 2.5\n  qty = 3",
                "meaning": "Read the variables to find the cause, so there is no guessing.",
            },
            "practice": {
                "h2": "Check how to run tests and debug them",
                "qs": [
                    ("Mechanism", "Why does the loop in `qualifies_for_free_shipping` run only once?",
                     "How long is `range(1)`?",
                     ["The list has 2 items.", "`range(len(items) - 1)` is `range(1)`."],
                     "The range stops one item short."),
                    ("Keystrokes", "How do I run only the test under the cursor, then show its output?",
                     "Both live under `<Space>t`.",
                     ["Press `<Space>tr`.", "Press `<Space>to`."],
                     "`<Space>tr`, then `<Space>to`."),
                    ("Application", "How do I make LSP, tests and the debugger use `.venv`?",
                     "A key under `<Space>c`.",
                     ["Press `<Space>cv`.", "Pick `.venv`."],
                     "`<Space>cv`."),
                    ("Common mistake", "After the fix, pytest still shows one failure. Is something wrong?",
                     "Check which test is left.",
                     ["`test_history_tracks_results` is intentional."],
                     "No. One intentional failure remains."),
                ],
            },
        },
    ],
}
