"""Module 8: Coming from VS Code. Source: the live Neovim config (LazyVim) and plain Vim; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


MODULE = {
    "n": 8,
    "folder": "m8-from-vscode",
    "title": "VS Code shortcuts in Neovim (Cmd+P and more)",
    "footer": "Neovim keys for VS Code shortcuts: open a file, go to definition, zen mode, sort lines, diff files, copy a path",
    "tagline": "Find the Neovim key for a VS Code shortcut: Cmd+P, F12, Cmd+/, sort lines and more.",
    "glossary": [
        ("tw-zen", "Zen mode", ["zen mode", "zen"], "Hide the bars and centre the file in the window. Turn it on and off with Space u z."),
        ("tw-diff", "Diff mode", ["diff mode"], "Compare two files: both windows scroll together and the lines that differ are coloured. Start it with :diffthis in each window."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Cmd+P, F12 and other VS Code shortcuts in Neovim",
            "subtitle": "Open a file by name (Cmd+P), open the command palette, go to definition, rename a symbol, comment a line",
            "idea": (
                "Find the Neovim key for a VS Code shortcut: look it up, press it, keep going.",
                [
                    ("Open a file by name (Cmd+P)", "<Space><Space>", "VS Code: Cmd+P."),
                    ("Open the command palette", "<Space>sC", "VS Code: Cmd+Shift+P."),
                    ("Go to definition", "gd", "VS Code: F12."),
                    ("Rename a symbol", "<Space>cr", "VS Code: F2."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I find the Neovim key for a VS Code shortcut I already know? Without it you reach for the mouse.",
                "fix": "Find the shortcut in the tables below and press the Neovim key. Muscle memory moves over one key at a time.",
            },
            "drills": [
                {
                    "h2": "Open a file, search the project and jump to a symbol (Cmd+P, Cmd+Shift+F)",
                    "intro": "Find the shortcuts you press all day. Multi cursor (Cmd+D and Cmd+Shift+L) lives in Module 3, page 4.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open a file by name, search the project and find a symbol", "rows": [
                            ("<Space><Space>", "Open a file by name (VS Code Cmd+P)"),
                            ("<Space>sC", "Open the command palette and run any command by name (VS Code Cmd+Shift+P)"),
                            ("<Space>sk", "Search every key map (VS Code Cmd+K Cmd+S)"),
                            ("<Space>ss", "Jump to a symbol in this file (VS Code Cmd+Shift+O)"),
                            ("<Space>sS", "Jump to a symbol in the project (VS Code Cmd+T)"),
                            ("<Space>/", "Search text in the project (VS Code Cmd+Shift+F)"),
                            ("<Space>,", "Switch to another open buffer (tab): files below `:pwd` (VS Code Ctrl+Tab)"),
                            ("<Space>fB", "List every buffer, hidden ones too: files below `:pwd`"),
                            ("<Space>e", "Show or hide the file explorer (VS Code Cmd+B)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Go to a line number and jump back", "rows": [
                            ("12G", "Go to line 12 (VS Code Ctrl+G, then 12; `:12` does the same)"),
                            ("Ctrl-o", "Jump back to where you were (VS Code Ctrl+-)"),
                            ("Ctrl-i", "Jump forward again (VS Code Ctrl+Shift+-)"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Go to line 12 and jump back to where you were", "code": C('''
3G
12G
Ctrl-o
'''),
                         "expect": "`12G` puts the cursor on line 12, the `print(code, ...)` line in `report`. `Ctrl-o` takes you back to line 3."},
                        {"type": "cmd", "where": "shell", "title": "Open a folder or file from the terminal (VS Code code .)", "code": C('''
cd ~/tw
v.
v notes.md
v --help
'''),
                         "expect": "`v.` opens the current folder in Neovim, and `v notes.md` opens that file. Quit each with `:q` to reach the next line. `v --help` prints the launcher's shortcut sheet and returns to the prompt without opening Neovim. `vi` and `vim` run `v` too."},
                        {"type": "text", "body": "Why does `Ctrl-o` not go back after I move? Open `~/tw/orders.py` first. `Ctrl-o` follows jumps such as `G`, `gd` and searches. It does not follow `h`, `j`, `k` or `l`."},
                    ],
                },
                {
                    "h2": "Comment, move, copy and delete a line (Cmd+/, Option+Down)",
                    "intro": "Edit a line with one or two keys, and repeat the last change with `.`. Autosave writes a file about 3 seconds after you stop typing, and when you leave the buffer, so `:e!` cannot bring the original back. Undo practice edits with `u`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Comment, move, copy, delete and indent a line", "rows": [
                            ("gcc", "Comment or uncomment the line (VS Code Cmd+/)"),
                            ("Option+j / Option+k", "Move the line down or up (VS Code Option+Down / Option+Up)"),
                            ("V, then Option+j / Option+k", "Move all the selected lines; they stay selected (VS Code Option+Down / Option+Up on a selection)"),
                            ("yyp", "Copy the line below (VS Code Shift+Option+Down)"),
                            ("dd", "Delete the line (VS Code Cmd+Shift+K)"),
                            ("V", "Select the line (VS Code Cmd+L)"),
                            ("o / O", "Open a new line below or above (VS Code Cmd+Enter / Cmd+Shift+Enter)"),
                            (">> / <<", "Indent or outdent the line (VS Code Cmd+] / Cmd+[)"),
                            ("u / Ctrl-r", "Undo or redo (VS Code Cmd+Z / Cmd+Shift+Z)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Leave insert mode and move the cursor without the arrow keys", "rows": [
                            ("jk", "Leave insert mode: type `j` then `k` quickly (same as `Esc`)"),
                            ("Option+h / j / k / l", "Move the cursor left, down, up or right without leaving insert mode (VS Code arrow keys)"),
                        ], "try": "In `~/tw/notes.md` press `o`, type `hello`, then `jk`. Press `u` to remove the line.",
                         "expect": "The `j` and `k` are not typed and you are back in normal mode. After `u`, the added line disappears."},
                        {"type": "keys", "where": "nvim", "title": "Turn autosave off and on", "rows": [
                            (":ASToggle", "Pause autosave. Run it again to turn it back on"),
                        ], "try": "Run `:ASToggle`, change a word, wait 5 seconds, run `:e!`, then run `:ASToggle` again.",
                         "expect": "While paused, nothing is written until you save with `:w`, so `:e!` reloads the original word. After the second `:ASToggle`, autosave saves your edits again."},
                        {"type": "keys", "where": "nvim", "title": "Select a bigger piece of code with each press (expand selection)", "rows": [
                            ("Ctrl-Space", "Select the syntax node under the cursor (VS Code Ctrl+Shift+Right)"),
                            ("Ctrl-Space", "Grow the selection to the next node out: press again"),
                            ("<BS>", "Shrink the selection by one node"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Duplicate a line and comment out the copy", "code": C('''
15G
yyp
gcc
'''),
                         "expect": "Line 16 is now `# name = \"pen\"`, a commented copy of line 15. `gcc` needs a file type, so it works in `orders.py` but not in an unnamed buffer. Press `u` twice to undo both edits."},
                        {"type": "cmd", "where": "nvim", "title": "Undo a change and redo it", "code": C('''
15G
yyp
u
Ctrl-r
'''),
                         "expect": "`yyp` adds a copy of line 15. `u` removes it. `Ctrl-r` brings it back, so lines 15 and 16 both read `name = \"pen\"`. Press `u` once more to remove the copy."},
                    ],
                },
                {
                    "h2": "Go to definition, rename a symbol and format code (F12, F2)",
                    "intro": "Use these keys after the language server from Module 5 is running. Give it a second after opening the file.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Go to definition, find references, rename, fix and format", "rows": [
                            ("gd", "Go to definition (VS Code F12)"),
                            ("gr", "Find references (VS Code Shift+F12)"),
                            ("<Space>cr", "Rename the symbol in every file (VS Code F2)"),
                            ("<Space>ca", "Show code actions and quick fixes (VS Code Cmd+.)"),
                            ("K", "Show the docs for the symbol: hover"),
                            ("gK", "Show the function signature (VS Code Ctrl+Shift+Space)"),
                            ("]d", "Jump to the next problem (VS Code F8)"),
                            ("<Space>xx", "List every problem (VS Code Cmd+Shift+M)"),
                            ("<Space>cf", "Format the file (VS Code Shift+Option+F)"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Jump to where a function is defined and go back", "code": C('''
12G
/calc_totl
Enter
gd
Ctrl-o
'''),
                         "expect": "The search lands on `calc_totl` in line 12. `gd` jumps to `def calc_totl` in line 6. `Ctrl-o` returns you to line 12."},
                        {"type": "text", "body": "How do I change every copy of a selected name, like VS Code's Cmd+D multi cursor? It has its own page: Module 3, page 4."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which Neovim key replaces a VS Code shortcut",
                "cards": [
                    ("The five VS Code shortcuts you use most", "Press these first.", ["VS Code", "Neovim"], [
                        ["Cmd+P", "`<Space><Space>`"],
                        ["Cmd+Shift+P", "`<Space>sC`"],
                        ["F12", "`gd`"],
                        ["F2", "`<Space>cr`"],
                        ["Cmd+/", "`gcc`"],
                    ]),
                    ("Select a line, expand the selection, undo and redo", "Four keys cover most of the rest.", ["VS Code", "Neovim"], [
                        ["Cmd+L", "`V`"],
                        ["Ctrl+Shift+Right", "`Ctrl-Space`, then `<BS>` to shrink"],
                        ["Cmd+Z", "`u`"],
                        ["Cmd+Shift+Z", "`Ctrl-r`"],
                    ]),
                    ("Jump to a line and go back", "Every jump leaves a trail you can walk back.", ["Keys", "Action"], [
                        ["`12G`", "Go to line 12"],
                        ["`Ctrl-o`", "Go back along the trail"],
                        ["`Ctrl-i`", "Go forward along the trail"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Duplicate a line and comment out the copy",
                "frame": "Keep `price` as a note and try a new value. In VS Code that is Shift+Option+Down, then Cmd+/.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 17, on `price`", "`17G`"), "`yyp`", "Copy the line below it."),
                    (None, "`gcc`", "Comment out the copy, line 18."),
                    (None, "`u` twice", "Undo the comment and the copy. Autosave writes the original back."),
                ],
                "before": 'price = 2.50\nnote = "rush"',
                "after": 'price = 2.50\n# price = 2.50\nnote = "rush"',
                "meaning": "Each VS Code shortcut maps to one or two keys. The copy sits on line 18 and the original stays on line 17.",
            },
            "practice": {
                "h2": "Check your answers: VS Code shortcuts in Neovim",
                "qs": [
                    ("Mechanism", "Why does `Ctrl-o` take me back after `gd`, while `u` does nothing?",
                     "What does each key walk back through?",
                     ["`gd` is a jump, so Neovim saves where you were.", "`Ctrl-o` walks back along those jumps.", "`u` walks back through edits, and a jump changes no text."],
                     "`Ctrl-o` undoes jumps. `u` undoes edits."),
                    ("Keystrokes", "How do I put a commented copy of line 15 on line 16?",
                     "Go to the line, copy it below, comment it.",
                     ["Press `15G`.", "Press `yyp` to copy the line below.", "Press `gcc` to comment the copy."],
                     "`15G`, `yyp`, `gcc`."),
                    ("Application", "How do I delete line 15 the way Cmd+Shift+K does?",
                     "One operator, doubled.",
                     ["Press `15G`.", "Press `dd`."],
                     "`15G` `dd`. `qty = 3` becomes line 15."),
                    ("Common mistake", "How do I shrink a selection that `Ctrl-Space` made too big?",
                     "Which key goes the other way?",
                     ["`Ctrl-Space` grows one syntax node each press.", "`<BS>` shrinks it one node."],
                     "Press `<BS>` until the selection is the size you want."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Turn on zen mode, zoom a window and wrap lines in Neovim",
            "subtitle": "Turn on zen mode (Cmd+K Z), zoom a window, wrap long lines, close other buffers, turn off format on save",
            "idea": (
                "Turn a view setting on or off with Space u plus one letter. Press once to switch, again to switch back.",
                [
                    ("Turn on zen mode", "<Space>uz", "VS Code: Cmd+K Z."),
                    ("Zoom a window", "<Space>wm", "The window fills the screen."),
                    ("Wrap long lines", "<Space>uw", "VS Code: Option+Z."),
                    ("Close other buffers (tabs)", "<Space>bo", "VS Code: Close Others."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I turn wrap, zen or inlay hints on and off? There is no View menu, so you leave them as they are.",
                "fix": "Learn the toggles once. Each one flips with the same key you used to turn it on.",
            },
            "drills": [
                {
                    "h2": "Hide the clutter and close the files you no longer need",
                    "intro": "Hide the clutter, or close what you no longer need.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Turn on zen mode, zoom a window and open a scratch note", "rows": [
                            ("<Space>uz", "Turn zen mode on or off (VS Code Cmd+K Z)"),
                            ("<Space>wm", "Zoom the current window to fill the screen"),
                            ("<Space>.", "Open a scratch buffer: a persistent scratch buffer for notes"),
                            ("<Space>su", "Browse the undo history as a list: timeline"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Close this file or every other file (VS Code Cmd+W)", "rows": [
                            ("<Space>bd", "Close this buffer (VS Code Cmd+W)"),
                            ("<Space>bo", "Close every buffer except this one (VS Code Close Others)"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Turn zen mode on and off", "code": C('''
<Space>uz
<Space>uz
'''),
                         "expect": "The first press centres the file in a window about 120 columns wide, hides the status line and the tab line, and dims the code around it. The second press brings the normal layout back."},
                        {"type": "cmd", "where": "nvim", "title": "Zoom one window, then bring the split back", "code": C('''
:vsplit ~/tw/notes.md
<Space>wm
<Space>wm
'''),
                         "expect": "`:vsplit` shows two windows side by side. The first `<Space>wm` makes the current window fill the screen, with a zoom label. The second press brings the split back."},
                    ],
                },
                {
                    "h2": "Turn word wrap, format on save and spell check on or off",
                    "intro": "See which way a toggle went: each one prints a short notification.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Wrap lines, format on save, inlay hints and spell check", "rows": [
                            ("<Space>uw", "Wrap long lines, or stop wrapping (VS Code Option+Z)"),
                            ("<Space>uf", "Turn format on save on or off for every file"),
                            ("<Space>uF", "Turn format on save on or off for this buffer only"),
                            ("<Space>uh", "Show or hide the grey type hints: inlay hints"),
                            ("<Space>us", "Turn spell check on or off"),
                            ("<Space>n", "Open the notification history"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Wrap a long line or stop wrapping it", "code": C('''
:e ~/tw/notes.md
3G
<Space>uw
<Space>uw
'''),
                         "expect": "Line 3 is 81 characters long. In a window narrower than that, each `<Space>uw` flips it between wrapping onto a second row and running off the right edge. A notification names the new state."},
                        {"type": "cmd", "where": "nvim", "title": "Read the message a toggle printed", "code": C('''
<Space>us
<Space>n
'''),
                         "expect": "Spell check flips and a notification says so. `<Space>n` opens the notification history, where the message is listed. Press `<Space>us` again to switch spelling back."},
                    ],
                },
                {
                    "h2": "Open a file on GitHub and keep scratch notes",
                    "intro": "Share a line of code, or keep a note you do not want in a file.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open or copy a GitHub link and show the scratch buffer", "rows": [
                            ("<Space>gB", "Open this file on GitHub in the browser"),
                            ("<Space>gY", "Copy the GitHub link to this file or selection"),
                            ("<Space>.", "Show or hide the scratch buffer"),
                        ]},
                        {"type": "text", "body": "Why do `<Space>gB` and `<Space>gY` fail on my practice files? They need a git repository with a GitHub remote, and the `~/tw` practice files are not in one. Try them in a project of your own."},
                        {"type": "cmd", "where": "nvim", "title": "Write a quick note in the scratch buffer", "code": C('''
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
                "h2": "Which key turns zen mode, wrap or spell check on and off",
                "cards": [
                    ("Turn a view setting on or off", "Press once to switch, again to switch back.", ["Key", "Toggles"], [
                        ["`<Space>uz`", "Zen mode"],
                        ["`<Space>wm`", "Zoom the window"],
                        ["`<Space>uw`", "Wrap"],
                        ["`<Space>uh`", "Inlay hints"],
                        ["`<Space>us`", "Spell check"],
                    ]),
                    ("Turn off format on save for every file or one file", "Two switches, one scope each.", ["Key", "Scope"], [
                        ["`<Space>uf`", "Every file"],
                        ["`<Space>uF`", "This buffer only"],
                    ]),
                    ("Close this buffer or every other buffer", "Keep only what you are using.", ["Key", "Closes"], [
                        ["`<Space>bd`", "This buffer"],
                        ["`<Space>bo`", "Every other buffer"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Read a long line in zen mode",
                "frame": "Read line 3 of the shipping notes, one long sentence, without the bars around it.",
                "open": "nvim ~/tw/notes.md",
                "steps": [
                    (("line 3, the long sentence", "`3G`"), "`<Space>uz`", "Centre the file and hide the bars."),
                    (None, "`<Space>uw`", "Flip wrapping for the long line."),
                    (None, "`<Space>uz`", "Bring the normal layout back."),
                ],
                "after": "Zen mode shows the file centred, with the status line and tab line hidden. A second `<Space>uz` restores them.",
                "meaning": "Toggles stack, and each one undoes itself with the same key.",
            },
            "practice": {
                "h2": "Check your answers: zen mode, toggles and closing buffers",
                "qs": [
                    ("Mechanism", "Why does a second `<Space>uz` restore my layout?",
                     "Is zen a switch or a one-way command?",
                     ["Zen is a toggle.", "The same key turns it on and off."],
                     "A toggle flips between two states, so the same key returns you."),
                    ("Keystrokes", "Which key closes every buffer except the one I am in?",
                     "It starts with `<Space>b`.",
                     ["Press `<Space>b` for the buffer keys.", "Press `o` for others."],
                     "`<Space>bo`."),
                    ("Application", "How do I turn off format on save for this file only, so other files keep formatting?",
                     "Capital letter, this buffer.",
                     ["Press `<Space>uF` for this buffer only."],
                     "`<Space>uF`."),
                    ("Common mistake", "Why does nothing format after I pressed `<Space>uf` to stop formatting one file?",
                     "Compare the two letters.",
                     ["`<Space>uf` switches format on save for every file.", "`<Space>uF` switches it for this buffer only."],
                     "`uf` is global. Use `<Space>uF` for one buffer."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Sort lines, compare files and copy a path in Neovim",
            "subtitle": "Sort lines, compare two files (diff), copy the file path, change case, use autocomplete and snippets",
            "idea": (
                "Do the VS Code menu and palette jobs in Neovim: each one is a short command.",
                [
                    ("Sort lines", ":sort", "VS Code: Sort Lines Ascending."),
                    ("Compare two files (diff)", ":diffthis", "VS Code: Compare Selected."),
                    ("Copy the file path", ":let @+ = expand('%:p')", "VS Code: Copy Path."),
                    ("Change case to UPPER or lower", "gUiw", "VS Code: Transform to Uppercase."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I sort lines, copy a path or compare two files without the VS Code palette? Here there is no menu to look in.",
                "fix": "Each helper is a command you type, and each one works on any text.",
            },
            "drills": [
                {
                    "h2": "Use autocomplete and snippets (completion menu)",
                    "intro": "Pick an item from the completion menu, which opens as you type. These keys drive it.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open the completion menu and pick an item", "rows": [
                            ("Ctrl-Space", "Show the completion menu"),
                            ("Ctrl-n / Ctrl-p", "Go to the next or previous item"),
                            ("Enter / Ctrl-y", "Accept the item"),
                            ("Ctrl-e", "Close the menu without accepting"),
                        ], "try": "Go to the end of `~/tw/orders.py`, press `o`, type `calc` and press `Ctrl-Space`.",
                         "expect": "A completion menu opens under the cursor. `Ctrl-n` moves down it and `Enter` accepts the highlighted item. `Ctrl-e` closes it instead."},
                        {"type": "keys", "where": "nvim", "title": "Jump between the fields of a snippet", "rows": [
                            ("Tab", "Jump to the next field of the snippet"),
                            ("Shift-Tab", "Jump to the previous field"),
                        ]},
                    ],
                },
                {
                    "h2": "Sort lines, join lines and change case (UPPER, lower)",
                    "intro": "Use these on any text, not just code.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Sort lines and join lines", "rows": [
                            (":sort", "Sort every line in the file"),
                            (":sort u", "Sort and drop duplicate lines"),
                            (":sort i", "Sort and ignore upper and lower case"),
                            (":'<,'>sort", "Sort the selected lines (press `:` after `V`)"),
                            ("J", "Join the next line onto this one"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Change case and duplicate a selection", "rows": [
                            ("gUiw", "Upper-case the word"),
                            ("guiw", "Lower-case the word"),
                            ("~", "Flip the case of the character under the cursor"),
                            ("y then P", "Duplicate a selection: yank it, paste it before the cursor"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Sort the to-do lines", "code": C('''
:e ~/tw/todo.txt
:12,16sort
'''),
                         "expect": "Lines 12 to 16 read: `TODO call the carrier`, `TODO print labels`, `TODO reply to Sam`, `buy boxes`, `buy tape`. Capital letters sort before small ones. Press `u` to undo the sort."},
                        {"type": "cmd", "where": "nvim", "title": "Sort lines and ignore upper and lower case", "code": C('''
:12,16sort i
'''),
                         "expect": "Lines 12 to 16 now read: `buy boxes`, `buy tape`, `TODO call the carrier`, `TODO print labels`, `TODO reply to Sam`. The `i` makes the sort ignore case, so `b` comes before `T`. Press `u` to undo the sort."},
                        {"type": "cmd", "where": "nvim", "title": "Change a word to UPPER case", "code": C('''
:e ~/tw/orders.py
15G
gUiw
'''),
                         "expect": "Line 15 reads `NAME = \"pen\"`. `guiw` on the same word turns it back, or press `u`."},
                        {"type": "cmd", "where": "nvim", "title": "Join two lines into one", "code": C('''
:e ~/tw/todo.txt
1G
J
'''),
                         "expect": "Lines 1 and 2 become one line: `item 1: pending item 2: pending`. Press `u` to split them again."},
                    ],
                },
                {
                    "h2": "Compare two files (diff), copy a file path and paste from the clipboard",
                    "intro": "Put two files side by side with diff mode. Move text around with registers.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Compare two files side by side (diff)", "rows": [
                            (":vsplit other", "Open the other file in a second window"),
                            (":diffthis", "Run in each window: start diff mode"),
                            (":diffoff!", "End diff mode in every window"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Open the file in another app", "rows": [
                            ("<Space>oi", "Open this file in its default macOS app"),
                        ], "try": "Open `~/tw/notes.md` and press `<Space>oi`.",
                         "expect": "The file opens in the macOS app that is the default for `.md` files."},
                        {"type": "keys", "where": "nvim", "title": "Copy text to the system clipboard with the mouse", "rows": [
                            ("Drag, then release", "Copy the dragged text to the system clipboard (VS Code Cmd+C on a selection)"),
                        ], "try": "In `~/tw/notes.md`, drag over a line, release, then press `Cmd+V` in another app.",
                         "expect": "The highlight clears and the text is on the system clipboard."},
                        {"type": "keys", "where": "nvim", "title": "Copy a file path and paste from the clipboard", "rows": [
                            (":let @+ = expand('%:p')", "Copy the full path of the file"),
                            (":let @+ = expand('%')", "Copy the path as Neovim shows it"),
                            ("Ctrl-r +", "Paste the clipboard in insert mode or the command line"),
                            ("Ctrl-r 0", "Paste the last yank, even after a delete"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Compare two files and clear the diff colours", "code": C('''
:e ~/tw/orders.py
:diffthis
:vsplit ~/tw/notes.md
:diffthis
:diffoff!
'''),
                         "expect": "After the second `:diffthis`, both windows show coloured lines and scroll together. `:diffoff!` clears the colours in both windows and they scroll on their own again."},
                        {"type": "cmd", "where": "nvim", "title": "Copy the path of the file you are editing", "code": C('''
:e ~/tw/orders.py
:let @+ = expand('%')
:echo @+
'''),
                         "expect": "The command line prints the path of `orders.py`. It is your own path, so it differs from the next reader's. Use `expand('%:p')` for the full path."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which Neovim command replaces a VS Code palette command",
                "cards": [
                    ("Sort, compare, copy a path and paste (VS Code palette to Neovim)", "Each palette command, as a key or a command.", ["VS Code", "Neovim"], [
                        ["Sort Lines Ascending", "`:sort`"],
                        ["Transform to Uppercase", "`gUiw`"],
                        ["Join Lines", "`J`"],
                        ["Compare Selected", "`:diffthis` in each window"],
                        ["Copy Path", "`:let @+ = expand('%:p')`"],
                        ["Paste", "`Ctrl-r +` in insert mode"],
                        ["Open this file in its default macOS app", "`<Space>oi`"],
                    ]),
                    ("Pick an item from the completion menu", "The menu opens as you type.", ["Key", "Action"], [
                        ["`Ctrl-Space`", "Show the menu"],
                        ["`Ctrl-n` / `Ctrl-p`", "Go to the next or previous item"],
                        ["`Enter` / `Ctrl-y`", "Accept the item"],
                        ["`Ctrl-e`", "Cancel and close the menu"],
                    ]),
                    ("Sort lines, ignore case or drop duplicates", "One letter changes how lines compare.", ["Command", "Result"], [
                        ["`:sort`", "Capitals first, then small letters"],
                        ["`:sort i`", "Ignore case"],
                        ["`:sort u`", "Drop duplicate lines"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Sort the to-do lines (Sort Lines Ascending)",
                "frame": "Sort the mixed-up shipping to-dos. In VS Code you would select them and run Sort Lines Ascending.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 12, first `TODO`", "`12G`"), "`V4j`", "Select lines 12 to 16."),
                    (None, "`:sort` then `Enter`", "Sort the selection. Neovim fills in `'<,'>` for you."),
                    (None, "`u`", "Undo the sort. Autosave writes the original back."),
                ],
                "before": "TODO call the carrier\nbuy tape\nTODO print labels\nbuy boxes\nTODO reply to Sam",
                "after": "TODO call the carrier\nTODO print labels\nTODO reply to Sam\nbuy boxes\nbuy tape",
                "meaning": "Select with `V`, then type a command: the selection becomes the range.",
            },
            "practice": {
                "h2": "Check your answers: sort, case, join and paste",
                "qs": [
                    ("Mechanism", "Why do the `TODO` lines come before the `buy` lines after `:sort`?",
                     "How does sort compare letters?",
                     ["`:sort` compares character codes.", "Capital letters have lower codes than small letters."],
                     "Capitals sort first. Add `i` to ignore case."),
                    ("Keystrokes", "How do I upper-case the word `name` on line 15?",
                     "Go to the line, then use an operator on the word.",
                     ["Press `15G`.", "Press `gUiw`."],
                     "`15G`, `gUiw`."),
                    ("Application", "How do I join lines 1 and 2 of `todo.txt` into one line?",
                     "One letter.",
                     ["Press `1G`.", "Press `J`."],
                     "`1G` `J`. The line reads `item 1: pending item 2: pending`."),
                    ("Common mistake", "How do I paste a yanked word after I deleted a line, when `p` pastes the deleted line?",
                     "Which register keeps the last yank?",
                     ["A delete overwrites the unnamed register.", "Register `0` keeps the last yank.", "Press `\"0p`, or `Ctrl-r 0` in insert mode."],
                     "`\"0p`, or `Ctrl-r 0` in insert mode."),
                ],
            },
        },
    ],
}
