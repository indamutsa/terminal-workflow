"""Shared data for every module: the module list and the site-wide glossary."""

MODULE_META = [
    {"n": 1, "folder": "m1-tmux", "title": "tmux and the shell"},
    {"n": 2, "folder": "m2-nvim-essentials", "title": "Neovim essentials"},
    {"n": 3, "folder": "m3-power-editing", "title": "Power editing"},
    {"n": 4, "folder": "m4-worktrees", "title": "Worktrees and the agent loop"},
    {"n": 5, "folder": "m5-lsp-git", "title": "Code intelligence and git"},
    {"n": 6, "folder": "m6-plugins-keymaps", "title": "Plugins and the key map"},
    {"n": 7, "folder": "m7-expert", "title": "Expert Neovim"},
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
