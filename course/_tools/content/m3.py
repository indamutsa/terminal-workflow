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
    "title": "Change, copy and replace text fast in Neovim",
    "footer": "Delete, change and copy text, edit columns, record macros, replace words, bookmark places, edit many files",
    "tagline": "Change words, repeat edits with macros, copy with registers, replace text in many files.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Delete, change and copy text with a few keys in Neovim",
            "subtitle": "Delete a word, change the text inside quotes, delete what is inside parentheses, fix the indentation of the whole file",
            "idea": (
                "Delete or change text in two or three keys: pick an operator, then a motion.",
                [
                    ("Delete a word", "dw", "d is the operator, w is the motion."),
                    ("Change the text inside quotes", "ci\"", "Deletes the text and lets you type a new one."),
                    ("Delete what is inside parentheses", "di(", "Keeps the parentheses."),
                    ("Fix the indentation of the whole file", "gg=G", "Runs = from the top to the bottom of the file."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I edit text without selecting it with the mouse or deleting one character at a time?",
                "fix": "Name the action and the target. `ci\"` changes the text inside the quotes, wherever the cursor sits in them.",
            },
            "drills": [
                {
                    "h2": "Delete, change, copy or indent text (operators and motions)",
                    "intro": "Find every practice file here in `Terminal-Workflow/practice/nvim-drills`. Autosave writes a file about 3 seconds after you stop typing, and when you leave the buffer, so `:e!` cannot bring the original back. Where an edit should not stay, press `u` to undo it. For a drill that must stay unsaved, run `:ASToggle` first and again after. To reset a file, run `git checkout -- <file>` in that folder.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Delete, change, copy or indent text (operators)", "rows": [
                            ("d", "Delete text"),
                            ("c", "Change text (delete it and start typing)"),
                            ("y", "Copy (yank) text"),
                            (">", "Indent text to the right"),
                            ("<", "Indent text to the left"),
                            ("=", "Fix the indentation (auto-indent)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Delete, change, copy or indent a word, a line or the rest of the file", "rows": [
                            ("dw", "Delete a word forward"),
                            ("db", "Delete a word backward"),
                            ("d$ or D", "Delete to the end of the line"),
                            ("d0", "Delete to the start of the line"),
                            ("dG", "Delete to the end of the file"),
                            ("dgg", "Delete to the start of the file"),
                            ("cw", "Change a word (delete it and start typing)"),
                            ("c$ or C", "Change to the end of the line"),
                            ("yy", "Copy (yank) the whole line"),
                            ("yw", "Copy (yank) a word"),
                            ("y$", "Copy (yank) to the end of the line"),
                            (">>", "Indent the current line"),
                            ("<<", "Unindent the current line"),
                            ("5>>", "Indent 5 lines"),
                            ("=G", "Auto-indent from here to the end of the file"),
                            ("gg=G", "Auto-indent the entire file"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Change a number in a line (tax rate 8% to 7.5%)", "code": C('''
5G
dw
u
f0
cW
0.075
Esc
'''),
                         "expect": "The line now reads `TAX_RATE = 0.075`. Press `u` to bring `0.08` back: later lessons expect it."},
                        {"type": "text", "body": "Open `src/orders.py` first. `dw` leaves `= 0.08`; `u` undoes it, as a proof that `dw` deletes the word and the space after it. To change a whole number, use `cW`, not `cw`: the dot splits `0.08` into three vim words, so `cw` would change only the leading `0` and leave `0.075.08`."},
                    ],
                },
                {
                    "h2": "Change or delete the text inside quotes, brackets and tags (text objects)",
                    "intro": "Change or delete what is inside brackets, quotes and tags. Type the operator, then `a` or `i`, then the object. `a` means around (includes the delimiters). `i` means inside (just the content).",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Change the text inside parentheses, brackets, quotes or a tag", "rows": [
                            ("ci(", "Change inside parentheses: (hello) → () + insert"),
                            ("ci[", "Change inside brackets: [1, 2, 3] → []"),
                            ("ci{", "Change inside braces: { code } → {}"),
                            ("ci\"", "Change inside double quotes: \"text\" → \"\""),
                            ("ci'", "Change inside single quotes: 'text' → ''"),
                            ("ci`", "Change inside backticks"),
                            ("ciw", "Change inside word (replaces the word)"),
                            ("cit", "Change inside HTML tag: <div>content</div> → <div></div>"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Delete, copy or select the text inside brackets and quotes", "rows": [
                            ("di(", "Delete inside parentheses (keeps the parens)"),
                            ("da(", "Delete around parentheses (deletes parens too)"),
                            ("yi\"", "Copy (yank) inside quotes"),
                            ("ya{", "Copy (yank) around braces (includes the braces)"),
                            ("vi{", "Select inside braces (visual mode)"),
                            ("va\"", "Select around quotes"),
                            ("vip", "Select inside a paragraph"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "See every text object: word, sentence, paragraph, quotes, tag", "rows": [
                            ("iw / aw", "Work on a word"),
                            ("iW / aW", "Work on a WORD (includes punctuation)"),
                            ("is / as", "Work on a sentence"),
                            ("ip / ap", "Work on a paragraph"),
                            ("i) / a)", "Work on parentheses (same as i( / a()"),
                            ("i] / a]", "Work on brackets"),
                            ("i} / a}", "Work on braces"),
                            ("i\" / a\"", "Work on double quotes"),
                            ("i' / a'", "Work on single quotes"),
                            ("it / at", "Work on an HTML/XML tag"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Change the text inside quotes (reword an error message)", "code": C('''
/Cannot divide
ci"
Division by zero is not allowed
Esc
'''),
                         "expect": "The line reads `raise Exception(\"Division by zero is not allowed\")`. Press `u` to undo it."},
                        {"type": "text", "body": "To put the cursor inside quotes, search for the text. Open `src/calculator.py` first. The search leaves the cursor inside `raise Exception(\"Cannot divide by zero\")`."},
                        {"type": "keys", "where": "nvim", "title": "Empty or remove a function call's arguments on real code", "rows": [
                            ("di(", "Empty the parentheses of Order(raw[\"id\"], raw[\"items\"], raw[\"discount\"]) and keep them"),
                            ("da(", "Delete the parentheses AND their contents on the same line, so Order(...) becomes Order"),
                            ("ci{", "Clear the whole dict body: put the cursor inside the first RAW_ORDERS entry {\"id\": \"A1\", ...}"),
                        ], "try": "In `src/orders.py`, use these on `build_order_book` and the `RAW_ORDERS` list. Press `u` after each. After `di(`, press `%` on the opening `(`.",
                         "expect": "The cursor jumps straight to the now-adjacent `)`. Press `u` before moving on: `RAW_ORDERS` needs its six original entries."},
                    ],
                },
            ],
            "rules": {
                "h2": "How to build any edit: operator, then a or i, then an object",
                "cards": [
                    ("Build any edit: operator + a or i + object", "Say it as one sentence: the action, inside or around, the object.", ["Part", "Meaning"], [
                        ["`d` `c` `y`", "The action: delete, change, copy (yank)"],
                        ["`i`", "Inside: just the content"],
                        ["`a`", "Around: includes the delimiters"],
                        ["`w` `(` `\"` `{` `t`", "The object: word, parens, quotes, braces, tag"],
                    ]),
                    ("Why does cw leave 0.075.08 when I change a number?", "Vim sees the dot as a word break, so a number is three words.", ["Keys", "Result on `0.08`"], [
                        ["`cw` then `0.075`", "`0.075.08`"],
                        ["`cW` then `0.075`", "`0.075`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Delete the arguments of a function call, then undo it",
                "frame": "How do I delete what is inside the parentheses of a call and keep the parentheses?",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 19, on `(`", "`19G` `f(`"), "`di(`", "Deletes the arguments and keeps the parentheses."),
                    (("on the `(`", "`F(`"), "`%`", "Jumps to the matching `)`."),
                    (None, "`u`", "Undoes the delete and restores the line."),
                ],
                "before": "total = calc_totl(price, qty)",
                "after": "total = calc_totl()",
                "meaning": "The cursor only has to be inside the parentheses. Use `da(` to delete the parentheses too.",
            },
            "practice": {
                "h2": "Check yourself: delete, change and copy with operators and text objects",
                "qs": [
                    ("Mechanism", "Why does `ci\"` work when my cursor is in the middle of the quotes?",
                     "The object is the quotes, not the cursor.",
                     ["`i\"` means the text inside the nearest double quotes.", "`c` deletes it and enters insert mode."],
                     "A text object covers the whole structure around the cursor."),
                    ("Keystrokes", "How do I delete the parentheses and what is inside them?",
                     "Around, not inside.",
                     ["Put the cursor inside the parens.", "Press `da(`."],
                     "`da(`."),
                    ("Application", "How do I change `8%` to `7.5%` on the `TAX_RATE = 0.08` line?",
                     "Whole WORD, not word.",
                     ["Move to `0.08` with `f0`.", "Press `cW`, type `0.075`, press `Esc`."],
                     "`cW` then `0.075`."),
                    ("Common mistake", "Why did `cw` on `0.08` leave me with `0.075.08`?",
                     "How does vim see the dot?",
                     ["A word stops at the dot.", "`cw` changed only the leading `0`.", "Use `cW` for the whole space-delimited WORD."],
                     "Use `cW`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Change many lines at once: select, record a macro, replace",
            "subtitle": "Select lines or a column, comment out several lines, repeat an edit with a macro, replace a word in the whole file",
            "idea": (
                "Change many lines at once: select them, record a macro, or replace text.",
                [
                    ("Select whole lines", "V", "Line-wise visual mode."),
                    ("Edit the same column on many lines", "Ctrl-v", "Block mode edits many lines at once."),
                    ("Record an edit to repeat it", "qa", "Records into register a. Press q to stop."),
                    ("Replace a word in the whole file", ":%s/old/new/g", "Whole file, every match."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I make the same fix on five lines, or change a word that appears fifty times, without editing each one by hand?",
                "fix": "Use a column insert for the same prefix, a macro for the same edit, and `:%s` for the same word.",
            },
            "drills": [
                {
                    "h2": "Select text, lines or a column before you edit (visual mode)",
                    "intro": "Select the text first, then delete, change or copy it.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Select characters, whole lines or a column", "rows": [
                            ("v", "Select characters (character-wise)"),
                            ("V", "Select whole lines (line-wise)"),
                            ("Ctrl-v", "Select a block or column (vertical selection!)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Select words, lines or a column, then edit them", "rows": [
                            ("v3w", "Select 3 words"),
                            ("Vj", "Select 2 lines"),
                            ("V5j d", "Select 6 lines and delete them"),
                            ("Ctrl-v jjj I", "Add text to many lines at once (column insert)"),
                            ("Ctrl-v jjj d", "Remove a column (column delete)"),
                            ("vip", "Select the entire paragraph"),
                            ("vi{", "Select inside braces"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Comment out four lines at once (orders A2 to A5)", "code": C('''
^
Ctrl-v
jjj
I
#
Esc
'''),
                         "expect": "Lines for A2 through A5 now start with `# `. A1 and A6 are untouched. Press `u` to undo it: `RAW_ORDERS` needs all six live entries."},
                        {"type": "text", "body": "Put the cursor in the right column before you start. Open `src/orders.py` and put the cursor on the `{\"id\": \"A2\", ...` line. `^` puts it on the opening `{`. A block insert happens at the cursor's column, so the column matters."},
                    ],
                },
                {
                    "h2": "Repeat the same edit on many lines with a macro",
                    "intro": "Record your keystrokes once, then replay them on every line that needs the same edit.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Record, replay and repeat a macro", "rows": [
                            ("qa", "Start recording a macro into register 'a' (do your edits...)"),
                            ("q", "Stop recording"),
                            ("@a", "Play macro 'a'"),
                            ("@@", "Repeat the last macro"),
                            ("5@a", "Play macro 'a' 5 times"),
                        ]},
                        {"type": "text", "body": "Why are my class fields not attributes? In `src/calculator.py`, the `Person` class has five `__init__` fields with no `self.` prefix. They are dead local variables instead of attributes."},
                        {"type": "code", "file": "src/calculator.py", "title": "Fields missing the self. prefix (the bug)", "code": PERSON_INIT},
                        {"type": "cmd", "where": "nvim", "title": "Add self. to the start of five lines with a macro", "code": C('''
qa
Iself.
Esc
j
q
4@a
'''),
                         "expect": "All five lines now read `self.<field> = ...`. This is a genuine bug fix: keep it, or press `u` until the fields read as before to leave the fixture broken for a re-run."},
                        {"type": "text", "body": "Start with the cursor on `name`. `Iself.` goes to the start of the line and inserts `self.`. `j` moves to the next field. `4@a` replays the macro on the remaining four lines (age, email, phone, address)."},
                    ],
                },
                {
                    "h2": "Replace a word in the whole file (search and replace)",
                    "intro": "Replace text in the whole file with `:%s`. Add `c` to confirm each change.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Replace a word in the file, on one line, or delete it", "rows": [
                            (":%s/old/new/g", "Replace all in the file"),
                            (":%s/old/new/gc", "Replace all and confirm each change"),
                            (":s/old/new/g", "Replace on the current line only"),
                            (":%s/foo//g", "Delete all \"foo\""),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Remove trailing spaces or add text to every line", "rows": [
                            (":%s/\\s\\+$//g", "Remove trailing whitespace"),
                            (":%s/^/# /g", "Add \"# \" to the start of every line"),
                            (":%s/$/;/g", "Add \";\" to the end of every line"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Replace pending with done in the whole file, then count what is left", "code": C('''
:%s/pending/done/g
:%s/pending//gn
'''),
                         "expect": "The count command (trailing `n` means count, don't replace) reports `0 matches`. Press `u` to undo it: Lesson 7 uses this same \"pending\" text."},
                        {"type": "text", "body": "Open `data/log.txt` first. It has ten lines like `item 1: pending`, mixed with `# TODO` comments and blank lines."},
                    ],
                },
            ],
            "rules": {
                "h2": "Record a macro, copy to a register, comment out lines: keys at a glance",
                "cards": [
                    ("Record a macro or copy into a named register", "Record and replay a macro, copy to named registers, use the clipboard.", ["Keys", "Action"], [
                        ["`qa...q`", "Record a macro into 'a'"],
                        ["`@a / 5@a`", "Play the macro / 5 times"],
                        ["`\"ayy/\"ap`", "Copy (yank) to / paste from register a"],
                        ["`\"+y/\"+p`", "Copy to / paste from the system clipboard"],
                        ["`\"0p`", "Paste the last yank (survives deletes)"],
                    ]),
                    ("Comment out five lines", "A column insert takes a few keys and a prefix.", ["Keys", "Result"], [
                        ["`Ctrl-v 4j I # Esc`", "Block insert `# ` on 5 lines"],
                        ["`:%s/^/# /g`", "Add the same prefix to every line"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Add a prefix to four lines with one macro",
                "frame": "How do I add an `order_` prefix to four assignments?",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 15, on `name`", "`15G`"), "`qa` `I` then `order_` then `Esc` `j` `q`", "Records one edit into register a and ends on the next line."),
                    (None, "`3@a`", "Replays it on lines 16 to 18."),
                    (None, "`u` until the original lines are back", "Undoes the edit. Autosave then writes the original back."),
                ],
                "before": 'name = "pen"\nqty = 3\nprice = 2.50\nnote = "rush"',
                "after": 'order_name = "pen"\norder_qty = 3\norder_price = 2.50\norder_note = "rush"',
                "meaning": "End the macro on the next line so it chains: record one clean edit and let the count repeat it.",
            },
            "practice": {
                "h2": "Check yourself: select, macros and replace",
                "qs": [
                    ("Mechanism", "Why does `4@a` fix four more lines after I edited one?",
                     "What did the macro end on?",
                     ["The macro ended with `j`, on the next line.", "Each replay starts where the last one stopped."],
                     "The macro moves to the next line, so replays chain."),
                    ("Keystrokes", "How do I add `# ` to the start of four lines in a column?",
                     "Block mode, then insert.",
                     ["Press `Ctrl-v` and `jjj`.", "Press `I`, type `# `, press `Esc`."],
                     "`Ctrl-v jjj I`, `# `, `Esc`."),
                    ("Application", "How do I replace `pending` with `done` everywhere and then count what is left?",
                     "Substitute, then substitute with `n`.",
                     ["Run `:%s/pending/done/g`.", "Run `:%s/pending//gn`."],
                     "The count reports `0 matches`."),
                    ("Common mistake", "Why did my block insert land in the wrong column?",
                     "Where does the block start?",
                     ["Block insert uses the cursor's column.", "Press `^` first to sit on the first non-blank."],
                     "The cursor column matters. Press `^` before `Ctrl-v`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Fix indentation, copy with registers, bookmark places, edit many files",
            "subtitle": "Fix a badly indented file, paste after a delete, copy to the system clipboard, jump back to a bookmarked line, replace text in many files",
            "idea": (
                "Fix indentation in one key, keep many clipboards, jump to bookmarks, edit many files.",
                [
                    ("Fix the indentation of the whole file", "gg=G", "Fixes indentation everywhere."),
                    ("Copy a line into its own clipboard", "\"ayy", "Yanks (copies) a line into register a."),
                    ("Bookmark a line and jump back from any file", "mA", "Jump back from any file with 'A."),
                    ("Change text in many files", ":args src/*.py", "Load the files, then run :argdo."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why is my pasted text indented wrong, why did a delete wipe what I copied, and why does my bookmark only work in one file?",
                "fix": "Re-indent with `gg=G`, paste the last yank (copy) with `\"0p`, and use an uppercase mark such as `mA` across files.",
            },
            "drills": [
                {
                    "h2": "Fix the indentation of a file or a block of lines",
                    "intro": "Use `src/messy.py`: it has three functions and a class with deliberately inconsistent, but valid, indentation.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Indent, unindent or auto-indent lines", "rows": [
                            (">>", "Indent the current line"),
                            ("<<", "Unindent the current line"),
                            ("5>>", "Indent 5 lines"),
                            (">}", "Indent to the next paragraph"),
                            ("==", "Auto-indent the current line"),
                            ("=G", "Auto-indent from here to the end of the file"),
                            ("gg=G", "Auto-indent the entire file"),
                            ("=i{", "Auto-indent inside braces"),
                            ("<Space>cf", "Format the file with its language formatter (ruff, prettier, etc.)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Indent or auto-indent the lines you selected", "rows": [
                            ("V5j >", "Indent 6 selected lines"),
                            ("V5j <", "Unindent the selected lines"),
                            ("V5j =", "Auto-indent the selected lines"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Fix inconsistent indentation in a Python file", "code": C('''
gg=G
:!python3 -m py_compile %
'''),
                         "expect": "Every block lines up on a consistent 4-space grid. The file is valid Python either way. Press `u` to undo it: Lesson 7 reuses this file messy, on purpose."},
                    ],
                },
                {
                    "h2": "Copy and paste with many clipboards (registers)",
                    "intro": "Vim has 26 named registers (a-z) plus special ones. If you copy (yank) something and then delete something else, the default register is overwritten. `\"0p` pastes what you originally yanked.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Copy and paste with a named register or the system clipboard", "rows": [
                            ("\"ayy", "Copy (yank) a line into register a"),
                            ("\"ap", "Paste from register a"),
                            ("\"byy", "Copy (yank) a line into register b"),
                            ("\"bp", "Paste from register b"),
                            ("\"+y", "Copy (yank) into the system clipboard (Cmd+V works after)"),
                            ("\"+p", "Paste from the system clipboard"),
                            (":reg", "See all registers"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "See what the special registers hold: last yank, clipboard, filename", "rows": [
                            ("\"\"", "Use the last yanked or deleted text (default)"),
                            ("\"0", "Use the last yank (survives deletes!)"),
                            ("\"+", "Use the system clipboard"),
                            ("\".", "Use the last inserted text"),
                            ("\"%", "Use the current filename"),
                            ("\":", "Use the last command"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Paste text and match the indentation", "rows": [
                            ("]p", "Paste below and match the indent of the current line"),
                            ("[p", "Paste above and match the indent of the current line"),
                            ("p then =']", "Paste, then auto-indent the pasted block (proper reformat)"),
                            ("p then V']=", "Paste, select pasted text, auto-indent (visual way)"),
                        ]},
                        {"type": "text", "body": "Pasted text indented wrong? `]p` matches the indent of the surrounding line, a shallow fix. For full reformatting, do `p` then `=']`."},
                        {"type": "cmd", "where": "nvim", "title": "Paste your copy after you delete another line", "code": C(r'''
5G
"ayy
/A3
dd
"ap
"0p
:reg a
:reg 0
'''),
                         "expect": "`:reg a` and `:reg 0` both show `TAX_RATE = 0.08`. Press `u` three times to undo it all."},
                    ],
                },
                {
                    "h2": "Bookmark a line and jump back to it (marks)",
                    "intro": "Lowercase marks (a-z) work in one file. Uppercase marks (A-Z) are global: they work across files.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Set a bookmark, jump to it, list all bookmarks", "rows": [
                            ("ma", "Set mark 'a' at the cursor"),
                            ("'a", "Jump to mark 'a' (line)"),
                            ("`a", "Jump to mark 'a' (exact position)"),
                            ("''", "Jump back to the previous position"),
                            ("`.", "Jump to the last edit location"),
                            (":marks", "List all marks"),
                        ], "try": "In `src/calculator.py`, put the cursor on `class Person:` and press `mA`. Open `src/orders.py` with `<Space>sf`, then press `'A`.",
                         "expect": "`'A` jumps back to the `Person` class line in `calculator.py`. `:marks` lists `A` with `calculator.py` as its file."},
                    ],
                },
                {
                    "h2": "Change text in many files at once",
                    "intro": "Search with `<Space>/`, press `Ctrl-q` to send the results to quickfix, then run `:cdo s/old/new/g | w`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Replace text in many files, open buffers or search results", "rows": [
                            (":args **/*.py", "Load all Python files"),
                            (":argdo %s/old/new/g | w", "Replace across all the loaded files"),
                            (":bufdo %s/old/new/g | w", "Replace across open buffers"),
                            (":cdo s/old/new/g | w", "Replace in quickfix results"),
                        ]},
                        {"type": "cmd", "where": "nvim", "title": "Edit every Python file, then undo it safely", "code": C('''
:ASToggle
:args src/*.py
:args
:next
:prev
:argdo $put ='# reviewed'
:ls
:argdo e!
:ASToggle
'''),
                         "expect": "`:ASToggle` pauses autosave. `:ls` shows a `+` on every arglist buffer: modified in memory only, since there is no `| w`. `:argdo e!` reloads every buffer from disk and discards the edits, because nothing was written. The last `:ASToggle` turns autosave back on."},
                        {"type": "text", "body": "Which files does `:args src/*.py` load? The four real modules plus the empty `__init__.py` (and `scratch.py` if the git drills created it). `:next` and `:prev` flip through the buffers and show the marker at the bottom of each. Run them before the edit: with autosave on, leaving a changed buffer writes it. Use the full form, `:argdo %s/old/new/g | w`, when you want the change saved."},
                    ],
                },
            ],
            "rules": {
                "h2": "Find the key for an edit: delete, change, copy, indent, replace",
                "cards": [
                    ("Find the key for an edit (cheat sheet)", "What you want to do, the keys, and what happens.", ["Intent", "Keys", "Example"], [
                        ["Delete a word", "`dw`", "`hello world` → `world`"],
                        ["Delete inside parentheses", "`di(`", "`func(arg1, arg2)` → `func()`"],
                        ["Change the text inside quotes", "`ci\"`", "`\"old\"` → `\"\"` + insert"],
                        ["Change a word", "`ciw`", "replaces the whole word"],
                        ["Delete to the end of the line", "`D`", "removes everything after the cursor"],
                        ["Delete the entire line", "`dd`", "line gone"],
                        ["Copy inside braces", "`yi{`", "copies between `{}`"],
                        ["Select inside a block", "`vi{`", "highlights between `{}`"],
                        ["Indent 5 lines", "`5>>`", "pushes them right"],
                        ["Auto-indent the file", "`gg=G`", "fixes all indentation"],
                        ["Format the file", "`<Space>cf`", "language formatter"],
                        ["Comment out 5 lines", "`Ctrl-v 4j I # Esc`", "block insert"],
                        ["Repeat the last edit", "`.`", "exact same change"],
                        ["Record a macro", "`qa ... q`", "`@a` to replay"],
                        ["Paste your last copy (yank)", "`\"0p`", "even after deleting"],
                        ["Copy to the system clipboard", "`\"+y`", "works with Cmd+V"],
                        ["Jump to the matching bracket", "`%`", "`(` ↔ `)`"],
                        ["Jump to line 50", "`50G`", "instant"],
                        ["Search and replace", "`:%s/old/new/g`", "whole file"],
                    ]),
                    ("Which mark jumps between files?", "Lowercase stays in the file. Uppercase crosses files.", ["Mark", "Scope"], [
                        ["`ma`", "This file only"],
                        ["`mA`", "Global: jump back with `'A` from any file"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Paste your copy after you deleted another line",
                "frame": "How do I paste a line I copied after I deleted another line?",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 1", "`gg`"), '`yy` then `"ayy`', "Yanks the line into register 0 and into register a."),
                    (("line 18", "`18G`"), "`dd`", "Deletes the `note` line. Only the default register changes."),
                    (None, '`"ap`', "The `TAX_RATE` line is pasted below."),
                    (None, '`"0p`', 'The same line again: `"0` survives deletes.'),
                    (None, "`u` three times", "Undoes the paste, the second paste and the delete. Autosave writes the original back."),
                ],
                "before": 'note = "rush"\ntotal = calc_totl(price, qty)',
                "after": "total = calc_totl(price, qty)\nTAX_RATE = 0.08\nTAX_RATE = 0.08",
                "meaning": 'Copy into a named register or use `"0`, and later deletes cannot overwrite your yank.',
            },
            "practice": {
                "h2": "Check yourself: indent, registers and marks",
                "qs": [
                    ("Mechanism", "Why does `p` paste the line I deleted instead of the one I copied?",
                     "Deletes use the default register too.",
                     ["A delete overwrites the default register.", "`\"0` holds the last yank."],
                     "Use `\"0p` to paste the last yank."),
                    ("Keystrokes", "How do I re-indent the whole file?",
                     "Top, then auto-indent to the end.",
                     ["Press `gg` to go to the top.", "Press `=G`."],
                     "`gg=G`."),
                    ("Application", "How do I bookmark `class Person:` in one file and jump back to it from another?",
                     "Uppercase mark.",
                     ["Press `mA` on the class line.", "Open another file.", "Press `'A`."],
                     "`mA`, then `'A`."),
                    ("Common mistake", "My files show `+` after `:argdo` and I do not want the edits. What do I run?",
                     "Nothing was saved.",
                     ["The edits live in memory only while autosave is paused (`:ASToggle`).", "Then `:argdo e!` reloads from disk. If autosave already wrote them, undo with `u` in each buffer."],
                     "`:argdo e!`, with autosave paused."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Change every copy of a word or rename a variable (Cmd+D in Neovim)",
            "subtitle": "Do VS Code's Cmd+D in Neovim, change every copy of a word at once, edit many lines together, rename a variable in every file",
            "idea": (
                "Change many copies of a word: search it once, then let one key change each copy.",
                [
                    ("Change a word one copy at a time", "* cgn .", "Cmd+D, the Vim way."),
                    ("Change every copy of a word at once", ":%s//new/g", "Reuses the word you just searched."),
                    ("Edit the same column on many lines", "Ctrl-v", "Edit many lines together."),
                    ("Rename a variable in every file", "<Space>cr", "Every file, real references only."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I change a name that appears five times? In VS Code I press Cmd+D five times. In Neovim I retype the same change five times.",
                "fix": "Search the word with `*`, change the first copy with `cgn`, then press `.` for each next copy. Or change them all with `:%s//new/g`.",
            },
            "drills": [
                {
                    "h2": "Change a word one copy at a time (Cmd+D in VS Code)",
                    "intro": "Search the word under the cursor with `*`, change the next match with `cgn`, then press `.` to repeat it on the one after.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Search a word, change the next copy, repeat", "rows": [
                            ("*", "Search the word under the cursor and jump to the next copy"),
                            ("#", "Search the same word and jump backward"),
                            ("gn", "Select the next match"),
                            ("cgn", "Change the next match"),
                            (".", "Repeat the change on the next copy"),
                            ("n", "Jump to the next copy without changing it"),
                            ("dgn", "Delete the next match"),
                            ("u", "Undo one change"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Search any selected text, not only a word", "rows": [
                            ("v ... *", "Select text, then `*` searches exactly that text"),
                        ], "try": "In `~/tw/notes.md` press `3G`, `fR`, `w`, `v`, `ee`, then `*`.",
                         "expect": "The cursor jumps to `Orders ship` at the start of line 3. The words you selected are now the search, so `cgn` would change them."},
                        {"type": "text", "body": "Open the file with `nvim ~/tw/orders.py`. `*` jumps to the next copy of the word, so the first `cgn` changes line 19 and the dots go on from there."},
                        {"type": "cmd", "where": "nvim", "title": "Rename a variable in one file (qty to quantity)", "code": C('''
16G
*
cgn
quantity
Esc
.
.
.
.
'''),
                         "expect": "All five `qty` words now read `quantity`: lines 6, 7, 16, 19 and 20. The search wraps from the end of the file back to the top. Press `u` five times to undo it."},
                        {"type": "text", "body": "Why use `cgn` and not `ciw`? After `ciw`, `.` changes the word under the cursor again, so the cursor must walk to the next copy first. After `cgn`, `.` finds the next copy itself."},
                        {"type": "text", "body": "How do I skip a copy? `.` changes the copy you stand on, or the next one if you are not on a copy. To skip one, press `n` to land on it, then `n` again to pass it, then `.`."},
                    ],
                },
                {
                    "h2": "Change every copy of a word at once (Cmd+Shift+L in VS Code)",
                    "intro": "Change all copies with an empty pattern, which means the last search. Press `*`, then substitute with nothing between the slashes.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Replace every copy of a word, ask first, or only count them", "rows": [
                            (":%s//new/g", "Change every copy of the word you just searched"),
                            (":%s/\\<old\\>/new/g", "Change the same copies, with the word typed out"),
                            (":%s/old/new/gc", "Ask before each change: y yes, n no, a all, q quit, l last"),
                            ("Ctrl-r Ctrl-w", "Put the word under the cursor into the command line"),
                            (":%s//new/gn", "Count the copies without changing them"),
                            ("\\C", "Match upper and lower case exactly (use inside the pattern)"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Replace a word on one line or in the selected lines only", "rows": [
                            (":s/old/new/g", "Change the copies on this line only"),
                            (":'<,'>s/old/new/g", "Change the copies in the selected lines"),
                            (":'<,'>s/\\%Vold/new/g", "Change the copies only inside the selected characters or block"),
                            ("&", "Repeat the last `:s` on this line"),
                            ("g&", "Repeat it on every line, with the last search"),
                        ]},
                        {"type": "text", "body": "Can I see the change before I press Enter? Yes: as you type a `:s` command, Neovim previews the change in the file. Press `Esc` to cancel."},
                        {"type": "cmd", "where": "nvim", "title": "Rename a variable everywhere in the file (price to cost)", "code": C('''
17G
*
:%s//cost/g
'''),
                         "expect": "Neovim reports `5 substitutions on 5 lines`: lines 6, 7, 17, 19 and 20. `PRICES` on lines 3 and 12 is untouched, because `*` matches whole words. Press `u` to undo it."},
                    ],
                },
                {
                    "h2": "Edit many lines at once (Alt+Click, Cmd+Option+Down in VS Code)",
                    "intro": "Add the same text to a run of lines with a column edit. Do it to every matching line with `:g` and `norm`.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Add or change text in a column on many lines", "rows": [
                            ("Ctrl-v", "Start a column, then `j` to extend it down"),
                            ("I", "Insert before the column on every line"),
                            ("A", "Append after the column on every line"),
                            ("$A", "Append at the end of each line, even when lines differ in length"),
                            ("c", "Change the whole column"),
                            ("r", "Replace every selected character with one you type"),
                            ("o", "Jump to the other corner"),
                            ("gv", "Select the last selection again"),
                        ]},
                        {"type": "keys", "where": "nvim", "title": "Add text to every line that matches a word", "rows": [
                            (":g/pat/norm A text", "Run `A text` on every line that matches `pat`"),
                        ]},
                        {"type": "text", "body": "Open the file with `nvim ~/tw/todo.txt`. Lines 1 to 10 are `item N: pending`, and `item 10` is longer than the rest."},
                        {"type": "cmd", "where": "nvim", "title": "Add text to the end of ten lines", "code": C('''
gg
Ctrl-v
9j
$
A
 (done)
Esc
'''),
                         "expect": "Lines 1 to 10 end with `pending (done)`, including `item 10`. Without the `$`, `A` would append after the first column, and the text would land inside the word `item`. Press `u` to undo it."},
                        {"type": "cmd", "where": "nvim", "title": "Add text to the end of every TODO line", "code": C('''
:g/TODO/norm A !
'''),
                         "expect": "The three `TODO` lines (12, 14 and 16) end with ` !`. The `buy` lines are untouched. Press `u` to undo it."},
                    ],
                },
                {
                    "h2": "Rename a function or variable in every file (F2, Cmd+Shift+H in VS Code)",
                    "intro": "Rename the real symbol, not just matching text: the language server renames it in every file, and grug-far replaces text across files.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Rename a symbol or replace text across files", "rows": [
                            ("<Space>cr", "Rename a symbol in every file: type the new name, then Enter"),
                            ("grn", "Rename a symbol with Neovim's built-in rename (same as `<Space>cr`)"),
                            ("<Space>sr", "Replace text across files: open the search and replace panel (grug-far). On a word it fills that word; in visual mode it fills the selection"),
                            ("]]", "Jump to the next copy of the word under the cursor"),
                            ("[[", "Jump to the previous copy"),
                        ], "try": "In `~/tw/orders.py` press `6G`, `fq`, wait a moment, then `]]`.",
                         "expect": "Every `qty` in the file is highlighted. `]]` moves the cursor to the next one, on line 7. `[[` moves back."},
                        {"type": "text", "body": "Rename step by step: module 5 teaches `<Space>cr` and `<Space>sr` with the same `orders.py` rename."},
                        {"type": "text", "body": "How do I get multiple cursors like VS Code? A plugin called multicursor.nvim brings them to Neovim. It is not installed here, and the keys above do the same jobs."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which keys should I use to change many copies of a word?",
                "cards": [
                    ("Pick a way to change many copies, by job size", "Match the size of the job to the keys.", ["The job", "Use"], [
                        ["A few copies, you choose each", "`*` `cgn` `.` (`n` skips)"],
                        ["Every copy in the file", "`*` then `:%s//new/g`"],
                        ["Some copies, reviewed one by one", "`:%s/old/new/gc`"],
                        ["A code symbol in every file", "`<Space>cr`"],
                        ["Text across the project", "`<Space>sr`"],
                        ["The same column on many lines", "`Ctrl-v`"],
                        ["Edits that differ per line", "A macro: `qa` ... `q`"],
                    ]),
                    ("Find the Neovim keys for a VS Code shortcut", "Look up the VS Code shortcut you know and type its Neovim keys.", ["VS Code", "Neovim"], [
                        ["Cmd+D", "`*` `cgn` `.`"],
                        ["Cmd+K Cmd+D (skip one)", "`n`"],
                        ["Cmd+Shift+L", "`*` then `:%s//new/g`"],
                        ["Cmd+F2 (change all occurrences)", "`*` then `:%s//new/g`"],
                        ["F2", "`<Space>cr`"],
                        ["Cmd+Shift+H", "`<Space>sr`"],
                        ["Option+Click, Cmd+Option+Down", "`Ctrl-v` then `j`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Rename a variable in one file with cgn",
                "frame": "How do I rename `qty`, which appears five times, to `quantity`?",
                "open": "nvim ~/tw/orders.py",
                "steps": [
                    (("line 16, on `qty`", "`16G`"), "`*`", "Searches for `qty` and jumps to line 19."),
                    (None, "`cgn` `quantity` `Esc`", "Changes the match on line 19."),
                    (None, "`.` four times", "Changes lines 20, 6, 7 and then 16. The search wraps to the top."),
                    (None, "`u` five times", "Undoes the edit. Autosave then writes the original back."),
                ],
                "before": "total = calc_totl(price, qty)\nprint(name, qty, price, note, total)",
                "after": "total = calc_totl(price, quantity)\nprint(name, quantity, price, note, total)",
                "meaning": "The first `cgn` changes one copy, and each `.` finds the next, so one clean edit becomes five.",
            },
            "practice": {
                "h2": "Check yourself: change every copy of a word",
                "qs": [
                    ("Mechanism", "Why does `.` after `cgn` move on to the next copy by itself?",
                     "What does `gn` select?",
                     ["`gn` selects the next match.", "`.` repeats `cgn`, so it changes the next match."],
                     "`.` repeats `cgn`, which finds the next match itself. After `ciw`, `.` stays on the cursor."),
                    ("Keystrokes", "I changed one copy with `cgn`. How do I skip the next copy and change the one after?",
                     "`n` moves without changing.",
                     ["Press `n` to land on the next copy.", "Press `n` again to pass it.", "Press `.`."],
                     "`n` `n` `.`."),
                    ("Application", "How do I rename the loop variable `code` on lines 11 and 12 without touching `codes`?",
                     "Whole words only.",
                     ["Press `11G`, then `fc` to land on `code`.", "Press `*`, then `cgn`, the new name and `Esc`.", "Press `.` twice."],
                     "`*` matches whole words, so `codes` stays. Three copies change."),
                    ("Common mistake", "Why does my next edit land in the wrong place when I rename with `cw` and `.`?",
                     "Where does `.` act?",
                     ["`.` repeats at the cursor.", "Only `cgn` finds the next match for you."],
                     "Use `cgn`, not `cw`, so each `.` jumps to the next copy."),
                ],
            },
        },
    ],
}
