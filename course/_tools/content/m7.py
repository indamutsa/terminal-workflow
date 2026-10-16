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
2ci"             Change the text inside the 2nd pair of quotes
d/pattern        Delete everything up to a search match
c/foo            Change everything up to "foo"
y?bar            Copy (yank) backwards up to "bar"
'''

OP_SEARCH = r'''
d/function       Delete everything from the cursor up to "function"
c/return         Change everything from the cursor up to "return"
y/class          Copy (yank) from the cursor up to "class"
v/end            Select from the cursor up to "end"
'''

TILL = r'''
dt)              Delete up to the ) and keep the )
ct,              Change up to the next comma
yt:              Copy (yank) up to the colon
vt"              Select up to the quote
df)              Delete up to and including the ) (f lands on the character, t stops before it)
'''

RELATIVE = r'''
d5j              Delete from here down 5 lines
y3k              Copy (yank) from here up 3 lines
>8j              Indent 9 lines (current line + 8 below)
gq5j             Reformat 6 lines
v5j              Select 6 lines
'''

MINI_AI = r'''
cin)             Change the text inside the next parentheses (the cursor can be outside them)
cil)             Change the text inside the previous parentheses
c2i{             Change the text inside the 2nd enclosing braces
d2a"             Delete the 2nd enclosing quotes, quotes included
'''

TS_ARGS = r'''
cia              Change one function argument
daa              Delete an argument and its comma
via              Select one argument
'''

DOT = r'''
/pattern         Search for the text you want to change
cgn              Change the next match (c + gn motion)
.                Repeat the change on the next match
.                Repeat it on the one after
n                Skip a match (leave it unchanged)
.                Change this one
'''

BAD = r'''
f"ldt"           (several motions: . repeats only dt")
'''

GOOD = r'''
ci"              (one operation: . repeats the whole change)
'''

SELF_CORRECT = r'''
qa               Start recording
0                Go to the start of the line (a known position)
f:               Jump to the colon (the anchor point)
l                Move right
dw               Delete a word
A,               Add a comma at the end of the line
j                Go to the next line
q                Stop recording
'''

RECURSIVE = r'''
qqq              Empty register q first
qa               Start recording into register a
0f:ldwA,Escj@aq  Do the work, move down, call @a, stop recording
@a               Run it on all remaining lines
'''

MACRO_EDIT = r'''
"qp              Paste the macro from register q as text
                 (edit the text)
0"qy$            Copy the edited line back into register q
dd               Delete the temporary line
'''

MACRO_VISUAL = r'''
V5j              Select 6 lines
:normal @a       Run macro 'a' on each selected line
'''

EXPR_INSERT = r'''
Ctrl-r =         Open the expression register (calculate in insert mode)
5 * 42 Enter     Insert "210"
system('date')   Insert the current date
'''

EXPR_NORMAL = r'''
"=5*42p          Paste the result of a calculation
'''

APPEND = r'''
"ayy             Copy the line into register a (replaces what was there)
"Ayy             Add another line to register a
"ap              Paste all the lines collected in register a
'''

BLACK_HOLE = r'''
"_dd             Delete a line without touching any register
"_diw            Delete a word and keep what you copied
'''

FILENAME = r'''
Ctrl-r %         Insert the current file name (in insert mode)
Ctrl-r #         Insert the other (alternate) file name
"%p              Paste the current file name (in normal mode)
'''

CMDLINE_WIN = r'''
q:               Open the command-line window (edit and rerun old commands)
q/               Open the search history window
Ctrl-f           Switch from the : prompt to the command-line window
'''

QUICKFIX = r'''
:copen           Open the quickfix window
:cclose          Close the quickfix window
:cnext / :cprev  Go to the next / previous item (or ]q / [q)
:cfirst / :clast Jump to first / last
:cdo s/a/b/g     Run a command on every quickfix entry
'''

LOCLIST = r'''
:lopen           Open the location list
:lclose          Close the location list
:lnext / :lprev  Go to the next / previous item
'''

AUTO_MARKS = r'''
`.               Jump to where you last edited
`^               Jump to where you last left insert mode
`[               Jump to the start of the last copy or change
`]               Jump to the end of the last copy or change
`<               Jump to the start of the last visual selection
`>               Jump to the end of the last visual selection
``               Jump back to where you were before the last jump
'''

MARK_OPERATE = r'''
ma               Mark this position
                 (move somewhere else, do stuff)
d`a              Delete from here back to mark a
y`a              Copy (yank) from here to mark a
v`a              Select from here to mark a
'''

GLOBAL_MARKS = r'''
mA               Set global mark A (remembered across files)
'A               Jump to the file and line of mark A
'''

REGEX_GROUPS = r'''
:%s/\(\w\+\)/"\1"/g           Wrap every word in quotes
:%s/\v(\w+)/"\1"/g            Do the same with "very magic" (less escaping)
:%s/foo\(.*\)bar/baz\1qux/g  Keep the middle, change what surrounds it
'''

CASE_SUB = r'''
:%s/\<\(\w\)/\u\1/g          Capitalize the first letter of every word
:%s/.*/\L&/g                  Lowercase the whole file
:%s/.*/\U&/g                  Uppercase the whole file
:%s/\<\w/\u&/g               Make every word Title Case
'''

EXPR_SUB = r'''
:%s/\d\+/\=submatch(0)+1/g   Add 1 to every number
:%s/\d\+/\=printf("%03d",submatch(0))/g  Zero-pad every number
'''

RANGE_MOD = r'''
:5,10s/a/b/g     Replace only on lines 5-10
:'<,'>s/a/b/g    Replace only in the visual selection (filled in when you type : in visual mode)
:.,$s/a/b/g      Replace from the current line to the end of the file
:.,+5s/a/b/g     Replace on the current line and the next 5
:g/pattern/d     Delete all lines that match a pattern
:v/pattern/d     Delete all lines that do NOT match a pattern
'''

GLOBAL = r'''
:g/TODO/d              Delete all lines with "TODO"
:g/^$/d                Delete all empty lines
:g/pattern/normal A;   Add ";" to the end of all matching lines
:g/import/t$           Copy all import lines to the end of the file
:g/def /normal O       Add a blank line above each function
:v/keep/d              Delete all lines that do NOT contain "keep"
:g/pattern/m0          Move all matching lines to the top
'''

ARGS = r'''
:args **/*.py          Load all Python files into the argument list
:args `git diff --name-only`  Load only the changed files
:argdo %s/old/new/g | w       Replace in every file of the list and save
:next / :prev          Go to the next / previous file in the list
'''

BUFFER_TRICKS = r'''
:b#               Switch to the last buffer (alternate file)
Ctrl-^            Do the same as :b#, faster
:bufdo            Run a command in every open buffer
:ball             Open all buffers in splits
:tab ball         Open all buffers in tabs
'''

TABS = r'''
:tabnew          Open a new tab page
:tabclose        Close the tab page
gt / gT          Go to the next / previous tab page
:tabmove 0       Move the current tab to the first position
'''

COMPLETE = r'''
Ctrl-n           Complete with the next match (from the buffer, tags and more)
Ctrl-p           Complete with the previous match
Ctrl-x Ctrl-f    Complete a file name
Ctrl-x Ctrl-l    Complete a whole line
Ctrl-x Ctrl-o    Complete with LSP (omni-completion)
'''

INSERT_TRICKS = r'''
Ctrl-o {cmd}     Run one normal-mode command without leaving insert mode
                 e.g., Ctrl-o dd = delete the line, stay in insert mode
Ctrl-r =         Calculate and insert the result
Ctrl-r "         Paste from the default register
Ctrl-r 0         Paste what you last copied (yank register)
Ctrl-r %         Paste the current file name
Ctrl-a           Insert the text you last inserted again
Ctrl-w           Delete the word before the cursor
Ctrl-u           Delete back to the start of the line
Ctrl-t           Indent the current line
Ctrl-d           Unindent the current line
'''

BLOCK_COLUMN = r'''
Ctrl-v           Start block (column) mode
jjjj             Select a column
I                Insert before the column (applies to all lines after Esc)
A                Add text after the column
c                Change the column
r{char}          Replace the column with one character
d                Delete the column
>                Indent the selected block
'''

BLOCK_SEQ = r'''
Ctrl-v jjjj      Select 5 lines
g Ctrl-a         Number the lines 1,2,3,4,5
'''

BLOCK_SEQ2 = r'''
Ctrl-v jjjj      Select 5 lines
I0 Esc           Insert "0" on every line
gv               Select the same block again
g Ctrl-a         Number the lines 1,2,3,4,5
'''

BLOCK_ALIGN = r'''
Ctrl-v           Start block mode
jjj              Select the rows
$                Extend to the end of each line (ragged selection)
A                Add text at the end of each line
'''

RANGE_SYNTAX = r'''
.                The current line
$                The last line
%                The whole file (same as 1,$)
'<,'>            The visual selection
.,.+5            The current line and the next 5
'a,'b            From mark a to mark b
/pat1/,/pat2/    From the first pattern to the second
'''

EX_USEFUL = r'''
:t.              Duplicate the current line (copy it here)
:t5              Copy the current line to after line 5
:m$              Move the current line to the end of the file
:m0              Move the current line to the top
:5,10m$          Move lines 5-10 to the end
:5,10t.          Copy lines 5-10 to the current position
:read !ls        Insert the output of a shell command below the cursor
:read file.txt   Insert the contents of a file below the cursor
:.!sort          Run the current line through the shell sort command
:'<,'>!sort      Sort the selected lines
'''

JUMP_LIST = r'''
Ctrl-d / Ctrl-u      Scroll without adding to the jump list (good for browsing)
gg / G / /pattern    Add to the jump list (good for deliberate jumps)
'''

QUICK_SWITCH = r'''
Ctrl-^               Switch between the last two files (the fastest way)
<Space><Space>       Find a file by name in a file picker (the buffer list is `<Space>,`)
:b partial_name      Switch to a buffer by part of its name
'''

FIX_MOVE = r'''
ciw → type → Esc → n → .    Fix the same pattern across the file
*cwreplacement Esc n.n.n.    Replace a word everywhere (review each one)
'''

NUMBER_TRICK = r'''
Ctrl-a           Add 1 to the number under the cursor
Ctrl-x           Subtract 1
5 Ctrl-a         Add 5 to the number
'''

UNDO_TREE = r'''
:earlier 5m      Go back to the file as it was 5 minutes ago
:later 2m        Go forward 2 minutes
:earlier 3f      Go back 3 saves
g-               Go to an older state in the undo tree
g+               Go to a newer state in the undo tree
'''

MODULE = {
    "n": 7,
    "folder": "m7-expert",
    "title": "Edit faster in Neovim: repeat, macros, undo",
    "footer": "Repeat edits with the dot, record macros, use registers, quickfix, marks and :g, edit columns and undo by time",
    "tagline": "Repeat an edit, record macros, change every match in a project and go back in time.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Repeat an edit on every match in Neovim",
            "subtitle": "Change the 2nd quoted string, delete up to a word, change up to a comma, change every match one by one, repeat the last change",
            "idea": (
                "Repeat an edit with one key: shape the change so `.` can run it again.",
                [
                    ("Change the 2nd quoted string", "2ci\"", "Change the text inside the 2nd pair of quotes."),
                    ("Delete up to a word", "d/pattern", "Delete everything up to the match."),
                    ("Change every match one by one", "cgn", "Change the next match, then press `.`."),
                    ("Repeat the last change", ".", "Run the last change again."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I change the same text in many places without retyping it? You count characters, hold `l` and retype the same change at every match.",
                "fix": "Land exactly with counts, searches and till-motions, then use `cgn` and `.` to repeat the change.",
            },
            "drills": [
                {
                    "h2": "Open the Neovim practice project",
                    "intro": "How do I try these drills safely? Every drill runs against `nvim-drills`. These are throwaway reps: undo with `u` once you have seen the mechanic work. Autosave writes a file about 3 seconds after you stop typing, and when you leave the buffer, so `:e!` cannot bring the original back. For a drill that must stay unsaved, run `:ASToggle` first and again after it. To reset one file, run `git checkout -- <file>`. Lesson 6 makes the permanent fixes, but none of these drills depend on it.",
                    "blocks": [
                        X("Open Neovim in the practice project (nvim-drills)", "cd Terminal-Workflow/practice/nvim-drills\nnvim .", "Neovim opens on the project, ready for the drills.", "shell"),
                    ],
                },
                {
                    "h2": "Repeat a command with a count (3dw, 5j, 2ci\")",
                    "intro": "Add a count to almost any command.",
                    "blocks": [
                        K("Delete, move or change several times with a count", COUNT),
                        PY("Look at the A4 line: it has six quoted strings", '''
{"id": "A4", "items": [{"price": 8, "qty": 3}], "discount": 2},
'''),
                        K("Change the 2nd quoted string on a line", [
                            ("2ci\"", "Put the cursor before the first `\"` on the A4 line: jump to the 2nd quoted string (`\"A4\"`) and start insert mode"),
                            ("A4-REVIEW", "Type it, then press Esc"),
                            ("u", "Undo"),
                            ("3dw", "From the start of the line: delete 3 words (punctuation runs like `{\"` count as words)"),
                            ("u", "Undo"),
                        ], **{"try": "Open `src/orders.py` and find the `RAW_ORDERS` list.",
                              "expect": "After the `2ci\"` step, before undoing, the line reads `{\"id\": \"A4-REVIEW\", \"items\": ...}`: only the second quoted string changed, not `\"id\"`."}),
                    ],
                },
                {
                    "h2": "Delete or change up to a search match (d/pattern)",
                    "intro": "A search only deletes text when you give it to an operator.",
                    "blocks": [
                        K("Delete, change or copy up to a search match", OP_SEARCH),
                        K("Jump to a method by searching for its name", [
                            ("gg", "Go to line 1 of `src/calculator.py`"),
                            ("d/def divide", "Delete from the top up to the start of `divide`"),
                            ("u", "Undo at once"),
                            ("/def divide", "Then press Enter: this only moves the cursor"),
                        ], **{"try": "Run the keys in order. `y/def divide` Enter is the halfway house: it yanks the range `d/` would delete, but the cursor stays put.",
                              "expect": "The cursor sits on the `d` of `def divide`, and nothing changed on disk."}),
                    ],
                },
                {
                    "h2": "Change up to a character, not including it (t and T)",
                    "intro": "Stop before a character with `t`, or land on it with `f`.",
                    "blocks": [
                        K("Delete or change up to a comma, quote or bracket", TILL),
                        PY("Look at the line in build_order_book()", '''
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
'''),
                        K("Replace one function argument", [
                            ("ct,", "Put the cursor on the `r` of the first `raw[\"id\"]`: change up to the next comma"),
                            ("raw.get(\"id\")", "Type it, then press Esc"),
                            ("u", "Undo"),
                        ], **{"try": "Swap a dict-index for a `.get()` call in three keystrokes plus typing.",
                              "expect": "Before undoing, the line reads `book.add_order(Order(raw.get(\"id\"), raw[\"items\"], raw[\"discount\"]))`: only the first argument changed."}),
                    ],
                },
                {
                    "h2": "Delete or copy several lines with relative line numbers",
                    "intro": "Turn on relative line numbers with `:set relativenumber`. Then you can read each count straight off the screen.",
                    "blocks": [
                        K("Delete, copy, indent or select N lines from here", RELATIVE),
                        K("Delete the lines of a list with a count", [
                            (":set relativenumber", "In `src/orders.py`, put the cursor on the `RAW_ORDERS = [` line"),
                            ("j", "Move to the `\"A1\"` entry"),
                            ("d5j", "Delete `A1` plus the next 5 (`A2` to `A6`); the brackets stay"),
                            ("u", "Undo right away: this only proves the count math"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Right before undoing, `RAW_ORDERS` is an empty list body (`[` then `]` on adjacent lines). After `u`, all 6 orders are back."}),
                    ],
                },
                {
                    "h2": "Change inside the next or Nth brackets, quotes or argument",
                    "intro": "How do I change inside the 2nd enclosing braces? With mini.ai the count goes before the `i` or `a`: `c2i{`, not `ci2{`. After an operator, vim reads `i{` as a two-character text object, so a digit between them is not a count.",
                    "blocks": [
                        K("Change inside the next, previous or 2nd brackets (mini.ai)", MINI_AI),
                        K("Change, delete or select a function argument (Treesitter)", TS_ARGS),
                        PY("Look at the line in Order.subtotal", '''
return sum(item["price"] * item["qty"] for item in self.items)
'''),
                        PY("Look at the A6 entry: it has two levels of braces", '''
{"id": "A6", "items": [{"price": 3, "qty": 3}, {"price": 3, "qty": 3}], "discount": 0},
'''),
                        PY("Look at the build_order_book() line again", '''
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
'''),
                        K("Edit inside nested brackets and arguments", [
                            ("cin)", "Put the cursor on the `s` of `sum(`: change inside the next parens. Type `x for x in []`, press Esc, then `u`"),
                            ("c2i{", "Put the cursor inside the first `{\"price\": 3, \"qty\": 3}` on the A6 line: target the 2nd enclosing brace. Type `\"REPLACED\"`, press Esc, then `u`"),
                            ("daa", "Put the cursor anywhere inside `raw[\"items\"]`: delete that argument and its trailing comma, then press `u`"),
                        ], **{"try": "Undo after each step.",
                              "expect": "Step 1: `subtotal` briefly returns `sum(x for x in [])`. Step 2: the whole A6 entry collapses to `{\"REPLACED\"},`. Step 3: the constructor call has 2 arguments instead of 3."}),
                    ],
                },
                {
                    "h2": "Repeat a change with the dot (.) and review each match",
                    "intro": "The `.` command repeats the last change. Shape every edit so it can repeat. `cgn` plus `.` beats `:%s` when you want to review each change.",
                    "blocks": [
                        K("Change the next match, then repeat on each match", DOT),
                        K("Bad: a change that . cannot repeat", BAD),
                        K("Good: a change that . repeats whole", GOOD),
                        {"type": "text", "body": "How do I change several matches without multiple cursors? Press `*` to select a word into the search register, `cgn` to change the current match, `.` to apply it to the next, `n` to skip one, `.` to change this one. You get interactive find-and-replace with undo per match."},
                        K("Change 9 of 10 matches and skip one", [
                            ("gg", "Go to the top of `data/log.txt` (ten lines `item 1: pending` to `item 10: pending`)"),
                            ("/pending", "Then press Enter: land on the first match"),
                            ("cgn", "Type `queued`, press Esc"),
                            (".", "Press three times: matches 2, 3 and 4 become `queued`"),
                            ("n", "Press twice to skip match 5: the first `n` lands on it, the second hops to 6"),
                            (".", "Change match 6; keep pressing for the other 4"),
                        ], **{"try": "Press the keys in order. Then press `u` until every line reads `pending` again: other lessons reuse this file.",
                              "expect": "`<Space>sg pending` returns exactly 1 result (the skipped one) and `<Space>sg queued` returns 9."}),
                    ],
                },
            ],
            "rules": {
                "h2": "Choose the keys to change text exactly where you want",
                "cards": [
                    ("Land on the text you want to change", "Pick the motion that starts the change in the right place.", ["I want to", "Use"], [
                        ["Change the Nth quoted string", "`2ci\"`"],
                        ["Delete up to a pattern", "`d/pattern`"],
                        ["Change up to a comma", "`ct,`"],
                        ["Change inside the next parentheses", "`cin)`"],
                        ["Change inside the 2nd enclosing braces", "`c2i{`"],
                    ]),
                    ("Repeat a change on every match", "Change one match, then repeat the same change on the others.", ["Key", "Does"], [
                        ["`/pattern`", "Find the first match"],
                        ["`cgn`", "Change that match"],
                        ["`.`", "Repeat on the next match"],
                        ["`n`", "Skip one match (press twice if the cursor is on the match)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Change most matches and keep one (review each)",
                "frame": "How do I change most `pending` lines and keep one? Review each match.",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (None, "`/pending` `Enter`, then `cgn` `queued` `Esc`", "Change the first match, item 1."),
                    (None, "`.`", "Repeat on the next match, item 2."),
                    (None, "`n` `n`", "Skip item 3, the one to keep."),
                    (None, "`.` then `u` three times", "Change item 4, then undo all three changes. Autosave writes the original back."),
                ],
                "before": "item 1: pending\nitem 2: pending\nitem 3: pending\nitem 4: pending",
                "after": "item 1: queued\nitem 2: queued\nitem 3: pending\nitem 4: queued",
                "meaning": "You choose each change. A blind `:%s` never lets you do that.",
            },
            "practice": {
                "h2": "Check how to repeat a change with counts, till and the dot",
                "qs": [
                    ("Mechanism", "Why do I press `n` twice to skip a match when I use `cgn` and `.`?",
                     "Where is the cursor after the first `n`?",
                     ["The first `n` lands on the match.", "`gn` operates on the match under the cursor, so `.` would change it."],
                     "The second `n` hops over it."),
                    ("Keystrokes", "How do I change the 2nd quoted string on a line?",
                     "Put the count before the object.",
                     ["Press `2ci\"`.", "Type the new text, then press Esc."],
                     "`2ci\"`."),
                    ("Application", "How do I replace an argument up to the next comma?",
                     "Till, not find.",
                     ["Put the cursor on the argument.", "Press `ct,`."],
                     "`ct,`."),
                    ("Common mistake", "I typed `ci2{` instead of `c2i{` and it failed. Why?",
                     "Where does the count go?",
                     ["After an operator `i{` is a two-character object.", "A digit between is not a count."],
                     "The count goes before: `c2i{`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Repeat edits with macros and registers",
            "subtitle": "Record a macro that works on every line, make a macro repeat itself, fix a macro, calculate in the editor, collect lines in one register, delete without losing a copy",
            "idea": (
                "Keep text and macros in registers: edit them, add to them and keep them safe.",
                [
                    ("Record a macro", "qa", "Record a macro into register a."),
                    ("Collect lines from different places", "\"Ayy", "Add a line to register a."),
                    ("Delete without losing what I copied", "\"_dd", "Delete without touching any register."),
                    ("Edit and rerun an old command", "q:", "Open the command history, edit a command and run it."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does my macro work on one line and break on the next? Or a delete overwrites the text I meant to paste.",
                "fix": "Start every macro from a known position, append with capital registers and delete into the black hole.",
            },
            "drills": [
                {
                    "h2": "Record a macro that works on every line",
                    "intro": "Make a macro that works wherever the cursor starts. Start each one at a known position: `0`, `^`, `$` or a search.",
                    "blocks": [K("Record a macro that finds its own starting point", SELF_CORRECT)],
                },
                {
                    "h2": "Make a macro repeat itself until the last line",
                    "intro": "A macro that calls itself stops by itself when a motion fails, such as `j` at the last line or `f:` with no colon.",
                    "blocks": [K("Record a macro that calls itself", RECURSIVE)],
                },
                {
                    "h2": "Fix a macro without recording it again",
                    "intro": "Paste the macro, edit the text, then copy it back into the register. Then `@q` runs the edited macro.",
                    "blocks": [
                        K("Paste a macro, edit it and save it back", MACRO_EDIT),
                        K("Run a macro on many selected lines at once", MACRO_VISUAL),
                    ],
                },
                {
                    "h2": "Add a comment to the end of every order (two ways)",
                    "intro": "`RAW_ORDERS` in `src/orders.py` has exactly 6 entries (`A1` to `A6`). Add `  # reviewed` to the end of each.",
                    "blocks": [
                        K("Add a comment to every line with a macro", [
                            ("qa", "Put the cursor on the `A1` line: start recording into register a"),
                            ("A  # reviewed", "Go to the end of the line, type the comment, press Esc"),
                            ("j", "Go down to the `A2` line"),
                            ("q", "Stop recording. `A1` is tagged; `A2` is ready"),
                            ("5@a", "Replay exactly 5 times, once per remaining line"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Every entry from `A1` to `A6` ends with `# reviewed`."}),
                        K("Add a comment to every line with a visual selection", [
                            ("u", "Undo everything first"),
                            ("qa", "Record again on the `A1` line"),
                            ("A  # reviewed", "Go to the end of the line, type the comment, press Esc"),
                            ("q", "Stop recording; no `j` this time"),
                            ("Vjjjjj", "Select all 6 lines"),
                            (":normal @a", "Run the macro on each selected line"),
                        ], **{"try": "Same result, different technique.",
                              "expect": "`<Space>sg \"# reviewed\"` returns 6 hits. Press `u` until the tags are gone: Lesson 6 depends on the exact structure of `orders.py`."}),
                    ],
                },
                {
                    "h2": "Calculate a sum inside the editor",
                    "intro": "Do the maths in the editor.",
                    "blocks": [
                        K("Calculate and insert the result (insert mode)", EXPR_INSERT, **{"try": "In insert mode press `Ctrl-r =`, type `5 * 42`, then Enter.", "expect": "`210` is inserted."}),
                        K("Calculate and paste the result (normal mode)", EXPR_NORMAL),
                    ],
                },
                {
                    "h2": "Collect lines, delete without losing a copy, paste a file name",
                    "intro": "A lowercase register replaces its text. An uppercase register adds to it. Delete into the black hole to keep what you copied.",
                    "blocks": [
                        K("Collect several lines in one register", APPEND),
                        K("Delete a line without losing the line you copied", BLACK_HOLE),
                        K("Paste the current file name", FILENAME),
                        K("Copy two TODO lines into one new buffer", [
                            ("gg", "Go to the top of `data/log.txt`"),
                            ("/# TODO", "Then press Enter: the first of 2 TODO comment lines"),
                            ("\"ayy", "Copy it into register a (replaces the contents)"),
                            ("n", "Jump to the second `# TODO` line"),
                            ("\"Ayy", "Add it to register a"),
                            (":enew", "Open a blank scratch buffer"),
                            ("\"ap", "Paste both TODO lines at once"),
                        ]),
                        X("See what register a holds before you paste", ":reg a", "Register a holds both TODO lines together, in file order."),
                        K("Check that the black hole keeps what you copied", [
                            ("yy", "Copy the `def summarize(items):` line in `src/messy.py`"),
                            ("\"_dd", "Move to a different line and delete it"),
                            ("p", "Paste `def summarize(items):`, not the deleted line"),
                            ("u", "Press twice to restore `messy.py`"),
                            (":bd!", "Close the scratch buffer without saving"),
                        ], **{"try": "`\"_dd` never touched the default register.",
                              "expect": "The paste is `def summarize(items):`, not the line you just deleted."}),
                    ],
                },
                {
                    "h2": "Edit and rerun an old command from your history (q:)",
                    "intro": "Press `q:` to open command history as an editable buffer. Move with `j` and `k`, edit a command, then press Enter to run it.",
                    "blocks": [
                        K("Open the command history and search history windows", CMDLINE_WIN),
                        K("Edit an old command and run it again", [
                            (":echo \"first\"", "Run it, then run `:echo \"second\"`"),
                            ("q:", "Open the command-line window"),
                            ("k", "Go up to the `:echo \"first\"` line"),
                            ("ci\"", "Change `\"first\"` to `\"third\"`, then press Enter"),
                        ], **{"try": "Press the keys in order in any buffer.",
                              "expect": "The message area shows `third`, and `:messages` shows all three echoes in order: `first`, `second`, `third`."}),
                    ],
                },
            ],
            "rules": {
                "h2": "Pick the right register or macro habit",
                "cards": [
                    ("Choose a register for the job", "Match what you want to do to a register.", ["I want to", "Use"], [
                        ["Collect lines from different places", "`\"Ayy` after `\"ayy`"],
                        ["Delete without losing what I copied", "`\"_dd` or `\"_diw`"],
                        ["Paste the current file name", "`\"%p`"],
                        ["Calculate inside a line", "`Ctrl-r =`"],
                    ]),
                    ("Make a macro reliable", "Follow these habits so a macro keeps working.", ["Habit", "Why"], [
                        ["Start at `0`, `^`, `$` or a search", "A known starting position makes it repeatable"],
                        ["End with `j` and `@a`", "The macro stops when a motion fails"],
                        ["Edit as text with `\"qp`", "Fix a macro without recording it again"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Collect two lines from different places in one register",
                "frame": "How do I get two TODO lines into one place?",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (None, "`/TODO` `Enter`, then `\"ayy`", "Find line 12 and copy it into register a."),
                    (None, "`n`", "Jump to the second TODO, line 14."),
                    (None, "`\"Ayy`", "Add that line to register a."),
                    (None, "`:enew` then `\"ap`", "Paste both lines, below the empty first line."),
                ],
                "after": "\nTODO call the carrier\nTODO print labels",
                "meaning": "Register `a` collected lines from two places, in file order.",
            },
            "practice": {
                "h2": "Check how to use macros and registers",
                "qs": [
                    ("Mechanism", "Why does a recursive macro stop by itself?",
                     "What happens when a motion has nowhere to go?",
                     ["`j` fails at the last line.", "A failed motion aborts the macro."],
                     "A failing motion ends it."),
                    ("Keystrokes", "How do I add the current line to register a?",
                     "A capital letter adds to the register.",
                     ["Press `\"Ayy`."],
                     "`\"Ayy`."),
                    ("Application", "How do I run macro a on six selected lines?",
                     "Select the lines, then use an ex command.",
                     ["Select with `V5j`.", "Run `:normal @a`."],
                     "`V5j`, then `:normal @a`."),
                    ("Common mistake", "I deleted a line and lost the text I copied. What should I do next time?",
                     "Use a register that nothing reads.",
                     ["Delete into the black hole."],
                     "Use `\"_dd`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Change every match in a project: quickfix, marks and :g",
            "subtitle": "Replace text in every file, collect all TODOs, bookmark files, rewrite text with regex, delete lines that match a pattern",
            "idea": (
                "Collect every match once, then change all of them.",
                [
                    ("Collect all search results in a list", "Ctrl-q", "Send the results to the quickfix list."),
                    ("Replace text in every listed file", ":cdo s/a/b/g", "Replace across the list."),
                    ("Bookmark a file and line", "mA", "Mark a file and line."),
                    ("Delete every line that matches", ":g/pattern/d", "Delete every line that matches."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I stop changing one file at a time, and stop a regex rewrite from touching lines I want to keep?",
                "fix": "Collect matches in quickfix, bookmark files with marks and limit substitution with ranges and `:g`.",
            },
            "drills": [
                {
                    "h2": "Collect every search result in one list (quickfix)",
                    "intro": "Quickfix holds results for the whole project. The location list belongs to one buffer.",
                    "blocks": [
                        K("Open, close and walk through the quickfix list", QUICKFIX),
                        {"type": "text", "body": "How do I replace text in every file? Press `<Space>/` to grep, `Ctrl-q` to send all results to quickfix, then `:cdo s/old/new/g | w` to replace across all files, or `:cfdo %s/old/new/g | w` for the same per file (faster)."},
                        K("Use a location list for one buffer", LOCLIST),
                        K("Find every TODO in the project and step through them", [
                            ("<Space>/", "Search text in all files: type `TODO` (or use `<Space>sg`)"),
                            ("Ctrl-q", "Send every hit to the quickfix list"),
                            (":copen", "See them all in one window"),
                            ("]q", "Step through the results, with `[q` to go back; Enter on a line jumps to it"),
                            (":cclose", "Close the list when you are done"),
                        ], **{"try": "You always get the 2 `# TODO` lines in `data/log.txt` and 2 hits in `scripts/dirty.patch` (the reset script's patch carries the same text). Depending on Lesson 6, you may also see the rename TODO and the `average()` TODO.",
                              "expect": "The quickfix title bar shows a match count equal to what `<Space>sg TODO` reported."}),
                    ],
                },
                {
                    "h2": "Bookmark a place and jump back to it (marks)",
                    "intro": "Vim sets the automatic marks for you. Use A to D for your four most-used files.",
                    "blocks": [
                        K("Jump to where you last edited, inserted or copied", AUTO_MARKS),
                        K("Delete or copy from here back to a mark", MARK_OPERATE),
                        K("Bookmark a file and jump back from any file", GLOBAL_MARKS),
                        K("Bookmark two files and jump between them without typing names", [
                            ("mA", "In `src/calculator.py`, on `class Person:`"),
                            ("mB", "In `src/orders.py`, on `class OrderBook:`"),
                            ("'A", "From an unrelated file such as `README.md`: jump to `class Person:`"),
                            ("'B", "Jump straight to `class OrderBook:`"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "You land in `orders.py` on the `OrderBook` line without typing a single filename."}),
                        K("Delete up to a mark (destructive: undo at once)", [
                            ("ma", "In `calculator.py`, on `class Person:`"),
                            ("G", "Jump to the end of the file"),
                            ("d`a", "Delete everything from the end back to the mark: the whole `Person` class"),
                            ("u", "Restore it right away"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "`Person` is back. Confirm with `<Space>sg \"class Person\"`."}),
                    ],
                },
                {
                    "h2": "Search and replace with regex groups, case and ranges",
                    "intro": "Use groups, case changes, expressions and ranges.",
                    "blocks": [
                        K("Keep part of the match in the replacement (groups)", REGEX_GROUPS),
                        K("Change the case of matched text", CASE_SUB),
                        K("Replace numbers with a calculated value", EXPR_SUB),
                        K("Replace only in some lines (ranges)", RANGE_MOD),
                        X("Rename a word and keep its number (one regex)", r":%s/item \(\d\+\)/entry \1/g", "Every `item N` becomes `entry N`, keeping the right number on each line."),
                        X("Count the matches without replacing them", ":%s/item//gn\n:%s/entry//gn", "The first reports 0 matches and the second reports 10. `entry 7` still says `entry 7`: the backreference kept the number."),
                        {"type": "text", "body": "How do I check the result? Not with `<Space>sg item`. That greps the whole project, and `orders.py` and `messy.py` legitimately use `item` as a variable name. Press `u` to undo it."},
                        X("Make one line Title Case", r":'<,'>s/\<\(\w\)/\u\1/g", "Select the `keep: this line matches a filter pattern` line with `V` first. It reads `Keep: This Line Matches A Filter Pattern` and every other line is unchanged. Press `u` to undo it."),
                    ],
                },
                {
                    "h2": "Run a command on every line that matches (:g)",
                    "intro": "Run a command on all lines that match a pattern. `:v` does the opposite: it runs on lines that do not match.",
                    "blocks": [
                        K("Delete, copy or move every matching line", GLOBAL),
                        X("Delete all TODO lines and all blank lines", ":g/TODO/d\n:g/^$/d", "The first deletes both `# TODO` comment lines in one shot. The second deletes every blank line (there are 3). Press `u` after each to bring them back.", where="nvim"),
                        X("Keep only the lines that match, on a scratch copy", ":w /tmp/log-copy.txt\n:e /tmp/log-copy.txt\n:v/keep/d", "The copy has exactly 3 lines, all starting with `keep:`. Close it with `:bd!`: you never touched the real `data/log.txt`."),
                    ],
                },
            ],
            "rules": {
                "h2": "Pick the scope: list, line, mark or range",
                "cards": [
                    ("Change every match in a list or by pattern", "Decide which lines to change first, then pick the command.", ["Scope", "Command"], [
                        ["Every entry in the quickfix list", "`:cdo s/old/new/g | w`"],
                        ["Every file in the quickfix list", "`:cfdo %s/old/new/g | w`"],
                        ["Lines that match a pattern", "`:g/pattern/d`"],
                        ["Lines that do not match", "`:v/pattern/d`"],
                    ]),
                    ("Bookmark a place in a file or across files", "A lowercase mark stays in one file. An uppercase mark works across files.", ["Key", "Does"], [
                        ["`ma`", "Mark a place in this file"],
                        ["`mA`", "Mark a place across files"],
                        ["`'A`", "Jump to the file and line of mark A"],
                    ]),
                    ("Undo a drill safely", "These drills are throwaway: undo them like this.", ["Situation", "Undo with"], [
                        ["After a substitution", "`u`"],
                        ["Autosave paused (`:ASToggle`), nothing saved", "`:e!` reloads from disk"],
                        ["After `:v/keep/d`", "Work on a `/tmp` copy"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Replace every TODO in the project after checking each hit",
                "frame": "Three lines say `TODO`. How do I review them before I change any?",
                "open": "cd ~/tw && nvim todo.txt",
                "steps": [
                    (None, "`<Space>/` then `TODO`", "The picker lists the three hits."),
                    (None, "`Ctrl-q` then `:copen`", "Quickfix holds all three. Check each one."),
                    (None, "`:cdo s/TODO/DONE/g | w`", "Change and save every hit."),
                    (None, "`:cdo s/DONE/TODO/g | w`", "Put them back."),
                ],
                "before": "TODO call the carrier\nbuy tape\nTODO print labels\nbuy boxes\nTODO reply to Sam",
                "after": "DONE call the carrier\nbuy tape\nDONE print labels\nbuy boxes\nDONE reply to Sam",
                "meaning": "You reviewed the list before changing anything.",
            },
            "practice": {
                "h2": "Check how to use quickfix, marks and substitution",
                "qs": [
                    ("Mechanism", "What is the difference between a mark set with `ma` and one set with `mA`?",
                     "Case decides the scope.",
                     ["Lowercase is local to the file.", "Uppercase remembers the file."],
                     "`mA` is a global mark across files."),
                    ("Keystrokes", "How do I delete every empty line?",
                     "Use `:g` with an anchor pattern.",
                     ["Run `:g/^$/d`."],
                     "`:g/^$/d`."),
                    ("Application", "How do I keep only the lines that contain `keep`?",
                     "Use the inverse of `:g`.",
                     ["Run `:v/keep/d`, on a copy."],
                     "`:v/keep/d`."),
                    ("Common mistake", "Why does the drill run `:v/keep/d` on a `/tmp` copy?",
                     "What does it delete?",
                     ["It deletes everything that does not match.", "That includes all the item lines."],
                     "It would wreck the real file."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Edit many files, columns and lines, and go back in time",
            "subtitle": "Open a set of files, edit a column of text, number lines, duplicate or move a line, go back to an earlier state of a file",
            "idea": (
                "Edit many files and a column of text, and go back in time.",
                [
                    ("Open a set of files", ":args src/*.py", "Load a set of files."),
                    ("Edit a column of text", "Ctrl-v", "Select a column as a block."),
                    ("Duplicate a line", ":t.", "Copy the line below itself."),
                    ("Go back to an earlier version of a file", ":earlier 5m", "Return to the file 5 minutes ago."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I stop opening files one by one, editing columns line by line and undoing one step at a time?",
                "fix": "Load files with `:args`, edit columns with `Ctrl-v` and go back in time with `:earlier` and `g-`.",
            },
            "drills": [
                {
                    "h2": "Open a set of files and switch between them",
                    "intro": "Tabs in vim are layouts (arrangements of splits), not files. Use buffers for files.",
                    "blocks": [
                        K("Load many files into a list and step through them", ARGS),
                        K("Switch between open files (buffers)", BUFFER_TRICKS),
                        K("Use tab pages for layouts, not files", TABS),
                        K("Open every Python file in src/ as one list", [
                            (":args src/*.py", "Load every `.py` directly under `src/`: the four real modules plus the empty `__init__.py` (and `scratch.py` if the git drills made it)"),
                            (":args", "Run it with no arguments: it prints the list with the current file in brackets"),
                            (":next", "Go to the next file; `:prev` goes back"),
                            ("Ctrl-^", "After two files: toggle back to the one you were just on"),
                        ], **{"try": "Run it from inside `nvim-drills`. Globs grab everything that matches, so curating is on you.",
                              "expect": "`:args` again shows the same list with `[ ]` around whichever file you are viewing."}),
                    ],
                },
                {
                    "h2": "Complete text and run commands without leaving insert mode",
                    "intro": "Complete text and run one-off commands without leaving insert mode.",
                    "blocks": [
                        K("Complete a word, file name or line as you type", COMPLETE),
                        K("Delete, paste and indent without leaving insert mode", INSERT_TRICKS),
                        K("Delete a line while you are typing", [
                            ("A", "Start typing at the end of `total = 0` inside `summarize()` in `src/messy.py`"),
                            ("Ctrl-o dd", "Delete the current line and drop back into insert mode"),
                            ("Esc", "Leave insert mode"),
                            ("u", "Restore the line: this drill is throwaway"),
                        ], **{"try": "Press the keys in order.",
                              "expect": "Right after `Ctrl-o dd`, `total = 0` is gone and you never left insert mode: no flicker to NORMAL."}),
                    ],
                },
                {
                    "h2": "Edit a column of text with block mode",
                    "intro": "Edit the same column on many lines.",
                    "blocks": [
                        K("Insert, change or delete a column on every line", BLOCK_COLUMN),
                        K("Number lines 1, 2, 3 down a column", BLOCK_SEQ),
                        K("Number lines after inserting a start value", BLOCK_SEQ2),
                        K("Add text at the end of lines of different lengths", BLOCK_ALIGN),
                        K("Renumber a column: zero it, then count up", [
                            ("Ctrl-v", "On the `7` in `item 7: pending` in `data/log.txt`"),
                            ("2j", "Extend down 2 rows to cover `7`, `8` and `9` as a one-wide column"),
                            ("r0", "Turn every character in the block into `0`"),
                            ("gv", "Select the same block again"),
                            ("g Ctrl-a", "Add 1 to line 1, 2 to line 2 and 3 to line 3"),
                        ], **{"try": "Leave `item 10` out of the column, since it has two digits.",
                              "expect": "The three lines read `item 1: pending`, `item 2: pending`, `item 3: pending`: each line got a different increment. Press `u` twice to undo both steps."}),
                    ],
                },
                {
                    "h2": "Copy, move or sort lines with ex commands and ranges",
                    "intro": "A range says where. An ex command says what.",
                    "blocks": [
                        K("Write a range: current line, whole file, selection or marks", RANGE_SYNTAX),
                        K("Copy, move, read in and sort lines", EX_USEFUL),
                        K("Duplicate a line and move the copy to the end of the file", [
                            (":t.", "On the `A1` line in `RAW_ORDERS`: make two identical `A1` entries"),
                            (":m$", "Move the duplicate to the very end of the file, past `build_order_book()`"),
                            ("G", "Jump to the end of the file"),
                            ("u", "Press twice to undo: the move, then the duplicate"),
                        ], **{"try": "Press the keys in order. `:m$` operates on the whole buffer, not the enclosing structure.",
                              "expect": "The duplicated `A1` dict literal is the last line in `orders.py`, outside the list and outside `build_order_book()`. After `u` twice and a moment for autosave to write the undo, `<Space>sg \"id.*A1\"` shows only 1 hit."}),
                    ],
                },
                {
                    "h2": "Switch files fast and change numbers in place",
                    "intro": "Small habits save many keystrokes.",
                    "blocks": [
                        K("Scroll without filling the jump list", JUMP_LIST),
                        K("Switch quickly between files", QUICK_SWITCH),
                        K("Fix the same pattern across the file and move on", FIX_MOVE),
                        K("Add to or subtract from a number under the cursor", NUMBER_TRICK),
                        {"type": "text", "body": "How do I update a date, version or port number? Use the number trick for an instant update."},
                        K("Switch between two files without typing", [
                            ("<Space>sf", "Find a file by name: type `calculator`, press Enter to open `src/calculator.py`"),
                            ("<Space>sf", "Find a file by name: open `src/orders.py` the same way"),
                            ("Ctrl-^", "Switch back to `calculator.py` instantly"),
                            ("Ctrl-^", "Switch back to `orders.py`"),
                        ], **{"try": "Nothing to undo: this is pure navigation.",
                              "expect": "Each `Ctrl-^` flips between the two files, faster than a fuzzy search."}),
                    ],
                },
                {
                    "h2": "Go back to an earlier state of a file (undo tree)",
                    "intro": "How do I undo further than `u`? Vim's undo is a tree, not a line. If you undo and make new changes, the old changes are a branch, and `g-` and `g+` walk the whole tree. Undo history is already persistent: it survives quitting Neovim.",
                    "blocks": [
                        K("Go back or forward in time, by minutes, saves or steps", UNDO_TREE),
                        {"type": "text", "body": "How do I travel through saved states? This is the one exercise in this lesson that must write to disk, because `:earlier` and `:later` with an `f` count are save-based. Autosave would add saves of its own and spoil the count, so pause it first and turn it back on at the end."},
                        K("Go back to an earlier save of a file", [
                            (":ASToggle", "Pause autosave: only your own `:w` counts as a save now"),
                            (":w", "In `src/messy.py`: add `# checkpoint 1` at the top, then save. Repeat for `# checkpoint 2` and `# checkpoint 3`"),
                            (":earlier 2f", "Go back 2 saves: only `# checkpoint 1` is present"),
                            (":later 1f", "Go forward 1 save: `# checkpoint 2` reappears"),
                            ("g-", "Press a few times, then `g+`: walk one small change at a time"),
                        ], **{"try": "At each step run `:%s/checkpoint//gn` (count only). Do not use `<Space>sg checkpoint`: ripgrep reads the file on disk.",
                              "expect": "The match count equals the checkpoint number you are at."}),
                        X("Restore messy.py after the drill (required: it saved to disk)", "git checkout -- src/messy.py", "`src/messy.py` is back to its committed state. `:e!` alone would not help, since the dirty state is already on disk. From inside nvim use `:!git checkout -- %`. Reload with `:e!`, then run `:ASToggle` again to turn autosave back on.", where="shell"),
                    ],
                },
            ],
            "rules": {
                "h2": "Find the keys for an expert edit",
                "cards": [
                    ("Find the keys for an edit", "Find what you want to do on the left, the keys on the right.", ["Intent", "Keys"], [
                        ["Delete up to a pattern", "`d/pattern`"],
                        ["Change up to a character", "`ct{char}`"],
                        ["Repeat the last search and change", "`cgn` then `.`"],
                        ["Delete without overwriting what I copied", "`\"_dd`"],
                        ["Add a line to a register", "`\"Ayy`"],
                        ["Run a macro on the selected lines", "`:'<,'>normal @a`"],
                        ["Count up numbers in a column", "`Ctrl-v` select → `g Ctrl-a`"],
                        ["Run a command from insert mode", "`Ctrl-o {cmd}`"],
                        ["Calculate in insert mode", "`Ctrl-r = 5*42 Enter`"],
                        ["Delete all lines that match a pattern", "`:g/pattern/d`"],
                        ["Keep only lines that match a pattern", "`:v/pattern/d`"],
                        ["Copy all matching lines to the end of the file", "`:g/pattern/t$`"],
                        ["Sort the selected lines", "`:'<,'>!sort`"],
                        ["Go back 5 minutes in time", "`:earlier 5m`"],
                        ["Duplicate a line", "`:t.` or `yyp`"],
                        ["Move a line to the end of the file", "`:m$`"],
                        ["Switch between the last 2 files", "`Ctrl-^`"],
                        ["Capitalize the first letter of every word", r"`:%s/\<\w/\u&/g`"],
                    ]),
                    ("How do I undo or discard my changes?", "Autosave writes most edits within 3 seconds, so assume the change reached the disk.", ["Situation", "Use"], [
                        ["Any edit you made this session", "`u`, step by step"],
                        ["Autosave paused (`:ASToggle`), nothing saved", "`:e!` reloads from disk"],
                        ["Already saved to disk, and I want the committed file back", "`git checkout -- src/messy.py`"],
                        ["Go back to an earlier save", "`:earlier 2f` or `:later 1f`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Number lines 1, 2, 3 down a column",
                "frame": "How do I make three lines read 1, 2, 3?",
                "open": "nvim ~/tw/todo.txt",
                "steps": [
                    (("line 7, on the `7`", "`7G` `f7`"), "`Ctrl-v` then `2j`", "Select the digit on lines 7 to 9."),
                    (None, "`r0`", "Zero the column."),
                    (None, "`gv`", "Select the same block again."),
                    (None, "`g` `Ctrl-a`, then `u` twice", "Add 1, 2, 3 down the column, then undo the add and the zeroing. Autosave writes the original back."),
                ],
                "before": "item 7: pending\nitem 8: pending\nitem 9: pending",
                "after": "item 1: pending\nitem 2: pending\nitem 3: pending",
                "meaning": "Each line received a different increment, so the numbers became a sequence.",
            },
            "practice": {
                "h2": "Check how to edit many files and columns, and go back in time",
                "qs": [
                    ("Mechanism", "What is the difference between `u` and `:earlier 2f`?",
                     "One counts changes, one counts saves.",
                     ["`u` undoes the last change.", "`:earlier 2f` jumps back 2 file saves."],
                     "`:earlier 2f` travels by save, not by change."),
                    ("Keystrokes", "How do I delete a line from insert mode without leaving it?",
                     "Use one normal command.",
                     ["Press `Ctrl-o`.", "Press `dd`."],
                     "`Ctrl-o dd`."),
                    ("Application", "How do I duplicate the current line and move the copy to the end of the file?",
                     "Use two ex commands.",
                     ["Run `:t.`.", "Run `:m$`."],
                     "`:t.` then `:m$`."),
                    ("Common mistake", "I ran `:e!` to restore a file and nothing changed. Why?",
                     "Where is the dirty state now?",
                     ["Autosave or `:w` already wrote it to disk.", "`:e!` reloads from disk."],
                     "Use `git checkout -- src/messy.py`."),
                ],
            },
        },
    ],
}
