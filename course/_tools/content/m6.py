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
:w               Save the file
:q               Quit the window
:wq              Save and quit
:q!              Quit without saving
:qa!             Quit ALL windows without saving
:e file.py       Open a file
:saveas new.py   Save as a new file
'''

X_BUFFERS = r'''
:ls              List open buffers
:b2              Switch to buffer 2
:bn / :bp        Go to the next / previous buffer
:bd              Close the buffer
:bufdo cmd       Run a command on all buffers
'''

X_SPLITS = r'''
:split           Split the window horizontally
:vsplit          Split the window vertically
:only            Close all other splits
:close           Close the current split
'''

X_USEFUL = r'''
:noh             Clear search highlighting
:set wrap        Toggle line wrapping
:set nowrap      Turn off wrapping
:set number      Show line numbers
:set relativenumber   Show relative line numbers
:checkhealth     Run health checks
:Mason           Open the package manager (LSPs, formatters)
:Lazy            Open the plugin manager
:messages        See recent messages and errors
:registers       See all register contents
:marks           See all marks
'''

MODULE = {
    "n": 6,
    "folder": "m6-plugins-keymaps",
    "title": "Use Neovim plugins and find any key",
    "footer": "Jump with labels, select code, restore sessions, paste old yanks, and look up g, bracket, z, Ctrl, Space and colon keys",
    "tagline": "Jump anywhere, select code by structure, restore sessions and find any key.",
    "glossary": [],
    "coverage_allow": [
        ("]y / [y", "key order swapped to [y / ]y: in the live yanky config [y cycles forward to older yanks and ]y backward"),
        ("a) i) a] i] a} i} Brackets — searches forward on the line if not inside one", "row reworded to start with the task in plain words; the keys are unchanged"),
    ],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Jump around a file, switch files and select code fast",
            "subtitle": "Put quotes around a word, jump to any text with labels, switch between favourite files, see every function in a file, select a whole function",
            "idea": (
                "Jump to text and select code by meaning, not by counting characters.",
                [
                    ("Jump to any text on screen", "s", "Type a few letters, then press the label."),
                    ("Jump to a favourite file", "<Space>2", "Jump to the second Harpoon file."),
                    ("See every class and function in a file", "<Space>cs", "Open the symbols outline."),
                    ("Select a function body", "vif", "Select its body only."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I cross the screen without pressing `j` and `w` again and again, and reach the same four files without opening the fuzzy finder all day?",
                "fix": "Jump to any text with Flash labels, pin files in Harpoon, and select whole functions with text objects.",
            },
            "drills": [
                {
                    "h2": "Put quotes or brackets around a word (surround)",
                    "intro": "Add, remove or change quotes and brackets with the `gs` prefix: in LazyVim mini.surround uses `gs`. Bare `sa`, `sd` and `sr` are not the surround keys here: `s` is Flash and `<Space>s*` are pickers.",
                    "blocks": [
                        K("Add, remove or change quotes and brackets around text", SURROUND),
                        K("Surround a word or 3 words, then remove or change the brackets", SURROUND_EX),
                        K("Put quotes around a word, then undo it", [
                            ("gsaiw\"", "Surround the word with double quotes"),
                            ("u", "Undo the change: this is a motion drill, not a real edit"),
                        ], **{"try": "Open `data/log.txt` and put the cursor on `pattern` in 'this line matches a filter pattern'.",
                              "expect": "The line reads exactly as it did before."}),
                        {"type": "cmd", "where": "shell", "title": "Check that the file did not change", "code": "git diff data/log.txt",
                         "expect": "Nothing: the file has no diff, once autosave has written the undo (about 3 seconds)."},
                    ],
                },
                {
                    "h2": "Jump to any text on screen with a few letters (Flash)",
                    "intro": "Jump instead of pressing motions again and again: press a key, type characters, pick a label. Press `Esc` to cancel any Flash operation.",
                    "blocks": [
                        K("Jump to any visible text", FLASH_JUMP),
                        K("Select a function, block or class with labels (treesitter)", FLASH_TS),
                        K("Copy, delete or change text far away without moving the cursor", FLASH_REMOTE),
                        K("Search for text or a character and jump with labels", FLASH_SEARCH),
                        K("Jump to a long function name by its first letters", [
                            ("gg", "Go to the top of `orders.py`"),
                            ("s", "Jump to text: type `qu`, the first two letters of `qualifies_for_free_shipping`"),
                            ("label", "Jump to the match: press the label that appears on it"),
                        ], **{"try": "Press the keys in order.", "expect": "The cursor lands exactly on `def qualifies_for_free_shipping(order):`."}),
                    ],
                },
                {
                    "h2": "Switch between your favourite files with one key (Harpoon)",
                    "intro": "Mark your most-used files and jump between them with one keystroke. Close the menu with `q` or `Esc`.",
                    "blocks": [
                        K("Mark a file, open the list and jump to file 1 to 9", HARPOON),
                        K("Mark the 4 files you switch between all day", [
                            ("<Space>H", "Add the file to the harpoon list: in each of `src/calculator.py`, `src/orders.py`, `src/report.py` and `tests/test_orders.py`"),
                            ("<Space>2", "Jump to harpoon file 2: from anywhere, straight to `orders.py`"),
                            ("<Space>h", "Open the harpoon menu"),
                        ], **{"try": "Open each file and press `<Space>H`, then use the other two keys.",
                              "expect": "The quick menu lists all 4 files, in the order you added them."}),
                    ],
                },
                {
                    "h2": "See every function and class in a file (outline)",
                    "intro": "See all functions, classes and methods in the current file in a sidebar (Aerial). Close it with `<Space>cs` or `q` inside the panel.",
                    "blocks": [
                        K("Open the outline and jump between functions and classes", AERIAL),
                        K("Move around inside the outline panel", AERIAL_PANEL),
                        K("See the structure of a file without reading it", [("<Space>cs", "Open the symbols outline in `orders.py`")],
                          **{"try": "Open `orders.py` and press `<Space>cs`.",
                             "expect": "2 classes (`Order`, `OrderBook`), 3 top-level functions (`calculate_total`, `qualifies_for_free_shipping`, `build_order_book`) and the `RAW_ORDERS` constant: 6 top-level symbols."}),
                    ],
                },
                {
                    "h2": "Select, copy or delete a whole function or class (text objects)",
                    "intro": "Select, jump between and operate on functions, classes and parameters as text objects (treesitter).",
                    "blocks": [
                        K("Select, delete or copy a function, class or argument", TS_SELECT),
                        K("Jump to the next or previous function or class", TS_MOVE),
                        K("Select a function body or a whole class without deleting it", [
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
                    "h2": "Change text inside brackets or quotes ahead of the cursor (mini.ai)",
                    "intro": "Use more text objects after any operator (`d`, `c`, `y`, `v`): mini.ai extends the `a` and `i` objects with treesitter awareness and new targets.",
                    "blocks": [
                        K("Target a function, class, block, brackets, quotes or the next match", MINI_AI),
                        K("Change the text inside parens that are ahead of the cursor", [
                            ("ci)", "Change the text inside parens: on `return` in `Order.subtotal`, it finds the `sum(...)` parens ahead and enters insert mode inside them"),
                            ("Esc", "Leave insert mode, after typing anything first"),
                            ("u", "Undo the change at once: this is a motion drill"),
                        ], **{"try": "Put the cursor on `return` in `return sum(item[\"price\"] * item[\"qty\"] for item in self.items)`.",
                              "expect": "The line shows no change once you undo."}),
                        {"type": "cmd", "where": "shell", "title": "Check that the line did not change", "code": "git diff src/orders.py",
                         "expect": "No diff for that line, once autosave has written the undo (about 3 seconds)."},
                    ],
                },
            ],
            "rules": {
                "h2": "Pick the right way to jump, switch files or select code",
                "cards": [
                    ("Which key jumps, switches files or shows an outline?", "Find your job in the left column, then use the key on the right.", ["I want to", "Use"], [
                        ["Jump to any visible text", "`s` then characters"],
                        ["Go back to a favourite file", "`<Space>H` to add, `<Space>1` to `<Space>9` to jump"],
                        ["See every function and class in a file", "`<Space>cs`"],
                        ["Put quotes or brackets around a word, or remove them", "`gsa`, `gsd`, `gsr`"],
                    ]),
                    ("Select or change a function, class, argument or quote", "The same letters work after `v`, `d`, `c` and `y`.", ["Objects", "Meaning"], [
                        ["`af` / `if`", "Around / inside a function"],
                        ["`ac` / `ic`", "Around / inside a class"],
                        ["`aa` / `ia`", "Around / inside an argument"],
                        ["`aq` / `iq`", "Around / inside any quote"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Copy only the body of a function into a scratch buffer",
                "frame": "Copy the body of `report` into a scratch buffer.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 12, in `report`", "`12G`"), "`yif`", "Copy the body of the function."),
                    (None, "`:new` then `p`", "Paste it into a scratch buffer: it starts at `for code in codes:`."),
                    (None, "`:bd!`", "Discard the scratch buffer."),
                ],
                "after": "for code in codes:\n        print(code, calc_totl(PRICES[code], 2))",
                "meaning": "Copy a function body with one text object instead of a drag-select with the mouse.",
            },
            "practice": {
                "h2": "Check how to jump, switch files and select code",
                "qs": [
                    ("Mechanism", "Why don't bare `sa`, `sd` and `sr` surround a word here?",
                     "Check which plugin uses `s`.",
                     ["`s` belongs to Flash.", "Surround moved to the `gs` prefix."],
                     "Use `gsa`, `gsd` and `gsr` to surround."),
                    ("Keystrokes", "How do I add this file to Harpoon and open the list?",
                     "Capital adds, lowercase opens.",
                     ["Press `<Space>H`.", "Press `<Space>h`."],
                     "`<Space>H`, then `<Space>h`."),
                    ("Application", "How do I select a whole function with its signature?",
                     "Around, not inside.",
                     ["Put the cursor inside it.", "Press `vaf`."],
                     "`vaf`."),
                    ("Common mistake", "Why is the `def` line missing after I select with `vif`?",
                     "Inside versus around.",
                     ["`if` is inside: body only.", "`af` includes the signature."],
                     "Use `vaf` to select the whole function."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Restore your session, paste an old yank and find any key",
            "subtitle": "Reopen the files and layout from last time, paste something you copied earlier, search every TODO, find a key by what it does",
            "idea": (
                "Get back your layout, your old yanks and your todos without rebuilding them by hand.",
                [
                    ("Get back the files and layout from last time", "<Space>qs", "Same buffers and layout as before."),
                    ("Paste something you copied earlier", "<Space>p", "Pick any earlier yank."),
                    ("List every todo comment", "<Space>st", "Search every TODO and FIXME."),
                    ("Find a key by what it does", "<Space>sk", "Fuzzy-search every keymap."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I get my layout back after I quit Neovim, or recover a yank I overwrote?",
                "fix": "Restore the session with `<Space>qs` and cycle yank history with `[y` and `]y`.",
            },
            "drills": [
                {
                    "h2": "See and switch open files in the tab bar (bufferline)",
                    "intro": "Open files show as tabs at the top, like a VS Code tab bar.",
                    "blocks": [
                        K("Switch, pin and close open files (buffers)", BUFFERLINE),
                        {"type": "text", "body": "See where a word is used: Illuminate highlights every occurrence of the word under the cursor. It needs no keymap, so you see where a variable is used at a glance."},
                    ],
                },
                {
                    "h2": "Get back your files and layout after you quit (sessions)",
                    "intro": "LazyVim auto-saves a session per project directory. Restore exactly where you left off.",
                    "blocks": [
                        K("Restore, pick or stop saving a session", PERSISTENCE),
                        K("Quit Neovim completely", [(":qa", "With a few files open in `nvim-drills`")]),
                        {"type": "cmd", "where": "shell", "title": "Reopen the project and restore the session", "code": "v .",
                         "expect": "Neovim opens on `nvim-drills`. Press `<Space>qs`: the same buffers and split layout you had before `:qa` reappear."},
                    ],
                },
                {
                    "h2": "Paste something you copied earlier (yank history)",
                    "intro": "Every yank and delete goes into a ring you can cycle through when pasting.",
                    "blocks": [
                        K("Paste an earlier yank or cycle through the history", YANKY),
                        K("Get back a line you copied before the last one", [
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
                    "h2": "Find every TODO and FIXME comment in the project",
                    "intro": "Highlight `TODO`, `FIX`, `FIXME`, `HACK`, `NOTE` and `WARN`, then jump to or search them.",
                    "blocks": [
                        K("Jump to, search or list todo comments", TODO),
                        K("Search every TODO that is left", [("<Space>st", "Search all TODO comments project-wide")],
                          **{"try": "Run it after the rename, import cleanup and debugger fix.",
                             "expect": "Exactly 5 results: the `average()` TODO in `calculator.py`, the 2 TODOs in `data/log.txt`, and 2 duplicates in `scripts/dirty.patch`. A 6th means an earlier exercise was not cleaned up."}),
                    ],
                },
                {
                    "h2": "Query a database, preview Markdown and read messages and the status line",
                    "intro": "Query databases, render Markdown and read floating messages. Most need no keymap.",
                    "blocks": [
                        K("Open the database UI to query a database (vim-dadbod)", DADBOD),
                        {"type": "text", "body": "Run SQL in the database UI: inside DBUI, `Enter` expands a connection or table. Write SQL in a buffer and run it with `<Space>S` (or `:DB`). SQL buffers get autocompletion from `vim-dadbod-completion`."},
                        K("Turn on Markdown rendering inside the file (render-markdown)", RENDER_MD),
                        {"type": "text", "body": "See Markdown rendered in the file: render-markdown draws headings, code-block backgrounds, bullets and checkboxes inline on `.md` files. No keymap needed."},
                        K("Preview a Markdown file in the browser", MD_PREVIEW),
                        {"type": "text", "body": "Stop the preview: press `<Space>cp` again, or close the browser tab."},
                        {"type": "text", "body": "See messages and the command line in a floating window: Noice and the snacks notifier give you a floating command line and search input, and notifications (LSP progress, messages) in the top-right. `<Space>sn` opens the Noice message group, `<Space>snh` shows history and `<Space>snd` dismisses all."},
                        {"type": "text", "body": "See mode, git branch and position in the status line: Lualine is the bottom statusline: mode, git branch, diff, diagnostics, file info and position. Always visible, no keymaps."},
                        {"type": "text", "body": "Fix icons that look wrong: set the iTerm2 font to JetBrainsMono Nerd Font Mono (Settings, Profiles, Text, Font)."},
                    ],
                },
                {
                    "h2": "Move between nvim splits and tmux panes, and find any key (which-key)",
                    "intro": "Move across Neovim splits and tmux panes with one set of keys. Which-key shows every continuation of a prefix.",
                    "blocks": [
                        K("Move to the split or pane on the left, below, above or right", NAVIGATOR),
                        {"type": "text", "body": "Switch tmux panes with the same four keys when the pane is not running Neovim."},
                        K("See every key that follows a prefix", WHICH_KEY, **{"try": "Press `<Space>` and wait.",
                                                                              "expect": "A popup lists every leader group. Press `g` or `z` and wait to see theirs."}),
                        {"type": "cmd", "where": "nvim", "title": "Find a key by what it does", "code": "<Space>sk",
                         "expect": "A picker lists all keymaps; type part of a description to filter."},
                    ],
                },
            ],
            "rules": {
                "h2": "Get your work back after quitting or overwriting, and know which helpers need no key",
                "cards": [
                    ("Get your work back after quitting or overwriting", "Press these keys to bring your work back.", ["Keys", "Does"], [
                        ["`<Space>qs`", "Restore this directory's session"],
                        ["`<Space>ql`", "Restore the last session"],
                        ["`[y` / `]y`", "Swap the pasted text for an older / newer yank"],
                        ["`<Space>p`", "Paste an earlier yank: yank history picker"],
                    ]),
                    ("Helpers that work without any key", "These work on their own.", ["Plugin", "What you see"], [
                        ["Illuminate", "Other uses of the word under the cursor"],
                        ["Render-markdown", "Rendered headings and checkboxes in `.md` files"],
                        ["Lualine", "Statusline with mode, branch and diagnostics"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Get back a line you copied before the last one",
                "frame": "Copy one line, then another, and get the first one back.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 2", "`2G`"), "`yy`, `j`, then `yy`", "Copy `ORDERS`, then `PRICES`."),
                    (None, "`:new` then `p`", "The `PRICES` line appears, below the empty first line."),
                    (None, "`[y`", "The pasted text swaps to the `ORDERS` line."),
                    (None, "`:bd!`", "Close the scratch buffer."),
                ],
                "after": "\nORDERS = [\"A1\", \"A2\", \"A3\"]",
                "meaning": "Recover an overwritten yank: the yank ring remembers everything, so an overwrite never costs you the earlier copy.",
            },
            "practice": {
                "h2": "Check how to restore sessions and find yanks and keys",
                "qs": [
                    ("Mechanism", "What does the persistence plugin save, and for which folder?",
                     "Think of your project folder.",
                     ["It auto-saves a session per project directory."],
                     "One session per directory."),
                    ("Keystrokes", "How do I swap a pasted line for the previous yank?",
                     "Square bracket, then y.",
                     ["Press `[y`."],
                     "`[y`."),
                    ("Application", "How do I find a key when I forgot its name?",
                     "Search the keymaps.",
                     ["Press `<Space>sk`.", "Type part of the description."],
                     "`<Space>sk`."),
                    ("Common mistake", "Is there a key for Lualine?",
                     "Look at the plugin notes.",
                     ["Lualine is always visible.", "It has no keymaps."],
                     "No. It needs none."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Comment, jump, scroll and fold with the g, [ ] and z keys",
            "subtitle": "Comment a line, jump to the next error, change a word to upper case, center a line on the screen, fold a function",
            "idea": (
                "Find a key you forgot: press the prefix, wait, and which-key lists the rest.",
                [
                    ("Comment or uncomment a line", "gcc", "Toggle comment on the line."),
                    ("Jump to the next error or warning", "]d", "Jump to the next diagnostic."),
                    ("Put the cursor line in the middle of the screen", "zz", "Scroll the cursor line to the middle."),
                    ("Fold or unfold code under the cursor", "za", "Open or close the fold under the cursor."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I scroll, comment lines and find a jump I half remember, without the mouse or doing it by hand?",
                "fix": "Use three prefixes: `g` for actions, `[` and `]` for next and previous, `z` for view and folds.",
            },
            "drills": [
                {
                    "h2": "Go to a line, a file or an earlier change with g keys",
                    "intro": "Press `g` followed by another key. Which-key shows them when you press `g`.",
                    "blocks": [
                        K("Go to a line, open a file or link, and go to an earlier change", G_NAV),
                        K("Select the next or previous search match (after g in operator-pending or visual)", G_SEARCH),
                        {"type": "cmd", "where": "nvim", "title": "Change one search match, then repeat on the next", "code": "/pattern\ncgn\n.",
                         "expect": "`cgn` changes the match and `.` repeats it on the next match. Lesson 7 drills this in depth."},
                    ],
                },
                {
                    "h2": "Change text to upper or lower case and comment lines",
                    "intro": "Change case and comment text with operators that take a motion.",
                    "blocks": [
                        K("Make text lowercase or uppercase, or swap its case", G_CASE),
                        {"type": "cmd", "where": "nvim", "title": "Change the case of a word", "code": "guiw\ngUiw\ng~iw",
                         "expect": "The word under the cursor is lowercased, uppercased, then toggled."},
                        K("Comment or uncomment lines", G_COMMENTS),
                        {"type": "cmd", "where": "nvim", "title": "Comment a paragraph", "code": "gcip",
                         "expect": "The paragraph under the cursor is commented. In visual mode, select lines and press `gc`."},
                    ],
                },
                {
                    "h2": "Jump to a definition, find its uses, format text, and use tabs and marks",
                    "intro": "LazyVim sets its primary LSP jumps when a server attaches.",
                    "blocks": [
                        K("Jump to a definition, find every use and show docs (LSP)", G_LSP),
                        {"type": "text", "body": "Use Neovim 0.11's built-in LSP keys as a fallback: `grn` rename, `gra` code action, `grr` references, `gri` implementation, `grt` type definition, `grx` codelens."},
                        K("Wrap text to the text width", G_FORMAT),
                        K("Go to the next or previous tab page (not buffers)", G_TABS),
                        K("Jump to a mark without changing the jump list", G_MARKS),
                        K("Show a character's code, reselect text and join lines", G_MISC),
                    ],
                },
                {
                    "h2": "Jump to the next or previous error, git change or function (brackets)",
                    "intro": "Jump between diagnostics, hunks, functions and more.",
                    "blocks": [K("Jump to the next or previous item with [ and ]", BRACKETS)],
                },
                {
                    "h2": "Scroll the screen, fold code and fix spelling (z keys)",
                    "intro": "Scroll and fold with the `z` prefix.",
                    "blocks": [
                        K("Move a line to the center, top or bottom of the screen (cursor stays)", Z_SCROLL),
                        K("Open or close folds", Z_FOLD, **{"try": "`nvim ~/tw/orders.py`, then `10G` (the `def report` line) and `zc`. Then `zM`, then `zR`.",
                          "expect": "`zc` hides lines 11–12 behind `def report(codes):`. `zM` leaves only signatures and top-level lines. `zR` opens everything."}),
                        {"type": "text", "body": "Why does `zf` fail with `E350`? Folds here come from treesitter, so every function and block folds on its own. To fold lines you pick, run `:setlocal foldmethod=manual`, select with `V`, press `zf`; `zd` removes it. Without that, `zf` stops with `E350`."},
                        K("Fix a misspelled word or add it to the dictionary", Z_SPELL),
                    ],
                },
            ],
            "rules": {
                "h2": "Find out what the g, [ ] and z prefixes and fold keys do",
                "cards": [
                    ("What do the g, [ ] and z prefixes do?", "Press one and wait for which-key.", ["Prefix", "Family"], [
                        ["`g`", "Actions: go, case, comment, format"],
                        ["`[` and `]`", "Jump to the previous and next of something"],
                        ["`z`", "View: scroll, folds, spelling"],
                    ]),
                    ("Open or close one fold, or all folds", "Lowercase acts once, capital acts recursively.", ["Open", "Close"], [
                        ["`zo` open fold", "`zc` close fold"],
                        ["`zO` open recursively", "`zC` close recursively"],
                        ["`zR` open all", "`zM` close all"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Skim an unfamiliar file with a few fold keys",
                "frame": "Skim an unfamiliar file quickly.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (None, "`zM`", "Close every fold, leaving the outline below."),
                    (None, "`zj` then `za`", "Move to the next fold, `calc_totl`, and open it."),
                    (None, "`]d`", "Jump to the next diagnostic, if the file has one."),
                    (None, "`zz` then `zR`", "Center the line, then open all folds."),
                ],
                "after": "PRICES = {\"A1\": 2.50, \"A2\": 4.00, \"A3\": 1.25}\n\n\n+--  2 lines: def calc_totl(price, qty):\n\n\n+--  3 lines: def report(codes):\n\n\nname = \"pen\"",
                "meaning": "Read the structure first and the details second.",
            },
            "practice": {
                "h2": "Check how to use the g, bracket and z keys",
                "qs": [
                    ("Mechanism", "What is the difference between `gu` and `gU`?",
                     "Case of the letter.",
                     ["Lowercase `gu` lowercases.", "Capital `gU` uppercases."],
                     "`gu` lowercases and `gU` uppercases the motion."),
                    ("Keystrokes", "How do I comment or uncomment the current line?",
                     "Double the last letter.",
                     ["Press `gcc`."],
                     "`gcc`."),
                    ("Application", "How do I jump to the next git hunk?",
                     "Bracket plus the hunk letter.",
                     ["Press `]h`."],
                     "`]h`."),
                    ("Common mistake", "I pressed `zH` expecting a fold. What does it do?",
                     "Fold keys are lowercase or `zM`/`zR`.",
                     ["`zH` scrolls half a screen to the left."],
                     "It scrolls left. Folds use `za`, `zo`, `zc`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Split windows, use the Space menu and run colon commands",
            "subtitle": "Split a window, delete a line without leaving insert mode, find any Space leader key, save and quit with a colon command",
            "idea": (
                "Find a key you forgot: Ctrl keys, the Space leader menu and colon commands.",
                [
                    ("Split the window side by side", "Ctrl-w v", "Two windows side by side."),
                    ("Run one normal command while typing", "Ctrl-o", "Run one normal command, then return to insert."),
                    ("See every Space leader group", "<Space>", "Wait to see every group."),
                    ("Save, split or manage buffers with a command", ":", "Save, split and manage buffers."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I delete one line without leaving insert mode, and split windows without the mouse?",
                "fix": "Use `Ctrl-o` for one normal command in insert mode, and `Ctrl-w` plus a letter for windows.",
            },
            "drills": [
                {
                    "h2": "Scroll, edit and split windows with Ctrl keys",
                    "intro": "Scroll and jump, edit in normal and insert mode, and manage windows.",
                    "blocks": [
                        K("Scroll, jump back and forward, and switch files", CTRL_NAV),
                        K("Add to or subtract from a number, and redo (normal mode)", CTRL_NORMAL),
                        K("Delete words, indent and paste while typing (insert mode)", CTRL_INSERT),
                        {"type": "cmd", "where": "nvim", "title": "Delete a line without leaving insert mode", "code": "Ctrl-o dd",
                         "expect": "The line is deleted and you are still in insert mode. `Ctrl-o` in insert mode is huge."},
                        K("Split, move between and close windows", CTRL_WINDOWS, **{"try": "Press `Ctrl-w v`, then `Ctrl-w l`, then `Ctrl-w q`.",
                                                                                   "expect": "The window splits side by side, the cursor moves to the right split, and that split closes."}),
                    ],
                },
                {
                    "h2": "Find a file or search text with the Space leader",
                    "intro": "See the groups: press `<Space>` and wait for which-key. The main groups follow.",
                    "blocks": [
                        K("Find a file, a recent file or an open buffer (<Space>f)", L_FIND),
                        {"type": "text", "body": "Find where a search starts: in the current config the find keys (`<Space><Space>`, `<Space>ff`, `<Space>sf`) and the grep keys (`<Space>/`, `<Space>sg`, `<Space>sw`) search `:pwd`, not the project root. The arrow keys are disabled in normal, visual and insert mode."},
                        K("Search text, diagnostics, help and keymaps (<Space>s)", L_SEARCH),
                    ],
                },
                {
                    "h2": "Use git, see errors and switch buffers with the Space leader",
                    "intro": "The git, Trouble and buffer groups.",
                    "blocks": [
                        K("Open LazyGit, see history, diffs and pull requests (<Space>g)", L_GIT),
                        {"type": "text", "body": "Open Diffview by command: `:DiffviewOpen` and `:DiffviewFileHistory %` also work."},
                        K("See errors, warnings and todo comments in a list (<Space>x)", L_TROUBLE),
                        K("Switch, pin and close buffers (<Space>b)", L_BUFFERS),
                    ],
                },
                {
                    "h2": "Format code, stage a hunk, open a terminal and run tests",
                    "intro": "Code actions, hunk staging, terminals and the test prefix are all under Space.",
                    "blocks": [
                        K("Format, rename and fix code (<Space>c)", L_CODE),
                        K("Stage, discard or preview a changed block of code (<Space>gh)", L_HUNKS),
                        K("Open a terminal or run tests (<Space>f and <Space>t)", L_TERMINAL),
                        {"type": "text", "body": "Find the test and terminal keys: `<Space>t` holds both: the test keys (neotest) and the terminals `<Space>tf`, `<Space>tv` and `<Space>th`. `<Space>ft` is the floating terminal, and `Ctrl-\\` and `Ctrl-/` toggle the last terminal you used. Every terminal opens in `:pwd`. The inlay-hints toggle lives under `<Space>u`: verify the subkey in which-key."},
                    ],
                },
                {
                    "h2": "Save, quit, split and manage buffers with colon commands",
                    "intro": "Type these commands after you press `:`.",
                    "blocks": [
                        K("Save, quit and open files", X_FILES),
                        K("List, switch and close buffers", X_BUFFERS),
                        K("Split or close windows", X_SPLITS),
                        {"type": "cmd", "where": "nvim", "title": "Split, then close the split", "code": ":vsplit\n:close",
                         "expect": "The window splits vertically, then the current split closes."},
                        K("Clear highlighting, change options and check health", X_USEFUL),
                    ],
                },
            ],
            "rules": {
                "h2": "Find the right key for windows, leader groups and quitting",
                "cards": [
                    ("Split, move between and close windows", "Press Ctrl-w, then one letter.", ["Keys", "Does"], [
                        ["`Ctrl-w v`", "Split the window vertically"],
                        ["`Ctrl-w s`", "Split the window horizontally"],
                        ["`Ctrl-w h/j/k/l`", "Change to another split"],
                        ["`Ctrl-w q`", "Close this split"],
                        ["`Ctrl-w o`", "Close all other splits"],
                    ]),
                    ("Which Space key opens which group?", "Each letter after Space opens one group.", ["Group", "Holds"], [
                        ["`<Space>f`", "Find files, buffers, recent"],
                        ["`<Space>s`", "Search and pickers"],
                        ["`<Space>g`", "Git"],
                        ["`<Space>c`", "Code actions"],
                        ["`<Space>t`", "Tests and terminals"],
                        ["`<Space>x`", "Trouble lists"],
                    ]),
                    ("Quit Neovim with or without saving", "Pick the right exit.", ["Command", "Does"], [
                        ["`:q`", "Quit"],
                        ["`:wq`", "Save and quit"],
                        ["`:q!`", "Quit without saving"],
                        ["`:qa!`", "Quit all windows without saving"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Fix a line without leaving insert mode",
                "frame": "Remove a stale last line while you type at the end of the list.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 16, end of line", "`G` `A`"), "`Ctrl-o` then `dd`", "Delete `TODO reply to Sam`. You stay in insert mode."),
                    (None, "type ` x2`", "The text lands at the end of `buy boxes`."),
                    (None, "`Esc`, then `Ctrl-w v`", "Open a vertical split for reference."),
                    (None, "`Ctrl-w q`", "Close it."),
                ],
                "before": "buy boxes\nTODO reply to Sam",
                "after": "buy boxes x2",
                "meaning": "Keep typing: your flow never breaks.",
            },
            "practice": {
                "h2": "Check how to use Ctrl, Space and colon keys",
                "qs": [
                    ("Mechanism", "What does `Ctrl-o` do in insert mode?",
                     "One command only.",
                     ["It runs ONE normal-mode command.", "Then you are back in insert mode."],
                     "One normal command, then back to insert."),
                    ("Keystrokes", "How do I open a vertical split and close it again?",
                     "Ctrl-w plus a letter each time.",
                     ["Press `Ctrl-w v`.", "Press `Ctrl-w q`."],
                     "`Ctrl-w v`, then `Ctrl-w q`."),
                    ("Application", "How do I show relative line numbers?",
                     "A `:set` option.",
                     ["Run `:set relativenumber`."],
                     "`:set relativenumber`."),
                    ("Common mistake", "I typed `:q!` and lost my edits. What should I have used?",
                     "Save first.",
                     ["`:q!` quits without saving.", "`:wq` saves, then quits."],
                     "`:wq`."),
                ],
            },
        },
    ],
}
