"""Module 13: Commit, branch and undo with LazyGit. Source: lazygit 0.64.1 default keys (lazygit --config), run in a throwaway repo in /tmp/tw-lazygit; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


REPO = "/tmp/tw-lazygit"

MODULE = {
    "n": 13,
    "folder": "m13-lazygit",
    "title": "Commit, branch and undo with LazyGit",
    "footer": "LazyGit keys to stage lines, commit, amend, branch, squash, stash, undo, push and pull in a practice repo",
    "tagline": "Commit, branch, squash and undo in LazyGit without remembering git commands.",
    "glossary": [
        ("tw-panel", "Panel", ["panel", "panels"], "One box on the LazyGit screen: Status, Files, Branches, Commits or Stash. Press 1 to 5 to jump to one."),
        ("tw-stash", "Stash", ["stash", "stashes"], "A shelf where git keeps your uncommitted changes for later, so the folder is clean again."),
        ("tw-upstream", "Upstream", ["upstream"], "The remote branch your local branch pushes to and pulls from, such as origin/main."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Open lazygit and find the files, branches and commits panels",
            "subtitle": "Open lazygit in a repo, jump between panels with 1 to 5, find a key with ?, open it from Neovim, quit",
            "idea": (
                "Run lazygit in a git folder. Press a number to jump to a panel, ? to see its keys, q to leave.",
                [
                    ("Open lazygit in this repo", "lazygit", "Run it from any folder inside a git repository."),
                    ("Jump to the branches panel", "3", "1 status, 2 files, 3 branches, 4 commits, 5 stash."),
                    ("See every key for this panel", "?", "Type / to filter the list. Esc clears the filter; Esc again closes help."),
                    ("Quit lazygit", "q", "You are back at the shell prompt."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I use git without remembering every command? You lose track of what is staged, and you avoid squashing commits or undoing a mistake.",
                "fix": "Open LazyGit. It shows files, branches, commits and stash on one screen, and one key does each job.",
            },
            "drills": [
                {
                    "h2": "Open lazygit in a repo and see what changed",
                    "intro": f"Build a practice repo with three commits and three uncommitted changes. Every block in this module runs in `{REPO}`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a practice git repo for lazygit (3 commits, 3 changes)", "code": C('''
mkdir -p /tmp/tw-lazygit && cd /tmp/tw-lazygit
git init -q -b main
git config user.name "Sam Lee"
git config user.email "sam@example.com"
printf '# Shop\\n\\nA tiny order calculator.\\n' > README.md
git add README.md && git commit -q -m "Add README"
cat > app.py <<'EOF'
def price(item):
    return 10

def tax(amount):
    return amount * 0.2

def shipping(weight):
    return 5
EOF
git add app.py && git commit -q -m "Add app.py"
printf 'buy tape\\nbuy boxes\\n' > notes.txt
git add notes.txt && git commit -q -m "Add notes"
cat > app.py <<'EOF'
def price(item):
    return 12

def tax(amount):
    return amount * 0.25

def shipping(weight):
    return 7
EOF
echo 'buy glue' >> notes.txt
echo 'draft' > scratch.txt
git log --oneline
git status --short
'''),
                         "expect": "`git log --oneline` lists three commits, newest first: `Add notes`, `Add app.py` and `Add README`, each with a short hash that differs on your machine. `git status --short` lists ` M app.py`, ` M notes.txt` and `?? scratch.txt`."},
                        {"type": "text", "body": "To build the repo again from scratch, run `mv /tmp/tw-lazygit /tmp/tw-lazygit-old` first, then the block above. The `git config` lines keep the commits in this repo under the name Sam Lee."},
                        {"type": "cmd", "where": "shell", "title": "Check that lazygit is installed", "code": C('''
lazygit --version
'''),
                         "expect": "One line that contains `version=` and your version number, such as `version=0.64.1`. If the shell says `command not found`, run `brew install lazygit`. The keys in this module are the lazygit defaults of 0.64.1."},
                        {"type": "cmd", "where": "shell", "title": "Open lazygit in a git folder", "code": C('''
cd /tmp/tw-lazygit
lazygit
'''),
                         "expect": "Five panels fill the left side. `Status` reads `tw-lazygit → main`. `Files` lists `app.py`, `notes.txt` and `scratch.txt` with `M`, `M` and `??`, under a `▼ /` line for the folder. `Local branches` shows `* main`. `Commits` lists `Add notes`, `Add app.py` and `Add README`. `Stash` is empty. The diff of the selected file fills the right side, and a hint bar with keys runs along the bottom. The first time, a welcome box says `Press <enter> to get started`: press `Enter`."},
                        {"type": "text", "body": "The `▼ /` line is the top of the file tree. Press `Space` on it and lazygit stages every file below it. Press the backtick key to switch the tree to a flat list."},
                    ],
                },
                {
                    "h2": "Switch between panels in lazygit (1 to 5, Tab, h and l)",
                    "intro": "Jump to a panel by its number. The number is in the panel's title bar.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Jump to the files, branches, commits or stash panel", "rows": [
                            ("1", "Go to the Status panel"),
                            ("2", "Go to the Files panel: changed files"),
                            ("3", "Go to the Local branches panel"),
                            ("4", "Go to the Commits panel: the commit log"),
                            ("5", "Go to the Stash panel"),
                            ("Tab / l", "Go to the next panel"),
                            ("Shift-Tab / h", "Go to the previous panel"),
                            ("0", "Go to the diff on the right (Esc goes back)"),
                        ], "try": "Press `3`, then `4`, then `Tab`.",
                         "expect": "The hint bar at the bottom changes with each panel: `Checkout: <space> | New branch: n` for branches, then `Squash: s | Fixup: f` for commits, then only `Keybindings: ?` for the empty Stash panel."},
                        {"type": "keys", "where": "lazygit", "title": "Show the reflog, remotes or tags inside a panel (tabs)", "rows": [
                            ("]", "Go to the next tab of this panel"),
                            ("[", "Go to the previous tab of this panel"),
                        ], "try": "Press `4`, then `]`, then `[`.",
                         "expect": "`]` switches Commits to Reflog, which lists `commit: Add notes`, `commit: Add app.py` and `commit (initial): Add README`. `[` switches back. Files has the tabs Worktrees and Submodules. Branches has Remotes and Tags."},
                        {"type": "keys", "where": "lazygit", "title": "Move in a list, open an item and filter it", "rows": [
                            ("j / k", "Move down or up one line (arrow keys work too)"),
                            ("< / >", "Jump to the top or the bottom of the list"),
                            ("Enter", "Open the selected item: a file's lines, a branch's commits"),
                            ("Esc", "Go back or close a popup"),
                            ("/", "Filter the list by text (Enter keeps the filter, Esc clears it)"),
                        ], "try": "Press `2`, then `/`, type `notes` and press `Enter`.",
                         "expect": "The Files panel shows only ` M notes.txt` and the hint bar reads `Filter: matches for 'notes'`. `Esc` brings back all three files."},
                        {"type": "keys", "where": "lazygit", "title": "Make a panel bigger", "rows": [
                            ("+", "Make the current panel bigger: half the screen, then full width"),
                            ("_", "Make it smaller again"),
                        ], "try": "Press `2`, `+`, `+`, then `_` twice.",
                         "expect": "The Files panel grows wider and hides the diff. After the second `+` it takes the full width. Two presses of `_` bring the normal layout back."},
                        {"type": "cmd", "where": "shell", "title": "Check that lazygit shows the same branch and commits as git", "code": C('''
git -C /tmp/tw-lazygit branch
git -C /tmp/tw-lazygit log --oneline
'''),
                         "expect": "`* main`, then the same three commits as the Commits panel: `Add notes`, `Add app.py` and `Add README`. LazyGit has no copy of your repository: it runs git and draws the result."},
                    ],
                },
                {
                    "h2": "Find a lazygit key you forgot (? and /)",
                    "intro": "Every panel lists its own keys. You never need to remember them all.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "See every key for this panel and search them", "rows": [
                            ("?", "Show every key of the current panel, then the global keys"),
                            ("/", "Inside that list: type to filter it"),
                            ("Esc", "Clear the filter; press again to close help"),
                            ("@, then f", "Open the extras menu, then focus the command log: the git commands lazygit ran for you"),
                            ("q", "Quit lazygit"),
                        ], "try": "Press `2`, then `?`, then `/`, and type `stash`.",
                         "expect": "The long list shrinks to two lines under Local: `s Stash` and `S View stash options...`. First `Esc` clears the filter; second `Esc` closes help."},
                        {"type": "text", "body": "Why does `Esc` not quit lazygit? At the top level it only closes popups and filters. Quit with `q`."},
                    ],
                },
                {
                    "h2": "Open lazygit from Neovim (Space g g)",
                    "intro": "Module 5 opens LazyGit in a float. Use the same keys on the practice repo.",
                    "blocks": [
                        {"type": "keys", "where": "nvim", "title": "Open lazygit from Neovim and go back", "rows": [
                            ("<Space>gg", "Open LazyGit at the repository root"),
                            ("<Space>gG", "Open LazyGit in the current folder (working directory)"),
                            ("q", "Quit LazyGit and go back to Neovim"),
                        ], "try": "Run `nvim /tmp/tw-lazygit/app.py`, press `<Space>gg`, then `q`.",
                         "expect": "LazyGit opens in a float over `app.py` with the same five panels. `q` closes the float and you are back in the file."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which lazygit key opens which panel",
                "cards": [
                    ("Jump to a panel with a number key", "The number is in the title of each panel.", ["Key", "Panel"], [
                        ["`1`", "Status"],
                        ["`2`", "Files (`]` for Worktrees and Submodules)"],
                        ["`3`", "Local branches (`]` for Remotes and Tags)"],
                        ["`4`", "Commits (`]` for Reflog)"],
                        ["`5`", "Stash"],
                    ]),
                    ("Keys that work in every panel", "Learn these once.", ["Key", "Action"], [
                        ["`j` / `k`", "Move down or up"],
                        ["`Enter`", "Open the selected item"],
                        ["`Esc`", "Go back or close a popup"],
                        ["`?`", "List the keys of this panel"],
                        ["`/`", "Filter the list"],
                        ["`q`", "Quit"],
                    ]),
                    ("Open lazygit from the shell or from Neovim", "Same screen, two ways in.", ["Where", "Keys"], [
                        ["Shell", "`lazygit`"],
                        ["Neovim, repository root", "`<Space>gg`"],
                        ["Neovim, current folder", "`<Space>gG`"],
                        ["Leave either one", "`q`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Look at what changed, then leave lazygit",
                "frame": "You come back to the shop repo and want to know what changed before you do anything.",
                "open": "cd /tmp/tw-lazygit\nlazygit",
                "steps": [
                    (None, "`2`", "Go to the Files panel."),
                    (None, "`j`", "The cursor starts on `▼ /`. Move to `app.py`. The diff on the right shows `return 10` replaced by `return 12`, and two more changed lines."),
                    (None, "`4`", "Go to the Commits panel and read the three commits."),
                    (None, "`q`", "Quit lazygit."),
                ],
                "after": "LazyGit closes and the shell prompt returns. `git -C /tmp/tw-lazygit status --short` still lists ` M app.py`, ` M notes.txt` and `?? scratch.txt`.",
                "meaning": "Looking changes nothing. You can open lazygit, read, and quit without touching your files.",
            },
            "practice": {
                "h2": "Check your answers: panels, keys and quitting",
                "qs": [
                    ("Mechanism", "Why does lazygit show the same changes as `git status --short`?",
                     "What does lazygit run underneath?",
                     ["LazyGit has no copy of your repository.", "It runs git commands for you and draws the result.", "Press `@`, then `f` to focus the command log."],
                     "LazyGit is a screen for git, so it always matches git."),
                    ("Keystrokes", "Which keys show the commits panel and then its reflog?",
                     "A number, then a bracket.",
                     ["Press `4` for the Commits panel.", "Press `]` for the next tab, Reflog."],
                     "`4`, then `]`. `[` goes back to Commits."),
                    ("Application", "How do I find the key that stashes my changes?",
                     "Open the key list and search it.",
                     ["Press `?` to open the key list.", "Press `/` and type `stash`."],
                     "`?`, `/`, `stash`. The list shows `s Stash`."),
                    ("Common mistake", "Why does lazygit stay open when I press `Esc`?",
                     "What does `Esc` do at the top level?",
                     ["`Esc` closes popups and filters.", "At the top level it has nothing to close.", "`q` quits."],
                     "Press `q` to quit."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Stage files or single lines and commit in lazygit",
            "subtitle": "Stage a file with Space, stage single lines with Enter, commit with c, add to the last commit with A, discard or ignore a file",
            "idea": (
                "Press Space on a file to stage it and c to commit. Press Enter on a file to stage single lines.",
                [
                    ("Stage a file", "Space", "Press it again to unstage the file."),
                    ("Commit the staged files", "c", "Type the message, then press Enter."),
                    ("Stage single lines of a file", "Enter", "Then Space stages the change under the cursor."),
                    ("Add to the last commit", "A", "Stage first, then A and Enter."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I commit only part of a file? `git add -p` asks a question for every change, and one wrong `y` stages the wrong lines.",
                "fix": "In LazyGit, open the file with Enter and press Space on exactly the change you want. The staged part moves to a second pane, so you see what the commit holds.",
            },
            "drills": [
                {
                    "h2": "Stage a file and commit it in lazygit",
                    "intro": "Start from the practice repo of page 1: three files have changes. Commit the notes first. Check results in a second shell, or press `q` to leave lazygit and open it again.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Commit a file in lazygit", "rows": [
                            ("Space", "Stage the selected file (press again to unstage it)"),
                            ("a", "Stage or unstage all files"),
                            ("c", "Commit the staged files: opens the message box"),
                            ("Enter", "In the message box: save the commit"),
                            ("Esc", "In the message box: cancel"),
                        ], "try": "Run `lazygit`, press `j` twice to reach `notes.txt`, press `Space`, then `c`, type `Add glue to notes` and press `Enter`.",
                         "expect": "After `Space`, the line for `notes.txt` shows `M` in the first column: it is staged. `c` opens a `Commit summary` box and a `Commit description` box. After `Enter`, `notes.txt` leaves the Files panel and `Add glue to notes` is at the top of the Commits panel."},
                        {"type": "cmd", "where": "shell", "title": "Check the commit that lazygit made", "code": C('''
git -C /tmp/tw-lazygit log --oneline -1
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "A short hash and `Add glue to notes`. Then ` M app.py` and `?? scratch.txt`: the other two files are still not committed."},
                        {"type": "text", "body": "Press `a` to stage every file in one key. In the commit box, `Tab` moves to the description box. To write the message in your own editor, press `C` instead of `c`."},
                    ],
                },
                {
                    "h2": "Stage single lines or one change of a file in lazygit (partial commit)",
                    "intro": "`app.py` has three changes: the price, the tax and the shipping. Commit only the price and the tax.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Stage one change of a file and see it in the staged pane", "rows": [
                            ("Enter", "Open the selected file's changes (staging view)"),
                            ("Space", "Stage the change under the cursor"),
                            ("j / k", "Move to the next or previous change"),
                            ("Tab", "Switch between the Unstaged and Staged panes"),
                            ("Esc", "Go back to the Files panel"),
                        ], "try": "Press `2`, `<`, then `j` to reach `app.py`, then `Enter`. If a box about hunk selection appears, press `Enter` again. Press `Space` once.",
                         "expect": "The line for `app.py` changes from ` M` to `MM`: staged and still modified. The right side splits into `Unstaged changes` and `Staged changes`. The price change, `-    return 10` and `+    return 12`, moves to Staged changes."},
                        {"type": "cmd", "where": "shell", "title": "Check which lines are staged (git diff --cached)", "code": C('''
git -C /tmp/tw-lazygit diff --cached --stat
'''),
                         "expect": "` app.py | 2 +-` and `1 file changed, 1 insertion(+), 1 deletion(-)`: one line replaced, the price."},
                        {"type": "keys", "where": "lazygit", "title": "Stage single lines instead of a whole change (line mode)", "rows": [
                            ("a", "Switch between change mode and line-by-line mode"),
                            ("v", "Start selecting a range of lines"),
                            ("j / k", "Extend the range or move the cursor"),
                            ("Space", "Stage the selected lines"),
                            ("d", "Discard the selected lines from the file (cannot be undone)"),
                        ], "try": "Still in the staging view, press `a`, then `v`, `j` and `Space`.",
                         "expect": "The hint bar now reads `Select hunks: a`, which means you are in line mode. The two tax lines, `-    return amount * 0.2` and `+    return amount * 0.25`, move to Staged changes. The shipping change stays unstaged."},
                        {"type": "cmd", "where": "shell", "title": "Check the line count of the staged change", "code": C('''
git -C /tmp/tw-lazygit diff --cached --stat
'''),
                         "expect": "` app.py | 4 ++--` and `1 file changed, 2 insertions(+), 2 deletions(-)`: the price and the tax are staged, not the shipping."},
                        {"type": "keys", "where": "lazygit", "title": "Commit only the staged lines", "rows": [
                            ("Esc", "Go back to the Files panel"),
                            ("c", "Open the commit box"),
                            ("Enter", "Save the commit"),
                        ], "try": "Press `Esc`, then `c`, type `Raise price and tax` and press `Enter`.",
                         "expect": "`Raise price and tax` is at the top of the Commits panel. `app.py` stays in the Files panel as ` M`: the shipping change is still waiting."},
                        {"type": "cmd", "where": "shell", "title": "Check what is still not committed", "code": C('''
git -C /tmp/tw-lazygit log --oneline -1
git -C /tmp/tw-lazygit diff --stat
'''),
                         "expect": "A short hash and `Raise price and tax`. Then ` app.py | 2 +-` and `1 file changed, 1 insertion(+), 1 deletion(-)`: only the shipping line is left."},
                    ],
                },
                {
                    "h2": "Add to the last commit or change its message in lazygit (amend and reword)",
                    "intro": "Put the shipping change in the commit you just made. Then fix the message.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Add the staged changes to the last commit (amend)", "rows": [
                            ("Space", "Stage the file first"),
                            ("A", "Add the staged changes to the last commit"),
                            ("Enter", "Confirm the question"),
                        ], "try": "Press `2`, `<`, `j` to reach `app.py`, press `Space`, then `A` and `Enter`.",
                         "expect": "A popup titled `Amend last commit` asks `Are you sure you want to amend last commit?`. After `Enter`, `app.py` leaves the Files panel. The Commits panel has the same number of commits as before."},
                        {"type": "cmd", "where": "shell", "title": "Check that the amend added no new commit", "code": C('''
git -C /tmp/tw-lazygit log --oneline
git -C /tmp/tw-lazygit show --stat --format=%s HEAD
'''),
                         "expect": "Five commits, newest first: `Raise price and tax`, `Add glue to notes`, `Add notes`, `Add app.py`, `Add README`. Then the message `Raise price and tax` again and ` app.py | 6 +++---` with `1 file changed, 3 insertions(+), 3 deletions(-)`: price, tax and shipping are all in that one commit."},
                        {"type": "keys", "where": "lazygit", "title": "Change the message of a commit (reword)", "rows": [
                            ("4", "Go to the Commits panel"),
                            ("r", "Reword: edit the message of the selected commit"),
                            ("Ctrl-u", "In the message box: delete the old message"),
                            ("Enter", "Save the new message"),
                        ], "try": "Press `4`, `<` to select the top commit, then `r`, `Ctrl-u`, type `Raise price, tax and shipping` and press `Enter`.",
                         "expect": "A `Reword commit` box opens with `Raise price and tax` already in it. After `Enter`, the top of the Commits panel reads `Raise price, tax and shipping`."},
                        {"type": "cmd", "where": "shell", "title": "Check the new commit message", "code": C('''
git -C /tmp/tw-lazygit log --oneline -1
'''),
                         "expect": "A short hash and `Raise price, tax and shipping`. The hash is new: amend and reword give the commit a new hash."},
                        {"type": "text", "body": "Amend and reword rewrite a commit. After you push it, the next push has to be a force push (page 4)."},
                    ],
                },
                {
                    "h2": "Discard or ignore a file in lazygit (undo edits, delete a new file, .gitignore)",
                    "intro": "Throw away `scratch.txt`, then tell git to ignore a log file.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Discard changes to a file in lazygit", "rows": [
                            ("d", "Open the discard menu for the selected file"),
                            ("x", "In that menu: discard all changes of the file"),
                            ("u", "In that menu: discard only the unstaged part (file needs staged and unstaged changes)"),
                            ("D", "Open the reset menu: discard everything staged, unstaged or untracked at once"),
                        ], "try": "Press `2`, `>` to jump to `scratch.txt`, then `d` and `x`.",
                         "expect": "A `Discard changes` menu opens with `x Discard all changes` and `u Discard unstaged changes`. After `x`, `scratch.txt` disappears from the Files panel and from the folder. A discard cannot be undone."},
                        {"type": "cmd", "where": "shell", "title": "Check that the file is gone", "code": C('''
cd /tmp/tw-lazygit
command ls
git status --short
'''),
                         "expect": "`ls` lists `app.py`, `notes.txt` and `README.md` (the order depends on your locale), with no `scratch.txt`. `git status --short` prints nothing: the folder is clean."},
                        {"type": "cmd", "where": "shell", "title": "Create a log file that git should ignore", "code": C('''
cd /tmp/tw-lazygit
echo trace > debug.log
git status --short
'''),
                         "expect": "`?? debug.log`: git sees a new file."},
                        {"type": "keys", "where": "lazygit", "title": "Stop git from listing a file (ignore)", "rows": [
                            ("R", "Refresh the file list if a new file is missing"),
                            ("i", "Open the ignore menu for the selected file"),
                            ("i then i", "Add the file to .gitignore (commit that file to share the rule)"),
                            ("i then e", "Add the file to .git/info/exclude (only on your machine)"),
                        ], "try": "Press `2`, then `R`, then `i` and `e`.",
                         "expect": "The menu `Ignore or exclude file` lists `i Add to .gitignore` and `e Add to .git/info/exclude`. After `e`, `debug.log` leaves the Files panel."},
                        {"type": "cmd", "where": "shell", "title": "Check the ignore rule", "code": C('''
tail -n 1 /tmp/tw-lazygit/.git/info/exclude
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "`/debug.log` is the last line of the exclude file. `git status --short` prints nothing."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which lazygit key stages, commits and discards",
                "cards": [
                    ("Stage and commit from the Files panel", "Select a file first.", ["Key", "Action"], [
                        ["`Space`", "Stage or unstage the file"],
                        ["`a`", "Stage or unstage all files"],
                        ["`Enter`", "Open the file's changes to stage single lines"],
                        ["`c`", "Commit the staged files (`Enter` saves)"],
                        ["`C`", "Commit and write the message in your editor"],
                        ["`A`", "Add the staged changes to the last commit"],
                    ]),
                    ("Stage part of a file (staging view)", "After `Enter` on a file.", ["Key", "Action"], [
                        ["`Space`", "Stage the change or lines under the cursor"],
                        ["`a`", "Switch between change mode and line mode"],
                        ["`v`", "Select a range of lines"],
                        ["`Tab`", "Switch between Unstaged and Staged panes"],
                        ["`d`", "Discard the selected lines"],
                        ["`Esc`", "Back to the Files panel"],
                    ]),
                    ("Get rid of a change or a file", "Pick by what you want to happen.", ["Goal", "Keys"], [
                        ["Throw away my edits or delete a new file", "`d`, then `x`"],
                        ["Throw away only the unstaged part", "`d`, then `u`"],
                        ["Stop git from listing a file", "`i`, then `i` or `e`"],
                        ["Change the last commit's message", "`4`, `r`"],
                        ["Reset everything at once", "`D` opens the menu"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Commit the price fix and throw away the debug print",
                "frame": "You raised the price to 13 and left a debug print at the end of app.py. Commit the price and discard the print.",
                "open": "cd /tmp/tw-lazygit\nperl -pi -e 's/return 12/return 13/' app.py\necho 'print(\"debug\")' >> app.py\nlazygit",
                "steps": [
                    (None, "`2`, `<`, `j`, `Enter`", "Go to Files, jump to the tree root, select `app.py` and open its changes. Two changes show: `return 12` becomes `return 13`, and a new `print(\"debug\")` line at the end."),
                    (None, "`Space`", "Stage the price change. It moves to the Staged changes pane. The print stays unstaged."),
                    (None, "`Esc`", "Go back to the Files panel. `app.py` shows `MM`."),
                    (None, "`c`", "Open the commit box."),
                    (None, "`Raise price to 13`, `Enter`", "Type the message and save. `app.py` stays in the list as ` M` because of the print."),
                    (None, "`d`", "Open the discard menu for `app.py`."),
                    (None, "`x`", "Discard the print. `app.py` leaves the Files panel."),
                ],
                "after": "`git -C /tmp/tw-lazygit log --oneline -1` shows `Raise price to 13`, `git -C /tmp/tw-lazygit status --short` prints nothing, and `app.py` has no `print` line.",
                "meaning": "Stage only what belongs in the commit, then discard the rest. A discard cannot be undone, so read the diff before you press `x`.",
            },
            "practice": {
                "h2": "Check your answers: stage, commit, amend and discard",
                "qs": [
                    ("Mechanism", "Why does `A` not create a second commit?",
                     "What does amend do to the top commit?",
                     ["`A` is amend.", "It rewrites the top commit with your staged changes added.", "The commit count stays the same and the hash changes."],
                     "Amend replaces the last commit instead of adding one."),
                    ("Keystrokes", "Which keys stage one change of `app.py` and commit it?",
                     "Open the file, stage, go back, commit.",
                     ["Select `app.py` in the Files panel and press `Enter`.", "Press `Space` on the change you want.", "Press `Esc`, then `c`, type the message and press `Enter`."],
                     "`Enter`, `Space`, `Esc`, `c`, message, `Enter`."),
                    ("Application", "How do I stop git from listing `debug.log` without editing `.gitignore`?",
                     "The ignore menu has two choices.",
                     ["Select `debug.log` in the Files panel.", "Press `i` to open the ignore menu.", "Press `e` to add it to `.git/info/exclude`."],
                     "`i`, then `e`. Only your machine ignores the file."),
                    ("Common mistake", "Why does `d` then `u` do nothing on my file?",
                     "Read the bar at the bottom of the popup.",
                     ["`u` discards only the unstaged part.", "It works only when the file has staged and unstaged changes.", "The bar says `Disabled` for any other file."],
                     "Use `d` then `x` to discard all changes of the file."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Create a branch, squash commits, rebase and merge in lazygit",
            "subtitle": "Make a branch with n, drop or squash commits, rebase onto main, merge with M, copy one commit to another branch",
            "idea": (
                "Press n for a new branch, s to squash a commit, r to rebase and M to merge.",
                [
                    ("Create a new branch", "n", "In the Branches panel (3). Type a name, then Enter."),
                    ("Squash a commit into the one below", "s", "In the Commits panel (4). Enter confirms."),
                    ("Rebase the current branch onto main", "r", "Select main in panel 3, press r, then s."),
                    ("Merge a branch into the current branch", "M", "Select the other branch in panel 3, then press M."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I clean up my commits before merging? `git rebase -i` opens a text file where one typo in `pick`, `squash` or `fixup` rewrites the wrong history.",
                "fix": "Open the Commits panel in LazyGit. Press one key per commit: `s` squash, `f` fixup, `d` drop, `r` reword. The list shows what will happen before you continue.",
            },
            "drills": [
                {
                    "h2": "Create a branch and switch between branches in lazygit",
                    "intro": "Go on with the practice repo of page 2. Work on a branch called `tidy-up`, so `main` stays clean.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Create a new branch in lazygit", "rows": [
                            ("3", "Go to the Local branches panel"),
                            ("n", "New branch: type a name"),
                            ("Enter", "Create the branch and switch to it"),
                        ], "try": "Run `lazygit`, press `3`, then `n`, type `tidy-up` and press `Enter`.",
                         "expect": "A box titled `New branch name (branch is off of 'main')` opens. After `Enter`, the Status panel reads `tw-lazygit → tidy-up` and the Branches panel lists `* tidy-up` above `main`."},
                        {"type": "cmd", "where": "shell", "title": "Make four quick commits on the branch", "code": C('''
cd /tmp/tw-lazygit
echo 'labels: 100' > labels.txt && git add labels.txt && git commit -q -m 'Add labels'
echo 'labels: 200' > labels.txt && git commit -qa -m 'Fix label count'
echo 'ribon: red' > ribbon.txt && git add ribbon.txt && git commit -q -m 'Add ribon'
echo 'print(debug)' > debug.py && git add debug.py && git commit -q -m 'Debug print'
git log --oneline
'''),
                         "expect": "Ten commits, newest first: `Debug print`, `Add ribon`, `Fix label count`, `Add labels`, then `Raise price to 13` and the five older ones. `ribon` is a typo on purpose."},
                        {"type": "keys", "where": "lazygit", "title": "Check out a branch in lazygit", "rows": [
                            ("Space", "Check out the selected branch in lazygit"),
                            ("-", "Check out the previous branch"),
                            ("j / k", "Select the next or previous branch"),
                        ], "try": "In the Branches panel press `j` to select `main`, then `Space`, then `-`.",
                         "expect": "`Space` moves the `*` to `main` and the Status panel reads `tw-lazygit → main`. `-` brings you back to `tidy-up`."},
                        {"type": "cmd", "where": "shell", "title": "Check which branch you are on", "code": C('''
git -C /tmp/tw-lazygit branch
'''),
                         "expect": "`  main` and `* tidy-up`. The star marks the branch you are on."},
                    ],
                },
                {
                    "h2": "Squash, fix up, drop or reword commits in lazygit (interactive rebase)",
                    "intro": "`tidy-up` has a debug commit, a typo in `ribon` and a fix for the label count. Clean it up before merging: drop the debug print, fold the fix into `Add labels`, fix the typo. Drop removes the commit's changes; rewrite only unshared history.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Drop and fix up commits with an interactive rebase", "rows": [
                            ("4", "Go to the Commits panel"),
                            ("<", "Select the top commit"),
                            ("i", "Start an interactive rebase: every commit of the branch gets a word, `pick`"),
                            ("d", "Mark the selected commit as drop"),
                            ("f", "Mark the selected commit as fixup (it joins the commit below)"),
                            ("s", "Mark the selected commit as squash"),
                            ("m", "Open the rebase menu: `c` continue, `a` abort, `s` skip"),
                        ], "try": "Press `4`, `<`, then `i`. Press `d` on `Debug print`, press `j` twice to reach `Fix label count` and press `f`. Then press `m` and `c`.",
                         "expect": "After `i`, the commits of the branch show `pick` in front of their names. `d` changes the word to `drop` and `f` changes it to `fixup`. The `m` menu lists `c continue`, `a abort` and `s skip`. After `c`, the branch has only `Add ribon` on top of `Add labels`."},
                        {"type": "cmd", "where": "shell", "title": "Check the cleaned-up history", "code": C('''
git -C /tmp/tw-lazygit log --oneline -5
'''),
                         "expect": "`Add ribon`, `Add labels`, `Raise price to 13`, `Raise price, tax and shipping` and `Add glue to notes`. `Debug print` and `Fix label count` are gone. The hashes of the two kept commits are new."},
                        {"type": "keys", "where": "lazygit", "title": "Fix a typo in a commit message (reword)", "rows": [
                            ("r", "Reword: edit the message of the selected commit"),
                            ("Ctrl-u", "In the message box: delete the old message"),
                            ("Enter", "Save the new message"),
                        ], "try": "In the Commits panel press `<` to select the top commit, then `r`, `Ctrl-u`, type `Add ribbon` and press `Enter`.",
                         "expect": "The top of the Commits panel reads `Add ribbon`."},
                        {"type": "keys", "where": "lazygit", "title": "Move a commit up or down in lazygit", "rows": [
                            ("Ctrl-j", "Move the selected commit down one place"),
                            ("Ctrl-k", "Move the selected commit up one place"),
                        ], "try": "With `Add ribbon` selected, press `Ctrl-j`, then `Ctrl-k`.",
                         "expect": "`Add ribbon` and `Add labels` swap places, then swap back. Two commits that change the same lines stop with a conflict when you swap them."},
                        {"type": "cmd", "where": "shell", "title": "Check the new commit message", "code": C('''
git -C /tmp/tw-lazygit log --oneline -3
'''),
                         "expect": "A short hash and `Add ribbon`, then `Add labels`, then `Raise price to 13`."},
                        {"type": "text", "body": "You do not need `i` for one commit. Select it and press `s` (squash into the commit below), `f` (fixup, a menu asks which kind), `d` (drop) or `r` (reword). Read the diff before you rewrite a commit."},
                    ],
                },
                {
                    "h2": "Rebase my branch onto main in lazygit",
                    "intro": "Someone adds a commit to `main` while you work on `tidy-up`. A rebase puts your commits on top of it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Add a new commit to main while your branch waits", "code": C('''
cd /tmp/tw-lazygit
git switch -q main
printf '\\ndef tip(amount):\\n    return amount * 0.1\\n' >> app.py
git commit -qam 'Add tip()'
git switch -q tidy-up
git log --oneline --graph --all
'''),
                         "expect": "A graph with a fork. `Add tip()` is alone on one line. `Add ribbon` and `Add labels` run beside it on a second line. Both lines meet at `Raise price to 13`, which is followed by the five older commits."},
                        {"type": "keys", "where": "lazygit", "title": "Rebase the current branch onto main", "rows": [
                            ("3", "Go to the Local branches panel"),
                            ("r", "Open the rebase menu for the selected branch"),
                            ("s", "In the menu: simple rebase onto the selected branch"),
                            ("i", "In the menu: interactive rebase onto the selected branch"),
                        ], "try": "Press `3`, then `j` to select `main` (not your own branch), then `r` and `s`.",
                         "expect": "A menu titled `Rebase 'tidy-up'` lists `s Simple rebase onto 'main'`, `i Interactive rebase onto 'main'` and `b Rebase onto base branch (main)`. After `s`, your two commits sit on top of `Add tip()`."},
                        {"type": "cmd", "where": "shell", "title": "Check that your commits now sit on top of main", "code": C('''
git -C /tmp/tw-lazygit log --oneline --graph --all
'''),
                         "expect": "One straight line, no fork: `Add ribbon`, `Add labels`, `Add tip()`, `Raise price to 13`, then the five older commits. `Add ribbon` and `Add labels` have new hashes."},
                    ],
                },
                {
                    "h2": "Merge a branch into main in lazygit and delete it",
                    "intro": "Check out `main`, merge `tidy-up` into it, then delete the branch you no longer need.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Merge a branch into the current branch", "rows": [
                            ("Space", "Check out the selected branch"),
                            ("M", "Merge the selected branch into the branch you are on"),
                            ("Enter", "Pick the highlighted line of the merge menu"),
                        ], "try": "In the Branches panel press `j` to select `main`, `Space`, then `j` to select `tidy-up`, then `M` and `Enter`.",
                         "expect": "The `Merge` menu lists `m Regular merge (fast-forward)`, `n Regular merge (with merge commit)` and two squash lines. A line under the menu says `Fast-forward 'main' to 'tidy-up' without creating a merge commit.` After `Enter`, `main` moves forward to `Add ribbon`."},
                        {"type": "text", "body": "The letters in the `Merge` menu depend on the branches. When both have new commits, `m` makes a merge commit and the fast-forward line gets another letter. Read the line before you press a key."},
                        {"type": "cmd", "where": "shell", "title": "Check that main has the commits of tidy-up", "code": C('''
git -C /tmp/tw-lazygit log --oneline -4
git -C /tmp/tw-lazygit branch
'''),
                         "expect": "`Add ribbon`, `Add labels`, `Add tip()` and `Raise price to 13`, then `* main` and `  tidy-up`. No merge commit appears: the fast-forward only moved `main`."},
                        {"type": "keys", "where": "lazygit", "title": "Delete a branch after merging it", "rows": [
                            ("d", "Open the delete menu for the selected branch"),
                            ("c", "In the menu: delete the local branch"),
                            ("r", "In the menu: delete the remote branch"),
                            ("b", "In the menu: delete the local and the remote branch"),
                        ], "try": "With `tidy-up` still selected, press `d`, then `c`.",
                         "expect": "A menu titled `Delete branch 'tidy-up'?` lists `c Delete local branch`, `r Delete remote branch` and `b Delete local and remote branch`. After `c`, only `main` is left in the Branches panel."},
                        {"type": "cmd", "where": "shell", "title": "Check that the branch is gone", "code": C('''
git -C /tmp/tw-lazygit branch
'''),
                         "expect": "`* main` and nothing else."},
                    ],
                },
                {
                    "h2": "Copy one commit to another branch in lazygit (cherry-pick)",
                    "intro": "Take a single commit from the branch `extras` and put it on `main`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make a branch with one commit to copy", "code": C('''
cd /tmp/tw-lazygit
git switch -q -c extras
printf '\\ndef gift(box):\\n    return box + 1\\n' >> app.py
git commit -qam 'Add gift()'
git switch -q main
git branch
git log --oneline -1 extras
'''),
                         "expect": "`  extras` and `* main`. Then a short hash and `Add gift()`: the commit lives on `extras` only."},
                        {"type": "keys", "where": "lazygit", "title": "Copy a commit from another branch (cherry-pick)", "rows": [
                            ("Enter", "In the Branches panel: show the commits of the selected branch"),
                            ("C", "Copy the selected commit"),
                            ("Esc", "Leave the branch's commit list"),
                            ("V", "Paste the copied commit onto the current branch (cherry-pick)"),
                        ], "try": "Press `3`, `j` to select `extras`, `Enter`, then `C`. Press `Esc`, `4`, then `V` and `Enter`.",
                         "expect": "The commit list is titled `Commits (extras)`. After `C`, the bottom right reads `1 commit copied`. `V` asks `Are you sure you want to cherry-pick the 1 copied commit(s) onto this branch?`. After `Enter`, `Add gift()` is at the top of the Commits panel of `main`."},
                        {"type": "cmd", "where": "shell", "title": "Check that the commit was copied", "code": C('''
git -C /tmp/tw-lazygit log --oneline -3
'''),
                         "expect": "A short hash and `Add gift()`, then `Add ribbon` and `Add labels`. The hash differs from the one on `extras`: the commit is a copy."},
                        {"type": "keys", "where": "lazygit", "title": "Rename a branch or delete one that is not merged", "rows": [
                            ("R", "Rename the selected branch (the box is filled with the old name)"),
                            ("Ctrl-u", "In the name box: delete the old name"),
                            ("d", "Open the delete menu"),
                            ("c", "In the menu: delete the local branch"),
                        ], "try": "In the Branches panel press `j` to select `extras`, then `R`, `Ctrl-u`, type `gifts` and press `Enter`. Press `d`, `c` and `Enter`.",
                         "expect": "A box titled `Enter new branch name for branch extras:` opens. A second box titled `Force delete branch` says `'gifts' is not fully merged. Are you sure you want to delete it?`. After `Enter`, only `main` is left."},
                        {"type": "cmd", "where": "shell", "title": "Check the branches after the rename and delete", "code": C('''
git -C /tmp/tw-lazygit branch
'''),
                         "expect": "`* main` and nothing else."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which lazygit key works on branches and commits",
                "cards": [
                    ("Branch keys (Branches panel, 3)", "Select a branch first.", ["Key", "Action"], [
                        ["`n`", "New branch from the selected branch"],
                        ["`Space`", "Check out the selected branch"],
                        ["`-`", "Check out the previous branch"],
                        ["`M`", "Merge the selected branch into the current one"],
                        ["`r`", "Rebase the current branch onto the selected one"],
                        ["`R`", "Rename the selected branch"],
                        ["`d`", "Delete menu: local, remote or both"],
                    ]),
                    ("Commit keys (Commits panel, 4)", "Select a commit first.", ["Key", "Action"], [
                        ["`s`", "Squash into the commit below"],
                        ["`f`", "Fixup into the commit below"],
                        ["`d`", "Drop the commit"],
                        ["`r`", "Reword the message"],
                        ["`i`", "Start an interactive rebase"],
                        ["`Ctrl-j` / `Ctrl-k`", "Move the commit down or up"],
                        ["`C` then `V`", "Copy it, then paste it on another branch"],
                    ]),
                    ("Pick the way to combine work", "Match the goal.", ["Goal", "Keys"], [
                        ["Put my commits on top of main", "Select `main`, `r`, `s`"],
                        ["Bring a finished branch into main", "Check out `main`, select the branch, `M`"],
                        ["Take one commit from another branch", "`C`, then `V`"],
                        ["Make several commits one", "`s` on each, or `i`"],
                        ["Remove a commit", "`d`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Squash three small commits into one and merge it into main",
                "frame": "You made three small commits on a cards branch. Turn them into one commit, then bring it into main.",
                "open": "cd /tmp/tw-lazygit\ngit switch -q -c cards\necho 'card: red' > cards.txt && git add cards.txt && git commit -q -m 'Add cards'\necho 'card: blue' >> cards.txt && git commit -qam 'Add blue card'\necho 'card: gold' >> cards.txt && git commit -qam 'Add gold card'\nlazygit",
                "steps": [
                    (None, "`4`, `<`", "Go to the Commits panel and select the top commit, `Add gold card`."),
                    (None, "`s`, `Enter`", "Squash it into the commit below. The popup asks `Are you sure you want to squash the selected commit(s) into the commit below?`"),
                    (None, "`s`, `Enter`", "Squash again. Only `Add cards` is left on top of the older commits."),
                    (None, "`r`", "Open the reword box. It shows `Add cards`, and the description holds the older messages."),
                    (None, "`Ctrl-u`, `Add three cards`, `Enter`", "Replace the summary and save."),
                    (None, "`3`, `j`, `Space`", "Go to the Branches panel, select `main` and check it out."),
                    (None, "`j`, `M`, `Enter`", "Select `cards`, open the merge menu and pick the fast-forward line."),
                ],
                "after": "`git -C /tmp/tw-lazygit branch` lists `cards` and `* main`. `git -C /tmp/tw-lazygit log --oneline -3` shows `Add three cards`, `Add gift()` and `Add ribbon`. `git -C /tmp/tw-lazygit show --stat --format=%s HEAD` ends with ` cards.txt | 3 +++`.",
                "meaning": "Squash first, merge second: `main` gets one commit instead of three small ones. The old messages stay in the commit description.",
            },
            "practice": {
                "h2": "Check your answers: branches, squash, rebase and merge",
                "qs": [
                    ("Mechanism", "Why do my commits get new hashes after a rebase?",
                     "A commit's hash depends on its parent.",
                     ["Rebase puts your commits on top of a new parent.", "Git makes a copy of each commit on that parent.", "The content is the same, so only the hash changes."],
                     "A rebase copies your commits onto a new base, so each copy has a new hash."),
                    ("Keystrokes", "Which keys rebase my branch onto `main`?",
                     "Select the target, not your own branch.",
                     ["Press `3` and select `main` in the Branches panel.", "Press `r` to open the rebase menu.", "Press `s` for a simple rebase."],
                     "`3`, select `main`, `r`, `s`."),
                    ("Application", "How do I merge `tidy-up` into `main`?",
                     "You merge into the branch you are on.",
                     ["Select `main` and press `Space` to check it out.", "Select `tidy-up` and press `M`.", "Pick the fast-forward line with `Enter`."],
                     "Check out `main`, select `tidy-up`, press `M`."),
                    ("Common mistake", "Why did `m` make a merge commit when it fast-forwarded last time?",
                     "Read the menu before you press a letter.",
                     ["The letters follow the menu order.", "When both branches have new commits, `m` is the regular merge.", "The fast-forward line gets another letter."],
                     "Read the line you press. The letters change with the branches."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Stash, undo, push, pull and fix a merge conflict in lazygit",
            "subtitle": "Stash with s, undo with z, push with P, pull with p, fetch with f, pick a side in a merge conflict",
            "idea": (
                "Press s to stash, z to undo, P to push and p to pull. A conflict opens with Enter on the file.",
                [
                    ("Stash my unfinished changes", "s", "In the Files panel. Name it, then Enter."),
                    ("Undo my last action", "z", "Enter confirms. Z redoes it."),
                    ("Push my commits", "P", "The first time, a box asks for the remote and branch."),
                    ("Pull new commits", "p", "Fetch first with f to see how many are waiting."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I undo a commit, put my work aside before a pull, or fix a merge conflict? The git commands are easy to mix up, and a wrong reset loses work.",
                "fix": "In LazyGit, `s` stashes, `z` undoes a supported local reflog action, and a conflict shows both versions side by side.",
            },
            "drills": [
                {
                    "h2": "Stash my changes and get them back in lazygit",
                    "intro": "Go on with the practice repo of page 3. Start an edit, put it on the shelf, bring it back.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make an unfinished change to notes.txt", "code": C('''
cd /tmp/tw-lazygit
echo 'buy ink' >> notes.txt
git status --short
'''),
                         "expect": "` M notes.txt`: one file has a change that is not committed."},
                        {"type": "keys", "where": "lazygit", "title": "Stash my changes and keep working (git stash)", "rows": [
                            ("s", "Stash the changes of tracked files: type a name"),
                            ("S", "Open the stash options: all, keep index, include untracked, staged only, unstaged only"),
                            ("5", "Go to the Stash panel"),
                        ], "try": "Run `lazygit`, press `2`, then `s`, type `ink` and press `Enter`. Press `5`.",
                         "expect": "A box titled `Stash changes` asks for a name. After `Enter`, `notes.txt` leaves the Files panel. The Stash panel lists `On main: ink`."},
                        {"type": "cmd", "where": "shell", "title": "Check the stash", "code": C('''
git -C /tmp/tw-lazygit stash list
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "`stash@{0}: On main: ink`. `git status --short` prints nothing: the folder is clean."},
                        {"type": "keys", "where": "lazygit", "title": "Put a stash back (apply, pop or drop)", "rows": [
                            ("Space", "Apply the stash and keep it in the list"),
                            ("g", "Pop the stash: apply it and remove it from the list"),
                            ("d", "Drop the stash: remove it without applying"),
                        ], "try": "In the Stash panel (`5`) press `Space`, then `Enter`.",
                         "expect": "A popup asks `Are you sure you want to apply this stash entry?`. After `Enter`, the focus moves to the Files panel, `notes.txt` is back, and the stash is still in the Stash panel."},
                        {"type": "cmd", "where": "shell", "title": "Check that the stash is still there after apply", "code": C('''
git -C /tmp/tw-lazygit stash list
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "`stash@{0}: On main: ink` and ` M notes.txt`: the change is back and the shelf still holds a copy."},
                        {"type": "keys", "where": "lazygit", "title": "Delete a stash you no longer need", "rows": [
                            ("5", "Go to the Stash panel"),
                            ("d", "Drop the selected stash"),
                            ("Enter", "Confirm"),
                        ], "try": "Press `5`, then `d` and `Enter`.",
                         "expect": "A popup titled `Stash drop` asks `Are you sure you want to drop the selected stash entry(ies)?`. After `Enter`, the Stash panel is empty. `notes.txt` keeps its change."},
                        {"type": "text", "body": "Use `Space` or `g`, not both: the change is already in the folder after an apply. `s` leaves new untracked files where they are. For those, press `S`, then `U`."},
                    ],
                },
                {
                    "h2": "Undo my last commit or action in lazygit (z, Z, revert, reflog)",
                    "intro": "Commit the notes change, undo the commit, bring it back, lose it on purpose, and recover it. Undo cannot restore discarded edits, undo remote pushes, or run during a merge/rebase. Hard reset overwrites staged and unstaged tracked edits and can overwrite obstructing untracked files; commit or stash first.",
                    "blocks": [
                        {"type": "keys", "where": "lazygit", "title": "Commit the change", "rows": [
                            ("2", "Go to the Files panel"),
                            ("Space", "Stage the selected file"),
                            ("c", "Open the commit box"),
                            ("Enter", "Save the commit"),
                        ], "try": "Press `2`, `Space`, `c`, type `Buy ink` and press `Enter`.",
                         "expect": "`Buy ink` is at the top of the Commits panel and the Files panel is empty."},
                        {"type": "cmd", "where": "shell", "title": "Check the commit", "code": C('''
git -C /tmp/tw-lazygit log --oneline -2
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "A short hash and `Buy ink`, then `Add three cards`. `git status --short` prints nothing."},
                        {"type": "keys", "where": "lazygit", "title": "Undo a local reflog action in lazygit (z) and redo it (Z)", "rows": [
                            ("z", "Undo a supported local reflog action"),
                            ("Z", "Redo the action you undid"),
                            ("Enter", "Confirm the question"),
                        ], "try": "Press `z`, then `Enter`. Then press `Z` and `Enter`.",
                         "expect": "`z` asks `Are you sure you want to soft reset to` and a hash. After `Enter`, `Buy ink` is gone from Commits and `notes.txt` is staged again in Files. `Z` asks `Are you sure you want to hard reset to` and a hash, with a note about an auto-stash. After `Enter`, the commit is back."},
                        {"type": "cmd", "where": "shell", "title": "Check the branch after undo and redo", "code": C('''
git -C /tmp/tw-lazygit log --oneline -2
git -C /tmp/tw-lazygit status --short
'''),
                         "expect": "`Buy ink` on top of `Add three cards`, and nothing from `git status --short`: undo and redo ended in the same place."},
                        {"type": "keys", "where": "lazygit", "title": "Get back a commit I dropped by mistake (reflog)", "rows": [
                            ("4", "Go to the Commits panel"),
                            ("d", "Drop the selected commit (Enter confirms)"),
                            ("]", "Switch the panel to the Reflog tab"),
                            ("g", "Open the reset menu for the selected line"),
                            ("h", "In the menu: hard reset to that line"),
                        ], "try": "Press `4`, `<`, then `d` and `Enter` to drop `Buy ink`. Press `]`, `<`, then `j` twice to reach `[lazygit redo]: updating HEAD`. Press `g`, then `h`.",
                         "expect": "After the drop, `Buy ink` is gone from the log. The Reflog still has it: the line `[lazygit redo]: updating HEAD` shows the state before the drop. `g` opens a menu with `m Mixed reset`, `s Soft reset` and `h Hard reset`. After `h`, `Buy ink` is back at the top."},
                        {"type": "cmd", "where": "shell", "title": "Check that the dropped commit is back", "code": C('''
git -C /tmp/tw-lazygit log --oneline -2
'''),
                         "expect": "A short hash and `Buy ink`, then `Add three cards`. The hash is the same as before the drop: reset restores the original commit."},
                        {"type": "keys", "where": "lazygit", "title": "Undo a commit with a new commit (revert)", "rows": [
                            ("[", "Switch the panel back to the Commits tab"),
                            ("t", "Revert the selected commit"),
                            ("Enter", "Confirm"),
                        ], "try": "Press `[`, `<`, then `t` and `Enter`.",
                         "expect": "A popup asks `Are you sure you want to revert` and a hash. After `Enter`, `Revert \"Buy ink\"` is at the top of the Commits panel and `Buy ink` stays below it."},
                        {"type": "cmd", "where": "shell", "title": "Check the revert", "code": C('''
git -C /tmp/tw-lazygit log --oneline -3
tail -n 2 /tmp/tw-lazygit/notes.txt
'''),
                         "expect": "`Revert \"Buy ink\"`, `Buy ink` and `Add three cards`. The last two lines of `notes.txt` are `buy boxes` and `buy glue`: the `buy ink` line is gone."},
                        {"type": "text", "body": "Use `z` for something only on your machine. Use `t` for a commit you already pushed: it adds a new commit and rewrites nothing."},
                    ],
                },
                {
                    "h2": "Fix a merge conflict in lazygit (pick a side)",
                    "intro": "Two branches change the same line. Merge them and choose which line stays.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make two branches that change the same line", "code": C('''
cd /tmp/tw-lazygit
git switch -q -c tax-cut
perl -pi -e 's/0\\.25/0.18/' app.py
git commit -qam 'Cut tax to 0.18'
git switch -q main
perl -pi -e 's/0\\.25/0.3/' app.py
git commit -qam 'Raise tax to 0.3'
git log --oneline --graph --all -n 4
'''),
                         "expect": "A graph with a fork: `Raise tax to 0.3` on one line, `Cut tax to 0.18` beside it, both starting from `Revert \"Buy ink\"`."},
                        {"type": "keys", "where": "lazygit", "title": "Merge a branch and see the conflict", "rows": [
                            ("3", "Go to the Local branches panel"),
                            ("M", "Merge the selected branch into the current one"),
                            ("Enter", "Pick the highlighted line of the menu"),
                        ], "try": "Press `3`, `j` to select `tax-cut`, then `M` and `Enter`. Press `Enter` on `View conflicts`.",
                         "expect": "The `Merge` menu starts with `m Regular merge (with merge commit)`. After `Enter`, a `Conflicts!` popup offers `View conflicts` and `a Abort the merge`. After the second `Enter`, the Status panel reads `(merging) tw-lazygit → main`, and the Files panel is marked `(only conflicting)` and lists `UU app.py`."},
                        {"type": "keys", "where": "lazygit", "title": "Pick which side to keep in a merge conflict", "rows": [
                            ("Enter", "Open the conflicting file"),
                            ("Up / Down", "Go to the previous or next hunk"),
                            ("Space", "Keep the selected hunk"),
                            ("b", "Keep both hunks"),
                            ("z", "Undo the last pick"),
                        ], "try": "Select `app.py` and press `Enter`. Press `Down`, then `Space`, then `Enter`.",
                         "expect": "The file shows `<<<<<<< HEAD`, `return amount * 0.3`, `=======`, `return amount * 0.18` and `>>>>>>> tax-cut`. The bottom bar lists `Pick hunk: <space>` and `Pick both hunks: b`. After `Space`, a popup asks `All merge conflicts resolved. Continue the merge?`. After `Enter`, `(merging)` leaves the Status panel and `Merge branch 'tax-cut'` is at the top of Commits."},
                        {"type": "cmd", "where": "shell", "title": "Check the merge commit and the line you kept", "code": C('''
git -C /tmp/tw-lazygit log --oneline --graph -n 4
grep -n 'return amount' /tmp/tw-lazygit/app.py
'''),
                         "expect": "A graph with `Merge branch 'tax-cut'` on top, joining `Cut tax to 0.18` and `Raise tax to 0.3`. Then `5:    return amount * 0.18` and `11:    return amount * 0.1`: the tax-cut line won."},
                        {"type": "text", "body": "To give up, press `a` in the `Conflicts!` popup, or `Esc` in the Files panel while the status says `(merging)`, then `Enter` to confirm. Your files go back to before the merge."},
                    ],
                },
                {
                    "h2": "Push, fetch and pull in lazygit (with a local remote)",
                    "intro": "A bare repo on disk plays the part of GitHub, so nothing leaves your machine. This disposable local demo is an exception: it rewrites `main` only in the practice remote. For shared history, revert; amend and force-push only an unshared personal branch.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a local remote and connect it", "code": C('''
git init -q --bare -b main /tmp/tw-lazygit-remote.git
git -C /tmp/tw-lazygit remote add origin /tmp/tw-lazygit-remote.git
git -C /tmp/tw-lazygit remote -v
'''),
                         "expect": "Two lines: `origin	/tmp/tw-lazygit-remote.git (fetch)` and `origin	/tmp/tw-lazygit-remote.git (push)`."},
                        {"type": "keys", "where": "lazygit", "title": "Push a branch for the first time", "rows": [
                            ("P", "Push the current branch"),
                            ("p", "Pull the current branch"),
                            ("f", "Fetch: look for new commits without changing your files"),
                        ], "try": "Press `2`, then `P`, then `Enter`.",
                         "expect": "A box titled `Enter upstream as '<remote> <branchname>'` is filled with `origin main`. After `Enter`, the Status panel reads `✓ tw-lazygit → main` and the Branches panel shows `* main ✓`."},
                        {"type": "cmd", "where": "shell", "title": "Check that the remote got the commits", "code": C('''
git -C /tmp/tw-lazygit-remote.git log --oneline -1
git -C /tmp/tw-lazygit status -sb
'''),
                         "expect": "A short hash and `Merge branch 'tax-cut'`. Then `## main...origin/main`: your branch and the remote match."},
                        {"type": "cmd", "where": "shell", "title": "Pretend a teammate pushes a commit", "code": C('''
git clone -q /tmp/tw-lazygit-remote.git /tmp/tw-lazygit-teammate
cd /tmp/tw-lazygit-teammate
git config user.name 'Ana Ray'
git config user.email 'ana@example.com'
echo 'buy staples' >> notes.txt
git commit -qam 'Add staples'
git push -q origin main
git log --oneline -1
'''),
                         "expect": "A short hash and `Add staples`. The commit is on the remote now, not in `/tmp/tw-lazygit`."},
                        {"type": "keys", "where": "lazygit", "title": "Check for new commits (fetch) and download them (pull)", "rows": [
                            ("2", "Go to the Files panel first"),
                            ("f", "Fetch"),
                            ("p", "Pull"),
                        ], "try": "Press `2`, then `f`, wait two seconds, then `p`.",
                         "expect": "After `f`, the Status panel reads `↓1 tw-lazygit → main` and the Branches panel shows `* main ↓1`: one commit is waiting. After `p`, both show `✓` and `Add staples` is at the top of the Commits panel."},
                        {"type": "text", "body": "Press `2` before `f`. In the Commits panel, `f` means fixup and changes your commits."},
                        {"type": "cmd", "where": "shell", "title": "Check that you have the teammate's commit", "code": C('''
git -C /tmp/tw-lazygit log --oneline -2
git -C /tmp/tw-lazygit status -sb
'''),
                         "expect": "`Add staples` on top of `Merge branch 'tax-cut'`, then `## main...origin/main` with no `behind`."},
                        {"type": "cmd", "where": "shell", "title": "Make a change to commit and push", "code": C('''
cd /tmp/tw-lazygit
echo 'buy rope' >> notes.txt
git status --short
'''),
                         "expect": "` M notes.txt`. LazyGit lists the file after a few seconds. Press `R` in lazygit to refresh at once."},
                        {"type": "keys", "where": "lazygit", "title": "Commit and push my change", "rows": [
                            ("Space", "Stage the file"),
                            ("c", "Commit"),
                            ("P", "Push (no box the second time)"),
                        ], "try": "Press `2`, `Space`, `c`, type `Add rope to notes`, press `Enter`, then `P`.",
                         "expect": "After the commit, the Status panel reads `↑1 tw-lazygit → main`: one commit to upload. After `P`, it reads `✓` and no box appears."},
                        {"type": "cmd", "where": "shell", "title": "Check that the remote has your commit", "code": C('''
git -C /tmp/tw-lazygit-remote.git log --oneline -1
'''),
                         "expect": "A short hash and `Add rope to notes`."},
                        {"type": "cmd", "where": "shell", "title": "Change the pushed commit: disposable local demo", "code": C('''
cd /tmp/tw-lazygit
echo 'buy twine' >> notes.txt
git status --short
'''),
                         "expect": "` M notes.txt`."},
                        {"type": "keys", "where": "lazygit", "title": "Push after changing a commit (force push)", "rows": [
                            ("A", "Add the staged file to the last commit"),
                            ("P", "Push: a diverged branch asks before it force pushes"),
                            ("Enter", "In the Force push box: force push"),
                            ("Esc", "In the Force push box: cancel"),
                        ], "try": "Press `2`, `Space`, `A`, `Enter`, then `P`.",
                         "expect": "After the amend, the Status panel reads `↓1↑1`: your commit and the remote's copy differ. `P` opens a `Force push` box: `Your branch has diverged from the remote branch. Press <esc> to cancel, or <enter> to force push.` After `Enter`, the Status panel reads `✓`."},
                        {"type": "cmd", "where": "shell", "title": "Check that the remote has the amended commit", "code": C('''
git -C /tmp/tw-lazygit-remote.git log --oneline -2
git -C /tmp/tw-lazygit status -sb
'''),
                         "expect": "A short hash and `Add rope to notes`, then `Add staples`. Then `## main...origin/main`. The remote copy of `Add rope to notes` was replaced, not added to."},
                        {"type": "text", "body": "A force push replaces commits on the remote. This disposable local demo is an exception for the practice `main`. For shared history, revert; amend and force-push only an unshared personal branch."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which lazygit key stashes, undoes, syncs and resolves",
                "cards": [
                    ("Stash keys", "Files panel and Stash panel (5).", ["Key", "Action"], [
                        ["`s`", "Stash tracked changes (name it)"],
                        ["`S`", "Stash options, such as untracked files"],
                        ["`Space`", "Apply the stash, keep it"],
                        ["`g`", "Pop the stash: apply and remove"],
                        ["`d`", "Drop the stash"],
                    ]),
                    ("Undo keys", "Pick by how far the mistake went.", ["Goal", "Keys"], [
                        ["Undo a supported local reflog action", "`z`, `Enter`"],
                        ["Redo it", "`Z`, `Enter`"],
                        ["Undo a commit that is already pushed", "`t`, `Enter`"],
                        ["Get back a dropped commit", "`4`, `]`, select the line, `g`, `h`"],
                    ]),
                    ("Sync keys and what the arrows mean", "Press them in the Files panel.", ["Key or sign", "Meaning"], [
                        ["`f`", "Fetch: look for new commits"],
                        ["`p`", "Pull: download and merge them"],
                        ["`P`", "Push (a box asks the first time)"],
                        ["`↑1`", "One commit to upload"],
                        ["`↓1`", "One commit to download"],
                        ["`✓`", "In sync with the remote"],
                    ]),
                    ("Merge conflict keys", "Open the file with `Enter`.", ["Key", "Action"], [
                        ["`Up` / `Down`", "Previous or next hunk"],
                        ["`Space`", "Keep this hunk"],
                        ["`b`", "Keep both hunks"],
                        ["`z`", "Undo the last pick"],
                        ["`Esc`, then `Enter`", "Request and confirm aborting the merge (from the Files panel)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Stash my edit, pull a teammate's change and pop the stash",
                "frame": "You edited notes.txt. A teammate pushed a change to the same file. Pull refuses to run until your edit is out of the way.",
                "open": "cd /tmp/tw-lazygit\nperl -pi -e 'print \"buy pins\\n\" if $. == 1' notes.txt\n(cd /tmp/tw-lazygit-teammate && git fetch -q origin && git switch -q -c add-tags origin/main && echo 'buy tags' >> notes.txt && git commit -qam 'Add tags' && git push -q origin HEAD:main)\nlazygit",
                "steps": [
                    (None, "`f`", "Fetch. The Status panel shows `↓1`: one commit to download."),
                    (None, "`p`", "Pull. An `Error` popup says the incoming merge would overwrite your local changes to `notes.txt`. Your git may word it differently."),
                    (None, "`Esc`", "Close the popup."),
                    (None, "`2`, `s`", "Go to Files and stash. A box asks for a name."),
                    (None, "`pins`, `Enter`", "Name it and save. `notes.txt` leaves the Files panel."),
                    (None, "`p`", "Pull again. The Status panel shows `✓` and `Add tags` is at the top of the Commits panel."),
                    (None, "`5`, `g`, `Enter`", "Go to the Stash panel, pop the stash and confirm. `notes.txt` is back in the Files panel."),
                ],
                "after": "`git -C /tmp/tw-lazygit log --oneline -1` shows `Add tags`. `git -C /tmp/tw-lazygit stash list` prints nothing. `git -C /tmp/tw-lazygit status --short` shows ` M notes.txt`, and the file starts with `buy pins` and ends with `buy tags`.",
                "meaning": "Pull refuses when incoming changes would overwrite your local edits; stash those edits first. Stash keeps your edit safe, pull brings the new commit, pop puts your edit back on top of it.",
            },
            "practice": {
                "h2": "Check your answers: stash, undo, sync and conflicts",
                "qs": [
                    ("Mechanism", "Why does `p` fail when I have unsaved changes?",
                     "Pull has to update your files.",
                     ["A pull rewrites files in your folder.", "Git refuses when your own edits are in the way.", "A stash puts the edits aside for a moment."],
                     "Stash first, pull, then pop the stash."),
                    ("Keystrokes", "Which keys undo my last commit and keep the changes?",
                     "One key, then a confirm.",
                     ["Press `z` to undo the local commit action.", "A popup asks to soft reset. Press `Enter`.", "The commit disappears and the file is staged again."],
                     "`z`, then `Enter`. `Z` brings the commit back."),
                    ("Application", "How do I keep the other branch's line in a conflict?",
                     "Open the file and pick a hunk.",
                     ["Select the file in the Files panel and press `Enter`.", "Press `Up` or `Down` to reach the other branch's hunk.", "Press `Space` to keep it, or `b` to keep both."],
                     "`Enter`, `Down`, `Space`, then `Enter` to continue the merge."),
                    ("Common mistake", "Why did `f` change my commits instead of fetching?",
                     "The same key means different things in different panels.",
                     ["In the Files panel, `f` fetches.", "In the Commits panel, `f` is fixup.", "Press `2` before you fetch."],
                     "Go to the Files panel with `2`, then press `f`."),
                ],
            },
        },
    ],
}
