"""Module 2: Neovim essentials. Sources: lesson 02 Neovim Essentials.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


PRACTICE_DIR = "Terminal-Workflow/practice/nvim-drills"

QUICK_START = C(r'''
nvim .                              # open project

\                File explorer (Snacks, toggle)
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
    "title": "Edit files in the terminal with Neovim",
    "footer": "Open a file, jump around, search, edit, undo; use buffers, terminals, splits, tabs and the leader key",
    "tagline": "Open, move, search, edit and undo in Neovim without touching the mouse.",
    "glossary": [],
    "coverage_allow": [
        ("<Space>T...", "lesson maps terminals under capital <Space>T; the live config has lowercase <Space>tf/tv/th, which the leader-group card now lists"),
        ('cd "Terminal Workflow/practice/nvim-drills"', "folder renamed to Terminal-Workflow"),
        ("demo-project/", "file tree shown as the expected result of the demo-project commit"),
        ('vp() { cd "$1" && nvim . ; }', "definition replaced by usage; installed in user's config"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Open, edit, save and quit Neovim",
            "subtitle": "Open a project in Neovim, find a file by name, search text in every file, save and quit, get out when you are stuck",
            "idea": (
                "Open a project, find a file, type and save: four moves cover a first edit.",
                [
                    ("Open a project in Neovim", "v .", "Open Neovim with the file explorer."),
                    ("Find a file by name", "<Space>sf", "Fuzzy search by name. Your Cmd+P."),
                    ("Search text in every file", "<Space>sg", "Search (grep) inside every file."),
                    ("Save and quit", ":wq", "Write the file and leave."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does typing do nothing when I open Neovim? I cannot find a file, and I cannot get out.",
                "fix": "Press `i` to type and `Esc` to stop. Save with `:w`, leave with `:q`. The exit table below gets you out of anything.",
            },
            "drills": [
                {
                    "h2": "Set up the practice project",
                    "intro": "Every exercise runs against a small Python project with deliberate flaws. This lesson only moves around in it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Go to the practice project", "code": C(f'''
cd {PRACTICE_DIR}
ls
'''),
                         "expect": "`ls` lists `data`, `scripts`, `src` and `tests`."},
                        {"type": "text", "body": "Undo a throwaway edit with `u`. The project has bad names, an unused import, an off-by-one bug and a failing test. You fix none of that here."},
                        {"type": "text", "body": "Why can `:e!` not bring back the original file? Autosave writes a file about 3 seconds after you stop typing, and when you leave the buffer. Once that has happened, `:e!` cannot bring back the original. To make `:e!` work, run `:ASToggle` before a throwaway drill and again after it. With autosave paused, a changed file stays unsaved until you run `:w`."},
                        {"type": "keys", "where": "nvim", "title": "Pause autosave so Neovim stops saving for you", "rows": [
                            (":ASToggle", "Pause autosave. Run it again to turn autosave back on"),
                        ]},
                        {"type": "text", "body": "Get a changed practice file back: for `~/tw`, run the Get the practice files box at the top of this page again. For `nvim-drills`, run `git checkout -- <file>` in that folder."},
                        {"type": "cmd", "where": "shell", "title": "Set up a smaller practice project (demo-project)", "code": C('''
cd demo-project
git init && git add -A && git commit -m "Initial commit"
'''),
                         "expect": "Git creates a repository with one commit, \"Initial commit\". The files are `src/calculator.py`, `src/app.py` and `tests/test_calculator.py`."},
                    ],
                },
                {
                    "h2": "Open a project folder in Neovim",
                    "intro": "Run this from inside `nvim-drills`. `v` with no argument opens the dashboard. `v .` opens the file explorer.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Open a folder in Neovim", "code": "v .          # or: nvim .",
                         "expect": "The file explorer opens. Press `Enter` on `src/calculator.py` to open it."},
                        {"type": "cmd", "where": "shell", "title": "See all the launcher shortcuts", "code": "v --help",
                         "expect": "The launcher prints its shortcut sheet and returns to the prompt. Neovim does not open."},
                        {"type": "text", "body": "Other ways to open Neovim: `v.` is the same as `v .`, and `vi` and `vim` run `v` too."},
                    ],
                },
                {
                    "h2": "Find a file and jump around the project without the mouse",
                    "intro": "Learn `<Space>sf` and `<Space>sg` first. You will use them a hundred times a day.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Find a file, search text and jump to a definition", "rows": [
                            ("\\", "Open or close the file explorer sidebar: Snacks Explorer on `:pwd`"),
                            ("<Space>e", "Open or close the file explorer: Snacks Explorer on the project root (LazyVim default)"),
                            ("<Space>sf", "Find a file by name: fuzzy search in `:pwd` (your Cmd+P)"),
                            ("<Space><Space>", "Find a file by name: same as `<Space>sf`, in `:pwd`"),
                            ("<Space>sg", "Search text in all files: grep in `:pwd`"),
                            ("<Space>/", "Search text in all files: same as `<Space>sg`, in `:pwd`"),
                            ("<Space>fr", "Open a recent file"),
                            ("<Space>fg", "Find a git-tracked file in `:pwd`"),
                            ("<Space>,", "Switch to another open buffer: files below `:pwd`"),
                            ("gd", "Go to definition: jump to where the symbol under the cursor is defined"),
                            ("gr", "Find all references"),
                            ("gO", "Show the outline of functions and classes in this file"),
                            ("Ctrl-o", "Jump back after going to a definition"),
                        ], "try": "Press `<Space>sf`, type `orders`, press `Enter`.",
                         "expect": "`src/orders.py` opens."},
                        {"type": "text", "body": "See every search key: the `<Space>s` search group has `sf` files, `sg` grep, `sw` word, `sk` keymaps, `sh` help, `sd` diagnostics, `sr` search and replace. Press `<Space>s` and wait to see them all."},
                        {"type": "keys", "where": "nvim", "title": "Find every place TAX_RATE is used", "rows": [
                            ("<Space>sf", "Type orders, Enter: opens src/orders.py"),
                            ("<Space>sg", "Search for TAX_RATE: type it, Enter. Greps `:pwd`"),
                            ("Ctrl-n / Ctrl-p", "Move between the 5 matches (2 in orders.py, 3 in report.py)"),
                            ("Enter", "Jump to the match"),
                        ], "try": "Run the three steps in order.",
                         "expect": "Matches in `src/orders.py` (the definition and its use inside `calc`) and `src/report.py` (the import line plus two f-string uses)."},
                        {"type": "keys", "where": "nvim", "title": "Jump to where a function is defined and back", "rows": [
                            ("gd", "Jump to the `calc` definition"),
                            ("Ctrl-o", "Jump back to where you were"),
                            ("gr", "List every place `calc` is referenced"),
                        ], "try": "In `src/orders.py`, put the cursor on `calc` inside the `all_totals` list comprehension. Press `gd`, `Ctrl-o`, then `gr`.",
                         "expect": "`gr` shows references in 3 files: `orders.py`, `report.py` and `tests/test_orders.py`. Imports count as references."},
                    ],
                },
                {
                    "h2": "Type text, save the file and quit",
                    "intro": "The rhythm: `i` to type, `Esc` to stop, `:w` to save.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Start typing, stop typing, save and quit", "rows": [
                            ("i", "Enter insert mode (now you can type)"),
                            ("Esc", "Go back to normal mode"),
                            ("jk", "Leave insert mode: type `j` then `k` quickly. Same as `Esc`"),
                            ("Option+h / j / k / l", "Move the cursor left, down, up or right without leaving insert mode"),
                            (":w", "Save the file"),
                            (":q", "Quit Neovim"),
                            (":wq", "Save and quit"),
                            ("ZZ", "Save and quit (faster, no colon needed)"),
                        ], "try": "Open `src/calculator.py`, go to the blank line 2, press `i`, type `# scratch`, press `Esc`, then `:w`. Press `u`, then `:w` again.",
                         "expect": "The save, undo, save loop works and the file is left unmodified."},
                    ],
                },
            ],
            "rules": {
                "h2": "Get out of Neovim and start fast",
                "cards": [
                    ("How do I get out of a mode, popup or window in Neovim?", "Stuck somewhere? Find the row and press the exit.", ["Stuck in...", "Exit with"], [
                        ["Insert mode", "`Esc` or `jk`"],
                        ["Visual mode", "`Esc`"],
                        ["Terminal mode (nvim)", "`Ctrl-\\ Ctrl-n` (then `q`, or `Ctrl-\\` to hide it)"],
                        ["Picker / fuzzy finder (snacks)", "`Esc` or `Ctrl-c`"],
                        ["LazyGit", "`q`"],
                        ["Snacks explorer (`<Space>e` or `\\`)", "The same key again, or `q`"],
                        ["grug-far (search/replace)", "`q` or `:q`"],
                        ["tmux copy mode", "`q` or `Esc`"],
                        ["tmux window picker (`Ctrl-a w`)", "`Esc` or `q`"],
                        ["A command-line prompt (`:`)", "`Esc`"],
                        ["Neovim entirely", "`:q` (or `:q!` to force without saving)"],
                        ["Stuck and nothing works", "`:qa!` (force quit everything)"],
                    ]),
                    ("Neovim quick start: the keys for your first five minutes", "Open a project, find a file, edit, save, undo.", None, QUICK_START),
                ],
            },
            "worked": {
                "h2": "Try an edit, undo it and leave the file clean",
                "frame": "Make a throwaway edit, then leave the file clean.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 1", "`gg`"), "`O` then `# scratch` then `Esc`", "Open a line above and type the comment."),
                    (None, "`:w`", "Save the file."),
                    (None, "`u` then `:w`", "Undo the edit and save the original again."),
                ],
                "before": "TAX_RATE = 0.08",
                "after": "# scratch\nTAX_RATE = 0.08",
                "meaning": "Try an edit safely: save, undo, save works for any throwaway edit.",
            },
            "practice": {
                "h2": "Check how to open, save and quit Neovim",
                "qs": [
                    ("Mechanism", "Why does typing do nothing when I open Neovim?",
                     "Which mode do you start in?",
                     ["Neovim starts in normal mode, where keys are commands.", "Press `i` to enter insert mode."],
                     "Normal mode treats keys as commands. `i` switches to typing."),
                    ("Keystrokes", "How do I save and quit without typing a colon?",
                     "Two capital letters.",
                     ["Make sure you are in normal mode.", "Press `ZZ`."],
                     "`ZZ`. The same as `:wq`."),
                    ("Application", "How do I find every use of `TAX_RATE` in the project?",
                     "Search inside files, not file names.",
                     ["Press `<Space>sg`.", "Type `TAX_RATE` and press `Enter`.", "Move through the matches with `Ctrl-n` and `Ctrl-p`."],
                     "`<Space>sg`, then `TAX_RATE`. Five matches in two files."),
                    ("Common mistake", "I am in a terminal inside Neovim and nothing navigates. What do I press first?",
                     "Terminal mode has its own exit.",
                     ["Press `Ctrl-\\ Ctrl-n` to leave terminal mode.", "Now navigation keys work again."],
                     "`Ctrl-\\ Ctrl-n`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Move around a file fast and search in it",
            "subtitle": "Jump to a word, a line or a line number, jump to the matching bracket, search for text in a file, step through the matches",
            "idea": (
                "Jump around a file with short keys instead of holding the arrow keys.",
                [
                    ("Jump by word", "w / b / e", "Go forward, go back, go to the end of the word."),
                    ("Jump to the start or end of a line", "0 / $ / ^", "Start, end, first non-blank."),
                    ("Jump to the top, bottom or a line number", "gg / G", "Top or bottom. 42G goes to line 42."),
                    ("Search for text in the file", "/pattern", "Then n and N step through the matches."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I get to line 50 without holding `j`? You hold it, overshoot, and scroll back. Finding one word means reading the whole screen.",
                "fix": "Jump with `51G`, `%` and `gg`. Search with `/pattern` and step with `n`.",
            },
            "drills": [
                {
                    "h2": "Jump to a word, a line, a bracket or a line number",
                    "intro": "Line numbers can drift if you edited the file earlier. `/RAW_ORDERS` then `Enter` always works too.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Move the cursor by word, line, page or bracket", "rows": [
                            ("h/j/k/l", "Move left, down, up or right (instead of arrow keys)"),
                            ("w", "Jump forward one word"),
                            ("b", "Jump back one word"),
                            ("e", "Jump to the end of the word"),
                            ("0", "Jump to the start of the line"),
                            ("$", "Jump to the end of the line"),
                            ("^", "Jump to the first non-whitespace character on the line"),
                            ("gg", "Jump to the top of the file"),
                            ("G", "Jump to the bottom of the file"),
                            ("42G", "Jump to line 42 (any number works)"),
                            ("Ctrl-d", "Scroll half a page down"),
                            ("Ctrl-u", "Scroll half a page up"),
                            ("Ctrl-f", "Scroll a full page down"),
                            ("Ctrl-b", "Scroll a full page up"),
                            ("%", "Jump to the matching bracket, paren or brace"),
                            ("{", "Jump up to the previous empty line (paragraph up)"),
                            ("}", "Jump down to the next empty line (paragraph down)"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Jump to RAW_ORDERS, its closing bracket and back to the top without scrolling", "code": C('''
51G
%
gg
'''),
                         "expect": "`51G` lands on `RAW_ORDERS = [`. `%` on that `[` lands on the closing `]`, 7 lines down. `gg` is back at the top."},
                    ],
                },
                {
                    "h2": "Search for text in a file and jump between matches",
                    "intro": "`src/orders.py` has a TODO above `calc` and a FIXME above `qualifies_for_free_shipping`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Search forward and backward, or jump to a character on the line", "rows": [
                            ("/pattern", "Search forward"),
                            ("?pattern", "Search backward"),
                            ("n", "Jump to the next match"),
                            ("N", "Jump to the previous match"),
                            ("*", "Search forward for the word under the cursor"),
                            ("#", "Search backward for the word under the cursor"),
                            ("f{char}", "Jump to the next {char} on this line"),
                            ("F{char}", "Jump to the previous {char} on this line"),
                            (";", "Repeat the last f/F jump"),
                        ], "try": "Open `src/calculator.py`, run `/divide`, then press `n` and `N`.",
                         "expect": "You land on the `divide` method and on the `raise Exception(\"Cannot divide by zero\")` line inside it."},
                        {"type": "cmd", "where": "nvim", "title": "Find every TODO and FIXME in a file without grepping", "code": C('''
gg
/TODO
/FIXME
'''),
                         "expect": "`/TODO` and `/FIXME` each find exactly one match in `src/orders.py`."},
                        {"type": "text", "body": "Jump to the next use of a word: put the cursor on `calc` after the TODO comment and press `*`. Use `#` to search backward and compare."},
                    ],
                },
                {
                    "h2": "Start typing before, after or on a new line (insert mode)",
                    "intro": "Instead of `$a`, press `A`. Each variant saves a step.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Start typing before the cursor, after it, or on a new line", "rows": [
                            ("i", "Start typing before the cursor"),
                            ("a", "Start typing after the cursor"),
                            ("I", "Start typing at the start of the line"),
                            ("A", "Start typing at the end of the line"),
                            ("o", "Open a new line below and start typing"),
                            ("O", "Open a new line above and start typing"),
                            ("s", "Delete the character under the cursor and start typing"),
                            ("S", "Delete the whole line and start typing"),
                            ("C", "Delete to the end of the line and start typing"),
                        ], "try": "In `src/calculator.py` run `/clear_history`, go to the `self.history = []` line and press `o`. Type `pass  # scratch line, will discard`, press `Esc`, then press `u`.",
                         "expect": "`o` opens an indented line below. After `u`, `/scratch` reports pattern not found: the file is clean."},
                    ],
                },
            ],
            "rules": {
                "h2": "Jump and search keys on one card",
                "cards": [
                    ("Keys to move around a file", "The keys that carry most of your day.", ["Keys", "Action"], [
                        ["`h/j/k/l`", "Move the cursor"],
                        ["`w/b/e`", "Jump a word forward/back/to the end"],
                        ["`0/$`", "Jump to the start/end of the line"],
                        ["`gg/G`", "Jump to the top/bottom of the file"],
                        ["`Ctrl-d/Ctrl-u`", "Scroll half a page down/up"],
                        ["`%`", "Jump to the matching bracket"],
                        ["`/pattern`", "Search the file (n=next, N=prev)"],
                        ["`*/#`", "Search for the word under the cursor"],
                        ["`f{c}/F{c}`", "Jump to a character on the line"],
                    ]),
                    ("Jump to a line when the line number changed", "Edits move lines. Search for the name instead.", ["Step", "Keys"], [
                        ["Jump to a line", "`51G`"],
                        ["Jump by name (always works)", "`/RAW_ORDERS` then `Enter`"],
                        ["Go back to the top", "`gg`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Jump to a list and its closing bracket",
                "frame": "Get to `ORDERS` and its closing bracket without scrolling.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (None, "`2G`", "Jump to line 2, the list."),
                    (("line 2, on `[`", "`f[`"), "`%`", "Jump to the matching `]`."),
                    (None, "`gg`", "Return to the top."),
                ],
                "after": 'ORDERS = ["A1", "A2", "A3"]\n' + " " * 26 + "^ cursor after `%`",
                "meaning": "Jump to the matching bracket: `%` works on any bracket pair.",
            },
            "practice": {
                "h2": "Check how to move around and search a file",
                "qs": [
                    ("Mechanism", "Why does `%` jump from `[` to `]`?",
                     "It matches pairs.",
                     ["`%` finds the partner of the bracket under the cursor.", "It works for (), [] and {}."],
                     "`%` jumps to the matching bracket."),
                    ("Keystrokes", "How do I jump to line 42?",
                     "A number, then a capital letter.",
                     ["Type `42`.", "Press `G`."],
                     "`42G`."),
                    ("Application", "How do I find the TODO and then the FIXME in `src/orders.py`?",
                     "Search twice.",
                     ["Press `gg`.", "Run `/TODO`.", "Run `/FIXME`."],
                     "`/TODO` then `/FIXME`. One match each."),
                    ("Common mistake", "Why does `51G` land on the wrong line after I edited the file? What do I do?",
                     "Search, not count.",
                     ["Line numbers drift after edits.", "Run `/RAW_ORDERS` and press `Enter`."],
                     "Search for the name. It always works."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Delete, copy, paste, comment and undo in Neovim",
            "subtitle": "Delete a line, copy and paste a line, comment out lines, undo a mistake, repeat the last change",
            "idea": (
                "Delete and copy a line in one or two keys. Undo and repeat make mistakes cheap.",
                [
                    ("Delete a line", "dd", "Cut the whole line."),
                    ("Copy a line", "yy", "Yank (copy) it. Paste with p."),
                    ("Comment out a line", "gcc", "Toggle a comment on the line."),
                    ("Undo, redo or repeat a change", "u", "Ctrl-r redoes. . repeats."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I get a deleted line back? You delete the wrong line and have no idea how to undo it. You retype the same edit on ten lines.",
                "fix": "Undo with `u`, redo with `Ctrl-r`, and repeat the last change with `.`.",
            },
            "drills": [
                {
                    "h2": "Delete, copy (yank) and paste lines",
                    "intro": "`RAW_ORDERS` in `src/orders.py` has six entries, `A1` to `A6`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Delete, copy and paste a line or character", "rows": [
                            ("dd", "Delete (cut) the whole line"),
                            ("5dd", "Delete 5 lines"),
                            ("D", "Delete to the end of the line"),
                            ("yy", "Copy (yank) the whole line"),
                            ("5yy", "Copy 5 lines"),
                            ("y$", "Copy to the end of the line"),
                            ("p", "Paste below or after the cursor"),
                            ("P", "Paste above or before the cursor"),
                            ("x", "Delete the character under the cursor"),
                            ("X", "Delete the character before the cursor (Backspace)"),
                            ("J", "Join this line with the next (remove the newline)"),
                            ("yyp", "Duplicate this line (yank and paste)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Comment out or uncomment lines", "rows": [
                            ("gcc", "Toggle a comment on this line"),
                            ("gc{motion}", "Comment a range (e.g., gcip comments a paragraph)"),
                            ("gc5j", "Comment 5 lines down"),
                            ("V then gc", "Select lines, then toggle the comment"),
                            ("gcO", "Add a comment on the line above"),
                            ("gco", "Add a comment on the line below"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Duplicate an order line, comment it out, then delete it", "code": C('''
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
                    "h2": "Undo a change, redo it or repeat it",
                    "intro": "The `.` command repeats your last change. Make a change, move to another word, press `.`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Undo, redo and repeat a change", "rows": [
                            ("u", "Undo the last change"),
                            ("Ctrl-r", "Redo the change you undid"),
                            (".", "Repeat the last change"),
                        ], "try": "In `data/log.txt`, put the cursor on `pending` in line 1, press `ciw`, type `done`, press `Esc`. On line 2 press `.`. Then `u` twice, `Ctrl-r` twice, then `u` twice again.",
                         "expect": "Line 1 reads `item 1: done`, and line 2 reads `item 2: done` after `.`. After the last two `u`, `/done` finds nothing: every line says `pending` again."},
                    ],
                },
            ],
            "rules": {
                "h2": "Edit, delete, copy and undo keys on one card",
                "cards": [
                    ("Keys to edit text in Neovim", "The edits you repeat all day.", ["Keys", "Action"], [
                        ["`i/a/o/O`", "Enter insert mode"],
                        ["`A/I`", "Start typing at the end/start of the line"],
                        ["`dd/D`", "Delete the line / to the end of the line"],
                        ["`cc/C`", "Change the line / to the end of the line"],
                        ["`yy/p`", "Copy the line / paste"],
                        ["`ci\"/ci(/ci{`", "Change inside quotes/parens/braces"],
                        ["`di\"/da(`", "Delete inside/around"],
                        ["`vi{/vip`", "Select inside braces/paragraph"],
                        ["`u / Ctrl-r`", "Undo / redo"],
                        ["`.`", "Repeat the last change"],
                        ["`>>  / <<`", "Indent / unindent"],
                        ["`gg=G`", "Auto-indent the entire file"],
                        ["`<Space>cf`", "Format the file"],
                        ["`:%s/old/new/g`", "Find and replace text in the file"],
                    ]),
                    ("Take back an edit: undo, redo or reload the file", "Three ways back, from smallest to biggest.", ["Situation", "Keys"], [
                        ["Undo the last change", "`u`"],
                        ["Redo it", "`Ctrl-r`"],
                        ["Reload from disk (autosave paused with `:ASToggle` first)", "`:e!`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Change a word on two lines, then undo both",
                "frame": "Change one word on two lines, then take both changes back.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 1, on `pending`", "`1G` `fp`"), "`ciw` then `done` then `Esc`", "Replace the word."),
                    (("line 2, on `pending`", "`j` `0` `fp`"), "`.`", "Repeat the same edit."),
                    (None, "`u` `u`", "Both lines say `pending` again."),
                    (None, "`Ctrl-r` `Ctrl-r`", "Both say `done` again."),
                    (None, "`u` `u`", "Both lines say `pending` again. Autosave writes the original back."),
                ],
                "before": "item 1: pending\nitem 2: pending",
                "after": "item 1: done\nitem 2: done",
                "meaning": "Repeat one edit with a key, then undo all of it.",
            },
            "practice": {
                "h2": "Check how to edit, copy and undo",
                "qs": [
                    ("Mechanism", "Why does `yyp` duplicate a line?",
                     "Two commands in a row.",
                     ["`yy` yanks the line.", "`p` pastes it below."],
                     "Yank the line, then paste it below."),
                    ("Keystrokes", "How do I comment out or uncomment the current line?",
                     "g, c, then c again.",
                     ["Press `gcc`.", "Press `gcc` again to uncomment."],
                     "`gcc`."),
                    ("Application", "How do I change `pending` to `done` on two lines without retyping?",
                     "Change once, then repeat.",
                     ["On the first line, run `ciw`, type `done`, press `Esc`.", "Move to the second line and press `.`."],
                     "`ciw` once, then `.`."),
                    ("Common mistake", "How do I get a lesson file back to clean after I edited it?",
                     "Undo, step by step.",
                     ["`u` undoes one change at a time, so press it until the text is back.", "`:e!` discards edits that are not saved yet, and autosave has usually saved the edit already (pause it with `:ASToggle` first)."],
                     "`u` until it is clean."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Work on several files, terminals and splits in Neovim",
            "subtitle": "Switch between open files, open a terminal inside Neovim, show two files side by side, use tabs, find a key you forgot",
            "idea": (
                "Switch between open files (buffers), arrange them in splits and tabs, and press the leader key to find the rest.",
                [
                    ("Switch to the next open file", "Shift-L", "Shift-H goes back."),
                    ("Open a terminal inside Neovim", "Ctrl-\\", "Open the last terminal you used. Press again to hide it."),
                    ("Show two files side by side", ":vsplit file.py", "Open the second file in a vertical split."),
                    ("Find a key you forgot", "<Space>", "Wait for the which-key menu."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I switch files without closing one to open another? Running the tests also means leaving the editor.",
                "fix": "Cycle open files with `Shift-H` and `Shift-L`, open a terminal with `Ctrl-\\`, and split the screen when you need two files.",
            },
            "drills": [
                {
                    "h2": "Switch between open files (buffers)",
                    "intro": "Cycle through the three source files.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Switch, list and close open files", "rows": [
                            ("Shift-L", "Go to the next open buffer"),
                            ("Shift-H", "Go to the previous open buffer"),
                            ("<Space>,", "Switch to another open buffer: fuzzy-find, files below `:pwd`"),
                            ("<Space>fb", "Switch to another open buffer: same as `<Space>,`"),
                            ("<Space>fB", "List every buffer, hidden ones too: files below `:pwd`"),
                            ("<Space>bd", "Close this buffer"),
                            ("<Space>bp", "Pin or unpin this buffer"),
                            ("<Space>bP", "Close all non-pinned buffers"),
                        ], "try": "Open `calculator`, `orders` and `report` with `<Space>sf`. Press `Shift-H` twice, `Shift-L` once, then `<Space>,` and type `report`.",
                         "expect": "`<Space>,` lists `calculator.py`, `orders.py` and `report.py`, plus anything still open such as `data/log.txt`."},
                    ],
                },
                {
                    "h2": "Open a terminal inside Neovim and run commands",
                    "intro": "Terminals are Snacks terminals and open in `:pwd`. `Ctrl-\\` and `Ctrl-/` toggle the last terminal you used, whether float, right or bottom.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open or hide a terminal", "rows": [
                            ("Ctrl-\\", "Open or hide the last terminal you used (also `Ctrl-/`)"),
                            ("<Space>ft", "Open or hide the floating terminal"),
                            ("Ctrl-\\ Ctrl-n", "Leave terminal mode and go back to normal navigation"),
                            ("q", "Hide the terminal (from normal mode inside it)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Open a terminal in a floating window or a split", "rows": [
                            ("<Space>tf", "Open a floating terminal"),
                            ("<Space>tv", "Open a terminal on the right (vertical split)"),
                            ("<Space>th", "Open a terminal at the bottom (horizontal split)"),
                        ]},
                        {"type": "text", "body": "Keep several terminals open: these are lowercase `<Space>t` keys, next to the test keys. Each of the three keeps its own terminal. For several long-running terminals, prefer tmux panes (`Ctrl-a |`, `Ctrl-a -`). The built-in splits below also work."},
                        {"type": "keys", "where": "nvim", "title": "Open a terminal in a Neovim split (top and bottom, or side by side)", "rows": [
                            (":split | terminal", "Open a terminal in a horizontal split (top/bottom)"),
                            (":vsplit | terminal", "Open a terminal in a vertical split (side by side)"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Run the tests (pytest) and read the result", "code": "pytest",
                         "expect": "The summary ends with `2 failed, 7 passed`. The failures are `tests/test_calculator.py::test_history_tracks_results` and `tests/test_orders.py::test_free_shipping_threshold`."},
                        {"type": "text", "body": "Run pytest inside Neovim: open the terminal first (`Ctrl-\\`). If `pytest` is not the one on your PATH, run `python3 -m pytest`. Then `Ctrl-\\ Ctrl-n` to leave terminal mode and press the toggle again to close it. The pass count can drift if you left a file edited: press `u` until it is back to the original, give autosave 3 seconds, and re-run."},
                        {"type": "keys", "where": "nvim", "title": "Follow a log file inside Neovim (watch new lines in a split)", "rows": [
                            (":split | terminal tail -F ~/tw/app.log", "Watch the log in a bottom split; new lines appear as they are written"),
                            (":split | terminal tail -F ~/tw/app.log | grep -E \"OK|SUCCESS|FAIL\"", "Watch only the lines with OK, SUCCESS or FAIL"),
                            ("Ctrl-\\ Ctrl-n", "Leave terminal mode to scroll or copy; `i` goes back to live"),
                        ], "try": "In another tmux pane run `echo \"backup start\" >> ~/tw/app.log`. In Neovim run `:split | terminal tail -F ~/tw/app.log` and press `i`. In the tmux pane run `echo \"backup OK\" >> ~/tw/app.log`.",
                         "expect": "The bottom split shows `backup start`, then `backup OK` as soon as you write it. Run the second row instead and only lines with `OK`, `SUCCESS` or `FAIL` show. The whole line after `:split | terminal` goes to the shell, including its own `|`. Close the split with `Ctrl-\\ Ctrl-n`, then `Ctrl-w q`."},
                        {"type": "keys", "where": "nvim", "title": "Paste a command's output into the file (:r !cmd)", "rows": [
                            (":r !date", "Insert the output of date below the cursor"),
                            (":r !grep -E \"OK|SUCCESS|FAIL\" ~/tw/app.log | tail -n 5", "Insert the last 5 lines with OK, SUCCESS or FAIL"),
                        ], "try": "Run `:enew` for an empty buffer. Run `:r !date`, then `:r !grep -E \"OK|SUCCESS|FAIL\" ~/tw/app.log | tail -n 5`.",
                         "expect": "The date line appears, then the last 5 lines of `~/tw/app.log` that contain `OK`, `SUCCESS` or `FAIL`, such as `backup OK`. In `:r !` commands `%` and `#` stand for file names: type `\\%` for a literal percent sign."},
                    ],
                },
                {
                    "h2": "Copy and paste text in Neovim and its terminal",
                    "intro": "`Cmd+C` and `Cmd+V` do not work inside Neovim. Your clipboard is synced (`unnamedplus`), so anything you `y` is ready for `Cmd+V` outside.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Copy text from a file to the system clipboard", "rows": [
                            ("yy", "Copy the current line → system clipboard"),
                            ("5yy", "Copy 5 lines"),
                            ("v → select → y", "Select text in visual mode, then yank → system clipboard"),
                            ("Vi{y", "Copy everything inside braces"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Copy text with the mouse", "rows": [
                            ("Drag, then release", "Copy the dragged text to the system clipboard. Releasing ends the selection"),
                        ], "try": "Drag over a line of `~/tw/notes.md` in Neovim, release, then press `Cmd+V` in another app.",
                         "expect": "The highlight clears and the text is on the clipboard."},
                        {"type": "keys", "where": "tmux", "title": "Copy text from terminal output", "rows": [
                            ("Ctrl-\\ Ctrl-n", "Leave terminal mode"),
                            ("Ctrl-a [", "Enter tmux copy mode (navigate freely)"),
                            ("v", "Start selecting text"),
                            ("y", "Copy the selection → system clipboard (via pbcopy)"),
                        ]},
                        {"type": "keys", "where": "tmux", "title": "Paste text into the terminal", "rows": [
                            ("Ctrl-a ]", "Paste with tmux (bypasses nvim, always works)"),
                        ], "try": "Or press `i` (terminal insert mode), then `Ctrl-a ]`.", "expect": "The text lands at the terminal prompt."},
                        {"type": "keys", "where": "tmux", "title": "Select and copy terminal output with the mouse", "rows": [
                            ("Ctrl-a z", "Zoom the pane to fullscreen first (Option + mouse-drag selects only this pane)"),
                            ("Cmd+C", "Copy the selection"),
                            ("Ctrl-a z", "Unzoom back to the normal layout"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Move between a terminal and your code", "rows": [
                            ("Ctrl-\\ Ctrl-n", "Leave terminal mode first (required before navigating)"),
                            ("Ctrl-h/j/k/l", "Move to the split or tmux pane in that direction"),
                            ("Ctrl-w q", "Close this split"),
                        ]},
                    ],
                },
                {
                    "h2": "Show two files at once in a split",
                    "intro": "From the picker, press `Ctrl-v` (vsplit) or `Ctrl-s` (hsplit) instead of `Enter` to open a file in a split.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Split the window and move between splits", "rows": [
                            (":vsplit file.py", "Open a file in a vertical split (side by side)"),
                            (":split file.py", "Open a file in a horizontal split (top and bottom)"),
                            ("Ctrl-w h/j/k/l", "Move to the split on the left, below, above or right"),
                            ("Ctrl-w =", "Make all splits the same size"),
                            ("Ctrl-w _", "Make this split as tall as possible (maximize height)"),
                            ("Ctrl-w |", "Make this split as wide as possible (maximize width)"),
                            ("Ctrl-w q", "Close this split"),
                        ], "try": "In `src/orders.py` run `/def calc`. Press `<Space>sf`, type `report`, press `Ctrl-v`. In the new pane run `/def print_report`. Flip with `Ctrl-w h` and `Ctrl-w l`, then close with `Ctrl-w q`.",
                         "expect": "Two panes open at once, each showing a different file. `Ctrl-w h` and `Ctrl-w l` move focus between them without closing either."},
                        {"type": "text", "body": "Why does a \"Pick window\" prompt appear? The cursor is in the explorer sidebar. Press `Esc`, then `Ctrl-l` to reach the code area, or close the explorer with `\\` before splitting."},
                    ],
                },
                {
                    "h2": "Use tabs as separate workspaces",
                    "intro": "A tab is a layout. Each tab has its own arrangement of splits. For switching files, use buffers.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open, switch and close tabs", "rows": [
                            (":tabnew", "Open a new empty tab"),
                            (":tabnew file.py", "Open a file in a new tab"),
                            ("gt", "Go to the next tab"),
                            ("gT", "Go to the previous tab"),
                            (":tabclose", "Close this tab"),
                            (":tabs", "List all tabs"),
                        ], "try": "With `src/calculator.py` open, run `:tabnew tests/test_calculator.py`. Flip with `gt` and `gT`, then `:tabclose`.",
                         "expect": "The test file opens in a brand-new tab: source and tests kept in separate layouts."},
                    ],
                },
                {
                    "h2": "Find a key you forgot with the leader key",
                    "intro": "`<Space>` is your leader key. Press it and wait: the which-key popup shows every command group.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "See what each leader key group does", "rows": [
                            ("<Space>f...", "Find files, recent files, buffers and config files"),
                            ("<Space>s...", "Search text, keymaps, help, diagnostics and marks"),
                            ("<Space>g...", "Use git: status, LazyGit, blame, diff"),
                            ("<Space>c...", "Work on code: actions, rename, format, symbols"),
                            ("<Space>x...", "Show diagnostics in Trouble"),
                            ("<Space>b...", "Manage buffers"),
                            ("<Space>t...", "Run tests (neotest) and open terminals (`tf`, `tv`, `th`)"),
                            ("<Space>u...", "Switch UI toggles; `<Space>uC` changes the colorscheme"),
                            ("<Space>1-9", "Jump to Harpoon file 1-9 (<Space>H adds current file)"),
                        ], "try": "Press `<Space>`, wait for the popup, press `s`, then press `g` and grep for `qualifies_for_free_shipping`.",
                         "expect": "The grep finds 4 matches: the definition in `src/orders.py`, and an import, a comment and the test call in `tests/test_orders.py`."},
                        {"type": "text", "body": "Forgot a key? Press `<Space>` and read the menu, or `<Space>sk` to fuzzy-search every keymap by description."},
                        {"type": "cmd", "where": "shell", "title": "Open Neovim in a folder and stay in that folder after you quit", "code": "vp ~/tw",
                         "expect": "Your shell moves to `~/tw` and Neovim opens the folder in its file explorer. After you quit, you are still in `~/tw`."},
                        {"type": "cmd", "where": "shell", "title": "Open the current folder or one file in Neovim", "code": C('''
cd ~/tw
v.
v orders.py
vi notes.md
'''),
                         "expect": "`v.` opens the current folder in Neovim, and `v orders.py` and `vi notes.md` open those files. Quit each with `:q` to reach the next line. `v` is a shortcut for `nvim`, and `vim` and `vi` run it too."},
                    ],
                },
            ],
            "rules": {
                "h2": "Terminal, split and leader keys on one card",
                "cards": [
                    ("Open and leave a terminal inside Neovim", "Keys for terminals inside Neovim.", ["Keys", "Action"], [
                        ["`Ctrl-\\`", "Toggle the last terminal you used (in `:pwd`)"],
                        ["`<Space>ft`", "Toggle the floating terminal (in `:pwd`)"],
                        ["`<Space>tf`", "Open a floating terminal"],
                        ["`<Space>th`", "Open a terminal at the bottom"],
                        ["`<Space>tv`", "Open a terminal on the right"],
                        ["`Ctrl-\\ Ctrl-n`", "Leave terminal mode, back to normal"],
                    ]),
                    ("Open a found file in a split", "Open a found file beside the current one.", ["Keys", "Result"], [
                        ["`Ctrl-v`", "Open the picked file in a vertical split"],
                        ["`Ctrl-s`", "Open the picked file in a horizontal split"],
                        ["`Esc` then `Ctrl-l`", "Leave the explorer for the code area when \"Pick window\" appears"],
                    ]),
                    ("How do I find a key I forgot?", "Let Neovim tell you.", ["Keys", "Result"], [
                        ["`<Space>`", "Wait for the which-key menu"],
                        ["`<Space>sk`", "Fuzzy-search every keymap"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Edit a file and run it without leaving Neovim",
                "frame": "Change code and see the result in the same window.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 17, on `2.50`", "`17G` `f2`"), "`cW` then `3.00` then `Esc` then `:w`", "Change the price and save."),
                    (None, "`<Space>th` then `python3 orders.py`", "A terminal opens and prints the new total."),
                    (None, "`Ctrl-\\ Ctrl-n`", "Leave terminal mode so you can scroll the output."),
                    (None, "`<Space>th`", "Hide the terminal. Press it again to bring it back."),
                ],
                "before": "price = 2.50",
                "after": "price = 3.00",
                "meaning": "Open and hide a terminal like a drawer; run long jobs in tmux panes.",
            },
            "practice": {
                "h2": "Check how to use buffers, terminals and splits",
                "qs": [
                    ("Mechanism", "What is the difference between a buffer and a tab?",
                     "A file versus a layout.",
                     ["A buffer is an open file.", "A tab is an arrangement of splits."],
                     "A buffer holds a file. A tab holds a layout."),
                    ("Keystrokes", "How do I open the picked file in a vertical split?",
                     "Not Enter.",
                     ["Press `<Space>sf` and find the file.", "Press `Ctrl-v` instead of `Enter`."],
                     "`Ctrl-v`."),
                    ("Application", "How do I run `pytest` and then get back to editing?",
                     "Toggle the terminal and leave terminal mode.",
                     ["Open the terminal and run `pytest`.", "Press `Ctrl-\\ Ctrl-n`.", "Toggle the terminal closed."],
                     "`Ctrl-\\`, `pytest`, `Ctrl-\\ Ctrl-n`, then toggle closed."),
                    ("Common mistake", "Why does `Ctrl-h` not move to the split when I am in a terminal?",
                     "Which mode are you in?",
                     ["Terminal mode sends the key to the shell.", "Press `Ctrl-\\ Ctrl-n` first."],
                     "Leave terminal mode before navigating."),
                ],
            },
        },
    ],
}
