"""Module 9: Find and text tools. Source: commands run on macOS (fd, find, mdfind, rg, grep, cut, sort, uniq, awk, sed, xargs, jq); no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


MODULE = {
    "n": 9,
    "folder": "m9-find-text",
    "title": "Find files, search text and change output",
    "footer": "Find files, search text, sort and count lines, replace words and read JSON; see the output of each command.",
    "tagline": "Find a file, search for a word, and change command output with short pipelines.",
    "glossary": [],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Find files by name, size or date on your Mac",
            "subtitle": "Find a file by name, find big files, find files changed before or after a date, see the biggest folders",
            "idea": (
                "Find files in a folder with fd or find; search the whole Mac with mdfind.",
                [
                    ("Find a file by part of its name", "fd report", "Find only PDF files: add -e pdf."),
                    ("Find files bigger than 100 MB", "fd -S +100m", "Find the same size with find: use -size +100M."),
                    ("Find a file anywhere on your Mac", "mdfind -name report", "Search only Documents: add -onlyin ~/Documents."),
                    ("See which folders use the most space", "du -sh * | sort -h", "Read the last line for the biggest entry."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I find a file when I know it exists but cannot remember the folder? Opening and scrolling through folders takes time.",
                "fix": "Find the file by its name, extension, size or date. Search a folder and its subfolders with `fd` or `find`. Search the whole Mac at once with `mdfind`.",
            },
            "drills": [
                {
                    "h2": "Find a file by part of its name (fd)",
                    "intro": "Find a file below the current folder: give `fd` part of its name. Use the practice files in `/tmp/tw/find`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for finding files", "code": C('''
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
                        {"type": "text", "body": "Create the same practice files on Linux: give `dd` a capital M in `bs=1M`. Keep the rest of the setup the same."},
                        {"type": "cmd", "where": "shell", "title": "Find files by part of the name", "code": C('''
fd app
'''),
                         "expect": "`src/app.py` and `src/test_app.py`. Both names contain `app`."},
                        {"type": "cmd", "where": "shell", "title": "Find every file of one type (.md or .py)", "code": C('''
fd -e md
fd -e py
'''),
                         "expect": "`docs/Notes.md` first. Then `src/app.py` and `src/test_app.py`."},
                        {"type": "cmd", "where": "shell", "title": "Find only folders or only files", "code": C('''
fd -t d
fd -t f log
'''),
                         "expect": "`-t d` prints the folders `docs/` and `src/`. `-t f log` prints the file `run.log`."},
                        {"type": "cmd", "where": "shell", "title": "Find hidden files that fd skips", "code": C('''
fd env
fd -H env
'''),
                         "expect": "The first command prints nothing, because fd skips hidden files and folders. The second prints `.cfg/.env`."},
                        {"type": "cmd", "where": "shell", "title": "Skip a folder when you search", "code": C('''
fd -e txt -E docs
'''),
                         "expect": "`my file.txt` and `old.txt`. `docs/todo.txt` is skipped."},
                        {"type": "text", "body": "Find files excluded by `.gitignore`: add `-I`, because fd skips them too. Find hidden and ignored files together with `-u`."},
                    ],
                },
                {
                    "h2": "Find files by size or when they last changed (fd)",
                    "intro": "Find files by size or when they changed: add a filter to the same command. Give sizes in `k`, `m`, `g` and times in `d`, `h`, `min`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 MB", "code": C('''
fd -S +100m
'''),
                         "expect": "`big.bin`. It is the only file over 100 MB."},
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 KB", "code": C('''
fd -t f -S +100k
'''),
                         "expect": "`big.bin` and `docs/data.bin`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Find files last changed more than one day ago", "code": C('''
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
                    "h2": "Find files on a Mac or Linux server without fd",
                    "intro": "Find files when fd is not installed: use `find`, available on every Mac and Linux machine. Give it a starting folder (`.`) and put patterns in quotes.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find a file by name with find", "code": C('''
find . -name "*.py"
find . -iname "notes*"
'''),
                         "expect": "`./src/app.py` and `./src/test_app.py`. Then `./docs/Notes.md`: `-iname` ignores case, so `notes*` matches `Notes.md`."},
                        {"type": "cmd", "where": "shell", "title": "Find folders or list files without searching subfolders", "code": C('''
find . -type d
find . -maxdepth 1 -type f
'''),
                         "expect": "`-type d` prints `.`, `./.cfg`, `./docs` and `./src`. `-maxdepth 1 -type f` prints the four files in this folder: `./big.bin`, `./my file.txt`, `./old.txt` and `./run.log`. The order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Find files bigger than 100 MB with find", "code": C('''
find . -type f -size +100M
'''),
                         "expect": "`./big.bin`."},
                        {"type": "cmd", "where": "shell", "title": "Find files changed over 30 days ago or logs changed in the last day", "code": C('''
find . -type f -mmin +43200
find . -type f -mtime -1 -name "*.log"
'''),
                         "expect": "`./old.txt`: changed more than 43200 minutes (30 days) ago. Then `./run.log`: changed within the last day. `-mtime +30` rounds to whole days and would skip a file that is 30.5 days old, so `-mmin` matches fd."},
                        {"type": "cmd", "where": "shell", "title": "Run a command on every file find lists", "code": C('''
find . -name "*.log" -exec wc -l {} +
'''),
                         "expect": "`3 ./run.log`. The `+` hands many files to one `wc` call."},
                        {"type": "cmd", "where": "shell", "title": "Preview which files find would delete (dry run)", "code": C('''
find . -name "*.log" -print
'''),
                         "expect": "`./run.log`. Nothing is deleted. These are the files `-delete` would remove."},
                        {"type": "text", "body": "Check which files find will delete: run with `-print` first and read the list. `-delete` asks no questions and has no undo. Put `-delete` last because find checks each test in order."},
                        {"type": "code", "file": "shell", "title": "Delete files only after checking the preview", "code": C('''
find . -name "*.log" -print
find . -name "*.log" -delete
''')},
                        {"type": "cmd", "where": "shell", "title": "Find duplicate files (md5, sort, awk)", "code": C('''
mkdir -p /tmp/tw/dupes && cd /tmp/tw/dupes
echo 'same text' > a.txt
echo 'same text' > b.txt
echo 'other text' > c.txt
find . -type f -exec md5 -r {} + | sort
find . -type f -exec md5 -r {} + | sort | awk 'seen[$1]++ { print "duplicate:", $0 }'
'''),
                         "expect": "The first command prints one line per file: its md5 hash and its path. `./a.txt` and `./b.txt` share the hash `abcb64ed947cb225988f26378a31bba7`; `./c.txt` has `426e712f0524e4dee5de612f6520bf86`. The second command prints `duplicate: abcb64ed947cb225988f26378a31bba7 ./b.txt`: every copy after the first one for a hash. Files with the same content get the same hash, whatever their names. `md5 -r` is the macOS tool; on Linux use `md5sum`, or `shasum` on both."},
                    ],
                },
                {
                    "h2": "Find and pick a file by typing a few letters (fzf)",
                    "intro": "Pick a file from a searchable list: pipe `fd` output into `fzf`, type a few letters, then press Enter. Use letters from different parts of the name: `sapp` finds `src/app.py`. `fzf` can turn any list into a picker. Use the same practice files in `/tmp/tw/find`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Search a list of files and pick one (fuzzy find)", "code": C('''
fd -e py | fzf
'''),
                         "expect": "A list with `src/app.py` and `src/test_app.py` and a prompt `>`. Type `tes`: the list narrows to `src/test_app.py` and the counter reads `1/2`. Press Enter: fzf prints the pick, `src/test_app.py`, and exits. Esc leaves without printing."},
                        {"type": "cmd", "where": "shell", "title": "Find files with fzf in a script without opening the picker", "code": C('''
fd -t f | fzf --filter app
fd -t f | fzf --filter 'md$'
fd -t f | fzf --filter '^src !test'
'''),
                         "expect": "`src/app.py` and `src/test_app.py`: both names contain `app`. Then `docs/Notes.md`: `$` means the name ends there. Then `src/app.py`: `^` anchors the start and `!` drops the matches. `--filter` prints the matches and never opens the picker, so it works in scripts. The interactive picker takes the same query words."},
                        {"type": "cmd", "where": "shell", "title": "Preview a file while you pick it", "code": C('''
fd -t f | fzf --preview 'bat --color=always {}'
'''),
                         "expect": "The list sits on the left and the preview on the right. Type `app`: the list narrows to `src/app.py` and `src/test_app.py` (`2/9`). The preview of the highlighted file shows `File: src/app.py` and `1 │ print(\"hi\")`, with colors. `{}` stands for the highlighted line."},
                        {"type": "cmd", "where": "shell", "title": "Pick several files and open them in nvim", "code": C('''
nvim $(fd -e py | fzf -m)
'''),
                         "expect": "`-m` allows several picks. Move to a line and press `Tab` to mark it, mark a second one, then press Enter. nvim opens `src/app.py` and `src/test_app.py` as two buffers. The top bar shows `app.py` and `test_app.py`, and `:bn` jumps to the other file. With one pick, nvim opens that single file."},
                        {"type": "text", "body": "Open one picked file with spaces in its name: quote the pick as `nvim \"$(fzf)\"`. Unquoted file names split at spaces inside `$(...)`."},
                        {"type": "keys", "where": "fzf", "title": "Pick files, search command history and change folders with fzf keys", "rows": [
                            ("Ctrl-T", "Insert a picked file path at the cursor; use `ff` here because this key is unbound"),
                            ("Ctrl-R", "Find a previous command and paste it at the prompt"),
                            ("Alt-C", "Change to a picked folder; press Esc then c if Option types a letter"),
                            ("Tab", "Select or deselect the highlighted line and move down (with -m)"),
                            ("Enter", "Accept selected lines, or the highlighted line when none are selected"),
                            ("Esc", "Close the picker without choosing an item"),
                        ]},
                        {"type": "text", "body": "Find a file with `ff`, search text with `frg`, go up to a parent folder with `fcd`, or kill a process with `fkill`. Find these fzf helpers for this machine in module 1, page 3: Copy mode, the command line and fzf."},
                    ],
                },
                {
                    "h2": "Find files across your Mac with Spotlight (mdfind)",
                    "intro": "Search your Mac quickly with `mdfind`: it uses the Spotlight index. Find only files Spotlight has indexed; folders excluded in System Settings, new files awaiting indexing and `/tmp` are missing. Search your own folders with these commands; your results will differ.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find a file in Downloads by part of its name", "code": C('''
mdfind -name zshrc -onlyin ~/Downloads
'''),
                         "expect": "One full path for each file whose name contains `zshrc`, such as `/Users/you/Downloads/zshrc.sh`. `-onlyin` limits the search to one folder."},
                        {"type": "cmd", "where": "shell", "title": "Find Documents files with a word in the name or text", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Find large files over 500 MB in your home folder", "code": C('''
mdfind -onlyin ~ 'kMDItemFSSize > 500000000' | head -3
'''),
                         "expect": "Up to three full paths of files over 500 MB, often under `~/Library`. The size is in bytes."},
                        {"type": "cmd", "where": "shell", "title": "See which files and folders use the most disk space", "code": C('''
du -sh * | sort -h
du -sh * | sort -rh | head -3
'''),
                         "expect": "The first command lists `0B old.txt`, `4.0K my file.txt`, `4.0K run.log`, `8.0K src`, `204K docs` and `120M big.bin`, smallest first. Sizes can differ a little, and a file that was written twice may show more. The second prints the top three: `120M big.bin`, `204K docs`, `8.0K src`. `*` skips hidden names such as `.cfg`."},
                        {"type": "cmd", "where": "shell", "title": "Show the newest files first", "code": C('''
command ls -lt | head -4
'''),
                         "expect": "A `total` line, then the newest entries with sizes and dates. `big.bin` comes first here. `ls` is an alias for `eza` in this shell and `eza` reads `-t` differently, so `command ls` runs the real one."},
                        {"type": "cmd", "where": "shell", "title": "Find a file with this name opened last week (mdfind, find)", "code": C('''
mdfind -onlyin ~ 'kMDItemFSName == "*.pdf"c && kMDItemLastUsedDate >= $time.today(-7)' | head -3
find /tmp/tw/find -name "*.txt" -atime -7
'''),
                         "expect": "The first command prints up to three full paths of PDF files you opened in the last 7 days, and nothing if you opened none. `kMDItemFSName` is the file name, `*` is a wildcard and the trailing `c` ignores upper and lower case. Spotlight records an open when Finder or an app opens the file, not when `cat` reads it. The second command prints `/tmp/tw/find/my file.txt` and `/tmp/tw/find/docs/todo.txt` when you made the practice files within the last 7 days, and leaves out `old.txt`. The order can differ. `-atime -7` tests the last time a file was read, and macOS may not update that time on every read, so trust `mdfind` first."},
                        {"type": "cmd", "where": "shell", "title": "Find files created today (mdfind, find)", "code": C('''
mdfind -onlyin ~/Downloads 'kMDItemFSCreationDate >= $time.today' | head -3
find /tmp/tw/find -type f -newerBt "$(date +%Y-%m-%d)" | sort
'''),
                         "expect": "The first command prints up to three full paths of files in Downloads created since midnight, and nothing if there are none. `$time.today` is midnight today. The second command prints nine paths when you made the practice files today, from `/tmp/tw/find/.cfg/.env` to `/tmp/tw/find/src/test_app.py`, and leaves out `old.txt` because `touch -t` moved its creation time back to 2024. `-newerBt` compares the creation (birth) time on macOS. `-newerct` compares the change time instead, which `touch` and renames also update, so it lists `old.txt` too and is not a creation date."},
                    ],
                },
                {
                    "h2": "Make a shortcut (link) to a file",
                    "intro": "Make a second name that points to a file: `ln -s target linkname`. Opening the link opens the target.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Make a shortcut link to a file (ln -s)", "code": C('''
mkdir -p /tmp/tw/links && cd /tmp/tw/links
echo 'real file' > report.txt
ln -s report.txt latest.txt
command ls -l latest.txt
readlink latest.txt
cat latest.txt
'''),
                         "expect": "`ls -l` prints a line that starts with `l` (`lrwxr-xr-x`) and ends with `latest.txt -> report.txt`; the arrow shows where the link points. Owner and date differ. `readlink` prints `report.txt`. `cat` prints `real file`, the content of the target. Run `ln -s` a second time and it says `File exists`; add `-f` to replace the link."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose a command to find files by name, size or date",
                "cards": [
                    ("Choose how to find a file", "Match what you want to find to a command.", ["Find a file or folder", "Run this command"], [
                        ["Find a file here by part of its name", "`fd name`"],
                        ["Find a file by name on any Linux machine", "`find . -name \"*name*\"`"],
                        ["Find an indexed file by name with Spotlight", "`mdfind -name name`"],
                        ["Find an indexed file by a word inside it", "`mdfind -onlyin ~ word`"],
                        ["See the biggest folders here", "`du -sh * | sort -h`"],
                    ]),
                    ("Find files by size or last change", "Find the same files with fd or find using these filters.", ["Find matching files", "fd", "find"], [
                        ["Find files bigger than 100 MB", "`-S +100m`", "`-size +100M`"],
                        ["Find files changed in the last day", "`--changed-within 1d`", "`-mtime -1`"],
                        ["Find files not changed for 30 days", "`--changed-before 30d`", "`-mmin +43200`"],
                        ["Find files only", "`-t f`", "`-type f`"],
                        ["Find folders (directories) only", "`-t d`", "`-type d`"],
                    ]),
                    ("Check files before deleting them with find", "List the files, count them, then delete them, always in that order.", ["Check and delete files", "Run this command"], [
                        ["1. List the matches", "`find . -name \"*.log\" -print`"],
                        ["2. Count them", "`find . -name \"*.log\" -print | wc -l`"],
                        ["3. Delete them", "`find . -name \"*.log\" -delete`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find the files and folders taking up disk space",
                "frame": "Find the biggest file and folder when a folder uses too much space.",
                "open": "cd /tmp/tw/find",
                "steps": [
                    (None, "`fd -S +100m`", "Find every file over 100 MB: `big.bin`."),
                    (None, "`du -sh * | sort -rh | head -3`", "Show the three biggest files and folders, ranked by size. Sizes can differ a little."),
                    (None, "`fd -t f --changed-before 1d`", "Find files you have not changed since yesterday: `old.txt`."),
                ],
                "after": "120M\tbig.bin\n204K\tdocs\n8.0K\tsrc",
                "meaning": "Find what to clean up: check size, then age, with two short commands.",
            },
            "practice": {
                "h2": "Check how to find files and preview deletions",
                "qs": [
                    ("Mechanism", "Why does `fd env` find nothing when `.cfg/.env` exists?",
                     "Check which files fd skips unless you ask for them.",
                     ["Find hidden files by asking for them; fd skips them by default.", "Recognize hidden names by the leading dot in both `.cfg` and `.env`."],
                     "Find the hidden file with `fd -H env`: it prints `.cfg/.env`."),
                    ("Keystrokes", "How do I list regular files bigger than 100 MB with find?",
                     "Filter by both file type and size.",
                     ["Search the current folder with `find .`.", "Keep files only with `-type f`.", "Find files over 100 MB with `-size +100M`."],
                     "Find the large file with `find . -type f -size +100M`: it prints `./big.bin`."),
                    ("Application", "How do I count lines in every Markdown file below the current folder?",
                     "Find files by extension, then run a command on each match.",
                     ["Find Markdown files with `fd -e md`.", "Count each file's lines: `-x wc -l` runs `wc -l` on each one."],
                     "Count Markdown lines with `fd -e md -x wc -l`: it prints `1 ./docs/Notes.md`."),
                    ("Common mistake", "How should I have checked the files before `find . -name \"*.log\" -delete` deleted one I needed?",
                     "Check whether -delete asks first or keeps a copy.",
                     ["Expect immediate removal with `-delete`, without a prompt or undo.", "Preview the files: swap `-delete` for `-print` and read the list."],
                     "Preview files with `find . -name \"*.log\" -print` first. Replace `-print` with `-delete` only after checking the list."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Search for a word in every file (rg and grep)",
            "subtitle": "Find a word in a folder of files, filter command output, show lines around a match",
            "idea": (
                "Search files below the current folder with rg. Search named files or piped command output with grep.",
                [
                    ("Find a word in every file", "rg word", "Ignore upper and lower case with -i; rg matches case by default."),
                    ("List only files that contain a word", "rg -l word", "Count matches in each file with -c."),
                    ("Show lines before and after a match", "rg -C 2 word", "Show two lines on each side."),
                    ("Find a word in command output", "command | grep word", "Keep lines without the word with -v."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I find a word in hundreds of project files without opening each file? Opening them one by one takes too long.",
                "fix": "Search for the word with rg to see each file name, line number and matching line. Search fewer files by adding a file type, a glob or a flag.",
            },
            "drills": [
                {
                    "h2": "Find a word and its line number in files (rg)",
                    "intro": "Find matching lines in a terminal: rg shows the file name, then `line:text` for each match. Pipe rg into another command to get output without the headings.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for searching text", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Search for a word ignoring upper and lower case", "code": C('''
rg -i error
'''),
                         "expect": "Both files. `notes.md` with `3:- error budget review`, and `app.log` with `2:` (the `ERROR disk full` line) and `4:` (the `ERROR timeout` line). The file order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Find a whole word without matching part of another word", "code": C('''
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
                    "h2": "Search only certain file types or skip files (rg)",
                    "intro": "Search one file type with `-t`, or match file names with a glob using `-g`. Exclude files by putting `!` before the glob.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Search only Python files", "code": C('''
rg -t py load
'''),
                         "expect": "`main.py`, then `2:def load(path):` and `5:print(load(\"app.log\"))`."},
                        {"type": "cmd", "where": "shell", "title": "Search only .log files with a file-name pattern (glob)", "code": C('''
rg -g '*.log' ERROR
'''),
                         "expect": "`app.log` with its two `ERROR` lines, 2 and 4."},
                        {"type": "cmd", "where": "shell", "title": "Search files while excluding Markdown files", "code": C('''
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
                    "h2": "Show nearby lines and search text or patterns (rg)",
                    "intro": "Search text containing special characters with `-F`. Search several words with `-e`. Put every regex in quotes.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show the lines around a match", "code": C('''
rg -C 1 timeout
'''),
                         "expect": "`app.log`, then line 3 (`WARN slow query`) with a `-`, line 4 (the `ERROR timeout` line) with a `:`, and line 5 (`INFO done`) with a `-`. A `:` marks the match and a `-` marks the context."},
                        {"type": "cmd", "where": "shell", "title": "Search for literal text containing special characters", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Show only matching text instead of the whole line", "code": C('''
rg -o 'host=\\w+'
'''),
                         "expect": "`app.log`, then `4:host=db1`. `-o` prints the match and not the whole line."},
                    ],
                },
                {
                    "h2": "Find words in files or folders with grep",
                    "intro": "Search on any Linux machine or Mac with `grep`. Give it file names or pipe in command output to search.",
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
                    "h2": "Find a word in any command's output (grep)",
                    "intro": "Keep output lines containing a word: put `| grep word` after any command. Add another grep to narrow the results further.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Show command output lines containing one word or both words", "code": C('''
cat app.log | grep ERROR
cat app.log | grep ERROR | grep timeout
'''),
                         "expect": "The two `ERROR` lines. Then only the `ERROR timeout host=db1` line."},
                        {"type": "cmd", "where": "shell", "title": "Search rg results for another word with grep", "code": C('''
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
                "h2": "Choose flags to find words, files and matching lines",
                "cards": [
                    ("Find the same text with rg or grep", "Use the same flag letter for most searches in either tool.", ["Find matching text", "rg", "grep"], [
                        ["Search a folder", "`rg word`", "`grep -r word .`"],
                        ["Ignore upper and lower case", "`-i`", "`-i`"],
                        ["Match whole words only", "`-w`", "`-w`"],
                        ["Show line numbers", "`-n` (already on in a terminal)", "`-n`"],
                        ["List matching file names only", "`-l`", "`-l`"],
                        ["Count matching lines", "`-c`", "`-c`"],
                        ["Skip matching lines", "`-v`", "`-v`"],
                        ["Show lines before and after a match", "`-C 2`", "`-C 2`"],
                        ["Search for several patterns", "`-e a -e b`", "`-E 'a|b'`"],
                        ["Print only the matching text", "`-o`", "`-o`"],
                        ["Search plain text without regex", "`-F`", "`-F`"],
                    ]),
                    ("Choose which files rg searches", "Include skipped files when needed; rg skips hidden, git-ignored and binary files by default.", ["Choose files to search", "Run this command"], [
                        ["Search Python files only", "`rg -t py word`"],
                        ["Search files that match a glob", "`rg -g '*.log' word`"],
                        ["Search everything except Markdown", "`rg -g '!*.md' word`"],
                        ["Search hidden files too", "`rg --hidden word`"],
                        ["Search git-ignored files too", "`rg -u word`"],
                        ["Search hidden and git-ignored files too", "`rg -uu word`"],
                        ["Find a file by name", "`rg --files | rg name`"],
                    ]),
                    ("Find words in command output", "Search output from any command by piping it into grep.", ["Find matching output lines", "Run this command"], [
                        ["List processes that mention nginx", "`ps aux | grep nginx`"],
                        ["Show ERROR lines without the word disk", "`cat app.log | grep ERROR | grep -v disk`"],
                        ["Keep rg matches containing another word too", "`rg -n word | grep other`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find a timeout in a log and see what happened around it",
                "frame": "Find which error log contains a timeout and see the nearby events.",
                "open": "cd /tmp/tw/grep",
                "steps": [
                    (None, "`rg -l ERROR`", "Find file names containing an error: `app.log`."),
                    (None, "`rg -c ERROR`", "Count the error lines: `app.log:2`."),
                    (None, "`rg -C 1 timeout`", "Show the timeout with one line before and after it."),
                ],
                "after": "app.log\n3-2026-10-14 10:02:11 WARN  slow query ms=950\n4:2026-10-14 10:03:40 ERROR timeout host=db1\n5-2026-10-14 10:04:00 INFO  done worker=1",
                "meaning": "Find the file names, count the matches, then show the lines around the match you need.",
            },
            "practice": {
                "h2": "Check how to find words and show nearby lines",
                "qs": [
                    ("Mechanism", "Why does `rg error` find only `notes.md` and skip the ERROR lines in `app.log`?",
                     "Check whether rg matches upper and lower case.",
                     ["Match letter case when searching with rg by default.", "Compare the lower-case pattern with the capital `ERROR` in `app.log`."],
                     "Find both files regardless of case: add `-i` to run `rg -i error`."),
                    ("Keystrokes", "How do I list only file names containing ERROR?",
                     "List file names with the lower-case L flag.",
                     ["Start the search with `rg`.", "List file names by adding `-l`.", "Search for the word by adding it."],
                     "List matching files with `rg -l ERROR`: it prints `app.log`."),
                    ("Application", "How do I show the `timeout` line with one line before and after it?",
                     "Show context with the C flag.",
                     ["Show lines on both sides with `-C`.", "Show one line on each side by giving it `1`."],
                     "Show the nearby lines with `rg -C 1 timeout`: it prints lines 3, 4 and 5 of `app.log`."),
                    ("Common mistake", "Why does `grep ERROR .` print `grep: .: Is a directory`, and which flag fixes it?",
                     "Search folders by telling grep to walk them; it reads files otherwise.",
                     ["Recognize `.` as a folder; grep skips folders by default.", "Search inside the folder with `-r`.", "Show line numbers with `-n`."],
                     "Search the folder with `grep -rn ERROR .`: each match looks like `./app.log:2:...`. Use plain `-r` for output without line numbers."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Get columns, sort lines and count repeated values",
            "subtitle": "Get a column from a file, sort numbers, count repeated lines, change characters, line up output",
            "idea": (
                "Get columns, sort lines and count values by joining tools with |. Each tool does one small job and passes its output to the next.",
                [
                    ("Get one column from a file", "cut -d' ' -f1 access.log", "Choose the separator with -d and the column with -f."),
                    ("Count how many times each line appears", "sort | uniq -c", "Count repeated lines after sorting them."),
                    ("Show the 5 most common lines", "sort | uniq -c | sort -rn | head -5", "Read the first line for the most common value."),
                    ("Count the lines in a file", "wc -l file", "Count words with -w and bytes with -c."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I get a column, rank values or count rows in a long log or CSV without a spreadsheet? A spreadsheet is too much for this job.",
                "fix": "Get the column with `cut`, put it in order with `sort`, count repeats with `uniq -c`, and keep the top results with `head`. Build the pipeline one tool at a time and see the result of each step.",
            },
            "drills": [
                {
                    "h2": "Get columns or characters from each line (cut)",
                    "intro": "Get a column from each line with `cut`. Use the practice files in `/tmp/tw/cols`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for sorting and counting", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Get the first column of a space-separated file", "code": C('''
cut -d' ' -f1 access.log
'''),
                         "expect": "The first column of each line: `10.0.0.1`, `10.0.0.2`, `10.0.0.1`, `10.0.0.3`, `10.0.0.1`, `10.0.0.2`. `-d' '` splits on spaces and `-f1` keeps field 1."},
                        {"type": "cmd", "where": "shell", "title": "Get columns 1 and 3 from a CSV file", "code": C('''
cut -d, -f1,3 users.csv
'''),
                         "expect": "`name,age`, `ana,31`, `ben,28`, `cleo,35`, `dan,28`. Fields 1 and 3, split on commas."},
                        {"type": "cmd", "where": "shell", "title": "Get the first 8 characters of every line", "code": C('''
cut -c1-8 access.log
'''),
                         "expect": "The first 8 characters of each line: `10.0.0.1`, `10.0.0.2`, `10.0.0.1`, `10.0.0.3`, `10.0.0.1`, `10.0.0.2`."},
                    ],
                },
                {
                    "h2": "Sort text, numbers, file sizes or CSV columns",
                    "intro": "Sort numbers by value with `-n` and sizes such as `2M` with `-h`. Plain `sort` compares text, putting `100` before `9`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Sort numbers in numeric order", "code": C('''
printf '10\\n9\\n100\\n' | sort
printf '10\\n9\\n100\\n' | sort -n
'''),
                         "expect": "The first prints `10`, `100`, `9`. The second prints `9`, `10`, `100`."},
                        {"type": "cmd", "where": "shell", "title": "Sort lines in reverse order or remove duplicates", "code": C('''
printf 'b\\na\\nb\\n' | sort -r
printf 'b\\na\\nb\\n' | sort -u
'''),
                         "expect": "`-r` prints `b`, `b`, `a`. `-u` prints `a`, `b`."},
                        {"type": "cmd", "where": "shell", "title": "Sort sizes such as 1K and 2M", "code": C('''
printf '1K\\n2M\\n500\\n' | sort -h
'''),
                         "expect": "`500`, `1K`, `2M`."},
                        {"type": "cmd", "where": "shell", "title": "Sort CSV rows by age or team and skip the header", "code": C('''
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
                    "h2": "Count repeated lines and show the most common values",
                    "intro": "Count repeats after sorting: `uniq` compares only neighbouring lines. Use the last recipe to rank the most common values.",
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
                    "h2": "Change letters, remove characters and join lines (tr)",
                    "intro": "Replace or remove individual characters with `tr`. Feed it standard input through a pipe or `< file`; it takes no file name argument.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Change text to upper case", "code": C('''
echo "Hello World" | tr 'a-z' 'A-Z'
'''),
                         "expect": "`HELLO WORLD`."},
                        {"type": "cmd", "where": "shell", "title": "Delete a character from text", "code": C('''
echo "Hello World" | tr -d 'l'
'''),
                         "expect": "`Heo Word`."},
                        {"type": "cmd", "where": "shell", "title": "Replace multiple spaces with one space", "code": C('''
echo "a    b     c" | tr -s ' '
'''),
                         "expect": "`a b c`."},
                        {"type": "cmd", "where": "shell", "title": "Turn lines into one comma-separated line", "code": C('''
cut -d' ' -f1 access.log | sort -u | tr '\\n' ','
'''),
                         "expect": "`10.0.0.1,10.0.0.2,10.0.0.3,` on one line, with a trailing comma and no newline, so the next prompt follows on the same line."},
                        {"type": "cmd", "where": "shell", "title": "Split a comma-separated line into separate lines", "code": C('''
echo "a,b,c" | tr ',' '\\n'
'''),
                         "expect": "`a`, `b` and `c`, one per line."},
                    ],
                },
                {
                    "h2": "Show file lines, align columns and save command output",
                    "intro": "Show the first or last lines with `head` and `tail`. Align columns with `column -t`. Join files side by side with `paste`. Save a copy of output within a pipeline with `tee`.",
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
                        {"type": "cmd", "where": "shell", "title": "Save command output to a file and pass it to the next command", "code": C('''
cut -d' ' -f1 access.log | sort -u | tee ips.txt | wc -l
cat ips.txt
'''),
                         "expect": "`3`, the number of different IPs. Then `ips.txt` holds `10.0.0.1`, `10.0.0.2`, `10.0.0.3`."},
                        {"type": "cmd", "where": "shell", "title": "Watch new log lines appear as a file changes", "code": C('''
cp access.log live.log
tail -n 2 -f live.log
'''),
                         "expect": "The last 2 lines of `live.log`, then the command waits. In a second pane run `echo \"10.0.0.9 GET /new 200 1\" >> live.log`: the new line appears at once. Press `Ctrl-c` to stop."},
                    ],
                },
                {
                    "h2": "Compare two files: find lines in only one and see what changed (comm, join, diff)",
                    "intro": "Compare two lists with `comm`; both lists must be sorted first. Match rows of two files by a shared first column with `join`. See what changed between two versions with `diff`. Use the practice files in `/tmp/tw/cols`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create two lists and two file versions to compare", "code": C('''
cd /tmp/tw/cols
printf 'ana\\nben\\ncleo\\ndan\\n' > team-a.txt
printf 'ben\\ndan\\neve\\nfay\\n' > team-b.txt
printf 'one\\ntwo\\nthree\\n' > v1.txt
printf 'one\\n2\\nthree\\nfour\\n' > v2.txt
wc -l team-a.txt team-b.txt v1.txt v2.txt
'''),
                         "expect": "`4 team-a.txt`, `4 team-b.txt`, `3 v1.txt`, `4 v2.txt` and `15 total`."},
                        {"type": "cmd", "where": "shell", "title": "Find lines that are in one file but not the other", "code": C('''
comm -23 team-a.txt team-b.txt
comm -13 team-a.txt team-b.txt
'''),
                         "expect": "The first prints the lines only in `team-a.txt`: `ana` and `cleo`. The second prints the lines only in `team-b.txt`: `eve` and `fay`. `-1` hides the lines only in file 1, `-2` hides the lines only in file 2 and `-3` hides the lines in both."},
                        {"type": "cmd", "where": "shell", "title": "Find lines that are in both files", "code": C('''
comm -12 team-a.txt team-b.txt
'''),
                         "expect": "`ben` and `dan`, the two names in both lists."},
                        {"type": "cmd", "where": "shell", "title": "Compare two lists that are not sorted", "code": C('''
printf 'dan\\nana\\nben\\n' > late.txt
printf 'ben\\neve\\nana\\n' > early.txt
comm -12 <(sort late.txt) <(sort early.txt)
'''),
                         "expect": "`ana` and `ben`. `<(sort file)` hands `comm` a sorted copy of each list. `comm` on unsorted input gives wrong results."},
                        {"type": "cmd", "where": "shell", "title": "Match rows of two files by a shared ID (join)", "code": C('''
printf '1,ana\\n2,ben\\n3,cleo\\n' > who.csv
printf '1,ops\\n3,dev\\n4,hr\\n' > where.csv
join -t, who.csv where.csv
join -t, -v1 who.csv where.csv
'''),
                         "expect": "The first prints the rows whose first column is in both files: `1,ana,ops` and `3,cleo,dev`. The second adds `-v1` and prints the rows only in the first file: `2,ben`. Both files must be sorted on the first column."},
                        {"type": "cmd", "where": "shell", "title": "See what changed between two files (diff)", "code": C('''
diff v1.txt v2.txt
'''),
                         "expect": "`2c2`, `< two`, `---`, `> 2`, `3a4` and `> four`. `<` marks a line from the first file and `>` a line from the second. `2c2` means line 2 changed; `3a4` means a line was added after line 3. `diff` prints nothing when the files are the same."},
                        {"type": "cmd", "where": "shell", "title": "See what changed with context, like a git diff (diff -u)", "code": C('''
diff -u v1.txt v2.txt | tail -n +3
'''),
                         "expect": "`@@ -1,3 +1,4 @@`, ` one`, `-two`, `+2`, ` three` and `+four`. `-` marks a removed line and `+` an added line. `tail -n +3` drops the two header lines that show each file's name and change time."},
                    ],
                },
                {
                    "h2": "Number lines, reverse text, wrap long lines and split a big file (nl, rev, fold, split)",
                    "intro": "Number lines with `nl` or `cat -n`. Reverse the characters of a line with `rev`. Wrap long lines with `fold` and cut a big file into parts with `split`. Use the practice files in `/tmp/tw/cols`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Number the lines of a file", "code": C('''
nl users.csv
cat -n users.csv
'''),
                         "expect": "Both print the same five lines with a number in front: `1 name,team,age`, `2 ana,ops,31`, `3 ben,dev,28`, `4 cleo,dev,35`, `5 dan,ops,28`. `nl` leaves blank lines unnumbered; `cat -n` numbers them."},
                        {"type": "cmd", "where": "shell", "title": "Reverse the characters on a line (rev)", "code": C('''
echo "hello" | rev
'''),
                         "expect": "`olleh`."},
                        {"type": "cmd", "where": "shell", "title": "Reverse the order of the lines in a file (tail -r)", "code": C('''
tail -r users.csv
'''),
                         "expect": "The lines in reverse order: `dan,ops,28`, `cleo,dev,35`, `ben,dev,28`, `ana,ops,31`, `name,team,age`."},
                        {"type": "text", "body": "Reverse the order of the lines on Linux with `tac users.csv`. macOS has no `tac`, and GNU `tail` on Linux has no `-r`."},
                        {"type": "cmd", "where": "shell", "title": "Wrap long lines at a fixed width (fold)", "code": C('''
echo abcdefghijklmnopqrstuvwxyz | fold -w 10
echo "the quick brown fox jumps over the lazy dog" | fold -s -w 15
'''),
                         "expect": "The first prints `abcdefghij`, `klmnopqrst` and `uvwxyz`: the line breaks after 10 characters, even inside a word. The second adds `-s` to break at spaces and prints `the quick`, `brown fox`, `jumps over the` and `lazy dog`."},
                        {"type": "cmd", "where": "shell", "title": "Break a big file into smaller files (split)", "code": C('''
split -l 2 access.log part-
wc -l part-*
'''),
                         "expect": "`2 part-aa`, `2 part-ab`, `2 part-ac` and `6 total`. `-l 2` puts 2 lines in each file and `part-` is the start of each file name."},
                    ],
                },
                {
                    "h2": "Save output and still see it, or read a long file page by page (tee, less)",
                    "intro": "Write output to a file and see it on screen with `tee`. Read a file longer than the screen with `less`. Use the practice files in `/tmp/tw/cols`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Save output to a file and still see it", "code": C('''
echo "first" | tee out.txt
'''),
                         "expect": "`first` on screen, and `out.txt` now holds the same line."},
                        {"type": "cmd", "where": "shell", "title": "Add output to the end of a file instead of overwriting it (tee -a)", "code": C('''
echo "second" | tee -a out.txt
cat out.txt
'''),
                         "expect": "`second` from `tee`, then `cat` shows both lines: `first` and `second`. Without `-a`, `tee` replaces the file."},
                        {"type": "keys", "where": "shell", "title": "Read a huge file page by page and search in it (less)", "rows": [
                            ("less access.log", "Open the file and read it one screen at a time"),
                            ("Space", "Show the next page"),
                            ("b", "Show the previous page"),
                            ("/word", "Search forward for a word"),
                            ("n", "Jump to the next match"),
                            ("N", "Jump to the previous match"),
                            ("G", "Jump to the end of the file"),
                            ("g", "Jump back to the start of the file"),
                            ("F", "Follow new lines as they are added, like tail -f; press Ctrl-c to stop following"),
                            ("q", "Quit less and return to the prompt"),
                        ]},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose commands to get columns, sort and count lines",
                "cards": [
                    ("Get columns, sort lines and count repeats", "Choose flags for cut, sort and uniq to get the output you need.", ["Get and sort text", "Run this command"], [
                        ["Get column 2 from comma-separated text", "`cut -d, -f2`"],
                        ["Get the first 8 characters of each line", "`cut -c1-8`"],
                        ["Sort numbers by value", "`sort -n`"],
                        ["Sort in reverse order", "`sort -r`"],
                        ["Sort sizes such as 500, 1K and 2M by size", "`sort -h`"],
                        ["Sort and keep each line once", "`sort -u`"],
                        ["Sort a CSV by column 3", "`sort -t, -k3`"],
                        ["Count occurrences of each line after sorting", "`uniq -c`"],
                        ["Show only the lines that repeat", "`uniq -d`"],
                    ]),
                    ("Show the most common values in a column", "Count and rank repeated values. Choose another column or change the 5 to get a different number of results.", None, C('''
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head -5
''')),
                    ("Count text, change characters and show file lines", "Count with wc, change characters with tr, and keep first or last lines with head and tail.", ["Count or change text", "Run this command"], [
                        ["Count lines", "`wc -l file`"],
                        ["Count words", "`wc -w file`"],
                        ["Count bytes", "`wc -c file`"],
                        ["Change text to upper case", "`tr 'a-z' 'A-Z'`"],
                        ["Remove a character from text", "`tr -d 'l'`"],
                        ["Replace repeated characters with one", "`tr -s ' '`"],
                        ["Turn newlines into commas", "`tr '\\n' ','`"],
                        ["Show the first or last 3 lines", "`head -n 3` or `tail -n 3`"],
                        ["Skip the header line", "`tail -n +2`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Find which IP address makes the most requests",
                "frame": "Find the IP making the most requests in a web server log with one request per line.",
                "open": "cd /tmp/tw/cols",
                "steps": [
                    (None, "`cut -d' ' -f1 access.log`", "Get only the IP address column."),
                    (None, "`| sort`", "Put repeated IP addresses next to each other."),
                    (None, "`| uniq -c`", "Keep one line for each IP and count its occurrences."),
                    (None, "`| sort -rn | head -3`", "Show the three highest counts, largest first."),
                ],
                "after": "   3 10.0.0.1\n   2 10.0.0.2\n   1 10.0.0.3",
                "meaning": "Rank IP addresses, pages, error codes or words with the same four steps.",
            },
            "practice": {
                "h2": "Check how to count repeats and sort numbers",
                "qs": [
                    ("Mechanism", "Why does `uniq -c` give every IP a count of one when I skip `sort`?",
                     "Check which lines uniq compares.",
                     ["Combine identical lines with `uniq` only when they are next to each other.", "Find the same IP in several places when the input is unsorted."],
                     "Sort first: without `sort`, `cut -d' ' -f1 access.log | uniq -c` prints six lines, each counted as `1`."),
                    ("Keystrokes", "How do I find the most requested page in `access.log`?",
                     "Get column 3, count and rank repeats, then keep one line.",
                     ["Get the page with `cut -d' ' -f3 access.log`.", "Count requests for each page with `sort | uniq -c`.", "Keep the highest count with `sort -rn | head -1`."],
                     "Find the most requested page with `cut -d' ' -f3 access.log | sort | uniq -c | sort -rn | head -1`: it prints `3 /home`."),
                    ("Application", "How do I put unique IPs on one comma-separated line without a trailing comma?",
                     "Join lines with paste.",
                     ["List each IP once with `cut -d' ' -f1 access.log | sort -u`.", "Join lines with commas using `paste -sd, -`. Read piped input with the last `-`."],
                     "Join the unique IPs with `cut -d' ' -f1 access.log | sort -u | paste -sd, -`: it prints `10.0.0.1,10.0.0.2,10.0.0.3`."),
                    ("Common mistake", "Why does `sort` put `100` before `9`, and how do I sort by number?",
                     "Check how plain sort compares characters.",
                     ["Compare text with plain `sort`: `1` comes before `9`.", "Compare numbers by adding `-n`."],
                     "Sort numerically with `sort -n`: `9`, `10`, `100`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Replace text, total columns and read JSON",
            "subtitle": "Add up a column, replace words in a file, run a command on each input line, get a JSON field, chain commands for an answer",
            "idea": (
                "Get or change columns with awk, change text patterns with sed, turn lines into command arguments with xargs, and read JSON with jq.",
                [
                    ("Get one column from a file", "awk '{print $3}' file", "Read CSV columns by adding -F,."),
                    ("Replace text in a file", "sed -i '' 's/old/new/g' file", "Keep the empty '' on macOS."),
                    ("Run a command on every output line", "xargs", "Handle file names with spaces by adding -0."),
                    ("Get a field from JSON without quotes", "jq -r '.name' file.json", "Remove the quotes with -r."),
                ],
                None,
            ),
            "problem": {
                "fail": "How do I get one column, change a word or read one JSON field when the output is almost what I need?",
                "fix": "Work on columns with awk, text patterns with sed, or JSON with jq. Pass lines to another command with xargs. Choose the tool that fits the data.",
            },
            "drills": [
                {
                    "h2": "Get columns, filter rows and add up values (awk)",
                    "intro": "Read columns with `awk`: it splits each line into `$1`, `$2` and so on. Change the separator with `-F,`. Use the practice files in `/tmp/tw/xf`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for changing text and reading JSON", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Get selected columns from a log or CSV file", "code": C('''
awk '{print $3, $5}' access.log | head -2
awk -F, '{print $1, $3}' pay.csv
'''),
                         "expect": "`/home 512` and `/about 1024`. Then the name and pay of every row: `name pay`, `ana 3100`, `ben 2800`, `cleo 3500`, `dan 2800`."},
                        {"type": "cmd", "where": "shell", "title": "Find rows by pay, team or HTTP status code", "code": C('''
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
                        {"type": "cmd", "where": "shell", "title": "Count log rows for each IP address", "code": C('''
awk '{n[$1]++} END {for (k in n) print k, n[k]}' access.log | sort
'''),
                         "expect": "`10.0.0.1 3`, `10.0.0.2 2`, `10.0.0.3 1`. The `sort` fixes the order, because awk loops over keys in no set order."},
                        {"type": "cmd", "where": "shell", "title": "Count lines and columns or print the last column (NR and NF)", "code": C('''
awk 'END {print NR}' access.log
awk '{print NF}' access.log | head -1
awk '{print $NF}' access.log | head -2
'''),
                         "expect": "`6` lines. Then `5` fields on the first line. Then the last field of the first two lines: `512` and `1024`."},
                        {"type": "cmd", "where": "shell", "title": "Align output columns and show average pay to one decimal place", "code": C('''
awk '{printf "%-10s %s\\n", $1, $3}' access.log | head -3
awk -F, 'NR > 1 {sum += $3} END {printf "avg %.1f\\n", sum / (NR - 1)}' pay.csv
'''),
                         "expect": "Two aligned columns: `10.0.0.1   /home`, `10.0.0.2   /about`, `10.0.0.1   /home`. Then `avg 3050.0`."},
                    ],
                },
                {
                    "h2": "Replace words, remove lines and save file edits (sed)",
                    "intro": "Replace the first match on each line with `sed 's/old/new/'`. Replace every match by adding `g`. Save the changes only when you use `-i`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Replace a word in every line", "code": C('''
sed 's/hello/hi/' notes.txt
'''),
                         "expect": "`hi world`, `hi bash`, `bye world`. The file itself is unchanged."},
                        {"type": "cmd", "where": "shell", "title": "Replace every occurrence of a character on each line", "code": C('''
sed 's/o/0/g' notes.txt
'''),
                         "expect": "`hell0 w0rld`, `hell0 bash`, `bye w0rld`. Without the `g`, only the first `o` on each line changes."},
                        {"type": "cmd", "where": "shell", "title": "Delete a line by number or by pattern", "code": C('''
sed '2d' notes.txt
sed '/bye/d' notes.txt
'''),
                         "expect": "`2d` leaves `hello world` and `bye world`. `/bye/d` leaves `hello world` and `hello bash`."},
                        {"type": "cmd", "where": "shell", "title": "Show a range of lines, matching lines or the last line", "code": C('''
sed -n '2,3p' notes.txt
sed -n '/bash/p' notes.txt
sed -n '$p' notes.txt
'''),
                         "expect": "Lines 2 to 3: `hello bash` and `bye world`. Then the line with `bash`: `hello bash`. Then the last line: `bye world`. `-n` turns off the normal output, and `p` prints."},
                        {"type": "cmd", "where": "shell", "title": "Make several replacements at once", "code": C('''
sed -e 's/hello/hi/' -e 's/world/earth/' notes.txt
'''),
                         "expect": "`hi earth`, `hi bash`, `bye earth`."},
                        {"type": "cmd", "where": "shell", "title": "Replace text and save changes in the file on macOS", "code": C('''
cp notes.txt edit.txt
sed -i '' 's/hello/hi/' edit.txt
cat edit.txt
'''),
                         "expect": "`hi world`, `hi bash`, `bye world`. `edit.txt` itself changed. The `''` after `-i` is the backup suffix, empty here."},
                        {"type": "text", "body": "Fix `invalid command code` when saving sed changes on a Mac: include `''`. Use `sed -i 's/old/new/' file` without `''` with GNU sed on Linux."},
                        {"type": "cmd", "where": "shell", "title": "Add text at the start of every line", "code": C('''
sed 's/^/> /' notes.txt
'''),
                         "expect": "`> hello world`, `> hello bash`, `> bye world`."},
                        {"type": "cmd", "where": "shell", "title": "Swap the order of two words with regex groups", "code": C('''
sed -E 's/([a-z]+) ([a-z]+)/\\2 \\1/' notes.txt
'''),
                         "expect": "`world hello`, `bash hello`, `world bye`. `-E` turns on groups and `\\1`, `\\2` paste them back."},
                        {"type": "cmd", "where": "shell", "title": "Replace a word in every file of a folder from the shell (rg, xargs, sed)", "code": C('''
mkdir -p /tmp/tw/replace/sub && cd /tmp/tw/replace
echo 'colour red' > a.txt
echo 'dark colour' > "my notes.txt"
echo 'no match here' > b.txt
echo 'colour colour' > sub/c.txt
rg colour .
rg -l0 colour . | xargs -0 sed -i '' 's/colour/color/g'
rg colo .
'''),
                         "expect": "The first `rg` lists the three files that hold the old word: `./a.txt:colour red`, `./my notes.txt:dark colour` and `./sub/c.txt:colour colour`. The order can differ. The second `rg` shows the same lines with `color`: `./a.txt:color red`, `./my notes.txt:dark color`, `./sub/c.txt:color color`. `b.txt` is untouched because it never matched. `rg -l0` lists only the names of matching files, separated by NUL characters, and `xargs -0` keeps `my notes.txt` whole. On Linux drop the `''` after `-i`, or use `perl -pi -e 's/colour/color/g'` in place of `sed -i ''` on both."},
                    ],
                },
                {
                    "h2": "Edit a file in place the same way on Mac and Linux (perl)",
                    "intro": "Replace text in a file with `perl -pi -e`. It works the same on macOS and Linux, so you do not need the `''` that macOS `sed -i` requires. Use the practice files in `/tmp/tw/xf`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Edit a file in place the same way on Mac and Linux", "code": C('''
cp notes.txt perl.txt
perl -pi -e 's/hello/hi/g' perl.txt
cat perl.txt
'''),
                         "expect": "`hi world`, `hi bash`, `bye world`. `perl.txt` itself changed. `-p` prints every line, `-i` saves the result in the file and `-e` takes the command."},
                        {"type": "cmd", "where": "shell", "title": "Edit a file in place and keep a backup copy", "code": C('''
cp notes.txt keep.txt
perl -pi.bak -e 's/world/earth/g' keep.txt
cat keep.txt keep.txt.bak
'''),
                         "expect": "`keep.txt` now reads `hello earth`, `hello bash`, `bye earth`. The original is saved as `keep.txt.bak`: `hello world`, `hello bash`, `bye world`."},
                        {"type": "cmd", "where": "shell", "title": "Search a file or get a column with perl (grep and awk alternative)", "code": C('''
perl -ne 'print if /bash/' notes.txt
perl -ne 'print "$.: $_" if /world/' notes.txt
perl -lane 'print $F[2]' access.log | head -3
'''),
                         "expect": "The first prints the line with `bash`: `hello bash`. The second adds the line number: `1: hello world` and `3: bye world`. The third prints column 3 of the log: `/home`, `/about`, `/home`. `-n` reads each line without printing it, `$.` is the line number and `-a` splits the line into `@F`."},
                    ],
                },
                {
                    "h2": "Edit a file quickly without Neovim (nano) or from a script (ed)",
                    "intro": "Open a small file in `nano` for a quick edit; the shortcuts are listed at the bottom of its screen. Use `ed` to edit a file from a script, with no screen. Use the practice files in `/tmp/tw/xf`.",
                    "blocks": [
                        {"type": "keys", "where": "shell", "title": "Edit a file quickly without Neovim (nano)", "rows": [
                            ("nano notes.txt", "Open the file for editing"),
                            ("Ctrl-O", "Save the file; press Enter to keep the name"),
                            ("Ctrl-X", "Exit nano; it asks to save if you have unsaved changes"),
                            ("Ctrl-W", "Search for text in the file"),
                            ("Ctrl-K", "Cut the current line"),
                            ("Ctrl-U", "Paste the cut line"),
                        ]},
                        {"type": "cmd", "where": "shell", "title": "Edit a file from a script with ed", "code": C('''
cp notes.txt ed.txt
printf '%s\\n' '2s/bash/shell/' 'a' 'added line' '.' 'w' 'q' | ed -s ed.txt
cat ed.txt
'''),
                         "expect": "`hello world`, `hello shell`, `added line`, `bye world`. Each `printf` line is one `ed` command: `2s/bash/shell/` replaces text on line 2, `a` starts adding lines after it, `.` ends the new text, `w` saves and `q` quits. `-s` hides `ed` messages."},
                    ],
                },
                {
                    "h2": "Pass input lines to a command and run jobs in parallel (xargs)",
                    "intro": "Build a command from input lines with `xargs`. Pass file names containing spaces as a null-separated list and use `-0`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Run a command with one or two arguments at a time", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -n 1 echo item
printf 'a\\nb\\nc\\n' | xargs -n 2 echo
'''),
                         "expect": "`item a`, `item b`, `item c`. Then `a b` and `c`. `-n 1` gives each run one argument, and `-n 2` gives two."},
                        {"type": "cmd", "where": "shell", "title": "Put each line in the middle of a command", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -I {} echo file-{}.txt
'''),
                         "expect": "`file-a.txt`, `file-b.txt`, `file-c.txt`. `-I {}` marks where each line goes."},
                        {"type": "cmd", "where": "shell", "title": "Run up to three commands at once with xargs", "code": C('''
printf 'a\\nb\\nc\\n' | xargs -P 3 -I {} echo job {}
'''),
                         "expect": "`job a`, `job b` and `job c`. `-P 3` runs up to three at once, so the order can differ."},
                        {"type": "cmd", "where": "shell", "title": "Pass file names with spaces to xargs without splitting them", "code": C('''
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
                    "h2": "Get JSON fields, filter items and count them (jq)",
                    "intro": "Get a JSON value by giving `jq` a path such as `.users[0].name`. Go through a list with `.[]`. Pass results to the next step with `|` inside the quotes.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Format a JSON file with readable lines and indentation", "code": C('''
jq . users.json | head -8
'''),
                         "expect": "The JSON spread over lines with two-space indents: `{`, `\"users\": [`, `{`, `\"name\": \"ana\",`, `\"age\": 31,`, `\"team\": \"ops\"` and so on."},
                        {"type": "cmd", "where": "shell", "title": "Get names from JSON with or without quotes", "code": C('''
jq '.users[0].name' users.json
jq -r '.users[].name' users.json
'''),
                         "expect": "`\"ana\"` with quotes. Then the names without quotes, one per line: `ana`, `ben`, `cleo`. `-r` prints raw text."},
                        {"type": "cmd", "where": "shell", "title": "Count JSON items and list an object's field names", "code": C('''
jq '.users | length' users.json
jq '.users[0] | keys' users.json
'''),
                         "expect": "`3`. Then the keys of the first user, in order: `\"age\"`, `\"name\"`, `\"team\"`."},
                        {"type": "cmd", "where": "shell", "title": "Find JSON users by age or team", "code": C('''
jq '.users[] | select(.age > 30) | .name' users.json
jq -r '.users[] | select(.team == "dev") | "\\(.name) \\(.age)"' users.json
'''),
                         "expect": "`\"ana\"` and `\"cleo\"`, the users over 30. Then the dev team as text: `ben 28` and `cleo 35`."},
                        {"type": "cmd", "where": "shell", "title": "Join JSON names with commas or add up ages", "code": C('''
jq -r '.users | map(.name) | join(",")' users.json
jq '.users | map(.age) | add' users.json
'''),
                         "expect": "`ana,ben,cleo`. Then `94`, the sum of the ages."},
                    ],
                },
                {
                    "h2": "Find the busiest IPs, total log sizes and rename files",
                    "intro": "Answer these searches by joining the tools above in a pipeline. Build each pipeline one step at a time: run the first command, add a pipe, then run it again.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Find the 5 IP addresses with the most requests in a log", "code": C('''
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
'''),
                         "expect": "`3 10.0.0.1`, `2 10.0.0.2`, `1 10.0.0.3`. The log has only three IPs, so `head -5` shows all three."},
                        {"type": "cmd", "where": "shell", "title": "Add up the size of all .log files", "code": C('''
find . -name "*.log" -print0 | xargs -0 wc -c | tail -n 1
fd -e log -x stat -f %z | awk '{s += $1} END {print s " bytes"}'
'''),
                         "expect": "`4666 total`, then `4666 bytes`. On Linux, `stat -c %s` replaces `stat -f %z`."},
                        {"type": "cmd", "where": "shell", "title": "Preview file names before replacing spaces with underscores", "code": C('''
for f in *\\ *; do echo mv "'$f'" "'${f// /_}'"; done
'''),
                         "expect": "`mv 'my first file.txt' 'my_first_file.txt'` and `mv 'old notes.txt' 'old_notes.txt'`. Nothing is renamed: `echo` only prints the commands."},
                        {"type": "cmd", "where": "shell", "title": "Rename files by replacing spaces with underscores", "code": C('''
for f in *\\ *; do mv "$f" "${f// /_}"; done
printf '%s\\n' *.txt
'''),
                         "expect": "`edit.txt`, `my_first_file.txt`, `notes.txt` and `old_notes.txt`. The files with spaces are gone. The rename changed the sample files, so to redo this page use a fresh sample folder: change `xf` to `xf2` in the first block and run the page again."},
                    ],
                },
            ],
            "rules": {
                "h2": "Choose commands to change text, run jobs and read JSON",
                "cards": [
                    ("Get columns, filter rows and add totals with awk", "Choose columns, keep matching rows and add up values.", ["Get or count rows and columns", "Run this command"], [
                        ["Print column 1", "`awk '{print $1}'`"],
                        ["Print column 2 of a CSV", "`awk -F, '{print $2}'`"],
                        ["Print rows where column 3 is over 100", "`awk '$3 > 100'`"],
                        ["Add up column 2", "`awk '{s += $2} END {print s}'`"],
                        ["Count rows by column 1", "`awk '{n[$1]++} END {for (k in n) print k, n[k]}'`"],
                        ["Skip the first line", "`awk 'NR > 1'`"],
                        ["Count lines", "`awk 'END {print NR}'`"],
                    ]),
                    ("Replace words, delete lines and save edits with sed", "Replace text, remove lines or print the lines you need.", ["Change or show text", "Run this command"], [
                        ["Replace the first match on each line", "`sed 's/old/new/'`"],
                        ["Replace every match", "`sed 's/old/new/g'`"],
                        ["Delete line 2", "`sed '2d'`"],
                        ["Delete lines that contain a word", "`sed '/word/d'`"],
                        ["Print lines 2 to 3", "`sed -n '2,3p'`"],
                        ["Make two replacements", "`sed -e 's/a/b/' -e 's/c/d/'`"],
                        ["Save text changes in the file on macOS", "`sed -i '' 's/old/new/' file`"],
                        ["Save text changes in the file with GNU sed on Linux", "`sed -i 's/old/new/' file`"],
                    ]),
                    ("Run commands on input lines and get JSON values", "Pass lines to commands with xargs and read JSON with jq.", ["Run commands or read JSON", "Run this command"], [
                        ["Run a command once per argument", "`xargs -n 1 cmd`"],
                        ["Put each line in the middle of a command", "`xargs -I {} cmd {}`"],
                        ["Pass file names with spaces without splitting them", "`fd -0 | xargs -0 cmd`"],
                        ["Run up to four jobs at once", "`xargs -n 1 -P 4 cmd`"],
                        ["Get JSON field b inside a without quotes", "`jq -r '.a.b'`"],
                        ["Count JSON items", "`jq '.items | length'`"],
                        ["Keep JSON items where n is over 3", "`jq '.[] | select(.n > 3)'`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Replace spaces in file names with underscores",
                "frame": "Rename two files whose names contain spaces and keep causing scripts to fail.",
                "open": "cd /tmp/tw/xf",
                "steps": [
                    (None, "`for f in *\\ *; do echo mv \"'$f'\" \"'${f// /_}'\"; done`", "Preview the two `mv` commands and check them."),
                    (None, "`for f in *\\ *; do mv \"$f\" \"${f// /_}\"; done`", "Run the rename commands by dropping `echo`."),
                    (None, "`printf '%s\\n' *.txt`", "List the `.txt` files to check the new names."),
                ],
                "before": "my first file.txt\nold notes.txt",
                "after": "my_first_file.txt\nold_notes.txt",
                "meaning": "Check the printed command before dropping `echo` to run it. Catch a mistake in one line of output before it affects your files.",
            },
            "practice": {
                "h2": "Check how to pass file names, select lines and total columns",
                "qs": [
                    ("Mechanism", "Why does `fd -e txt | xargs wc -c` fail on `my first file.txt`?",
                     "Check how xargs splits input into arguments.",
                     ["Split input at spaces and newlines with xargs by default.", "See why the name breaks: `my first file.txt` becomes three arguments."],
                     "Keep file names intact with `fd -e txt -0 | xargs -0 wc -c`. A null byte never appears in a file name."),
                    ("Keystrokes", "How do I print only lines 2 and 3 of `notes.txt`?",
                     "Select the lines with -n and p.",
                     ["Stop sed from printing every line with `-n`.", "Print lines 2 to 3 with `2,3p`."],
                     "Show the selected lines with `sed -n '2,3p' notes.txt`: it prints `hello bash` and `bye world`."),
                    ("Application", "How do I add up the pay column of `pay.csv` without the header?",
                     "Skip the header and print the total with awk, NR and END.",
                     ["Split columns at commas with `-F,`.", "Skip the header with `NR > 1`.", "Print the sum after the last line with `END`."],
                     "Total the pay column with `awk -F, 'NR > 1 {sum += $3} END {print sum}' pay.csv`: it prints `12200`."),
                    ("Common mistake", "Why does `sed -i 's/hello/hi/' edit.txt` fail with `invalid command code` on a Mac?",
                     "Give BSD sed a value after -i.",
                     ["Supply the backup suffix required by `-i` on macOS.", "Use an empty suffix: `''`."],
                     "Save the edit on macOS with `sed -i '' 's/hello/hi/' edit.txt`. Drop the `''` on Linux."),
                ],
            },
        },
    ],
}
