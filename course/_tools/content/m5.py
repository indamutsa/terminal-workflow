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
gd               Go to definition (Ctrl-t to jump back)
gr               Find all references (who uses this?)
gI               Go to implementation
gy               Go to type definition
gD               Go to declaration
gK               Signature help
gO               Document symbols (outline of current file)
K                Hover docs (press again to enter the float)
'''

DIAG = r'''
]d               Jump to next error/warning
[d               Jump to previous error/warning
<Space>xx        Toggle diagnostics panel (Trouble)
<Space>xX        Current buffer diagnostics only
<Space>sd        Search/list diagnostics (picker)
<Space>cs        Symbols outline (Aerial)
<Space>xQ        Quickfix list (Trouble)
<Space>xL        Location list (Trouble)
'''

GITSIGNS = r'''
]h               Next hunk (changed block)
[h               Previous hunk
<Space>ghs       Stage hunk
<Space>ghu       Undo stage hunk
<Space>ghr       Reset hunk (discard change)
<Space>ghS       Stage entire buffer
<Space>ghR       Reset entire buffer
<Space>ghp       Preview hunk diff inline
<Space>ghb       Detailed blame for current line
<Space>ghB       Blame the entire buffer
<Space>ghd       Diff current file
<Space>ghD       Diff current file against the previous commit
'''

LAZYGIT_OPEN = r'''
<Space>gg        Open LazyGit at the repository root
<Space>gG        Open LazyGit at the current working directory
'''

LAZYGIT_KEYS = r'''
Space            Stage/unstage file
c                Commit
P                Push
p                Pull
b                Branches
s                Stash
l                Log
?                Help (shows all keys)

EXIT:
q                Quit LazyGit (back to nvim)
'''

SNACKS_GIT = r'''
<Space>gL        Git log for the current working directory
<Space>gb        Commit history for the current line
<Space>gf        Commit history for the current file
<Space>gl        Repository log
<Space>gB        Open the current file/line on its remote (e.g. GitHub)
<Space>gY        Copy the remote URL for the current file/line
<Space>gs        Git status (picker)
<Space>gd        Git diff — hunks (picker)
<Space>gD        Git diff against origin
<Space>gS        Git stash
<Space>gi / gI   Open / all GitHub issues
<Space>gp / gP   Open / all GitHub pull requests
'''

DIFFVIEW_OPEN = r'''
<Space>gv        Open the working-tree diff
<Space>gV        Open history for the current file
'''

DIFFVIEW_KEYS = r'''
Tab / Shift-Tab  Open the next / previous changed file
Enter            Open the selected diff
s or -           Stage / unstage the selected file
S / U            Stage all / unstage all files
[x / ]x          Previous / next merge conflict
<Space>co        Choose ours for the current conflict
<Space>ct        Choose theirs for the current conflict
<Space>cb        Choose the base for the current conflict
<Space>ca        Choose all versions for the current conflict
g?               Show context-sensitive Diffview help
'''

EXPLORER = r'''
<Space>e         Toggle snacks explorer (root dir)
<Space>E         Toggle snacks explorer (cwd)
\                Toggle neo-tree sidebar (custom mapping)
'''

NEOTREE_OPEN = r'''
\                Toggle sidebar
'''

NEOTREE_KEYS = r'''
a                Add file/directory (end with / for dir)
d                Delete
r                Rename
c                Copy
m                Move
/                Filter
H                Toggle hidden files
?                Show help

EXIT:
\                Toggle sidebar off (same key that opened it)
q                Close Neo-tree
'''

LSP_ACTIONS = r'''
<Space>cr        Rename symbol across the whole project
<Space>ca        Code actions (quick fixes, auto-imports, refactors)
<Space>cf        Format file (ruff for Python, prettier for JS, etc.)
<Space>cd        Line diagnostics (float)
<Space>cl        LSP info (which servers are attached)
'''

GRUG = r'''
<Space>sr        Open search & replace panel (works on a word/selection too)
'''

GRUG_EXIT = r'''
EXIT:
q                Close grug-far panel
:q               Also works
'''

TERM_FLOAT = r'''
Ctrl-\           Toggle floating terminal
Ctrl-/           Toggle floating terminal (same one)
<Space>ft        Toggle floating terminal (same one)
'''

TERM_SPLIT = r'''
<Space>Tf        Terminal — float
<Space>Tv        Terminal — vertical split (right)
<Space>Th        Terminal — horizontal split (bottom)
'''

TERM_EXIT = r'''
EXIT TERMINAL MODE:
Ctrl-\ Ctrl-n    Leave terminal (insert) mode back to normal mode
'''

FIND = r'''
<Space>sf        Search files by name (added — your primary find-file)
<Space><Space>   Find files (built-in alias)
<Space>ff        Find files (root dir)
<Space>fF        Find files (cwd)
<Space>fr        Recent files
<Space>fg        Find git files
<Space>fb        Buffers
<Space>,         Buffers (quick switch)
<Space>fc        Find a config file
'''

GREP = r'''
<Space>/         Grep (root dir)
<Space>sg        Grep (root dir)
<Space>sG        Grep (cwd)
<Space>sw        Grep word / selection under cursor (root dir)
<Space>sb        Search lines in current buffer
<Space>sB        Grep across all open buffers
'''

PICKERS = r'''
<Space>sd        Diagnostics
<Space>sR        Resume last picker
<Space>sh        Help pages
<Space>sk        Keymaps
<Space>sC        Commands
<Space>s"        Registers
<Space>sm        Marks
<Space>sj        Jumps
<Space>st        Todo comments
'''

PICKER_KEYS = r'''
Ctrl-n / Ctrl-p  Navigate results
Ctrl-s           Open in horizontal split
Ctrl-v           Open in vertical split
Enter            Open file
Ctrl-q           Send ALL results to quickfix

EXIT:
Esc              Close the picker
Ctrl-c           Also closes it
'''

NEOTEST = r'''
<Space>tr        Run nearest test (test under cursor)
<Space>tt        Run all tests in the current file
<Space>tT        Run all test files
<Space>ts        Toggle test summary panel (see all pass/fail)
<Space>to        Show test output (print/debug output)
<Space>tO        Toggle the output panel
<Space>tl        Run last test
<Space>tw        Toggle watch mode
<Space>tS        Stop the running test
<Space>td        Debug nearest test (via DAP)
'''

DAP = r'''
<Space>db        Toggle breakpoint on current line
<Space>dB        Set conditional breakpoint (prompts for condition)
<Space>dc        Start / Continue (run)
<Space>di        Step into function
<Space>dO        Step over (next line)
<Space>do        Step out of function
<Space>dC        Run to cursor
<Space>du        Toggle debugger UI (variables, stack, breakpoints)
<Space>de        Eval expression (also works on a visual selection)
<Space>dr        Toggle REPL
<Space>dl        Run last
<Space>dt        Terminate
'''

DAP_TEST = r'''
<Space>td        Debug the nearest test (neotest + DAP)
<Space>dPt       Debug the Python test method under cursor
<Space>dPc       Debug the Python test class
'''

VENV = r'''
<Space>cv        Select the Python virtualenv/interpreter for this project
'''

MODULE = {
    "n": 5,
    "folder": "m5-lsp-git",
    "title": "Code intelligence and git",
    "footer": "LSP navigation and diagnostics; gitsigns, LazyGit and Diffview; refactor, files and search; tests and the debugger",
    "tagline": "Jump to definitions, stage hunks, rename safely and debug a test.",
    "glossary": [],
    "coverage_allow": [],
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
                            ("<Space>sf orders.py", "Open orders.py"),
                            ("gd", "Jump to `def calc(o):` a few lines down"),
                            ("gr", "Open the references list"),
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
                            ("gg", "Top of orders.py"),
                            ("]d", "First unused-import warning"),
                            ("]d", "Second unused-import warning"),
                            ("<Space>cd", "Float the exact diagnostic over the cursor line"),
                            ("<Space>sd", "Project-wide diagnostics picker"),
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
                        ["`gr` / `grr`", "Find references"],
                        ["`gri`", "Go to implementation"],
                        ["`grn`", "Rename"],
                        ["`gra`", "Code action"],
                        ["`K`", "Hover docs"],
                        ["`]d/[d`", "Next/prev diagnostic"],
                        ["`<Space>xx`", "Diagnostics panel (Trouble)"],
                        ["`<Space>cf`", "Format buffer"],
                    ]),
                    ("When LSP does not work", "Check the server first.", ["Problem", "Run"], [
                        ["LSP not working", "`:checkhealth lsp`, `:Mason`, `:LspInfo`"],
                        ["Scala Metals broken", "`rm -rf .metals/ .bloop/ metals.sbt`, reopen the file, accept Import build"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find who uses a function",
                "frame": "You want to change `calc` and need to know what breaks.",
                "given": "`src/orders.py` is open in `nvim-drills`.",
                "steps": [
                    "Put the cursor on `calc` inside `all_totals`.",
                    "Press `gd` to read the definition.",
                    "Press `Ctrl-o` to come back, then `gr` for the references.",
                    "Open the `report.py` hit, then press `Ctrl-o` again.",
                ],
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
                    ("Application", "List every diagnostic in the project.",
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
                            ("<Space>ghp", "Preview the diff inline"),
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
                            ("c", "Commit; type a message such as Add average() and a scratch file"),
                            ("q", "Back to nvim"),
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
                        ["`<Space>gg`", "LazyGit"],
                        ["`<Space>gd`", "Git Diff — hunks (snacks)"],
                        ["`<Space>gD`", "Git Diff vs origin"],
                        ["`<Space>gs`", "Git status"],
                        ["`]h/[h`", "Next/prev hunk"],
                        ["`<Space>ghs`", "Stage hunk"],
                        ["`<Space>ghb`", "Blame line"],
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
                "frame": "Your working tree has a useful change and a leftover TODO.",
                "given": "You ran `./scripts/reset-dirty.sh` in `nvim-drills`.",
                "code": "./scripts/reset-dirty.sh\ngit status --short",
                "steps": [
                    "In `src/calculator.py`, press `]h`, then `<Space>ghs` to stage the hunk.",
                    "In `src/orders.py`, press `]h`, then `<Space>ghr` to discard the TODO.",
                    "Open LazyGit with `<Space>gg`, stage `src/scratch.py` with `Space`, and press `c` to commit.",
                    "Press `q` to leave LazyGit.",
                ],
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
                            ("<Space>cr", "On `calc` in `def calc(o):`: type `calculate_total`, then Enter"),
                            ("dd", "Delete the stale `# TODO: rename this` line above it"),
                            ("gr", "On `calculate_total`: check the references"),
                        ], **{"try": "Put the cursor on `calc` at its definition and press the keys in order.",
                              "expect": "`gr` shows references in exactly 3 files (`orders.py`, `report.py`, `tests/test_orders.py`), the same 3 as before, just renamed."}),
                        {"type": "text", "body": "Do not verify with a plain `<Space>sg calc` grep. It also matches the local variable `calc = Calculator()` in `tests/test_calculator.py`. `gr` is scope-aware."},
                        K("Clean up the dead imports", [
                            ("gg", "Top of orders.py"),
                            ("dd", "Line 2 is `import json`: delete it"),
                            ("dd", "The new line 2 is `import sys`: delete it"),
                            ("<Space>sd", "Project-wide diagnostics picker"),
                        ], **{"try": "Press the keys in order."
                              , "expect": "`<Space>sd` is now empty (0 diagnostics)."}),
                        {"type": "cmd", "where": "shell", "title": "Behavior is unchanged", "code": "python -m src.report",
                         "expect": "It still runs and prints the same totals as before: the rename and the import cleanup changed nothing."},
                    ],
                },
                {
                    "h2": "File management",
                    "intro": "LazyVim does not ship Oil.nvim. File management is the snacks explorer plus neo-tree.",
                    "blocks": [
                        K("Explorers", EXPLORER),
                        K("Create and delete a scratch file", [
                            ("<Space>e", "Open the snacks explorer"),
                            ("a", "In `src/`: add a file, type `notes.md`, Enter"),
                            ("d", "On `notes.md`: delete it and confirm"),
                            ("<Space>sf notes", "Find it"),
                        ], **{"try": "Press the keys in order.", "expect": "`<Space>sf notes` finds nothing: the file is gone."}),
                        {"type": "text", "body": "The snacks explorer gives you picker-style navigation plus add, rename and delete on the highlighted entry. For bulk renames, use neo-tree or a shell `:!mv` command."},
                        K("Neo-tree sidebar", NEOTREE_OPEN),
                        K("Inside Neo-tree", NEOTREE_KEYS),
                    ],
                },
                {
                    "h2": "Search and replace across the project",
                    "intro": "LazyVim uses grug-far, not Spectre.",
                    "blocks": [
                        K("grug-far", GRUG),
                        K("Rename a constant across two files", [
                            ("<Space>sr", "On `TAX_RATE`: opens grug-far pre-filled with it"),
                            ("SALES_TAX_RATE", "Type it in the replace field"),
                            ("sync", "Apply with the panel's sync action"),
                        ], **{"try": "Check the preview first: 2 matches in `orders.py` and 3 in `report.py`, 5 in total.",
                              "expect": "`<Space>sg TAX_RATE` gives 0 hits and `<Space>sg SALES_TAX_RATE` gives 5 hits across 2 files."}),
                        K("Leave grug-far", GRUG_EXIT),
                        {"type": "text", "body": "In grug-far you preview all matches grouped by file and can edit the buffer to fine-tune the replacement. Plain `:%s/old/new/g` (current file) and `:cdo s/old/new/g` (over a quickfix list) still work for ad-hoc replaces."},
                    ],
                },
                {
                    "h2": "Terminals",
                    "intro": "Three keys toggle the same floating terminal.",
                    "blocks": [
                        K("Floating terminal", TERM_FLOAT),
                        K("Split terminals", TERM_SPLIT),
                        {"type": "text", "body": "These `<Space>T*` maps are the lesson's mapping and are not in the current config. `<Space>t` is the test prefix (neotest), and `<Space>1`..`<Space>9` are Harpoon file jumps now, not terminals."},
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
                        {"type": "text", "body": "In the current config `<Space><Space>`, `<Space>ff` and `<Space>sf` search the current directory, not the root dir."},
                        K("Grep", GREP),
                        K("Other pickers", PICKERS),
                        K("Inside the picker", PICKER_KEYS),
                        {"type": "text", "body": "These are the snacks defaults. If one does not match, press `?` inside the picker to see its live keymap."},
                        K("Grep, quickfix, browse", [
                            ("<Space>sg", "Search `TODO` across the project"),
                            ("Ctrl-q", "Send every result to the quickfix list"),
                            (":copen", "Browse the list as a window"),
                            ("]q", "Next item"),
                            ("[q", "Previous item"),
                        ], **{"try": "Search `TODO`, read the file column, then send the results to quickfix.",
                              "expect": "The quickfix count matches the picker: 5 hits. Three are real code or data (`src/calculator.py`, 2 in `data/log.txt`) and 2 are in `scripts/dirty.patch`."}),
                    ],
                },
            ],
            "rules": {
                "h2": "Files and search at a glance",
                "cards": [
                    ("Files and search", "The keys from the quick-start card.", ["Keys", "Action"], [
                        ["`<Space>sf`", "Search files (fuzzy)"],
                        ["`<Space><Space>`", "Find file (built-in alias)"],
                        ["`<Space>sg`", "Grep project (search contents)"],
                        ["`<Space>,`", "Switch buffers"],
                        ["`<Space>e`", "Snacks explorer (sidebar)"],
                        ["`\\`", "Toggle file tree (neo-tree)"],
                        ["`Shift-H/L`", "Prev/next buffer"],
                        ["`<Space>sr`", "Search & replace (grug-far)"],
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
                "frame": "`calc` is a bad name and you want it gone everywhere.",
                "given": "`orders.py` is open and the git exercises are done.",
                "steps": [
                    "Put the cursor on `calc` at `def calc(o):`.",
                    "Press `<Space>cr`, type `calculate_total` and press Enter.",
                    "Press `dd` on the stale TODO comment.",
                    "Press `gr` on `calculate_total` and count the files: 3.",
                    "Run `python -m src.report` in a terminal and compare the totals.",
                ],
                "meaning": "The server renamed the symbol and nothing else, and the report still matches.",
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
                     ["`<Space>ft` is the floating terminal.", "`<Space>t*` is neotest."],
                     "`<Space>ft` for the terminal, `<Space>t` for tests."),
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
                            ("<Space>tt", "In `tests/test_calculator.py`: run the whole file"),
                            ("<Space>to", "On the red test: see actual vs. expected"),
                            ("<Space>ts", "Toggle the summary panel"),
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
                            ("<Space>db", "In `orders.py`, on `for i in range(len(items) - 1):`: set a breakpoint"),
                            ("<Space>td", "In `test_free_shipping_threshold`: debug this test"),
                            ("<Space>du", "Open the debug UI; watch `items` and `total_qty`"),
                            ("<Space>dO", "Step over, repeatedly"),
                            ("<Space>dt", "Terminate the debug session"),
                            ("<Space>tr", "After the fix: run the test again"),
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
                "h2": "Find an off-by-one",
                "frame": "A test fails and the code looks fine.",
                "given": "`test_free_shipping_threshold` fails in `nvim-drills`.",
                "steps": [
                    "Press `<Space>db` on the `for i in range(len(items) - 1):` line.",
                    "Press `<Space>td` on the test and `<Space>du` to open the UI.",
                    "Press `<Space>dO` and watch the loop run only once.",
                    "Press `<Space>dt`, change the range to `range(len(items))` and rerun with `<Space>tr`.",
                ],
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
