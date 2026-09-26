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

# Lesson 6: Neovim LSP, Git, and Advanced Features

> **This guide is for LazyVim.** Leader = spacebar.

Come here when the basics feel natural. These make you fast, not functional.

> **Practice repo:** every exercise below runs against
> `Terminal Workflow/practice/nvim-drills` — a small, deliberately imperfect
> Python project (bad names, an off-by-one bug, unused imports, a failing
> test) with real git history. One-time setup and reset instructions are in
> its `README.md`. Open it with `v .` from that folder.
>
> The exercises are ordered so each one's outcome is what the next one
> assumes — follow this lesson top to bottom the first time through rather
> than jumping around. In particular: do the **Git Inside Neovim** exercises
> (which reset the repo to a "dirty" state) *before* the **Actions** exercise
> that renames `calc` — otherwise the reset script will silently undo your
> rename.

---

## LSP — Code Intelligence

Already configured per language. Just open a file and it works.

### Navigation

```
gd               Go to definition (Ctrl-t to jump back)
gr               Find all references (who uses this?)
gI               Go to implementation
gy               Go to type definition
gD               Go to declaration
gK               Signature help
gO               Document symbols (outline of current file)
K                Hover docs (press again to enter the float)
```

Neovim 0.11 also ships native `gr*` LSP maps that work alongside the above:
`grn` rename, `gra` code action, `grr` references, `gri` implementation,
`grt` type definition. Use `gd`/`gr` as your primaries; the `gr*` set is there
as a fallback.

### Exercise 6.1: Trace a function to every caller

`OrderBook.all_totals()` in `src/orders.py` calls a function named `calc` —
find out where it's defined and everywhere it's used.

1. `<Space>sf orders.py` to open it
2. Put the cursor on `calc` inside `all_totals` (`return [calc(o) for o in self.orders]`)
3. `gd` — jumps to `def calc(o):` a few lines down
4. `gr` — opens the references list

**Check yourself:** the references list should show **3 files** — `orders.py`
itself, `report.py`, and `tests/test_orders.py`. Open the `report.py` hit,
then `Ctrl-o` to jump straight back to where you started.

### Diagnostics

```
]d               Jump to next error/warning
[d               Jump to previous error/warning
<Space>xx        Toggle diagnostics panel (Trouble)
<Space>xX        Current buffer diagnostics only
<Space>sd        Search/list diagnostics (picker)
<Space>cs        Symbols outline (Aerial)
<Space>xQ        Quickfix list (Trouble)
<Space>xL        Location list (Trouble)
```

### Exercise 6.2: Find the dead imports

`src/orders.py` imports two modules it never uses.

1. With `orders.py` open, `gg` to the top, then `]d` — jumps to the first
   unused-import warning
2. `]d` again — jumps to the second
3. `<Space>cd` — floats the exact diagnostic text over the cursor line
4. `<Space>sd` — project-wide diagnostics picker

**Check yourself:** `<Space>sd` lists exactly **2** diagnostics, both "unused
import" in `orders.py`. Leave them unfixed for now — Exercise 6.7 cleans them
up. (No LSP diagnostics showing at all? Your environment may not have
ruff/basedpyright wired up — run `ruff check src/orders.py` from a terminal
instead; per the repo's `pyproject.toml` it'll report the same two `F401`
findings.)

### Supported languages

| Language | LSP | Formatter | Linter |
|----------|-----|-----------|--------|
| Python | basedpyright | ruff | ruff + mypy |
| Scala | Metals | Metals | Metals |
| Bash | bashls | shfmt | shellcheck |
| TypeScript | ts_ls | prettier | eslint |
| YAML | yamlls | prettier | — |
| JSON | jsonls | prettier | — |
| Lua | lua_ls | stylua | — |
| Docker | dockerls | — | — |

---

## Git Inside Neovim

### Gitsigns (inline changes)

```
]h               Next hunk (changed block)
[h               Previous hunk
<Space>ghs       Stage hunk
<Space>ghu       Undo stage hunk
<Space>ghr       Reset hunk (discard change)
<Space>ghS       Stage entire buffer
<Space>ghR       Reset entire buffer
<Space>ghp       Preview hunk diff inline
<Space>ghb       Detailed blame for current line
<Space>ghB       Blame the entire buffer
<Space>ghd       Diff current file
<Space>ghD       Diff current file against the previous commit
```

Inline blame is already enabled: pause on a line for 300 ms and its author,
relative time, and commit summary appear at the end of the line.

### Exercise 6.3: Stage one hunk, discard another

From a terminal (`<Space>ft`) in the `nvim-drills` root:

```bash
./scripts/reset-dirty.sh
```

This gives you two real unstaged hunks and one untracked file:
`src/calculator.py` (a new `average()` method), `src/orders.py` (a new TODO
comment inside `calc`), and `src/scratch.py` (untracked). Safe to re-run any
time you want a fresh dirty state.

1. Open `src/calculator.py` — `]h` jumps straight to the new hunk
2. `<Space>ghp` — preview the diff inline
3. `<Space>ghs` — stage it (you're keeping `average()`)
4. Open `src/orders.py` — `]h` jumps to its hunk
5. `<Space>ghr` — discard it (you've decided that TODO isn't worth keeping)

**Check yourself:** `:DiffviewOpen` shows `orders.py` clean — no diff. A
terminal `git status --short` shows `M  src/calculator.py` (staged) and
`?? src/scratch.py` (still untracked), but no entry for `orders.py`.

### LazyGit (full git TUI)

```
<Space>gg        Open LazyGit at the repository root
<Space>gG        Open LazyGit at the current working directory
```

Inside LazyGit:
```
Space            Stage/unstage file
c                Commit
P                Push
p                Pull
b                Branches
s                Stash
l                Log
?                Help (shows all keys)

EXIT:
q                Quit LazyGit (back to nvim)
```

### Exercise 6.4: Stage, commit, and verify from LazyGit

Continuing from 6.3 — `src/calculator.py`'s hunk is staged, `src/scratch.py`
is still untracked.

1. `<Space>gg` — opens LazyGit
2. Select `src/scratch.py` in the files panel, press `Space` to stage it
3. Press `c`, type a commit message (e.g. "Add average() and a scratch
   file"), confirm
4. `q` — back to nvim

**Check yourself:** a terminal `git log --oneline -1` shows your new commit
on top of `Add messy.py for reformat/auto-indent drills`.

### Snacks git pickers

```
<Space>gL        Git log for the current working directory
<Space>gb        Commit history for the current line
<Space>gf        Commit history for the current file
<Space>gl        Repository log
<Space>gB        Open the current file/line on its remote (e.g. GitHub)
<Space>gY        Copy the remote URL for the current file/line
<Space>gs        Git status (picker)
<Space>gd        Git diff — hunks (picker)
<Space>gD        Git diff against origin
<Space>gS        Git stash
<Space>gi / gI   Open / all GitHub issues
<Space>gp / gP   Open / all GitHub pull requests
```

The GitHub issue and pull-request pickers require the GitHub CLI and access to
the repository.

### Diffview (side-by-side diffs and history)

Your custom Diffview setup uses dedicated mappings that do not overlap with
the Snacks diff pickers:

```
<Space>gv        Open the working-tree diff
<Space>gV        Open history for the current file
```

You can also open either view directly:

```vim
:DiffviewOpen
:DiffviewFileHistory %
```

Essential keys inside Diffview:

```
Tab / Shift-Tab  Open the next / previous changed file
Enter            Open the selected diff
s or -           Stage / unstage the selected file
S / U            Stage all / unstage all files
[x / ]x          Previous / next merge conflict
<Space>co        Choose ours for the current conflict
<Space>ct        Choose theirs for the current conflict
<Space>cb        Choose the base for the current conflict
<Space>ca        Choose all versions for the current conflict
g?               Show context-sensitive Diffview help
```

> **Safety:** never press `X` in Diffview. It restores the selected entry to
> the left-side state and can remove an untracked file. This conflicts with
> the no-delete rule.

**Want a clean slate later?** From the `nvim-drills` root, use
`./scripts/reset-dirty.sh`, which is the lesson's purpose-built reset path.

---

## File management (snacks explorer + neo-tree)

LazyVim does not ship Oil.nvim. File management is via the snacks explorer
and neo-tree instead:

```
<Space>e         Toggle snacks explorer (root dir)
<Space>E         Toggle snacks explorer (cwd)
\                Toggle neo-tree sidebar (custom mapping)
```

### Exercise 6.5: Create and delete a scratch file

1. `<Space>e` — opens the snacks explorer
2. Navigate into `src/`, press `a`, type `notes.md`, `Enter`
3. Highlight `notes.md`, press `d`, confirm the delete

**Check yourself:** `<Space>sf notes` finds nothing — the file's gone.

Inside the snacks explorer you get the same picker-style navigation as the
file finders, plus file operations (add/rename/delete) on the highlighted
entry. For bulk renames, use neo-tree (below) or a shell/`:!mv` command.

---

## Neo-tree (sidebar file explorer)

```
\                Toggle sidebar
```

Inside Neo-tree:
```
a                Add file/directory (end with / for dir)
d                Delete
r                Rename
c                Copy
m                Move
/                Filter
H                Toggle hidden files
?                Show help

EXIT:
\                Toggle sidebar off (same key that opened it)
q                Close Neo-tree
```

---

## LSP Actions

```
<Space>cr        Rename symbol across the whole project
<Space>ca        Code actions (quick fixes, auto-imports, refactors)
<Space>cf        Format file (ruff for Python, prettier for JS, etc.)
<Space>cd        Line diagnostics (float)
<Space>cl        LSP info (which servers are attached)
```

Inlay hints (inline type annotations) toggle via `<Space>u` (UI toggles
menu) — verify the exact subkey with the `<Space>` which-key menu.

### Exercise 6.6: Rename `calc` project-wide

`orders.py` has carried a `# TODO: rename this` comment on `calc` since
Exercise 6.1. Fix it for real, everywhere, in one move.

1. Cursor on `calc` at its definition (`def calc(o):`)
2. `<Space>cr` — type `calculate_total`, `Enter`
3. Delete the now-stale comment line above it (`# TODO: rename this...`) —
   cursor on it, `dd`

**Check yourself:** `gr` on `calculate_total` shows references in exactly
**3 files** (`orders.py`, `report.py`, `tests/test_orders.py`) — the same
3 files from Exercise 6.1, just renamed. Don't verify this with a plain
`<Space>sg calc` text grep: it'll also match the unrelated local variable
`calc = Calculator()` used repeatedly in `tests/test_calculator.py`, and the
word "Calculator"/"calculator.py" — `gr` is scope-aware and only shows real
references to the renamed symbol.

### Exercise 6.7: Clean up the dead imports

From Exercise 6.2 you know exactly where the two diagnostics are.

1. `gg` to the top of `orders.py`
2. Line 2 is `import json` — `dd`
3. The new line 2 is `import sys` — `dd`
4. `<Space>sd` — project-wide diagnostics picker

**Check yourself:** `<Space>sd` is now empty (0 diagnostics), and
`python -m src.report` from a terminal still runs and prints the same
totals as before — the rename and the import cleanup didn't change behavior.

---

## Search & Replace Across Project (grug-far)

LazyVim uses **grug-far** (not Spectre) for project-wide search and replace:

```
<Space>sr        Open search & replace panel (works on a word/selection too)
```

### Exercise 6.8: Rename a constant across two files

`TAX_RATE` is defined in `orders.py` and read in `report.py`. Give it a
clearer name.

1. Cursor on `TAX_RATE` anywhere, `<Space>sr` — opens grug-far pre-filled
   with `TAX_RATE`
2. Type `SALES_TAX_RATE` in the replace field
3. Check the preview: **2 matches in `orders.py`** (the definition and the
   one usage inside `calculate_total`), **3 matches in `report.py`** (the
   import plus two f-strings) — 5 total
4. Apply with the panel's "sync" action (shown in the panel header)

**Check yourself:** `<Space>sg TAX_RATE` → 0 hits. `<Space>sg SALES_TAX_RATE`
→ 5 hits across 2 files. `python -m src.report` still runs and prints the
same numbers, just under the new name.

In grug-far:
- Type the search term and the replacement
- Preview all matches across the project, grouped by file
- Edit the buffer directly to fine-tune the replacement
- Apply with the in-panel "sync" action (shown in the panel header)

You can always fall back to plain `:%s/old/new/g` (current file) or
`:cdo s/old/new/g` over a quickfix list for ad-hoc replaces.

```
EXIT:
q                Close grug-far panel
:q               Also works
```

---

## Terminals

The floating terminal has three keys that all toggle the **same** terminal:

```
Ctrl-\           Toggle floating terminal
Ctrl-/           Toggle floating terminal (same one)
<Space>ft        Toggle floating terminal (same one)
```

Split terminals (these open in a split rather than a float):

```
<Space>Tf        Terminal — float
<Space>Tv        Terminal — vertical split (right)
<Space>Th        Terminal — horizontal split (bottom)
```

> Note: `<Space>t` is the **test** prefix (neotest), not terminal. The
> terminal splits live under the capital `<Space>T`. The numbers
> `<Space>1`..`<Space>9` are **Harpoon** file jumps now, not terminals.

```
EXIT TERMINAL MODE:
Ctrl-\ Ctrl-n    Leave terminal (insert) mode back to normal mode
```

### Exercise 6.9: Run the suite from inside nvim

1. `<Space>ft` — floating terminal
2. Run `pytest` (or `python3 -m pytest` if you haven't activated the venv
   from the README)
3. `Ctrl-\ Ctrl-n` then `<Space>ft` to hide it, `<Space>ft` again to bring it
   back

**Check yourself:** 7 passed, 2 failed — `test_history_tracks_results` and
`test_free_shipping_threshold`. If a *different* test fails too, something
went wrong in an earlier exercise (most likely the rename) — worth chasing
down before continuing.

(Or skip the terminal entirely and use neotest — see the Neotest section.)

---

## Fuzzy finder (snacks picker) — advanced

LazyVim uses the snacks picker (not Telescope). The keys:

### Find

```
<Space>sf        Search files by name (added — your primary find-file)
<Space><Space>   Find files (built-in alias)
<Space>ff        Find files (root dir)
<Space>fF        Find files (cwd)
<Space>fr        Recent files
<Space>fg        Find git files
<Space>fb        Buffers
<Space>,         Buffers (quick switch)
<Space>fc        Find a config file
```

### Grep / search

```
<Space>/         Grep (root dir)
<Space>sg        Grep (root dir)
<Space>sG        Grep (cwd)
<Space>sw        Grep word / selection under cursor (root dir)
<Space>sb        Search lines in current buffer
<Space>sB        Grep across all open buffers
```

### Exercise 6.10: Grep, quickfix, browse

1. `<Space>sg` — search `TODO` across the project. You should see hits in
   `src/calculator.py` (the `average()` TODO from Exercise 6.3/6.4),
   `data/log.txt` (2 TODOs) — and 2 more inside `scripts/dirty.patch`: the
   patch file that `reset-dirty.sh` applies carries the same TODO text as
   the hunks it creates. Grep doesn't distinguish code from tooling — noise
   like this is exactly why you learn to read the file column before acting
   on results.
2. `Ctrl-q` — send every result to the quickfix list
3. `:copen` — browse it as a window, `]q`/`[q` to step through

**Check yourself:** the quickfix count matches what the picker showed —
**5 hits** (3 in real code/data, 2 in the patch file).

### Other pickers

```
<Space>sd        Diagnostics
<Space>sR        Resume last picker
<Space>sh        Help pages
<Space>sk        Keymaps
<Space>sC        Commands
<Space>s"        Registers
<Space>sm        Marks
<Space>sj        Jumps
<Space>st        Todo comments
```

Inside the picker:
```
Ctrl-n / Ctrl-p  Navigate results
Ctrl-s           Open in horizontal split
Ctrl-v           Open in vertical split
Enter            Open file
Ctrl-q           Send ALL results to quickfix

EXIT:
Esc              Close the picker
Ctrl-c           Also closes it
```

> The in-picker keys above are the snacks defaults; if one doesn't match,
> press `?` inside the picker to see its live keymap, or check the
> `<Space>` which-key menu.

---

## Surround (mini.surround)

In LazyVim mini.surround uses the **`gs` prefix** (bare `sa`/`sd`/`sr` are NOT
the surround keys here — `s` is Flash, `<Space>s*` are pickers):

```
gsa{motion}{char}   Add surrounding (gsa + motion + char)
gsd{char}           Delete surrounding
gsr{old}{new}       Replace surrounding
gsf / gsF           Find next / previous surrounding
gsh                 Highlight surrounding
```

### Exercise 6.11: Surround a word, then undo it

Throwaway drill — open `data/log.txt`, cursor on `pattern` in "this line
matches a filter pattern".

1. `gsaiw"` — wraps the word in double quotes
2. `u` — undo it; this was just a motion drill, not a real edit

**Check yourself:** the line reads exactly as it did before (`git diff
data/log.txt` from a terminal shows nothing).

Examples:
```
gsaiw"           Surround word with "
gsa3w(           Surround 3 words with ()
gsd(             Delete surrounding ()
gsr({            Replace () with {}
```

---

## Flash.nvim (instant cursor jumps)

Flash replaces traditional motions — press a key, type chars, pick a label to jump/select.

### Exercise 6.12: Jump straight to a long function name

1. `gg` to the top of `orders.py`
2. `s`, then type `qu` (first two letters of
   `qualifies_for_free_shipping`)
3. A label appears on the match — press it

**Check yourself:** cursor lands exactly on
`def qualifies_for_free_shipping(order):`.

### Basic jump

```
s{chars}         Type 's' then start typing — labels appear on matches, press label to jump
                 Works in normal, visual, and operator-pending mode
```

### Treesitter select

```
S                Select a treesitter node (function, block, class)
                 Press S → labels appear on code structures → pick one to select it
                 Chain: S → label → expand with S again for parent node
```

### Remote operations (operator-pending)

```
yr{label}        Yank text at a remote location without moving cursor
dr{label}        Delete text at a remote location without moving cursor
cr{label}        Change text at a remote location
```

### Enhanced search

```
/pattern         Normal search gets jump labels — press a label to jump directly
f{char}          f/t motions get labels when multiple matches exist on line
t{char}          Same — type the label to jump further
```

**EXIT:** Press `Esc` to cancel any Flash operation.

---

## Harpoon (instant file switching)

Mark your most-used files and jump between them with one keystroke — no fuzzy finding, no thinking.

### Exercise 6.13: Mark the 4 files you keep bouncing between

1. Open `src/calculator.py` — `<Space>H`
2. Open `src/orders.py` — `<Space>H`
3. Open `src/report.py` — `<Space>H`
4. Open `tests/test_orders.py` — `<Space>H`
5. From anywhere, `<Space>2` — jumps straight to `orders.py`

**Check yourself:** `<Space>h` opens the quick menu and lists all 4, in the
order you added them.

```
<Space>H         Add current file to harpoon list
<Space>h         Open harpoon quick menu (see all marked files, reorder, delete)
<Space>1         Jump to harpoon file 1
<Space>2         Jump to harpoon file 2
<Space>3         Jump to harpoon file 3
<Space>4         Jump to harpoon file 4
...              up to
<Space>9         Jump to harpoon file 9
```

**EXIT:** Close harpoon menu with `q` or `Esc`.

---

## Aerial (code outline / symbol tree)

A sidebar showing all functions, classes, methods in the current file — click or navigate to jump.

### Exercise 6.14: Get the shape of a file without reading it

1. Open `orders.py`, `<Space>cs`

**Check yourself:** the outline shows 2 classes (`Order`, `OrderBook`) and
3 top-level functions (`calculate_total`, `qualifies_for_free_shipping`,
`build_order_book`) plus the `RAW_ORDERS` constant — 6 top-level symbols.

```
<Space>cs        Toggle aerial outline (symbols)
{                Jump to previous symbol (function/class)
}                Jump to next symbol (function/class)
```

Inside the aerial panel:
```
Enter            Jump to that symbol
o                Jump to symbol but keep aerial open
l                Expand node
h                Collapse node
L                Expand all
H                Collapse all
```

**EXIT:** Close aerial with `<Space>cs` or `q` inside the panel.

---

## Treesitter Text Objects

Select, move between, and operate on code structures (functions, classes, parameters) as text objects.

### Exercise 6.15: Select without deleting

1. Cursor anywhere inside `qualifies_for_free_shipping`'s body
2. `vif` — selects the body only; note where it starts/ends, `Esc`
3. `vaf` — selects the whole `def` including the signature, `Esc`
4. Cursor inside `OrderBook`, `vic` — body only; `vac` — the whole class
5. Back on `qualifies_for_free_shipping`, `yif` to yank just the body, then
   `:new` for a scratch buffer, `p` to paste, confirm it looks right, `:bd!`
   to close the scratch buffer without saving

**Check yourself:** the pasted text in the scratch buffer starts with
`items = order.items` and ends with `return total_qty >= 5` — body only, no
`def` line.

### Selection (use in visual or operator-pending mode)

```
vaf              Select around function (including def/signature)
vif              Select inside function (body only)
vac              Select around class
vic              Select inside class
vaa              Select around argument/parameter
via              Select inside argument/parameter
daf              Delete entire function
yif              Yank function body
caa              Change argument
```

### Movement (jump between code structures)

```
]f               Jump to next function start
[f               Jump to previous function start
]c               Jump to next class start
[c               Jump to previous class start
```

---

## Neotest (run tests inside nvim)

Run tests without leaving the editor — see results inline, jump to failures.

### Exercise 6.16: Run a file, read the failure

1. Open `tests/test_calculator.py`, `<Space>tt` — runs the whole file
2. Gutter signs: 5 green, 1 red (`test_history_tracks_results`)
3. Cursor on the red test, `<Space>to` — see actual vs. expected
4. `<Space>ts` — toggle the summary panel

**Check yourself:** the summary panel shows 5/6 passed for this file. Leave
this one failing — it's an intentional "watch it fail" drill, not a bug to
fix (contrast with the DAP exercise next, which debugs a real bug).

```
<Space>tr        Run nearest test (test under cursor)
<Space>tt        Run all tests in the current file
<Space>tT        Run all test files
<Space>ts        Toggle test summary panel (see all pass/fail)
<Space>to        Show test output (print/debug output)
<Space>tO        Toggle the output panel
<Space>tl        Run last test
<Space>tw        Toggle watch mode
<Space>tS        Stop the running test
<Space>td        Debug nearest test (via DAP)
```

**EXIT:** Close test panels with `q`.

---

## DAP (Debugger)

Real debugger — breakpoints, step through, inspect variables. No more `print()`.

### Exercise 6.17: Debug the free-shipping bug for real

`tests/test_orders.py::test_free_shipping_threshold` fails.
`qualifies_for_free_shipping` in `orders.py` carries a
`# FIXME: off-by-one` comment. Find out why, live.

1. Open `orders.py`, cursor on the line
   `for i in range(len(items) - 1):`
2. `<Space>db` — sets a breakpoint (red dot in the gutter)
3. Open `tests/test_orders.py`, cursor inside `test_free_shipping_threshold`
4. `<Space>td` — debug this test; execution stops at your breakpoint
5. `<Space>du` — open the debug UI; watch `items` (2 dicts) and `total_qty`
   (starts at 0)
6. `<Space>dO` (step over) repeatedly — the loop body only runs once
   (`i=0`), because `range(len(items) - 1)` is `range(1)` for a 2-item list;
   `total_qty` ends at 3, never adding the second item's `qty` of 3
7. `<Space>dt` — terminate the debug session
8. Fix it: change `range(len(items) - 1)` to `range(len(items))`
9. Delete the now-resolved `# FIXME:` comment above the function
10. `<Space>tr` on the test (or rerun the file) — green

**Check yourself:** `pytest` from a terminal now shows exactly **1**
failure (`test_history_tracks_results` — still intentional), down from 2.

### Controls (LazyVim `<Space>d` prefix)

```
<Space>db        Toggle breakpoint on current line
<Space>dB        Set conditional breakpoint (prompts for condition)
<Space>dc        Start / Continue (run)
<Space>di        Step into function
<Space>dO        Step over (next line)
<Space>do        Step out of function
<Space>dC        Run to cursor
<Space>du        Toggle debugger UI (variables, stack, breakpoints)
<Space>de        Eval expression (also works on a visual selection)
<Space>dr        Toggle REPL
<Space>dl        Run last
<Space>dt        Terminate
```

### Test debugging

```
<Space>td        Debug the nearest test (neotest + DAP)
<Space>dPt       Debug the Python test method under cursor
<Space>dPc       Debug the Python test class
```

### Python environments (venv-selector)

```
<Space>cv        Select the Python virtualenv/interpreter for this project
```

If you set up `.venv` per the practice repo's README, pick it here so the
LSP, debugger, and tests all use the right interpreter.

**EXIT:** Stop the debugger with `<Space>dt` (terminate) or close the UI
with `<Space>du`.

---

## Bufferline (tab bar)

Shows open files as tabs at the top — like VS Code's tab bar.

```
L  (Shift-L)     Next buffer/tab
H  (Shift-H)     Previous buffer/tab
<Space>bp        Pin/unpin current buffer
<Space>bP        Delete all non-pinned buffers
<Space>bj        Pick a buffer by label
<Space>bl        Delete buffers to the left
<Space>br        Delete buffers to the right
<Space>bd        Close current buffer (LazyVim default — verify in which-key)
```

---

## Illuminate (highlight word under cursor)

Automatically highlights all occurrences of the word under cursor — no keymap needed, it just works. Helps you see where a variable is used at a glance.

---

## Persistence (auto sessions)

LazyVim auto-saves a session per project directory. Restore exactly where you left off.

### Exercise 6.18: Quit and pick up where you left off

1. With a few files open in `nvim-drills`, quit entirely: `:qa`
2. Reopen: `v .` from the `nvim-drills` root
3. `<Space>qs` — restore the session

**Check yourself:** the same buffers and split layout you had before `:qa`
reappear.

```
<Space>qs        Restore session for this directory
<Space>ql        Restore last session
<Space>qS        Select a session to restore
<Space>qd        Don't save the current session (stop auto-save)
```

---

## Yanky (yank history)

Every yank/delete goes into a ring you can cycle through when pasting — no more losing a copy to an overwrite.

### Exercise 6.19: Recover an earlier yank

In `orders.py`'s `RAW_ORDERS` list:

1. Yank the `"A1"` line: cursor on it, `yy`
2. Move down, yank the `"A2"` line: `yy`
3. Move to a scratch buffer (`:new`), `p` — pastes the A2 line (most recent)
4. `[y` — the pasted text swaps to the A1 line instead, without re-yanking

**Check yourself:** after step 4 the scratch buffer shows the `"A1"` line,
not `"A2"`. Close the scratch buffer without saving (`:bd!`).

```
<Space>p         Open yank history picker (pick any past yank)
p / P            Paste after / before (yanky-aware)
]y / [y          Cycle forward / backward through yank history
]p / [p          Paste with indent matched to current line
gp / gP          Paste, leaving cursor after the pasted text
```

---

## Mini.ai (smarter text objects)

Extends `a`/`i` text objects with treesitter awareness and new targets. Use after any operator (`d`, `c`, `y`, `v`).

### Exercise 6.20: Change inside parens you're not even touching

`Order.subtotal` in `orders.py`:
`return sum(item["price"] * item["qty"] for item in self.items)`

1. Put the cursor on `return` — you're *before* the parens, not inside them
2. `ci)` — mini.ai searches forward on the line, finds the `sum(...)` parens,
   and puts you in insert mode inside them
3. Type anything, `Esc`, then `u` immediately — this is a motion drill, undo
   it

**Check yourself:** `git diff src/orders.py` (or just eyeball the line)
shows no change — you undid it.

```
af / if          Around / inside function
ac / ic          Around / inside class
ao / io          Around / inside a code block (treesitter)
a) i) a] i] a} i} Brackets — searches forward on the line if not inside one
aq / iq          Around / inside any quote
an / in          Next text object (e.g. cin) targets the next match)
al / il          Last text object (previous match)
g[ / g]          Jump to start / end of the text object under cursor
```

---

## Todo Comments

Highlights `TODO`, `FIX`, `FIXME`, `HACK`, `NOTE`, `WARN` in your code and lets you jump/search them.

### Exercise 6.21: Sweep for what's left

After Exercises 6.6–6.7 (rename + import cleanup) and 6.17 (DAP fix), two of
`orders.py`'s original TODO/FIXME comments are gone. What's still open?

1. `<Space>st` — search all TODOs project-wide

**Check yourself:** exactly **5** results — the `average()` TODO in
`calculator.py` (from the git drill in 6.3/6.4), the 2 TODOs in
`data/log.txt`, and 2 duplicates inside `scripts/dirty.patch` (the patch
file that plants those TODOs — todo-comments scans every file, patches
included). If you see a 6th, something from an earlier exercise didn't get
cleaned up as instructed — go back and check.

```
]t / [t          Jump to next / previous todo comment
<Space>st        Search all todos (picker)
<Space>sT        Search only TODO/FIX/FIXME
<Space>xt        Todos in the Trouble panel
```

---

## Database UI (vim-dadbod)

Query databases inside nvim — connections, tables, and a SQL scratchpad.

```
<Space>D         Toggle the DB UI (explorer of connections/tables)
```

Inside DBUI: `Enter` expands a connection/table, write SQL in a buffer and run it with `<Space>S` (or `:DB`). SQL buffers get autocompletion from `vim-dadbod-completion`.

---

## Markdown

### Render-markdown (inline rendering)

Renders markdown live inside nvim — headings, code-block backgrounds, bullets, checkboxes. Activates on `.md` files, no keymap needed.

```
<Space>um        Toggle inline rendering on/off (UI toggle)
```

### Browser preview

```
<Space>cp        Markdown Preview (opens live-refreshing browser view)
```

**EXIT:** `<Space>cp` again, or close the browser tab.

---

## Noice + Snacks notifier (modern UI)

The command line, messages, and popups use a modern floating UI — automatic, no keymaps:

- Command line and search (`/`) appear as floating inputs
- Notifications (LSP progress, messages) pop in the top-right via the snacks notifier
- `<Space>sn` opens the Noice message group (`<Space>snh` history, `<Space>snd` dismiss all)

---

## Lualine (statusline)

The bottom statusline shows mode, git branch, diff, diagnostics, file info, and position. Always visible, no keymaps.

---

## Vim-tmux navigator

`Ctrl-h/j/k/l` moves seamlessly between nvim splits AND tmux panes — one set of keys for both layers.

```
Ctrl-h           Move left (works across nvim ↔ tmux)
Ctrl-j           Move down
Ctrl-k           Move up
Ctrl-l           Move right
```

---

## Which-key (keymap discovery)

Press any prefix and **wait** — a popup lists every continuation. This is how you learn the config without memorizing it.

```
<Space>           Wait → see all leader groups
<Space>?          Buffer-local keymaps
g                 Wait → see all g-prefix commands
z                 Wait → see all z-prefix commands
<Space>sk         Fuzzy-search ALL keymaps by description
```

---

## The `g` prefix commands

These are all triggered with `g` followed by another key. Shown in which-key when you press `g`:

### Navigation

```
gg               First line of file
G                Last line of file (not g prefix, but related)
gi               Go to last insert position and enter insert mode
gf               Go to file under cursor (opens the file path)
gx               Open filepath or URL under cursor in system handler (browser, Finder)
gO               Document symbols (LSP outline of current file)
g,               Go to newer position in change list
g;               Go to older position in change list
```

### Search (after pressing `g` in operator-pending / visual)

```
gn               Search forwards and select the match
gN               Search backwards and select the match
```

Useful pattern: `/pattern` then `cgn` — change the match, then `.` to repeat on next match. (Lesson 7 drills this in depth.)

### Case

```
gu{motion}       Lowercase (e.g., `guiw` = lowercase word)
gU{motion}       Uppercase (e.g., `gUiw` = uppercase word)
g~{motion}       Toggle case (e.g., `g~iw` = toggle word)
~                Toggle case of char under cursor
```

### Comments

```
gc{motion}       Toggle comment (e.g., `gcip` = comment paragraph)
gcc              Toggle comment on current line
gcO              Add comment on line above
gco              Add comment on line below
```

In visual mode: select lines, then `gc` to toggle comment.

### LSP (the `g` keys)

LazyVim's primary LSP jumps (set when a server attaches):

```
gd               Go to definition
gr               Find all references
gI               Go to implementation
gy               Go to type definition
gD               Go to declaration
gK               Signature help
gO               Document symbols
K                Hover docs
```

Neovim 0.11 natives also work as a fallback: `grn` rename, `gra` code
action, `grr` references, `gri` implementation, `grt` type definition,
`grx` codelens.

### Formatting

```
gw{motion}       Format text (wraps to textwidth)
gq{motion}       Format text and move cursor to end
```

### Tabs (not buffers)

```
gt               Go to next tab page
gT               Go to previous tab page
```

### Marks

```
g'{mark}         Jump to mark (like `'{mark}` but doesn't change jump list)
```

### Misc

```
ga               Show character code under cursor (ASCII, hex, octal)
g8               Show UTF-8 byte sequence for char under cursor
gv               Reselect last visual selection
gJ               Join lines without adding space
gf               Go to file under cursor
```

---

## The `[` and `]` bracket commands

Navigate between things — diagnostics, hunks, functions, etc:

```
]d / [d          Next / previous diagnostic (error/warning)
]h / [h          Next / previous git hunk
]m / [m          Next / previous method/function start
]M / [M          Next / previous method/function end
]{ / [{          Next / previous unmatched {
]] / [[          Next / previous section/class
]s / [s          Next / previous misspelled word
]q / [q          Next / previous quickfix item
]b / [b          Next / previous buffer
```

---

## The `z` prefix commands

Scroll and fold control:

### Scrolling (reposition screen without moving cursor)

```
zz               Center current line on screen
zt               Move current line to top of screen
zb               Move current line to bottom of screen
zH               Scroll half screen to the left
zL               Scroll half screen to the right
```

### Folding

```
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
```

### Spelling

```
z=               Show spelling suggestions for word under cursor
zg               Mark word as good (add to dictionary)
zw               Mark word as wrong
```

---

## The `Ctrl` commands

### Navigation

```
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
```

### Editing (normal mode)

```
Ctrl-a           Increment number under cursor
Ctrl-x           Decrement number under cursor
Ctrl-r           Redo
```

### Editing (insert mode)

```
Ctrl-w           Delete word backward (like Option+Delete)
Ctrl-u           Delete to start of line (like Cmd+Delete)
Ctrl-h           Delete character backward (like Backspace)
Ctrl-t           Indent current line
Ctrl-d           Unindent current line
Ctrl-r "         Paste from register (e.g., Ctrl-r 0 = last yank)
Ctrl-n           Autocomplete next match
Ctrl-p           Autocomplete previous match
Ctrl-o           Execute ONE normal mode command, then back to insert
```

`Ctrl-o` in insert mode is huge: `Ctrl-o dd` deletes a line without leaving insert mode.

### Window management

```
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
```

---

## The `<Space>` (leader) commands

Press `<Space>` and wait for which-key. The main groups:

### Find (`<Space>f`) and the quick-finders

```
<Space><Space>   Find files (root dir)
<Space>ff        Find files (root dir)
<Space>fr        Recent files
<Space>fg        Find git files
<Space>fb        Buffers
<Space>,         Buffers (quick switch)
```

### Search (`<Space>s`)

```
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
```

### Git (`<Space>g`)

```
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
```

Direct Diffview commands are also available: `:DiffviewOpen` and
`:DiffviewFileHistory %`.

### Diagnostics/Trouble (`<Space>x`)

```
<Space>xx        Diagnostics (Trouble)
<Space>xX        Buffer diagnostics (Trouble)
<Space>xt        Todo (Trouble)
<Space>xT        Todo/Fix/Fixme (Trouble)
<Space>xL        Location list (Trouble)
<Space>xQ        Quickfix list (Trouble)
```

### Buffers (`<Space>b`)

```
<Space>bp        Toggle pin
<Space>bP        Delete non-pinned buffers
<Space>bj        Pick buffer by label
<Space>bl        Delete buffers to the left
<Space>br        Delete buffers to the right
<Space>bd        Delete buffer (LazyVim default — verify in which-key)
<Space><Space>   Find files / switch (snacks)
<Space>,         Switch between open buffers
```

### Code (`<Space>c`)

```
<Space>cf        Format file
<Space>cr        Rename (LSP)
<Space>ca        Code action (LSP)
<Space>cd        Line diagnostics
<Space>cl        LSP info
<Space>cs        Symbols outline (Aerial)
<Space>cm        Mason (LSP/formatter installer)
```

### Hunks/Git signs (`<Space>gh`)

```
<Space>ghs       Stage hunk
<Space>ghr       Reset hunk
<Space>ghp       Preview hunk
<Space>ghb       Blame line
<Space>ghS       Stage buffer
<Space>ghR       Reset buffer
```

### Terminal (`<Space>f` / `<Space>T`) and Test (`<Space>t`)

```
<Space>ft        Toggle floating terminal
<Space>Tf        Terminal — float (split)
<Space>Tv        Terminal — vertical split
<Space>Th        Terminal — horizontal split

<Space>t         TEST prefix (neotest) — tt run file, tr run nearest, ts summary
```

> Don't confuse them: `<Space>t*` is **test**, `<Space>T*` is the **split**
> terminal, and `<Space>ft` / `Ctrl-\` / `Ctrl-/` is the **floating** terminal.
> Inlay-hints toggle lives under `<Space>u` (UI toggles) — verify the subkey
> in which-key.

---

## The `:` command mode

Useful commands you type after pressing `:`:

### Files

```
:w               Save
:q               Quit
:wq              Save and quit
:q!              Quit without saving
:qa!             Quit ALL windows without saving
:e file.py       Open a file
:saveas new.py   Save as new file
```

### Buffers

```
:ls              List open buffers
:b2              Switch to buffer 2
:bn / :bp        Next / previous buffer
:bd              Close buffer
:bufdo cmd       Run command across all buffers
```

### Windows/Splits

```
:split           Horizontal split
:vsplit          Vertical split
:only            Close all other splits
:close           Close current split
```

### Useful

```
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
```

---

Back to: [[Library Map]] | [[Learning Map]]
