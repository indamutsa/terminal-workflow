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
gsa{motion}{char}   Add surrounding (gsa + motion + char)
gsd{char}           Delete surrounding
gsr{old}{new}       Replace surrounding
gsf / gsF           Find next / previous surrounding
gsh                 Highlight surrounding
'''

SURROUND_EX = r'''
gsaiw"           Surround word with "
gsa3w(           Surround 3 words with ()
gsd(             Delete surrounding ()
gsr({            Replace () with {}
'''

FLASH_JUMP = r'''
s{chars}         Type 's' then start typing — labels appear on matches, press label to jump
                 Works in normal, visual, and operator-pending mode
'''

FLASH_TS = r'''
S                Select a treesitter node (function, block, class)
                 Press S → labels appear on code structures → pick one to select it
                 Chain: S → label → expand with S again for parent node
'''

FLASH_REMOTE = r'''
yr{label}        Yank text at a remote location without moving cursor
dr{label}        Delete text at a remote location without moving cursor
cr{label}        Change text at a remote location
'''

FLASH_SEARCH = r'''
/pattern         Normal search gets jump labels — press a label to jump directly
f{char}          f/t motions get labels when multiple matches exist on line
t{char}          Same — type the label to jump further
'''

HARPOON = r'''
<Space>H         Add current file to harpoon list
<Space>h         Open harpoon quick menu (see all marked files, reorder, delete)
<Space>1         Jump to harpoon file 1
<Space>2         Jump to harpoon file 2
<Space>3         Jump to harpoon file 3
<Space>4         Jump to harpoon file 4
...              up to
<Space>9         Jump to harpoon file 9
'''

AERIAL = r'''
<Space>cs        Toggle aerial outline (symbols)
{                Jump to previous symbol (function/class)
}                Jump to next symbol (function/class)
'''

AERIAL_PANEL = r'''
Enter            Jump to that symbol
o                Jump to symbol but keep aerial open
l                Expand node
h                Collapse node
L                Expand all
H                Collapse all
'''

TS_SELECT = r'''
vaf              Select around function (including def/signature)
vif              Select inside function (body only)
vac              Select around class
vic              Select inside class
vaa              Select around argument/parameter
via              Select inside argument/parameter
daf              Delete entire function
yif              Yank function body
caa              Change argument
'''

TS_MOVE = r'''
]f               Jump to next function start
[f               Jump to previous function start
]c               Jump to next class start
[c               Jump to previous class start
'''

MINI_AI = r'''
af / if          Around / inside function
ac / ic          Around / inside class
ao / io          Around / inside a code block (treesitter)
a) i) a] i] a} i}  Brackets — searches forward on the line if not inside one
aq / iq          Around / inside any quote
an / in          Next text object (e.g. cin) targets the next match)
al / il          Last text object (previous match)
g[ / g]          Jump to start / end of the text object under cursor
'''

BUFFERLINE = [
    ("L (Shift-L)", "Next buffer/tab"),
    ("H (Shift-H)", "Previous buffer/tab"),
] + R(r'''
<Space>bp        Pin/unpin current buffer
<Space>bP        Delete all non-pinned buffers
<Space>bj        Pick a buffer by label
<Space>bl        Delete buffers to the left
<Space>br        Delete buffers to the right
<Space>bd        Close current buffer (LazyVim default — verify in which-key)
''')

PERSISTENCE = r'''
<Space>qs        Restore session for this directory
<Space>ql        Restore last session
<Space>qS        Select a session to restore
<Space>qd        Don't save the current session (stop auto-save)
'''

YANKY = r'''
<Space>p         Open yank history picker (pick any past yank)
p / P            Paste after / before (yanky-aware)
]y / [y          Cycle forward / backward through yank history
]p / [p          Paste with indent matched to current line
gp / gP          Paste, leaving cursor after the pasted text
'''

TODO = r'''
]t / [t          Jump to next / previous todo comment
<Space>st        Search all todos (picker)
<Space>sT        Search only TODO/FIX/FIXME
<Space>xt        Todos in the Trouble panel
'''

DADBOD = r'''
<Space>D         Toggle the DB UI (explorer of connections/tables)
'''

RENDER_MD = r'''
<Space>um        Toggle inline rendering on/off (UI toggle)
'''

MD_PREVIEW = r'''
<Space>cp        Markdown Preview (opens live-refreshing browser view)
'''

NAVIGATOR = r'''
Ctrl-h           Move left (works across nvim ↔ tmux)
Ctrl-j           Move down
Ctrl-k           Move up
Ctrl-l           Move right
'''

WHICH_KEY = r'''
<Space>           Wait → see all leader groups
<Space>?          Buffer-local keymaps
g                 Wait → see all g-prefix commands
z                 Wait → see all z-prefix commands
<Space>sk         Fuzzy-search ALL keymaps by description
'''

G_NAV = r'''
gg               First line of file
G                Last line of file (not g prefix, but related)
gi               Go to last insert position and enter insert mode
gf               Go to file under cursor (opens the file path)
gx               Open filepath or URL under cursor in system handler (browser, Finder)
gO               Document symbols (LSP outline of current file)
g,               Go to newer position in change list
g;               Go to older position in change list
'''

G_SEARCH = r'''
gn               Search forwards and select the match
gN               Search backwards and select the match
'''

G_CASE = r'''
gu{motion}       Lowercase (e.g., `guiw` = lowercase word)
gU{motion}       Uppercase (e.g., `gUiw` = uppercase word)
g~{motion}       Toggle case (e.g., `g~iw` = toggle word)
~                Toggle case of char under cursor
'''

G_COMMENTS = r'''
gc{motion}       Toggle comment (e.g., `gcip` = comment paragraph)
gcc              Toggle comment on current line
gcO              Add comment on line above
gco              Add comment on line below
'''

G_LSP = r'''
gd               Go to definition
gr               Find all references
gI               Go to implementation
gy               Go to type definition
gD               Go to declaration
gK               Signature help
gO               Document symbols
K                Hover docs
'''

G_FORMAT = r'''
gw{motion}       Format text (wraps to textwidth)
gq{motion}       Format text and move cursor to end
'''

G_TABS = r'''
gt               Go to next tab page
gT               Go to previous tab page
'''

G_MARKS = r'''
g'{mark}         Jump to mark (like `'{mark}` but doesn't change jump list)
'''

G_MISC = r'''
ga               Show character code under cursor (ASCII, hex, octal)
g8               Show UTF-8 byte sequence for char under cursor
gv               Reselect last visual selection
gJ               Join lines without adding space
gf               Go to file under cursor
'''

BRACKETS = r'''
]d / [d          Next / previous diagnostic (error/warning)
]h / [h          Next / previous git hunk
]m / [m          Next / previous method/function start
]M / [M          Next / previous method/function end
]{ / [{          Next / previous unmatched {
]] / [[          Next / previous section/class
]s / [s          Next / previous misspelled word
]q / [q          Next / previous quickfix item
]b / [b          Next / previous buffer
'''

Z_SCROLL = r'''
zz               Center current line on screen
zt               Move current line to top of screen
zb               Move current line to bottom of screen
zH               Scroll half screen to the left
zL               Scroll half screen to the right
'''

Z_FOLD = r'''
za               Toggle fold under cursor
zA               Toggle fold recursively
zo               Open fold
zO               Open fold recursively
zc               Close fold
zC               Close fold recursively
zM               Close ALL folds in file
zR               Open ALL folds in file
zj               Move to next fold
zk               Move to previous fold
'''

Z_SPELL = r'''
z=               Show spelling suggestions for word under cursor
zg               Mark word as good (add to dictionary)
zw               Mark word as wrong
'''

CTRL_NAV = r'''
Ctrl-o           Jump back (in jump list — like browser back)
Ctrl-i           Jump forward (in jump list)
Ctrl-d           Half-page down
Ctrl-u           Half-page up
Ctrl-f           Full page down
Ctrl-b           Full page up
Ctrl-e           Scroll down one line (cursor stays)
Ctrl-y           Scroll up one line (cursor stays)
Ctrl-]           Jump to definition (ctags — LSP uses gd instead)
Ctrl-t           Jump back from definition
Ctrl-^           Switch to alternate (last) file
'''

CTRL_NORMAL = r'''
Ctrl-a           Increment number under cursor
Ctrl-x           Decrement number under cursor
Ctrl-r           Redo
'''

CTRL_INSERT = r'''
Ctrl-w           Delete word backward (like Option+Delete)
Ctrl-u           Delete to start of line (like Cmd+Delete)
Ctrl-h           Delete character backward (like Backspace)
Ctrl-t           Indent current line
Ctrl-d           Unindent current line
Ctrl-r "         Paste from register (e.g., Ctrl-r 0 = last yank)
Ctrl-n           Autocomplete next match
Ctrl-p           Autocomplete previous match
Ctrl-o           Execute ONE normal mode command, then back to insert
'''

CTRL_WINDOWS = r'''
Ctrl-w h/j/k/l   Navigate between splits
Ctrl-w s          Horizontal split
Ctrl-w v          Vertical split
Ctrl-w q          Close split
Ctrl-w =          Equalize split sizes
Ctrl-w _          Maximize height
Ctrl-w |          Maximize width
Ctrl-w o          Close all other splits (keep only current)
Ctrl-w r          Rotate splits
Ctrl-w T          Move current split to new tab
'''

L_FIND = r'''
<Space><Space>   Find files (root dir)
<Space>ff        Find files (root dir)
<Space>fr        Recent files
<Space>fg        Find git files
<Space>fb        Buffers
<Space>,         Buffers (quick switch)
'''

L_SEARCH = r'''
<Space>sf        Search files by name (added — your primary find-file)
<Space>sF        Search files (cwd)
<Space>sg        Grep (search file contents, root dir)
<Space>sw        Grep word / selection under cursor
<Space>sd        Diagnostics
<Space>sR        Resume last picker
<Space>sh        Help pages
<Space>sk        Keymaps
<Space>sC        Commands
<Space>sm        Marks
<Space>st        Todo comments
<Space>sr        Search & replace (grug-far)   ← note: lowercase r = replace
'''

L_GIT = r'''
<Space>gg        LazyGit (repository root)
<Space>gG        LazyGit (current working directory)
<Space>gL        Git log (current working directory)
<Space>gb        Commit history for current line
<Space>gf        Commit history for current file
<Space>gl        Git log (repository root)
<Space>gB        Git browse (open on remote)
<Space>gY        Git browse (copy remote URL)
<Space>gs        Git status (picker)
<Space>gS        Git stash
<Space>gi / gI   Open / all GitHub issues
<Space>gp / gP   Open / all GitHub pull requests
<Space>gd        Git diff — hunks (Snacks picker)
<Space>gD        Git diff against origin (Snacks picker)
<Space>gv        Working-tree diff (Diffview)
<Space>gV        Current-file history (Diffview)
'''

L_TROUBLE = r'''
<Space>xx        Diagnostics (Trouble)
<Space>xX        Buffer diagnostics (Trouble)
<Space>xt        Todo (Trouble)
<Space>xT        Todo/Fix/Fixme (Trouble)
<Space>xL        Location list (Trouble)
<Space>xQ        Quickfix list (Trouble)
'''

L_BUFFERS = r'''
<Space>bp        Toggle pin
<Space>bP        Delete non-pinned buffers
<Space>bj        Pick buffer by label
<Space>bl        Delete buffers to the left
<Space>br        Delete buffers to the right
<Space>bd        Delete buffer (LazyVim default — verify in which-key)
<Space><Space>   Find files / switch (snacks)
<Space>,         Switch between open buffers
'''

L_CODE = r'''
<Space>cf        Format file
<Space>cr        Rename (LSP)
<Space>ca        Code action (LSP)
<Space>cd        Line diagnostics
<Space>cl        LSP info
<Space>cs        Symbols outline (Aerial)
<Space>cm        Mason (LSP/formatter installer)
'''

L_HUNKS = r'''
<Space>ghs       Stage hunk
<Space>ghr       Reset hunk
<Space>ghp       Preview hunk
<Space>ghb       Blame line
<Space>ghS       Stage buffer
<Space>ghR       Reset buffer
'''

L_TERMINAL = r'''
<Space>ft        Toggle floating terminal
<Space>Tf        Terminal — float (split)
<Space>Tv        Terminal — vertical split
<Space>Th        Terminal — horizontal split

<Space>t         TEST prefix (neotest) — tt run file, tr run nearest, ts summary
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
    "coverage_allow": [],
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
                            ("gsaiw\"", "Wrap the word in double quotes"),
                            ("u", "Undo it: this is a motion drill, not a real edit"),
                        ], **{"try": "Open `data/log.txt` and put the cursor on `pattern` in 'this line matches a filter pattern'.",
                              "expect": "The line reads exactly as it did before."}),
                        {"type": "cmd", "where": "shell", "title": "Prove nothing changed", "code": "git diff data/log.txt",
                         "expect": "Nothing: the file has no diff."},
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
                            ("gg", "Top of `orders.py`"),
                            ("s", "Then type `qu`, the first two letters of `qualifies_for_free_shipping`"),
                            ("label", "A label appears on the match: press it"),
                        ], **{"try": "Press the keys in order.", "expect": "The cursor lands exactly on `def qualifies_for_free_shipping(order):`."}),
                    ],
                },
                {
                    "h2": "Harpoon: instant file switching",
                    "intro": "Mark your most-used files and jump between them with one keystroke. Close the menu with `q` or `Esc`.",
                    "blocks": [
                        K("Harpoon keys", HARPOON),
                        K("Mark the 4 files you keep bouncing between", [
                            ("<Space>H", "In each of `src/calculator.py`, `src/orders.py`, `src/report.py` and `tests/test_orders.py`"),
                            ("<Space>2", "From anywhere: jump straight to `orders.py`"),
                            ("<Space>h", "Open the quick menu"),
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
                        K("Get the shape of a file without reading it", [("<Space>cs", "Open the outline in `orders.py`")],
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
                            ("vif", "Inside `qualifies_for_free_shipping`: select the body only, then Esc"),
                            ("vaf", "Select the whole def including the signature, then Esc"),
                            ("vic", "Inside `OrderBook`: body only"),
                            ("vac", "The whole class"),
                            ("yif", "Back on `qualifies_for_free_shipping`: yank just the body"),
                            (":new", "Open a scratch buffer"),
                            ("p", "Paste and look"),
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
                            ("ci)", "On `return` in `Order.subtotal`: finds the `sum(...)` parens ahead and enters insert mode inside them"),
                            ("Esc", "Type anything first, then leave insert mode"),
                            ("u", "Undo at once: this is a motion drill"),
                        ], **{"try": "Put the cursor on `return` in `return sum(item[\"price\"] * item[\"qty\"] for item in self.items)`.",
                              "expect": "The line shows no change once you undo."}),
                        {"type": "cmd", "where": "shell", "title": "Prove nothing changed", "code": "git diff src/orders.py",
                         "expect": "No diff for that line."},
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
                            ("yy", "In the `RAW_ORDERS` list: yank the \"A1\" line"),
                            ("yy", "Move down and yank the \"A2\" line"),
                            (":new", "Open a scratch buffer"),
                            ("p", "Pastes the A2 line (most recent)"),
                            ("[y", "Swaps the pasted text to the A1 line, without re-yanking"),
                        ], **{"try": "Work in `orders.py`'s `RAW_ORDERS` list and press the keys in order.",
                              "expect": "The scratch buffer now shows the \"A1\" line, not \"A2\". Close it without saving with `:bd!`."}),
                    ],
                },
                {
                    "h2": "Todo comments",
                    "intro": "Highlights `TODO`, `FIX`, `FIXME`, `HACK`, `NOTE` and `WARN`, and lets you jump to or search them.",
                    "blocks": [
                        K("Todo keys", TODO),
                        K("Sweep for what is left", [("<Space>st", "Search all TODOs project-wide")],
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
                        ["`[y` / `]y`", "Cycle yank history"],
                        ["`<Space>p`", "Yank history picker"],
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
                    ("Keystrokes", "Cycle to the previous yank after a paste.",
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
                        K("Find (`<Space>f`) and the quick-finders", L_FIND),
                        {"type": "text", "body": "In the current config `<Space><Space>`, `<Space>ff` and `<Space>sf` search the current directory, not the root dir. The arrow keys are disabled in normal, visual and insert mode."},
                        K("Search (`<Space>s`)", L_SEARCH),
                    ],
                },
                {
                    "h2": "The Space leader: git, diagnostics and buffers",
                    "intro": "Git, Trouble and buffer groups.",
                    "blocks": [
                        K("Git (`<Space>g`)", L_GIT),
                        {"type": "text", "body": "Direct Diffview commands are also available: `:DiffviewOpen` and `:DiffviewFileHistory %`."},
                        K("Diagnostics and Trouble (`<Space>x`)", L_TROUBLE),
                        K("Buffers (`<Space>b`)", L_BUFFERS),
                    ],
                },
                {
                    "h2": "The Space leader: code, hunks, terminals and tests",
                    "intro": "Code actions, hunk staging, terminals and the test prefix.",
                    "blocks": [
                        K("Code (`<Space>c`)", L_CODE),
                        K("Hunks and git signs (`<Space>gh`)", L_HUNKS),
                        K("Terminal (`<Space>f` and `<Space>T`) and Test (`<Space>t`)", L_TERMINAL),
                        {"type": "text", "body": "Do not confuse them: `<Space>t*` is test, `<Space>T*` is the split terminal (the lesson's mapping, not in the current config), and `<Space>ft`, `Ctrl-\\` and `Ctrl-/` are the floating terminal. The inlay-hints toggle lives under `<Space>u`: verify the subkey in which-key."},
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
                        ["`Ctrl-w v`", "Vertical split"],
                        ["`Ctrl-w s`", "Horizontal split"],
                        ["`Ctrl-w h/j/k/l`", "Move between splits"],
                        ["`Ctrl-w q`", "Close split"],
                        ["`Ctrl-w o`", "Keep only this split"],
                    ]),
                    ("Leader groups", "Each letter after Space opens one group.", ["Group", "Holds"], [
                        ["`<Space>f`", "Find files, buffers, recent"],
                        ["`<Space>s`", "Search and pickers"],
                        ["`<Space>g`", "Git"],
                        ["`<Space>c`", "Code actions"],
                        ["`<Space>t`", "Tests"],
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
