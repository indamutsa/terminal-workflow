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

# Lesson 7: Neovim Expert — Advanced Techniques

Things that separate power users from everyone else. Learn these once you're comfortable with Lessons 2-3 and 6.

> **Practice codebase:** every drill below runs against `Terminal Workflow/practice/nvim-drills`
> (the same project used in Lessons 2, 3, and 6). `cd` into it and run `nvim .` to start. One-time
> setup and the `reset-dirty.sh` script are documented in that folder's `README.md`.
>
> **Discard-after, unless a step says otherwise:** Lesson 6 does the "real", permanent fixes to this
> codebase — renaming `calc` → `calculate_total`, `TAX_RATE` → `SALES_TAX_RATE`, removing the unused
> imports, and fixing the off-by-one bug in `qualifies_for_free_shipping`. Everything below is
> throwaway practice reps: undo (`u`) or reload the file from disk (`:e!`) once you've seen the
> mechanic work. It doesn't matter whether you've done Lesson 6 yet — none of these drills depend on
> it except where called out explicitly.

---

## Advanced Motions & Operators

### Count + operator + motion

Everything takes a count:
```
3dw              Delete 3 words
5j               Move down 5 lines
2ci"             Change inside the 2nd outer quotes
d/pattern        Delete until pattern match
c/foo            Change everything until "foo"
y?bar            Yank backwards until "bar"
```

### Exercise 7.1: Edit the 2nd order in a list without counting characters

Open `src/orders.py` and find the `RAW_ORDERS` list. The `A4` line has *six* separate quoted
strings on it:

```python
{"id": "A4", "items": [{"price": 8, "qty": 3}], "discount": 2},
```

1. Put your cursor anywhere before the first `"` on the line (e.g. column 0).
2. `2ci"` — this jumps to the **2nd** quoted string on the line (`"A4"`) and puts you in insert
   mode inside it. Type `A4-REVIEW`, `Esc`.
3. Undo it: `u`.
4. Now try `3dw` from the start of the line — it deletes 3 "words" (vim counts punctuation runs
   like `{"` as their own word too, so watch exactly what disappears). `u` to undo.

**Check yourself:** after step 2 (before undoing), the line should read
`{"id": "A4-REVIEW", "items": ...}` — only the *second* quoted string changed, not the first (`"id"`).

---

### Operator + search

```
d/function       Delete everything from cursor until "function"
c/return         Change from cursor until "return"
y/class          Yank from cursor until "class"
v/end            Select from cursor until "end"
```

### Exercise 7.2: Jump to a method by searching, not scrolling

Open `src/calculator.py`, put your cursor on line 1 (`gg`).

1. `d/def divide` — deletes everything from the top of the file up to (not including) the start
   of the `divide` method definition.
2. `u` to undo immediately — you don't want to actually delete the `add`/`subtract`/`multiply`
   methods.
3. Now get there non-destructively: plain `/def divide` `Enter` just moves the cursor — a search
   is only destructive when you hand it to an operator (`d/`, `c/`). (For the record,
   `y/def divide` `Enter` is the halfway house: it *yanks* the same range `d/` would have deleted,
   without changing the buffer — but a yank leaves the cursor where it started, so it's not a
   navigation trick.)

**Check yourself:** after step 3 your cursor sits on the `d` of `def divide`, and `:w` was never
needed because nothing changed on disk.

---

### The power of `t` and `T` (till)

```
dt)              Delete till ) (not including the ))
ct,              Change till comma
yt:              Yank till colon
vt"              Select till quote
df)              Delete including ) (f = on the char, t = before it)
```

### Exercise 7.3: Rewrite one argument of a constructor call

In `src/orders.py`, find `build_order_book()`:

```python
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
```

1. Put your cursor on the `r` of the first `raw["id"]`.
2. `ct,` — changes everything up to (not including) the next comma. Type `raw.get("id")`, `Esc`.
   You've swapped a dict-index for a `.get()` call in three keystrokes plus typing.
3. Undo: `u`.

**Check yourself:** before undoing, the line should read
`book.add_order(Order(raw.get("id"), raw["items"], raw["discount"]))` — only the first argument
changed.

---

### Relative line operations

Turn on relative line numbers (`:set relativenumber`). Then:
```
d5j              Delete from here down 5 lines
y3k              Yank from here up 3 lines
>8j              Indent 9 lines (current + 8 below)
gq5j             Format 6 lines
v5j              Select 6 lines
```

### Exercise 7.4: Delete an entire list using relative counts

`:set relativenumber`, then in `src/orders.py` put your cursor on the `RAW_ORDERS = [` line — the
6 lines below it are one order each (`A1` through `A6`), and the closing `]` is the 7th line down.

1. Move down one line (`j`) to land on the `"A1"` entry.
2. `d5j` — deletes the current line (`A1`) plus the next 5 (`A2`-`A6`), wiping out the *contents*
   of the list (the surrounding `RAW_ORDERS = [ ... ]` brackets stay).
3. **Immediately** `u` — this drill is only to prove the relative-count math; you don't want an
   empty order book.

**Check yourself:** right before undoing, `RAW_ORDERS` should be an empty list body (`[` then `]`
on adjacent lines). After `u`, all 6 orders are back.

---

## Advanced Text Objects (with plugins)

With mini.ai (you have this):

```
cin)             Change inside next parentheses (cursor doesn't need to be inside)
cil)             Change inside last (previous) parentheses
c2i{             Change inside the 2nd enclosing brace
d2a"             Delete around the 2nd enclosing quotes
```

(The count goes *before* the `i`/`a` — `c2i{`, not `ci2{`. After an operator,
vim reads `i{`/`a{` as a two-character text object, so a digit wedged between
`i` and `{` isn't parsed as a count.)

Function arguments (treesitter text objects):
```
cia              Change inside argument
daa              Delete around argument (including comma)
via              Select argument
```

### Exercise 7.5: Edit the innermost, then the outer, structure without moving far

In `src/orders.py`, `Order.subtotal` has nested parens:

```python
return sum(item["price"] * item["qty"] for item in self.items)
```

1. Put your cursor on the `s` of `sum(`, before the opening paren.
2. `cin)` — jumps forward into the **next** set of parens (the outer `sum(...)` call, since that's
   the first `(` after the cursor) and lets you retype the whole generator expression. Type
   `x for x in []`, `Esc`. `u` to undo.

Now a real 2-level nesting example for `c2i{`. Find the `A6` entry in `RAW_ORDERS` — it has an
order dict `{...}` whose `"items"` value is itself a list of item dicts `{...}`, so there are two
enclosing `{` levels stacked:

```python
{"id": "A6", "items": [{"price": 3, "qty": 3}, {"price": 3, "qty": 3}], "discount": 0},
```

3. Put your cursor inside the first `{"price": 3, "qty": 3}` (innermost = the 1st enclosing brace).
4. `c2i{` — skips past that inner brace pair and targets the **2nd** enclosing one: the whole `A6`
   order dict. You're now in insert mode having deleted the entire order body. Type `"REPLACED"`,
   `Esc`. `u` to undo.

Finally, the treesitter argument object on `build_order_book()`'s constructor call:

```python
book.add_order(Order(raw["id"], raw["items"], raw["discount"]))
```

5. Put your cursor anywhere inside `raw["items"]` (the middle argument).
6. `daa` — deletes that whole argument *and* its trailing comma, leaving
   `Order(raw["id"], raw["discount"])`. `u` to undo.

**Check yourself:** step 2, before undoing, `subtotal` briefly returns `sum(x for x in [])`. Step
4, before undoing, `c2i{` replaced *everything* between the outer `{` and `}` — the whole `A6`
entry collapses to `{"REPLACED"},`, not just the `"items"` field, since the 2nd enclosing brace is
the entire order dict. Step 6, before undoing, the constructor call has 2 arguments instead of 3.

---

## Dot Formula — The Most Important Concept

The `.` command repeats the last *change*. Master vim users structure every edit to be repeatable.

### The formula: search → change → repeat

```
/pattern         Find what you want to change
cgn              Change the next match (combines c + gn motion)
.                Repeat on next match
.                And the next one
n                Skip one (don't change it)
.                Change this one
```

`cgn` + `.` is better than `:%s` when you want to review each change.

### Design repeatable changes

BAD (not repeatable):
```
f"ldt"           (multiple motions — . only repeats dt")
```

GOOD (repeatable):
```
ci"              (one operation — . repeats the whole thing)
```

### Multi-cursor without multi-cursor

1. Select a word: `*` (puts it in search register)
2. `cgn` — change the current match
3. `.` — apply same change to next match
4. `n` — skip without changing
5. `.` — change this one

This gives you interactive find-and-replace with undo per match.

### Exercise 7.6: Selectively promote 9 out of 10 "pending" items

Open `data/log.txt`. It has ten lines like `item 1: pending` through `item 10: pending` — perfect
for practicing *selective*, reviewed replacement (the whole reason `cgn` beats `:%s`).

1. `gg` to the top, then `/pending` and `Enter` to land on the first match.
2. `cgn` — changes that match; type `queued`, `Esc`.
3. Press `.` three times — watch matches 2, 3, and 4 all become `queued`.
4. To skip match 5, press `n` **twice**. The first `n` lands *on* match 5 — and because `gn`
   operates on the match under the cursor, pressing `.` there would change the very match you're
   trying to spare. The second `n` hops over it to match 6.
5. `.` — changes match 6 — then keep pressing `.` for the rest (4 more).

**Check yourself:** `<Space>sg pending` should now return exactly **1** result (the one you
skipped), and `<Space>sg queued` should return **9**. Discard the whole thing when you're done —
`:e!` — since other lessons reuse this file's original "all pending" state.

---

## Macros — Expert Patterns

### Self-correcting macros

Build macros that work regardless of cursor position:
```
qa               Start recording
0                Go to start of line (known position)
f:               Jump to colon (find anchor point)
l                Move right
dw               Delete word
A,               Append comma at end
j                Next line
q                Stop recording
```

Key: start each macro at a known position (`0`, `^`, `$`, or a search).

### Recursive macros

A macro that calls itself:
```
qqq              Clear register q
qa               Start recording into a
0f:ldwA,Escj@aq  Do work, move down, call @a, stop
@a               Run it — processes all remaining lines
```

It stops automatically when a motion fails (e.g., `j` at last line, `f:` with no colon).

### Macro to register, edit, save back

```
"qp              Paste macro from register q as text
                 (edit the text)
0"qy$            Yank the line back into register q
dd               Delete the temp line
```

Now `@q` runs the edited macro.

### Parallel macro application (visual)

```
V5j              Select 6 lines
:normal @a       Run macro 'a' on each selected line
```

### Exercise 7.7: Tag every order as reviewed, two ways

In `src/orders.py`, `RAW_ORDERS` has exactly 6 entries (`A1`-`A6`). You want to append
`  # reviewed` to the end of each one.

**Macro way:**
1. Cursor on the `A1` line. `qa` — start recording into register `a`.
2. `A  # reviewed` — go to end of line, type the comment, `Esc`.
3. `j` — move down to the `A2` line.
4. `q` — stop recording. `A1` is already tagged; `A2` is queued up, untagged.
5. `5@a` — replays the macro exactly 5 times, one per remaining line (`A2` through `A6`).

**Visual way (same result, different technique):** `u` everything first, then re-record the same
2-step macro on just the `A1` line (`qa`, `A  # reviewed`, `Esc`, `q` — no `j` this time). Then
select all 6 lines with `Vjjjjj` and run `:normal @a`.

**Check yourself:** `<Space>sg "# reviewed"` should return 6 hits. Discard with `:e!` when done —
Lesson 6 depends on `orders.py`'s exact structure.

---

## Registers — Expert Use

### Expression register (`=`)

In insert mode:
```
Ctrl-r =         Enter expression register
5 * 42 Enter     Inserts "210"
system('date')   Inserts current date
```

In normal mode:
```
"=5*42p          Paste result of expression
```

### Append to registers (uppercase)

Lowercase registers overwrite. Uppercase APPENDS:
```
"ayy             Yank line into register a (overwrite)
"Ayy             Append another line to register a
"ap              Paste all accumulated lines
```

Useful for collecting lines from different places.

### The black hole register

```
"_dd             Delete line without affecting any register
"_diw            Delete word, keep your yank intact
```

Use when you want to delete without overwriting what you previously yanked.

### The filename registers

```
Ctrl-r %         Insert current filename (in insert mode)
Ctrl-r #         Insert alternate filename
"%p              Paste current filename (normal mode)
```

### Exercise 7.8: Collect both TODOs into one place, without losing your other yank

Open `data/log.txt` — it has 2 comment lines starting with `# TODO`.

1. `gg` then `/# TODO` `Enter` to land on the first one.
2. `"ayy` — yank it into register `a` (overwrites whatever was there).
3. `n` to jump to the second `# TODO` line.
4. `"Ayy` — **append** it to register `a` instead of overwriting.
5. `:enew` — open a blank scratch buffer.
6. `"ap` — paste both TODO lines at once.

**Check yourself:** `:reg a` (run it before step 5) should show register `a` holding both TODO
lines together, in file order.

Now prove the black hole register doesn't clobber your yank: open `src/messy.py`, `yy` on the
`def summarize(items):` line, move down to a different line, `"_dd` to delete it. Press `p` — it
pastes `def summarize(items):`, not the line you just deleted, because `"_dd` never touched the
default register. `u` twice to restore `messy.py`. Close the scratch buffer without saving (`:bd!`).

---

## Command-line Window

Press `q:` to open command history as an editable buffer:
```
q:               Open command-line window (edit/search/rerun old commands)
q/               Open search history window
Ctrl-f           From : prompt, switch to command-line window
```

Inside: navigate with j/k, edit a command, press Enter to run it.

### Exercise 7.9: Rerun an edited command from history

1. In any buffer, run two throwaway commands: `:echo "first"` then `:echo "second"`.
2. `q:` — opens the command-line window with your recent `:` history.
3. Navigate up (`k`) to the `:echo "first"` line, change `"first"` to `"third"` (normal editing —
   `ci"` works fine here too), press `Enter` to run the edited version.

**Check yourself:** the message area shows `third`, and `:messages` shows all three echoes in
order (`first`, `second`, `third`).

---

## Quickfix & Location Lists

### Quickfix (project-wide results)

```
:copen           Open quickfix window
:cclose          Close quickfix window
:cnext / :cprev  Next / previous item (or ]q / [q)
:cfirst / :clast Jump to first / last
:cdo s/a/b/g     Run command on every quickfix entry
```

### The power workflow

1. `<Space>/` → search for something (grep)
2. `Ctrl-q` → send all results to quickfix
3. `:cdo s/old/new/g | w` → replace across all files
4. `:cfdo %s/old/new/g | w` → same but per-file (faster)

### Location list (buffer-local)

```
:lopen           Open location list
:lclose          Close
:lnext / :lprev  Navigate
```

### Exercise 7.10: Find every TODO in the project via quickfix

1. `<Space>/` (or `<Space>sg`) and search for `TODO`.
2. `Ctrl-q` — sends every hit to the quickfix list.
3. `:copen` — see them all in one window: you'll always get the 2 `# TODO` lines in
   `data/log.txt` **and** 2 hits inside `scripts/dirty.patch` (the reset script's patch file
   carries the same TODO text as the hunks it applies — grep doesn't care that it's tooling).
   Depending on how much of Lesson 6 you've done, you may also see the rename TODO in
   `src/orders.py` (removed by 6.6) and the `average()` TODO in `src/calculator.py` (added by the
   git drills).
4. `]q` / `[q` to step through the results one at a time; `Enter` on a quickfix line jumps to it.
5. `:cclose` when done.

**Check yourself:** the quickfix window's title bar shows the match count, and it matches what
`<Space>sg TODO` reported.

---

## Marks — Expert Patterns

### Auto-marks (vim sets these for you)

```
`.               Last edit position
`^               Last insert mode position
`[               Start of last yank/change
`]               End of last yank/change
`<               Start of last visual selection
`>               End of last visual selection
``               Position before last jump
```

### Mark + operate pattern

```
ma               Mark position
                 (move somewhere else, do stuff)
d`a              Delete from here back to mark a
y`a              Yank from here to mark a
v`a              Select from here to mark a
```

### Global marks (cross-file bookmarks)

```
mA               Set global mark A (remembered across files)
'A               Jump to file and line of mark A
```

Use A-D for your 4 most-used files. Jump between them instantly.

### Exercise 7.11: Bookmark two files, then jump between them blind

1. Open `src/calculator.py`, put your cursor on `class Person:`, press `mA`.
2. `:e src/orders.py` (or `<Space>sf` orders.py), put your cursor on `class OrderBook:`, press
   `mB`.
3. Open a third, unrelated file (e.g. `README.md`), then press `` 'A `` — you should land back on
   `class Person:` in `calculator.py`, in a completely different buffer. Press `` 'B `` — jumps
   straight to `class OrderBook:` in `orders.py`.

Now the local, single-file pattern — **this one is destructive, undo immediately**:

4. In `calculator.py`, put your cursor on `class Person:` and press `ma`.
5. `G` to jump to the end of the file.
6. `` d`a `` — deletes everything from the end of the file back up to the mark, i.e. the entire
   `Person` class.
7. **Immediately** `u` to restore it.

**Check yourself:** after step 3, you're in `orders.py` on the `OrderBook` line without having
typed a single filename. After step 7, `Person` is back — confirm with `<Space>sg "class Person"`.

---

## Advanced Substitution

### Regex groups and backreferences

```
:%s/\(\w\+\)/"\1"/g           Wrap every word in quotes
:%s/\v(\w+)/"\1"/g            Same with "very magic" (less escaping)
:%s/foo\(.*\)bar/baz\1qux/g  Keep middle, change surrounds
```

### Case-modifying substitution

```
:%s/\<\(\w\)/\u\1/g          Capitalize first letter of every word
:%s/.*/\L&/g                  Lowercase entire file
:%s/.*/\U&/g                  Uppercase entire file
:%s/\<\w/\u&/g               Title Case
```

### Substitute with expression

```
:%s/\d\+/\=submatch(0)+1/g   Increment all numbers by 1
:%s/\d\+/\=printf("%03d",submatch(0))/g  Zero-pad numbers
```

### Range modifiers

```
:5,10s/a/b/g     Lines 5-10 only
:'<,'>s/a/b/g    Visual selection only (auto-filled when you type : in visual)
:.,$s/a/b/g      Current line to end of file
:.,+5s/a/b/g     Current line plus next 5
:g/pattern/d     Delete all lines matching pattern
:v/pattern/d     Delete all lines NOT matching pattern
```

### Exercise 7.12: Rename a field across a whole file with one regex

Open `data/log.txt` — every line follows `item N: pending`.

1. `:%s/item \(\d\+\)/entry \1/g` — captures the number and reuses it, renaming every "item N" to
   "entry N" while keeping the right number on each line.
2. **Check yourself:** `:%s/item//gn` reports 0 matches and `:%s/entry//gn` reports 10 (the
   trailing `n` counts without replacing), and `entry 7` still says `entry 7`, not some other
   number (the backreference preserved it). Don't check with `<Space>sg item` — that greps the
   whole *project*, and `orders.py`/`messy.py` legitimately use `item` as a variable name.
3. `:e!` to discard.

Now a smaller, scoped one: visually select just the `keep: this line matches a filter pattern`
line (`V`), then `:'<,'>s/\<\(\w\)/\u\1/g` — Title Cases only that line, leaving the rest of the
file untouched. Check: that one line reads `Keep: This Line Matches A Filter Pattern`; every other
line is unchanged. `:e!` to discard.

---

## `:global` command (`:g`)

Operate on all lines matching a pattern:

```
:g/TODO/d              Delete all lines with "TODO"
:g/^$/d                Delete all empty lines
:g/pattern/normal A;   Append ";" to all matching lines
:g/import/t$           Copy all import lines to end of file
:g/def /normal O       Add blank line above each function
:v/keep/d              Delete all lines NOT containing "keep"
:g/pattern/m0          Move all matching lines to top
```

### Exercise 7.13: Strip TODOs and blank lines, then flip it around on a scratch copy

On `data/log.txt` (real file, but everything here gets undone):

1. `:g/TODO/d` — deletes both `# TODO` comment lines in one shot. `u` to bring them back.
2. `:g/^$/d` — deletes every blank line in the file (there are 3). `u` to bring them back.

Now the "keep"/"drop" lines at the bottom exist specifically for `:v` (the inverse of `:g`) — but
`:v/keep/d` deletes *everything that doesn't match*, which includes all 10 `item` lines too, not
just the `drop:` ones. Do this on a throwaway copy instead of the real file:

3. `:w /tmp/log-copy.txt` — save a copy without touching the original's git-tracked path.
4. `:e /tmp/log-copy.txt` — switch to editing the copy.
5. `:v/keep/d` — now only the 3 `keep:` lines survive; everything else (items, TODOs, blanks,
   `drop:` lines) is gone.

**Check yourself:** after step 5, the copy has exactly 3 lines, all starting with `keep:`. Close
the copy buffer (`:bd!`) — you never touched the real `data/log.txt` for this part.

---

## Window & Buffer Expert

### Argument list

```
:args **/*.py          Load all Python files into arglist
:args `git diff --name-only`  Load only changed files
:argdo %s/old/new/g | w       Run across all arg files
:next / :prev          Navigate arglist
```

### Buffer tricks

```
:b#               Switch to last buffer (alternate file)
Ctrl-^            Same as :b# (faster)
:bufdo            Run command across all open buffers
:ball             Open all buffers in splits
:tab ball         Open all buffers in tabs
```

### Tab pages (for layouts, not files)

```
:tabnew          New tab page
:tabclose        Close tab page
gt / gT          Next / previous tab page
:tabmove 0       Move current tab to first position
```

Tabs in vim are LAYOUTS (arrangements of splits), not files. Use buffers for files.

### Exercise 7.14: Load the whole `src/` folder as an arglist

From inside `nvim-drills`:

1. `:args src/*.py` — loads every `.py` directly under `src/` into the argument list: the four
   real modules plus the empty `__init__.py` (and `scratch.py`, if the git drills have created
   it). Globs grab everything that matches — curating is on you.
2. `:args` (no arguments) — prints the list with the current file bracketed.
3. `:next` repeatedly to step forward through the list; `:prev` to go back.
4. Once you've visited at least two of them, press `Ctrl-^` — toggles you straight back to
   whichever file you were on immediately before the current one, skipping the rest of the list.

**Check yourself:** `:args` run again always shows the same list with `[ ]` around whichever file
you're currently viewing.

---

## Insert Mode — Expert

### Auto-completion

```
Ctrl-n           Complete next match (from buffer/tags/etc.)
Ctrl-p           Complete previous match
Ctrl-x Ctrl-f    Complete filename
Ctrl-x Ctrl-l    Complete whole line
Ctrl-x Ctrl-o    Omni-completion (LSP)
```

### Insert mode tricks

```
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
```

### Exercise 7.15: Delete a line mid-sentence without breaking your typing flow

Open `src/messy.py`, find `total = 0` inside `summarize()`.

1. Press `A` at the end of that line to enter insert mode.
2. Without pressing `Esc`, press `Ctrl-o dd` — this executes one normal-mode command (`dd`,
   deleting the *current* line) and drops you right back into insert mode on what's now the
   following line.
3. `Esc`.
4. `u` to restore the deleted line — this drill is throwaway.

**Check yourself:** right after step 2 (before undoing), `total = 0` is gone from `summarize()`
and you never left insert mode to make it happen (no mode indicator flicker to NORMAL).

---

## Visual Block — Expert

### Column editing

```
Ctrl-v           Enter block mode
jjjj             Select column
I                Insert before column (affects all lines after Esc)
A                Append after column
c                Change column
r{char}          Replace column with char
d                Delete column
>                Indent selected block
```

### Add incrementing numbers

```
Ctrl-v jjjj      Select 5 lines
g Ctrl-a         Create incrementing sequence (1,2,3,4,5)
```

Or with a start value:
```
Ctrl-v jjjj      Select
I0 Esc           Insert "0" on all lines
gv               Reselect
g Ctrl-a         Now they're 1,2,3,4,5
```

### Align text with block mode

```
Ctrl-v           Block select
jjj              Select rows
$                Extend to end (makes ragged selection)
A                Append at end of each line
```

### Exercise 7.16: Reset a run of numbers, then regenerate them as a sequence

In `data/log.txt`, lines `item 7: pending`, `item 8: pending`, `item 9: pending` are three
consecutive rows with single-digit numbers — a clean target for block editing (`item 10` is two
digits, so leave it out of the column selection).

1. Put your cursor on the `7` in `item 7: pending`.
2. `Ctrl-v` to enter block (visual block) mode.
3. `2j` — extends the selection down 2 rows, covering the `7`, `8`, and `9` digits as a one-wide
   column.
4. `r0` — replaces every character in the block with `0`. All three lines now say `item 0:`.
5. `gv` — reselect that exact same block.
6. `g Ctrl-a` — increments each selected number by an increasing amount (line 1 by 1, line 2 by 2,
   line 3 by 3). Since they're all `0` now, you get `1`, `2`, `3`.

**Check yourself:** the three lines now read `item 1: pending`, `item 2: pending`,
`item 3: pending` — proving each line in the block got a *different* increment, not the same one.
`:e!` to discard.

---

## Ex commands & Ranges

### Range syntax

```
.                Current line
$                Last line
%                Entire file (same as 1,$)
'<,'>            Visual selection
.,.+5            Current line and next 5
'a,'b            From mark a to mark b
/pat1/,/pat2/    From pattern1 to pattern2
```

### Useful ex commands

```
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
```

### Exercise 7.17: Duplicate an order, then relocate it

In `src/orders.py`, cursor on the `A1` line inside `RAW_ORDERS`.

1. `:t.` — duplicates the current line directly below itself. You now have two identical `A1`
   entries.
2. `:m$` — moves the line you're currently on (the duplicate) to the very end of the *file* (past
   `build_order_book()`, not just past the list — a good reminder that `:m$` operates on the whole
   buffer, not the enclosing structure).
3. **Check yourself:** `G` to jump to the end of the file — the duplicated `A1` dict literal is
   now the last line in `orders.py`, clearly outside the `RAW_ORDERS` list and even outside
   `build_order_book()`.
4. `:e!` to discard both changes — this one is easy to forget mid-file, so double check
   `<Space>sg "id.*A1"` shows only 1 hit before moving on.

---

## Performance Tricks

### Jump without adding to jump list

```
Ctrl-d / Ctrl-u      These DON'T add to jump list (good for browsing)
gg / G / /pattern    These DO add to jump list (for intentional navigation)
```

### Quick file switching

```
Ctrl-^               Toggle between last two files (fastest switch)
<Space><Space>       Fuzzy buffer list
:b partial_name      Switch by partial filename
```

### Quickly fix and move on

```
ciw → type → Esc → n → .    Fix same pattern across file
*cwreplacement Esc n.n.n.    Replace word everywhere (review each)
```

### The number trick

```
Ctrl-a           Increment number under cursor
Ctrl-x           Decrement
5 Ctrl-a         Add 5 to number
```

On dates, versions, port numbers — instant updates.

### Exercise 7.18: Bounce between two files with zero typing

1. Open `src/calculator.py` (`<Space>sf`, type `calculator`, `Enter`).
2. Open `src/orders.py` the same way.
3. `Ctrl-^` — jumps back to `calculator.py` instantly, no fuzzy search needed.
4. `Ctrl-^` again — back to `orders.py`.

This is the fastest switch between exactly two files — faster than `<Space>sf` for the specific
case of "the file I was just in." Nothing to undo here; it's pure navigation.

---

## Undo — Expert

### Undo tree (not just linear)

```
:earlier 5m      Go back to file state 5 minutes ago
:later 2m        Go forward 2 minutes
:earlier 3f      Go back 3 file-saves ago
g-               Go to older state in undo tree
g+               Go to newer state in undo tree
```

### Undo branches

Vim's undo is a TREE, not a line. If you undo, make changes, the old changes aren't lost — they're a branch. Use `g-` and `g+` to walk the full tree.

### Persistent undo

Already configured — undo history survives quitting nvim. Open a file tomorrow and `u` still undoes yesterday's changes.

### Exercise 7.19: Time-travel through 3 saved states

> **This is the one exercise in this lesson that writes to disk** (`:earlier`/`:later` with an `f`
> count is save-based, so it needs real saves to travel between). Clean up with `git checkout --`
> at the end, not `:e!` — the changes will already be on disk.

In `src/messy.py`:

1. Add a comment `# checkpoint 1` at the top, `:w`.
2. Add a second comment `# checkpoint 2` right below it, `:w`.
3. Add a third, `# checkpoint 3`, `:w`. You now have 3 file-save checkpoints beyond the original.
4. `:earlier 2f` — jumps back 2 saves; you should see only `# checkpoint 1` present.
5. `:later 1f` — moves forward 1 save; `# checkpoint 2` reappears, `# checkpoint 3` still doesn't.
6. `g-` a few times, then `g+` — same idea, but walking one micro-change at a time instead of
   jumping whole saves.

**Check yourself:** at each step, `:%s/checkpoint//gn` (count-only) reports exactly as many
matches as the checkpoint number you're currently at. Don't use `<Space>sg checkpoint` for this —
`:earlier` rewinds the *buffer*, but ripgrep reads the file on *disk*, which still holds whatever
you last saved.

**Cleanup (required, since this exercise saved to disk):**
```bash
git checkout -- src/messy.py
```
Run that from a terminal (or `:!git checkout -- %` from inside nvim) to fully restore the file —
`:e!` alone won't help here since the "dirty" state is already what's on disk.

---

## Cheat Sheet — Expert Edition

| Intent | Keys |
|--------|------|
| Delete until pattern | `d/pattern` |
| Change until char | `ct{char}` |
| Repeat last search+change | `cgn` then `.` |
| Delete without affecting clipboard | `"_dd` |
| Append to register | `"Ayy` |
| Run macro on visual selection | `:'<,'>normal @a` |
| Increment numbers in column | `Ctrl-v` select → `g Ctrl-a` |
| Execute command from insert mode | `Ctrl-o {cmd}` |
| Calculate in insert mode | `Ctrl-r = 5*42 Enter` |
| Delete all lines matching pattern | `:g/pattern/d` |
| Keep only lines matching pattern | `:v/pattern/d` |
| Copy all matches to end of file | `:g/pattern/t$` |
| Sort visual selection | `:'<,'>!sort` |
| Go back in time | `:earlier 5m` |
| Duplicate line | `:t.` or `yyp` |
| Move line to end | `:m$` |
| Open last 2 files alternating | `Ctrl-^` |
| Capitalize first letters | `:%s/\<\w/\u&/g` |

---

Back to: [[Library Map]] | [[Learning Map]]
