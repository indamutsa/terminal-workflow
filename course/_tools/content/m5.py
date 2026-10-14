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
gd               Go to definition: jump to where a symbol is defined (Ctrl-t to jump back)
gr               Find every use of a symbol: references (who uses this?)
gI               Go to the implementation
gy               Go to the type definition
gD               Go to the declaration
gK               Show the function signature: signature help
gO               Show the outline of this file: document symbols
K                Show docs for the word under the cursor: hover (press again to enter the float)
'''

DIAG = r'''
]d               Jump to the next error or warning
[d               Jump to the previous error or warning
<Space>xx        Open or close the diagnostics panel: Trouble
<Space>xX        Show diagnostics for this buffer only
<Space>sd        List diagnostics: search them in a picker
<Space>cs        Show the symbols outline: Aerial
<Space>xQ        Show the quickfix list: Trouble
<Space>xL        Show the location list: Trouble
'''

GITSIGNS = r'''
]h               Jump to the next hunk (changed block)
[h               Jump to the previous hunk
<Space>ghs       Stage this hunk
<Space>ghu       Unstage the last staged hunk: undo stage hunk
<Space>ghr       Discard this hunk: reset hunk
<Space>ghS       Stage the whole buffer
<Space>ghR       Discard every change in the buffer: reset buffer
<Space>ghp       Preview the hunk diff inline
<Space>ghb       Show blame for this line: detailed blame
<Space>ghB       Show blame for the whole buffer
<Space>ghd       Show the diff of this file
<Space>ghD       Show the diff of this file against the previous commit
'''

LAZYGIT_OPEN = r'''
<Space>gg        Open LazyGit at the repository root
<Space>gG        Open LazyGit in the current working directory
'''

LAZYGIT_KEYS = r'''
Space            Stage or unstage the file
c                Commit the staged files
P                Push commits to the remote
p                Pull commits from the remote
3                Show the branches panel
4                Show the commits panel: the commit log
s                Stash all changes (in the files panel)
l                Move focus to the next panel
?                Show every key: help

EXIT:
q                Quit LazyGit and go back to Neovim
'''

SNACKS_GIT = r'''
<Space>gL        Show the git log for the current working directory
<Space>gb        Show the commit history for this line
<Space>gf        Show the commit history for this file
<Space>gl        Show the repository log
<Space>gB        Open this file or line on its remote (e.g. GitHub)
<Space>gY        Copy the remote URL of this file or line
<Space>gs        Show git status in a picker
<Space>gd        Show the git diff, hunk by hunk, in a picker
<Space>gD        Show the git diff against origin
<Space>gS        Show the git stashes
<Space>gi / gI   List GitHub issues: open / all
<Space>gp / gP   List GitHub pull requests: open / all
'''

DIFFVIEW_OPEN = r'''
<Space>gv        Open the working-tree diff in Diffview
<Space>gV        Open the history of this file in Diffview
'''

DIFFVIEW_KEYS = r'''
Tab / Shift-Tab  Go to the next / previous changed file
Enter            Open the selected diff
s or -           Stage or unstage the selected file
S / U            Stage all files / unstage all files
[x / ]x          Jump to the previous / next merge conflict
<Space>co        Resolve the conflict with our version: choose ours
<Space>ct        Resolve the conflict with their version: choose theirs
<Space>cb        Resolve the conflict with the base version: choose base
<Space>ca        Keep all versions of the conflict: choose all
g?               Show Diffview help for the current panel
'''

EXPLORER = r'''
<Space>e         Open or close the Snacks explorer at the project root
<Space>E         Open or close the Snacks explorer in the current working directory
\                Open or close the Snacks explorer in the current working directory (custom mapping)
'''

NEOTREE_OPEN = r'''
\                Open or close the explorer sidebar
'''

NEOTREE_KEYS = r'''
a                Add a file or directory (end with / for a directory)
d                Delete the entry
r                Rename the entry
c                Copy the entry
m                Move the entry
/                Switch between the file list and the filter box
H                Show or hide hidden files
?                Show the explorer help

EXIT:
\                Close the explorer: press the same key that opened it
q                Close the explorer
'''

LSP_ACTIONS = r'''
<Space>cr        Rename a symbol across the whole project
<Space>ca        Fix or refactor the code: code actions (quick fixes, auto-imports, refactors)
<Space>cf        Format the file (ruff for Python, prettier for JS, etc.)
<Space>cd        Show the diagnostics for this line in a float
<Space>cl        Show LSP info: which servers are attached
'''

GRUG = r'''
<Space>sr        Replace text across files: open the search and replace panel (grug-far; works on a word or selection too)
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
<Space>sf        Find a file by name in the current working directory (your primary find-file)
<Space><Space>   Find a file by name: same as <Space>sf, in the current working directory
<Space>ff        Find a file by name in the current working directory
<Space>fF        Find a file by name in the current working directory (same as <Space>ff)
<Space>fr        Open a recent file
<Space>fg        Find a git-tracked file in the current working directory
<Space>fb        Switch to an open buffer
<Space>,         Switch to an open buffer: quick switch
<Space>fc        Find a config file
'''

GREP = r'''
<Space>/         Search text in all files: grep in the current working directory
<Space>sg        Search text in all files: grep in the current working directory
<Space>sG        Search text in all files: grep in the current working directory (same as <Space>sg)
<Space>sw        Search for the word or selection under the cursor: grep in the current working directory
<Space>sb        Search for a line in this buffer
<Space>sB        Search text in open files: grep in listed file buffers below the current folder
'''

PICKERS = r'''
<Space>sd        List the diagnostics
<Space>sR        Reopen the last picker: resume
<Space>sh        Search the help pages
<Space>sk        Search the keymaps
<Space>sC        Run a command by name: command list
<Space>s"        Show the registers
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
<Space>tr        Run the nearest test: the one under the cursor
<Space>tt        Run all tests in this file
<Space>tT        Run every test file
<Space>ts        Open or close the test summary panel (see all pass and fail)
<Space>to        Show the test output (print and debug output)
<Space>tO        Open or close the output panel
<Space>tl        Run the last test again
<Space>tw        Turn watch mode on or off
<Space>tS        Stop the running test
<Space>td        Debug the nearest test (via DAP)
'''

DAP = r'''
<Space>db        Set or clear a breakpoint on this line
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
    "title": "Code intelligence and git",
    "footer": "LSP navigation and diagnostics; gitsigns, LazyGit and Diffview; refactor, files and search; tests and the debugger",
    "tagline": "Jump to definitions, stage hunks, rename safely and debug a test.",
    "glossary": [],
    "coverage_allow": [
        ("<Space>Tf", "lesson maps capital <Space>Tf; the live config has lowercase <Space>tf for the float terminal"),
        ("<Space>Tv", "lesson maps capital <Space>Tv; the live config has lowercase <Space>tv for the right terminal"),
        ("<Space>Th", "lesson maps capital <Space>Th; the live config has lowercase <Space>th for the bottom terminal"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Navigate code with LSP",
            "subtitle": "Jump to definitions and references, and read diagnostics without leaving the editor.",
            "idea": (
                "The language server knows what your code means. Ask it instead of searching text.",
                [
                    ("Definition", "gd", "Jump to where a name is defined."),
                    ("References", "gr", "List every real use of a name."),
                    ("Next problem", "]d", "Jump to the next error or warning."),
                    ("Jump back", "Ctrl-o", "Return to where you started."),
                ],
                None,
            ),
            "problem": {
                "fail": "You grep the project for a function name and wade through comments, strings and unrelated matches.",
                "fix": "Ask the language server. `gd` jumps to the definition and `gr` lists the real references.",
            },
            "drills": [
                {
                    "h2": "Open the practice project",
                    "intro": "Every exercise runs against `nvim-drills`: a small Python project with bad names, an off-by-one bug, unused imports and a failing test. This lesson is for LazyVim, where the leader key is Space.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open nvim-drills", "code": "cd Terminal-Workflow/practice/nvim-drills\nv .",
                         "expect": "Neovim opens on the project, ready for the exercises."},
                        {"type": "text", "body": "Work top to bottom. Do the git exercises on page 2 before the `calc` rename on page 3, because the reset script would silently undo your rename."},
                    ],
                },
                {
                    "h2": "Navigation",
                    "intro": "LSP is already configured per language. Open a file and it works.",
                    "blocks": [
                        K("LSP navigation", LSP_NAV),
                        {"type": "text", "body": "Neovim 0.11 also ships native `gr*` LSP maps that work alongside the above: `grn` rename, `gra` code action, `grr` references, `gri` implementation, `grt` type definition. Use `gd` and `gr` as your primaries; the `gr*` set is a fallback."},
                        K("Trace a function to every caller", [
                            ("<Space>sf orders.py", "Find and open orders.py"),
                            ("gd", "Go to definition: jumps to `def calc(o):` a few lines down"),
                            ("gr", "Find every use of `calc`: opens the references list"),
                            ("Ctrl-o", "Jump back to where you started"),
                        ], **{"try": "In `all_totals`, put the cursor on `calc` in `return [calc(o) for o in self.orders]`, then press `gd` and `gr`.",
                              "expect": "The references list shows 3 files: `orders.py`, `report.py` and `tests/test_orders.py`. Open the `report.py` hit, then `Ctrl-o` jumps straight back."}),
                    ],
                },
                {
                    "h2": "Diagnostics",
                    "intro": "`src/orders.py` imports two modules it never uses. Find them.",
                    "blocks": [
                        K("Diagnostic keys", DIAG),
                        K("Find the dead imports", [
                            ("gg", "Go to the top of orders.py"),
                            ("]d", "Jump to the first unused-import warning"),
                            ("]d", "Jump to the second unused-import warning"),
                            ("<Space>cd", "Show the exact diagnostic over the cursor line in a float"),
                            ("<Space>sd", "List every diagnostic reported by Neovim (open buffers): picker"),
                        ], **{"try": "Open `orders.py` and press the keys in order.",
                              "expect": "`<Space>sd` lists exactly 2 diagnostics, both unused import in `orders.py`. Leave them for page 3."}),
                        {"type": "cmd", "where": "shell", "title": "No diagnostics in Neovim? Ask ruff", "code": "ruff check src/orders.py",
                         "expect": "The same two `F401` findings (unused imports), per the repo's `pyproject.toml`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Servers and quick keys",
                "cards": [
                    ("Supported languages", "Each language has its own server, formatter and linter.", ["Language", "LSP", "Formatter", "Linter"], [
                        ["Python", "basedpyright", "ruff", "ruff + mypy"],
                        ["Scala", "Metals", "Metals", "Metals"],
                        ["Bash", "bashls", "shfmt", "shellcheck"],
                        ["TypeScript", "ts_ls", "prettier", "eslint"],
                        ["YAML", "yamlls", "prettier", "—"],
                        ["JSON", "jsonls", "prettier", "—"],
                        ["Lua", "lua_ls", "stylua", "—"],
                        ["Docker", "dockerls", "—", "—"],
                    ]),
                    ("LSP keys at a glance", "The nine you reach for first.", ["Keys", "Action"], [
                        ["`gd`", "Go to definition"],
                        ["`gr` / `grr`", "Find every use: references"],
                        ["`gri`", "Go to the implementation"],
                        ["`grn`", "Rename a symbol (built in)"],
                        ["`gra`", "Fix or refactor: code action"],
                        ["`K`", "Show docs under the cursor: hover"],
                        ["`]d/[d`", "Jump to the next / previous diagnostic"],
                        ["`<Space>xx`", "Open the diagnostics panel: Trouble"],
                        ["`<Space>cf`", "Format the buffer"],
                    ]),
                    ("When LSP does not work", "Check the server first.", ["Problem", "Run"], [
                        ["LSP not working", "`:checkhealth lsp`, `:Mason`, `:LspInfo`"],
                        ["Scala Metals broken", "`rm -rf .metals/ .bloop/ metals.sbt`, reopen the file, accept Import build"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find who uses a function",
                "frame": "You want to rename `calc_totl` and need to know what it touches.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 19, on `calc_totl`", "`19G` `fc`"), "`gd`", "Jumps to `def calc_totl` on line 6."),
                    (None, "`Ctrl-o`", "Back to line 19."),
                    (None, "`gr`", "Lists every reference."),
                    (None, "`Enter` on the line 12 hit, then `Ctrl-o`", "Opens it, then returns."),
                ],
                "after": "orders.py:6:5    def calc_totl(price, qty):\norders.py:12:21  print(code, calc_totl(PRICES[code], 2))\norders.py:19:9   total = calc_totl(price, qty)",
                "meaning": "The list comes from the language server, so it holds real references and no text matches.",
            },
            "practice": {
                "h2": "Practice: LSP",
                "qs": [
                    ("Mechanism", "Why is `gr` better than grepping a name?",
                     "What does the server understand that grep does not?",
                     ["Grep matches text.", "The server knows scope and symbols."],
                     "`gr` shows only real references to that symbol."),
                    ("Keystrokes", "Jump to a definition, then return.",
                     "Two keys out, one key back.",
                     ["Press `gd`.", "Press `Ctrl-o`."],
                     "`gd`, then `Ctrl-o` (or `Ctrl-t`)."),
                    ("Application", "List every diagnostic reported by Neovim (open buffers).",
                     "It is a picker under the search prefix.",
                     ["Press `<Space>sd`."],
                     "`<Space>sd`."),
                    ("Common mistake", "No diagnostics show at all. What do you try?",
                     "Is the linter wired up?",
                     ["The environment may lack ruff or basedpyright.", "Run `ruff check src/orders.py` in a terminal."],
                     "Run `ruff check` from a terminal."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Git inside Neovim",
            "subtitle": "Stage hunks, commit from LazyGit and review changes in Diffview.",
            "idea": (
                "Review and stage changes where you edit, one hunk at a time.",
                [
                    ("Next hunk", "]h", "Jump to the next changed block."),
                    ("Stage hunk", "<Space>ghs", "Stage only that block."),
                    ("LazyGit", "<Space>gg", "The full git UI inside Neovim."),
                    ("Diffview", "<Space>gv", "A side-by-side view of the working tree."),
                ],
                None,
            ),
            "problem": {
                "fail": "You stage whole files with `git add`, then discover half the change was a leftover experiment.",
                "fix": "Stage and discard hunk by hunk with gitsigns, and commit from LazyGit.",
            },
            "drills": [
                {
                    "h2": "Gitsigns: inline changes",
                    "intro": "Changed lines are marked in the gutter. These keys act on the block under the cursor.",
                    "blocks": [
                        K("Gitsigns hunk keys", GITSIGNS),
                        {"type": "text", "body": "Inline blame is already on: pause on a line for 300 ms and its author, relative time and commit summary appear at the end of the line."},
                    ],
                },
                {
                    "h2": "Stage one hunk, discard another",
                    "intro": "Open a terminal with `<Space>ft` in the `nvim-drills` root and reset the repo to a dirty state.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make two hunks and an untracked file", "code": "./scripts/reset-dirty.sh",
                         "expect": "Two unstaged hunks and one untracked file: `src/calculator.py` (new `average()`), `src/orders.py` (new TODO in `calc`) and `src/scratch.py`. Safe to re-run any time."},
                        K("Stage one, discard the other", [
                            ("]h", "In `src/calculator.py`, jump to the new hunk"),
                            ("<Space>ghp", "Preview the hunk diff inline"),
                            ("<Space>ghs", "Stage it (you are keeping `average()`)"),
                            ("]h", "In `src/orders.py`, jump to its hunk"),
                            ("<Space>ghr", "Discard it (the TODO is not worth keeping)"),
                        ], **{"try": "Open `src/calculator.py` and press the keys in order, then do the same in `src/orders.py`.",
                              "expect": "`:DiffviewOpen` shows `orders.py` clean, with no diff."}),
                        {"type": "cmd", "where": "shell", "title": "Check the status", "code": "git status --short",
                         "expect": "`M  src/calculator.py` (staged) and `?? src/scratch.py` (still untracked), but no entry for `orders.py`."},
                    ],
                },
                {
                    "h2": "LazyGit: the full git UI",
                    "intro": "A complete git interface in a float. Press `?` inside it for every key.",
                    "blocks": [
                        K("Open LazyGit", LAZYGIT_OPEN),
                        K("Inside LazyGit", LAZYGIT_KEYS, where="lazygit"),
                        K("Stage, commit and verify", [
                            ("<Space>gg", "Open LazyGit"),
                            ("Space", "On `src/scratch.py` in the files panel: stage it"),
                            ("c", "Commit the staged files: type a message such as Add average() and a scratch file"),
                            ("q", "Quit LazyGit and go back to Neovim"),
                        ]),
                        {"type": "cmd", "where": "shell", "title": "Verify the commit", "code": "git log --oneline -1",
                         "expect": "Your new commit on top of `Add messy.py for reformat/auto-indent drills`."},
                    ],
                },
                {
                    "h2": "Snacks git pickers",
                    "intro": "Fuzzy lists for logs, history, status and diffs.",
                    "blocks": [
                        K("Git pickers", SNACKS_GIT),
                        {"type": "text", "body": "The GitHub issue and pull-request pickers need the GitHub CLI and access to the repository."},
                    ],
                },
                {
                    "h2": "Diffview: side-by-side diffs and history",
                    "intro": "Your Diffview setup uses its own mappings, which do not overlap with the Snacks diff pickers.",
                    "blocks": [
                        K("Open Diffview", DIFFVIEW_OPEN),
                        {"type": "cmd", "where": "nvim", "title": "Or open either view by command", "code": ":DiffviewOpen\n:DiffviewFileHistory %",
                         "expect": "The first opens the working-tree diff. The second opens the history of the current file."},
                        K("Essential keys inside Diffview", DIFFVIEW_KEYS),
                        {"type": "text", "body": "Safety: never press `X` in Diffview. It restores the selected entry to the left-side state and can remove an untracked file. This conflicts with the no-delete rule."},
                        {"type": "text", "body": "Want a clean slate later? Run `./scripts/reset-dirty.sh` from the `nvim-drills` root: the purpose-built reset path."},
                    ],
                },
            ],
            "rules": {
                "h2": "Git keys at a glance",
                "cards": [
                    ("Git in Neovim", "The seven you use daily.", ["Keys", "Action"], [
                        ["`<Space>gg`", "Open LazyGit"],
                        ["`<Space>gd`", "Show the git diff, hunk by hunk (Snacks)"],
                        ["`<Space>gD`", "Show the git diff against origin"],
                        ["`<Space>gs`", "Show git status"],
                        ["`]h/[h`", "Jump to the next / previous hunk"],
                        ["`<Space>ghs`", "Stage this hunk"],
                        ["`<Space>ghb`", "Show blame for this line"],
                    ]),
                    ("Hunk, file or commit?", "Pick the smallest unit that does the job.", ["I want to", "Use"], [
                        ["Stage or discard one block", "`<Space>ghs` or `<Space>ghr`"],
                        ["Stage a whole file", "`s` in Diffview, or `Space` in LazyGit"],
                        ["Commit", "`c` in LazyGit"],
                    ]),
                    ("Reset the practice repo", "Run it from the `nvim-drills` root.", ["Step", "Command"], [
                        ["Back to the dirty state", "`./scripts/reset-dirty.sh`"],
                        ["Check what you have", "`git status --short`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Keep one change, drop another",
                "frame": "In the `~/tw` repo, one note is worth keeping, one comment is a leftover and one file is new.",
                "open": "cd ~/tw\necho 'buy glue' >> todo.txt\necho '# TODO tidy' >> orders.py\necho draft > scratch.txt\nnvim todo.txt orders.py",
                "steps": [
                    (None, "`]h` then `<Space>ghs`", "Jumps to the new line in `todo.txt` and stages it."),
                    (None, "`:n`, `]h`, `<Space>ghr`, then `:w`", "In `orders.py`, discards the TODO comment and saves."),
                    (None, "`<Space>gg`, `Space` on `scratch.txt`, then `c`", "LazyGit stages the new file and commits."),
                    (None, "`q`", "Back in Neovim."),
                ],
                "after": "Add glue\n\n scratch.txt | 1 +\n todo.txt    | 1 +\n 2 files changed, 2 insertions(+)",
                "meaning": "The commit holds exactly what you chose, and the discarded hunk is gone.",
            },
            "practice": {
                "h2": "Practice: git in Neovim",
                "qs": [
                    ("Mechanism", "What is a hunk?",
                     "Think of one block in a diff.",
                     ["A diff splits a file into changed blocks.", "Each block is a hunk."],
                     "One block of changed lines."),
                    ("Keystrokes", "Preview a hunk, then stage it.",
                     "Both live under `<Space>gh`.",
                     ["Press `<Space>ghp`.", "Press `<Space>ghs`."],
                     "`<Space>ghp`, then `<Space>ghs`."),
                    ("Application", "Open the history of the file you are editing.",
                     "Diffview has a capital-V map.",
                     ["Press `<Space>gV`, or run `:DiffviewFileHistory %`."],
                     "`<Space>gV`."),
                    ("Common mistake", "Why must you never press `X` in Diffview?",
                     "What does it restore?",
                     ["`X` restores the entry to the left-side state.", "It can remove an untracked file."],
                     "It can delete an untracked file."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Refactor, files and project search",
            "subtitle": "Rename across the project, manage files, replace everywhere and search with pickers.",
            "idea": (
                "Change a name once and let the tools update every use.",
                [
                    ("Rename symbol", "<Space>cr", "Updates every reference in the project."),
                    ("Replace everywhere", "<Space>sr", "A preview panel for project-wide replace."),
                    ("Grep", "<Space>sg", "Search file contents."),
                    ("To quickfix", "Ctrl-q", "Send every picker result to a list."),
                ],
                None,
            ),
            "problem": {
                "fail": "You rename a function with find-and-replace and also change a variable, a comment and a file name that merely look alike.",
                "fix": "Use the language server to rename a symbol, and grug-far to preview every text match before it changes.",
            },
            "drills": [
                {
                    "h2": "LSP actions: rename a symbol",
                    "intro": "Rename, fix and format from one prefix.",
                    "blocks": [
                        K("Code actions", LSP_ACTIONS),
                        {"type": "text", "body": "Inlay hints (inline type annotations) toggle under `<Space>u`, the UI toggles menu. Verify the exact subkey in the `<Space>` which-key menu."},
                        K("Rename calc project-wide", [
                            ("<Space>cr", "Rename the symbol: on `calc` in `def calc(o):`, type `calculate_total`, then Enter"),
                            ("dd", "Delete the stale `# TODO: rename this` line above it"),
                            ("gr", "Find every use of `calculate_total`: check the references"),
                        ], **{"try": "Put the cursor on `calc` at its definition and press the keys in order.",
                              "expect": "`gr` shows references in exactly 3 files (`orders.py`, `report.py`, `tests/test_orders.py`), the same 3 as before, just renamed."}),
                        {"type": "text", "body": "Do not verify with a plain `<Space>sg calc` grep. It also matches the local variable `calc = Calculator()` in `tests/test_calculator.py`. `gr` is scope-aware."},
                        K("Clean up the dead imports", [
                            ("gg", "Go to the top of orders.py"),
                            ("dd", "Delete line 2, `import json`"),
                            ("dd", "Delete the new line 2, `import sys`"),
                            ("<Space>sd", "List every diagnostic reported by Neovim (open buffers): picker"),
                        ], **{"try": "Press the keys in order."
                              , "expect": "`<Space>sd` is now empty (0 diagnostics)."}),
                        {"type": "cmd", "where": "shell", "title": "Behavior is unchanged", "code": "python -m src.report",
                         "expect": "It still runs and prints the same totals as before: the rename and the import cleanup changed nothing."},
                    ],
                },
                {
                    "h2": "File management",
                    "intro": "LazyVim does not ship Oil.nvim. File management is the Snacks explorer, opened with `<Space>e` or `\\`.",
                    "blocks": [
                        K("Explorers", EXPLORER),
                        K("Create and delete a scratch file", [
                            ("<Space>e", "Open the Snacks explorer"),
                            ("a", "Add a file in `src/`: type `notes.md`, Enter"),
                            ("d", "Delete `notes.md`: press it on the file and confirm"),
                            ("<Space>sf notes", "Find the file by name"),
                        ], **{"try": "Press the keys in order.", "expect": "`<Space>sf notes` finds nothing: the file is gone."}),
                        {"type": "text", "body": "The snacks explorer gives you picker-style navigation plus add, rename and delete on the highlighted entry. For bulk renames, use a shell `:!mv` command."},
                        K("Explorer sidebar", NEOTREE_OPEN),
                        K("Inside the explorer", NEOTREE_KEYS),
                    ],
                },
                {
                    "h2": "Search and replace across the project",
                    "intro": "LazyVim uses grug-far, not Spectre.",
                    "blocks": [
                        K("grug-far", GRUG),
                        K("Rename a constant across two files", [
                            ("<Space>sr", "Replace text across files: on `TAX_RATE`, opens grug-far pre-filled with it"),
                            ("SALES_TAX_RATE", "Type it in the replace field"),
                            ("sync", "Apply the replacement with the panel's sync action"),
                        ], **{"try": "Check the preview first: 2 matches in `orders.py` and 3 in `report.py`, 5 in total.",
                              "expect": "`<Space>sg TAX_RATE` gives 0 hits and `<Space>sg SALES_TAX_RATE` gives 5 hits across 2 files."}),
                        K("Leave grug-far", GRUG_EXIT),
                        {"type": "text", "body": "In grug-far you preview all matches grouped by file and can edit the buffer to fine-tune the replacement. Plain `:%s/old/new/g` (current file) and `:cdo s/old/new/g` (over a quickfix list) still work for ad-hoc replaces."},
                    ],
                },
                {
                    "h2": "Terminals",
                    "intro": "`Ctrl-\\` and `Ctrl-/` toggle the last terminal you used. The `<Space>tf`, `<Space>tv` and `<Space>th` keys open a float, a right and a bottom terminal. All of them open in `:pwd`.",
                    "blocks": [
                        K("Toggle a terminal", TERM_FLOAT),
                        K("Split terminals", TERM_SPLIT),
                        {"type": "text", "body": "Each of the three keeps its own terminal. `<Space>t` also holds the test keys (neotest), and `<Space>1`..`<Space>9` are Harpoon file jumps, not terminals."},
                        K("Leave terminal mode", TERM_EXIT),
                        {"type": "cmd", "where": "shell", "title": "Run the suite from a floating terminal", "code": "pytest",
                         "expect": "7 passed, 2 failed: `test_history_tracks_results` and `test_free_shipping_threshold`. A different failure means an earlier exercise went wrong, most likely the rename."},
                        {"type": "text", "body": "Open the terminal with `<Space>ft`, hide it with `Ctrl-\\ Ctrl-n` then `<Space>ft`, and bring it back with `<Space>ft`. If the venv is not active, use `python3 -m pytest`."},
                    ],
                },
                {
                    "h2": "Fuzzy finder (snacks picker)",
                    "intro": "LazyVim uses the snacks picker, not Telescope.",
                    "blocks": [
                        K("Find", FIND),
                        {"type": "text", "body": "In the current config the find keys (`<Space><Space>`, `<Space>ff`, `<Space>sf`) and the grep keys (`<Space>/`, `<Space>sg`, `<Space>sw`) search `:pwd`, not the project root."},
                        K("Grep", GREP),
                        K("Other pickers", PICKERS),
                        K("Inside the picker", PICKER_KEYS),
                        {"type": "text", "body": "These are the snacks defaults. If one does not match, press `?` inside the picker to see its live keymap."},
                        K("Grep, quickfix, browse", [
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
                "h2": "Files and search at a glance",
                "cards": [
                    ("Files and search", "The keys from the quick-start card.", ["Keys", "Action"], [
                        ["`<Space>sf`", "Find a file by name (fuzzy, in `:pwd`)"],
                        ["`<Space><Space>`", "Find a file by name (same as `<Space>sf`)"],
                        ["`<Space>sg`", "Search text in all files (grep in `:pwd`)"],
                        ["`<Space>,`", "Switch to an open buffer"],
                        ["`<Space>e`", "Open the Snacks explorer sidebar (project root)"],
                        ["`\\`", "Open or close the Snacks explorer (`:pwd`)"],
                        ["`Shift-H/L`", "Go to the previous / next buffer"],
                        ["`<Space>sr`", "Replace text across files (grug-far)"],
                    ]),
                    ("Rename or replace?", "Symbol rename and text replace are different tools.", ["I want to", "Use"], [
                        ["Rename a function or variable", "`<Space>cr`"],
                        ["Replace text across files", "`<Space>sr`"],
                        ["Replace in one file", "`:%s/old/new/g`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Rename, then prove it",
                "frame": "`calc_totl` is a typo and you want it gone everywhere.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 6, on `calc_totl`", "`6G` `w`"), "`<Space>cr`, `calc_total`, then `Enter`", "Renames the definition and both calls."),
                    (None, "`gr` on `calc_total`", "Three hits, one per use."),
                    (None, "`:w !python3`", "Runs the buffer without saving. The total is the same as before."),
                    (None, "`<Space>cr`, `calc_totl`, then `Enter`", "Renames it back, so `calc_totl` is there for the other pages. Autosave would have saved the rename, so `:e!` would not undo it."),
                ],
                "after": "orders.py:6:5    def calc_total(price, qty):\norders.py:12:21  print(code, calc_total(PRICES[code], 2))\norders.py:19:9   total = calc_total(price, qty)\n\npen 3 2.5 rush 8.100000000000001",
                "meaning": "The server renamed the symbol and nothing else, and the output still matches.",
            },
            "practice": {
                "h2": "Practice: refactor and search",
                "qs": [
                    ("Mechanism", "Why does `gr` beat `<Space>sg calc` after a rename?",
                     "One is scope-aware.",
                     ["Grep also matches the variable `calc = Calculator()`.", "`gr` follows the symbol."],
                     "`gr` shows only real references."),
                    ("Keystrokes", "Send every grep result to quickfix and browse it.",
                     "Picker key, then an ex command.",
                     ["Press `Ctrl-q`.", "Run `:copen`.", "Step with `]q` and `[q`."],
                     "`Ctrl-q`, `:copen`, `]q`."),
                    ("Application", "Rename `TAX_RATE` to `SALES_TAX_RATE` in two files.",
                     "Use the project-wide replace panel.",
                     ["Put the cursor on `TAX_RATE` and press `<Space>sr`.", "Type the new name and apply with sync."],
                     "`<Space>sr`, replace, sync."),
                    ("Common mistake", "Which key opens the float terminal, and which prefix is for tests?",
                     "Test and terminal keys look alike.",
                     ["`<Space>ft` is the floating terminal.", "`<Space>tf`, `<Space>tv` and `<Space>th` are terminals too. The other `<Space>t` keys run tests (neotest)."],
                     "`<Space>ft` for the float terminal; `<Space>tf`, `<Space>tv` and `<Space>th` toggle terminals; the remaining `<Space>t` keys run tests."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Tests and the debugger",
            "subtitle": "Run a test file, read the failure and step through a real bug.",
            "idea": (
                "Run tests and debug without leaving the editor.",
                [
                    ("Run the file", "<Space>tt", "Run every test in the current file."),
                    ("Run nearest", "<Space>tr", "Run only the test under the cursor."),
                    ("Breakpoint", "<Space>db", "Stop on this line."),
                    ("Debug a test", "<Space>td", "Run the nearest test under the debugger."),
                ],
                None,
            ),
            "problem": {
                "fail": "A test fails and you scatter `print()` calls through the code to see why.",
                "fix": "Set a breakpoint, debug the test, and watch the variables change as you step.",
            },
            "drills": [
                {
                    "h2": "Neotest: run a file, read the failure",
                    "intro": "Results show inline, and you can jump to failures.",
                    "blocks": [
                        K("Neotest keys", NEOTEST),
                        K("Run a file and read a failure", [
                            ("<Space>tt", "Run all tests in this file: in `tests/test_calculator.py`"),
                            ("<Space>to", "Show the test output: on the red test, see actual vs. expected"),
                            ("<Space>ts", "Open or close the test summary panel"),
                        ], **{"try": "Expect 5 green gutter signs and 1 red (`test_history_tracks_results`). Close test panels with `q`.",
                              "expect": "The summary panel shows 5/6 passed for this file. Leave it failing: it is an intentional watch-it-fail drill."}),
                    ],
                },
                {
                    "h2": "DAP: debug the free-shipping bug",
                    "intro": "`test_free_shipping_threshold` fails, and `qualifies_for_free_shipping` carries a `# FIXME: off-by-one` comment. Find out why, live.",
                    "blocks": [
                        K("Debugger controls", DAP),
                        K("Test debugging", DAP_TEST),
                        K("Debug it for real", [
                            ("<Space>db", "Set a breakpoint: in `orders.py`, on `for i in range(len(items) - 1):`"),
                            ("<Space>td", "Debug the test: in `test_free_shipping_threshold`"),
                            ("<Space>du", "Open the debugger UI: watch `items` and `total_qty`"),
                            ("<Space>dO", "Step over to the next line, repeatedly"),
                            ("<Space>dt", "Stop the debug session: terminate"),
                            ("<Space>tr", "Run the nearest test again, after the fix"),
                        ], **{"try": "The loop body runs only once (`i=0`): `range(len(items) - 1)` is `range(1)` for 2 items, so `total_qty` ends at 3. Change it to `range(len(items))` and delete the `# FIXME:` comment.",
                              "expect": "The test turns green."}),
                        {"type": "cmd", "where": "shell", "title": "Count the failures", "code": "pytest",
                         "expect": "Exactly 1 failure (`test_history_tracks_results`, still intentional), down from 2."},
                        {"type": "text", "body": "Stop the debugger with `<Space>dt` (terminate) or close the UI with `<Space>du`."},
                    ],
                },
                {
                    "h2": "Python environments",
                    "intro": "If you set up `.venv` per the practice repo's README, pick it here so the LSP, debugger and tests all use the right interpreter.",
                    "blocks": [
                        K("venv-selector", VENV),
                        {"type": "cmd", "where": "shell", "title": "Create the project venv", "code": "python3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt",
                         "expect": "The prompt shows `(.venv)`. Then `<Space>cv` in Neovim lets you pick it."},
                    ],
                },
            ],
            "rules": {
                "h2": "The debug loop",
                "cards": [
                    ("Five keys, one loop", "Reproduce, stop, look, step, finish.", ["Step", "Keys"], [
                        ["Stop on a line", "`<Space>db`"],
                        ["Run the test under the debugger", "`<Space>td`"],
                        ["Look at variables", "`<Space>du`"],
                        ["Step to the next line", "`<Space>dO`"],
                        ["Stop debugging", "`<Space>dt`"],
                    ]),
                    ("Failures left on purpose", "Two tests fail by design in `nvim-drills`.", ["Test", "Status"], [
                        ["`test_history_tracks_results`", "Intentional. Leave it failing."],
                        ["`test_free_shipping_threshold`", "A real off-by-one bug. Fix it in the debugger drill."],
                    ]),
                ],
            },
            "worked": {
                "h2": "Read the values behind a total",
                "frame": "The total prints `8.100000000000001` and you want to see what feeds it.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 7", "`7G`"), "`<Space>db`", "A breakpoint marks the `return` line."),
                    (None, "`<Space>du` then `<Space>dc`", "The debugger UI opens and the run stops on line 7."),
                    (None, "`<Space>dO`", "Steps over the `return`."),
                    (None, "`<Space>dt`", "Ends the session."),
                ],
                "after": "Locals\n  price = 2.5\n  qty = 3",
                "meaning": "You saw the cause in the variables, so there was no guessing.",
            },
            "practice": {
                "h2": "Practice: tests and debugging",
                "qs": [
                    ("Mechanism", "Why does the loop in `qualifies_for_free_shipping` run only once?",
                     "How long is `range(1)`?",
                     ["The list has 2 items.", "`range(len(items) - 1)` is `range(1)`."],
                     "The range stops one item short."),
                    ("Keystrokes", "Run only the test under the cursor, then show its output.",
                     "Both live under `<Space>t`.",
                     ["Press `<Space>tr`.", "Press `<Space>to`."],
                     "`<Space>tr`, then `<Space>to`."),
                    ("Application", "Make LSP, tests and the debugger use `.venv`.",
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
