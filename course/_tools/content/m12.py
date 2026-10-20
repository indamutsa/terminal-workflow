"""Module 12: Git in the terminal. Source: commands run in throwaway repos under /tmp/tw-git (git 2.55, macOS); no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


MODULE = {
    "n": 12,
    "folder": "m12-git",
    "title": "Save, undo, branch and sync with git in the terminal",
    "footer": "Git in the terminal: commit, undo a commit, branch, merge, fix a conflict, push and pull; see each result.",
    "tagline": "Save your work, undo a mistake, use branches and sync with GitHub, one command at a time.",
    "glossary": [
        ("tw-commit", "Commit", ["commit", "commits"], "A saved snapshot of your project with a message. Each commit has a short hash such as 3f2a9c1."),
        ("tw-staging", "Staging area", ["staging area", "staged", "stage"], "The list of changes your next commit will save. git add puts a change on it."),
        ("tw-branch", "Branch", ["branch", "branches"], "A line of commits with a name. The default one here is main."),
        ("tw-remote", "Remote", ["remote", "remotes"], "Another copy of the repository, such as the one on GitHub. Here it is called origin."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Save my work with git: stage, commit and see what changed",
            "subtitle": "Save my work, see what changed before I commit, commit only part of a file, look at my history",
            "idea": (
                "Save a snapshot of your project: look at what changed, choose the changes, commit them with a message.",
                [
                    ("See what changed", "git status", "Add -s for one short line per file."),
                    ("Choose what to save", "git add file", "Add -p to pick single changes inside a file."),
                    ("Save a snapshot", "git commit -m \"message\"", "Every commit gets a short hash."),
                    ("Look at my history", "git log --oneline", "Add --graph to see branches."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I save my work with git? You edit files all day, and you cannot tell which edits are saved, which are only chosen and which are still loose.",
                "fix": "Run `git status` to see it, `git add` to choose, `git commit` to save. Each commit is a snapshot you can come back to.",
            },
            "drills": [
                {
                    "h2": "Start a git repository and make my first commits",
                    "intro": "Build a small practice repo in `/tmp/tw-git/shop`. Every block on the four pages runs there, in order. Git needs a name and email on each commit: this block sets them for this repo only.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a git repository with three commits to practice on", "code": C(r'''
mkdir -p /tmp/tw-git/shop && cd /tmp/tw-git/shop
git init -b main
git config user.name "Sam Park"
git config user.email "sam@example.com"
printf 'A1 pen 2.50\nA2 book 4.00\nA3 tape 1.25\n' > orders.txt
printf '# Shop\n\nOrders for the pen shop.\n' > README.md
git add orders.txt README.md
git commit -m "Add orders and readme"
echo 'A4 ink 6.00' >> orders.txt
git commit -am "Add order A4"
echo 'ship same day before noon' > notes.txt
git add notes.txt
git commit -m "Add shipping notes"
git log --oneline
'''),
                         "expect": "`git init` prints `Initialized empty Git repository in /tmp/tw-git/shop/.git/` (macOS shows `/private/tmp/tw-git/shop/.git/`). Each commit prints a line like `[main 1fbfbcc] Add order A4`, and the first one also says `(root-commit)`. The last command lists three commits, newest first: `Add shipping notes`, `Add order A4`, `Add orders and readme`, each after a 7-character hash. Your hashes differ."},
                        {"type": "text", "body": "To start over, delete the folder with `rm -rf /tmp/tw-git` and run the block again. Git says \"Please tell me who you are\" when no name is set. Set one for every repo with `git config --global user.name \"Your Name\"` and `git config --global user.email \"you@example.com\"`."},
                    ],
                },
                {
                    "h2": "See what I changed before I commit (git status, git diff)",
                    "intro": "Look first, then save. `git status` lists the files. `git diff` shows the lines.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "See which files I changed (git status)", "code": C('''
echo 'A5 glue 3.00' >> orders.txt
echo 'draft' > todo.txt
git status
git status -s
'''),
                         "expect": "`git status` prints `On branch main`, then `Changes not staged for commit:` with `modified:   orders.txt`, then `Untracked files:` with `todo.txt`. `git status -s` shrinks that to two lines: ` M orders.txt` and `?? todo.txt`. The space before the `M` means edited but not staged."},
                        {"type": "cmd", "where": "shell", "title": "See what I changed (git diff)", "code": C('''
git diff
'''),
                         "expect": "A header (`diff --git a/orders.txt b/orders.txt`), then the changed place with a few lines around it. `+A5 glue 3.00` is the new line; a removed line would start with `-`. `todo.txt` is missing because git does not track it yet."},
                        {"type": "cmd", "where": "shell", "title": "See what my next commit will save (git diff --staged)", "code": C('''
git add orders.txt
git diff
git diff --staged
'''),
                         "expect": "`git diff` prints nothing, because the edit is staged now. `git diff --staged` prints the same `+A5 glue 3.00` change."},
                        {"type": "cmd", "where": "shell", "title": "Discard changes in a file (git restore)", "code": C('''
echo 'oops' >> notes.txt
git diff --stat
git restore notes.txt
git status -s
'''),
                         "expect": "`git diff --stat` prints ` notes.txt | 1 +`. After `git restore notes.txt`, `git status -s` lists `M  orders.txt` (staged, so the `M` comes first) and `?? todo.txt`. `notes.txt` is gone from the list."},
                        {"type": "text", "body": "`git restore file` cannot be undone: the edit was never committed, so git has no copy of it."},
                    ],
                },
                {
                    "h2": "Commit my changes with a message (git commit)",
                    "intro": "Commit what is staged. Write the message as what the commit does: \"Add order A5\", not \"changes\".",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Save my staged changes as a commit (git commit -m)", "code": C('''
git commit -m "Add order A5"
git status -s
'''),
                         "expect": "A line like `[main f12d620] Add order A5`, then `1 file changed, 1 insertion(+)`. `git status -s` now lists only `?? todo.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Stop git showing a file I never want to commit (.gitignore)", "code": C(r'''
printf 'todo.txt\n*.log\n' > .gitignore
echo 'x' > debug.log
git status -s
git add .gitignore
git commit -m "Ignore todo and log files"
'''),
                         "expect": "`git status -s` shows `?? .gitignore` and no `todo.txt` or `debug.log`: git hides both. The commit prints `create mode 100644 .gitignore`."},
                        {"type": "text", "body": "To save every edit to files git already tracks in one step, use `git commit -am \"message\"`. It skips new files, so run `git add` for those first."},
                        {"type": "cmd", "where": "shell", "title": "Commit only part of a file (git add -p)", "code": C(r'''
printf 'pen 2.50\nbook 4.00\nglue 3.00\nink 6.00\ntape 1.25\nruler 1.00\nstamp 0.60\nclip 0.10\nfolder 0.90\nstaple 0.30\n' > prices.txt
git add prices.txt
git commit -m "Add prices"
sed 's/^pen 2.50/pen 2.75/; s/^staple 0.30/staple 0.35/' prices.txt > prices.new && mv prices.new prices.txt
git add -p
git commit -m "Raise pen price"
git diff
'''),
                         "expect": "The first commit adds the ten price lines. `git add -p` then shows two changes and asks `Stage this hunk [y,n,q,a,d,...]?` for each: `(1/2)` is the `pen 2.50` to `pen 2.75` change and `(2/2)` is the `staple` change. Type `y` for the first and `n` for the second. The commit prints `1 file changed, 1 insertion(+), 1 deletion(-)`, and the last `git diff` still shows the left-over change: `-staple 0.30` and `+staple 0.35`."},
                        {"type": "text", "body": "`git add -p` shows one change at a time and asks what to do. Press `y` to stage it, `n` to skip it, `s` to split a big change, `q` to stop. Git asks about each change in turn, so the second change here gets its answer too."},
                    ],
                },
                {
                    "h2": "Look at my history (git log, git show)",
                    "intro": "Read the commits you made. Git opens long output in a pager: press `q` to leave it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "See my commit history, one line per commit (git log --oneline)", "code": C('''
git log --oneline
git log --oneline -3
'''),
                         "expect": "Seven lines, newest first, from `Raise pen price` down to `Add orders and readme`, each after a 7-character hash. The second command prints only the top three."},
                        {"type": "cmd", "where": "shell", "title": "Show what a commit changed (git show)", "code": C('''
git show --stat
git show HEAD~1 --oneline
'''),
                         "expect": "`git show --stat` prints `commit` and the full hash, `Author: Sam Park <sam@example.com>`, a date, the message `Raise pen price`, and `prices.txt | 2 +-`. The second command prints one line for the earlier commit, like `b992ef6 Add prices`, then the whole file as lines starting with `+`."},
                        {"type": "cmd", "where": "shell", "title": "Find the commits that changed one file", "code": C('''
git log --oneline -- orders.txt
'''),
                         "expect": "Three lines: `Add order A5`, `Add order A4` and `Add orders and readme`. The other commits did not touch `orders.txt`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which git command shows what, and where my changes live",
                "cards": [
                    ("See changes, staged changes and history", "Pick the command by what you want to see.", ["Command", "Shows"], [
                        ["`git status`", "Which files changed, and which are staged"],
                        ["`git diff`", "Edits you have not staged yet"],
                        ["`git diff --staged`", "What your next commit will save"],
                        ["`git log --oneline`", "One line per commit, newest first"],
                        ["`git show`", "The latest commit with its changes"],
                    ]),
                    ("Move a change from edited to staged to committed", "A change goes through three places.", ["Place", "How it gets there"], [
                        ["Edited", "Change a file in your editor"],
                        ["Staged", "`git add file`"],
                        ["Committed", "`git commit -m \"message\"`"],
                        ["Back to the staged version", "`git restore file`"],
                    ]),
                    ("Skip files git should never save", "List the names in a `.gitignore` file, one per line.", ["Line", "Skips"], [
                        ["`todo.txt`", "That one file"],
                        ["`*.log`", "Every file ending in .log"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Save one edit with a clear message",
                "frame": "Add a new order to `orders.txt` and save it as its own commit.",
                "open": "cd /tmp/tw-git/shop",
                "steps": [
                    (None, "`echo 'A5 glue 3.00' >> orders.txt`", "Edit the file."),
                    (None, "`git status -s`", "Check what changed."),
                    (None, "`git add orders.txt`", "Choose the file."),
                    (None, "`git commit -m \"Add order A5\"`", "Save it."),
                ],
                "after": " M orders.txt\n[main f12d620] Add order A5\n 1 file changed, 1 insertion(+)",
                "meaning": "Status, add, commit: three looks and one save. The hash differs on your machine.",
            },
            "practice": {
                "h2": "Check your answers: status, diff, add and commit",
                "qs": [
                    ("Mechanism", "Why does `git diff` print nothing after I run `git add orders.txt`?",
                     "Which two places does git compare?",
                     ["`git diff` compares your files with the staging area.", "After `git add`, the staging area holds the same text."],
                     "`git diff --staged` shows what the next commit will save."),
                    ("Keystrokes", "How do I save my staged changes with the message \"Add order A5\"?",
                     "One command, one flag.",
                     ["Type `git commit`.", "Add `-m` and the message in quotes."],
                     "`git commit -m \"Add order A5\"`."),
                    ("Application", "How do I commit the price change on line 1 of `prices.txt` and leave the one on line 10 for later?",
                     "Pick changes one by one.",
                     ["Run `git add -p prices.txt`.", "Press `y` for the first change and `n` for the second.", "Run `git commit -m \"Raise pen price\"`."],
                     "`git add -p`, then `y`, `n`, then `git commit`."),
                    ("Common mistake", "Why is `todo.txt` still in my `git status` after I added it to `.gitignore`?",
                     "Is the file tracked already?",
                     ["`.gitignore` only hides files git does not track yet.", "If the file was committed before, git keeps tracking it."],
                     "Stop tracking it with `git rm --cached todo.txt`, then commit."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Undo a mistake in git: unstage, amend, undo a commit, get it back",
            "subtitle": "Unstage a file, fix my last commit message, undo my last commit, get back a lost commit, put changes aside with stash",
            "idea": (
                "Pick the undo by what went wrong. Soft and mixed reset keep your edits. Plain restore and hard reset overwrite them.",
                [
                    ("Unstage a file", "git restore --staged file", "The edit stays in the file."),
                    ("Fix my last commit", "git commit --amend", "Add -m to change the message."),
                    ("Undo my last commit", "git reset --soft HEAD~1", "The changes stay staged."),
                    ("Get a lost commit back", "git reflog", "Find its hash, then make a branch there."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I undo a git mistake? You staged the wrong file, typed a message wrong or committed too early. Each mistake has its own fix, and the wrong one loses work.",
                "fix": "Match the mistake to the command in the rules below. `git restore --staged`, soft reset and mixed reset keep your working files. Plain restore overwrites unstaged edits. Reflog entries expire after 90 days by default, or 30 days for unreachable entries. Your config can shorten these times.",
            },
            "drills": [
                {
                    "h2": "Unstage a file or get an old version back (git restore)",
                    "intro": "`git restore` has two jobs: take a file off the staging area, or bring back an older copy of it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Commit every edit to files git already tracks (git commit -am)", "code": C('''
git commit -am "Raise staple price"
git status -s
'''),
                         "expect": "`[main b002589] Raise staple price` and `1 file changed, 1 insertion(+), 1 deletion(-)`. `git status -s` prints nothing: the folder is clean again."},
                        {"type": "cmd", "where": "shell", "title": "Unstage a file but keep my edits (git restore --staged)", "code": C('''
echo 'call the carrier' >> notes.txt
git add notes.txt
git status -s
git restore --staged notes.txt
git status -s
git restore notes.txt
'''),
                         "expect": "The first `git status -s` shows `M  notes.txt` (staged). After `git restore --staged notes.txt` it shows ` M notes.txt`: still edited, no longer staged. The last command throws the edit away."},
                        {"type": "cmd", "where": "shell", "title": "Get an old version of a file back (git restore --source)", "code": C('''
git show HEAD~5:orders.txt
git restore --source=HEAD~5 orders.txt
git diff --stat
git restore orders.txt
git status -s
'''),
                         "expect": "`git show HEAD~5:orders.txt` prints the file as it was five commits ago: `A1` to `A4` and no `A5`. `git restore --source=HEAD~5 orders.txt` writes that copy into your folder, and `git diff --stat` shows ` orders.txt | 1 -`. The last `git restore orders.txt` puts the current version back, and `git status -s` prints nothing."},
                    ],
                },
                {
                    "h2": "Fix my last commit: message or forgotten change (git commit --amend)",
                    "intro": "Amend replaces the last commit with a new one. Use it before you push, never after: a pushed commit is shared.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Fix a typo in my last commit message (git commit --amend)", "code": C('''
echo 'A6 stamps 0.60' >> orders.txt
git commit -am "Add oder A6"
git commit --amend -m "Add order A6"
git log --oneline -2
'''),
                         "expect": "The first commit is `Add oder A6`. The amend prints `[main b3467eb] Add order A6` with a new hash. `git log --oneline -2` shows `Add order A6` on top of `Raise staple price`: the typo commit is gone."},
                        {"type": "cmd", "where": "shell", "title": "Add a forgotten change to my last commit", "code": C('''
echo 'A7 clips 0.10' >> orders.txt
git commit -a --amend --no-edit
git show --stat --oneline
'''),
                         "expect": "The amend prints the same message with a new hash and `1 file changed, 2 insertions(+)`: both orders are in one commit. `git show --stat --oneline` prints the hash and `Add order A6`, then ` orders.txt | 2 ++`."},
                        {"type": "cmd", "where": "shell", "title": "Add a forgotten file to my last commit", "code": C('''
echo 'Pack orders before noon.' > packing.txt
git add packing.txt
git commit --amend --no-edit
git show --stat --oneline
git restore --source=HEAD~1 --staged --worktree packing.txt
git commit --amend --no-edit
'''),
                         "expect": "`git add packing.txt` stages the new file. The amend prints `[main <hash>] Add order A6`, `2 files changed, 3 insertions(+)` and `create mode 100644 packing.txt`. `git show --stat --oneline` shows a 7-character hash and the same message, then `orders.txt | 2 ++` and `packing.txt | 1 +` (spacing may differ). Your hash differs. The last two commands remove only the practice file from the commit so the next drill starts with just the two orders again: the final amend prints `1 file changed, 2 insertions(+)`."},
                    ],
                },
                {
                    "h2": "Undo my last commit and keep my changes (git reset)",
                    "intro": "`git reset HEAD~1` moves the branch back one commit. The flag decides what happens to your changes. Each block here makes the commit again, so you can repeat them.",
                    "blocks": [
                        {"type": "keys", "where": "shell", "title": "Undo my last commit, keep or delete the changes", "rows": [
                            ("git reset --soft HEAD~1", "Undo my last commit and keep the changes staged"),
                            ("git reset HEAD~1", "Undo my last commit and keep the changes unstaged"),
                            ("git reset --hard HEAD~1", "Undo my last commit and delete its changes"),
                            ("git revert HEAD", "Undo a commit by adding a new commit that reverses it"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Undo my last commit but keep the changes staged (git reset --soft)", "code": C('''
git reset --soft HEAD~1
git status -s
git commit -m "Add orders A6 and A7"
'''),
                         "expect": "`git status -s` prints `M  orders.txt`: the changes are staged. The new commit prints `[main 46a127d] Add orders A6 and A7` and `1 file changed, 2 insertions(+)`."},
                        {"type": "cmd", "where": "shell", "title": "Undo my last commit and unstage the changes (git reset)", "code": C('''
git reset HEAD~1
git status -s
git commit -am "Add orders A6 and A7"
'''),
                         "expect": "`git reset HEAD~1` prints `Unstaged changes after reset:` and then `M` and `orders.txt` on one line. `git status -s` prints ` M orders.txt`: edited, not staged. `-am` stages and commits it again."},
                        {"type": "cmd", "where": "shell", "title": "Throw away my last commit and its changes (git reset --hard)", "code": C('''
# Warning: this overwrites staged and unstaged tracked edits and may overwrite untracked files in the way; reflog cannot recover edits git never saved.
git reset --hard HEAD~1
git log --oneline -1
tail -2 orders.txt
'''),
                         "expect": "`HEAD is now at b002589 Raise staple price`. `git log --oneline -1` agrees. `tail -2 orders.txt` ends at `A5 glue 3.00`: the A6 and A7 lines are gone."},
                    ],
                },
                {
                    "h2": "Get back a lost commit or undo a shared one (git reflog, git revert)",
                    "intro": "A commit you reset away is not gone. `git reflog` lists every place HEAD has been. A commit that others already have needs `git revert`, which adds a new commit instead of rewriting history.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Get back a commit I reset by mistake (git reflog)", "code": C('''
# Warning: this overwrites staged and unstaged tracked edits and may overwrite untracked files in the way; reflog cannot recover edits git never saved.
git reflog -4
git reset --hard 'HEAD@{1}'
git log --oneline -1
'''),
                         "expect": "`git reflog -4` lists newest first. Each line starts with a hash and a reflog index: `HEAD@{0}`, `HEAD@{1}`, `HEAD@{2}`, `HEAD@{3}`. The top line reads `reset: moving to HEAD~1` and the one below it `commit: Add orders A6 and A7`. Resetting to `HEAD@{1}` prints `HEAD is now at` and that commit, and `git log --oneline -1` shows `Add orders A6 and A7` again."},
                        {"type": "cmd", "where": "shell", "title": "Revert a commit I already pushed (git revert)", "code": C('''
git revert --no-edit HEAD
git log --oneline -3
'''),
                         "expect": "A new commit named `Revert \"Add orders A6 and A7\"` with `1 file changed, 2 deletions(-)`. `git log --oneline -3` shows it on top, with the original commit still below it."},
                    ],
                },
                {
                    "h2": "Save my changes for later without committing (git stash)",
                    "intro": "Stash clears your edits so you can switch tasks. Bring them back when you are ready.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Put my changes aside and bring them back (git stash)", "code": C('''
echo 'A8 rubber 0.40' >> orders.txt
git stash push -m "half-done A8"
git status -s
git stash list
git stash pop
git commit -am "Add order A8"
'''),
                         "expect": "`Saved working directory and index state On main: half-done A8`. `git status -s` prints nothing and `git stash list` prints `stash@{0}: On main: half-done A8`. `git stash pop` prints the status with `modified:   orders.txt` and `Dropped refs/stash@{0}` plus a hash. The commit prints `[main bc95f96] Add order A8`."},
                        {"type": "text", "body": "A plain `git stash` skips new files that git does not track yet. Add `-u` to stash them too: `git stash push -u -m \"message\"`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which command undoes which git mistake",
                "cards": [
                    ("Match the mistake to the undo", "Start with the smallest fix.", ["What went wrong", "Command"], [
                        ["I edited a file and want the old text", "`git restore file`"],
                        ["I staged the wrong file", "`git restore --staged file`"],
                        ["My last commit message has a typo", "`git commit --amend -m \"new message\"`"],
                        ["I committed too early", "`git reset --soft HEAD~1`"],
                        ["I need to undo a commit others have", "`git revert HEAD`"],
                        ["I lost a commit", "`git reflog`, then `git branch recovered <hash>`"],
                    ]),
                    ("What each git reset keeps", "All three move the branch back. They differ in what they do to your work.", ["Command", "Staged changes", "Files"], [
                        ["`git reset --soft HEAD~1`", "Kept", "Kept"],
                        ["`git reset HEAD~1`", "Unstaged", "Kept"],
                        ["`git reset --hard HEAD~1`", "Deleted", "Deleted"],
                    ]),
                    ("Rewrite a commit or add a new one", "Rewriting is fine alone and wrong once others have the commit.", ["Command", "Use it when"], [
                        ["`git commit --amend`", "The commit is only on your machine"],
                        ["`git reset`", "The commit is only on your machine"],
                        ["`git revert`", "The commit is pushed or shared"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Undo a commit I made too early",
                "frame": "You committed `orders.txt` before adding one more order. Take the commit back and keep the edits.",
                "open": "cd /tmp/tw-git/shop",
                "steps": [
                    (None, "`git reset --soft HEAD~1`", "Undo the commit. The changes stay staged."),
                    (None, "`git status -s`", "Check: the file shows as staged."),
                    (None, "`git commit -m \"Add orders A6 and A7\"`", "Commit again when you are ready."),
                ],
                "after": "M  orders.txt\n[main 46a127d] Add orders A6 and A7\n 1 file changed, 2 insertions(+)",
                "meaning": "The commit disappears and the edits stay. Nothing is lost, so this is safe to try.",
            },
            "practice": {
                "h2": "Check your answers: restore, amend, reset, revert and stash",
                "qs": [
                    ("Mechanism", "Why can I get a commit back after `git reset --hard`?",
                     "Where does git write down where HEAD has been?",
                     ["`git reset --hard` moves the branch, but the commit object stays in the repository.", "`git reflog` keeps a list of every place HEAD pointed to."],
                     "Run `git reflog`, find the hash, then `git reset --hard <hash>`."),
                    ("Keystrokes", "How do I fix the message of my last commit to \"Add order A6\"?",
                     "Replace the commit, with a new message.",
                     ["Type `git commit --amend`.", "Add `-m \"Add order A6\"`."],
                     "`git commit --amend -m \"Add order A6\"`."),
                    ("Application", "How do I undo a commit I already pushed, without rewriting history?",
                     "Add a commit that does the opposite.",
                     ["Run `git revert --no-edit HEAD`.", "Push the new commit as usual."],
                     "`git revert --no-edit HEAD` adds a commit that reverses the last one."),
                    ("Common mistake", "Why did `git stash` leave my new file `scratch.txt` in the folder?",
                     "Does a plain stash take files git does not track?",
                     ["A plain `git stash` only saves tracked files.", "Add `-u` to include untracked files."],
                     "Use `git stash push -u`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Create, switch and merge a git branch and fix a merge conflict",
            "subtitle": "Create a branch, switch branches, merge a branch into main, fix a merge conflict, rebase, cherry-pick, delete a branch",
            "idea": (
                "Work on a copy of the history, then bring it back. Branches are cheap: make one for every task.",
                [
                    ("Create a branch and switch to it", "git switch -c name", "Switch back with git switch main."),
                    ("Merge a branch into main", "git merge name", "Run it while main is checked out."),
                    ("Fix a merge conflict", "git add file", "Edit the file first, then add it and commit."),
                    ("Copy one commit to another branch", "git cherry-pick name", "Use a commit hash for any commit."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I try something without breaking main? You edit on main, and a half-done change gets mixed with the fixes you need to ship.",
                "fix": "Make a branch for the change, commit there, and merge it when it works. If two branches change the same line, git asks you to choose.",
            },
            "drills": [
                {
                    "h2": "Create a branch and switch between branches (git switch)",
                    "intro": "A branch is a name for a line of commits. Switching changes the files in your folder to match.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create a branch and switch to it (git switch -c)", "code": C('''
git switch -c add-labels
git branch
echo 'label: fragile' > labels.txt
git add labels.txt
git commit -m "Add labels file"
'''),
                         "expect": "`Switched to a new branch 'add-labels'`. `git branch` lists `* add-labels` and `  main`: the `*` marks the branch you are on. The commit prints `[add-labels 7e2f789] Add labels file` (your hash differs) and `create mode 100644 labels.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Switch back to main and see the files change (git switch)", "code": C('''
git switch main
command ls
git switch add-labels
command ls
git switch main
'''),
                         "expect": "On `main`, `command ls` lists `debug.log`, `notes.txt`, `orders.txt`, `prices.txt`, `README.md` and `todo.txt`. On `add-labels` the list also has `labels.txt`. Switching changes the files in the folder to match the branch."},
                        {"type": "cmd", "where": "shell", "title": "Go back to the previous branch (git switch -)", "code": C('''
git switch -
git branch --show-current
git switch -
'''),
                         "expect": "The first `git switch -` prints `Switched to branch 'add-labels'`: that was the branch you were on before `main`. `git branch --show-current` prints `add-labels`. Running `git switch -` again prints `Switched to branch 'main'`, ready for the merge drill."},
                    ],
                },
                {
                    "h2": "Merge a branch into main (git merge)",
                    "intro": "Check out the branch that should receive the work, then name the branch to bring in. Git may open an editor with a merge message: save and close it, or add `--no-edit` to skip it.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Merge a branch into main (git merge)", "code": C('''
echo 'Open 9 to 5.' >> README.md
git commit -am "Add opening hours"
git merge --no-edit add-labels
git log --oneline --graph -5
'''),
                         "expect": "The commit prints `[main 5a02ace] Add opening hours`. The merge prints `Merge made by the 'ort' strategy.` and ` labels.txt | 1 +`. The graph shows a merge commit on top, `Merge branch 'add-labels'`, with two lines under it: `Add opening hours` on the left (main) and the branch commit `Add labels file` on the right, which join again below."},
                        {"type": "cmd", "where": "shell", "title": "Delete a branch I already merged (git branch -d)", "code": C('''
git branch -d add-labels
git branch
'''),
                         "expect": "`Deleted branch add-labels (was 7e2f789).` and `git branch` lists only `* main`. Git deletes a merged branch without asking, because its commits are on main."},
                    ],
                },
                {
                    "h2": "Fix a merge conflict",
                    "intro": "A conflict happens when two branches change the same line. Git stops, marks both versions in the file and waits for you.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make two branches change the same line", "code": C('''
git switch -c fix-price
sed 's/^A1 pen 2.50/A1 pen 2.75/' orders.txt > orders.new && mv orders.new orders.txt
git commit -am "Raise pen price to 2.75"
git switch main
sed 's/^A1 pen 2.50/A1 pen 3.00/' orders.txt > orders.new && mv orders.new orders.txt
git commit -am "Raise pen price to 3.00"
git merge --no-edit fix-price
git status -s
'''),
                         "expect": "The merge prints `CONFLICT (content): Merge conflict in orders.txt` and `Automatic merge failed; fix conflicts and then commit the result.` Then `git status -s` prints `UU orders.txt`: both branches changed it."},
                        {"type": "cmd", "where": "shell", "title": "See the conflict markers git wrote in the file", "code": C('''
head -6 orders.txt
'''),
                         "expect": "Git put both versions in the file. Your branch comes first, after `<<<<<<< HEAD`: `A1 pen 3.00`. A line of `=======` separates it from the other branch, `A1 pen 2.75`, which ends at `>>>>>>> fix-price`. Everything below is unchanged: `A2 book 4.00`."},
                        {"type": "cmd", "where": "shell", "title": "Fix a merge conflict and finish the merge", "code": C('''
sed -e '/^<<<<<<< /d' -e '/^=======$/d' -e '/^>>>>>>> /d' -e '/^A1 pen 2.75$/d' orders.txt > orders.new && mv orders.new orders.txt
head -2 orders.txt
git add orders.txt
git commit --no-edit
git log --oneline --graph -4
'''),
                         "expect": "`head -2 orders.txt` shows `A1 pen 3.00` and `A2 book 4.00`: no markers left. The commit prints `[main 7faf737] Merge branch 'fix-price'`. The graph shows `Merge branch 'fix-price'` on top and the two price commits side by side below it."},
                        {"type": "text", "body": "In a real conflict, open the file in Neovim, delete the marker lines and the version you do not want, then save. The `sed` line does the same job here, so the block gives the same result every time. To back out of a merge, run `git merge --abort`."},
                    ],
                },
                {
                    "h2": "Put my branch's commits on top of the latest main (git rebase)",
                    "intro": "Rebase replays your commits after the newest commit of another branch. The history becomes one straight line instead of a fork and a merge. Rebase only commits that are not pushed yet.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make a branch that main has moved past", "code": C('''
git switch -c add-stamps
echo 'stamps: 100' > stamps.txt
git add stamps.txt
git commit -m "Add stamps file"
git switch main
echo 'Closed Sundays.' >> README.md
git commit -am "Add closed days"
git switch add-stamps
git log --oneline --graph --all -4
'''),
                         "expect": "The branch commit prints `[add-stamps 8038d66] Add stamps file` and the main commit prints `[main 100e07d] Add closed days`. The graph shows a fork: `Add stamps file` on one line and `Add closed days` on another, both leaving the same older commit."},
                        {"type": "cmd", "where": "shell", "title": "Rebase my branch onto main (git rebase)", "code": C('''
git rebase main
git log --oneline --graph --all -4
git switch main
git merge add-stamps
git branch -d add-stamps fix-price
'''),
                         "expect": "`Rebasing (1/1)` then `Successfully rebased and updated refs/heads/add-stamps.` The graph is a straight line now: `Add stamps file` (a new hash) sits on top of `Add closed days`. On main, `git merge add-stamps` prints `Fast-forward` and ` stamps.txt | 1 +`. Both finished branches are deleted: `Deleted branch add-stamps (was ac87ba5).` and `Deleted branch fix-price (was 5991ddd).`"},
                    ],
                },
                {
                    "h2": "Copy one commit to another branch, or get a deleted branch back",
                    "intro": "`git cherry-pick` copies a single commit. A deleted branch is only a lost name: its commits are still in the reflog.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Copy one commit from another branch onto main (git cherry-pick)", "code": C('''
git switch -c hotfix
echo 'Support: 555-0100' >> notes.txt
git commit -am "Add support phone"
git switch main
echo 'A9 staples 0.80' >> orders.txt
git commit -am "Add order A9"
git cherry-pick hotfix
git log --oneline -3
'''),
                         "expect": "The cherry-pick prints `[main 2d12386] Add support phone` plus a `Date:` line: the same message, a new hash. `git log --oneline -3` shows `Add support phone`, `Add order A9` and `Add stamps file`."},
                        {"type": "cmd", "where": "shell", "title": "Delete a branch git says is not merged (git branch -D)", "code": C('''
git branch -d hotfix
git branch -D hotfix
'''),
                         "expect": "The first command prints `error: the branch 'hotfix' is not fully merged` and a hint to use `git branch -D hotfix`. Git sees the cherry-picked copy as a different commit. The second command prints `Deleted branch hotfix (was ef044d1).`"},
                        {"type": "cmd", "where": "shell", "title": "Get back a branch I deleted (git reflog)", "code": C('''
git reflog | grep "commit: Add support phone"
git branch hotfix $(git reflog | grep "commit: Add support phone" | cut -d' ' -f1)
git branch
'''),
                         "expect": "The first line shows one reflog entry, like `ef044d1 HEAD@{3}: commit: Add support phone` (your hash and number differ). The second command makes a branch at that hash. `git branch` lists `hotfix` again beside `* main`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which branch command to use, and how to fix a conflict",
                "cards": [
                    ("List, create, switch and delete branches", "Names go after the command.", ["Command", "Does"], [
                        ["`git branch`", "List branches; the current one has a `*`"],
                        ["`git switch name`", "Go to a branch"],
                        ["`git switch -c name`", "Create a branch and go to it"],
                        ["`git branch -d name`", "Delete a branch that is merged"],
                        ["`git branch -D name`", "Delete a branch even if it is not merged"],
                    ]),
                    ("Bring work together: merge, rebase or cherry-pick", "All three move commits. The history looks different afterwards.", ["Command", "History afterwards"], [
                        ["`git merge name`", "Fast-forwards when possible; otherwise joins diverged histories with a merge commit"],
                        ["`git rebase main`", "One straight line; your commits get new hashes"],
                        ["`git cherry-pick hash`", "One commit copied, with a new hash"],
                    ]),
                    ("Fix a merge conflict in four steps", "Git marks the file with `<<<<<<<`, `=======` and `>>>>>>>`.", ["Step", "Do"], [
                        ["1", "`git status -s` and find the files marked `UU`"],
                        ["2", "Edit each file: keep what you want, delete the marker lines"],
                        ["3", "`git add file`"],
                        ["4", "`git commit --no-edit`, or `git merge --abort` to give up"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Merge two branches that changed the same line",
                "frame": "Two branches set a different price for `A1 pen`. Finish the merge and keep the price from main.",
                "open": "cd /tmp/tw-git/shop",
                "steps": [
                    (None, "`git status -s`", "Find the file marked `UU`."),
                    (None, "Edit `orders.txt`", "Delete the marker lines and the line you do not want."),
                    (None, "`git add orders.txt`", "Tell git the conflict is solved."),
                    (None, "`git commit --no-edit`", "Finish the merge with git's own message."),
                ],
                "after": "UU orders.txt\n[main 7faf737] Merge branch 'fix-price'",
                "meaning": "A conflict is git asking a question. Answer it in the file, then add and commit.",
            },
            "practice": {
                "h2": "Check your answers: branches, merge, rebase and conflicts",
                "qs": [
                    ("Mechanism", "Why does the file `labels.txt` disappear when I run `git switch main`?",
                     "Where was the file committed?",
                     ["`labels.txt` was committed on `add-labels` only.", "Switching makes your folder match the branch you switch to."],
                     "Main has no `labels.txt` yet. It comes back on `add-labels`, or after a merge."),
                    ("Keystrokes", "How do I create a branch named `fix-price` and switch to it in one command?",
                     "A flag on `git switch` makes a new branch.",
                     ["Type `git switch`.", "Add `-c` and the name."],
                     "`git switch -c fix-price`."),
                    ("Application", "How do I get a branch back after `git branch -D`?",
                     "The commits are still in the reflog.",
                     ["Run `git reflog` and find the last commit of the branch.", "Run `git branch name hash` with that hash."],
                     "`git branch hotfix <hash>`."),
                    ("Common mistake", "Why does `git branch -d hotfix` refuse to delete a branch I cherry-picked?",
                     "Does git see the copy as the same commit?",
                     ["A cherry-pick makes a copy with a new hash.", "Git sees the original as not merged."],
                     "Check the work is on main, then use `git branch -D hotfix`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Push to GitHub, pull changes and fix a rejected git push",
            "subtitle": "Push my project to GitHub, clone a repository, pull the latest changes, fix a rejected push, tag a release, find who changed a line",
            "idea": (
                "Your history lives on your machine, and a copy lives on a remote. Send yours with push. Get theirs with fetch or pull.",
                [
                    ("Download a repository", "git clone url", "It makes a folder and sets origin."),
                    ("Get the latest changes", "git pull --rebase", "git fetch only looks and leaves your files alone."),
                    ("Upload my commits", "git push", "Use git push -u origin main the first time."),
                    ("Find who changed a line", "git blame file", "Add -L 1,5 for lines 1 to 5."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I share my commits and get my teammates' commits? Your repo is only on your machine until you push it, and a push fails when someone pushed first.",
                "fix": "Push to `origin`, fetch to look, and `git pull --rebase` to put their commits under yours. Here `origin` is a folder on your disk; GitHub works the same way.",
            },
            "drills": [
                {
                    "h2": "Push my project to GitHub (git remote add, git push -u)",
                    "intro": "A remote is another copy of the repo. This block makes a bare repo in `/tmp/tw-git/remote.git` that plays the part of GitHub, so nothing leaves your machine.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Add a remote and push my branch for the first time (git push -u)", "code": C('''
git init --bare -b main /tmp/tw-git/remote.git
git remote add origin /tmp/tw-git/remote.git
git remote -v
git push -u origin main
'''),
                         "expect": "`git init --bare` prints `Initialized empty Git repository in /tmp/tw-git/remote.git/` (macOS shows `/private/tmp/...`). `git remote -v` lists `origin` twice, `(fetch)` and `(push)`, with the folder path. The push prints `* [new branch]      main -> main` and `branch 'main' set up to track 'origin/main'.`"},
                        {"type": "code", "file": "shell", "title": "Push to a real GitHub repository (fresh repo; skip this exercise)", "code": C('''
git remote add origin git@github.com:YOUR-NAME/shop.git
git push -u origin main
''')},
                        {"type": "text", "body": "This is the alternative for a fresh repo with no `origin`; skip it during this exercise. Create the empty repository on GitHub first, then copy its address from the green Code button. Use that address in place of `YOUR-NAME/shop.git`. If `origin` already exists, use `git remote set-url origin <url>` instead of `git remote add`, with the GitHub address in place of `<url>`. After `-u`, a plain `git push` and `git pull` know where to go."},
                    ],
                },
                {
                    "h2": "Clone a repo from GitHub (git clone)",
                    "intro": "Clone makes a folder with the full history and sets `origin` for you. This block clones the repo for a second person, Alex, who then pushes a commit.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Clone a repo and list all branches including remote ones (git clone, git branch -a)", "code": C('''
git clone /tmp/tw-git/remote.git /tmp/tw-git/friend
cd /tmp/tw-git/friend
git config user.name "Alex Lee"
git config user.email "alex@example.com"
git log --oneline -3
git branch -a
'''),
                         "expect": "`Cloning into '/tmp/tw-git/friend'...` (a real GitHub clone also prints counting and receiving lines). `git log --oneline -3` shows the same last three commits as your repo: `Add support phone`, `Add order A9`, `Add stamps file`. `git branch -a` lists `* main`, `remotes/origin/HEAD -> origin/main` and `remotes/origin/main`."},
                        {"type": "cmd", "where": "shell", "title": "Push a commit to the remote (git push)", "code": C('''
echo 'A10 folders 0.90' >> orders.txt
git commit -am "Add order A10"
git push
'''),
                         "expect": "The commit prints `[main ab0a52e] Add order A10`. The push prints `To /tmp/tw-git/remote.git` and a line like `   2232f7f..ab0a52e  main -> main`: the old and new tip of the remote branch."},
                    ],
                },
                {
                    "h2": "Get the newest changes from GitHub (git fetch, git pull --rebase)",
                    "intro": "Go back to your own repo. Alex pushed a commit that you do not have. If a rebase stops for conflicts, fix the files, run `git add <file>`, then `git rebase --continue`. Repeat until it finishes, then push. Use `git rebase --abort` to cancel.",
                    "blocks": [
                        {"type": "keys", "where": "shell", "title": "Download, update and upload with a remote", "rows": [
                            ("git clone url", "Download a repository from GitHub"),
                            ("git remote -v", "See where origin points"),
                            ("git fetch", "Download new commits without changing my files"),
                            ("git pull --rebase", "Pull without a merge commit: rebase my commits on the downloaded changes"),
                            ("git push", "Upload my commits"),
                            ("git push -u origin branch", "Push a new branch and remember it"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "See if the remote has new commits (git fetch)", "code": C('''
cd /tmp/tw-git/shop
git fetch
git status
git log --oneline main..origin/main
'''),
                         "expect": "`git fetch` prints `From /tmp/tw-git/remote` and a line like `2232f7f..ab0a52e  main       -> origin/main`. `git status` says `Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.` Your files did not change. The last command lists the commit you lack: `Add order A10`."},
                        {"type": "cmd", "where": "shell", "title": "Pull the latest changes and keep my commits on top (git pull --rebase)", "code": C('''
git pull --rebase
git log --oneline -2
'''),
                         "expect": "`Updating 2232f7f..ab0a52e`, `Fast-forward` and ` orders.txt | 1 +`. `git log --oneline -2` now has `Add order A10` on top of `Add support phone`."},
                        {"type": "cmd", "where": "shell", "title": "Fix \"rejected, fetch first\" when I push", "code": C('''
echo 'A11 pins 0.20' >> orders.txt
git commit -am "Add order A11"
cd /tmp/tw-git/friend
echo 'Back on Monday.' >> notes.txt
git commit -am "Add Monday note"
git push
cd /tmp/tw-git/shop
git push
'''),
                         "expect": "Both commits succeed: `[main b8b1de2] Add order A11` here and `[main c354bd0] Add Monday note` in Alex's folder. Alex's push works (`ab0a52e..c354bd0  main -> main`). Yours does not: `! [rejected]        main -> main (fetch first)` and `error: failed to push some refs to '/tmp/tw-git/remote.git'`, followed by hints."},
                        {"type": "cmd", "where": "shell", "title": "Pull, then push again after a rejected push", "code": C('''
git pull --rebase
git push
git log --oneline --graph -4
'''),
                         "expect": "`git pull --rebase` prints `Rebasing (1/1)` and `Successfully rebased and updated refs/heads/main.` The push now works: `c354bd0..6d535dc  main -> main`. The graph is a straight line with your `Add order A11` on top of Alex's `Add Monday note`."},
                    ],
                },
                {
                    "h2": "Tag a release (git tag)",
                    "intro": "A tag is a name for one commit, such as `v1.0`. Tags are not pushed with `git push`: push them by name.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Tag a release and push the tag (git tag)", "code": C('''
git tag -a v1.0 -m "First release"
git tag
git push origin v1.0
git show v1.0 --stat | head -8
'''),
                         "expect": "`git tag` prints `v1.0`. The push prints `* [new tag]         v1.0 -> v1.0`. `git show v1.0 --stat` starts with `tag v1.0`, `Tagger: Sam Park <sam@example.com>`, a date and the message `First release`, then the commit it points to."},
                    ],
                },
                {
                    "h2": "Find who changed a line and when (git blame, git log -S)",
                    "intro": "Blame shows who last changed each line. The search option `-S` finds commits where the number of occurrences of a piece of text changed.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "See who last changed each line of a file (git blame)", "code": C('''
git blame orders.txt
'''),
                         "expect": "One line per line of the file: a short hash (a `^` in front means the first commit), the author in brackets, the date, the line number and the text. Lines 1 to 7 and 9 show `Sam Park`, and line 8, `A10 folders 0.90`, shows `Alex Lee`. Hashes and dates differ on your machine."},
                        {"type": "cmd", "where": "shell", "title": "Find commits that added or removed text (git log -S)", "code": C('''
git log -S"A9" --oneline
git log -S"A9" --format="%h %an %s"
'''),
                         "expect": "The first command prints one line, `Add order A9`, with its hash: the only commit that added that text. The second adds the author: `Sam Park`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which command syncs with a remote, and how to fix a rejected push",
                "cards": [
                    ("Download, update and upload", "Each command touches a different place.", ["Command", "Changes"], [
                        ["`git fetch`", "Only the remote copy in your repo (`origin/main`)"],
                        ["`git pull --rebase`", "Fetch, then put your commits on top"],
                        ["`git push`", "The remote branch"],
                        ["`git push origin v1.0`", "Sends one tag"],
                    ]),
                    ("Fix a rejected push in two commands", "Someone pushed first. Your push would erase their commit, so git stops.", ["Step", "Command"], [
                        ["1", "`git pull --rebase`"],
                        ["2", "`git push`"],
                    ]),
                    ("Find who changed a line, or when it appeared", "Ask the history, not a teammate.", ["Command", "Shows"], [
                        ["`git blame file`", "The last commit and author of each line"],
                        ["`git log -S\"text\"`", "Commits changing the text's occurrence count"],
                        ["`git log --oneline -- file`", "Commits that changed the file"],
                        ["`git show hash`", "What one commit changed"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Share my commit after a teammate pushed first",
                "frame": "You committed `Add order A11` and Alex pushed `Add Monday note` before you. Get his commit, then send yours.",
                "open": "cd /tmp/tw-git/shop",
                "steps": [
                    (None, "`git push`", "Git rejects it: the remote has a commit you lack."),
                    (None, "`git pull --rebase`", "Download his commit and put yours on top."),
                    (None, "`git push`", "Send yours."),
                ],
                "after": " ! [rejected]        main -> main (fetch first)\nSuccessfully rebased and updated refs/heads/main.\n   c354bd0..6d535dc  main -> main",
                "meaning": "A rejected push is a request to look first. Pull, then push again.",
            },
            "practice": {
                "h2": "Check your answers: remotes, pull, push, tags and blame",
                "qs": [
                    ("Mechanism", "Why does `git push` say \"rejected\" when someone pushed before me?",
                     "What would happen to their commit?",
                     ["The remote branch has a commit that your branch does not have.", "A push would replace their commit with your history, so git refuses."],
                     "Run `git pull --rebase`, then `git push`."),
                    ("Keystrokes", "How do I push a new branch `add-labels` and remember it for later pushes?",
                     "One flag links your branch to the remote one.",
                     ["Type `git push`.", "Add `-u origin add-labels`."],
                     "`git push -u origin add-labels`."),
                    ("Application", "How do I find the commit that first added the word `A9`?",
                     "Search the history for a piece of text.",
                     ["Run `git log -S\"A9\" --oneline`.", "Read the last line: it is the oldest commit."],
                     "`git log -S\"A9\" --oneline` prints the commit."),
                    ("Common mistake", "Why is my tag `v1.0` missing on GitHub after `git push`?",
                     "Does a plain push send tags?",
                     ["`git push` sends branches, not tags.", "Push the tag by name."],
                     "`git push origin v1.0`, or `git push --tags` for every tag."),
                ],
            },
        },
    ],
}
