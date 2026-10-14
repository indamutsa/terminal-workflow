"""Module 6: plugins and the key map. Sources: lesson 06 (second half) and the quick-start guide."""
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


SURROUND = r'''
gsa{motion}{char}   Surround text with a character: add surrounding (gsa + motion + char)
gsd{char}           Remove the surrounding characters: delete surrounding
gsr{old}{new}       Change the surrounding characters: replace surrounding
gsf / gsF           Jump to the next / previous surrounding: find surrounding
gsh                 Show the surrounding characters: highlight surrounding
'''

SURROUND_EX = r'''
gsaiw"           Surround the word with "
gsa3w(           Surround 3 words with ()
gsd(             Remove the surrounding ()
gsr({            Change () to {}
'''

FLASH_JUMP = r'''
s{chars}         Jump to any visible text: type s, then the first letters, then press the label that appears on the match
                 Works in normal, visual and operator-pending mode
'''

FLASH_TS = r'''
S                Select a function, block or class: treesitter node
                 Press S → labels appear on code structures → pick one to select it
                 Chain: S → label → expand with S again for parent node
'''

FLASH_REMOTE = r'''
yr{label}{motion}  Copy text from a far-away spot without moving the cursor: remote yank
dr{label}{motion}  Delete text at a far-away spot without moving the cursor: remote delete
cr{label}{motion}  Change text at a far-away spot: remote change
'''

FLASH_SEARCH = r'''
/pattern         Search for text and jump to a match: Ctrl-s turns on jump labels during a / search, then press a label
f{char}          Jump to a character on the line (f lands on it, t stops before it): ; repeats, , reverses
t{char}          Jump to just before a character: ; repeats the jump, , reverses it
'''

HARPOON = r'''
<Space>H         Add this file to the harpoon list
<Space>h         Open the harpoon menu: see all marked files, reorder or delete them
<Space>1         Jump to harpoon file 1
<Space>2         Jump to harpoon file 2
<Space>3         Jump to harpoon file 3
<Space>4         Jump to harpoon file 4
...              up to
<Space>9         Jump to harpoon file 9
'''

AERIAL = r'''
<Space>cs        Open or close the symbols outline: Aerial
{                Jump to the previous function or class: symbol
}                Jump to the next function or class: symbol
'''

AERIAL_PANEL = r'''
Enter            Jump to that symbol
o                Open or close the children of the symbol under the cursor: toggle
p                Preview the symbol in the code and keep the cursor in Aerial: scroll
l                Open the symbol's children: expand
h                Close the symbol's children: collapse
L                Open the symbol's children and everything below them: expand recursively
H                Close the symbol's children and everything below them: collapse recursively
zR               Open every symbol in the outline: expand all
zM               Close every symbol in the outline: collapse all
'''

TS_SELECT = r'''
vaf              Select a whole function: around function (including def/signature)
vif              Select a function body: inside function (body only)
vac              Select a whole class: around class
vic              Select a class body: inside class
vaa              Select an argument with its comma: around argument
via              Select an argument: inside argument
daf              Delete the entire function
yif              Copy the function body
caa              Change an argument
'''

TS_MOVE = r'''
]f               Jump to the next function start
[f               Jump to the previous function start
]c               Jump to the next class start
[c               Jump to the previous class start
'''

MINI_AI = r'''
af / if          Target a function: around / inside function
ac / ic          Target a class: around / inside class
ao / io          Target a code block: around / inside block (treesitter)
a) i) a] i] a} i}  Target the text in brackets: searches forward on the line if the cursor is not inside one
aq / iq          Target quoted text: around / inside any quote
an / in          Target the next match: next text object (e.g. `cin)` changes the text in the next parens)
al / il          Target the previous match: last text object
g[ / g]          Jump to the start / end of the text object named next, e.g. g[f
'''

BUFFERLINE = [
    ("L (Shift-L)", "Go to the next buffer"),
    ("H (Shift-H)", "Go to the previous buffer"),
] + R(r'''
<Space>bp        Pin or unpin this buffer
<Space>bP        Close all buffers that are not pinned
<Space>bj        Go to a buffer by its label: pick
<Space>bl        Close the buffers to the left
<Space>br        Close the buffers to the right
<Space>bd        Close this buffer
''')

PERSISTENCE = r'''
<Space>qs        Restore the session for this directory
<Space>ql        Restore the last session
<Space>qS        Pick a session to restore
<Space>qd        Stop saving the current session: don't save
'''

YANKY = r'''
<Space>p         Paste an earlier yank: open the yank history picker
p / P            Paste after / before the cursor (yanky-aware)
[y / ]y          Swap the pasted text for an older / newer yank: cycle the yank history
]p / [p          Paste and match the indent of the current line
gp / gP          Paste and leave the cursor after the pasted text
'''

TODO = r'''
]t / [t          Jump to the next / previous todo comment
<Space>st        Search all todo comments in a picker
<Space>sT        Search only TODO, FIX and FIXME comments
<Space>xt        Show the todo comments in the Trouble panel
'''

DADBOD = r'''
<Space>D         Open or close the database UI: explorer of connections and tables
'''

RENDER_MD = r'''
<Space>um        Turn inline Markdown rendering on or off: UI toggle
'''

MD_PREVIEW = r'''
<Space>cp        Preview the Markdown file in the browser: it refreshes live
'''

NAVIGATOR = r'''
Ctrl-h           Change to the window or tmux pane on the left (works across nvim and tmux)
Ctrl-j           Change to the window or tmux pane below
Ctrl-k           Change to the window or tmux pane above
Ctrl-l           Change to the window or tmux pane on the right
'''

WHICH_KEY = r'''
<Space>           Show all leader groups: press and wait
<Space>?          Show the keymaps of this buffer
g                 Show all g commands: press and wait
z                 Show all z commands: press and wait
<Space>sk         Find a key by what it does: fuzzy-search all keymaps by description
'''

G_NAV = r'''
gg               Go to the first line of the file
G                Go to the last line of the file (not a g key, but related)
gi               Go back to where you last typed and start inserting
gf               Open the file whose path is under the cursor
gx               Open the path or URL under the cursor in the system app (browser, Finder)
gO               Show the outline of this file: document symbols (LSP)
g,               Go to a newer position in the change list
g;               Go to an older position in the change list
'''

G_SEARCH = r'''
gn               Select the next match: search forwards and select it
gN               Select the previous match: search backwards and select it
'''

G_CASE = r'''
gu{motion}       Make text lowercase (e.g., `guiw` = lowercase word)
gU{motion}       Make text uppercase (e.g., `gUiw` = uppercase word)
g~{motion}       Swap upper and lower case (e.g., `g~iw` = toggle word)
~                Swap the case of the character under the cursor
'''

G_COMMENTS = r'''
gc{motion}       Comment or uncomment lines (e.g., `gcip` = comment paragraph)
gcc              Comment line: toggle the comment on this line
gcO              Add a comment line above
gco              Add a comment line below
'''

G_LSP = r'''
gd               Go to definition
gr               Find every use: references
gI               Go to the implementation
gy               Go to the type definition
gD               Go to the declaration
gK               Show the function signature: signature help
gO               Show the outline of this file: document symbols
K                Show docs for the word under the cursor: hover
'''

G_FORMAT = r'''
gw{motion}       Wrap text to the text width: format text
gq{motion}       Wrap text and move the cursor to the end: format text
'''

G_TABS = r'''
gt               Go to the next tab page
gT               Go to the previous tab page
'''

G_MARKS = r'''
g'{mark}         Jump to a mark without changing the jump list (like `'{mark}`)
'''

G_MISC = r'''
ga               Show the character code under the cursor (ASCII, hex, octal)
g8               Show the UTF-8 bytes of the character under the cursor
gv               Select the last selection again: reselect
gJ               Join lines without adding a space
gf               Open the file whose path is under the cursor
'''

BRACKETS = r'''
]d / [d          Jump to the next / previous diagnostic (error or warning)
]h / [h          Jump to the next / previous git hunk
]m / [m          Jump to the next / previous method or function start
]M / [M          Jump to the next / previous method or function end
]{ / [{          Jump to the next / previous unmatched {
]] / [[          Jump to the next / previous use of the word under the cursor
]s / [s          Jump to the next / previous misspelled word
]q / [q          Jump to the next / previous quickfix item
]b / [b          Go to the next / previous buffer
'''

Z_SCROLL = r'''
zz               Center this line on the screen
zt               Move this line to the top of the screen
zb               Move this line to the bottom of the screen
zH               Scroll half a screen to the left
zL               Scroll half a screen to the right
'''

Z_FOLD = r'''
za               Open or close the fold under the cursor
zA               Open or close the fold and its inner folds
zo               Open the fold
zO               Open the fold and its inner folds
zc               Close the fold
zC               Close the fold and its outer folds
zM               Close all folds in the file
zR               Open all folds in the file
zj               Go to the next fold
zk               Go to the previous fold
'''

Z_SPELL = r'''
z=               Fix a misspelled word: show spelling suggestions
zg               Add the word to the dictionary: mark as good
zw               Mark the word as wrong
'''

CTRL_NAV = r'''
Ctrl-o           Jump back: go back in the jump list, like browser back
Ctrl-i           Jump forward in the jump list
Ctrl-d           Scroll half a page down
Ctrl-u           Scroll half a page up
Ctrl-f           Scroll a full page down
Ctrl-b           Scroll a full page up
Ctrl-e           Scroll down one line (cursor stays)
Ctrl-y           Scroll up one line (cursor stays)
Ctrl-]           Jump to the definition (ctags; LSP uses gd instead)
Ctrl-t           Jump back from a definition
Ctrl-^           Switch to the alternate (last) file
'''

CTRL_NORMAL = r'''
Ctrl-a           Add 1 to the number under the cursor: increment
Ctrl-x           Subtract 1 from the number under the cursor: decrement
Ctrl-r           Redo the undone change
'''

CTRL_INSERT = r'''
Ctrl-w           Delete the previous word (like Option+Delete)
Ctrl-u           Delete to the start of the line (like Cmd+Delete)
Ctrl-h           Delete the previous character (like Backspace)
Ctrl-t           Indent this line
Ctrl-d           Unindent this line
Ctrl-r "         Paste from a register (e.g., Ctrl-r 0 = last yank)
Ctrl-n           Complete the word: next match
Ctrl-p           Complete the word: previous match
Ctrl-o           Run one normal-mode command, then go back to insert
'''

CTRL_WINDOWS = r'''
Ctrl-w h/j/k/l   Change to the split on the left, below, above or right
Ctrl-w s          Split the window horizontally: horizontal split
Ctrl-w v          Split the window vertically: vertical split
Ctrl-w q          Close this split
Ctrl-w =          Make all splits the same size: equalize
Ctrl-w _          Make this split as tall as possible: maximize height
Ctrl-w |          Make this split as wide as possible: maximize width
Ctrl-w o          Close all other splits: keep only this one
Ctrl-w r          Swap the splits around: rotate
Ctrl-w T          Move this split to a new tab
'''

L_FIND = r'''
<Space><Space>   Find a file by name in the current working directory (a file picker)
<Space>ff        Find a file by name in the current working directory
<Space>fr        Open a recent file
<Space>fg        Find a git-tracked file in the current working directory
<Space>fb        Switch to an open buffer
<Space>,         Switch to an open buffer: quick switch (the buffer list)
'''

L_SEARCH = r'''
<Space>sf        Find a file by name in the current working directory (your primary find-file)
<Space>sF        Find a file by name in the current working directory (same as <Space>sf)
<Space>sg        Search text in all files: grep in the current working directory
<Space>sw        Search for the word or selection under the cursor: grep in the current working directory
<Space>sd        List the diagnostics
<Space>sR        Reopen the last picker: resume
<Space>sh        Search the help pages
<Space>sk        Search the keymaps
<Space>sC        Run a command by name: command list
<Space>sm        Show the marks
<Space>st        List the todo comments
<Space>sr        Replace text across files: search and replace panel (grug-far). Lowercase r = replace
'''

L_GIT = r'''
<Space>gg        Open LazyGit at the repository root
<Space>gG        Open LazyGit in the current working directory
<Space>gL        Show the git log for the current working directory
<Space>gb        Show the commit history for this line
<Space>gf        Show the commit history for this file
<Space>gl        Show the git log for the repository root
<Space>gB        Open this file on the remote: git browse
<Space>gY        Copy the remote URL of this file: git browse
<Space>gs        Show git status in a picker
<Space>gS        Show the git stashes
<Space>gi / gI   List GitHub issues: open / all
<Space>gp / gP   List GitHub pull requests: open / all
<Space>gd        Show the git diff, hunk by hunk (Snacks picker)
<Space>gD        Show the git diff against origin (Snacks picker)
<Space>gv        Open the working-tree diff (Diffview)
<Space>gV        Open the history of this file (Diffview)
'''

L_TROUBLE = r'''
<Space>xx        Show the diagnostics: Trouble
<Space>xX        Show the diagnostics of this buffer: Trouble
<Space>xt        Show the todo comments: Trouble
<Space>xT        Show only Todo, Fix and Fixme comments: Trouble
<Space>xL        Show the location list: Trouble
<Space>xQ        Show the quickfix list: Trouble
'''

L_BUFFERS = r'''
<Space>bp        Pin or unpin this buffer
<Space>bP        Close all buffers that are not pinned
<Space>bj        Go to a buffer by its label: pick
<Space>bl        Close the buffers to the left
<Space>br        Close the buffers to the right
<Space>bd        Close this buffer
<Space><Space>   Find a file by name: a file picker (the buffer list is <Space>,)
<Space>,         Switch to an open buffer
'''

L_CODE = r'''
<Space>cf        Format the file
<Space>cr        Rename a symbol (LSP)
<Space>ca        Fix or refactor the code: code action (LSP)
<Space>cd        Show the diagnostics for this line
<Space>cl        Show LSP info: which servers are attached
<Space>cs        Show the symbols outline: Aerial
<Space>cm        Install LSP servers and formatters: Mason
'''

L_HUNKS = r'''
<Space>ghs       Stage this hunk
<Space>ghr       Discard this hunk: reset hunk
<Space>ghp       Preview this hunk
<Space>ghb       Show blame for this line
<Space>ghS       Stage the whole buffer
<Space>ghR       Discard every change in the buffer: reset buffer
'''

L_TERMINAL = r'''
<Space>ft        Open or hide the floating terminal
<Space>tf        Open a floating terminal
<Space>tv        Open a terminal on the right: vertical split
<Space>th        Open a terminal at the bottom: horizontal split

<Space>t         Run tests with neotest: tt runs this file, tr the nearest test, ts opens the summary
'''

X_FILES = r'''
:w               Save
:q               Quit
:wq              Save and quit
:q!              Quit without saving
:qa!             Quit ALL windows without saving
:e file.py       Open a file
:saveas new.py   Save as new file
'''

X_BUFFERS = r'''
:ls              List open buffers
:b2              Switch to buffer 2
:bn / :bp        Next / previous buffer
:bd              Close buffer
:bufdo cmd       Run command across all buffers
'''

X_SPLITS = r'''
:split           Horizontal split
:vsplit          Vertical split
:only            Close all other splits
:close           Close current split
'''

X_USEFUL = r'''
:noh             Clear search highlighting
:set wrap        Toggle line wrapping
:set nowrap      Turn off wrapping
:set number      Show line numbers
:set relativenumber   Relative line numbers
:checkhealth     Run health checks
:Mason           Package manager (LSPs, formatters)
:Lazy            Plugin manager
:messages        See recent messages/errors
:registers       See all register contents
:marks           See all marks
'''

MODULE = {
    "n": 6,
    "folder": "m6-plugins-keymaps",
    "title": "Plugins and the key map",
    "footer": "Surround, Flash, Harpoon, Aerial and text objects; sessions and yank history; the g, bracket, z, Ctrl, Space and colon maps",
    "tagline": "Jump anywhere, select by structure and learn every prefix map.",
    "glossary": [],
    "coverage_allow": [
        ("]y / [y", "key order swapped to [y / ]y: in the live yanky config [y cycles forward to older yanks and ]y backward"),
        ("a) i) a] i] a} i} Brackets — searches forward on the line if not inside one", "row reworded to start with the task in plain words; the keys are unchanged"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Jump and select",
            "subtitle": "Surround, jump with labels, mark favourite files and select code by structure.",
            "idea": (
                "Move and select by meaning, not by counting characters.",
                [
                    ("Jump anywhere", "s", "Type a few letters, then press the label."),
                    ("Favourite file", "<Space>2", "Jump to the second Harpoon file."),
                    ("File outline", "<Space>cs", "See every class and function."),
                    ("Select a function", "vif", "Select its body only."),
                ],
                None,
            ),
            "problem": {
                "fail": "You mash `j` and `w` to cross a screen, and open the fuzzy finder for the same four files all day.",
                "fix": "Jump with Flash labels, pin files in Harpoon, and select whole functions with text objects.",
            },
            "drills": [
                {
                    "h2": "Surround (mini.surround)",
                    "intro": "In LazyVim mini.surround uses the `gs` prefix. Bare `sa`, `sd` and `sr` are not the surround keys here: `s` is Flash and `<Space>s*` are pickers.",
                    "blocks": [
                        K("Surround keys", SURROUND),
                        K("Examples", SURROUND_EX),
                        K("Surround a word, then undo it", [
                            ("gsaiw\"", "Surround the word with double quotes"),
                            ("u", "Undo the change: this is a motion drill, not a real edit"),
                        ], **{"try": "Open `data/log.txt` and put the cursor on `pattern` in 'this line matches a filter pattern'.",
                              "expect": "The line reads exactly as it did before."}),
                        {"type": "cmd", "where": "shell", "title": "Prove nothing changed", "code": "git diff data/log.txt",
                         "expect": "Nothing: the file has no diff, once autosave has written the undo (about 3 seconds)."},
                    ],
                },
                {
                    "h2": "Flash.nvim: instant cursor jumps",
                    "intro": "Flash replaces traditional motions: press a key, type characters, pick a label. Press `Esc` to cancel any Flash operation.",
                    "blocks": [
                        K("Basic jump", FLASH_JUMP),
                        K("Treesitter select", FLASH_TS),
                        K("Remote operations (operator-pending)", FLASH_REMOTE),
                        K("Enhanced search", FLASH_SEARCH),
                        K("Jump straight to a long function name", [
                            ("gg", "Go to the top of `orders.py`"),
                            ("s", "Jump to text: type `qu`, the first two letters of `qualifies_for_free_shipping`"),
                            ("label", "Jump to the match: press the label that appears on it"),
                        ], **{"try": "Press the keys in order.", "expect": "The cursor lands exactly on `def qualifies_for_free_shipping(order):`."}),
                    ],
                },
                {
                    "h2": "Harpoon: instant file switching",
                    "intro": "Mark your most-used files and jump between them with one keystroke. Close the menu with `q` or `Esc`.",
                    "blocks": [
                        K("Harpoon keys", HARPOON),
                        K("Mark the 4 files you keep bouncing between", [
                            ("<Space>H", "Add the file to the harpoon list: in each of `src/calculator.py`, `src/orders.py`, `src/report.py` and `tests/test_orders.py`"),
                            ("<Space>2", "Jump to harpoon file 2: from anywhere, straight to `orders.py`"),
                            ("<Space>h", "Open the harpoon menu"),
                        ], **{"try": "Open each file and press `<Space>H`, then use the other two keys.",
                              "expect": "The quick menu lists all 4 files, in the order you added them."}),
                    ],
                },
                {
                    "h2": "Aerial: code outline",
                    "intro": "A sidebar of all functions, classes and methods in the current file. Close it with `<Space>cs` or `q` inside the panel.",
                    "blocks": [
                        K("Aerial keys", AERIAL),
                        K("Inside the aerial panel", AERIAL_PANEL),
                        K("Get the shape of a file without reading it", [("<Space>cs", "Open the symbols outline in `orders.py`")],
                          **{"try": "Open `orders.py` and press `<Space>cs`.",
                             "expect": "2 classes (`Order`, `OrderBook`), 3 top-level functions (`calculate_total`, `qualifies_for_free_shipping`, `build_order_book`) and the `RAW_ORDERS` constant: 6 top-level symbols."}),
                    ],
                },
                {
                    "h2": "Treesitter text objects",
                    "intro": "Select, move between and operate on functions, classes and parameters as text objects.",
                    "blocks": [
                        K("Selection (visual or operator-pending)", TS_SELECT),
                        K("Movement", TS_MOVE),
                        K("Select without deleting", [
                            ("vif", "Select a function body: inside `qualifies_for_free_shipping`, then Esc"),
                            ("vaf", "Select a whole function with its signature, then Esc"),
                            ("vic", "Select a class body: inside `OrderBook`"),
                            ("vac", "Select a whole class"),
                            ("yif", "Copy a function body: back on `qualifies_for_free_shipping`, yank just the body"),
                            (":new", "Open a scratch buffer"),
                            ("p", "Paste the text and look"),
                            (":bd!", "Close the scratch buffer without saving"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "The pasted text starts with `items = order.items` and ends with `return total_qty >= 5`: body only, no `def` line."}),
                    ],
                },
                {
                    "h2": "Mini.ai: smarter text objects",
                    "intro": "Extends the `a` and `i` objects with treesitter awareness and new targets. Use after any operator (`d`, `c`, `y`, `v`).",
                    "blocks": [
                        K("Mini.ai objects", MINI_AI),
                        K("Change inside parens you are not even touching", [
                            ("ci)", "Change the text inside parens: on `return` in `Order.subtotal`, it finds the `sum(...)` parens ahead and enters insert mode inside them"),
                            ("Esc", "Leave insert mode, after typing anything first"),
                            ("u", "Undo the change at once: this is a motion drill"),
                        ], **{"try": "Put the cursor on `return` in `return sum(item[\"price\"] * item[\"qty\"] for item in self.items)`.",
                              "expect": "The line shows no change once you undo."}),
                        {"type": "cmd", "where": "shell", "title": "Prove nothing changed", "code": "git diff src/orders.py",
                         "expect": "No diff for that line, once autosave has written the undo (about 3 seconds)."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choosing a jump tool",
                "cards": [
                    ("Which tool?", "Match the tool to the job.", ["I want to", "Use"], [
                        ["Jump to any visible text", "`s` then characters"],
                        ["Return to a favourite file", "`<Space>H` to add, `<Space>1` to `<Space>9` to jump"],
                        ["See the shape of a file", "`<Space>cs`"],
                        ["Wrap or unwrap a word", "`gsa`, `gsd`, `gsr`"],
                    ]),
                    ("Text object families", "The same letters work after `v`, `d`, `c` and `y`.", ["Objects", "Meaning"], [
                        ["`af` / `if`", "Around / inside function"],
                        ["`ac` / `ic`", "Around / inside class"],
                        ["`aa` / `ia`", "Around / inside argument"],
                        ["`aq` / `iq`", "Around / inside any quote"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Copy a function body",
                "frame": "You want the body of `report` in a scratch buffer.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 12, in `report`", "`12G`"), "`yif`", "Yanks the body of the function."),
                    (None, "`:new` then `p`", "Pastes it into a scratch buffer, starting at `for code in codes:`."),
                    (None, "`:bd!`", "Discards the scratch buffer."),
                ],
                "after": "for code in codes:\n        print(code, calc_totl(PRICES[code], 2))",
                "meaning": "One text object replaced a drag-select with the mouse.",
            },
            "practice": {
                "h2": "Practice: jump and select",
                "qs": [
                    ("Mechanism", "Why are bare `sa`, `sd` and `sr` not surround keys here?",
                     "Who owns `s`?",
                     ["`s` is Flash.", "Surround moved to the `gs` prefix."],
                     "Surround uses `gsa`, `gsd` and `gsr`."),
                    ("Keystrokes", "Add the current file to Harpoon, then open its menu.",
                     "Capital adds, lowercase opens.",
                     ["Press `<Space>H`.", "Press `<Space>h`."],
                     "`<Space>H`, then `<Space>h`."),
                    ("Application", "Select a whole function including its signature.",
                     "Around, not inside.",
                     ["Put the cursor inside it.", "Press `vaf`."],
                     "`vaf`."),
                    ("Common mistake", "You used `vif` and the `def` line is missing. Why?",
                     "Inside versus around.",
                     ["`if` is inside: body only.", "`af` includes the signature."],
                     "Use `vaf` for the whole function."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Sessions, history and UI helpers",
            "subtitle": "Restore a workspace, recover a yank and learn the helpers that need no keymap.",
            "idea": (
                "Small helpers save the context you would otherwise rebuild by hand.",
                [
                    ("Restore session", "<Space>qs", "Same buffers and layout as before."),
                    ("Yank history", "<Space>p", "Pick any earlier yank."),
                    ("All todos", "<Space>st", "Search every TODO and FIXME."),
                    ("Find any key", "<Space>sk", "Fuzzy-search every keymap."),
                ],
                None,
            ),
            "problem": {
                "fail": "You quit Neovim and lose your layout, or overwrite a yank and cannot get it back.",
                "fix": "Restore the session with `<Space>qs` and cycle yank history with `[y` and `]y`.",
            },
            "drills": [
                {
                    "h2": "Bufferline: the tab bar",
                    "intro": "Open files show as tabs at the top, like a VS Code tab bar.",
                    "blocks": [
                        K("Bufferline keys", BUFFERLINE),
                        {"type": "text", "body": "Illuminate highlights every occurrence of the word under the cursor. It needs no keymap, so you see where a variable is used at a glance."},
                    ],
                },
                {
                    "h2": "Persistence: auto sessions",
                    "intro": "LazyVim auto-saves a session per project directory. Restore exactly where you left off.",
                    "blocks": [
                        K("Session keys", PERSISTENCE),
                        K("Quit entirely", [(":qa", "With a few files open in `nvim-drills`")]),
                        {"type": "cmd", "where": "shell", "title": "Reopen the project", "code": "v .",
                         "expect": "Neovim opens on `nvim-drills`. Press `<Space>qs`: the same buffers and split layout you had before `:qa` reappear."},
                    ],
                },
                {
                    "h2": "Yanky: yank history",
                    "intro": "Every yank and delete goes into a ring you can cycle through when pasting.",
                    "blocks": [
                        K("Yank history keys", YANKY),
                        K("Recover an earlier yank", [
                            ("yy", "Copy a line: in the `RAW_ORDERS` list, yank the \"A1\" line"),
                            ("yy", "Copy the next line: move down and yank the \"A2\" line"),
                            (":new", "Open a scratch buffer"),
                            ("p", "Paste the most recent yank: the A2 line"),
                            ("[y", "Swap the pasted text for the A1 line, without re-yanking"),
                        ], **{"try": "Work in `orders.py`'s `RAW_ORDERS` list and press the keys in order.",
                              "expect": "The scratch buffer now shows the \"A1\" line, not \"A2\". Close it without saving with `:bd!`."}),
                    ],
                },
                {
                    "h2": "Todo comments",
                    "intro": "Highlights `TODO`, `FIX`, `FIXME`, `HACK`, `NOTE` and `WARN`, and lets you jump to or search them.",
                    "blocks": [
                        K("Todo keys", TODO),
                        K("Sweep for what is left", [("<Space>st", "Search all TODO comments project-wide")],
                          **{"try": "Run it after the rename, import cleanup and debugger fix.",
                             "expect": "Exactly 5 results: the `average()` TODO in `calculator.py`, the 2 TODOs in `data/log.txt`, and 2 duplicates in `scripts/dirty.patch`. A 6th means an earlier exercise was not cleaned up."}),
                    ],
                },
                {
                    "h2": "Database UI, Markdown and the modern UI",
                    "intro": "Query databases, render Markdown and use floating messages. Most need no keymap.",
                    "blocks": [
                        K("Database UI (vim-dadbod)", DADBOD),
                        {"type": "text", "body": "Inside DBUI, `Enter` expands a connection or table. Write SQL in a buffer and run it with `<Space>S` (or `:DB`). SQL buffers get autocompletion from `vim-dadbod-completion`."},
                        K("Render-markdown", RENDER_MD),
                        {"type": "text", "body": "Render-markdown draws headings, code-block backgrounds, bullets and checkboxes inline on `.md` files. No keymap needed."},
                        K("Browser preview", MD_PREVIEW),
                        {"type": "text", "body": "Press `<Space>cp` again, or close the browser tab, to stop the preview."},
                        {"type": "text", "body": "Noice and the snacks notifier give you a floating command line and search input, and notifications (LSP progress, messages) in the top-right. `<Space>sn` opens the Noice message group, `<Space>snh` shows history and `<Space>snd` dismisses all."},
                        {"type": "text", "body": "Lualine is the bottom statusline: mode, git branch, diff, diagnostics, file info and position. Always visible, no keymaps."},
                        {"type": "text", "body": "If icons look wrong, set the iTerm2 font to JetBrainsMono Nerd Font Mono (Settings, Profiles, Text, Font)."},
                    ],
                },
                {
                    "h2": "Vim-tmux navigator and which-key",
                    "intro": "One set of keys moves across Neovim splits and tmux panes. Which-key shows every continuation of a prefix.",
                    "blocks": [
                        K("Move across nvim and tmux", NAVIGATOR),
                        {"type": "text", "body": "In a tmux pane that is not running Neovim, the same four keys switch tmux panes."},
                        K("Keymap discovery", WHICH_KEY, **{"try": "Press `<Space>` and wait.",
                                                            "expect": "A popup lists every leader group. Press `g` or `z` and wait to see theirs."}),
                        {"type": "cmd", "where": "nvim", "title": "Find any key by description", "code": "<Space>sk",
                         "expect": "A picker lists all keymaps; type part of a description to filter."},
                    ],
                },
            ],
            "rules": {
                "h2": "Helpers at a glance",
                "cards": [
                    ("Context savers", "Keys that bring your work back.", ["Keys", "Does"], [
                        ["`<Space>qs`", "Restore this directory's session"],
                        ["`<Space>ql`", "Restore the last session"],
                        ["`[y` / `]y`", "Swap the pasted text for an older / newer yank"],
                        ["`<Space>p`", "Paste an earlier yank: yank history picker"],
                    ]),
                    ("No keymap needed", "These work on their own.", ["Plugin", "What you see"], [
                        ["Illuminate", "Other uses of the word under the cursor"],
                        ["Render-markdown", "Rendered headings and checkboxes in `.md` files"],
                        ["Lualine", "Statusline with mode, branch and diagnostics"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Never lose a yank",
                "frame": "You copy one line, then another, and need the first back.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 2", "`2G`"), "`yy`, `j`, then `yy`", "Yanks `ORDERS`, then `PRICES`."),
                    (None, "`:new` then `p`", "The `PRICES` line appears, below the empty first line."),
                    (None, "`[y`", "The pasted text swaps to the `ORDERS` line."),
                    (None, "`:bd!`", "Closes the scratch buffer."),
                ],
                "after": "\nORDERS = [\"A1\", \"A2\", \"A3\"]",
                "meaning": "The yank ring remembers everything, so an overwrite never costs you the earlier copy.",
            },
            "practice": {
                "h2": "Practice: sessions and history",
                "qs": [
                    ("Mechanism", "What does persistence save, and per what?",
                     "Think of your project folder.",
                     ["It auto-saves a session per project directory."],
                     "One session per directory."),
                    ("Keystrokes", "Swap a pasted line for the previous yank.",
                     "Square bracket, then y.",
                     ["Press `[y`."],
                     "`[y`."),
                    ("Application", "You forgot a key's name. How do you find it?",
                     "Search the keymaps.",
                     ["Press `<Space>sk`.", "Type part of the description."],
                     "`<Space>sk`."),
                    ("Common mistake", "You expect a mapping for Lualine. Is there one?",
                     "Look at the plugin notes.",
                     ["Lualine is always visible.", "It has no keymaps."],
                     "No. It needs none."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "The g, [ ], and z maps",
            "subtitle": "Three prefixes cover navigation, case, comments, brackets, scrolling and folds.",
            "idea": (
                "A prefix is a family. Press it, wait, and which-key lists the rest.",
                [
                    ("Comment", "gcc", "Toggle comment on the line."),
                    ("Next problem", "]d", "Jump to the next diagnostic."),
                    ("Center line", "zz", "Scroll the cursor line to the middle."),
                    ("Fold toggle", "za", "Open or close the fold under the cursor."),
                ],
                None,
            ),
            "problem": {
                "fail": "You scroll with the mouse, comment lines by hand and never find the jump you half remember.",
                "fix": "Learn three prefixes: `g` for actions, `[` and `]` for next and previous, `z` for view and folds.",
            },
            "drills": [
                {
                    "h2": "The g prefix: navigation",
                    "intro": "All triggered with `g` followed by another key. Which-key shows them when you press `g`.",
                    "blocks": [
                        K("Navigation", G_NAV),
                        K("Search (after g in operator-pending or visual)", G_SEARCH),
                        {"type": "cmd", "where": "nvim", "title": "Change a match, then repeat", "code": "/pattern\ncgn\n.",
                         "expect": "`cgn` changes the match and `.` repeats it on the next match. Lesson 7 drills this in depth."},
                    ],
                },
                {
                    "h2": "Case and comments",
                    "intro": "Operators that take a motion.",
                    "blocks": [
                        K("Case", G_CASE),
                        {"type": "cmd", "where": "nvim", "title": "Change the case of a word", "code": "guiw\ngUiw\ng~iw",
                         "expect": "The word under the cursor is lowercased, uppercased, then toggled."},
                        K("Comments", G_COMMENTS),
                        {"type": "cmd", "where": "nvim", "title": "Comment a paragraph", "code": "gcip",
                         "expect": "The paragraph under the cursor is commented. In visual mode, select lines and press `gc`."},
                    ],
                },
                {
                    "h2": "LSP, formatting, tabs and marks",
                    "intro": "LazyVim's primary LSP jumps are set when a server attaches.",
                    "blocks": [
                        K("LSP (the g keys)", G_LSP),
                        {"type": "text", "body": "Neovim 0.11 natives also work as a fallback: `grn` rename, `gra` code action, `grr` references, `gri` implementation, `grt` type definition, `grx` codelens."},
                        K("Formatting", G_FORMAT),
                        K("Tabs (not buffers)", G_TABS),
                        K("Marks", G_MARKS),
                        K("Misc", G_MISC),
                    ],
                },
                {
                    "h2": "Brackets: next and previous",
                    "intro": "Navigate between diagnostics, hunks, functions and more.",
                    "blocks": [K("Bracket commands", BRACKETS)],
                },
                {
                    "h2": "The z prefix: scroll, folds and spelling",
                    "intro": "Scroll and fold control.",
                    "blocks": [
                        K("Scrolling (reposition the screen, cursor stays)", Z_SCROLL),
                        K("Folding", Z_FOLD, **{"try": "`nvim ~/tw/orders.py`, then `10G` (the `def report` line) and `zc`. Then `zM`, then `zR`.",
                          "expect": "`zc` hides lines 11–12 behind `def report(codes):`. `zM` leaves only signatures and top-level lines. `zR` opens everything."}),
                        {"type": "text", "body": "Folds here come from treesitter, so every function and block folds on its own. To fold lines you pick, run `:setlocal foldmethod=manual`, select with `V`, press `zf`; `zd` removes it. Without that, `zf` stops with `E350`."},
                        K("Spelling", Z_SPELL),
                    ],
                },
            ],
            "rules": {
                "h2": "Prefix families",
                "cards": [
                    ("Three prefixes", "Press one and wait for which-key.", ["Prefix", "Family"], [
                        ["`g`", "Actions: go, case, comment, format"],
                        ["`[` and `]`", "Previous and next of something"],
                        ["`z`", "View: scroll, folds, spelling"],
                    ]),
                    ("Fold ladder", "Lowercase acts once, capital acts recursively.", ["Open", "Close"], [
                        ["`zo` open fold", "`zc` close fold"],
                        ["`zO` open recursively", "`zC` close recursively"],
                        ["`zR` open all", "`zM` close all"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Review a file in five keys",
                "frame": "You open an unfamiliar file and want a quick pass.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (None, "`zM`", "Every fold closes, leaving the outline below."),
                    (None, "`zj` then `za`", "Moves to the next fold, `calc_totl`, and opens it."),
                    (None, "`]d`", "Jumps to the next diagnostic, if the file has one."),
                    (None, "`zz` then `zR`", "Centers the line, then opens all folds."),
                ],
                "after": "PRICES = {\"A1\": 2.50, \"A2\": 4.00, \"A3\": 1.25}\n\n\n+--  2 lines: def calc_totl(price, qty):\n\n\n+--  3 lines: def report(codes):\n\n\nname = \"pen\"",
                "meaning": "You read the structure first and the details second.",
            },
            "practice": {
                "h2": "Practice: g, brackets and z",
                "qs": [
                    ("Mechanism", "What is the difference between `gu` and `gU`?",
                     "Case of the letter.",
                     ["Lowercase `gu` lowercases.", "Capital `gU` uppercases."],
                     "`gu` lowercases and `gU` uppercases the motion."),
                    ("Keystrokes", "Toggle a comment on the current line.",
                     "Double the last letter.",
                     ["Press `gcc`."],
                     "`gcc`."),
                    ("Application", "Step to the next git hunk.",
                     "Bracket plus the hunk letter.",
                     ["Press `]h`."],
                     "`]h`."),
                    ("Common mistake", "You pressed `zH` expecting a fold. What does it do?",
                     "Fold keys are lowercase or `zM`/`zR`.",
                     ["`zH` scrolls half a screen to the left."],
                     "It scrolls left. Folds use `za`, `zo`, `zc`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Ctrl, Space and colon maps",
            "subtitle": "Window management, insert-mode shortcuts, every leader group and the useful ex commands.",
            "idea": (
                "Three more families: Ctrl keys, the Space leader and the colon command line.",
                [
                    ("Vertical split", "Ctrl-w v", "Two windows side by side."),
                    ("Insert one command", "Ctrl-o", "Run one normal command, then return to insert."),
                    ("Leader menu", "<Space>", "Wait to see every group."),
                    ("Ex command", ":", "Save, split and manage buffers."),
                ],
                None,
            ),
            "problem": {
                "fail": "You leave insert mode just to delete one line, and split windows with the mouse.",
                "fix": "Use `Ctrl-o` for one normal command in insert mode, and `Ctrl-w` plus a letter for windows.",
            },
            "drills": [
                {
                    "h2": "The Ctrl commands",
                    "intro": "Navigation, editing and windows.",
                    "blocks": [
                        K("Navigation", CTRL_NAV),
                        K("Editing (normal mode)", CTRL_NORMAL),
                        K("Editing (insert mode)", CTRL_INSERT),
                        {"type": "cmd", "where": "nvim", "title": "Delete a line without leaving insert mode", "code": "Ctrl-o dd",
                         "expect": "The line is deleted and you are still in insert mode. `Ctrl-o` in insert mode is huge."},
                        K("Window management", CTRL_WINDOWS, **{"try": "Press `Ctrl-w v`, then `Ctrl-w l`, then `Ctrl-w q`.",
                                                                "expect": "The window splits side by side, the cursor moves to the right split, and that split closes."}),
                    ],
                },
                {
                    "h2": "The Space leader: find and search",
                    "intro": "Press `<Space>` and wait for which-key. The main groups follow.",
                    "blocks": [
                        K("Find (<Space>f) and the quick-finders", L_FIND),
                        {"type": "text", "body": "In the current config the find keys (`<Space><Space>`, `<Space>ff`, `<Space>sf`) and the grep keys (`<Space>/`, `<Space>sg`, `<Space>sw`) search `:pwd`, not the project root. The arrow keys are disabled in normal, visual and insert mode."},
                        K("Search (<Space>s)", L_SEARCH),
                    ],
                },
                {
                    "h2": "The Space leader: git, diagnostics and buffers",
                    "intro": "Git, Trouble and buffer groups.",
                    "blocks": [
                        K("Git (<Space>g)", L_GIT),
                        {"type": "text", "body": "Direct Diffview commands are also available: `:DiffviewOpen` and `:DiffviewFileHistory %`."},
                        K("Diagnostics and Trouble (<Space>x)", L_TROUBLE),
                        K("Buffers (<Space>b)", L_BUFFERS),
                    ],
                },
                {
                    "h2": "The Space leader: code, hunks, terminals and tests",
                    "intro": "Code actions, hunk staging, terminals and the test prefix.",
                    "blocks": [
                        K("Code (<Space>c)", L_CODE),
                        K("Hunks and git signs (<Space>gh)", L_HUNKS),
                        K("Terminals and tests (<Space>f and <Space>t)", L_TERMINAL),
                        {"type": "text", "body": "`<Space>t` holds both: the test keys (neotest) and the terminals `<Space>tf`, `<Space>tv` and `<Space>th`. `<Space>ft` is the floating terminal, and `Ctrl-\\` and `Ctrl-/` toggle the last terminal you used. Every terminal opens in `:pwd`. The inlay-hints toggle lives under `<Space>u`: verify the subkey in which-key."},
                    ],
                },
                {
                    "h2": "The colon command mode",
                    "intro": "Useful commands you type after pressing `:`.",
                    "blocks": [
                        K("Files", X_FILES),
                        K("Buffers", X_BUFFERS),
                        K("Windows and splits", X_SPLITS),
                        {"type": "cmd", "where": "nvim", "title": "Split, then close the split", "code": ":vsplit\n:close",
                         "expect": "The window splits vertically, then the current split closes."},
                        K("Useful", X_USEFUL),
                    ],
                },
            ],
            "rules": {
                "h2": "Map families at a glance",
                "cards": [
                    ("Window keys", "Ctrl-w, then one letter.", ["Keys", "Does"], [
                        ["`Ctrl-w v`", "Split the window vertically"],
                        ["`Ctrl-w s`", "Split the window horizontally"],
                        ["`Ctrl-w h/j/k/l`", "Change to another split"],
                        ["`Ctrl-w q`", "Close this split"],
                        ["`Ctrl-w o`", "Close all other splits"],
                    ]),
                    ("Leader groups", "Each letter after Space opens one group.", ["Group", "Holds"], [
                        ["`<Space>f`", "Find files, buffers, recent"],
                        ["`<Space>s`", "Search and pickers"],
                        ["`<Space>g`", "Git"],
                        ["`<Space>c`", "Code actions"],
                        ["`<Space>t`", "Tests and terminals"],
                        ["`<Space>x`", "Trouble lists"],
                    ]),
                    ("Quit variants", "Pick the right exit.", ["Command", "Does"], [
                        ["`:q`", "Quit"],
                        ["`:wq`", "Save and quit"],
                        ["`:q!`", "Quit without saving"],
                        ["`:qa!`", "Quit all windows without saving"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Fix a line without leaving insert mode",
                "frame": "You are typing at the end of the list and notice the last line is stale.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 16, end of line", "`G` `A`"), "`Ctrl-o` then `dd`", "Deletes `TODO reply to Sam`. You stay in insert mode."),
                    (None, "type ` x2`", "The text lands at the end of `buy boxes`."),
                    (None, "`Esc`, then `Ctrl-w v`", "Opens a vertical split for reference."),
                    (None, "`Ctrl-w q`", "Closes it."),
                ],
                "before": "buy boxes\nTODO reply to Sam",
                "after": "buy boxes x2",
                "meaning": "Your typing flow never broke.",
            },
            "practice": {
                "h2": "Practice: Ctrl, Space and colon",
                "qs": [
                    ("Mechanism", "What does `Ctrl-o` do in insert mode?",
                     "One command only.",
                     ["It runs ONE normal-mode command.", "Then you are back in insert mode."],
                     "One normal command, then back to insert."),
                    ("Keystrokes", "Open a vertical split and close it again.",
                     "Ctrl-w plus a letter each time.",
                     ["Press `Ctrl-w v`.", "Press `Ctrl-w q`."],
                     "`Ctrl-w v`, then `Ctrl-w q`."),
                    ("Application", "Show relative line numbers.",
                     "A `:set` option.",
                     ["Run `:set relativenumber`."],
                     "`:set relativenumber`."),
                    ("Common mistake", "You typed `:q!` and lost edits. What should you have used?",
                     "Save first.",
                     ["`:q!` quits without saving.", "`:wq` saves, then quits."],
                     "`:wq`."),
                ],
            },
        },
    ],
}
