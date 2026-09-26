---
up:
  - "[[Learning Map]]"
related:
  - "[[Bash]]"
  - "[[fzf]]"
  - "[[Git Worktree]]"
created: 2026-06-27
in:
  - "[[Library Map]]"
tags:
  - terminal
  - neovim
  - tmux
  - workflow
  - library
---

# Lesson 3: Neovim Power Editing — Operators, Text Objects, Macros

This is where vim becomes faster than any GUI editor. Come here after Lesson 2 feels natural.

> **Practice repo:** every exercise below runs against
> `Terminal Workflow/practice/nvim-drills/` — `cd` into it and `v .` (see that
> folder's `README.md` for one-time setup). Some exercises edit a file as
> part of the drill; each one says whether to keep the change or discard it
> with `:e!` (reload from disk). Lessons 6 and 7 reuse this same repo, so
> where a file needs to stay in its original "broken" state, discarding
> matters — don't skip that step.

---

## Operators + Motions = Power

Vim's secret: **operator + motion** combines into infinite commands.

### Operators

```
d                Delete
c                Change (delete + enter insert mode)
y                Yank (copy)
>                Indent right
<                Indent left
=                Auto-indent (fix indentation)
```

### Combine with any motion

```
dw               Delete word forward
db               Delete word backward
d$  or  D        Delete to end of line
d0               Delete to start of line
dG               Delete to end of file
dgg              Delete to start of file
cw               Change word (delete word, start typing)
c$  or  C        Change to end of line
yy               Yank (copy) whole line
yw               Yank word
y$               Yank to end of line
>>               Indent current line
<<               Unindent current line
5>>              Indent 5 lines
=G               Auto-indent from here to end of file
gg=G             Auto-indent the entire file
```

### Exercise 3.1: Bump the tax rate

Product wants the tax rate changed from 8% to 7.5%.

1. Open `src/orders.py`, jump to line 5 with `5G` — `TAX_RATE = 0.08`.
2. `dw` on `TAX_RATE` — deletes the word forward, leaving `= 0.08`. Press `u` to undo (that's not the task, just proving `dw` eats the word *and* the trailing space).
3. Move to `0.08` (`w` twice, or `f0`), press `cW`, type `0.075`, `Esc`.
   (`cW`, not `cw` — the dot splits `0.08` into three vim *words* (`0`, `.`, `08`),
   so `cw` would change only the leading `0` and leave you with `0.075.08`.
   `cW` operates on the whole space-delimited WORD.)

**Check yourself:** the line now reads `TAX_RATE = 0.075`. Discard with `:e!` — later lessons expect `0.08`.

---

## Text Objects (the killer feature)

Operate on structures — stuff inside brackets, quotes, tags. Pattern: `{operator}{a or i}{object}`

- `a` = "around" (includes the delimiters)
- `i` = "inside" (just the content)

### Change inside

```
ci(              Change inside parentheses: (hello) → () + insert
ci[              Change inside brackets: [1, 2, 3] → []
ci{              Change inside braces: { code } → {}
ci"              Change inside double quotes: "text" → ""
ci'              Change inside single quotes: 'text' → ''
ci`              Change inside backticks
ciw              Change inside word (replaces the word)
cit              Change inside HTML tag: <div>content</div> → <div></div>
```

### Delete / yank / select

```
di(              Delete inside parentheses (keeps the parens)
da(              Delete around parentheses (deletes parens too)
yi"              Yank (copy) inside quotes
ya{              Yank around braces (includes the braces)
vi{              Select inside braces (visual mode)
va"              Select around quotes
vip              Select inside paragraph
```

### All text objects

```
iw / aw          Word
iW / aW          WORD (includes punctuation)
is / as          Sentence
ip / ap          Paragraph
i) / a)          Parentheses (same as i( / a()
i] / a]          Brackets
i} / a}          Braces
i" / a"          Double quotes
i' / a'          Single quotes
it / at          HTML/XML tag
```

### Exercise 3.2: Reword an error message

1. Open `src/calculator.py`, search for the error: `/Cannot divide`.
2. Cursor lands inside `raise Exception("Cannot divide by zero")`. Press `ci"` — the text inside the quotes is deleted and you're in insert mode.
3. Type `Division by zero is not allowed`, `Esc`.

**Check yourself:** the line reads `raise Exception("Division by zero is not allowed")`. Discard with `:e!`.

### Exercise 3.3: Text objects on real data structures

Open `src/orders.py` and try these on the `build_order_book` function and the `RAW_ORDERS` list (undo/`:e!` after each, don't stack them):

```
di(   On Order(raw["id"], raw["items"], raw["discount"]) → empties the parens, keeps them
da(   Same line → deletes the parens AND their contents, "Order(...)" becomes "Order"
ci{   Cursor inside the first RAW_ORDERS entry {"id": "A1", ...} → clears the whole dict body
```

**Check yourself:** after `di(`, pressing `%` on the opening `(` should jump straight to the now-adjacent `)`. Run `:e!` before moving on — `RAW_ORDERS` is exercised again in Lessons 6 and 7 and needs its six original entries.

---

## Visual Mode

```
v                Character-wise (select chars)
V                Line-wise (select whole lines)
Ctrl-v           Block/column mode (vertical selection!)
```

After selecting, operate:
```
v3w              Select 3 words
Vj               Select 2 lines
V5j d            Select 6 lines and delete
Ctrl-v jjj I     Column insert: add text to multiple lines
Ctrl-v jjj d     Column delete: remove a column
vip              Select entire paragraph
vi{              Select inside braces
```

### Exercise 3.4: Comment out a batch of test orders

You want to temporarily disable orders A2–A5 while debugging, without touching A1 or A6.

1. Open `src/orders.py`, put the cursor on the `{"id": "A2", ...` line and press `^` so it sits on the opening `{` — block-insert happens at whatever column the cursor is in, so the column matters.
2. `Ctrl-v`, then `jjj` to extend the block down 3 more lines (4 lines selected: A2–A5).
3. `I`, type `# `, `Esc`.

**Check yourself:** lines for A2 through A5 now start with `# `; A1 and A6 are untouched. Discard with `:e!` — `RAW_ORDERS` needs all six live entries for later lessons.

---

## Macros (recording commands)

Record keystrokes. Replay them. Perfect for repetitive edits.

```
qa               Start recording macro into register 'a'
                 (do your edits...)
q                Stop recording
@a               Play macro 'a'
@@               Repeat last macro
5@a              Play macro 'a' 5 times
```

### Exercise 3.5: Fix a real bug with a macro

Open `src/calculator.py` and look at the `Person` class — none of its five
`__init__` fields have a `self.` prefix, so they're dead local variables
instead of attributes:

```python
def __init__(self):
    name = ""
    age = 0
    email = ""
    phone = ""
    address = ""
```

1. Cursor on `name` (first field line).
2. `qa` — start recording into register a.
3. `Iself.` — go to line start, insert `self.`.
4. `Esc` — back to normal mode.
5. `j` — move down to the next field.
6. `q` — stop recording.
7. `4@a` — replay on the remaining 4 lines (age, email, phone, address).

**Check yourself:** all five lines now read `self.<field> = ...`. This is a
genuine bug fix — feel free to keep it. If you'd rather leave the fixture
broken for a re-run later, discard with `:e!` instead.

---

## Search and Replace

```
:%s/old/new/g        Replace all in file
:%s/old/new/gc       Replace all with confirmation
:s/old/new/g         Replace on current line only
:%s/foo//g           Delete all "foo"
```

Useful patterns:
```
:%s/\s\+$//g         Remove trailing whitespace
:%s/^/# /g           Add "# " to start of every line
:%s/$/;/g            Add ";" to end of every line
```

### Exercise 3.6: Mark a batch of items done

Open `data/log.txt` — it has 10 lines like `item 1: pending` mixed with
`# TODO` comments and blank lines.

1. `:%s/pending/done/g`

**Check yourself:** `:%s/pending//gn` (the trailing `n` means "count, don't
replace") reports `0 matches`. Discard with `:e!` — Lesson 7's `:g`/`cgn`
drills use this same "pending" text on this same file.

---

## Indentation and Formatting

```
>>               Indent current line
<<               Unindent current line
5>>              Indent 5 lines
>}               Indent to next paragraph
==               Auto-indent current line
=G               Auto-indent from here to end of file
gg=G             Auto-indent entire file
=i{              Auto-indent inside braces
<Space>cf        Format file (language formatter: ruff, prettier, etc.)
```

In visual mode:
```
V5j >            Indent 6 selected lines
V5j <            Unindent
V5j =            Auto-indent
```

### Exercise 3.7: Clean up inconsistent indentation

Open `src/messy.py` — three functions and a class with deliberately
inconsistent (but valid) indentation.

1. `gg=G` — re-indents the whole file from the current LSP/treesitter rules.

**Check yourself:** every block now lines up on a consistent 4-space grid.
The file is still valid Python either way — confirm with
`:!python3 -m py_compile %`. Discard with `:e!` — Lesson 7 reuses this file
messy, on purpose, for its own multi-file drill.

---

## Registers (multiple clipboards)

Vim has 26 named registers (a-z) plus special ones:

```
"ayy             Yank line into register a
"ap              Paste from register a
"byy             Yank into register b
"bp              Paste from register b
"+y              Yank into system clipboard (Cmd+V works after)
"+p              Paste from system clipboard
:reg             See all registers
```

Special registers:
```
""               Last yanked/deleted text (default)
"0               Last yank (survives deletes!)
"+               System clipboard
".               Last inserted text
"%               Current filename
":               Last command
```

**Key pattern:** You yank text, then delete something (overwrites default register). Use `"0p` to paste what you originally yanked.

### Paste with auto-indentation

```
]p               Paste below, match indent level of current line
[p               Paste above, match indent level of current line
p then =']       Paste, then auto-indent the pasted block (proper reformat)
p then V']=      Paste, select pasted text, auto-indent (visual way)
```

`]p` matches the indent of the surrounding line (shallow fix). If you want full reformatting of the pasted code, do `p` then `=']` — that actually re-indents the pasted block correctly.

### Exercise 3.8: Registers survive an unrelated delete

Open `src/orders.py`.

1. Go to line 5 (`TAX_RATE = 0.08`), `"ayy` — yank it into register `a`.
2. Jump to the `{"id": "A3", ...}` line in `RAW_ORDERS`, `dd` — delete it (this only touches the *default* register, register `a` is untouched).
3. Move anywhere, `"ap` — paste from register `a`: the `TAX_RATE` line reappears.
4. `"0p` — paste from the "last yank" register: also the `TAX_RATE` line, proving `"0` survives deletes that a plain `p` would've lost it to.

**Check yourself:** `:reg a` and `:reg 0` both show `TAX_RATE = 0.08`. Discard everything with `:e!`.

---

## Marks (bookmarks)

```
ma               Set mark 'a' at cursor
'a               Jump to mark 'a' (line)
`a               Jump to mark 'a' (exact position)
''               Jump back to previous position
`.               Jump to last edit location
:marks           List all marks
```

Lowercase (a-z) = per-file. Uppercase (A-Z) = global (cross-file).

### Exercise 3.9: Bookmark across files

1. Open `src/calculator.py`, cursor on the `class Person:` line, press `mA` — sets a global (uppercase) mark.
2. Switch files: `<Space>sf` → open `src/orders.py`.
3. From anywhere in `orders.py`, press `'A` — jumps you straight back to the `Person` class line in `calculator.py`.

**Check yourself:** `:marks` lists `A` with `calculator.py` as its file. Uppercase marks are the reliable way to bookmark across files — lowercase marks are meant to stay within one file.

---

## Multi-file operations

```
:args **/*.py                  Load all Python files
:argdo %s/old/new/g | w       Replace across all
:bufdo %s/old/new/g | w       Replace across open buffers
:cdo s/old/new/g | w          Replace in quickfix results
```

Workflow: `<Space>/` to grep → `Ctrl-q` to send to quickfix → `:cdo s/old/new/g | w`

### Exercise 3.10: Touch every file in the project, safely

This drills the arglist mechanic without risking anything on disk — nothing
here is saved.

1. `:args src/*.py` — loads every `.py` directly under `src/` into the arglist: the four real modules plus the empty `__init__.py` (and `scratch.py` too, if the git drills have created it — globs don't curate for you).
2. `:args` — confirm they're all listed.
3. `:argdo $put ='# reviewed'` — appends a `# reviewed` line to the end of every loaded buffer. No `| w`, so this only exists in memory.
4. `:next` / `:prev` to flip through the buffers and see the marker at the bottom of each.

**Check yourself:** `:ls` — every arglist buffer now shows a `+` (modified; `:args` itself doesn't display modified-flags). Now throw
it all away before it ever touches disk: `:argdo e!` (reloads every buffer
from disk, discarding the in-memory edits). The full destructive form,
`:argdo %s/old/new/g | w`, is what you'd reach for once you actually want
the change saved — practice that version once you trust the arglist you've
built.

---

## Cheat sheet (print this)

| Intent | Keys | Example |
|--------|------|---------|
| Delete word | `dw` | `hello world` → `world` |
| Delete inside parens | `di(` | `func(arg1, arg2)` → `func()` |
| Change inside quotes | `ci"` | `"old"` → `""` + insert |
| Change word | `ciw` | replaces whole word |
| Delete to end of line | `D` | removes after cursor |
| Delete entire line | `dd` | line gone |
| Copy inside braces | `yi{` | copies between `{}` |
| Select inside block | `vi{` | highlights between `{}` |
| Indent 5 lines | `5>>` | pushes right |
| Auto-indent file | `gg=G` | fixes all indentation |
| Format file | `<Space>cf` | language formatter |
| Comment 5 lines | `Ctrl-v 4j I # Esc` | block insert |
| Repeat last edit | `.` | exact same change |
| Record macro | `qa ... q` | `@a` to replay |
| Paste from yank | `"0p` | even after deleting |
| System clipboard | `"+y` | works with Cmd+V |
| Jump bracket | `%` | `(` ↔ `)` |
| Jump to line 50 | `50G` | instant |
| Search & replace | `:%s/old/new/g` | whole file |

---

Back to: [[Library Map]] | [[Learning Map]]
