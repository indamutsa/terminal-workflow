"""Shared data for every module: the module list and the site-wide glossary."""

MODULE_META = [
    {"n": 1, "folder": "m1-tmux", "title": "tmux and the shell", "group": "tmux & Neovim"},
    {"n": 2, "folder": "m2-nvim-essentials", "title": "Neovim essentials", "group": "tmux & Neovim"},
    {"n": 3, "folder": "m3-power-editing", "title": "Power editing", "group": "tmux & Neovim"},
    {"n": 4, "folder": "m4-worktrees", "title": "Worktrees and the agent loop", "group": "tmux & Neovim"},
    {"n": 5, "folder": "m5-lsp-git", "title": "Code intelligence and git", "group": "tmux & Neovim"},
    {"n": 6, "folder": "m6-plugins-keymaps", "title": "Plugins and the key map", "group": "tmux & Neovim"},
    {"n": 7, "folder": "m7-expert", "title": "Expert Neovim", "group": "tmux & Neovim"},
    {"n": 8, "folder": "m8-from-vscode", "title": "Coming from VS Code", "group": "tmux & Neovim"},
    {"n": 9, "folder": "m9-find-text", "title": "Find and text tools", "group": "Linux & Bash"},
    {"n": 10, "folder": "m10-bash-basics", "title": "Bash basics", "group": "Linux & Bash"},
    {"n": 11, "folder": "m11-bash-expert", "title": "Bash expert", "group": "Linux & Bash"},
]

# (id, label, forms, definition) — shared by every module; a module's own glossary wins on a clash.
SITE_GLOSSARY = [
    ("tw-prefix", "Prefix key", ["prefix key", "prefix"], "The key you press first to tell tmux that the next key is a tmux command. Here: Ctrl-a."),
    ("tw-session", "Session", ["session", "sessions"], "A tmux workspace that keeps running when you close the terminal window. You re-attach to it later."),
    ("tw-pane", "Pane", ["pane", "panes"], "One rectangle inside a tmux window. Each pane runs its own shell."),
    ("tw-buffer", "Buffer", ["buffer", "buffers"], "A file loaded into Neovim's memory. You edit the buffer, and saving writes it to disk."),
    ("tw-register", "Register", ["register", "registers"], "A named slot in Neovim that holds text: yanked, deleted or typed."),
    ("tw-worktree", "Worktree", ["worktree", "worktrees"], "A second folder checked out from the same git repository, on its own branch."),
    ("tw-leader", "Leader key", ["leader key", "leader"], "A key you press first to start your own Neovim shortcuts. Here: Space."),
    ("tw-picker", "Picker", ["picker", "pickers"], "A pop-up list you filter by typing, such as the file finder."),
    ("tw-hunk", "Hunk", ["hunk", "hunks"], "One block of changed lines in a git diff."),
    ("tw-quickfix", "Quickfix list", ["quickfix list", "quickfix"], "A list of locations, such as search hits or errors, that you step through one by one."),
    ("tw-lsp", "LSP", ["LSP"], "Language Server Protocol. A background program that tells Neovim what the code means: definitions, errors, renames."),
]

SITE_URL = "https://nvim-workflow.vercel.app"

# Shell helpers from ~/.config/shell/fzf.zsh: (what to type, what you get). Shared by module 1 and the cheat sheet.
# Each description starts with the words a person would type: verb and object first.
FZF_HELPERS = [
    ("ff", "Find file by name and open it in nvim (Tab marks several)"),
    ("ffh pdf", "Find a file of one type anywhere under your home folder and open it"),
    ("fa", "Find any file, hidden and git-ignored ones too, and open it in nvim (skips .git)"),
    ("fv", "Find one file and open it in nvim (press Enter without Tab)"),
    ("fe ord", "Open the file matching a name at once, or pick from the matches"),
    ("frg word", "Find text in the project as you type and open nvim on the matching line"),
    ("frc word", "Find text in the project as you type and open the match in VS Code"),
    ("fcode", "Find files and open them in VS Code (Tab marks several)"),
    ("fdir", "Change into a folder you pick below the current one"),
    ("fcd", "Change to a parent folder you pick"),
    ("fopen", "Open files with their default macOS app"),
    ("fscp", "Copy file path: pick a file and its full path goes to the clipboard"),
    ("fsc", "Copy file content: pick a file and its whole text goes to the clipboard"),
    ("fsd", "Delete files you pick (Tab marks several); asks y/N first"),
    ("fsdd", "Delete folders you pick, contents included; asks y/N first"),
    ("fgb", "Switch to a git branch you pick and check it out"),
    ("fgs", "Stage or unstage a changed file, with a diff: Ctrl-a stages, Ctrl-r unstages"),
    ("fgl", "Browse the commit history with a diff preview (fgl --all for every branch)"),
    ("ftm", "Switch to another tmux session"),
    ("ftmk", "Kill tmux sessions you pick"),
    ("fkill", "Kill a process you pick (fkill 15 sends SIGTERM)"),
    ("fport 8000", "Kill whatever is listening on a port"),
    ("fenv", "Browse environment variables"),
    ("fchelp", "Search a command's man page or --help text"),
    ("fdocker", "List docker containers with a log preview; Enter prints the container ID"),
    ("f", "Short for fzf: pick a file from the current folder"),
    ("fzp", "Pick a file with a numbered bat preview (fzf plus preview)"),
    ("fh", "Print every helper with an example"),
    ("devh --pick", "Search the dev cheat sheet and put the pick on the prompt"),
]

# Each module is served at /<folder>/ from <folder>/MODULE_FILE.
MODULE_FILE = "index.html"


def module_path(folder):
    """File on disk and in the search index."""
    return f"{folder}/{MODULE_FILE}"


def module_href(folder):
    """Link to a module: the folder URL, with no file name."""
    return f"{folder}/"


PRACTICE_HOME = "~/tw"
PRACTICE_DIR = "practice"

# The only files the Neovim examples open. Each is at most PRACTICE_MAX_LINES lines and is written byte for byte to course/practice/.
PRACTICE_MAX_LINES = 20
PRACTICE_FILES = {
    "orders.py": '''TAX_RATE = 0.08
ORDERS = ["A1", "A2", "A3"]
PRICES = {"A1": 2.50, "A2": 4.00, "A3": 1.25}


def calc_totl(price, qty):
    return price * qty * (1 + TAX_RATE)


def report(codes):
    for code in codes:
        print(code, calc_totl(PRICES[code], 2))


name = "pen"
qty = 3
price = 2.50
note = "rush"
total = calc_totl(price, qty)
print(name, qty, price, note, total)
''',
    "notes.md": '''# Shipping notes

Orders ship within two days. Rush orders ship the same day, but only before noon.

If an order is late, tell the customer first. Then check the carrier.

## Checklist

Pack the box. Print the label. Hand it to the carrier.

## Contacts

Support answers email within one day. Call the carrier about lost parcels.
''',
    "todo.txt": '''item 1: pending
item 2: pending
item 3: pending
item 4: pending
item 5: pending
item 6: pending
item 7: pending
item 8: pending
item 9: pending
item 10: pending

TODO call the carrier
buy tape
TODO print labels
buy boxes
TODO reply to Sam
''',
}
