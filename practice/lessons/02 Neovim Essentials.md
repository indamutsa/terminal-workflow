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

# Lesson 2: Neovim Essentials — Navigation & Basic Editing

> **This guide is for LazyVim** (plain `nvim`, or the `v` alias). All `<leader>` is the
> spacebar. Core vim motions (h/j/k/l, operators, text objects) are universal;
> the `<leader>`-key commands below are LazyVim's.

You can edit files from minute one. Everything else (LSP, plugins) happens automatically.

## Setup: the practice repo

Every exercise below runs against a real (deliberately imperfect) Python project:

```bash
cd "Terminal Workflow/practice/nvim-drills"
```

It has bad names, an unused import, an off-by-one bug, and a failing test —
this lesson only touches navigation and basic editing, so you won't fix any
of that yet (Lessons 3, 6, and 7 do). For now it's just real code to move
around in. If an exercise tells you to make a throwaway edit, undo it (`u`)
or discard it (`:e!`) afterward so the file is clean for the next lesson.

---

## Exercise 2.1: Open a project

```bash
v .          # or: nvim .
```

Run this from inside `nvim-drills`. `v` (no args) opens the dashboard; `v .` opens
the file explorer. Press `Enter` on `src/calculator.py` to open it.

---

## Exercise 2.2: Navigate files without a mouse

```
\                Toggle the file tree sidebar (neo-tree)
<Space>e         Toggle the file explorer (snacks — LazyVim default)
<Space>sf        Search files by name (fuzzy — your Cmd+P)
<Space><Space>   Find files (built-in alias for <Space>sf)
<Space>sg        Search inside all files (grep)
<Space>/         Grep (built-in alias for <Space>sg)
<Space>fr        Recent files
<Space>fg        Find git-tracked files
<Space>,         Switch between open buffers
gd               Go to definition of symbol under cursor
gr               Find all references
gO               Outline of functions/classes in current file
Ctrl-o           Jump back after going to a definition
```

**This is your Cmd+P replacement.** Learn `<Space>sf` (search files) and `<Space>sg` (grep) — you'll use them 100 times a day. Use `gd` to jump to a definition, `gr` to find usages, `gO` for the file outline.

> **The `<Space>s` search group:** `sf` files · `sg` grep · `sw` word · `sk` keymaps · `sh` help · `sd` diagnostics · `sr` search&replace. Press `<Space>s` and wait to see them all.

### Exercise: find where `TAX_RATE` is used

`src/orders.py` defines `TAX_RATE`; `src/report.py` uses it three times. Find every use without opening the file tree:

1. `<Space>sf` → type `orders` → `Enter` to open `src/orders.py`.
2. `<Space>sg` → type `TAX_RATE` → `Enter` — this greps the whole project.
3. In the results list, `Ctrl-n`/`Ctrl-p` to move between the 5 matches (2 in `orders.py`, 3 in `report.py`), `Enter` to jump to one.

**Check yourself:** you should see matches in both `src/orders.py` (the definition and its use inside `calc`) and `src/report.py` (the import line plus two f-string uses).

### Exercise: jump to a definition and back

`OrderBook.all_totals` (in `src/orders.py`) calls a function named `calc`.

1. Open `src/orders.py` (`<Space>sf` → `orders`).
2. Put the cursor on `calc` inside `all_totals`'s list comprehension.
3. `gd` — jumps to the `calc` function definition a few lines below.
4. `Ctrl-o` — jumps back to where you were.
5. `gr` on `calc` — lists every place it's referenced.

**Check yourself:** `gr` should show references spread across **3 files** — `orders.py` (the `all_totals` call), `report.py` (import + the call in `print_report`), and `tests/test_orders.py` (import + a call). Imports count as references too.

---

## Exercise 2.3: Edit → save → quit

```
i               Enter insert mode (now you can type)
Esc             Back to normal mode
:w              Save
:q              Quit
:wq             Save and quit
ZZ              Save and quit (faster — no colon needed)
```

The rhythm: `i` to type, `Esc` to stop, `:w` to save.

**Practice:** open `src/calculator.py`, go to the blank line 2, press `i`, type `# scratch`, `Esc`, `:w` to save, then `u` to undo the change and `:w` again to save the clean version back. You just proved the save/undo/save loop works without leaving the file in a modified state.

---

## Exercise 2.4: Move fast

```
h/j/k/l          Left/down/up/right (instead of arrow keys)
w                Jump forward one word
b                Jump back one word
e                Jump to end of word
0                Start of line
$                End of line
^                First non-whitespace character on line
gg               Top of file
G                Bottom of file
42G              Jump to line 42 (any number works)
Ctrl-d           Half-page down
Ctrl-u           Half-page up
Ctrl-f           Full page down
Ctrl-b           Full page up
%                Jump to matching bracket/paren/brace
{                Previous empty line (paragraph up)
}                Next empty line (paragraph down)
```

### Exercise: get to `RAW_ORDERS` and back without scrolling

`src/orders.py` is about 65 lines. `RAW_ORDERS` (a 6-line list of dicts) sits near the bottom.

1. Open `src/orders.py`, cursor starts at line 1.
2. `51G` — jump straight to the `RAW_ORDERS = [` line. (Line numbers can drift if you edited the file earlier — `/RAW_ORDERS` `Enter` always works too.)
3. `%` with the cursor on the `[` that opens `RAW_ORDERS` — jumps to the matching `]`.
4. `gg` — back to the top instantly.

**Check yourself:** after `%` on the opening `[`, your cursor should land on the closing `]` of the same list, 7 lines down (6 order entries between them).

---

## Exercise 2.5: Searching

```
/pattern         Search forward
?pattern         Search backward
n                Next match
N                Previous match
*                Search for word under cursor (forward)
#                Search for word under cursor (backward)
f{char}          Jump to next {char} on this line
F{char}          Jump to previous {char} on this line
;                Repeat last f/F jump
```

**Practice:** open `src/calculator.py`, search for "divide" (`/divide`), jump between matches (`n`/`N`). You'll land on the `divide` method definition and the `raise Exception("Cannot divide by zero")` line inside it.

### Exercise: find every TODO without grepping

`src/calculator.py` has none, but `src/orders.py` has two markers worth knowing about: a `# TODO: rename this...` above `calc`, and a `# FIXME: off-by-one...` above `qualifies_for_free_shipping`.

1. Open `src/orders.py`, `gg` to the top.
2. `/TODO` `Enter` — jumps to the TODO comment above `calc`.
3. `n` — nothing else matches "TODO" exactly, so try `/FIXME` next — jumps to the FIXME above `qualifies_for_free_shipping`.
4. Put the cursor on the word `calc` right after the TODO comment, press `*` — jumps forward to the next use of the word `calc` (inside the function body doesn't count since it's the definition; it'll actually jump to the *next* occurrence, which wraps around to `all_totals`'s call site if you're at the last one). Use `#` to search backward instead and compare.

**Check yourself:** `/TODO` then `/FIXME` should each find exactly one match in this file.

---

## Exercise 2.6: Entering insert mode (many ways)

```
i                Insert before cursor
a                Insert after cursor
I                Insert at start of line
A                Insert at end of line
o                New line below, enter insert mode
O                New line above, enter insert mode
s                Delete char under cursor, enter insert mode
S                Delete entire line, enter insert mode
C                Delete to end of line, enter insert mode
```

Instead of `$a` (end of line + insert after), just press `A`. Each variant saves a step.

### Exercise: add a throwaway method with `o`

1. Open `src/calculator.py`, jump to the `clear_history` method (`/clear_history`).
2. Move to the end of its body (the `self.history = []` line), press `o` — opens a new line below, already indented to match, and drops you in insert mode.
3. Type `pass  # scratch line, will discard` and `Esc`.
4. Confirm it's there: `/scratch` should find it.
5. Discard it: `:e!` — reloads the file from disk, throwing away the unsaved change. (If you already saved, `u` first, then `:w`.)

**Check yourself:** after `:e!`, `/scratch` should report "pattern not found" — the file is back to its clean, committed state.

---

## Exercise 2.7: Delete, yank, paste

```
dd               Delete (cut) whole line
5dd              Delete 5 lines
D                Delete to end of line
yy               Yank (copy) whole line
5yy              Yank 5 lines
y$               Yank to end of line
p                Paste below / after cursor
P                Paste above / before cursor
x                Delete character under cursor
X                Delete character before cursor (Backspace)
J                Join current line with next (remove newline)
yyp              Duplicate current line (yank + paste)
```

### Commenting

```
gcc              Toggle comment on current line
gc{motion}       Comment a range (e.g., gcip = comment paragraph)
gc5j             Comment 5 lines down
V then gc        Select lines, then toggle comment
gcO              Add comment on line above
gco              Add comment on line below
```

### Exercise: duplicate and retire an order line

`RAW_ORDERS` in `src/orders.py` has 6 entries (`A1`–`A6`).

1. Open `src/orders.py`, jump to the `A1` line (`/A1`).
2. `yyp` — duplicates it directly below. You now have two identical `A1` lines.
3. On the duplicate, `gcc` — comments it out (turns it into a `#`-prefixed line), simulating "retiring" a test order without deleting it.
4. `gcc` again on the same line — uncomments it back.
5. `dd` on the duplicate — deletes it entirely, restoring the file to 6 orders.

**Check yourself:** `:%s/"A1"//gn` (the trailing `n` means "count only, don't replace") should report **1 match** once you're done — back to a single `A1` entry.

---

## Exercise 2.8: Undo, redo, repeat

```
u                Undo
Ctrl-r           Redo
.                Repeat last change (incredibly powerful)
```

The `.` command: make a change (e.g., `ciw hello Esc`), move to another word, press `.` — same edit applied again.

### Exercise: mark two log lines done, then undo everything

`data/log.txt` has ten lines like `item 1: pending` through `item 10: pending`.

1. Open `data/log.txt`, `gg` to the top.
2. Cursor on `pending` in the `item 1:` line, `ciw` (change inner word) → type `done` → `Esc`. Line 1 now reads `item 1: done`.
3. Move down to the `item 2:` line, cursor on `pending`, press `.` — repeats the exact same change. Line 2 now reads `item 2: done` too.
4. `u` twice — undoes both changes, back to `pending` on both lines.
5. `Ctrl-r` twice — redoes them, back to `done` on both lines.
6. `:e!` — discard everything, leaving the file untouched on disk for the next lesson.

**Check yourself:** after `:e!`, `/done` in `data/log.txt` should find nothing — every line still says `pending`.

---

## Exercise 2.9: Buffers (open files)

```
Shift-L          Next open buffer
Shift-H          Previous open buffer
<Space>,         Fuzzy-find / switch open buffers
<Space>bd        Close current buffer
<Space>bp        Pin / unpin buffer
<Space>bP        Close all non-pinned buffers
```

### Exercise: open the three source files and cycle through them

1. `<Space>sf` → `calculator` → `Enter`.
2. `<Space>sf` → `orders` → `Enter`.
3. `<Space>sf` → `report` → `Enter`. You now have 3 buffers open, `report.py` active.
4. `Shift-H` twice — walks back to `calculator.py`.
5. `Shift-L` once — forward to `orders.py`.
6. `<Space>,` — opens the buffer picker; fuzzy-type `report` and `Enter` to jump straight there.

**Check yourself:** `<Space>,` should list all three — `calculator.py`, `orders.py`, `report.py` (plus anything still open from earlier exercises, like `data/log.txt`; `<Space>bd` closes the current buffer if you want to tidy the list first).

---

## Exercise 2.10: Terminals inside Neovim

LazyVim uses **Snacks terminal** (a floating terminal), plus the split terminals we added.

### Toggle the floating terminal

```
Ctrl-\           Toggle floating terminal  (also Ctrl-/ or <Space>ft)
Ctrl-\ Ctrl-n    Exit terminal mode (back to normal navigation)
q                Hide terminal (from normal mode inside it)
```

All three (`Ctrl-\`, `Ctrl-/`, `<Space>ft`) toggle the **same** terminal — press again to hide.

### Split terminals (we added these under  > Space < T)

```
<Space>tf        Floating terminal
<Space>tv        Vertical terminal (right side)
<Space>th        Horizontal terminal (bottom)
```

> **Note:** `<Space>t` is the **test** prefix in LazyVim (`<Space>tt` run test, etc.),
> so terminals live under capital `<Space>T`. For *multiple* independent terminals,
> prefer tmux panes (`Ctrl-a |`, `Ctrl-a -`) — they persist across reboots.

### Split terminals (built-in vim way)

```
:split | terminal        Open terminal in horizontal split (top/bottom)
:vsplit | terminal       Open terminal in vertical split (side by side)
```

### Copy & paste inside nvim

`Cmd+C` / `Cmd+V` don't work inside nvim — use vim's yank/paste instead. Your clipboard is synced (`unnamedplus`), so anything you `y` in nvim is immediately available with `Cmd+V` outside.

**Copying from a code buffer (the normal way):**
```
yy               Copy current line → system clipboard
5yy              Copy 5 lines
v → select → y  Visual select then yank → system clipboard
Vi{y             Copy everything inside braces
```

After yanking, `Cmd+V` works anywhere outside nvim (browser, Slack, etc.)

**Copying from nvim's terminal output:**
```
Ctrl-\ Ctrl-n    Exit terminal mode
Ctrl-a [         Enter tmux copy mode (navigate freely)
v                Start selection
y                Yank → system clipboard (via pbcopy)
```

**Pasting into nvim's terminal:**
```
Ctrl-a ]         tmux paste (bypasses nvim — always works)
```
Or: press `i` (terminal insert mode) then `Ctrl-a ]`

**If you need mouse selection (avoid multi-panel selection):**
```
Ctrl-a z         Zoom pane to fullscreen first
                 Now Option + mouse-drag selects only this pane
Cmd+C            Copy
Ctrl-a z         Unzoom back to normal layout
```

### Navigating between terminals and code

```
Ctrl-\ Ctrl-n        Exit terminal mode first (REQUIRED before navigating)
Ctrl-h/j/k/l        Move between splits (works across nvim + tmux panes)
Ctrl-w q             Close current split
```

### Exercise: run the test suite and just look at it

`nvim-drills` has two intentionally failing tests — you're not fixing them here (that's a Lesson 6 drill), just seeing them from inside the editor.

1. With `nvim-drills` open in nvim, `<Space>th` — opens a horizontal terminal at the bottom.
2. Run `pytest` (or `python3 -m pytest` if `pytest` isn't the one on your `PATH` — see the repo's `README.md` for the venv setup).
3. Read the summary line: **2 failed, 7 passed**. The failures are `tests/test_calculator.py::test_history_tracks_results` and `tests/test_orders.py::test_free_shipping_threshold`.
4. `Ctrl-\ Ctrl-n` — exit terminal mode.
5. `<Space>th` again — toggles the same terminal closed.

**Check yourself:** your terminal output should end with `2 failed, 7 passed` (exact pass count may drift slightly if you edited files earlier in this lesson and didn't discard — run `:e!` on anything you left dirty and re-run).

### The workflow

1. Open code file
2. `<Space>th` — open a horizontal terminal, run `pytest`
3. `Ctrl-\ Ctrl-n` — exit terminal mode
4. Edit code, save (`:w`)
5. `<Space>th` — toggle back to the terminal, re-run
6. For *separate* long-running processes (test watcher + dev server + logs),
   use **tmux panes** beside nvim — they persist and don't clutter the editor

---

## Exercise 2.11: Splits (multiple files visible)

```
:vsplit file.py           Vertical split (side by side)
:split file.py            Horizontal split (top/bottom)
Ctrl-w h/j/k/l           Navigate between splits
Ctrl-w =                  Make all splits equal size
Ctrl-w _                  Maximize current split height
Ctrl-w |                  Maximize current split width
Ctrl-w q                  Close current split
```

From the picker (`<Space>sf`): find a file, press `Ctrl-v` (vsplit) or `Ctrl-s` (hsplit) instead of Enter to open it in a split.

**Note:** If you get a "Pick window" prompt, your cursor is in the explorer sidebar, not the code buffer. Press `Esc` to cancel, then `Ctrl-l` to move to the code area first, then split. Or close the explorer with `\` before splitting.

### Exercise: compare `calc` against the function that calls it

1. Open `src/orders.py` with `calc` visible on screen (`/def calc`).
2. `<Space>sf` → type `report`, but press `Ctrl-v` instead of `Enter` — opens `report.py` in a fresh vertical split beside `orders.py`.
3. In the new pane, `/def print_report` to bring the calling code into view.
4. `Ctrl-w h` / `Ctrl-w l` to flip focus between the two panes and compare `calc` (left, in `orders.py`) against `print_report` (right, in `report.py`) side by side.
5. `Ctrl-w q` on either pane to close it when done.

**Check yourself:** you should have two panes open at once, each showing a different file, and `Ctrl-w h`/`Ctrl-w l` should move focus between them without closing either.

---

## Exercise 2.12: Tabs (separate workspaces)

Tabs in nvim are layouts — each tab can have its own arrangement of splits.

```
:tabnew              New empty tab
:tabnew file.py      Open file in new tab
gt                   Next tab
gT                   Previous tab
:tabclose            Close current tab
:tabs                List all tabs
```

Use tabs when you want completely separate views (e.g., one tab for code, another tab for tests layout). For switching between files, use buffers (`Shift-H/L` or `<Space>,`).

**Practice:** with `src/calculator.py` open, `:tabnew tests/test_calculator.py` — opens the test file in a brand-new tab, source and tests kept in separate layouts. `gt`/`gT` to flip between the two tabs, `:tabclose` to close the second one when you're done.

---

## Exercise 2.13: The leader key

`<Space>` is your leader key. Press it and **wait** — the which-key popup shows every command group. This is how you discover keymaps without memorizing them.

```
<Space>f...      Find — files, recent, buffers, config
<Space>s...      Search — grep, keymaps, help, diagnostics, marks
<Space>g...      Git — status, lazygit, blame, diff
<Space>c...      Code — actions, rename, format, symbols
<Space>x...      Diagnostics / Trouble
<Space>b...      Buffer commands
<Space>t...      Test (neotest)
<Space>T...      Terminals (float / vertical / horizontal)
<Space>u...      UI toggles — <Space>uC switches colorscheme
<Space>1-9       Jump to Harpoon file 1-9   (<Space>H adds current file)
```

**The discovery loop:** forgot a key? Press `<Space>` and read the menu, or
`<Space>sk` to fuzzy-search all keymaps by description.

### Exercise: find the grep key without being told

You already know `<Space>sg` greps the project — pretend you forgot.

1. Anywhere in `nvim-drills`, press `<Space>` and **wait** for the which-key popup.
2. Press `s` — narrows the popup to the search group, showing `sf`, `sg`, `sw`, `sk`, `sh`, `sd`, `sr` and their descriptions.
3. Read the description next to `sg`, then actually press `g` to run it, and grep for `qualifies_for_free_shipping`.

**Check yourself:** the grep should find 4 matches — the definition in `src/orders.py`, and an import, a comment, and the actual test call in `tests/test_orders.py`.

---

Back to: [[Library Map]] | [[Learning Map]]
