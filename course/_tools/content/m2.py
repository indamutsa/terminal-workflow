"""Module 2: Neovim essentials. Sources: lesson 02 Neovim Essentials.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


PRACTICE_DIR = "Terminal-Workflow/practice/nvim-drills"

QUICK_START = C(r'''
nvim .                              # open project

\                File tree (toggle)
<Space>sf        Search files (fuzzy)
<Space>sg        Search all file contents (grep)
i                Insert mode (type)
Esc              Normal mode (commands)
:w               Save
dd               Delete line
ci"              Change inside quotes
gg               Top of file
G                Bottom of file
u                Undo
.                Repeat last change
''')

MODULE = {
    "n": 2,
    "folder": "m2-nvim-essentials",
    "title": "Neovim essentials",
    "footer": "Open, move, search, edit, undo; buffers, terminals, splits, tabs and the leader key",
    "tagline": "Edit a real project from minute one, without the mouse.",
    "glossary": [],
    "coverage_allow": [
        ('cd "Terminal Workflow/practice/nvim-drills"', "folder renamed to Terminal-Workflow"),
        ("demo-project/", "file tree shown as the expected result of the demo-project commit"),
        ('vp() { cd "$1" && nvim . ; }', "definition replaced by usage; installed in user's config"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Open, move, save, quit",
            "subtitle": "Open the practice project, find a file, make an edit, save it and get out.",
            "idea": (
                "Four moves cover a first edit: open, find, type, save.",
                [
                    ("Open", "v .", "Opens Neovim with the file explorer."),
                    ("Find a file", "<Space>sf", "Fuzzy search by name. Your Cmd+P."),
                    ("Search text", "<Space>sg", "Grep inside every file."),
                    ("Save and quit", ":wq", "Writes the file and leaves."),
                ],
                None,
            ),
            "problem": {
                "fail": "You open Neovim and typing does nothing useful. You cannot find a file, and you cannot get out.",
                "fix": "Press `i` to type and `Esc` to stop. Save with `:w`, leave with `:q`. The exit table below gets you out of anything.",
            },
            "drills": [
                {
                    "h2": "Setup: the practice repo",
                    "intro": "Every exercise runs against a small Python project with deliberate flaws. This lesson only moves around in it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Go to the practice project", "code": C(f'''
cd {PRACTICE_DIR}
ls
'''),
                         "expect": "`ls` lists `data`, `scripts`, `src` and `tests`."},
                        {"type": "text", "body": "The project has bad names, an unused import, an off-by-one bug and a failing test. You fix none of that here. Undo a throwaway edit with `u`, or discard it with `:e!`."},
                        {"type": "cmd", "where": "shell", "title": "Smaller sandbox: the demo project", "code": C('''
cd demo-project
git init && git add -A && git commit -m "Initial commit"
'''),
                         "expect": "Git creates a repository with one commit, \"Initial commit\". The files are `src/calculator.py`, `src/app.py` and `tests/test_calculator.py`."},
                    ],
                },
                {
                    "h2": "Open a project",
                    "intro": "Run this from inside `nvim-drills`. `v` with no argument opens the dashboard. `v .` opens the file explorer.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open the project", "code": "v .          # or: nvim .",
                         "expect": "The file explorer opens. Press `Enter` on `src/calculator.py` to open it."},
                    ],
                },
                {
                    "h2": "Navigate files without a mouse",
                    "intro": "Learn `<Space>sf` and `<Space>sg`. You will use them a hundred times a day.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Find files and symbols", "rows": [
                            ("\\", "Toggle the file tree sidebar (neo-tree)"),
                            ("<Space>e", "Toggle the file explorer (snacks, the LazyVim default)"),
                            ("<Space>sf", "Search files by name (fuzzy, your Cmd+P)"),
                            ("<Space><Space>", "Find files (built-in alias for <Space>sf)"),
                            ("<Space>sg", "Search inside all files (grep)"),
                            ("<Space>/", "Grep (built-in alias for <Space>sg)"),
                            ("<Space>fr", "Recent files"),
                            ("<Space>fg", "Find git-tracked files"),
                            ("<Space>,", "Switch between open buffers"),
                            ("gd", "Go to definition of symbol under cursor"),
                            ("gr", "Find all references"),
                            ("gO", "Outline of functions/classes in current file"),
                            ("Ctrl-o", "Jump back after going to a definition"),
                        ], "try": "Press `<Space>sf`, type `orders`, press `Enter`.",
                         "expect": "`src/orders.py` opens."},
                        {"type": "text", "body": "The `<Space>s` search group: `sf` files, `sg` grep, `sw` word, `sk` keymaps, `sh` help, `sd` diagnostics, `sr` search and replace. Press `<Space>s` and wait to see them all."},
                        {"type": "keys", "where": "nvim", "title": "Find where TAX_RATE is used", "rows": [
                            ("<Space>sf", "Type orders, Enter: opens src/orders.py"),
                            ("<Space>sg", "Type TAX_RATE, Enter: greps the whole project"),
                            ("Ctrl-n / Ctrl-p", "Move between the 5 matches (2 in orders.py, 3 in report.py)"),
                            ("Enter", "Jump to the match"),
                        ], "try": "Run the three steps in order.",
                         "expect": "Matches in `src/orders.py` (the definition and its use inside `calc`) and `src/report.py` (the import line plus two f-string uses)."},
                        {"type": "keys", "where": "nvim", "title": "Jump to a definition and back", "rows": [
                            ("gd", "Jump to the `calc` definition"),
                            ("Ctrl-o", "Jump back to where you were"),
                            ("gr", "List every place `calc` is referenced"),
                        ], "try": "In `src/orders.py`, put the cursor on `calc` inside the `all_totals` list comprehension. Press `gd`, `Ctrl-o`, then `gr`.",
                         "expect": "`gr` shows references in 3 files: `orders.py`, `report.py` and `tests/test_orders.py`. Imports count as references."},
                    ],
                },
                {
                    "h2": "Edit, save, quit",
                    "intro": "The rhythm: `i` to type, `Esc` to stop, `:w` to save.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Modes and saving", "rows": [
                            ("i", "Enter insert mode (now you can type)"),
                            ("Esc", "Back to normal mode"),
                            (":w", "Save"),
                            (":q", "Quit"),
                            (":wq", "Save and quit"),
                            ("ZZ", "Save and quit (faster, no colon needed)"),
                        ], "try": "Open `src/calculator.py`, go to the blank line 2, press `i`, type `# scratch`, press `Esc`, then `:w`. Press `u`, then `:w` again.",
                         "expect": "The save, undo, save loop works and the file is left unmodified."},
                    ],
                },
            ],
            "rules": {
                "h2": "Keep these at hand",
                "cards": [
                    ("How to exit everything", "Stuck somewhere? Find the row.", ["Stuck in...", "Exit with"], [
                        ["Insert mode", "`Esc`"],
                        ["Visual mode", "`Esc`"],
                        ["Terminal mode (nvim)", "`Ctrl-\\ Ctrl-n` (then `q` or `<Space>ft` to close)"],
                        ["Picker / fuzzy finder (snacks)", "`Esc` or `Ctrl-c`"],
                        ["LazyGit", "`q`"],
                        ["Snacks explorer (`<Space>e`)", "`<Space>e` or `q`"],
                        ["Neo-tree sidebar", "`\\` or `q`"],
                        ["grug-far (search/replace)", "`q` or `:q`"],
                        ["tmux copy mode", "`q` or `Esc`"],
                        ["tmux window picker (`Ctrl-a w`)", "`Esc` or `q`"],
                        ["A command-line prompt (`:`)", "`Esc`"],
                        ["Neovim entirely", "`:q` (or `:q!` to force without saving)"],
                        ["Stuck and nothing works", "`:qa!` (force quit everything)"],
                    ]),
                    ("Quick start", "The first five minutes of Neovim.", None, QUICK_START),
                ],
            },
            "worked": {
                "h2": "Save, undo, save",
                "frame": "You make a throwaway edit and leave the file clean.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 1", "`gg`"), "`O` then `# scratch` then `Esc`", "Opens a line above and types the comment."),
                    (None, "`:w`", "Saves."),
                    (None, "`u` then `:w`", "Undoes the edit and saves the original again."),
                ],
                "before": "TAX_RATE = 0.08",
                "after": "# scratch\nTAX_RATE = 0.08",
                "meaning": "Save, undo, save is the safe loop for any throwaway edit.",
            },
            "practice": {
                "h2": "Practice: open and save",
                "qs": [
                    ("Mechanism", "Why does typing do nothing when Neovim opens?",
                     "Which mode do you start in?",
                     ["Neovim starts in normal mode, where keys are commands.", "Press `i` to enter insert mode."],
                     "Normal mode treats keys as commands. `i` switches to typing."),
                    ("Keystrokes", "Which keys save and leave in one go, without a colon?",
                     "Two capital letters.",
                     ["Make sure you are in normal mode.", "Press `ZZ`."],
                     "`ZZ`. The same as `:wq`."),
                    ("Application", "Find every use of `TAX_RATE` in the project.",
                     "Search inside files, not file names.",
                     ["Press `<Space>sg`.", "Type `TAX_RATE` and press `Enter`.", "Move through the matches with `Ctrl-n` and `Ctrl-p`."],
                     "`<Space>sg`, then `TAX_RATE`. Five matches in two files."),
                    ("Common mistake", "You are in a terminal inside Neovim and nothing navigates. What first?",
                     "Terminal mode has its own exit.",
                     ["Press `Ctrl-\\ Ctrl-n` to leave terminal mode.", "Now navigation keys work again."],
                     "`Ctrl-\\ Ctrl-n`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Move fast and search",
            "subtitle": "Jump by word, line, bracket or pattern. Hold no arrow keys.",
            "idea": (
                "Every jump has a short key. Learn the jumps and the file stops being long.",
                [
                    ("Word", "w / b / e", "Forward, back, end of word."),
                    ("Line", "0 / $ / ^", "Start, end, first non-blank."),
                    ("File", "gg / G", "Top or bottom. 42G goes to line 42."),
                    ("Search", "/pattern", "Then n and N step through the matches."),
                ],
                None,
            ),
            "problem": {
                "fail": "You hold `j` to reach line 50, overshoot, and scroll back. Finding one word means reading the whole screen.",
                "fix": "Jump with `51G`, `%` and `gg`. Search with `/pattern` and step with `n`.",
            },
            "drills": [
                {
                    "h2": "Move fast",
                    "intro": "Line numbers can drift if you edited the file earlier. `/RAW_ORDERS` then `Enter` always works too.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Movement keys", "rows": [
                            ("h/j/k/l", "Left/down/up/right (instead of arrow keys)"),
                            ("w", "Jump forward one word"),
                            ("b", "Jump back one word"),
                            ("e", "Jump to end of word"),
                            ("0", "Start of line"),
                            ("$", "End of line"),
                            ("^", "First non-whitespace character on line"),
                            ("gg", "Top of file"),
                            ("G", "Bottom of file"),
                            ("42G", "Jump to line 42 (any number works)"),
                            ("Ctrl-d", "Half-page down"),
                            ("Ctrl-u", "Half-page up"),
                            ("Ctrl-f", "Full page down"),
                            ("Ctrl-b", "Full page up"),
                            ("%", "Jump to matching bracket/paren/brace"),
                            ("{", "Previous empty line (paragraph up)"),
                            ("}", "Next empty line (paragraph down)"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Get to RAW_ORDERS and back without scrolling", "code": C('''
51G
%
gg
'''),
                         "expect": "`51G` lands on `RAW_ORDERS = [`. `%` on that `[` lands on the closing `]`, 7 lines down. `gg` is back at the top."},
                    ],
                },
                {
                    "h2": "Searching",
                    "intro": "`src/orders.py` has a TODO above `calc` and a FIXME above `qualifies_for_free_shipping`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Search keys", "rows": [
                            ("/pattern", "Search forward"),
                            ("?pattern", "Search backward"),
                            ("n", "Next match"),
                            ("N", "Previous match"),
                            ("*", "Search for word under cursor (forward)"),
                            ("#", "Search for word under cursor (backward)"),
                            ("f{char}", "Jump to next {char} on this line"),
                            ("F{char}", "Jump to previous {char} on this line"),
                            (";", "Repeat last f/F jump"),
                        ], "try": "Open `src/calculator.py`, run `/divide`, then press `n` and `N`.",
                         "expect": "You land on the `divide` method and on the `raise Exception(\"Cannot divide by zero\")` line inside it."},
                        {"type": "cmd", "where": "nvim", "title": "Find every TODO without grepping", "code": C('''
gg
/TODO
/FIXME
'''),
                         "expect": "`/TODO` and `/FIXME` each find exactly one match in `src/orders.py`."},
                        {"type": "text", "body": "Put the cursor on `calc` after the TODO comment and press `*` to jump to its next use. Use `#` to search backward and compare."},
                    ],
                },
                {
                    "h2": "Entering insert mode",
                    "intro": "Instead of `$a`, press `A`. Each variant saves a step.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Ways into insert mode", "rows": [
                            ("i", "Insert before cursor"),
                            ("a", "Insert after cursor"),
                            ("I", "Insert at start of line"),
                            ("A", "Insert at end of line"),
                            ("o", "New line below, enter insert mode"),
                            ("O", "New line above, enter insert mode"),
                            ("s", "Delete char under cursor, enter insert mode"),
                            ("S", "Delete entire line, enter insert mode"),
                            ("C", "Delete to end of line, enter insert mode"),
                        ], "try": "In `src/calculator.py` run `/clear_history`, go to the `self.history = []` line and press `o`. Type `pass  # scratch line, will discard`, press `Esc`, then discard with `:e!`.",
                         "expect": "`o` opens an indented line below. After `:e!`, `/scratch` reports pattern not found: the file is clean."},
                    ],
                },
            ],
            "rules": {
                "h2": "Movement at a glance",
                "cards": [
                    ("Movement card", "The keys that carry most of your day.", ["Keys", "Action"], [
                        ["`h/j/k/l`", "Move cursor"],
                        ["`w/b/e`", "Word forward/back/end"],
                        ["`0/$`", "Start/end of line"],
                        ["`gg/G`", "Top/bottom of file"],
                        ["`Ctrl-d/Ctrl-u`", "Half-page down/up"],
                        ["`%`", "Matching bracket"],
                        ["`/pattern`", "Search (n=next, N=prev)"],
                        ["`*/#`", "Search word under cursor"],
                        ["`f{c}/F{c}`", "Jump to char on line"],
                    ]),
                    ("If the line number drifts", "Edits move lines. Search instead.", ["Step", "Keys"], [
                        ["Jump to a line", "`51G`"],
                        ["Always works", "`/RAW_ORDERS` then `Enter`"],
                        ["Back to the top", "`gg`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find a list and its end",
                "frame": "You need `ORDERS` and its closing bracket without scrolling.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (None, "`2G`", "Jumps to line 2, the list."),
                    (("line 2, on `[`", "`f[`"), "`%`", "Jumps to the matching `]`."),
                    (None, "`gg`", "Returns to the top."),
                ],
                "after": 'ORDERS = ["A1", "A2", "A3"]\n' + " " * 26 + "^ cursor after `%`",
                "meaning": "`%` works on any bracket pair.",
            },
            "practice": {
                "h2": "Practice: moving and searching",
                "qs": [
                    ("Mechanism", "Why does `%` jump from `[` to `]`?",
                     "It matches pairs.",
                     ["`%` finds the partner of the bracket under the cursor.", "It works for (), [] and {}."],
                     "`%` jumps to the matching bracket."),
                    ("Keystrokes", "Which keys go to line 42?",
                     "A number, then a capital letter.",
                     ["Type `42`.", "Press `G`."],
                     "`42G`."),
                    ("Application", "Find the TODO and then the FIXME in `src/orders.py`.",
                     "Search twice.",
                     ["Press `gg`.", "Run `/TODO`.", "Run `/FIXME`."],
                     "`/TODO` then `/FIXME`. One match each."),
                    ("Common mistake", "You edited the file and `51G` now lands on the wrong line. What do you do?",
                     "Search, not count.",
                     ["Line numbers drift after edits.", "Run `/RAW_ORDERS` and press `Enter`."],
                     "Search for the name. It always works."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Delete, yank, paste, undo",
            "subtitle": "Cut, copy, paste and comment lines, then undo and repeat any change.",
            "idea": (
                "Delete and yank are one or two keys. Undo and repeat make mistakes cheap.",
                [
                    ("Delete a line", "dd", "Cuts the whole line."),
                    ("Copy a line", "yy", "Yank. Paste with p."),
                    ("Comment", "gcc", "Toggle a comment on the line."),
                    ("Undo", "u", "Ctrl-r redoes. . repeats."),
                ],
                None,
            ),
            "problem": {
                "fail": "You delete the wrong line and have no idea how to get it back. You retype the same edit on ten lines.",
                "fix": "Undo with `u`, redo with `Ctrl-r`, and repeat the last change with `.`.",
            },
            "drills": [
                {
                    "h2": "Delete, yank, paste",
                    "intro": "`RAW_ORDERS` in `src/orders.py` has six entries, `A1` to `A6`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Delete, yank, paste", "rows": [
                            ("dd", "Delete (cut) whole line"),
                            ("5dd", "Delete 5 lines"),
                            ("D", "Delete to end of line"),
                            ("yy", "Yank (copy) whole line"),
                            ("5yy", "Yank 5 lines"),
                            ("y$", "Yank to end of line"),
                            ("p", "Paste below / after cursor"),
                            ("P", "Paste above / before cursor"),
                            ("x", "Delete character under cursor"),
                            ("X", "Delete character before cursor (Backspace)"),
                            ("J", "Join current line with next (remove newline)"),
                            ("yyp", "Duplicate current line (yank + paste)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Commenting", "rows": [
                            ("gcc", "Toggle comment on current line"),
                            ("gc{motion}", "Comment a range (e.g., gcip = comment paragraph)"),
                            ("gc5j", "Comment 5 lines down"),
                            ("V then gc", "Select lines, then toggle comment"),
                            ("gcO", "Add comment on line above"),
                            ("gco", "Add comment on line below"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Duplicate and retire an order line", "code": C('''
/A1
yyp
gcc
gcc
dd
:%s/"A1"//gn
'''),
                         "expect": "`yyp` duplicates the `A1` line. The first `gcc` comments the duplicate out, the second brings it back, `dd` deletes it. The last command reports 1 match: a single `A1` entry."},
                    ],
                },
                {
                    "h2": "Undo, redo, repeat",
                    "intro": "The `.` command repeats your last change. Make a change, move to another word, press `.`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Undo, redo, repeat", "rows": [
                            ("u", "Undo"),
                            ("Ctrl-r", "Redo"),
                            (".", "Repeat last change (incredibly powerful)"),
                        ], "try": "In `data/log.txt`, put the cursor on `pending` in line 1, press `ciw`, type `done`, press `Esc`. On line 2 press `.`. Then `u` twice, `Ctrl-r` twice, then `:e!`.",
                         "expect": "Line 1 reads `item 1: done`, and line 2 reads `item 2: done` after `.`. After `:e!`, `/done` finds nothing: every line still says `pending`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Editing at a glance",
                "cards": [
                    ("Editing card", "The edits you repeat all day.", ["Keys", "Action"], [
                        ["`i/a/o/O`", "Enter insert mode"],
                        ["`A/I`", "Insert at end/start of line"],
                        ["`dd/D`", "Delete line / to end"],
                        ["`cc/C`", "Change line / to end"],
                        ["`yy/p`", "Copy line / paste"],
                        ["`ci\"/ci(/ci{`", "Change inside quotes/parens/braces"],
                        ["`di\"/da(`", "Delete inside/around"],
                        ["`vi{/vip`", "Select inside braces/paragraph"],
                        ["`u / Ctrl-r`", "Undo / redo"],
                        ["`.`", "Repeat last change"],
                        ["`>>  / <<`", "Indent / unindent"],
                        ["`gg=G`", "Auto-indent entire file"],
                        ["`<Space>cf`", "Format file"],
                        ["`:%s/old/new/g`", "Find and replace"],
                    ]),
                    ("Undo a throwaway edit", "Three ways back, from smallest to biggest.", ["Situation", "Keys"], [
                        ["Undo the last change", "`u`"],
                        ["Redo it", "`Ctrl-r`"],
                        ["Discard everything unsaved", "`:e!`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Mark two lines done, then undo",
                "frame": "You change one word on two lines, then take both changes back.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 1, on `pending`", "`1G` `fp`"), "`ciw` then `done` then `Esc`", "Replaces the word."),
                    (("line 2, on `pending`", "`j` `0` `fp`"), "`.`", "Repeats the same edit."),
                    (None, "`u` `u`", "Both lines say `pending` again."),
                    (None, "`Ctrl-r` `Ctrl-r`", "Both say `done` again."),
                    (None, "`:e!`", "Discards the changes and reloads the file."),
                ],
                "before": "item 1: pending\nitem 2: pending",
                "after": "item 1: done\nitem 2: done",
                "meaning": "One edit, repeated with a key, and fully reversible.",
            },
            "practice": {
                "h2": "Practice: editing and undo",
                "qs": [
                    ("Mechanism", "Why does `yyp` duplicate a line?",
                     "Two commands in a row.",
                     ["`yy` yanks the line.", "`p` pastes it below."],
                     "Yank the line, then paste it below."),
                    ("Keystrokes", "Which keys toggle a comment on the current line?",
                     "g, c, then c again.",
                     ["Press `gcc`.", "Press `gcc` again to uncomment."],
                     "`gcc`."),
                    ("Application", "Change `pending` to `done` on two lines without retyping.",
                     "Change once, then repeat.",
                     ["On the first line, run `ciw`, type `done`, press `Esc`.", "Move to the second line and press `.`."],
                     "`ciw` once, then `.`."),
                    ("Common mistake", "You edited a lesson file and want it clean. What do you run?",
                     "Reload from disk.",
                     ["`u` only undoes one step at a time.", "`:e!` discards every unsaved change."],
                     "`:e!`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Buffers, terminals, splits, tabs, leader",
            "subtitle": "Work on several files and a terminal at once, and discover keys as you go.",
            "idea": (
                "Buffers are open files. Splits and tabs arrange them. The leader key finds the rest.",
                [
                    ("Next buffer", "Shift-L", "Shift-H goes back."),
                    ("Terminal", "Ctrl-\\", "Floating terminal. Press again to hide."),
                    ("Split", ":vsplit file.py", "Two files side by side."),
                    ("Discover", "<Space>", "Wait for the which-key menu."),
                ],
                None,
            ),
            "problem": {
                "fail": "You keep closing one file to open another. Running the tests means leaving the editor.",
                "fix": "Cycle open files with `Shift-H` and `Shift-L`, open a terminal with `Ctrl-\\`, and split the screen when you need two files.",
            },
            "drills": [
                {
                    "h2": "Buffers (open files)",
                    "intro": "Cycle through the three source files.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Buffer keys", "rows": [
                            ("Shift-L", "Next open buffer"),
                            ("Shift-H", "Previous open buffer"),
                            ("<Space>,", "Fuzzy-find / switch open buffers"),
                            ("<Space>bd", "Close current buffer"),
                            ("<Space>bp", "Pin / unpin buffer"),
                            ("<Space>bP", "Close all non-pinned buffers"),
                        ], "try": "Open `calculator`, `orders` and `report` with `<Space>sf`. Press `Shift-H` twice, `Shift-L` once, then `<Space>,` and type `report`.",
                         "expect": "`<Space>,` lists `calculator.py`, `orders.py` and `report.py`, plus anything still open such as `data/log.txt`."},
                    ],
                },
                {
                    "h2": "Terminals inside Neovim",
                    "intro": "LazyVim uses a floating Snacks terminal. All three keys below toggle the same one.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Toggle the floating terminal", "rows": [
                            ("Ctrl-\\", "Toggle floating terminal (also Ctrl-/ or <Space>ft)"),
                            ("Ctrl-\\ Ctrl-n", "Exit terminal mode (back to normal navigation)"),
                            ("q", "Hide terminal (from normal mode inside it)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Split terminals added to the lesson config", "rows": [
                            ("<Space>tf", "Floating terminal"),
                            ("<Space>tv", "Vertical terminal (right side)"),
                            ("<Space>th", "Horizontal terminal (bottom)"),
                        ]},
                        {"type": "text", "body": "The lesson mapped these under capital `<Space>T`, because `<Space>t` is the test prefix in LazyVim. That mapping is not in the current config. Use `<Space>ft` or `Ctrl-\\`, or the built-in splits below. For several independent terminals, prefer tmux panes (`Ctrl-a |`, `Ctrl-a -`)."},
                        {"type": "keys", "where": "nvim", "title": "Built-in split terminals", "rows": [
                            (":split | terminal", "Open terminal in horizontal split (top/bottom)"),
                            (":vsplit | terminal", "Open terminal in vertical split (side by side)"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Run the test suite and just look at it", "code": "pytest",
                         "expect": "The summary ends with `2 failed, 7 passed`. The failures are `tests/test_calculator.py::test_history_tracks_results` and `tests/test_orders.py::test_free_shipping_threshold`."},
                        {"type": "text", "body": "Open the terminal first (`Ctrl-\\`). If `pytest` is not the one on your PATH, run `python3 -m pytest`. Then `Ctrl-\\ Ctrl-n` to leave terminal mode and press the toggle again to close it. The pass count can drift if you left a file dirty: run `:e!` on it and re-run."},
                    ],
                },
                {
                    "h2": "Copy and paste inside Neovim",
                    "intro": "`Cmd+C` and `Cmd+V` do not work inside Neovim. Your clipboard is synced (`unnamedplus`), so anything you `y` is ready for `Cmd+V` outside.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Copy from a code buffer", "rows": [
                            ("yy", "Copy current line → system clipboard"),
                            ("5yy", "Copy 5 lines"),
                            ("v → select → y", "Visual select then yank → system clipboard"),
                            ("Vi{y", "Copy everything inside braces"),
                        ]},
                        {"type": "keys", "where": "tmux", "title": "Copy from the terminal output", "rows": [
                            ("Ctrl-\\ Ctrl-n", "Exit terminal mode"),
                            ("Ctrl-a [", "Enter tmux copy mode (navigate freely)"),
                            ("v", "Start selection"),
                            ("y", "Yank → system clipboard (via pbcopy)"),
                        ]},
                        {"type": "keys", "where": "tmux", "title": "Paste into the terminal", "rows": [
                            ("Ctrl-a ]", "tmux paste (bypasses nvim, always works)"),
                        ], "try": "Or press `i` (terminal insert mode), then `Ctrl-a ]`.", "expect": "The text lands at the terminal prompt."},
                        {"type": "keys", "where": "tmux", "title": "Select with the mouse", "rows": [
                            ("Ctrl-a z", "Zoom pane to fullscreen first (Option + mouse-drag selects only this pane)"),
                            ("Cmd+C", "Copy"),
                            ("Ctrl-a z", "Unzoom back to normal layout"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Navigate between terminals and code", "rows": [
                            ("Ctrl-\\ Ctrl-n", "Exit terminal mode first (REQUIRED before navigating)"),
                            ("Ctrl-h/j/k/l", "Move between splits (works across nvim + tmux panes)"),
                            ("Ctrl-w q", "Close current split"),
                        ]},
                    ],
                },
                {
                    "h2": "Splits (multiple files visible)",
                    "intro": "From the picker, press `Ctrl-v` (vsplit) or `Ctrl-s` (hsplit) instead of `Enter` to open a file in a split.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Split keys", "rows": [
                            (":vsplit file.py", "Vertical split (side by side)"),
                            (":split file.py", "Horizontal split (top/bottom)"),
                            ("Ctrl-w h/j/k/l", "Navigate between splits"),
                            ("Ctrl-w =", "Make all splits equal size"),
                            ("Ctrl-w _", "Maximize current split height"),
                            ("Ctrl-w |", "Maximize current split width"),
                            ("Ctrl-w q", "Close current split"),
                        ], "try": "In `src/orders.py` run `/def calc`. Press `<Space>sf`, type `report`, press `Ctrl-v`. In the new pane run `/def print_report`. Flip with `Ctrl-w h` and `Ctrl-w l`, then close with `Ctrl-w q`.",
                         "expect": "Two panes open at once, each showing a different file. `Ctrl-w h` and `Ctrl-w l` move focus between them without closing either."},
                        {"type": "text", "body": "A \"Pick window\" prompt means the cursor is in the explorer sidebar. Press `Esc`, then `Ctrl-l` to reach the code area, or close the explorer with `\\` before splitting."},
                    ],
                },
                {
                    "h2": "Tabs (separate workspaces)",
                    "intro": "A tab is a layout. Each tab has its own arrangement of splits. For switching files, use buffers.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Tab keys", "rows": [
                            (":tabnew", "New empty tab"),
                            (":tabnew file.py", "Open file in new tab"),
                            ("gt", "Next tab"),
                            ("gT", "Previous tab"),
                            (":tabclose", "Close current tab"),
                            (":tabs", "List all tabs"),
                        ], "try": "With `src/calculator.py` open, run `:tabnew tests/test_calculator.py`. Flip with `gt` and `gT`, then `:tabclose`.",
                         "expect": "The test file opens in a brand-new tab: source and tests kept in separate layouts."},
                    ],
                },
                {
                    "h2": "The leader key",
                    "intro": "`<Space>` is your leader key. Press it and wait: the which-key popup shows every command group.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Leader groups", "rows": [
                            ("<Space>f...", "Find: files, recent, buffers, config"),
                            ("<Space>s...", "Search: grep, keymaps, help, diagnostics, marks"),
                            ("<Space>g...", "Git: status, lazygit, blame, diff"),
                            ("<Space>c...", "Code: actions, rename, format, symbols"),
                            ("<Space>x...", "Diagnostics / Trouble"),
                            ("<Space>b...", "Buffer commands"),
                            ("<Space>t...", "Test (neotest)"),
                            ("<Space>T...", "Terminals (float / vertical / horizontal)"),
                            ("<Space>u...", "UI toggles; <Space>uC switches colorscheme"),
                            ("<Space>1-9", "Jump to Harpoon file 1-9 (<Space>H adds current file)"),
                        ], "try": "Press `<Space>`, wait for the popup, press `s`, then press `g` and grep for `qualifies_for_free_shipping`.",
                         "expect": "The grep finds 4 matches: the definition in `src/orders.py`, and an import, a comment and the test call in `tests/test_orders.py`."},
                        {"type": "text", "body": "Forgot a key? Press `<Space>` and read the menu, or `<Space>sk` to fuzzy-search every keymap by description."},
                        {"type": "cmd", "where": "shell", "title": "Open Neovim in a folder", "code": "vp ~/tw",
                         "expect": "Your shell moves to `~/tw` and Neovim opens the folder in its file explorer. After you quit, you are still in `~/tw`."},
                        {"type": "cmd", "where": "shell", "title": "Open the current folder or one file", "code": C('''
cd ~/tw
v.
v orders.py
'''),
                         "expect": "`v.` opens the current folder in Neovim and `v orders.py` opens that file. `v` is a shortcut for `nvim`, and `vim` and `vi` run it too."},
                    ],
                },
            ],
            "rules": {
                "h2": "Terminals, splits and keys at a glance",
                "cards": [
                    ("Terminal card", "Terminals inside Neovim.", ["Keys", "Action"], [
                        ["`Ctrl-\\`", "Toggle terminal (root dir)"],
                        ["`<Space>ft`", "Terminal (toggle, root)"],
                        ["`<Space>Tf`", "Terminal float"],
                        ["`<Space>Th`", "Terminal horizontal (bottom)"],
                        ["`<Space>Tv`", "Terminal vertical (right)"],
                        ["`Ctrl-\\ Ctrl-n`", "Exit terminal mode → normal"],
                    ]),
                    ("Split from the picker", "Open a found file beside the current one.", ["Keys", "Result"], [
                        ["`Ctrl-v`", "Open the picked file in a vertical split"],
                        ["`Ctrl-s`", "Open the picked file in a horizontal split"],
                        ["`Esc` then `Ctrl-l`", "Leave the explorer for the code area when \"Pick window\" appears"],
                    ]),
                    ("Forgot a key?", "Let Neovim tell you.", ["Keys", "Result"], [
                        ["`<Space>`", "Wait for the which-key menu"],
                        ["`<Space>sk`", "Fuzzy-search every keymap"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Edit, then test without leaving Neovim",
                "frame": "You change code and want the result in the same window.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 17, on `2.50`", "`17G` `f2`"), "`cW` then `3.00` then `Esc` then `:w`", "Changes the price and saves."),
                    (None, "`<Space>th` then `python3 orders.py`", "A terminal opens and prints the new total."),
                    (None, "`Ctrl-\\ Ctrl-n`", "Leaves terminal mode so you can scroll the output."),
                    (None, "`<Space>th`", "Hides the terminal. Press it again to bring it back."),
                ],
                "before": "price = 2.50",
                "after": "price = 3.00",
                "meaning": "The terminal toggles like a drawer; long-running jobs belong in tmux panes.",
            },
            "practice": {
                "h2": "Practice: buffers, terminals and splits",
                "qs": [
                    ("Mechanism", "What is a buffer, and how is it different from a tab?",
                     "A file versus a layout.",
                     ["A buffer is an open file.", "A tab is an arrangement of splits."],
                     "A buffer holds a file. A tab holds a layout."),
                    ("Keystrokes", "Which keys open the picked file in a vertical split?",
                     "Not Enter.",
                     ["Press `<Space>sf` and find the file.", "Press `Ctrl-v` instead of `Enter`."],
                     "`Ctrl-v`."),
                    ("Application", "Run `pytest` and then get back to editing.",
                     "Toggle the terminal and leave terminal mode.",
                     ["Open the terminal and run `pytest`.", "Press `Ctrl-\\ Ctrl-n`.", "Toggle the terminal closed."],
                     "`Ctrl-\\`, `pytest`, `Ctrl-\\ Ctrl-n`, then toggle closed."),
                    ("Common mistake", "Pressing `Ctrl-h` in a terminal does not move to the split. Why?",
                     "Which mode are you in?",
                     ["Terminal mode sends the key to the shell.", "Press `Ctrl-\\ Ctrl-n` first."],
                     "Leave terminal mode before navigating."),
                ],
            },
        },
    ],
}
