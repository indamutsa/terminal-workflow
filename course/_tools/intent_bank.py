"""Intent bank: what a person types into the course search, and where the answer lives.

INTENTS is a flat list of (query, target) pairs. A target is one of:
  (module_n, anchor)           a block in the site search index, e.g. (9, "module-1-d2-b1").
                               module_n is the module number (m9 = 9); the anchor is the id the page
                               scrolls to. The module folder is not used, and neither is any title.
  [target, target, ...]        any one of several equally good blocks.
  ("cheat", sheet_id, key)     a row of the cheat sheet drawer (content/cheatsheet.py): the sheet id and
                               the key or command column, which stay fixed when descriptions are reworded.
  None                         a content gap: no existing block answers it.

Anchors are built by kit.anchor(): "module-<page>-d<drill>-b<block>" for a block, "module-<page>-d<drill>"
for a drill section, "module-<page>-r<card>" for a rules card, "module-<page>-worked" for the worked example.
The page number is the page inside the module. Block structure and anchors stay fixed while titles are
reworded, so these targets survive a rewrite of every title and row.

A result also counts as a hit when it is the drill section that contains the target block, or an identical
row copied to another page (the search collapses identical rows into one result).
"""

# The "fzf helpers: what to type" table in module 1 lists every helper; it is a fair answer for any of them.
FZF_TABLE = (1, "module-3-d9-b1")


def fz(anchor):
    """A helper's own demo block, or the helper table."""
    return [(1, anchor), FZF_TABLE]


FIND_TEXT = [
    # find files (m9 page 1)
    ("find a file by part of its name", (9, "module-1-d1-b3")),
    ("find all the python files", (9, "module-1-d1-b4")),
    ("how do i find hidden files", (9, "module-1-d1-b6")),
    ("search for files but skip the docs folder", (9, "module-1-d1-b7")),
    ("find big files over 100 mb", (9, "module-1-d2-b1")),
    ("which files are eating my disk", (9, "module-1-worked")),
    ("find files i changed yesterday", (9, "module-1-d2-b4")),
    ("python files changed in the last 2 days", (9, "module-1-d2-b4")),
    ("files modified in the last 7 days", (9, "module-1-d5-b4")),
    ("find files older than 30 days", (9, "module-1-d3-b4")),
    ("find a file with this name opened last week", None),
    ("find files created today", None),
    ("run a command on every file i find", (9, "module-1-d2-b5")),
    ("find files by name with the find command", (9, "module-1-d3-b1")),
    ("delete the files i just found", (9, "module-1-d3-b8")),
    ("pick a file from a list by typing part of it", (9, "module-1-d4-b1")),
    ("open several files in nvim straight from a search", (9, "module-1-d4-b4")),
    ("search my whole mac for a file by name", (9, "module-1-d5-b1")),
    ("search the documents folder for invoice with spotlight", (9, "module-1-d5-b2")),
    ("how big is each folder", (9, "module-1-d5-b6")),
    ("find duplicate files", None),
    # search text (m9 page 2)
    ("search for a word in every file", (9, "module-2-d1-b2")),
    ("search ignoring case", (9, "module-2-d1-b3")),
    ("list the files that mention error", (9, "module-2-d1-b6")),
    ("how many times does error show up in each file", (9, "module-2-d1-b7")),
    ("search only python files", (9, "module-2-d2-b1")),
    ("show the lines around a match", (9, "module-2-d3-b1")),
    ("look for one word or another", (9, "module-2-d3-b3")),
    ("grep for lines that do not contain info", (9, "module-2-d4-b3")),
    ("filter the output of a command with grep", (9, "module-2-d5-b1")),
    # columns, sort, count (m9 page 3)
    ("get the first column of a log", (9, "module-3-d1-b2")),
    ("sort numbers properly not alphabetically", (9, "module-3-d2-b1")),
    ("sort users.csv by the third column", (9, "module-3-d2-b4")),
    ("count how many times each line appears", (9, "module-3-d3-b1")),
    ("how many lines does access.log have", (9, "module-3-d3-b4")),
    ("show the last 3 lines of a file", (9, "module-3-d5-b1")),
    ("watch a log file as new lines arrive", (9, "module-3-d5-b6")),
    # awk, sed, xargs, jq (m9 page 4)
    ("print the third column with awk", (9, "module-4-d1-b2")),
    ("add up a column of numbers", (9, "module-4-d1-b4")),
    ("show the top 5 ip addresses in my access log", (9, "module-4-d7-b1")),
    ("replace a word in a file with sed", (9, "module-4-d2-b1")),
    ("edit a file in place with sed on a mac", (9, "module-4-d2-b6")),
    ("replace a word in every file of a folder from the shell", None),
    ("run a command once for each line of input", (9, "module-4-d5-b1")),
    ("xargs breaks on file names with spaces", (9, "module-4-d5-b4")),
    ("pretty print a json file", (9, "module-4-d6-b1")),
    ("get one field out of users.json", (9, "module-4-d6-b2")),
    ("keep the json items where age is over 30", (9, "module-4-d6-b4")),
    ("rename files that have spaces in the name", (9, "module-4-d7-b4")),
    ("total size of all my log files", (9, "module-4-d7-b2")),
]

BASH = [
    # variables, tests, loops, arguments (m10)
    ("how do i run a bash script", (10, "module-1-d1-b2")),
    ("set a variable and print it", (10, "module-1-d2-b1")),
    ("why does my variable break when it has a space in it", (10, "module-1-d2-b3")),
    ("single quotes or double quotes", (10, "module-1-d2-b2")),
    ("save the output of a command in a variable", (10, "module-1-d3-b1")),
    ("do math in bash", (10, "module-1-d3-b2")),
    ("did my last command work", (10, "module-1-d4-b1")),
    ("exit a script with an error code", (10, "module-1-d4-b3")),
    ("check if a file exists", [(10, "module-2-d2-b1"), (10, "module-2-worked")]),
    ("compare two numbers in an if", (10, "module-2-d1-b4")),
    ("case statement", (10, "module-2-d3-b1")),
    ("why does my test always say true", (10, "module-2-d2-b5")),
    ("loop over all the txt files", (10, "module-3-d1-b3")),
    ("why does my loop break on names with spaces", (10, "module-3-d3-b6")),
    ("read a file line by line", (10, "module-3-d3-b1")),
    ("counter stays 0 after a pipe into while", (10, "module-3-d3-b5")),
    ("how do i read the arguments passed to my script", (10, "module-4-d1-b1")),
    ("give an argument a default value", (10, "module-4-d2-b1")),
    ("print a usage message when the arguments are wrong", (10, "module-4-d2-b3")),
    ("parse flags like -v and --name in a script", (10, "module-4-d3-b1")),
    ("ask the user a question and keep the answer", (10, "module-4-d4-b1")),
    # functions, strings, safety, redirects, ready-made scripts (m11)
    ("write a function in bash", (11, "module-1-d1-b2")),
    ("get the file name without the extension", (11, "module-1-d2-b2")),
    ("stop the script when a command fails", (11, "module-2-d1-b2")),
    ("clean up temp files when the script exits", (11, "module-2-d2-b1")),
    ("show which line made my script fail", (11, "module-2-d2-b3")),
    ("check that a tool is installed before using it", (11, "module-2-d2-b6")),
    ("debug a bash script line by line", (11, "module-2-d3-b1")),
    ("save error messages to a file", (11, "module-3-d1-b3")),
    ("compare the output of two commands", (11, "module-3-d3-b1")),
    ("back up a folder with the date in the name", (11, "module-4-d1-b2")),
    ("rename all the jpeg files to jpg", (11, "module-4-d1-b4")),
    ("try a command 3 times before giving up", (11, "module-4-d3-b1")),
    # gaps: nothing in the course answers these
    ("go back to the previous folder with cd", None),
    ("make a shortcut link to a file", None),
    ("unzip a downloaded archive", None),
    ("run my script every night", None),
    ("show free disk space", None),
    ("which process is using port 3000", None),
    ("download a file from a url", None),
]

TMUX = [
    ("how do i start a tmux session with a name", (1, "module-1-d1-b1")),
    ("leave tmux but keep everything running", (1, "module-1-d3-b1")),
    ("get back into my tmux session after closing the terminal", (1, "module-1-d3-b2")),
    ("list my tmux sessions", (1, "module-1-d5-b2")),
    ("rename a tmux session", [(1, "module-1-d4-b3"), (1, "module-1-d4-b4")]),
    ("kill every tmux session at once", (1, "module-1-d5-b9")),
    ("kill one tmux session by name", (1, "module-1-d5-b8")),
    ("make a new tmux window", (1, "module-1-d2-b1")),
    ("switch between tmux windows with number keys", (1, "module-2-d1-b1")),
    ("split the screen in two side by side", (1, "module-2-d2-b1")),
    ("make one pane full screen", (1, "module-2-d3-b1")),
    ("resize a pane", (1, "module-2-d3-b2")),
    ("close every pane except this one", (1, "module-2-d3-b3")),
    ("rename a tmux window", (1, "module-2-d3-b4")),
    ("run a command in another window without switching to it", (1, "module-2-d3-b5")),
    ("how do i scroll up in tmux", (1, "module-3-d1-b1")),
    ("copy text with the mouse inside tmux", (1, "module-3-d1-b2")),
    ("reload tmux.conf after editing it", (1, "module-4-d1-b1")),
    ("where is my tmux config file", (1, "module-4-d2-b1")),
    ("tmux inside tmux, how do i send keys to the inner one", (1, "module-4-d2-b2")),
    ("install tmux plugins", (1, "module-4-d3-b2")),
    ("save my tmux layout before a reboot", (1, "module-4-d4-b1")),
    ("check that tmux is saving my sessions in the background", (1, "module-4-d4-b2")),
    ("show the session name and the time in the tmux bar", (1, "module-4-worked")),
    ("bind my own key in tmux", (1, "module-4-d6-b1")),
    ("which command is this tmux key bound to", (1, "module-4-d6-b2")),
    ("ctrl a does nothing in tmux", (1, "module-1-r3")),
    ("start a tmux session named after the current folder", (1, "module-1-d5-b5")),
    ("break a long command onto a new line without running it", (1, "module-3-d2-b3")),
    ("accept the grey suggestion after my cursor", (1, "module-3-d2-b4")),
]

FZF = [
    ("find a file by name and open it in nvim", fz("module-3-d5-b1")),
    ("find a pdf somewhere in my home folder", fz("module-3-d5-b2")),
    ("open the one file that matches a name right away", fz("module-3-d5-b3")),
    ("search for a word in the project and jump to that line", fz("module-3-d5-b4")),
    ("find hidden and git ignored files too", fz("module-3-d5-b5")),
    ("search text and open the match in vs code", fz("module-3-d5-b7")),
    ("jump into a folder below this one", fz("module-3-d5-b9")),
    ("go up to a parent folder with a picker", fz("module-3-d5-b10")),
    ("open a file with its default mac app", fz("module-3-d5-b11")),
    ("copy the full path of a file to the clipboard", fz("module-3-d5-b12")),
    ("copy what is inside a file to the clipboard", fz("module-3-d5-b13")),
    ("switch git branch from a list", fz("module-3-d6-b1")),
    ("stage a changed file and see its diff", fz("module-3-d6-b2")),
    ("browse the commit history with a diff preview", fz("module-3-d6-b3")),
    ("switch to another tmux session from a list", fz("module-3-d6-b4")),
    ("delete files i pick from a list", fz("module-3-d7-b1")),
    ("kill a process i pick from a list", fz("module-3-d8-b1")),
    ("how do i stop the process on port 3000", fz("module-3-d8-b2")),
    ("look up an environment variable", fz("module-3-d8-b3")),
    ("find a dev command and put it on my prompt", fz("module-3-d8-b9")),
]

EDITING = [
    # Neovim basics (m2)
    ("how do i quit neovim", (2, "module-1-r1")),
    ("save a file in neovim", (2, "module-1-d4-b1")),
    ("find a file i had open recently", (2, "module-1-d3-b1")),
    ("find where a constant is used in the project", (2, "module-1-d3-b3")),
    ("jump to a definition and go back", (2, "module-1-d3-b4")),
    ("delete 5 lines at once", (2, "module-3-d1-b1")),
    ("comment out a line", (2, "module-3-d1-b2")),
    ("undo and redo", [(2, "module-3-d2-b1"), (8, "module-1-d2-b6")]),
    ("open a terminal inside neovim", (2, "module-4-d2-b1")),
    ("open a file in a vertical split", (2, "module-4-d4-b1")),
    ("copy text out of the terminal output", (2, "module-4-d3-b3")),
    ("get out of terminal mode", (5, "module-3-d4-b4")),
    # Power editing (m3, m6, m7)
    ("change the text inside parentheses", (3, "module-1-d2-b1")),
    ("record a macro", (3, "module-2-d2-b1")),
    ("replace a word in the whole file", (3, "module-2-d3-b1")),
    ("comment out five lines at once", (3, "module-2-r2")),
    ("fix messy indentation in the whole file", (3, "module-3-d1-b3")),
    ("paste what i yanked after deleting something", (3, "module-3-d2-b2")),
    ("set a mark and jump back to it", (3, "module-3-d3-b1")),
    ("rename a variable in one file", (3, "module-4-d1-b4")),
    ("rename a symbol in every file", (3, "module-4-d4-b1")),
    ("surround a word with quotes", [(6, "module-1-d1-b2"), (6, "module-1-d1-b3")]),
    ("see an outline of the functions in this file", [(6, "module-1-d4-b1"), (2, "module-1-d3-b1")]),
    ("find all the todo comments", (6, "module-2-d4-b1")),
    ("fold a block of code", (6, "module-3-d5-b2")),
    ("jump back to where i was", (6, "module-4-d1-b1")),
    ("delete without losing what i copied", (7, "module-2-d6-b2")),
    ("delete every line that contains todo", (7, "module-3-d4-b1")),
    ("go back to how the file looked 5 minutes ago", (7, "module-4-d6-b1")),
    # Coming from VS Code (m8)
    ("open a file by name like cmd p", (8, "module-1-d1-b1")),
    ("move a line up or down", (8, "module-1-d2-b1")),
    ("go to line 12", (8, "module-1-d1-b2")),
    ("zen mode", [(8, "module-2-d1-b1"), (8, "module-2-d1-b3")]),
    ("compare two files side by side", (8, "module-3-d3-b1")),
    # Worktrees and the agent loop (m4)
    ("create a git worktree for a new feature", (4, "module-1-d2-b1")),
    ("why use worktrees instead of stashing", (4, "module-1-d1-b1")),
    ("remove a worktree after the feature is merged", (4, "module-2-d3-b1")),
    ("make a worktree and open it in a new tmux window", (4, "module-2-d6-b2")),
    ("copy my env files into a new worktree", (4, "module-2-d5-b1")),
    ("let an agent work on a task in its own folder", (4, "module-3-worked")),
    # LSP, git, plugins (m5)
    ("go to the definition of a function", (5, "module-1-d2-b1")),
    ("stage one change and drop the other", (5, "module-2-d2-b2")),
    ("open lazygit", (5, "module-2-d3-b1")),
    ("commit my changes", (5, "module-2-d3-b2")),
    ("who changed this line", (5, "module-2-d4-b1")),
    ("replace text across several files", (5, "module-3-d3-b1")),
    ("run the tests", (5, "module-4-d1-b1")),
    ("merge a branch into main", None),
    ("squash my last 3 commits", None),
    ("resolve a merge conflict", (5, "module-2-d5-b3")),
]

CHEAT = [
    ("list all my worktrees", ("cheat", "worktree", "git worktree list")),
    ("clean up stale worktrees", ("cheat", "worktree", "git worktree prune")),
    ("amend the last commit", ("cheat", "lazygit", "A (Files)")),
    ("create a new branch", ("cheat", "lazygit", "n (Branches)")),
    ("go to the implementation of a function", ("cheat", "lsp", "gri")),
    ("keep only the lines that match a pattern", ("cheat", "expert", ":v/pattern/d")),
    ("swap two panes", ("cheat", "tmux", "Ctrl-a {")),
    ("turn a pane into its own window", ("cheat", "tmux", "Ctrl-a !")),
    ("find a tmux window by its name", ("cheat", "tmux", "Ctrl-a f")),
    ("see which dev tools are missing", ("cheat", "shell", "devh --check")),
]

# Reporting groups, mirroring the target mix: find/text, bash, tmux, editing/git/worktrees, fzf helpers, cheat sheet.
AREAS = {
    "find-text": FIND_TEXT,
    "bash": BASH,
    "tmux": TMUX,
    "editing-git": EDITING,
    "fzf-helpers": FZF,
    "cheat-sheet": CHEAT,
}

INTENTS = [pair for group in AREAS.values() for pair in group]
