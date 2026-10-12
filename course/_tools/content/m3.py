"""Module 3: Power editing. Sources: lesson 03 Neovim Power Editing.md and the quick-start guide."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


PERSON_INIT = C('''
def __init__(self):
    name = ""
    age = 0
    email = ""
    phone = ""
    address = ""
''')

MODULE = {
    "n": 3,
    "folder": "m3-power-editing",
    "title": "Power editing",
    "footer": "Operators and text objects, visual mode, macros, search and replace, registers, marks and multi-file edits",
    "tagline": "Operators, text objects, macros and registers: where vim gets fast.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Operators, motions, text objects",
            "subtitle": "Combine a verb with a target and every edit becomes two or three keys.",
            "idea": (
                "Vim's secret: an operator plus a motion is a new command.",
                [
                    ("Delete a word", "dw", "Operator d, motion w."),
                    ("Change inside quotes", "ci\"", "Deletes the text and starts typing."),
                    ("Delete inside parens", "di(", "Keeps the parens."),
                    ("Auto-indent file", "gg=G", "Operator = from top to bottom."),
                ],
                None,
            ),
            "problem": {
                "fail": "You edit by selecting with the mouse, or by deleting one character at a time.",
                "fix": "Name the verb and the target: `ci\"` changes what is inside the quotes, wherever the cursor sits in them.",
            },
            "drills": [
                {
                    "h2": "Operators and motions",
                    "intro": "Every practice file here is in `Terminal-Workflow/practice/nvim-drills`. Where an edit should not stay, discard it with `:e!`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Operators", "rows": [
                            ("d", "Delete"),
                            ("c", "Change (delete + enter insert mode)"),
                            ("y", "Yank (copy)"),
                            (">", "Indent right"),
                            ("<", "Indent left"),
                            ("=", "Auto-indent (fix indentation)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Combine with any motion", "rows": [
                            ("dw", "Delete word forward"),
                            ("db", "Delete word backward"),
                            ("d$ or D", "Delete to end of line"),
                            ("d0", "Delete to start of line"),
                            ("dG", "Delete to end of file"),
                            ("dgg", "Delete to start of file"),
                            ("cw", "Change word (delete word, start typing)"),
                            ("c$ or C", "Change to end of line"),
                            ("yy", "Yank (copy) whole line"),
                            ("yw", "Yank word"),
                            ("y$", "Yank to end of line"),
                            (">>", "Indent current line"),
                            ("<<", "Unindent current line"),
                            ("5>>", "Indent 5 lines"),
                            ("=G", "Auto-indent from here to end of file"),
                            ("gg=G", "Auto-indent the entire file"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Bump the tax rate from 8% to 7.5%", "code": C('''
5G
dw
u
f0
cW
0.075
Esc
'''),
                         "expect": "The line now reads `TAX_RATE = 0.075`. Discard with `:e!`: later lessons expect `0.08`."},
                        {"type": "text", "body": "Open `src/orders.py` first. `dw` leaves `= 0.08`; `u` undoes it, as a proof that `dw` eats the word and the trailing space. Use `cW`, not `cw`: the dot splits `0.08` into three vim words, so `cw` would change only the leading `0` and leave `0.075.08`."},
                    ],
                },
                {
                    "h2": "Text objects",
                    "intro": "Operate on structures: stuff inside brackets, quotes and tags. The pattern is operator, then `a` or `i`, then the object. `a` is around (includes the delimiters). `i` is inside (just the content).",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Change inside", "rows": [
                            ("ci(", "Change inside parentheses: (hello) → () + insert"),
                            ("ci[", "Change inside brackets: [1, 2, 3] → []"),
                            ("ci{", "Change inside braces: { code } → {}"),
                            ("ci\"", "Change inside double quotes: \"text\" → \"\""),
                            ("ci'", "Change inside single quotes: 'text' → ''"),
                            ("ci`", "Change inside backticks"),
                            ("ciw", "Change inside word (replaces the word)"),
                            ("cit", "Change inside HTML tag: <div>content</div> → <div></div>"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Delete, yank, select", "rows": [
                            ("di(", "Delete inside parentheses (keeps the parens)"),
                            ("da(", "Delete around parentheses (deletes parens too)"),
                            ("yi\"", "Yank (copy) inside quotes"),
                            ("ya{", "Yank around braces (includes the braces)"),
                            ("vi{", "Select inside braces (visual mode)"),
                            ("va\"", "Select around quotes"),
                            ("vip", "Select inside paragraph"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "All text objects", "rows": [
                            ("iw / aw", "Word"),
                            ("iW / aW", "WORD (includes punctuation)"),
                            ("is / as", "Sentence"),
                            ("ip / ap", "Paragraph"),
                            ("i) / a)", "Parentheses (same as i( / a()"),
                            ("i] / a]", "Brackets"),
                            ("i} / a}", "Braces"),
                            ("i\" / a\"", "Double quotes"),
                            ("i' / a'", "Single quotes"),
                            ("it / at", "HTML/XML tag"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Reword an error message", "code": C('''
/Cannot divide
ci"
Division by zero is not allowed
Esc
'''),
                         "expect": "The line reads `raise Exception(\"Division by zero is not allowed\")`. Discard with `:e!`."},
                        {"type": "text", "body": "Open `src/calculator.py` first. The search leaves the cursor inside `raise Exception(\"Cannot divide by zero\")`."},
                        {"type": "keys", "where": "nvim", "title": "Text objects on real data", "rows": [
                            ("di(", "On Order(raw[\"id\"], raw[\"items\"], raw[\"discount\"]) → empties the parens, keeps them"),
                            ("da(", "Same line → deletes the parens AND their contents, Order(...) becomes Order"),
                            ("ci{", "Cursor inside the first RAW_ORDERS entry {\"id\": \"A1\", ...} → clears the whole dict body"),
                        ], "try": "In `src/orders.py`, use these on `build_order_book` and the `RAW_ORDERS` list. Undo or `:e!` after each. After `di(`, press `%` on the opening `(`.",
                         "expect": "The cursor jumps straight to the now-adjacent `)`. Run `:e!` before moving on: `RAW_ORDERS` needs its six original entries."},
                    ],
                },
            ],
            "rules": {
                "h2": "The pattern",
                "cards": [
                    ("operator + a or i + object", "One sentence, three parts.", ["Part", "Meaning"], [
                        ["`d` `c` `y`", "The verb: delete, change, yank"],
                        ["`i`", "Inside: just the content"],
                        ["`a`", "Around: includes the delimiters"],
                        ["`w` `(` `\"` `{` `t`", "The object: word, parens, quotes, braces, tag"],
                    ]),
                    ("Why cW and not cw", "The dot splits a number into three words.", ["Keys", "Result on `0.08`"], [
                        ["`cw` then `0.075`", "`0.075.08`"],
                        ["`cW` then `0.075`", "`0.075`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Empty a call, then take it back",
                "frame": "You want the arguments of a call gone, and the parens kept.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 19, on `(`", "`19G` `f(`"), "`di(`", "The arguments vanish and the parens stay."),
                    (("on the `(`", "`F(`"), "`%`", "Jumps to the matching `)`."),
                    (None, "`u`", "Restores the line."),
                ],
                "before": "total = calc_totl(price, qty)",
                "after": "total = calc_totl()",
                "meaning": "The cursor only has to be inside the object; `da(` would remove the parens too.",
            },
            "practice": {
                "h2": "Practice: operators and text objects",
                "qs": [
                    ("Mechanism", "Why does `ci\"` work from the middle of the quoted text?",
                     "The object is the quotes, not the cursor.",
                     ["`i\"` means the text inside the nearest double quotes.", "`c` deletes it and enters insert mode."],
                     "A text object covers the whole structure around the cursor."),
                    ("Keystrokes", "Which keys delete the parens and what is inside them?",
                     "Around, not inside.",
                     ["Put the cursor inside the parens.", "Press `da(`."],
                     "`da(`."),
                    ("Application", "Change `8%` to `7.5%` on the `TAX_RATE = 0.08` line.",
                     "Whole WORD, not word.",
                     ["Move to `0.08` with `f0`.", "Press `cW`, type `0.075`, press `Esc`."],
                     "`cW` then `0.075`."),
                    ("Common mistake", "`cw` on `0.08` left you with `0.075.08`. Why?",
                     "How does vim see the dot?",
                     ["A word stops at the dot.", "`cw` changed only the leading `0`.", "Use `cW` for the whole space-delimited WORD."],
                     "Use `cW`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Visual mode, macros, search and replace",
            "subtitle": "Select what you mean, record an edit once, replay it on many lines.",
            "idea": (
                "Select, record, replace: three ways to change many lines at once.",
                [
                    ("Select lines", "V", "Line-wise visual mode."),
                    ("Column edit", "Ctrl-v", "Block mode. Edit many lines at once."),
                    ("Record a macro", "qa", "Records into register a. q stops."),
                    ("Replace all", ":%s/old/new/g", "Whole file, every match."),
                ],
                None,
            ),
            "problem": {
                "fail": "Five lines need the same fix, and you type it five times. A word appears fifty times and you edit each by hand.",
                "fix": "Use a column insert for the same prefix, a macro for the same edit, and `:%s` for the same word.",
            },
            "drills": [
                {
                    "h2": "Visual mode",
                    "intro": "Select first, then operate.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Visual modes", "rows": [
                            ("v", "Character-wise (select chars)"),
                            ("V", "Line-wise (select whole lines)"),
                            ("Ctrl-v", "Block/column mode (vertical selection!)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Select, then operate", "rows": [
                            ("v3w", "Select 3 words"),
                            ("Vj", "Select 2 lines"),
                            ("V5j d", "Select 6 lines and delete"),
                            ("Ctrl-v jjj I", "Column insert: add text to multiple lines"),
                            ("Ctrl-v jjj d", "Column delete: remove a column"),
                            ("vip", "Select entire paragraph"),
                            ("vi{", "Select inside braces"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Comment out orders A2 to A5", "code": C('''
^
Ctrl-v
jjj
I
#
Esc
'''),
                         "expect": "Lines for A2 through A5 now start with `# `. A1 and A6 are untouched. Discard with `:e!`: `RAW_ORDERS` needs all six live entries."},
                        {"type": "text", "body": "Open `src/orders.py` and put the cursor on the `{\"id\": \"A2\", ...` line. `^` puts it on the opening `{`. Block insert happens at the cursor's column, so the column matters."},
                    ],
                },
                {
                    "h2": "Macros (recording commands)",
                    "intro": "Record keystrokes once. Replay them. Perfect for repetitive edits.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Macro keys", "rows": [
                            ("qa", "Start recording macro into register 'a' (do your edits...)"),
                            ("q", "Stop recording"),
                            ("@a", "Play macro 'a'"),
                            ("@@", "Repeat last macro"),
                            ("5@a", "Play macro 'a' 5 times"),
                        ]},
                        {"type": "text", "body": "In `src/calculator.py`, the `Person` class has five `__init__` fields with no `self.` prefix. They are dead local variables instead of attributes."},
                        {"type": "code", "file": "src/calculator.py", "title": "The bug", "code": PERSON_INIT},
                        {"type": "cmd", "where": "nvim", "title": "Fix it with a macro", "code": C('''
qa
Iself.
Esc
j
q
4@a
'''),
                         "expect": "All five lines now read `self.<field> = ...`. This is a genuine bug fix: keep it, or discard with `:e!` to leave the fixture broken for a re-run."},
                        {"type": "text", "body": "Start with the cursor on `name`. `Iself.` goes to the line start and inserts `self.`. `j` moves to the next field. `4@a` replays on the remaining four lines (age, email, phone, address)."},
                    ],
                },
                {
                    "h2": "Search and replace",
                    "intro": "`:%s` works on the whole file. Add `c` to confirm each change.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Substitute", "rows": [
                            (":%s/old/new/g", "Replace all in file"),
                            (":%s/old/new/gc", "Replace all with confirmation"),
                            (":s/old/new/g", "Replace on current line only"),
                            (":%s/foo//g", "Delete all \"foo\""),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Useful patterns", "rows": [
                            (":%s/\\s\\+$//g", "Remove trailing whitespace"),
                            (":%s/^/# /g", "Add \"# \" to start of every line"),
                            (":%s/$/;/g", "Add \";\" to end of every line"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Mark a batch of items done", "code": C('''
:%s/pending/done/g
:%s/pending//gn
'''),
                         "expect": "The count command (trailing `n` means count, don't replace) reports `0 matches`. Discard with `:e!`: Lesson 7 uses this same \"pending\" text."},
                        {"type": "text", "body": "Open `data/log.txt` first: ten lines like `item 1: pending`, mixed with `# TODO` comments and blank lines."},
                    ],
                },
            ],
            "rules": {
                "h2": "Macros and registers at a glance",
                "cards": [
                    ("Macros and registers card", "Record, replay, copy to named slots.", ["Keys", "Action"], [
                        ["`qa...q`", "Record macro into 'a'"],
                        ["`@a / 5@a`", "Play macro / 5 times"],
                        ["`\"ayy/\"ap`", "Yank/paste register a"],
                        ["`\"+y/\"+p`", "System clipboard"],
                        ["`\"0p`", "Paste last yank (survives deletes)"],
                    ]),
                    ("Comment five lines", "A column insert in four keys and a prefix.", ["Keys", "Result"], [
                        ["`Ctrl-v 4j I # Esc`", "Block insert `# ` on 5 lines"],
                        ["`:%s/^/# /g`", "Same prefix on every line"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Fix four lines with one macro",
                "frame": "Four assignments need an `order_` prefix.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 15, on `name`", "`15G`"), "`qa` `I` then `order_` then `Esc` `j` `q`", "Records one edit into register a and ends on the next line."),
                    (None, "`3@a`", "Replays it on lines 16 to 18."),
                    (None, "`:e!`", "Discards the edit."),
                ],
                "before": 'name = "pen"\nqty = 3\nprice = 2.50\nnote = "rush"',
                "after": 'order_name = "pen"\norder_qty = 3\norder_price = 2.50\norder_note = "rush"',
                "meaning": "The macro ends on the next line, so it chains: record one clean edit and let the count do the rest.",
            },
            "practice": {
                "h2": "Practice: visual, macros, replace",
                "qs": [
                    ("Mechanism", "Why does `4@a` fix four lines after you edited one?",
                     "What did the macro end on?",
                     ["The macro ended with `j`, on the next line.", "Each replay starts where the last one stopped."],
                     "The macro moves to the next line, so replays chain."),
                    ("Keystrokes", "Which keys add `# ` to four lines in a column?",
                     "Block mode, then insert.",
                     ["Press `Ctrl-v` and `jjj`.", "Press `I`, type `# `, press `Esc`."],
                     "`Ctrl-v jjj I`, `# `, `Esc`."),
                    ("Application", "Replace `pending` with `done` everywhere, then count what is left.",
                     "Substitute, then substitute with `n`.",
                     ["Run `:%s/pending/done/g`.", "Run `:%s/pending//gn`."],
                     "The count reports `0 matches`."),
                    ("Common mistake", "Your block insert landed in the wrong column. Why?",
                     "Where does the block start?",
                     ["Block insert uses the cursor's column.", "Press `^` first to sit on the first non-blank."],
                     "The cursor column matters. Press `^` before `Ctrl-v`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Indent, registers, marks, many files",
            "subtitle": "Fix indentation, keep several clipboards, bookmark places and edit across files.",
            "idea": (
                "Indent in one key, keep many clipboards, jump to bookmarks, edit many files.",
                [
                    ("Auto-indent file", "gg=G", "Fixes indentation everywhere."),
                    ("Named register", "\"ayy", "Yank a line into register a."),
                    ("Global mark", "mA", "Jump back from any file with 'A."),
                    ("Many files", ":args src/*.py", "Load files, then run :argdo."),
                ],
                None,
            ),
            "problem": {
                "fail": "A paste is mis-indented. A delete wiped what you copied. A bookmark only works inside one file.",
                "fix": "Re-indent with `gg=G`, paste the last yank with `\"0p`, and use an uppercase mark such as `mA` across files.",
            },
            "drills": [
                {
                    "h2": "Indentation and formatting",
                    "intro": "`src/messy.py` has three functions and a class with deliberately inconsistent, but valid, indentation.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Indent keys", "rows": [
                            (">>", "Indent current line"),
                            ("<<", "Unindent current line"),
                            ("5>>", "Indent 5 lines"),
                            (">}", "Indent to next paragraph"),
                            ("==", "Auto-indent current line"),
                            ("=G", "Auto-indent from here to end of file"),
                            ("gg=G", "Auto-indent entire file"),
                            ("=i{", "Auto-indent inside braces"),
                            ("<Space>cf", "Format file (language formatter: ruff, prettier, etc.)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "In visual mode", "rows": [
                            ("V5j >", "Indent 6 selected lines"),
                            ("V5j <", "Unindent"),
                            ("V5j =", "Auto-indent"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Clean up inconsistent indentation", "code": C('''
gg=G
:!python3 -m py_compile %
'''),
                         "expect": "Every block lines up on a consistent 4-space grid. The file is valid Python either way. Discard with `:e!`: Lesson 7 reuses this file messy, on purpose."},
                    ],
                },
                {
                    "h2": "Registers (multiple clipboards)",
                    "intro": "Vim has 26 named registers (a-z) plus special ones. Yank something, delete something else, and the default register is overwritten. `\"0p` pastes what you originally yanked.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Named registers", "rows": [
                            ("\"ayy", "Yank line into register a"),
                            ("\"ap", "Paste from register a"),
                            ("\"byy", "Yank into register b"),
                            ("\"bp", "Paste from register b"),
                            ("\"+y", "Yank into system clipboard (Cmd+V works after)"),
                            ("\"+p", "Paste from system clipboard"),
                            (":reg", "See all registers"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Special registers", "rows": [
                            ("\"\"", "Last yanked/deleted text (default)"),
                            ("\"0", "Last yank (survives deletes!)"),
                            ("\"+", "System clipboard"),
                            ("\".", "Last inserted text"),
                            ("\"%", "Current filename"),
                            ("\":", "Last command"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Paste with auto-indentation", "rows": [
                            ("]p", "Paste below, match indent level of current line"),
                            ("[p", "Paste above, match indent level of current line"),
                            ("p then =']", "Paste, then auto-indent the pasted block (proper reformat)"),
                            ("p then V']=", "Paste, select pasted text, auto-indent (visual way)"),
                        ]},
                        {"type": "text", "body": "`]p` matches the indent of the surrounding line, a shallow fix. For full reformatting, do `p` then `=']`."},
                        {"type": "cmd", "where": "nvim", "title": "Registers survive an unrelated delete", "code": C(r'''
5G
"ayy
/A3
dd
"ap
"0p
:reg a
:reg 0
'''),
                         "expect": "`:reg a` and `:reg 0` both show `TAX_RATE = 0.08`. Discard everything with `:e!`."},
                    ],
                },
                {
                    "h2": "Marks (bookmarks)",
                    "intro": "Lowercase marks (a-z) are per-file. Uppercase marks (A-Z) are global, across files.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Mark keys", "rows": [
                            ("ma", "Set mark 'a' at cursor"),
                            ("'a", "Jump to mark 'a' (line)"),
                            ("`a", "Jump to mark 'a' (exact position)"),
                            ("''", "Jump back to previous position"),
                            ("`.", "Jump to last edit location"),
                            (":marks", "List all marks"),
                        ], "try": "In `src/calculator.py`, put the cursor on `class Person:` and press `mA`. Open `src/orders.py` with `<Space>sf`, then press `'A`.",
                         "expect": "`'A` jumps back to the `Person` class line in `calculator.py`. `:marks` lists `A` with `calculator.py` as its file."},
                    ],
                },
                {
                    "h2": "Multi-file operations",
                    "intro": "Workflow: `<Space>/` to grep, `Ctrl-q` to send to quickfix, then `:cdo s/old/new/g | w`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Edit many files", "rows": [
                            (":args **/*.py", "Load all Python files"),
                            (":argdo %s/old/new/g | w", "Replace across all"),
                            (":bufdo %s/old/new/g | w", "Replace across open buffers"),
                            (":cdo s/old/new/g | w", "Replace in quickfix results"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Touch every file, safely", "code": C('''
:args src/*.py
:args
:argdo $put ='# reviewed'
:next
:prev
:ls
:argdo e!
'''),
                         "expect": "`:ls` shows a `+` on every arglist buffer: modified in memory only, since there is no `| w`. `:argdo e!` reloads every buffer from disk and discards the edits."},
                        {"type": "text", "body": "`:args src/*.py` loads the four real modules plus the empty `__init__.py` (and `scratch.py` if the git drills created it). `:next` and `:prev` flip through the buffers and show the marker at the bottom of each. The full form, `:argdo %s/old/new/g | w`, is for when you want the change saved."},
                    ],
                },
            ],
            "rules": {
                "h2": "Cheat sheet",
                "cards": [
                    ("Cheat sheet (print this)", "Intent, keys and what happens.", ["Intent", "Keys", "Example"], [
                        ["Delete word", "`dw`", "`hello world` → `world`"],
                        ["Delete inside parens", "`di(`", "`func(arg1, arg2)` → `func()`"],
                        ["Change inside quotes", "`ci\"`", "`\"old\"` → `\"\"` + insert"],
                        ["Change word", "`ciw`", "replaces whole word"],
                        ["Delete to end of line", "`D`", "removes after cursor"],
                        ["Delete entire line", "`dd`", "line gone"],
                        ["Copy inside braces", "`yi{`", "copies between `{}`"],
                        ["Select inside block", "`vi{`", "highlights between `{}`"],
                        ["Indent 5 lines", "`5>>`", "pushes right"],
                        ["Auto-indent file", "`gg=G`", "fixes all indentation"],
                        ["Format file", "`<Space>cf`", "language formatter"],
                        ["Comment 5 lines", "`Ctrl-v 4j I # Esc`", "block insert"],
                        ["Repeat last edit", "`.`", "exact same change"],
                        ["Record macro", "`qa ... q`", "`@a` to replay"],
                        ["Paste from yank", "`\"0p`", "even after deleting"],
                        ["System clipboard", "`\"+y`", "works with Cmd+V"],
                        ["Jump bracket", "`%`", "`(` ↔ `)`"],
                        ["Jump to line 50", "`50G`", "instant"],
                        ["Search & replace", "`:%s/old/new/g`", "whole file"],
                    ]),
                    ("Which mark?", "Lowercase stays in the file. Uppercase crosses files.", ["Mark", "Scope"], [
                        ["`ma`", "This file only"],
                        ["`mA`", "Global: jump back with `'A` from any file"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Paste what you yanked, after a delete",
                "frame": "You yank a line, delete another, and still want the first.",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 1", "`gg`"), '`yy` then `"ayy`', "Yanks the line into register 0 and into register a."),
                    (("line 18", "`18G`"), "`dd`", "Deletes the `note` line. Only the default register changes."),
                    (None, '`"ap`', "The `TAX_RATE` line is pasted below."),
                    (None, '`"0p`', 'The same line again: `"0` survives deletes.'),
                    (None, "`:e!`", "Discards it all."),
                ],
                "before": 'note = "rush"\ntotal = calc_totl(price, qty)',
                "after": "total = calc_totl(price, qty)\nTAX_RATE = 0.08\nTAX_RATE = 0.08",
                "meaning": 'Named registers and `"0` keep your yank safe from later deletes.',
            },
            "practice": {
                "h2": "Practice: indent, registers, marks",
                "qs": [
                    ("Mechanism", "Why does `p` paste the deleted line instead of the yanked one?",
                     "Deletes use the default register too.",
                     ["A delete overwrites the default register.", "`\"0` holds the last yank."],
                     "Use `\"0p` to paste the last yank."),
                    ("Keystrokes", "Which keys re-indent the whole file?",
                     "Top, then auto-indent to the end.",
                     ["Press `gg` to go to the top.", "Press `=G`."],
                     "`gg=G`."),
                    ("Application", "Bookmark `class Person:` in one file and jump back from another.",
                     "Uppercase mark.",
                     ["Press `mA` on the class line.", "Open another file.", "Press `'A`."],
                     "`mA`, then `'A`."),
                    ("Common mistake", "After `:argdo` your files show `+` and you do not want them. What do you run?",
                     "Nothing was saved.",
                     ["The edits live in memory.", "Run `:argdo e!` to reload from disk."],
                     "`:argdo e!`."),
                ],
            },
        },
    ],
}
