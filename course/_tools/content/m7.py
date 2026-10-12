"""Module 7: expert Neovim. Source: lesson 07 Neovim Expert.md."""
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


def PY(title, code):
    return {"type": "code", "file": "src/orders.py", "title": title, "code": C(code)}


def X(title, code, expect, where="nvim"):
    return {"type": "cmd", "where": where, "title": title, "code": C(code), "expect": expect}


COUNT = r'''
3dw              Delete 3 words
5j               Move down 5 lines
2ci"             Change inside the 2nd outer quotes
d/pattern        Delete until pattern match
c/foo            Change everything until "foo"
y?bar            Yank backwards until "bar"
'''

OP_SEARCH = r'''
d/function       Delete everything from cursor until "function"
c/return         Change from cursor until "return"
y/class          Yank from cursor until "class"
v/end            Select from cursor until "end"
'''

TILL = r'''
dt)              Delete till ) (not including the ))
ct,              Change till comma
yt:              Yank till colon
vt"              Select till quote
df)              Delete including ) (f = on the char, t = before it)
'''

RELATIVE = r'''
d5j              Delete from here down 5 lines
y3k              Yank from here up 3 lines
>8j              Indent 9 lines (current + 8 below)
gq5j             Format 6 lines
v5j              Select 6 lines
'''

MINI_AI = r'''
cin)             Change inside next parentheses (cursor doesn't need to be inside)
cil)             Change inside last (previous) parentheses
c2i{             Change inside the 2nd enclosing brace
d2a"             Delete around the 2nd enclosing quotes
'''

TS_ARGS = r'''
cia              Change inside argument
daa              Delete around argument (including comma)
via              Select argument
'''

DOT = r'''
/pattern         Find what you want to change
cgn              Change the next match (combines c + gn motion)
.                Repeat on next match
.                And the next one
n                Skip one (don't change it)
.                Change this one
'''

BAD = r'''
f"ldt"           (multiple motions — . only repeats dt")
'''

GOOD = r'''
ci"              (one operation — . repeats the whole thing)
'''

SELF_CORRECT = r'''
qa               Start recording
0                Go to start of line (known position)
f:               Jump to colon (find anchor point)
l                Move right
dw               Delete word
A,               Append comma at end
j                Next line
q                Stop recording
'''

RECURSIVE = r'''
qqq              Clear register q
qa               Start recording into a
0f:ldwA,Escj@aq  Do work, move down, call @a, stop
@a               Run it — processes all remaining lines
'''

MACRO_EDIT = r'''
"qp              Paste macro from register q as text
                 (edit the text)
0"qy$            Yank the line back into register q
dd               Delete the temp line
'''

MACRO_VISUAL = r'''
V5j              Select 6 lines
:normal @a       Run macro 'a' on each selected line
'''

EXPR_INSERT = r'''
Ctrl-r =         Enter expression register
5 * 42 Enter     Inserts "210"
system('date')   Inserts current date
'''

EXPR_NORMAL = r'''
"=5*42p          Paste result of expression
'''

APPEND = r'''
"ayy             Yank line into register a (overwrite)
"Ayy             Append another line to register a
"ap              Paste all accumulated lines
'''

BLACK_HOLE = r'''
"_dd             Delete line without affecting any register
"_diw            Delete word, keep your yank intact
'''

FILENAME = r'''
Ctrl-r %         Insert current filename (in insert mode)
Ctrl-r #         Insert alternate filename
"%p              Paste current filename (normal mode)
'''

CMDLINE_WIN = r'''
q:               Open command-line window (edit/search/rerun old commands)
q/               Open search history window
Ctrl-f           From : prompt, switch to command-line window
'''

QUICKFIX = r'''
:copen           Open quickfix window
:cclose          Close quickfix window
:cnext / :cprev  Next / previous item (or ]q / [q)
:cfirst / :clast Jump to first / last
:cdo s/a/b/g     Run command on every quickfix entry
'''

LOCLIST = r'''
:lopen           Open location list
:lclose          Close
:lnext / :lprev  Navigate
'''

AUTO_MARKS = r'''
`.               Last edit position
`^               Last insert mode position
`[               Start of last yank/change
`]               End of last yank/change
`<               Start of last visual selection
`>               End of last visual selection
``               Position before last jump
'''

MARK_OPERATE = r'''
ma               Mark position
                 (move somewhere else, do stuff)
d`a              Delete from here back to mark a
y`a              Yank from here to mark a
v`a              Select from here to mark a
'''

GLOBAL_MARKS = r'''
mA               Set global mark A (remembered across files)
'A               Jump to file and line of mark A
'''

REGEX_GROUPS = r'''
:%s/\(\w\+\)/"\1"/g           Wrap every word in quotes
:%s/\v(\w+)/"\1"/g            Same with "very magic" (less escaping)
:%s/foo\(.*\)bar/baz\1qux/g  Keep middle, change surrounds
'''

CASE_SUB = r'''
:%s/\<\(\w\)/\u\1/g          Capitalize first letter of every word
:%s/.*/\L&/g                  Lowercase entire file
:%s/.*/\U&/g                  Uppercase entire file
:%s/\<\w/\u&/g               Title Case
'''

EXPR_SUB = r'''
:%s/\d\+/\=submatch(0)+1/g   Increment all numbers by 1
:%s/\d\+/\=printf("%03d",submatch(0))/g  Zero-pad numbers
'''

RANGE_MOD = r'''
:5,10s/a/b/g     Lines 5-10 only
:'<,'>s/a/b/g    Visual selection only (auto-filled when you type : in visual)
:.,$s/a/b/g      Current line to end of file
:.,+5s/a/b/g     Current line plus next 5
:g/pattern/d     Delete all lines matching pattern
:v/pattern/d     Delete all lines NOT matching pattern
'''

GLOBAL = r'''
:g/TODO/d              Delete all lines with "TODO"
:g/^$/d                Delete all empty lines
:g/pattern/normal A;   Append ";" to all matching lines
:g/import/t$           Copy all import lines to end of file
:g/def /normal O       Add blank line above each function
:v/keep/d              Delete all lines NOT containing "keep"
:g/pattern/m0          Move all matching lines to top
'''

ARGS = r'''
:args **/*.py          Load all Python files into arglist
:args `git diff --name-only`  Load only changed files
:argdo %s/old/new/g | w       Run across all arg files
:next / :prev          Navigate arglist
'''

BUFFER_TRICKS = r'''
:b#               Switch to last buffer (alternate file)
Ctrl-^            Same as :b# (faster)
:bufdo            Run command across all open buffers
:ball             Open all buffers in splits
:tab ball         Open all buffers in tabs
'''

TABS = r'''
:tabnew          New tab page
:tabclose        Close tab page
gt / gT          Next / previous tab page
:tabmove 0       Move current tab to first position
'''

COMPLETE = r'''
Ctrl-n           Complete next match (from buffer/tags/etc.)
Ctrl-p           Complete previous match
Ctrl-x Ctrl-f    Complete filename
Ctrl-x Ctrl-l    Complete whole line
Ctrl-x Ctrl-o    Omni-completion (LSP)
'''

INSERT_TRICKS = r'''
Ctrl-o {cmd}     Execute one normal command without leaving insert
                 e.g., Ctrl-o dd = delete line, stay in insert
Ctrl-r =         Calculate expression and insert result
Ctrl-r "         Paste from default register
Ctrl-r 0         Paste from yank register
Ctrl-r %         Paste current filename
Ctrl-a           Insert last inserted text again
Ctrl-w           Delete word back
Ctrl-u           Delete to line start
Ctrl-t           Indent current line
Ctrl-d           Unindent current line
'''

BLOCK_COLUMN = r'''
Ctrl-v           Enter block mode
jjjj             Select column
I                Insert before column (affects all lines after Esc)
A                Append after column
c                Change column
r{char}          Replace column with char
d                Delete column
>                Indent selected block
'''

BLOCK_SEQ = r'''
Ctrl-v jjjj      Select 5 lines
g Ctrl-a         Create incrementing sequence (1,2,3,4,5)
'''

BLOCK_SEQ2 = r'''
Ctrl-v jjjj      Select
I0 Esc           Insert "0" on all lines
gv               Reselect
g Ctrl-a         Now they're 1,2,3,4,5
'''

BLOCK_ALIGN = r'''
Ctrl-v           Block select
jjj              Select rows
$                Extend to end (makes ragged selection)
A                Append at end of each line
'''

RANGE_SYNTAX = r'''
.                Current line
$                Last line
%                Entire file (same as 1,$)
'<,'>            Visual selection
.,.+5            Current line and next 5
'a,'b            From mark a to mark b
/pat1/,/pat2/    From pattern1 to pattern2
'''

EX_USEFUL = r'''
:t.              Duplicate current line (copy to here)
:t5              Copy current line to after line 5
:m$              Move current line to end of file
:m0              Move current line to top
:5,10m$          Move lines 5-10 to end
:5,10t.          Copy lines 5-10 to current position
:read !ls        Insert output of shell command below cursor
:read file.txt   Insert contents of file below cursor
:.!sort          Sort current line through shell sort
:'<,'>!sort      Sort selected lines
'''

JUMP_LIST = r'''
Ctrl-d / Ctrl-u      These DON'T add to jump list (good for browsing)
gg / G / /pattern    These DO add to jump list (for intentional navigation)
'''

QUICK_SWITCH = r'''
Ctrl-^               Toggle between last two files (fastest switch)
<Space><Space>       Fuzzy buffer list
:b partial_name      Switch by partial filename
'''

FIX_MOVE = r'''
ciw → type → Esc → n → .    Fix same pattern across file
*cwreplacement Esc n.n.n.    Replace word everywhere (review each)
'''

NUMBER_TRICK = r'''
Ctrl-a           Increment number under cursor
Ctrl-x           Decrement
5 Ctrl-a         Add 5 to number
'''

UNDO_TREE = r'''
:earlier 5m      Go back to file state 5 minutes ago
:later 2m        Go forward 2 minutes
:earlier 3f      Go back 3 file-saves ago
g-               Go to older state in undo tree
g+               Go to newer state in undo tree
'''

MODULE = {
    "n": 7,
    "folder": "m7-expert",
    "title": "Expert Neovim",
    "footer": "Counts, operators and the dot formula; macros and registers; quickfix, marks, substitution and :g; windows, insert, block, ranges and undo",
    "tagline": "Edit like a power user: the dot formula, macros, :g and undo trees.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Motions and the dot formula",
            "subtitle": "Counts, searches as motions, till-motions, text objects and the repeatable change.",
            "idea": (
                "Shape every edit so that one key repeats it.",
                [
                    ("Count a quote", "2ci\"", "Change inside the 2nd quoted string."),
                    ("Operate to a search", "d/pattern", "Delete up to the match."),
                    ("Change a match", "cgn", "Change the next match, then press `.`."),
                    ("Repeat", ".", "Run the last change again."),
                ],
                None,
            ),
            "problem": {
                "fail": "You count characters, hold `l` and retype the same change at every match.",
                "fix": "Use counts, searches and till-motions to land exactly, then `cgn` and `.` to repeat the change.",
            },
            "drills": [
                {
                    "h2": "Open the practice project",
                    "intro": "Every drill runs against `nvim-drills`. These are throwaway reps: undo with `u` or reload with `:e!` once you have seen the mechanic work. Lesson 6 makes the permanent fixes, but none of these drills depend on it.",
                    "blocks": [
                        X("Start Neovim in nvim-drills", "cd Terminal-Workflow/practice/nvim-drills\nnvim .", "Neovim opens on the project, ready for the drills.", "shell"),
                    ],
                },
                {
                    "h2": "Count + operator + motion",
                    "intro": "Everything takes a count.",
                    "blocks": [
                        K("Counts", COUNT),
                        PY("The A4 line has six quoted strings", '''
{"id": "A4", "items": [{"price": 8, "qty": 3}], "discount": 2},
'''),
                        K("Edit the 2nd quoted string", [
                            ("2ci\"", "Cursor before the first `\"` on the A4 line: jumps to the 2nd quoted string (`\"A4\"`) and enters insert mode"),
                            ("A4-REVIEW", "Type it, then Esc"),
                            ("u", "Undo"),
                            ("3dw", "From the start of the line: deletes 3 words (punctuation runs like `{\"` count as words)"),
                            ("u", "Undo"),
                        ], **{"try": "Open `src/orders.py` and find the `RAW_ORDERS` list.",
                              "expect": "After the `2ci\"` step, before undoing, the line reads `{\"id\": \"A4-REVIEW\", \"items\": ...}`: only the second quoted string changed, not `\"id\"`."}),
                    ],
                },
                {
                    "h2": "Operator + search",
                    "intro": "A search is only destructive when you hand it to an operator.",
                    "blocks": [
                        K("Operator and search", OP_SEARCH),
                        K("Jump to a method by searching", [
                            ("gg", "Line 1 of `src/calculator.py`"),
                            ("d/def divide", "Deletes from the top up to the start of `divide`"),
                            ("u", "Undo at once"),
                            ("/def divide", "Then Enter: just moves the cursor"),
                        ], **{"try": "Run the keys in order. `y/def divide` Enter is the halfway house: it yanks the range `d/` would delete, but the cursor stays put.",
                              "expect": "The cursor sits on the `d` of `def divide`, and nothing changed on disk."}),
                    ],
                },
                {
                    "h2": "The power of t and T (till)",
                    "intro": "`t` stops before the character, `f` lands on it.",
                    "blocks": [
                        K("Till", TILL),
                        PY("In build_order_book()", '''
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
'''),
                        K("Rewrite one argument", [
                            ("ct,", "Cursor on the `r` of the first `raw[\"id\"]`: change up to the next comma"),
                            ("raw.get(\"id\")", "Type it, then Esc"),
                            ("u", "Undo"),
                        ], **{"try": "Swap a dict-index for a `.get()` call in three keystrokes plus typing.",
                              "expect": "Before undoing, the line reads `book.add_order(Order(raw.get(\"id\"), raw[\"items\"], raw[\"discount\"]))`: only the first argument changed."}),
                    ],
                },
                {
                    "h2": "Relative line operations",
                    "intro": "Turn on relative line numbers with `:set relativenumber`. Then counts read straight off the screen.",
                    "blocks": [
                        K("Relative counts", RELATIVE),
                        K("Delete a list body using relative counts", [
                            (":set relativenumber", "In `src/orders.py`, cursor on the `RAW_ORDERS = [` line"),
                            ("j", "Land on the `\"A1\"` entry"),
                            ("d5j", "Deletes `A1` plus the next 5 (`A2` to `A6`); the brackets stay"),
                            ("u", "Immediately: this only proves the count math"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Right before undoing, `RAW_ORDERS` is an empty list body (`[` then `]` on adjacent lines). After `u`, all 6 orders are back."}),
                    ],
                },
                {
                    "h2": "Advanced text objects (with plugins)",
                    "intro": "With mini.ai the count goes before the `i` or `a`: `c2i{`, not `ci2{`. After an operator, vim reads `i{` as a two-character text object, so a digit between them is not a count.",
                    "blocks": [
                        K("mini.ai", MINI_AI),
                        K("Treesitter arguments", TS_ARGS),
                        PY("Order.subtotal", '''
return sum(item["price"] * item["qty"] for item in self.items)
'''),
                        PY("The A6 entry has two enclosing brace levels", '''
{"id": "A6", "items": [{"price": 3, "qty": 3}, {"price": 3, "qty": 3}], "discount": 0},
'''),
                        PY("build_order_book() again", '''
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
'''),
                        K("Edit nested structures", [
                            ("cin)", "Cursor on the `s` of `sum(`: change inside the next parens. Type `x for x in []`, Esc, then `u`"),
                            ("c2i{", "Cursor inside the first `{\"price\": 3, \"qty\": 3}` on the A6 line: targets the 2nd enclosing brace. Type `\"REPLACED\"`, Esc, then `u`"),
                            ("daa", "Cursor anywhere inside `raw[\"items\"]`: delete that argument and its trailing comma, then `u`"),
                        ], **{"try": "Undo after each step.",
                              "expect": "Step 1: `subtotal` briefly returns `sum(x for x in [])`. Step 2: the whole A6 entry collapses to `{\"REPLACED\"},`. Step 3: the constructor call has 2 arguments instead of 3."}),
                    ],
                },
                {
                    "h2": "The dot formula",
                    "intro": "The `.` command repeats the last change. Master users structure every edit to be repeatable. `cgn` plus `.` beats `:%s` when you want to review each change.",
                    "blocks": [
                        K("Search, change, repeat", DOT),
                        K("Bad: not repeatable", BAD),
                        K("Good: repeatable", GOOD),
                        {"type": "text", "body": "Multi-cursor without multi-cursor: `*` selects a word into the search register, `cgn` changes the current match, `.` applies it to the next, `n` skips one, `.` changes this one. You get interactive find-and-replace with undo per match."},
                        K("Selectively promote 9 of 10 items", [
                            ("gg", "Top of `data/log.txt` (ten lines `item 1: pending` to `item 10: pending`)"),
                            ("/pending", "Then Enter: land on the first match"),
                            ("cgn", "Type `queued`, Esc"),
                            (".", "Three times: matches 2, 3 and 4 become `queued`"),
                            ("n", "Twice, to skip match 5: the first `n` lands on it, the second hops to 6"),
                            (".", "Changes match 6; keep pressing for the other 4"),
                        ], **{"try": "Press the keys in order. Discard with `:e!` afterwards: other lessons reuse this file.",
                              "expect": "`<Space>sg pending` returns exactly 1 result (the skipped one) and `<Space>sg queued` returns 9."}),
                    ],
                },
            ],
            "rules": {
                "h2": "The edit toolkit",
                "cards": [
                    ("Choose the motion", "Land exactly where the change starts.", ["I want to", "Use"], [
                        ["Change the Nth quoted string", "`2ci\"`"],
                        ["Delete up to a pattern", "`d/pattern`"],
                        ["Change up to a comma", "`ct,`"],
                        ["Edit the next parens", "`cin)`"],
                        ["Edit the 2nd enclosing brace", "`c2i{`"],
                    ]),
                    ("The dot formula", "One repeatable change, applied at each match.", ["Key", "Does"], [
                        ["`/pattern`", "Find the first match"],
                        ["`cgn`", "Change that match"],
                        ["`.`", "Repeat on the next match"],
                        ["`n`", "Skip one (press twice if the cursor is on the match)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Review each rename",
                "frame": "Nine of ten lines should change, and one should stay.",
                "given": "`data/log.txt` is open with ten `pending` lines.",
                "steps": [
                    "Run `/pending`, then `cgn` and type `queued`, Esc.",
                    "Press `.` to repeat on the next matches.",
                    "Press `n` twice to skip the match you want to keep.",
                    "Press `.` to continue, then `:e!` to discard.",
                ],
                "meaning": "You chose each change, which a blind `:%s` never lets you do.",
            },
            "practice": {
                "h2": "Practice: motions and the dot formula",
                "qs": [
                    ("Mechanism", "Why does `n` have to be pressed twice to skip a match with `cgn` and `.`?",
                     "Where is the cursor after the first `n`?",
                     ["The first `n` lands on the match.", "`gn` operates on the match under the cursor, so `.` would change it."],
                     "The second `n` hops over it."),
                    ("Keystrokes", "Change the 2nd quoted string on a line.",
                     "Put the count before the object.",
                     ["Press `2ci\"`.", "Type the new text, then Esc."],
                     "`2ci\"`."),
                    ("Application", "Replace an argument up to the next comma.",
                     "Till, not find.",
                     ["Put the cursor on the argument.", "Press `ct,`."],
                     "`ct,`."),
                    ("Common mistake", "You wrote `c2i{` as `ci2{` and it failed. Why?",
                     "Where does the count go?",
                     ["After an operator `i{` is a two-character object.", "A digit between is not a count."],
                     "The count goes before: `c2i{`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Expert macros and registers",
            "subtitle": "Self-correcting and recursive macros, the expression register, appending and the black hole.",
            "idea": (
                "Registers hold text and macros alike. Edit them, append to them and keep them safe.",
                [
                    ("Record", "qa", "Record a macro into register a."),
                    ("Append yank", "\"Ayy", "Add a line to register a."),
                    ("Black hole", "\"_dd", "Delete without touching any register."),
                    ("History window", "q:", "Edit and rerun an old command."),
                ],
                None,
            ),
            "problem": {
                "fail": "A macro works on one line and breaks on the next, or a delete overwrites the text you meant to paste.",
                "fix": "Start every macro from a known position, append with capital registers and delete into the black hole.",
            },
            "drills": [
                {
                    "h2": "Self-correcting macros",
                    "intro": "Build macros that work regardless of cursor position. Start each one at a known position: `0`, `^`, `$` or a search.",
                    "blocks": [K("A macro that finds its own anchor", SELF_CORRECT)],
                },
                {
                    "h2": "Recursive macros",
                    "intro": "A macro that calls itself stops automatically when a motion fails, such as `j` at the last line or `f:` with no colon.",
                    "blocks": [K("Record a recursive macro", RECURSIVE)],
                },
                {
                    "h2": "Edit a macro and save it back",
                    "intro": "Paste the macro, edit the text, yank it back. Then `@q` runs the edited macro.",
                    "blocks": [
                        K("Macro to register, edit, save back", MACRO_EDIT),
                        K("Parallel macro application (visual)", MACRO_VISUAL),
                    ],
                },
                {
                    "h2": "Tag every order as reviewed, two ways",
                    "intro": "`RAW_ORDERS` in `src/orders.py` has exactly 6 entries (`A1` to `A6`). Append `  # reviewed` to each.",
                    "blocks": [
                        K("Macro way", [
                            ("qa", "Cursor on the `A1` line: start recording into register a"),
                            ("A  # reviewed", "End of line, type the comment, Esc"),
                            ("j", "Down to the `A2` line"),
                            ("q", "Stop. `A1` is tagged; `A2` is queued up"),
                            ("5@a", "Replay exactly 5 times, one per remaining line"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Every entry from `A1` to `A6` ends with `# reviewed`."}),
                        K("Visual way", [
                            ("u", "Undo everything first"),
                            ("qa", "Record again on the `A1` line"),
                            ("A  # reviewed", "End of line, type the comment, Esc"),
                            ("q", "Stop; no `j` this time"),
                            ("Vjjjjj", "Select all 6 lines"),
                            (":normal @a", "Run the macro on each selected line"),
                        ], **{"try": "Same result, different technique.",
                              "expect": "`<Space>sg \"# reviewed\"` returns 6 hits. Discard with `:e!`: Lesson 6 depends on the exact structure of `orders.py`."}),
                    ],
                },
                {
                    "h2": "Expression register",
                    "intro": "Calculate in the editor.",
                    "blocks": [
                        K("In insert mode", EXPR_INSERT, **{"try": "In insert mode press `Ctrl-r =`, type `5 * 42`, then Enter.", "expect": "`210` is inserted."}),
                        K("In normal mode", EXPR_NORMAL),
                    ],
                },
                {
                    "h2": "Append, black hole and filename registers",
                    "intro": "Lowercase registers overwrite. Uppercase appends. Use the black hole to delete without overwriting a yank.",
                    "blocks": [
                        K("Append to registers (uppercase)", APPEND),
                        K("The black hole register", BLACK_HOLE),
                        K("The filename registers", FILENAME),
                        K("Collect both TODOs into one place", [
                            ("gg", "Top of `data/log.txt`"),
                            ("/# TODO", "Then Enter: the first of 2 TODO comment lines"),
                            ("\"ayy", "Yank it into register a (overwrites)"),
                            ("n", "Jump to the second `# TODO` line"),
                            ("\"Ayy", "Append it to register a"),
                            (":enew", "Open a blank scratch buffer"),
                            ("\"ap", "Paste both TODO lines at once"),
                        ]),
                        X("Check register a before pasting", ":reg a", "Register a holds both TODO lines together, in file order."),
                        K("Prove the black hole keeps your yank", [
                            ("yy", "In `src/messy.py`, on the `def summarize(items):` line"),
                            ("\"_dd", "Move to a different line and delete it"),
                            ("p", "Pastes `def summarize(items):`, not the deleted line"),
                            ("u", "Twice, to restore `messy.py`"),
                            (":bd!", "Close the scratch buffer without saving"),
                        ], **{"try": "`\"_dd` never touched the default register.",
                              "expect": "The paste is `def summarize(items):`, not the line you just deleted."}),
                    ],
                },
                {
                    "h2": "The command-line window",
                    "intro": "Press `q:` to open command history as an editable buffer. Navigate with `j` and `k`, edit a command and press Enter to run it.",
                    "blocks": [
                        K("Command-line window", CMDLINE_WIN),
                        K("Rerun an edited command from history", [
                            (":echo \"first\"", "Run it, then run `:echo \"second\"`"),
                            ("q:", "Open the command-line window"),
                            ("k", "Up to the `:echo \"first\"` line"),
                            ("ci\"", "Change `\"first\"` to `\"third\"`, then Enter"),
                        ], **{"try": "Press the keys in order in any buffer.",
                              "expect": "The message area shows `third`, and `:messages` shows all three echoes in order: `first`, `second`, `third`."}),
                    ],
                },
            ],
            "rules": {
                "h2": "Registers at a glance",
                "cards": [
                    ("Register recipes", "Pick the register that fits the job.", ["I want to", "Use"], [
                        ["Collect lines from different places", "`\"Ayy` after `\"ayy`"],
                        ["Delete without losing my yank", "`\"_dd` or `\"_diw`"],
                        ["Paste the current filename", "`\"%p`"],
                        ["Calculate in a line", "`Ctrl-r =`"],
                    ]),
                    ("Macro habits", "Rules that keep macros reliable.", ["Habit", "Why"], [
                        ["Start at `0`, `^`, `$` or a search", "A known position makes it repeatable"],
                        ["End with `j` and `@a`", "It stops when a motion fails"],
                        ["Edit as text with `\"qp`", "Fix a macro without re-recording"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Append two lines to one register",
                "frame": "You want two TODO lines in one place.",
                "given": "`data/log.txt` is open.",
                "steps": [
                    "Find the first TODO and press `\"ayy`.",
                    "Press `n` to jump to the second one.",
                    "Press `\"Ayy` to append.",
                    "Run `:enew`, then `\"ap` to paste both.",
                ],
                "meaning": "Register `a` collected lines from two places in file order.",
            },
            "practice": {
                "h2": "Practice: macros and registers",
                "qs": [
                    ("Mechanism", "Why does a recursive macro stop on its own?",
                     "What happens when a motion has nowhere to go?",
                     ["`j` fails at the last line.", "A failed motion aborts the macro."],
                     "A failing motion ends it."),
                    ("Keystrokes", "Append the current line to register a.",
                     "Capital letter appends.",
                     ["Press `\"Ayy`."],
                     "`\"Ayy`."),
                    ("Application", "Run macro a on six selected lines.",
                     "Visual select, then an ex command.",
                     ["Select with `V5j`.", "Run `:normal @a`."],
                     "`V5j`, then `:normal @a`."),
                    ("Common mistake", "You deleted a line and lost the text you yanked. What next time?",
                     "Use a register that nothing reads.",
                     ["Delete into the black hole."],
                     "Use `\"_dd`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Quickfix, marks, substitution and :g",
            "subtitle": "Work on every match in the project, bookmark files and rewrite text with regex.",
            "idea": (
                "Collect locations once, then act on all of them.",
                [
                    ("Send to quickfix", "Ctrl-q", "Pick results into a list."),
                    ("Run on every entry", ":cdo s/a/b/g", "Replace across the list."),
                    ("Global bookmark", "mA", "Mark a file and line."),
                    ("Act on matching lines", ":g/pattern/d", "Delete every line that matches."),
                ],
                None,
            ),
            "problem": {
                "fail": "You change one file at a time, and a regex rewrite touches lines you wanted to keep.",
                "fix": "Collect matches in quickfix, bookmark files with marks and scope substitution with ranges and `:g`.",
            },
            "drills": [
                {
                    "h2": "Quickfix and location lists",
                    "intro": "Quickfix holds project-wide results. The location list is buffer-local.",
                    "blocks": [
                        K("Quickfix", QUICKFIX),
                        {"type": "text", "body": "The power workflow: `<Space>/` to grep, `Ctrl-q` to send all results to quickfix, `:cdo s/old/new/g | w` to replace across all files, or `:cfdo %s/old/new/g | w` for the same per file (faster)."},
                        K("Location list", LOCLIST),
                        K("Find every TODO via quickfix", [
                            ("<Space>/", "Or `<Space>sg`: search for `TODO`"),
                            ("Ctrl-q", "Send every hit to the quickfix list"),
                            (":copen", "See them all in one window"),
                            ("]q", "Step through the results, with `[q` back; Enter on a line jumps to it"),
                            (":cclose", "Close it when done"),
                        ], **{"try": "You always get the 2 `# TODO` lines in `data/log.txt` and 2 hits in `scripts/dirty.patch` (the reset script's patch carries the same text). Depending on Lesson 6, you may also see the rename TODO and the `average()` TODO.",
                              "expect": "The quickfix title bar shows a match count equal to what `<Space>sg TODO` reported."}),
                    ],
                },
                {
                    "h2": "Marks: expert patterns",
                    "intro": "Vim sets the auto-marks for you. Use A to D for your four most-used files.",
                    "blocks": [
                        K("Auto-marks", AUTO_MARKS),
                        K("Mark + operate pattern", MARK_OPERATE),
                        K("Global marks (cross-file bookmarks)", GLOBAL_MARKS),
                        K("Bookmark two files, then jump blind", [
                            ("mA", "In `src/calculator.py`, on `class Person:`"),
                            ("mB", "In `src/orders.py`, on `class OrderBook:`"),
                            ("'A", "From an unrelated file such as `README.md`: lands on `class Person:`"),
                            ("'B", "Jumps straight to `class OrderBook:`"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "You land in `orders.py` on the `OrderBook` line without typing a single filename."}),
                        K("The local pattern (destructive: undo at once)", [
                            ("ma", "In `calculator.py`, on `class Person:`"),
                            ("G", "Jump to the end of the file"),
                            ("d`a", "Deletes everything from the end back to the mark: the whole `Person` class"),
                            ("u", "Immediately restore it"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "`Person` is back. Confirm with `<Space>sg \"class Person\"`."}),
                    ],
                },
                {
                    "h2": "Advanced substitution",
                    "intro": "Groups, case modifiers, expressions and ranges.",
                    "blocks": [
                        K("Regex groups and backreferences", REGEX_GROUPS),
                        K("Case-modifying substitution", CASE_SUB),
                        K("Substitute with expression", EXPR_SUB),
                        K("Range modifiers", RANGE_MOD),
                        X("Rename a field with one regex", r":%s/item \(\d\+\)/entry \1/g", "Every `item N` becomes `entry N`, keeping the right number on each line."),
                        X("Count the matches without replacing", ":%s/item//gn\n:%s/entry//gn", "The first reports 0 matches and the second reports 10. `entry 7` still says `entry 7`: the backreference kept the number."),
                        {"type": "text", "body": "Do not check with `<Space>sg item`. That greps the whole project, and `orders.py` and `messy.py` legitimately use `item` as a variable name. Run `:e!` to discard."},
                        X("Title-case one line only", r":'<,'>s/\<\(\w\)/\u\1/g", "Select the `keep: this line matches a filter pattern` line with `V` first. It reads `Keep: This Line Matches A Filter Pattern` and every other line is unchanged. `:e!` to discard."),
                    ],
                },
                {
                    "h2": "The :global command",
                    "intro": "Operate on all lines matching a pattern. `:v` is the inverse.",
                    "blocks": [
                        K("Global commands", GLOBAL),
                        X("Strip TODOs and blank lines", ":g/TODO/d\n:g/^$/d", "The first deletes both `# TODO` comment lines in one shot. The second deletes every blank line (there are 3). Press `u` after each to bring them back.", where="nvim"),
                        X("Flip it around on a scratch copy", ":w /tmp/log-copy.txt\n:e /tmp/log-copy.txt\n:v/keep/d", "The copy has exactly 3 lines, all starting with `keep:`. Close it with `:bd!`: you never touched the real `data/log.txt`."),
                    ],
                },
            ],
            "rules": {
                "h2": "Lists, marks and regex at a glance",
                "cards": [
                    ("Collect then act", "Pick the scope first.", ["Scope", "Command"], [
                        ["Every quickfix entry", "`:cdo s/old/new/g | w`"],
                        ["Every quickfix file", "`:cfdo %s/old/new/g | w`"],
                        ["Lines matching a pattern", "`:g/pattern/d`"],
                        ["Lines not matching", "`:v/pattern/d`"],
                    ]),
                    ("Mark types", "Lowercase is per file, uppercase is global.", ["Key", "Does"], [
                        ["`ma`", "Mark in this file"],
                        ["`mA`", "Mark across files"],
                        ["`'A`", "Jump to the file and line of mark A"],
                    ]),
                    ("Stay safe", "These drills are throwaway.", ["Situation", "Undo with"], [
                        ["After a substitution", "`u` or `:e!`"],
                        ["After `:v/keep/d`", "Work on a `/tmp` copy"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Replace across files, reviewed",
                "frame": "You need one rename in every file that mentions it.",
                "given": "You are in `nvim-drills`.",
                "steps": [
                    "Press `<Space>/` and search for the text.",
                    "Press `Ctrl-q` to send every hit to quickfix.",
                    "Run `:copen` and check each hit.",
                    "Run `:cdo s/old/new/g | w`.",
                ],
                "meaning": "You reviewed the list before changing anything.",
            },
            "practice": {
                "h2": "Practice: lists, marks and substitution",
                "qs": [
                    ("Mechanism", "What is the difference between `ma` and `mA`?",
                     "Case decides the scope.",
                     ["Lowercase is local to the file.", "Uppercase remembers the file."],
                     "`mA` is a global mark across files."),
                    ("Keystrokes", "Delete every empty line.",
                     "Use `:g` with an anchor pattern.",
                     ["Run `:g/^$/d`."],
                     "`:g/^$/d`."),
                    ("Application", "Keep only the lines that contain `keep`.",
                     "The inverse of `:g`.",
                     ["Run `:v/keep/d`, on a copy."],
                     "`:v/keep/d`."),
                    ("Common mistake", "Why do the drill use a `/tmp` copy for `:v/keep/d`?",
                     "What does it delete?",
                     ["It deletes everything that does not match.", "That includes all the item lines."],
                     "It would wreck the real file."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Windows, insert, block, ranges and undo",
            "subtitle": "The arglist, insert tricks, block editing, ex ranges and the undo tree.",
            "idea": (
                "The last techniques: edit many files, columns and time itself.",
                [
                    ("Arglist", ":args src/*.py", "Load a set of files."),
                    ("Column edit", "Ctrl-v", "Block-select a column."),
                    ("Duplicate line", ":t.", "Copy the line below itself."),
                    ("Go back in time", ":earlier 5m", "Return to the file 5 minutes ago."),
                ],
                None,
            ),
            "problem": {
                "fail": "You open files one by one, edit columns line by line and undo one step at a time.",
                "fix": "Load files with `:args`, edit columns with `Ctrl-v` and travel through time with `:earlier` and `g-`.",
            },
            "drills": [
                {
                    "h2": "Window and buffer expert",
                    "intro": "Tabs in vim are layouts (arrangements of splits), not files. Use buffers for files.",
                    "blocks": [
                        K("Argument list", ARGS),
                        K("Buffer tricks", BUFFER_TRICKS),
                        K("Tab pages (for layouts, not files)", TABS),
                        K("Load the whole src/ folder as an arglist", [
                            (":args src/*.py", "Loads every `.py` directly under `src/`: the four real modules plus the empty `__init__.py` (and `scratch.py` if the git drills made it)"),
                            (":args", "No arguments: prints the list with the current file bracketed"),
                            (":next", "Step forward, with `:prev` to go back"),
                            ("Ctrl-^", "After two files: toggle back to the one you were just on"),
                        ], **{"try": "Run it from inside `nvim-drills`. Globs grab everything that matches, so curating is on you.",
                              "expect": "`:args` again shows the same list with `[ ]` around whichever file you are viewing."}),
                    ],
                },
                {
                    "h2": "Insert mode: expert",
                    "intro": "Completion and one-off commands without leaving insert mode.",
                    "blocks": [
                        K("Auto-completion", COMPLETE),
                        K("Insert mode tricks", INSERT_TRICKS),
                        K("Delete a line mid-sentence", [
                            ("A", "At the end of `total = 0` inside `summarize()` in `src/messy.py`"),
                            ("Ctrl-o dd", "Deletes the current line and drops you back into insert mode"),
                            ("Esc", "Leave insert mode"),
                            ("u", "Restore the line: this drill is throwaway"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Right after `Ctrl-o dd`, `total = 0` is gone and you never left insert mode: no flicker to NORMAL."}),
                    ],
                },
                {
                    "h2": "Visual block: expert",
                    "intro": "Column editing.",
                    "blocks": [
                        K("Column editing", BLOCK_COLUMN),
                        K("Add incrementing numbers", BLOCK_SEQ),
                        K("Or with a start value", BLOCK_SEQ2),
                        K("Align text with block mode", BLOCK_ALIGN),
                        K("Reset a run of numbers, then regenerate them", [
                            ("Ctrl-v", "On the `7` in `item 7: pending` in `data/log.txt`"),
                            ("2j", "Extend down 2 rows to cover `7`, `8` and `9` as a one-wide column"),
                            ("r0", "Every character in the block becomes `0`"),
                            ("gv", "Reselect the same block"),
                            ("g Ctrl-a", "Increments line 1 by 1, line 2 by 2, line 3 by 3"),
                        ], **{"try": "Leave `item 10` out of the column, since it has two digits.",
                              "expect": "The three lines read `item 1: pending`, `item 2: pending`, `item 3: pending`: each line got a different increment. `:e!` to discard."}),
                    ],
                },
                {
                    "h2": "Ex commands and ranges",
                    "intro": "Ranges say where, ex commands say what.",
                    "blocks": [
                        K("Range syntax", RANGE_SYNTAX),
                        K("Useful ex commands", EX_USEFUL),
                        K("Duplicate an order, then relocate it", [
                            (":t.", "On the `A1` line in `RAW_ORDERS`: two identical `A1` entries"),
                            (":m$", "Moves the duplicate to the very end of the file, past `build_order_book()`"),
                            ("G", "Jump to the end of the file"),
                            (":e!", "Discard both changes"),
                        ], **{"try": "Press the keys in order. `:m$` operates on the whole buffer, not the enclosing structure.",
                              "expect": "The duplicated `A1` dict literal is the last line in `orders.py`, outside the list and outside `build_order_book()`. After `:e!`, `<Space>sg \"id.*A1\"` shows only 1 hit."}),
                    ],
                },
                {
                    "h2": "Performance tricks",
                    "intro": "Small habits with large payoffs.",
                    "blocks": [
                        K("Jump without adding to the jump list", JUMP_LIST),
                        K("Quick file switching", QUICK_SWITCH),
                        K("Quickly fix and move on", FIX_MOVE),
                        K("The number trick", NUMBER_TRICK),
                        {"type": "text", "body": "On dates, versions and port numbers, the number trick is an instant update."},
                        K("Bounce between two files with zero typing", [
                            ("<Space>sf", "Type `calculator`, Enter: open `src/calculator.py`"),
                            ("<Space>sf", "Open `src/orders.py` the same way"),
                            ("Ctrl-^", "Back to `calculator.py` instantly"),
                            ("Ctrl-^", "Back to `orders.py`"),
                        ], **{"try": "Nothing to undo: this is pure navigation.",
                              "expect": "Each `Ctrl-^` flips between the two files, faster than a fuzzy search."}),
                    ],
                },
                {
                    "h2": "Undo: expert",
                    "intro": "Vim's undo is a tree, not a line. If you undo and make new changes, the old changes are a branch, and `g-` and `g+` walk the whole tree. Undo history is already persistent: it survives quitting Neovim.",
                    "blocks": [
                        K("Undo tree", UNDO_TREE),
                        {"type": "text", "body": "This is the one exercise in this lesson that writes to disk, because `:earlier` and `:later` with an `f` count are save-based."},
                        K("Time-travel through 3 saved states", [
                            (":w", "In `src/messy.py`: add `# checkpoint 1` at the top, then save. Repeat for `# checkpoint 2` and `# checkpoint 3`"),
                            (":earlier 2f", "Back 2 saves: only `# checkpoint 1` is present"),
                            (":later 1f", "Forward 1 save: `# checkpoint 2` reappears"),
                            ("g-", "A few times, then `g+`: walk one micro-change at a time"),
                        ], **{"try": "At each step run `:%s/checkpoint//gn` (count only). Do not use `<Space>sg checkpoint`: ripgrep reads the file on disk.",
                              "expect": "The match count equals the checkpoint number you are at."}),
                        X("Restore messy.py (required, it saved to disk)", "git checkout -- src/messy.py", "`src/messy.py` is back to its committed state. `:e!` alone would not help, since the dirty state is already on disk. From inside nvim use `:!git checkout -- %`.", where="shell"),
                    ],
                },
            ],
            "rules": {
                "h2": "The expert cheat sheet",
                "cards": [
                    ("Cheat sheet — expert edition", "Intent on the left, keys on the right.", ["Intent", "Keys"], [
                        ["Delete until pattern", "`d/pattern`"],
                        ["Change until char", "`ct{char}`"],
                        ["Repeat last search+change", "`cgn` then `.`"],
                        ["Delete without affecting clipboard", "`\"_dd`"],
                        ["Append to register", "`\"Ayy`"],
                        ["Run macro on visual selection", "`:'<,'>normal @a`"],
                        ["Increment numbers in column", "`Ctrl-v` select → `g Ctrl-a`"],
                        ["Execute command from insert mode", "`Ctrl-o {cmd}`"],
                        ["Calculate in insert mode", "`Ctrl-r = 5*42 Enter`"],
                        ["Delete all lines matching pattern", "`:g/pattern/d`"],
                        ["Keep only lines matching pattern", "`:v/pattern/d`"],
                        ["Copy all matches to end of file", "`:g/pattern/t$`"],
                        ["Sort visual selection", "`:'<,'>!sort`"],
                        ["Go back in time", "`:earlier 5m`"],
                        ["Duplicate line", "`:t.` or `yyp`"],
                        ["Move line to end", "`:m$`"],
                        ["Open last 2 files alternating", "`Ctrl-^`"],
                        ["Capitalize first letters", r"`:%s/\<\w/\u&/g`"],
                    ]),
                    ("Undo or discard?", "Which one depends on whether the change reached the disk.", ["Situation", "Use"], [
                        ["Nothing saved", "`u` or `:e!`"],
                        ["Saved to disk", "`git checkout -- src/messy.py`"],
                        ["Between saves", "`:earlier 2f` or `:later 1f`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Number a column of items",
                "frame": "Three lines need to read 1, 2, 3.",
                "given": "`data/log.txt` shows `item 7`, `item 8` and `item 9`.",
                "steps": [
                    "Put the cursor on the `7` and press `Ctrl-v`, then `2j`.",
                    "Press `r0` to zero the column.",
                    "Press `gv` to reselect the same block.",
                    "Press `g Ctrl-a`, then `:e!` to discard.",
                ],
                "meaning": "Each line received a different increment, so the numbers became a sequence.",
            },
            "practice": {
                "h2": "Practice: windows, insert, block and undo",
                "qs": [
                    ("Mechanism", "What is the difference between `u` and `:earlier 2f`?",
                     "One counts changes, one counts saves.",
                     ["`u` undoes the last change.", "`:earlier 2f` jumps back 2 file saves."],
                     "`:earlier 2f` travels by save, not by change."),
                    ("Keystrokes", "Delete a line from insert mode without leaving it.",
                     "One normal command.",
                     ["Press `Ctrl-o`.", "Press `dd`."],
                     "`Ctrl-o dd`."),
                    ("Application", "Duplicate the current line and move the copy to the end of the file.",
                     "Two ex commands.",
                     ["Run `:t.`.", "Run `:m$`."],
                     "`:t.` then `:m$`."),
                    ("Common mistake", "You restored a file with `:e!` after `:w` and nothing changed. Why?",
                     "Where is the dirty state now?",
                     ["`:w` already wrote it to disk.", "`:e!` reloads from disk."],
                     "Use `git checkout -- src/messy.py`."),
                ],
            },
        },
    ],
}
