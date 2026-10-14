"""Module 8: Coming from VS Code. Source: the live Neovim config (LazyVim) and plain Vim; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


MODULE = {
    "n": 8,
    "folder": "m8-from-vscode",
    "title": "Coming from VS Code",
    "footer": "VS Code shortcuts and Neovim keys side by side: find, edit, code, view toggles, sort, diff and clipboard",
    "tagline": "Every VS Code shortcut you know, and the Neovim key that does the same job.",
    "glossary": [
        ("tw-zen", "Zen mode", ["zen mode", "zen"], "A distraction-free view: the file sits centred in the window and the bars are hidden. Toggle it with Space u z."),
        ("tw-diff", "Diff mode", ["diff mode"], "Two windows scroll together and the lines that differ are coloured. Start it with :diffthis in each window."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Your VS Code shortcuts in Neovim",
            "subtitle": "Look up the shortcut you already know, then press the Neovim key for it.",
            "idea": (
                "Every VS Code shortcut has a Neovim key. Look it up, press it, keep going.",
                [
                    ("Open a file by name", "<Space><Space>", "VS Code: Cmd+P."),
                    ("Run any command", "<Space>sC", "VS Code: Cmd+Shift+P."),
                    ("Go to definition", "gd", "VS Code: F12."),
                    ("Rename a symbol", "<Space>cr", "VS Code: F2."),
                ],
                None,
            ),
            "problem": {
                "fail": "You know the VS Code shortcut but not the Neovim key, so you reach for the mouse.",
                "fix": "Find the shortcut in the tables below and press the Neovim key. Muscle memory moves over one key at a time.",
            },
            "drills": [
                {
                    "h2": "Find and open",
                    "intro": "These are the shortcuts you press all day. Cmd+D and Cmd+Shift+L live in Module 3, page 4.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Find and open", "rows": [
                            ("<Space><Space>", "Cmd+P: open a file by name"),
                            ("<Space>sC", "Cmd+Shift+P: run any command by name"),
                            ("<Space>sk", "Cmd+K Cmd+S: search every key map"),
                            ("<Space>ss", "Cmd+Shift+O: jump to a symbol in this file"),
                            ("<Space>sS", "Cmd+T: jump to a symbol in the project"),
                            ("<Space>/", "Cmd+Shift+F: search text in the project"),
                            ("<Space>,", "Ctrl+Tab: switch to another open buffer"),
                            ("<Space>e", "Cmd+B: show or hide the file tree"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Go to a line, go back", "rows": [
                            ("12G", "Ctrl+G, then 12: go to line 12 (`:12` does the same)"),
                            ("Ctrl-o", "Ctrl+-: jump back to where you were"),
                            ("Ctrl-i", "Ctrl+Shift+-: jump forward again"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Jump to a line and come back", "code": C('''
3G
12G
Ctrl-o
'''),
                         "expect": "`12G` puts the cursor on line 12, the `print(code, ...)` line in `report`. `Ctrl-o` takes you back to line 3."},
                        {"type": "text", "body": "Open `~/tw/orders.py` first. `Ctrl-o` follows jumps such as `G`, `gd` and searches. It does not follow `h`, `j`, `k` or `l`."},
                    ],
                },
                {
                    "h2": "Edit lines",
                    "intro": "Line edits are one or two keys, and `.` repeats the last change.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Line edits", "rows": [
                            ("gcc", "Cmd+/: comment or uncomment the line"),
                            ("Option+j / Option+k", "Option+Down / Option+Up: move the line down or up"),
                            ("yyp", "Shift+Option+Down: copy the line below"),
                            ("dd", "Cmd+Shift+K: delete the line"),
                            ("V", "Cmd+L: select the line"),
                            ("o / O", "Cmd+Enter / Cmd+Shift+Enter: new line below or above"),
                            (">> / <<", "Cmd+] / Cmd+[: indent or outdent the line"),
                            ("u / Ctrl-r", "Cmd+Z / Cmd+Shift+Z: undo or redo"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Grow the selection", "rows": [
                            ("Ctrl-Space", "Ctrl+Shift+Right: select the syntax node under the cursor"),
                            ("Ctrl-Space", "Press again to grow to the next node out"),
                            ("<BS>", "Shrink the selection by one node"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Copy a line and comment out the copy", "code": C('''
15G
yyp
gcc
'''),
                         "expect": "Line 16 is now `# name = \"pen\"`, a commented copy of line 15. `gcc` needs a file type, so it works in `orders.py` but not in an unnamed buffer. Discard with `:e!`."},
                        {"type": "cmd", "where": "nvim", "title": "Undo and redo the copy", "code": C('''
15G
yyp
u
Ctrl-r
'''),
                         "expect": "`yyp` adds a copy of line 15. `u` removes it. `Ctrl-r` brings it back, so lines 15 and 16 both read `name = \"pen\"`. Discard with `:e!`."},
                    ],
                },
                {
                    "h2": "Code",
                    "intro": "These need the language server from Module 5. Give it a second after opening the file.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Code keys", "rows": [
                            ("gd", "F12: go to definition"),
                            ("gr", "Shift+F12: find references"),
                            ("<Space>cr", "F2: rename the symbol in every file"),
                            ("<Space>ca", "Cmd+.: code actions and quick fixes"),
                            ("K", "Hover: show the docs for the symbol"),
                            ("gK", "Ctrl+Shift+Space: show the function signature"),
                            ("]d", "F8: jump to the next problem"),
                            ("<Space>xx", "Cmd+Shift+M: list every problem"),
                            ("<Space>cf", "Shift+Option+F: format the file"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Go to a definition and back", "code": C('''
12G
/calc_totl
Enter
gd
Ctrl-o
'''),
                         "expect": "The search lands on `calc_totl` in line 12. `gd` jumps to `def calc_totl` in line 6. `Ctrl-o` returns you to line 12."},
                        {"type": "text", "body": "Select a name and want every copy changed? That is VS Code's Cmd+D. It has its own page: Module 3, page 4."},
                    ],
                },
            ],
            "rules": {
                "h2": "VS Code to Neovim at a glance",
                "cards": [
                    ("The five you use most", "Press these first.", ["VS Code", "Neovim"], [
                        ["Cmd+P", "`<Space><Space>`"],
                        ["Cmd+Shift+P", "`<Space>sC`"],
                        ["F12", "`gd`"],
                        ["F2", "`<Space>cr`"],
                        ["Cmd+/", "`gcc`"],
                    ]),
                    ("Selection and undo", "Four keys cover most of the rest.", ["VS Code", "Neovim"], [
                        ["Cmd+L", "`V`"],
                        ["Ctrl+Shift+Right", "`Ctrl-Space`, then `<BS>` to shrink"],
                        ["Cmd+Z", "`u`"],
                        ["Cmd+Shift+Z", "`Ctrl-r`"],
                    ]),
                    ("Jump and return", "A jump leaves a trail you can walk back.", ["Keys", "Action"], [
                        ["`12G`", "Go to line 12"],
                        ["`Ctrl-o`", "Back along the trail"],
                        ["`Ctrl-i`", "Forward along the trail"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Copy a line and comment out the copy",
                "frame": "You want to keep `price` as a note and try a new value. In VS Code that is Shift+Option+Down, then Cmd+/.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 17, on `price`", "`17G`"), "`yyp`", "Puts a copy of the line below it."),
                    (None, "`gcc`", "Comments out the copy, line 18."),
                    (None, "`:e!`", "Discards the edit."),
                ],
                "before": 'price = 2.50\nnote = "rush"',
                "after": 'price = 2.50\n# price = 2.50\nnote = "rush"',
                "meaning": "Each VS Code shortcut maps to one or two keys. The copy sits on line 18 and the original stays on line 17.",
            },
            "practice": {
                "h2": "Practice: VS Code shortcuts",
                "qs": [
                    ("Mechanism", "After `gd`, why does `Ctrl-o` take you back, while `u` does nothing?",
                     "What does each key walk back through?",
                     ["`gd` is a jump, so Neovim saves where you were.", "`Ctrl-o` walks back along those jumps.", "`u` walks back through edits, and a jump changes no text."],
                     "`Ctrl-o` undoes jumps. `u` undoes edits."),
                    ("Keystrokes", "Which keys put a commented copy of line 15 on line 16?",
                     "Go to the line, copy it below, comment it.",
                     ["Press `15G`.", "Press `yyp` to copy the line below.", "Press `gcc` to comment the copy."],
                     "`15G`, `yyp`, `gcc`."),
                    ("Application", "Delete line 15 the way Cmd+Shift+K does.",
                     "One operator, doubled.",
                     ["Press `15G`.", "Press `dd`."],
                     "`15G` `dd`. `qty = 3` becomes line 15."),
                    ("Common mistake", "You grew a selection with `Ctrl-Space` and it is too big. How do you fix it?",
                     "Which key goes the other way?",
                     ["`Ctrl-Space` grows one syntax node each press.", "`<BS>` shrinks it one node."],
                     "Press `<BS>` until the selection is the size you want."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "View, layout and focus",
            "subtitle": "Zen mode, zoom and toggles: the View menu, one key at a time.",
            "idea": (
                "Most view toggles are Space u plus one letter. Press once to switch, again to switch back.",
                [
                    ("Zen mode", "<Space>uz", "VS Code: Cmd+K Z."),
                    ("Zoom a window", "<Space>wm", "The window fills the screen."),
                    ("Wrap long lines", "<Space>uw", "VS Code: Option+Z."),
                    ("Close other buffers", "<Space>bo", "VS Code: Close Others."),
                ],
                None,
            ),
            "problem": {
                "fail": "There is no View menu. You do not know which key turns wrap, zen or inlay hints on, so you leave them as they are.",
                "fix": "Learn the toggles once. Each one flips with the same key you used to turn it on.",
            },
            "drills": [
                {
                    "h2": "Focus and close",
                    "intro": "Hide the clutter, or close what you no longer need.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Focus", "rows": [
                            ("<Space>uz", "Cmd+K Z: zen mode"),
                            ("<Space>wm", "Zoom the current window to fill the screen"),
                            ("<Space>.", "New untitled file: open a scratch buffer"),
                            ("<Space>su", "Timeline: browse the undo history as a list"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Close", "rows": [
                            ("<Space>bd", "Cmd+W: close this buffer"),
                            ("<Space>bo", "Close Others: close every buffer except this one"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Zen mode on and off", "code": C('''
<Space>uz
<Space>uz
'''),
                         "expect": "The first press centres the file in a window about 120 columns wide, hides the status line and the tab line, and dims the code around it. The second press brings the normal layout back."},
                        {"type": "cmd", "where": "nvim", "title": "Zoom one window", "code": C('''
:vsplit ~/tw/notes.md
<Space>wm
<Space>wm
'''),
                         "expect": "`:vsplit` shows two windows side by side. The first `<Space>wm` makes the current window fill the screen, with a zoom label. The second press brings the split back."},
                    ],
                },
                {
                    "h2": "Toggles",
                    "intro": "Each toggle prints a short notification, so you can see which way it went.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Toggles", "rows": [
                            ("<Space>uw", "Option+Z: wrap long lines"),
                            ("<Space>uf", "Format on save: on or off for every file"),
                            ("<Space>uF", "Format on save: on or off for this buffer only"),
                            ("<Space>uh", "Inlay hints: show or hide the grey type hints"),
                            ("<Space>us", "Spell check: on or off"),
                            ("<Space>n", "Open the notification history"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Flip line wrapping", "code": C('''
:e ~/tw/notes.md
3G
<Space>uw
<Space>uw
'''),
                         "expect": "Line 3 is 81 characters long. In a window narrower than that, each `<Space>uw` flips it between wrapping onto a second row and running off the right edge. A notification names the new state."},
                        {"type": "cmd", "where": "nvim", "title": "Read what a toggle said", "code": C('''
<Space>us
<Space>n
'''),
                         "expect": "Spell check flips and a notification says so. `<Space>n` opens the notification history, where the message is listed. Press `<Space>us` again to switch spelling back."},
                    ],
                },
                {
                    "h2": "GitHub and scratch notes",
                    "intro": "Share a line of code, or keep a note you do not want in a file.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "GitHub and scratch", "rows": [
                            ("<Space>gB", "Open this file on GitHub in the browser"),
                            ("<Space>gY", "Copy the GitHub link to this file or selection"),
                            ("<Space>.", "Show or hide the scratch buffer"),
                        ]},
                        {"type": "text", "body": "`<Space>gB` and `<Space>gY` need a git repository with a GitHub remote. The `~/tw` practice files are not in one, so try them in a project of your own."},
                        {"type": "cmd", "where": "nvim", "title": "Keep a note in the scratch buffer", "code": C('''
<Space>.
i
buy more tape
Esc
<Space>.
<Space>.
'''),
                         "expect": "A scratch buffer opens in a floating window and your text goes in it. The first `<Space>.` after typing hides it. The last one shows it again, with the text still there."},
                    ],
                },
            ],
            "rules": {
                "h2": "Toggles at a glance",
                "cards": [
                    ("View toggles", "Press once to switch, again to switch back.", ["Key", "Toggles"], [
                        ["`<Space>uz`", "Zen mode"],
                        ["`<Space>wm`", "Zoom the window"],
                        ["`<Space>uw`", "Wrap"],
                        ["`<Space>uh`", "Inlay hints"],
                        ["`<Space>us`", "Spell check"],
                    ]),
                    ("Format on save", "Two switches, one scope each.", ["Key", "Scope"], [
                        ["`<Space>uf`", "Every file"],
                        ["`<Space>uF`", "This buffer only"],
                    ]),
                    ("Close things", "Keep only what you are using.", ["Key", "Closes"], [
                        ["`<Space>bd`", "This buffer"],
                        ["`<Space>bo`", "Every other buffer"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Read a long line in zen mode",
                "frame": "Line 3 of the shipping notes is one long sentence. You want to read it without the bars around it.",
                "open": "nvim ~/tw/notes.md",
                "steps": [
                    (("line 3, the long sentence", "`3G`"), "`<Space>uz`", "Centres the file and hides the bars."),
                    (None, "`<Space>uw`", "Flips wrapping for the long line."),
                    (None, "`<Space>uz`", "Brings the normal layout back."),
                ],
                "after": "Zen mode shows the file centred, with the status line and tab line hidden. A second `<Space>uz` restores them.",
                "meaning": "Toggles stack, and each one undoes itself with the same key.",
            },
            "practice": {
                "h2": "Practice: view and layout",
                "qs": [
                    ("Mechanism", "Why does a second `<Space>uz` restore your layout?",
                     "Is zen a switch or a one-way command?",
                     ["Zen is a toggle.", "The same key turns it on and off."],
                     "A toggle flips between two states, so the same key returns you."),
                    ("Keystrokes", "Which key closes every buffer except the one you are in?",
                     "It starts with `<Space>b`.",
                     ["Press `<Space>b` for the buffer keys.", "Press `o` for others."],
                     "`<Space>bo`."),
                    ("Application", "Turn off format on save for this file only. Other files keep formatting.",
                     "Capital letter, this buffer.",
                     ["Press `<Space>uF` for this buffer only."],
                     "`<Space>uF`."),
                    ("Common mistake", "You pressed `<Space>uf` to stop formatting one file, and now nothing formats. Why?",
                     "Compare the two letters.",
                     ["`<Space>uf` switches format on save for every file.", "`<Space>uF` switches it for this buffer only."],
                     "`uf` is global. Use `<Space>uF` for one buffer."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Editing helpers VS Code gave you free",
            "subtitle": "Completion, sort, compare, copy path and change case, as short Neovim commands.",
            "idea": (
                "VS Code hid these in menus and the palette. In Neovim each one is a short command.",
                [
                    ("Sort lines", ":sort", "VS Code: Sort Lines Ascending."),
                    ("Compare two files", ":diffthis", "VS Code: Compare Selected."),
                    ("Copy the file path", ":let @+ = expand('%:p')", "VS Code: Copy Path."),
                    ("Change case", "gUiw", "VS Code: Transform to Uppercase."),
                ],
                None,
            ),
            "problem": {
                "fail": "In VS Code you open the palette to sort lines, copy a path or compare two files. Here there is no menu to look in.",
                "fix": "Each helper is a command you type, and each one works on any text.",
            },
            "drills": [
                {
                    "h2": "Completion and snippets",
                    "intro": "The completion menu opens as you type. These keys drive it.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Completion", "rows": [
                            ("Ctrl-Space", "Show the completion menu"),
                            ("Ctrl-n / Ctrl-p", "Next or previous item"),
                            ("Enter / Ctrl-y", "Accept the item"),
                            ("Ctrl-e", "Close the menu without accepting"),
                        ], "try": "Go to the end of `~/tw/orders.py`, press `o`, type `calc` and press `Ctrl-Space`.",
                         "expect": "A completion menu opens under the cursor. `Ctrl-n` moves down it and `Enter` accepts the highlighted item. `Ctrl-e` closes it instead."},
                        {"type": "keys", "where": "nvim", "title": "Snippets", "rows": [
                            ("Tab", "Jump to the next field of the snippet"),
                            ("Shift-Tab", "Jump to the previous field"),
                        ]},
                    ],
                },
                {
                    "h2": "Sort, join and change case",
                    "intro": "All of these work on any text, not just code.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Sort and join", "rows": [
                            (":sort", "Sort every line in the file"),
                            (":sort u", "Sort and drop duplicate lines"),
                            (":sort i", "Sort and ignore upper and lower case"),
                            (":'<,'>sort", "Sort the selected lines (press `:` after `V`)"),
                            ("J", "Join the next line onto this one"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Change case and duplicate", "rows": [
                            ("gUiw", "Upper-case the word"),
                            ("guiw", "Lower-case the word"),
                            ("~", "Flip the case of the character under the cursor"),
                            ("y then P", "Duplicate a selection: yank it, paste it before the cursor"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Sort the to-do lines", "code": C('''
:e ~/tw/todo.txt
:12,16sort
'''),
                         "expect": "Lines 12 to 16 read: `TODO call the carrier`, `TODO print labels`, `TODO reply to Sam`, `buy boxes`, `buy tape`. Capital letters sort before small ones. Discard with `:e!`."},
                        {"type": "cmd", "where": "nvim", "title": "Sort and ignore case", "code": C('''
:12,16sort i
'''),
                         "expect": "Lines 12 to 16 now read: `buy boxes`, `buy tape`, `TODO call the carrier`, `TODO print labels`, `TODO reply to Sam`. The `i` makes the sort ignore case, so `b` comes before `T`. Discard with `:e!`."},
                        {"type": "cmd", "where": "nvim", "title": "Upper-case a word", "code": C('''
:e ~/tw/orders.py
15G
gUiw
'''),
                         "expect": "Line 15 reads `NAME = \"pen\"`. `guiw` on the same word turns it back. Discard with `:e!`."},
                        {"type": "cmd", "where": "nvim", "title": "Join two lines", "code": C('''
:e ~/tw/todo.txt
1G
J
'''),
                         "expect": "Lines 1 and 2 become one line: `item 1: pending item 2: pending`. Discard with `:e!`."},
                    ],
                },
                {
                    "h2": "Compare files, paths and the clipboard",
                    "intro": "Diff mode puts two files side by side. Registers move text around.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Compare two files", "rows": [
                            (":vsplit other", "Open the other file in a second window"),
                            (":diffthis", "Run in each window: start diff mode"),
                            (":diffoff!", "End diff mode in every window"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Paths and pasting", "rows": [
                            (":let @+ = expand('%:p')", "Copy the full path of the file"),
                            (":let @+ = expand('%')", "Copy the path as Neovim shows it"),
                            ("Ctrl-r +", "Paste the clipboard in insert mode or the command line"),
                            ("Ctrl-r 0", "Paste the last yank, even after a delete"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Compare two files", "code": C('''
:e ~/tw/orders.py
:diffthis
:vsplit ~/tw/notes.md
:diffthis
:diffoff!
'''),
                         "expect": "After the second `:diffthis`, both windows show coloured lines and scroll together. `:diffoff!` clears the colours in both windows and they scroll on their own again."},
                        {"type": "cmd", "where": "nvim", "title": "Copy the file path", "code": C('''
:e ~/tw/orders.py
:let @+ = expand('%')
:echo @+
'''),
                         "expect": "The command line prints the path of `orders.py`. It is your own path, so it differs from the next reader's. Use `expand('%:p')` for the full path."},
                    ],
                },
            ],
            "rules": {
                "h2": "VS Code helpers at a glance",
                "cards": [
                    ("VS Code to Neovim", "The palette commands, as keys and commands.", ["VS Code", "Neovim"], [
                        ["Sort Lines Ascending", "`:sort`"],
                        ["Transform to Uppercase", "`gUiw`"],
                        ["Join Lines", "`J`"],
                        ["Compare Selected", "`:diffthis` in each window"],
                        ["Copy Path", "`:let @+ = expand('%:p')`"],
                        ["Paste", "`Ctrl-r +` in insert mode"],
                    ]),
                    ("Completion keys", "The menu opens as you type.", ["Key", "Action"], [
                        ["`Ctrl-Space`", "Show the menu"],
                        ["`Ctrl-n` / `Ctrl-p`", "Next or previous"],
                        ["`Enter` / `Ctrl-y`", "Accept"],
                        ["`Ctrl-e`", "Cancel"],
                    ]),
                    ("Sort options", "One letter changes how lines compare.", ["Command", "Result"], [
                        ["`:sort`", "Capitals first, then small letters"],
                        ["`:sort i`", "Ignore case"],
                        ["`:sort u`", "Drop duplicate lines"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Sort the to-do lines",
                "frame": "The shipping to-dos are mixed up. In VS Code you would select them and run Sort Lines Ascending.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 12, first `TODO`", "`12G`"), "`V4j`", "Selects lines 12 to 16."),
                    (None, "`:sort` then `Enter`", "Sorts the selection. Neovim fills in `'<,'>` for you."),
                    (None, "`:e!`", "Discards the edit."),
                ],
                "before": "TODO call the carrier\nbuy tape\nTODO print labels\nbuy boxes\nTODO reply to Sam",
                "after": "TODO call the carrier\nTODO print labels\nTODO reply to Sam\nbuy boxes\nbuy tape",
                "meaning": "Select with `V`, then type a command: the selection becomes the range.",
            },
            "practice": {
                "h2": "Practice: editing helpers",
                "qs": [
                    ("Mechanism", "Why do the `TODO` lines come before the `buy` lines after `:sort`?",
                     "How does sort compare letters?",
                     ["`:sort` compares character codes.", "Capital letters have lower codes than small letters."],
                     "Capitals sort first. Add `i` to ignore case."),
                    ("Keystrokes", "Which keys upper-case the word `name` on line 15?",
                     "Go to the line, then use an operator on the word.",
                     ["Press `15G`.", "Press `gUiw`."],
                     "`15G`, `gUiw`."),
                    ("Application", "Join lines 1 and 2 of `todo.txt` into one line.",
                     "One letter.",
                     ["Press `1G`.", "Press `J`."],
                     "`1G` `J`. The line reads `item 1: pending item 2: pending`."),
                    ("Common mistake", "You yanked a word, then deleted a line, and `p` pastes the deleted line. How do you paste the word?",
                     "Which register keeps the last yank?",
                     ["A delete overwrites the unnamed register.", "Register `0` keeps the last yank.", "Press `\"0p`, or `Ctrl-r 0` in insert mode."],
                     "`\"0p`, or `Ctrl-r 0` in insert mode."),
                ],
            },
        },
    ],
}
