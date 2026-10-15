"""Module 9: Find and text tools. Source: commands run on macOS (fd, find, mdfind, rg, grep, cut, sort, uniq, awk, sed, xargs, jq); no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


MODULE = {
    "n": 9,
    "folder": "m9-find-text",
    "title": "Find and text tools",
    "footer": "Find files and text: fd, find, mdfind, rg, grep, cut, sort, uniq, tr, awk, sed, xargs and jq with real output",
    "tagline": "Find any file, search any text, and reshape output with short pipelines.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Find files",
            "subtitle": "Find a file by name, size or age with fd, find and mdfind, and spot the biggest folders.",
            "idea": (
                "Pick the tool by where you search: fd or find inside a folder, mdfind across the whole Mac.",
                [
                    ("Find files by name", "fd report", "Add -e pdf for one extension."),
                    ("Find files bigger than 100 MB", "fd -S +100m", "find: -size +100M."),
                    ("Find a file anywhere on the Mac", "mdfind -name report", "Add -onlyin ~/Documents to narrow it."),
                    ("Find the biggest folders", "du -sh * | sort -h", "The last line is the biggest."),
                ],
                None,
            ),
            "problem": {
                "fail": "You know a file exists but not where, so you open folder after folder and scroll.",
                "fix": "Type what you know: a name, an extension, a size or a day. `fd` and `find` search a folder tree. `mdfind` searches the whole Mac at once.",
            },
            "drills": [
                {
                    "h2": "Find files by name with fd",
                    "intro": "`fd` searches below the current folder. The pattern is part of a file name. The sample files live in `/tmp/tw/find`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make the sample files for this page", "code": C('''
mkdir -p /tmp/tw/find/src /tmp/tw/find/docs /tmp/tw/find/.cfg && cd /tmp/tw/find
echo 'print("hi")' > src/app.py
echo 'print("test")' > src/test_app.py
echo '# Notes' > docs/Notes.md
echo 'todo' > docs/todo.txt
echo 'KEY=1' > .cfg/.env
echo 'x' > "my file.txt"
cat > run.log <<'EOF'
start
ERROR disk full
done
EOF
head -c 200000 /dev/zero > docs/data.bin
dd if=/dev/zero of=big.bin bs=1m count=120 2>/dev/null
touch -t 202401010000 old.txt
fd
'''),
                         "expect": "`fd` lists the 11 entries: `big.bin`, `docs/`, `docs/Notes.md`, `docs/data.bin`, `docs/todo.txt`, `my file.txt`, `old.txt`, `run.log`, `src/`, `src/app.py`, `src/test_app.py`. The order can differ. `.cfg` is missing because it is hidden."},
                        {"type": "text", "body": "On Linux, `dd` wants `bs=1M` with a capital M. Everything else in the setup is the same."},
                        {"type": "cmd", "where": "shell", "title": "Find files by part of the name", "code": C('''
fd app
'''),
                         "expect": "`src/app.py` and `src/test_app.py`. Both names contain `app`."},
                        {"type": "cmd", "where": "shell", "title": "Find files by extension", "code": C('''
fd -e md
fd -e py
'''),
                         "expect": "`docs/Notes.md` first. Then `src/app.py` and `src/test_app.py`."},
                        {"type": "cmd", "where": "shell", "title": "Find only folders or only files", "code": C('''
fd -t d
fd -t f log
'''),
                         "expect": "`-t d` prints the folders `docs/` and `src/`. `-t f log` prints the file `run.log`."},
                        {"type": "cmd", "where": "shell", "title": "Find hidden files", "code": C('''
fd env
fd -H env
'''),
                         "expect": "The first command prints nothing, because fd skips hidden files and folders. The second prints `.cfg/.env`."},
                        {"type": "cmd", "where": "shell", "title": "Skip a folder when you search", "code": C('''
fd -e txt -E docs
'''),
                         "expect": "`my file.txt` and `old.txt`. `docs/todo.txt` is skipped."},
                        {"type": "text", "body": "fd also skips files that `.gitignore` lists. `-I` shows them, and `-u` shows hidden and ignored files together."},
                    ],
                },
                {
                    "h2": "Find files by size or age with fd",
                    "intro": "Add a size or time filter to the same command. Units are `k`, `m`, `g` for size and `d`, `h`, `min` for time.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 MB", "code": C('''
fd -S +100m
'''),
                         "expect": "`big.bin`. It is the only file over 100 MB."},
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 KB", "code": C('''
fd -t f -S +100k
'''),
                         "expect": "`big.bin` and `docs/data.bin`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Find files older than one day", "code": C('''
fd -t f --changed-before 1d
'''),
                         "expect": "`old.txt`, which `touch -t` dated 1 January 2024."},
                        {"type": "cmd", "where": "shell", "title": "Find files changed in the last day", "code": C('''
fd -t f --changed-within 1d
'''),
                         "expect": "Every file except `old.txt`: `big.bin`, `docs/Notes.md`, `docs/data.bin`, `docs/todo.txt`, `my file.txt`, `run.log`, `src/app.py` and `src/test_app.py`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Run a command on every file you find", "code": C('''
fd -e log -x wc -l
fd -e md -x echo found {}
'''),
                         "expect": "`3 ./run.log`, the line count of `run.log`. Then `found ./docs/Notes.md`. `-x` runs the command once per match, and `{}` stands for the match."},
                    ],
                },
                {
                    "h2": "Find files with find",
                    "intro": "`find` is on every Mac and Linux box, so these work on a server where fd is not installed. It needs a start folder (`.`) and quotes around patterns.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find a file by name with find", "code": C('''
find . -name "*.py"
find . -iname "notes*"
'''),
                         "expect": "`./src/app.py` and `./src/test_app.py`. Then `./docs/Notes.md`: `-iname` ignores case, so `notes*` matches `Notes.md`."},
                        {"type": "cmd", "where": "shell", "title": "Find only folders, or only the top level", "code": C('''
find . -type d
find . -maxdepth 1 -type f
'''),
                         "expect": "`-type d` prints `.`, `./.cfg`, `./docs` and `./src`. `-maxdepth 1 -type f` prints the four files in this folder: `./big.bin`, `./my file.txt`, `./old.txt` and `./run.log`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 MB with find", "code": C('''
find . -type f -size +100M
'''),
                         "expect": "`./big.bin`."},
                        {"type": "cmd", "where": "shell", "title": "Find files by age with find", "code": C('''
find . -type f -mmin +43200
find . -type f -mtime -1 -name "*.log"
'''),
                         "expect": "`./old.txt`: changed more than 43200 minutes (30 days) ago. Then `./run.log`: changed within the last day. `-mtime +30` rounds to whole days and would skip a file that is 30.5 days old, so `-mmin` matches fd."},
                        {"type": "cmd", "where": "shell", "title": "Run a command on every file find lists", "code": C('''
find . -name "*.log" -exec wc -l {} +
'''),
                         "expect": "`3 ./run.log`. The `+` hands many files to one `wc` call."},
                        {"type": "cmd", "where": "shell", "title": "List what -delete would remove (dry run)", "code": C('''
find . -name "*.log" -print
'''),
                         "expect": "`./run.log`. Nothing is deleted. These are the files `-delete` would remove."},
                        {"type": "text", "body": "Warning: `-delete` has no undo and no prompt. Run the command with `-print` first and read the list. Put `-delete` last, because find acts on tests in order."},
                        {"type": "code", "file": "shell", "title": "Delete the files you just listed (only after the dry run)", "code": C('''
find . -name "*.log" -print
find . -name "*.log" -delete
''')},
                    ],
                },
                {
                    "h2": "Fuzzy find a file and pick it interactively with fzf",
                    "intro": "`fzf` turns any list into a picker. Pipe the output of `fd` into it, type a few letters of the name, then press Enter. Letters can be spread out: `sapp` finds `src/app.py`. These use the same sample files in `/tmp/tw/find`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Pick a file interactively from a list (fuzzy find a file)", "code": C('''
fd -e py | fzf
'''),
                         "expect": "A list with `src/app.py` and `src/test_app.py` and a prompt `>`. Type `tes`: the list narrows to `src/test_app.py` and the counter reads `1/2`. Press Enter: fzf prints the pick, `src/test_app.py`, and exits. Esc leaves without printing."},
                        {"type": "cmd", "where": "shell", "title": "Fuzzy find a file without the picker (fzf --filter)", "code": C('''
fd -t f | fzf --filter app
fd -t f | fzf --filter 'md$'
fd -t f | fzf --filter '^src !test'
'''),
                         "expect": "`src/app.py` and `src/test_app.py`: both names contain `app`. Then `docs/Notes.md`: `$` means the name ends there. Then `src/app.py`: `^` anchors the start and `!` drops the matches. `--filter` prints the matches and never opens the picker, so it works in scripts. The interactive picker takes the same query words."},
                        {"type": "cmd", "where": "shell", "title": "Preview a file while you pick it", "code": C('''
fd -t f | fzf --preview 'bat --color=always {}'
'''),
                         "expect": "The list sits on the left and the preview on the right. Type `app`: the list narrows to `src/app.py` and `src/test_app.py` (`2/9`). The preview of the highlighted file shows `File: src/app.py` and `1 │ print(\"hi\")`, with colors. `{}` stands for the highlighted line."},
                        {"type": "cmd", "where": "shell", "title": "Open the picked files in nvim (pick several)", "code": C('''
nvim $(fd -e py | fzf -m)
'''),
                         "expect": "`-m` allows several picks. Move to a line and press `Tab` to mark it, mark a second one, then press Enter. nvim opens `src/app.py` and `src/test_app.py` as two buffers. The top bar shows `app.py` and `test_app.py`, and `:bn` jumps to the other file. With one pick, nvim opens that single file."},
                        {"type": "text", "body": "File names with spaces split into pieces inside `$(...)`. With a single pick, put quotes around it: `nvim \"$(fzf)\"`."},
                        {"type": "keys", "where": "fzf", "title": "Pick a file, search history or change folder from the prompt, then the keys inside fzf", "rows": [
                            ("Ctrl-T", "Insert the path of a file you pick at the cursor (unbound in this setup, use `ff`)"),
                            ("Ctrl-R", "Search your command history and paste the pick on the prompt"),
                            ("Alt-C", "cd into a folder you pick. If Option types a letter, press Esc then c"),
                            ("Tab", "Mark or unmark the highlighted line and move down (with -m)"),
                            ("Enter", "Accept the marked lines, or the highlighted line if none are marked"),
                            ("Esc", "Leave without a pick"),
                        ]},
                        {"type": "text", "body": "More fzf helpers for this machine, such as `ff` (find a file), `frg` (search text), `fcd` (go up to a parent folder) and `fkill` (kill a process), are in module 1, page 3: Copy mode, the command line and fzf."},
                    ],
                },
                {
                    "h2": "Find anything on my Mac",
                    "intro": "`mdfind` asks the Spotlight index, so it is fast, but it only finds files Spotlight has indexed. Folders you excluded in System Settings, new files not indexed yet and `/tmp` are missing. These run on your own folders and your results will differ.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find a file anywhere by part of its name", "code": C('''
mdfind -name zshrc -onlyin ~/Downloads
'''),
                         "expect": "One full path for each file whose name contains `zshrc`, such as `/Users/you/Downloads/zshrc.sh`. `-onlyin` limits the search to one folder."},
                        {"type": "cmd", "where": "shell", "title": "Find files that contain a word", "code": C('''
mdfind -onlyin ~/Documents invoice | head -3
'''),
                         "expect": "Up to three full paths of files in Documents whose name or text contains `invoice`. Without `-name`, mdfind looks inside files too."},
                        {"type": "cmd", "where": "shell", "title": "Count the matches before you list them", "code": C('''
mdfind -count -onlyin ~/Documents invoice
'''),
                         "expect": "A single number, such as `142`. Your number differs."},
                        {"type": "cmd", "where": "shell", "title": "Find files changed in the last 7 days", "code": C('''
mdfind -onlyin ~/Documents 'kMDItemContentModificationDate >= $time.today(-7)' | head -3
'''),
                         "expect": "Up to three full paths of recently changed files. The single quotes keep the shell from touching `$time`."},
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 500 MB anywhere under home", "code": C('''
mdfind -onlyin ~ 'kMDItemFSSize > 500000000' | head -3
'''),
                         "expect": "Up to three full paths of files over 500 MB, often under `~/Library`. The size is in bytes."},
                        {"type": "cmd", "where": "shell", "title": "Find the biggest folders and files", "code": C('''
du -sh * | sort -h
du -sh * | sort -rh | head -3
'''),
                         "expect": "The first command lists `0B old.txt`, `4.0K my file.txt`, `4.0K run.log`, `8.0K src`, `204K docs` and `120M big.bin`, smallest first. Sizes can differ a little, and a file that was written twice may show more. The second prints the top three: `120M big.bin`, `204K docs`, `8.0K src`. `*` skips hidden names such as `.cfg`."},
                        {"type": "cmd", "where": "shell", "title": "Show the newest files first", "code": C('''
command ls -lt | head -4
'''),
                         "expect": "A `total` line, then the newest entries with sizes and dates. `big.bin` comes first here. `ls` is an alias for `eza` in this shell and `eza` reads `-t` differently, so `command ls` runs the real one."},
                    ],
                },
            ],
            "rules": {
                "h2": "Which find tool at a glance",
                "cards": [
                    ("Pick the tool", "One question picks the command.", ["You want to find", "Type"], [
                        ["A file by part of its name in this folder", "`fd name`"],
                        ["The same on any Linux box", "`find . -name \"*name*\"`"],
                        ["A file Spotlight has indexed, by name", "`mdfind -name name`"],
                        ["An indexed file, by a word inside", "`mdfind -onlyin ~ word`"],
                        ["The biggest folders here", "`du -sh * | sort -h`"],
                    ]),
                    ("Size and age tests", "The same job in fd and in find.", ["You want", "fd", "find"], [
                        ["Bigger than 100 MB", "`-S +100m`", "`-size +100M`"],
                        ["Changed in the last day", "`--changed-within 1d`", "`-mtime -1`"],
                        ["Not changed for 30 days", "`--changed-before 30d`", "`-mmin +43200`"],
                        ["Only files", "`-t f`", "`-type f`"],
                        ["Only folders", "`-t d`", "`-type d`"],
                    ]),
                    ("Delete with find, safely", "Three steps, always in this order.", ["Step", "Type"], [
                        ["1. List the matches", "`find . -name \"*.log\" -print`"],
                        ["2. Count them", "`find . -name \"*.log\" -print | wc -l`"],
                        ["3. Delete them", "`find . -name \"*.log\" -delete`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find the file eating your disk",
                "frame": "The folder feels heavy. You want the biggest file and the biggest folder.",
                "open": "cd /tmp/tw/find",
                "steps": [
                    (None, "`fd -S +100m`", "Lists every file over 100 MB: `big.bin`."),
                    (None, "`du -sh * | sort -rh | head -3`", "Ranks files and folders by size and keeps the top three. Sizes can differ a little."),
                    (None, "`fd -t f --changed-before 1d`", "Lists files you have not touched since yesterday: `old.txt`."),
                ],
                "after": "120M\tbig.bin\n204K\tdocs\n8.0K\tsrc",
                "meaning": "Size first, then age: two short commands point at what to clean up.",
            },
            "practice": {
                "h2": "Practice: find files",
                "qs": [
                    ("Mechanism", "`.cfg/.env` exists, but `fd env` prints nothing. Why?",
                     "What does fd skip unless you ask?",
                     ["fd skips hidden files and folders by default.", "Both `.cfg` and `.env` start with a dot."],
                     "Run `fd -H env`. It prints `.cfg/.env`."),
                    ("Keystrokes", "Which find command lists regular files bigger than 100 MB?",
                     "Two tests: the type and the size.",
                     ["Start in the current folder with `find .`.", "Add `-type f` for files only.", "Add `-size +100M`."],
                     "`find . -type f -size +100M` prints `./big.bin`."),
                    ("Application", "Count the lines of every Markdown file below the current folder.",
                     "Find by extension, then run a command on each match.",
                     ["`fd -e md` finds the files.", "`-x wc -l` runs `wc -l` on each one."],
                     "`fd -e md -x wc -l` prints `1 ./docs/Notes.md`."),
                    ("Common mistake", "You ran `find . -name \"*.log\" -delete` and lost a file you wanted. What should you have done first?",
                     "Does -delete ask or keep a copy?",
                     ["`-delete` removes at once, with no prompt and no undo.", "Swap `-delete` for `-print` and read the list."],
                     "Run `find . -name \"*.log\" -print` first. Replace `-print` with `-delete` only when the list is right."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Search inside files",
            "subtitle": "Find a word in a folder of files with rg, grep it from any output, and show the lines around it.",
            "idea": (
                "rg searches every file below the current folder. grep searches the files you name, or any output you pipe in.",
                [
                    ("Find a word in every file", "rg word", "rg is case sensitive. Add -i to ignore case."),
                    ("List only the files that contain a word", "rg -l word", "-c counts the matches per file."),
                    ("Show lines around a match", "rg -C 2 word", "Two lines before and after."),
                    ("Filter any output for a word", "command | grep word", "-v keeps the lines without it."),
                ],
                None,
            ),
            "problem": {
                "fail": "A word is somewhere in a project of hundreds of files, and opening them one by one takes forever.",
                "fix": "Give rg the word. It prints each file name, the line number and the line. Narrow it with a file type, a glob or a flag.",
            },
            "drills": [
                {
                    "h2": "Search for a word with rg",
                    "intro": "Run these in a terminal: rg shows a file name, then `line:text` for each match. Piped into another command, rg drops the headings.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make the sample files for this page", "code": C('''
mkdir -p /tmp/tw/grep && cd /tmp/tw/grep
cat > app.log <<'EOF'
2026-10-14 10:01:02 INFO  start worker=1
2026-10-14 10:01:05 ERROR disk full path=/data
2026-10-14 10:02:11 WARN  slow query ms=950
2026-10-14 10:03:40 ERROR timeout host=db1
2026-10-14 10:04:00 INFO  done worker=1
EOF
cat > main.py <<'EOF'
import os
def load(path):
    # TODO fix path handling
    return open(path).read()
print(load("app.log"))
EOF
printf 'Todo list\\n- ship the report\\n- error budget review\\n' > notes.md
echo 'API_HOST=localhost' > .env
rg --files
'''),
                         "expect": "`rg --files` lists `app.log`, `main.py` and `notes.md`. The order can differ. `.env` is hidden, so rg skips it."},
                        {"type": "cmd", "where": "shell", "title": "Search for a word in every file", "code": C('''
rg error
'''),
                         "expect": "`notes.md`, then `3:- error budget review`. The lines with `ERROR` in `app.log` do not match, because rg is case sensitive."},
                        {"type": "cmd", "where": "shell", "title": "Search ignoring upper and lower case", "code": C('''
rg -i error
'''),
                         "expect": "Both files. `notes.md` with `3:- error budget review`, and `app.log` with `2:` (the `ERROR disk full` line) and `4:` (the `ERROR timeout` line). The file order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Match a whole word only", "code": C('''
rg ERR
rg -w ERR
'''),
                         "expect": "The first command prints the two `ERROR` lines of `app.log`, because `ERR` is inside `ERROR`. The second prints nothing: `-w` needs `ERR` to stand alone."},
                        {"type": "cmd", "where": "shell", "title": "Search one file and show line numbers", "code": C('''
rg -n ERROR app.log
'''),
                         "expect": "`2:2026-10-14 10:01:05 ERROR disk full path=/data` and `4:2026-10-14 10:03:40 ERROR timeout host=db1`. `-n` adds the line numbers. In a terminal rg adds them anyway, but when you pipe the output you need `-n`."},
                        {"type": "cmd", "where": "shell", "title": "List only the names of files that contain a word", "code": C('''
rg -l ERROR
'''),
                         "expect": "`app.log`."},
                        {"type": "cmd", "where": "shell", "title": "Count the matching lines in each file", "code": C('''
rg -c ERROR
'''),
                         "expect": "`app.log:2`."},
                    ],
                },
                {
                    "h2": "Narrow the search to some files",
                    "intro": "Name a file type with `-t`, or a glob with `-g`. A `!` in front of the glob leaves those files out.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Search only Python files", "code": C('''
rg -t py load
'''),
                         "expect": "`main.py`, then `2:def load(path):` and `5:print(load(\"app.log\"))`."},
                        {"type": "cmd", "where": "shell", "title": "Search only files that match a glob", "code": C('''
rg -g '*.log' ERROR
'''),
                         "expect": "`app.log` with its two `ERROR` lines, 2 and 4."},
                        {"type": "cmd", "where": "shell", "title": "Search every file except one kind", "code": C('''
rg -g '!*.md' -i error
'''),
                         "expect": "Only `app.log`, lines 2 and 4. `notes.md` is left out."},
                        {"type": "cmd", "where": "shell", "title": "Search hidden files too", "code": C('''
rg --hidden API
'''),
                         "expect": "`.env`, then `1:API_HOST=localhost`. Without `--hidden` rg skips it."},
                        {"type": "cmd", "where": "shell", "title": "Find a file by name with rg", "code": C('''
rg --files | rg app
'''),
                         "expect": "`app.log`. `rg --files` lists every file rg would search, and the second `rg` filters the names."},
                    ],
                },
                {
                    "h2": "Show context and match patterns",
                    "intro": "Use `-F` for text with special characters. Use `-e` for several words. Quote any regex.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show the lines around a match", "code": C('''
rg -C 1 timeout
'''),
                         "expect": "`app.log`, then line 3 (`WARN slow query`) with a `-`, line 4 (the `ERROR timeout` line) with a `:`, and line 5 (`INFO done`) with a `-`. A `:` marks the match and a `-` marks the context."},
                        {"type": "cmd", "where": "shell", "title": "Search for text with special characters as it is", "code": C('''
rg -F 'path=/data'
'''),
                         "expect": "`app.log`, then `2:2026-10-14 10:01:05 ERROR disk full path=/data`. `-F` reads the pattern as plain text, not a regex."},
                        {"type": "cmd", "where": "shell", "title": "Search for one word or another", "code": C('''
rg -e ERROR -e WARN
'''),
                         "expect": "`app.log`, then lines 2 (`ERROR disk full`), 3 (`WARN slow query`) and 4 (`ERROR timeout`)."},
                        {"type": "cmd", "where": "shell", "title": "Search with a regex", "code": C('''
rg 'worker=[0-9]+'
'''),
                         "expect": "`app.log`, then lines 1 (`INFO start worker=1`) and 5 (`INFO done worker=1`)."},
                        {"type": "cmd", "where": "shell", "title": "Print only the part that matched", "code": C('''
rg -o 'host=\\w+'
'''),
                         "expect": "`app.log`, then `4:host=db1`. `-o` prints the match and not the whole line."},
                    ],
                },
                {
                    "h2": "Search with grep",
                    "intro": "`grep` is on every Linux box and Mac. It reads the files you name, or its input from a pipe.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Search a file for a word with grep", "code": C('''
grep ERROR app.log
grep -n WARN app.log
'''),
                         "expect": "The two `ERROR` lines, 2 and 4, without line numbers. Then `3:2026-10-14 10:02:11 WARN  slow query ms=950`."},
                        {"type": "cmd", "where": "shell", "title": "Search a whole folder with grep", "code": C('''
grep -rn ERROR .
grep -rl ERROR .
'''),
                         "expect": "`./app.log:2:` and `./app.log:4:` with the lines. Then only the file name `./app.log`. `-r` searches folders. Without it `grep ERROR .` prints `grep: .: Is a directory`."},
                        {"type": "cmd", "where": "shell", "title": "Show lines that do not contain a word", "code": C('''
grep -v INFO app.log
'''),
                         "expect": "The three lines of `app.log` without `INFO`: the `ERROR disk full`, `WARN slow query` and `ERROR timeout` lines."},
                        {"type": "cmd", "where": "shell", "title": "Search for one word or another with grep", "code": C('''
grep -E 'ERROR|WARN' app.log
'''),
                         "expect": "Lines 2, 3 and 4 of `app.log`. `-E` turns on the `|` for \"or\"."},
                        {"type": "cmd", "where": "shell", "title": "Count matches, or print only the matching part", "code": C('''
grep -c ERROR app.log
grep -o 'ms=[0-9]*' app.log
'''),
                         "expect": "`2`, the number of `ERROR` lines. Then `ms=950`."},
                        {"type": "cmd", "where": "shell", "title": "Show lines after or before a match with grep", "code": C('''
grep -A1 ERROR app.log
grep -B1 timeout app.log
'''),
                         "expect": "`-A1` prints each `ERROR` line plus the line after it, 4 lines in all. `-B1` prints the `WARN slow query` line and then the `ERROR timeout` line."},
                    ],
                },
                {
                    "h2": "Pipe into grep to filter any output",
                    "intro": "Put `| grep word` after any command to keep only the lines with that word. Chain it to narrow further.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Filter a command's output with grep", "code": C('''
cat app.log | grep ERROR
cat app.log | grep ERROR | grep timeout
'''),
                         "expect": "The two `ERROR` lines. Then only the `ERROR timeout host=db1` line."},
                        {"type": "cmd", "where": "shell", "title": "Filter rg output with grep", "code": C('''
rg -n ERROR app.log | grep timeout
'''),
                         "expect": "`4:2026-10-14 10:03:40 ERROR timeout host=db1`."},
                        {"type": "cmd", "where": "shell", "title": "Count the lines that match", "code": C('''
cat app.log | grep -c INFO
'''),
                         "expect": "`2`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Search flags at a glance",
                "cards": [
                    ("rg and grep side by side", "Most flags have the same letter in both.", ["Task", "rg", "grep"], [
                        ["Search a folder", "`rg word`", "`grep -r word .`"],
                        ["Ignore case", "`-i`", "`-i`"],
                        ["Whole word only", "`-w`", "`-w`"],
                        ["Line numbers", "`-n` (on in a terminal)", "`-n`"],
                        ["File names only", "`-l`", "`-l`"],
                        ["Count matching lines", "`-c`", "`-c`"],
                        ["Skip matching lines", "`-v`", "`-v`"],
                        ["Lines around a match", "`-C 2`", "`-C 2`"],
                        ["Several patterns", "`-e a -e b`", "`-E 'a|b'`"],
                        ["Only the match", "`-o`", "`-o`"],
                        ["Plain text, no regex", "`-F`", "`-F`"],
                    ]),
                    ("Narrow where rg looks", "rg skips hidden, git-ignored and binary files unless you say otherwise.", ["Task", "Type"], [
                        ["Search Python files only", "`rg -t py word`"],
                        ["Search files that match a glob", "`rg -g '*.log' word`"],
                        ["Search everything except Markdown", "`rg -g '!*.md' word`"],
                        ["Search hidden files too", "`rg --hidden word`"],
                        ["Search git-ignored files too", "`rg -u word`"],
                        ["Search hidden and git-ignored files too", "`rg -uu word`"],
                        ["Find a file by name", "`rg --files | rg name`"],
                    ]),
                    ("Filter any output", "grep reads from a pipe, so it works on any command.", ["Task", "Type"], [
                        ["List processes that mention nginx", "`ps aux | grep nginx`"],
                        ["Show ERROR lines, minus the disk ones", "`cat app.log | grep ERROR | grep -v disk`"],
                        ["Keep rg hits that also contain another word", "`rg -n word | grep other`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find the failing host in a log",
                "frame": "A log has errors. You want to know which file holds the timeout and what happened around it.",
                "open": "cd /tmp/tw/grep",
                "steps": [
                    (None, "`rg -l ERROR`", "Names the files with an error: `app.log`."),
                    (None, "`rg -c ERROR`", "Counts them: `app.log:2`."),
                    (None, "`rg -C 1 timeout`", "Shows the timeout line and one line each side."),
                ],
                "after": "app.log\n3-2026-10-14 10:02:11 WARN  slow query ms=950\n4:2026-10-14 10:03:40 ERROR timeout host=db1\n5-2026-10-14 10:04:00 INFO  done worker=1",
                "meaning": "Names first, counts next, then the lines around the one you care about.",
            },
            "practice": {
                "h2": "Practice: search inside files",
                "qs": [
                    ("Mechanism", "`rg error` shows only `notes.md`, not the ERROR lines of `app.log`. Why?",
                     "Is rg case sensitive?",
                     ["rg matches letter case by default.", "`app.log` has `ERROR` in capitals, and the pattern is lower case."],
                     "Add `-i`: `rg -i error` finds both files."),
                    ("Keystrokes", "Which command prints only the names of the files that contain ERROR?",
                     "One letter, lower case L.",
                     ["Type `rg`.", "Add `-l`.", "Add the word."],
                     "`rg -l ERROR` prints `app.log`."),
                    ("Application", "Show the `timeout` line with one line before and one after.",
                     "C for context.",
                     ["Use `-C` for lines on both sides.", "Give it the count `1`."],
                     "`rg -C 1 timeout` prints lines 3, 4 and 5 of `app.log`."),
                    ("Common mistake", "`grep ERROR .` prints `grep: .: Is a directory`. What do you add?",
                     "grep reads files, not folders, until you tell it to walk them.",
                     ["`.` is a folder, and grep skips folders by default.", "`-r` makes grep walk the folder.", "`-n` adds the line numbers."],
                     "`grep -rn ERROR .` prints each match as `./app.log:2:...`. Plain `-r` leaves out the line numbers."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Slice, sort and count",
            "subtitle": "Cut columns, sort, count repeats and tidy output with cut, sort, uniq, wc, tr, head, tail, column and paste.",
            "idea": (
                "Each tool does one small job and passes its output on. Chain them with |.",
                [
                    ("Pick one column from a file", "cut -d' ' -f1 access.log", "-d is the separator, -f the column."),
                    ("Count how many times each line appears", "sort | uniq -c", "Sort first, then count."),
                    ("Show the top 5 most common lines", "sort | uniq -c | sort -rn | head -5", "The most common line comes first."),
                    ("Count the lines in a file", "wc -l file", "-w counts words, -c bytes."),
                ],
                None,
            ),
            "problem": {
                "fail": "You have a long log or CSV and need one column, a ranking or a count, and a spreadsheet is too much for it.",
                "fix": "Chain small tools. `cut` picks the column, `sort` orders it, `uniq -c` counts, `head` keeps the top. Each step shows its result, so you can build the chain one tool at a time.",
            },
            "drills": [
                {
                    "h2": "Pick columns with cut",
                    "intro": "`cut` takes a column from each line. The sample files live in `/tmp/tw/cols`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make the sample files for this page", "code": C('''
mkdir -p /tmp/tw/cols && cd /tmp/tw/cols
cat > access.log <<'EOF'
10.0.0.1 GET /home 200 512
10.0.0.2 GET /about 200 1024
10.0.0.1 GET /home 200 512
10.0.0.3 POST /login 302 90
10.0.0.1 GET /missing 404 0
10.0.0.2 GET /home 200 512
EOF
cat > users.csv <<'EOF'
name,team,age
ana,ops,31
ben,dev,28
cleo,dev,35
dan,ops,28
EOF
wc -l access.log users.csv
'''),
                         "expect": "`6 access.log`, `5 users.csv` and `11 total`."},
                        {"type": "cmd", "where": "shell", "title": "Cut one column from a file", "code": C('''
cut -d' ' -f1 access.log
'''),
                         "expect": "The first column of each line: `10.0.0.1`, `10.0.0.2`, `10.0.0.1`, `10.0.0.3`, `10.0.0.1`, `10.0.0.2`. `-d' '` splits on spaces and `-f1` keeps field 1."},
                        {"type": "cmd", "where": "shell", "title": "Cut columns from a CSV file", "code": C('''
cut -d, -f1,3 users.csv
'''),
                         "expect": "`name,age`, `ana,31`, `ben,28`, `cleo,35`, `dan,28`. Fields 1 and 3, split on commas."},
                        {"type": "cmd", "where": "shell", "title": "Cut the first characters of each line", "code": C('''
cut -c1-8 access.log
'''),
                         "expect": "The first 8 characters of each line: `10.0.0.1`, `10.0.0.2`, `10.0.0.1`, `10.0.0.3`, `10.0.0.1`, `10.0.0.2`."},
                    ],
                },
                {
                    "h2": "Sort lines",
                    "intro": "`sort` compares text, so `100` comes before `9`. Add `-n` for numbers and `-h` for sizes such as `2M`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Sort numbers by value, not as text", "code": C('''
printf '10\\n9\\n100\\n' | sort
printf '10\\n9\\n100\\n' | sort -n
'''),
                         "expect": "The first prints `10`, `100`, `9`. The second prints `9`, `10`, `100`."},
                        {"type": "cmd", "where": "shell", "title": "Sort backwards or drop duplicates", "code": C('''
printf 'b\\na\\nb\\n' | sort -r
printf 'b\\na\\nb\\n' | sort -u
'''),
                         "expect": "`-r` prints `b`, `b`, `a`. `-u` prints `a`, `b`."},
                        {"type": "cmd", "where": "shell", "title": "Sort sizes such as 1K and 2M", "code": C('''
printf '1K\\n2M\\n500\\n' | sort -h
'''),
                         "expect": "`500`, `1K`, `2M`."},
                        {"type": "cmd", "where": "shell", "title": "Sort a CSV by a column", "code": C('''
tail -n +2 users.csv | sort -t, -k3 -nr
tail -n +2 users.csv | sort -t, -k2,2
'''),
                         "expect": "`tail -n +2` drops the header. The first command sorts by age, oldest first: `cleo,dev,35`, `ana,ops,31`, `dan,ops,28`, `ben,dev,28`. The second sorts by team: `ben,dev,28`, `cleo,dev,35`, `ana,ops,31`, `dan,ops,28`. `-t,` sets the separator and `-k3` the column."},
                        {"type": "cmd", "where": "shell", "title": "List each different value once", "code": C('''
cut -d' ' -f1 access.log | sort -u
'''),
                         "expect": "`10.0.0.1`, `10.0.0.2`, `10.0.0.3`."},
                    ],
                },
                {
                    "h2": "Count and rank",
                    "intro": "`uniq` only compares neighbouring lines, so sort first. The last recipe is the one to remember.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Count how many times each line appears", "code": C('''
cut -d' ' -f1 access.log | sort | uniq -c
'''),
                         "expect": "`3 10.0.0.1`, `2 10.0.0.2`, `1 10.0.0.3`."},
                        {"type": "cmd", "where": "shell", "title": "Show only the lines that repeat", "code": C('''
cut -d' ' -f1 access.log | sort | uniq -d
'''),
                         "expect": "`10.0.0.1` and `10.0.0.2`. `10.0.0.3` appears once, so it is left out."},
                        {"type": "cmd", "where": "shell", "title": "Show the top 3 most common values", "code": C('''
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head -3
cut -d' ' -f3 access.log | sort | uniq -c | sort -rn | head -1
'''),
                         "expect": "The first prints `3 10.0.0.1`, `2 10.0.0.2`, `1 10.0.0.3`. The second prints the most requested page: `3 /home`."},
                        {"type": "cmd", "where": "shell", "title": "Count lines, words and bytes", "code": C('''
wc -l users.csv
wc -c users.csv
echo "one two three" | wc -w
'''),
                         "expect": "`5 users.csv` lines, then `59 users.csv` bytes, then `3` words."},
                    ],
                },
                {
                    "h2": "Change characters with tr",
                    "intro": "`tr` swaps or removes single characters. It reads standard input, from a pipe or from `< file`, and takes no file name argument.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Change text to upper case", "code": C('''
echo "Hello World" | tr 'a-z' 'A-Z'
'''),
                         "expect": "`HELLO WORLD`."},
                        {"type": "cmd", "where": "shell", "title": "Delete a character from text", "code": C('''
echo "Hello World" | tr -d 'l'
'''),
                         "expect": "`Heo Word`."},
                        {"type": "cmd", "where": "shell", "title": "Squeeze repeated spaces into one", "code": C('''
echo "a    b     c" | tr -s ' '
'''),
                         "expect": "`a b c`."},
                        {"type": "cmd", "where": "shell", "title": "Turn lines into one comma-separated line", "code": C('''
cut -d' ' -f1 access.log | sort -u | tr '\\n' ','
'''),
                         "expect": "`10.0.0.1,10.0.0.2,10.0.0.3,` on one line, with a trailing comma and no newline, so the next prompt follows on the same line."},
                        {"type": "cmd", "where": "shell", "title": "Turn a comma-separated line into lines", "code": C('''
echo "a,b,c" | tr ',' '\\n'
'''),
                         "expect": "`a`, `b` and `c`, one per line."},
                    ],
                },
                {
                    "h2": "Look at the start and end, line up columns, save as you go",
                    "intro": "`head` and `tail` keep the first or last lines. `column -t` lines up columns. `paste` joins files side by side. `tee` saves a copy mid-pipe.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show the first or last lines of a file", "code": C('''
head -n 2 access.log
tail -n 2 access.log
'''),
                         "expect": "Lines 1 and 2: `10.0.0.1 GET /home 200 512` and `10.0.0.2 GET /about 200 1024`. Then lines 5 and 6: `10.0.0.1 GET /missing 404 0` and `10.0.0.2 GET /home 200 512`."},
                        {"type": "cmd", "where": "shell", "title": "Show a file from line 5 onward", "code": C('''
tail -n +5 access.log
'''),
                         "expect": "Lines 5 and 6: `10.0.0.1 GET /missing 404 0` and `10.0.0.2 GET /home 200 512`."},
                        {"type": "cmd", "where": "shell", "title": "Line up the columns of a CSV file", "code": C('''
column -t -s, users.csv
'''),
                         "expect": "A table with aligned columns: `name  team  age`, `ana   ops   31`, `ben   dev   28`, `cleo  dev   35`, `dan   ops   28`."},
                        {"type": "cmd", "where": "shell", "title": "Join two files side by side", "code": C('''
cut -d, -f1 users.csv | tail -n +2 > names.txt
cut -d, -f3 users.csv | tail -n +2 > ages.txt
paste -d: names.txt ages.txt
paste -sd, names.txt
'''),
                         "expect": "`ana:31`, `ben:28`, `cleo:35`, `dan:28`. Then all names on one line: `ana,ben,cleo,dan`."},
                        {"type": "cmd", "where": "shell", "title": "Save a copy of the output and keep going", "code": C('''
cut -d' ' -f1 access.log | sort -u | tee ips.txt | wc -l
cat ips.txt
'''),
                         "expect": "`3`, the number of different IPs. Then `ips.txt` holds `10.0.0.1`, `10.0.0.2`, `10.0.0.3`."},
                        {"type": "cmd", "where": "shell", "title": "Watch a file grow", "code": C('''
cp access.log live.log
tail -n 2 -f live.log
'''),
                         "expect": "The last 2 lines of `live.log`, then the command waits. In a second pane run `echo \"10.0.0.9 GET /new 200 1\" >> live.log`: the new line appears at once. Press `Ctrl-c` to stop."},
                    ],
                },
            ],
            "rules": {
                "h2": "Text tools at a glance",
                "cards": [
                    ("cut, sort and uniq", "The flags that do the work.", ["Task", "Type"], [
                        ["Take field 2, split on commas", "`cut -d, -f2`"],
                        ["Take the first 8 characters", "`cut -c1-8`"],
                        ["Sort numbers by value", "`sort -n`"],
                        ["Sort in reverse order", "`sort -r`"],
                        ["Sort sizes such as 500, 1K, 2M", "`sort -h`"],
                        ["Sort and keep each line once", "`sort -u`"],
                        ["Sort a CSV by column 3", "`sort -t, -k3`"],
                        ["Count each line (sort first)", "`uniq -c`"],
                        ["Show only the lines that repeat", "`uniq -d`"],
                    ]),
                    ("The top-N recipe", "Count repeated values and rank them. Change the field or the 5.", None, C('''
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head -5
''')),
                    ("wc, tr, head and tail", "Count, change and trim.", ["Task", "Type"], [
                        ["Count lines", "`wc -l file`"],
                        ["Count words", "`wc -w file`"],
                        ["Count bytes", "`wc -c file`"],
                        ["Change to upper case", "`tr 'a-z' 'A-Z'`"],
                        ["Remove a character", "`tr -d 'l'`"],
                        ["Squeeze repeated characters into one", "`tr -s ' '`"],
                        ["Turn newlines into commas", "`tr '\\n' ','`"],
                        ["Show the first or last 3 lines", "`head -n 3` or `tail -n 3`"],
                        ["Skip the header line", "`tail -n +2`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find the busiest IP in a log",
                "frame": "A web server log has one line per request. Who asks the most?",
                "open": "cd /tmp/tw/cols",
                "steps": [
                    (None, "`cut -d' ' -f1 access.log`", "Keeps only the IP column."),
                    (None, "`| sort`", "Puts equal IPs next to each other."),
                    (None, "`| uniq -c`", "Collapses them and counts each."),
                    (None, "`| sort -rn | head -3`", "Ranks the counts from high to low and keeps three."),
                ],
                "after": "   3 10.0.0.1\n   2 10.0.0.2\n   1 10.0.0.3",
                "meaning": "The same four steps rank anything: IPs, pages, error codes or words.",
            },
            "practice": {
                "h2": "Practice: slice, sort and count",
                "qs": [
                    ("Mechanism", "Why does `uniq -c` count each IP once when you skip `sort`?",
                     "What does uniq compare?",
                     ["`uniq` only collapses neighbouring identical lines.", "Unsorted, the same IP sits in several places."],
                     "Without `sort`, `cut -d' ' -f1 access.log | uniq -c` prints six lines, each with a count of `1`. Sort first."),
                    ("Keystrokes", "Which pipeline prints the most requested page in `access.log`?",
                     "Field 3, then the top-N recipe with one line kept.",
                     ["`cut -d' ' -f3 access.log` keeps the page.", "`sort | uniq -c` counts each page.", "`sort -rn | head -1` keeps the highest."],
                     "`cut -d' ' -f3 access.log | sort | uniq -c | sort -rn | head -1` prints `3 /home`."),
                    ("Application", "Turn the different IPs into one comma-separated line with no trailing comma.",
                     "paste can join lines.",
                     ["`cut -d' ' -f1 access.log | sort -u` lists each IP once.", "`paste -sd, -` joins the lines with commas. The last `-` reads the pipe."],
                     "`cut -d' ' -f1 access.log | sort -u | paste -sd, -` prints `10.0.0.1,10.0.0.2,10.0.0.3`."),
                    ("Common mistake", "`sort` puts `100` before `9`. How do you fix it?",
                     "Plain sort compares characters.",
                     ["Plain `sort` compares text, and `1` comes before `9`.", "`-n` compares by number."],
                     "Use `sort -n`: `9`, `10`, `100`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Transform",
            "subtitle": "Reshape text with awk, sed, xargs and jq, then chain them to answer real questions.",
            "idea": (
                "awk works on columns, sed on patterns, xargs turns lines into arguments, and jq reads JSON.",
                [
                    ("Print one column", "awk '{print $3}' file", "Add -F, for a CSV."),
                    ("Replace text in a file", "sed -i '' 's/old/new/g' file", "macOS needs the empty ''."),
                    ("Run a command on every line of output", "xargs", "Add -0 for names with spaces."),
                    ("Read one field from JSON", "jq -r '.name' file.json", "-r removes the quotes."),
                ],
                None,
            ),
            "problem": {
                "fail": "The output is almost what you need: one column, one changed word, one field out of a JSON file.",
                "fix": "Pick the tool by the shape of the data: awk for columns, sed for text patterns, jq for JSON. Use xargs to feed lines to another command.",
            },
            "drills": [
                {
                    "h2": "Work with columns using awk",
                    "intro": "`awk` splits every line into `$1`, `$2` and so on. `-F,` changes the separator. The sample files live in `/tmp/tw/xf`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make the sample files for this page", "code": C('''
mkdir -p /tmp/tw/xf/logs && cd /tmp/tw/xf
cat > access.log <<'EOF'
10.0.0.1 GET /home 200 512
10.0.0.2 GET /about 200 1024
10.0.0.1 GET /home 200 512
10.0.0.3 POST /login 302 90
10.0.0.1 GET /missing 404 0
10.0.0.2 GET /home 200 512
EOF
cat > pay.csv <<'EOF'
name,team,pay
ana,ops,3100
ben,dev,2800
cleo,dev,3500
dan,ops,2800
EOF
printf 'hello world\\nhello bash\\nbye world\\n' > notes.txt
echo '{"users":[{"name":"ana","age":31,"team":"ops"},{"name":"ben","age":28,"team":"dev"},{"name":"cleo","age":35,"team":"dev"}]}' > users.json
head -c 3000 /dev/zero > logs/a.log
head -c 1500 /dev/zero > logs/b.log
echo x > "my first file.txt"
echo y > "old notes.txt"
wc -l access.log pay.csv notes.txt
'''),
                         "expect": "`6 access.log`, `5 pay.csv`, `3 notes.txt` and `14 total`."},
                        {"type": "cmd", "where": "shell", "title": "Print one or two columns", "code": C('''
awk '{print $3, $5}' access.log | head -2
awk -F, '{print $1, $3}' pay.csv
'''),
                         "expect": "`/home 512` and `/about 1024`. Then the name and pay of every row: `name pay`, `ana 3100`, `ben 2800`, `cleo 3500`, `dan 2800`."},
                        {"type": "cmd", "where": "shell", "title": "Print only the rows that match a condition", "code": C('''
awk -F, 'NR > 1 && $3 > 3000' pay.csv
awk -F, '$2 == "dev" {print $1}' pay.csv
awk '$4 == 404' access.log
'''),
                         "expect": "`ana,ops,3100` and `cleo,dev,3500`: pay over 3000, with the header skipped by `NR > 1`. Then the dev team: `ben` and `cleo`. Then the 404 line: `10.0.0.1 GET /missing 404 0`."},
                        {"type": "cmd", "where": "shell", "title": "Add up a column", "code": C('''
awk '{sum += $5} END {print sum}' access.log
awk -F, 'NR > 1 {sum += $3} END {print sum}' pay.csv
'''),
                         "expect": "`2650`, the total bytes served. Then `12200`, the total pay."},
                        {"type": "cmd", "where": "shell", "title": "Count rows by a key", "code": C('''
awk '{n[$1]++} END {for (k in n) print k, n[k]}' access.log | sort
'''),
                         "expect": "`10.0.0.1 3`, `10.0.0.2 2`, `10.0.0.3 1`. The `sort` fixes the order, because awk loops over keys in no set order."},
                        {"type": "cmd", "where": "shell", "title": "Count lines and fields with NR and NF", "code": C('''
awk 'END {print NR}' access.log
awk '{print NF}' access.log | head -1
awk '{print $NF}' access.log | head -2
'''),
                         "expect": "`6` lines. Then `5` fields on the first line. Then the last field of the first two lines: `512` and `1024`."},
                        {"type": "cmd", "where": "shell", "title": "Format the output with printf", "code": C('''
awk '{printf "%-10s %s\\n", $1, $3}' access.log | head -3
awk -F, 'NR > 1 {sum += $3} END {printf "avg %.1f\\n", sum / (NR - 1)}' pay.csv
'''),
                         "expect": "Two aligned columns: `10.0.0.1   /home`, `10.0.0.2   /about`, `10.0.0.1   /home`. Then `avg 3050.0`."},
                    ],
                },
                {
                    "h2": "Replace and delete text with sed",
                    "intro": "`sed 's/old/new/'` replaces the first match on each line. Add `g` for every match. Nothing is saved unless you use `-i`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Replace a word in every line", "code": C('''
sed 's/hello/hi/' notes.txt
'''),
                         "expect": "`hi world`, `hi bash`, `bye world`. The file itself is unchanged."},
                        {"type": "cmd", "where": "shell", "title": "Replace every match on a line, not just the first", "code": C('''
sed 's/o/0/g' notes.txt
'''),
                         "expect": "`hell0 w0rld`, `hell0 bash`, `bye w0rld`. Without the `g`, only the first `o` on each line changes."},
                        {"type": "cmd", "where": "shell", "title": "Delete a line by number or by pattern", "code": C('''
sed '2d' notes.txt
sed '/bye/d' notes.txt
'''),
                         "expect": "`2d` leaves `hello world` and `bye world`. `/bye/d` leaves `hello world` and `hello bash`."},
                        {"type": "cmd", "where": "shell", "title": "Print only some lines", "code": C('''
sed -n '2,3p' notes.txt
sed -n '/bash/p' notes.txt
sed -n '$p' notes.txt
'''),
                         "expect": "Lines 2 to 3: `hello bash` and `bye world`. Then the line with `bash`: `hello bash`. Then the last line: `bye world`. `-n` turns off the normal output, and `p` prints."},
                        {"type": "cmd", "where": "shell", "title": "Make several replacements at once", "code": C('''
sed -e 's/hello/hi/' -e 's/world/earth/' notes.txt
'''),
                         "expect": "`hi earth`, `hi bash`, `bye earth`."},
                        {"type": "cmd", "where": "shell", "title": "Edit a file in place (macOS)", "code": C('''
cp notes.txt edit.txt
sed -i '' 's/hello/hi/' edit.txt
cat edit.txt
'''),
                         "expect": "`hi world`, `hi bash`, `bye world`. `edit.txt` itself changed. The `''` after `-i` is the backup suffix, empty here."},
                        {"type": "text", "body": "GNU and Linux: `sed -i 's/old/new/' file` has no `''`. On a Mac, without the `''`, sed fails with `invalid command code`."},
                        {"type": "cmd", "where": "shell", "title": "Add text at the start of every line", "code": C('''
sed 's/^/> /' notes.txt
'''),
                         "expect": "`> hello world`, `> hello bash`, `> bye world`."},
                        {"type": "cmd", "where": "shell", "title": "Swap two words with a regex group", "code": C('''
sed -E 's/([a-z]+) ([a-z]+)/\\2 \\1/' notes.txt
'''),
                         "expect": "`world hello`, `bash hello`, `world bye`. `-E` turns on groups and `\\1`, `\\2` paste them back."},
                    ],
                },
                {
                    "h2": "Run a command on every line with xargs",
                    "intro": "`xargs` reads lines and builds a command from them. Names that contain spaces need `-0` with a null-separated list.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Run a command once per argument", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -n 1 echo item
printf 'a\\nb\\nc\\n' | xargs -n 2 echo
'''),
                         "expect": "`item a`, `item b`, `item c`. Then `a b` and `c`. `-n 1` gives each run one argument, and `-n 2` gives two."},
                        {"type": "cmd", "where": "shell", "title": "Put each line in the middle of a command", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -I {} echo file-{}.txt
'''),
                         "expect": "`file-a.txt`, `file-b.txt`, `file-c.txt`. `-I {}` marks where each line goes."},
                        {"type": "cmd", "where": "shell", "title": "Run jobs in parallel", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -P 3 -I {} echo job {}
'''),
                         "expect": "`job a`, `job b` and `job c`. `-P 3` runs up to three at once, so the order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Handle file names with spaces", "code": C('''
fd -e txt | xargs wc -c
fd -e log -0 | xargs -0 wc -c
'''),
                         "expect": "The first command breaks the names at the spaces. It prints four errors, such as `wc: my: open: No such file or directory`, for `my`, `first`, `file.txt` and `old`. It also counts the pieces that are real files: `27 edit.txt`, `33 notes.txt`, `33 notes.txt` and `93 total`. `notes.txt` appears twice because `old notes.txt` splits into `old` and `notes.txt`. The second command prints a count for each `.log` file: `166 ./access.log`, `3000 ./logs/a.log`, `1500 ./logs/b.log`, then `4666 total`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Pass find results that have spaces to xargs", "code": C('''
find . -name "*.log" -print0 | xargs -0 wc -c
'''),
                         "expect": "The same three counts and `4666 total`. `-print0` and `-0` use a null byte, not a space, to separate names."},
                    ],
                },
                {
                    "h2": "Read JSON with jq",
                    "intro": "`jq` takes a path like `.users[0].name`. `.[]` walks a list. The pipe `|` inside the quotes feeds one step into the next.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Pretty-print a JSON file", "code": C('''
jq . users.json | head -8
'''),
                         "expect": "The JSON spread over lines with two-space indents: `{`, `\"users\": [`, `{`, `\"name\": \"ana\",`, `\"age\": 31,`, `\"team\": \"ops\"` and so on."},
                        {"type": "cmd", "where": "shell", "title": "Read one field from JSON", "code": C('''
jq '.users[0].name' users.json
jq -r '.users[].name' users.json
'''),
                         "expect": "`\"ana\"` with quotes. Then the names without quotes, one per line: `ana`, `ben`, `cleo`. `-r` prints raw text."},
                        {"type": "cmd", "where": "shell", "title": "Count items and list the field names", "code": C('''
jq '.users | length' users.json
jq '.users[0] | keys' users.json
'''),
                         "expect": "`3`. Then the keys of the first user, in order: `\"age\"`, `\"name\"`, `\"team\"`."},
                        {"type": "cmd", "where": "shell", "title": "Keep only the items that match a condition", "code": C('''
jq '.users[] | select(.age > 30) | .name' users.json
jq -r '.users[] | select(.team == "dev") | "\\(.name) \\(.age)"' users.json
'''),
                         "expect": "`\"ana\"` and `\"cleo\"`, the users over 30. Then the dev team as text: `ben 28` and `cleo 35`."},
                        {"type": "cmd", "where": "shell", "title": "Turn a list into one value", "code": C('''
jq -r '.users | map(.name) | join(",")' users.json
jq '.users | map(.age) | add' users.json
'''),
                         "expect": "`ana,ben,cleo`. Then `94`, the sum of the ages."},
                    ],
                },
                {
                    "h2": "Pipelines that answer a real question",
                    "intro": "Each one chains the tools above. Build them one step at a time: run the first command, add a pipe, run again.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show the top 5 IPs in a log", "code": C('''
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
'''),
                         "expect": "`3 10.0.0.1`, `2 10.0.0.2`, `1 10.0.0.3`. The log has only three IPs, so `head -5` shows all three."},
                        {"type": "cmd", "where": "shell", "title": "Add up the size of all .log files", "code": C('''
find . -name "*.log" -print0 | xargs -0 wc -c | tail -n 1
fd -e log -x stat -f %z | awk '{s += $1} END {print s " bytes"}'
'''),
                         "expect": "`4666 total`, then `4666 bytes`. On Linux, `stat -c %s` replaces `stat -f %z`."},
                        {"type": "cmd", "where": "shell", "title": "Show what a rename would do before you do it", "code": C('''
for f in *\\ *; do echo mv "'$f'" "'${f// /_}'"; done
'''),
                         "expect": "`mv 'my first file.txt' 'my_first_file.txt'` and `mv 'old notes.txt' 'old_notes.txt'`. Nothing is renamed: `echo` only prints the commands."},
                        {"type": "cmd", "where": "shell", "title": "Rename files: replace spaces with underscores", "code": C('''
for f in *\\ *; do mv "$f" "${f// /_}"; done
printf '%s\\n' *.txt
'''),
                         "expect": "`edit.txt`, `my_first_file.txt`, `notes.txt` and `old_notes.txt`. The files with spaces are gone. The rename changed the sample files, so to redo this page use a fresh sample folder: change `xf` to `xf2` in the first block and run the page again."},
                    ],
                },
            ],
            "rules": {
                "h2": "Transform tools at a glance",
                "cards": [
                    ("awk", "Columns, conditions and totals.", ["Task", "Type"], [
                        ["Print column 1", "`awk '{print $1}'`"],
                        ["Print column 2 of a CSV", "`awk -F, '{print $2}'`"],
                        ["Print rows where column 3 is over 100", "`awk '$3 > 100'`"],
                        ["Add up column 2", "`awk '{s += $2} END {print s}'`"],
                        ["Count rows by column 1", "`awk '{n[$1]++} END {for (k in n) print k, n[k]}'`"],
                        ["Skip the first line", "`awk 'NR > 1'`"],
                        ["Count lines", "`awk 'END {print NR}'`"],
                    ]),
                    ("sed", "Replace, delete and print.", ["Task", "Type"], [
                        ["Replace the first match on each line", "`sed 's/old/new/'`"],
                        ["Replace every match", "`sed 's/old/new/g'`"],
                        ["Delete line 2", "`sed '2d'`"],
                        ["Delete lines that contain a word", "`sed '/word/d'`"],
                        ["Print lines 2 to 3", "`sed -n '2,3p'`"],
                        ["Make two replacements", "`sed -e 's/a/b/' -e 's/c/d/'`"],
                        ["Edit the file in place (macOS)", "`sed -i '' 's/old/new/' file`"],
                        ["Edit the file in place (GNU and Linux)", "`sed -i 's/old/new/' file`"],
                    ]),
                    ("xargs and jq", "Feed lines to commands, and read JSON.", ["Task", "Type"], [
                        ["Run a command once per argument", "`xargs -n 1 cmd`"],
                        ["Put each line in the middle of a command", "`xargs -I {} cmd {}`"],
                        ["Handle names with spaces", "`fd -0 | xargs -0 cmd`"],
                        ["Run up to four jobs at once", "`xargs -n 1 -P 4 cmd`"],
                        ["Read field b of a without quotes", "`jq -r '.a.b'`"],
                        ["Count the items", "`jq '.items | length'`"],
                        ["Keep items where n is over 3", "`jq '.[] | select(.n > 3)'`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Rename files that have spaces",
                "frame": "Two files have spaces in their names, and scripts keep choking on them.",
                "open": "cd /tmp/tw/xf",
                "steps": [
                    (None, "`for f in *\\ *; do echo mv \"'$f'\" \"'${f// /_}'\"; done`", "Prints the two `mv` commands. Check them."),
                    (None, "`for f in *\\ *; do mv \"$f\" \"${f// /_}\"; done`", "Runs them: drop the `echo`."),
                    (None, "`printf '%s\\n' *.txt`", "Lists the `.txt` files to confirm."),
                ],
                "before": "my first file.txt\nold notes.txt",
                "after": "my_first_file.txt\nold_notes.txt",
                "meaning": "Print the command first, then drop the `echo`. A mistake costs one line of output, not your files.",
            },
            "practice": {
                "h2": "Practice: transform text",
                "qs": [
                    ("Mechanism", "`fd -e txt | xargs wc -c` fails on `my first file.txt`. Why?",
                     "How does xargs split its input?",
                     ["xargs splits on spaces and newlines.", "`my first file.txt` becomes three arguments."],
                     "Use `fd -e txt -0 | xargs -0 wc -c`. The null byte never appears in a name."),
                    ("Keystrokes", "Which command prints lines 2 and 3 of `notes.txt`?",
                     "-n and p.",
                     ["`-n` stops sed from printing every line.", "`2,3p` prints lines 2 to 3."],
                     "`sed -n '2,3p' notes.txt` prints `hello bash` and `bye world`."),
                    ("Application", "Add up the pay column of `pay.csv`, skipping the header.",
                     "awk with NR and END.",
                     ["`-F,` splits on commas.", "`NR > 1` skips the header.", "`END` prints the sum after the last line."],
                     "`awk -F, 'NR > 1 {sum += $3} END {print sum}' pay.csv` prints `12200`."),
                    ("Common mistake", "`sed -i 's/hello/hi/' edit.txt` fails on a Mac with `invalid command code`. What changes?",
                     "BSD sed wants a value after -i.",
                     ["On macOS, `-i` takes a backup suffix.", "Pass an empty one: `''`."],
                     "`sed -i '' 's/hello/hi/' edit.txt`. On Linux, drop the `''`."),
                ],
            },
        },
    ],
}
