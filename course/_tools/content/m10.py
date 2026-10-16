"""Module 10: Bash basics. Source: snippets run in /bin/bash 3.2 on macOS; no lesson file."""


def C(s):
    """Code blocks are written between newlines so a closing quote never touches a code quote."""
    return s.strip("\n")


BASH_FIRST = "Type `bash` first: these snippets are bash, and zsh splits words differently. Type `exit` to return to zsh."

MODULE = {
    "n": 10,
    "folder": "m10-bash-basics",
    "title": "Write Bash scripts with variables, loops and flags",
    "footer": "Quote variables, check exit codes, use if and case, loop over files and lines, read flags and typed answers",
    "tagline": "Save values, test conditions, loop over files and read script arguments in bash.",
    "glossary": [
        ("tw-exit-code", "Exit code", ["exit code", "exit codes"], "How do I tell if a command worked? Every command leaves a number: 0 means it worked, anything else means it failed. Read it with $?."),
        ("tw-shebang", "Shebang", ["shebang"], "Which program runs my script? The first line, such as #!/bin/bash, names it."),
        ("tw-word-splitting", "Word splitting", ["word splitting"], "Why does a $variable with spaces break my command? Bash cuts an unquoted $variable into words at every space, tab and newline (the IFS characters), then expands any * patterns. Quote it to keep it whole."),
    ],
    "coverage_allow": [],
    "pages": [
        # ============================================================ page 1
        {
            "h1": "Run a bash script, save values and check if a command worked",
            "subtitle": "Run a script file, save a value in a variable, quote a file name with spaces, check if a command worked",
            "idea": (
                "Make a script safe with spaces and check if a command worked: quote every variable and read $? after the command.",
                [
                    ("Run a script file", "bash hello.sh", "Or chmod +x it and run ./hello.sh."),
                    ("Save a value in a variable", "name=Ada", "No spaces around the equals sign."),
                    ("Use a value with spaces safely", "\"$name\"", "Double quotes keep spaces inside the value."),
                    ("Check if a command worked", "echo $?", "0 is success, anything else is a failure."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does my script work on `report.txt` but break on `my notes.txt`? Why does `name = Ada` say `command not found`?",
                "fix": "Fix both: write `name=Ada` with no spaces, and put `\"$name\"` in double quotes every time you use it.",
            },
            "drills": [
                {
                    "h2": "Run a script file (bash or ./)",
                    "intro": "Run a script file: type `bash` and the file name, or make the file executable and run it by path.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for running scripts", "code": C(r'''
mkdir -p /tmp/tw/vars && cd /tmp/tw/vars
cat > hello.sh <<'EOF'
#!/bin/bash
echo "Hello from a script"
EOF
printf 'first line\nsecond line\n' > 'my notes.txt'
cat hello.sh
'''),
                         "expect": "The two lines of the script print: `#!/bin/bash` and `echo \"Hello from a script\"`. The folder `/tmp/tw/vars` now holds `hello.sh` and `my notes.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Run a script with bash, or run it as ./hello.sh", "code": C(r'''
cd /tmp/tw/vars
bash hello.sh
chmod +x hello.sh
./hello.sh
'''),
                         "expect": "`Hello from a script` prints twice, once from `bash hello.sh` and once from `./hello.sh`. Without the `chmod +x`, `./hello.sh` fails with `Permission denied`."},
                        {"type": "text", "body": "Which program runs my script? The first line `#!/bin/bash` (the shebang) names it when you run `./hello.sh`. `bash hello.sh` ignores it."},
                    ],
                },
                {
                    "h2": "Save a value in a variable and quote it",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Save a value in a variable and print it", "code": C(r'''
name=Ada
echo "Hello, $name"
name = Ada
'''),
                         "expect": "`Hello, Ada` prints, then `bash: name: command not found`. With spaces, bash runs `name` as a command."},
                        {"type": "cmd", "where": "shell", "title": "Print a $variable's value, or print it literally", "code": C(r'''
name=Ada
echo "Hi $name"
echo 'Hi $name'
echo Hi $name
'''),
                         "expect": "Three lines: `Hi Ada`, `Hi $name`, `Hi Ada`. Single quotes print the text, double quotes and no quotes expand it."},
                        {"type": "cmd", "where": "shell", "title": "Stop a file name with a space from breaking my command", "code": C(r'''
cd /tmp/tw/vars
f='my notes.txt'
cat $f
cat "$f"
'''),
                         "expect": "`cat $f` fails twice: `cat: my: No such file or directory` and `cat: notes.txt: No such file or directory`. `cat \"$f\"` prints `first line` and `second line`."},
                        {"type": "cmd", "where": "shell", "title": "Add text right after a variable (${var})", "code": C(r'''
fruit=apple
echo "$fruits"
echo "${fruit}s"
'''),
                         "expect": "The first `echo` prints an empty line, because `$fruits` is a different, unset variable. The second prints `apples`."},
                    ],
                },
                {
                    "h2": "Save a command's output and do maths",
                    "intro": "Save what a command prints with `$(command)`. Do whole-number maths with `$(( ))`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Save what a command prints in a variable ($(...))", "code": C(r'''
cd /tmp/tw/vars
first=$(head -1 'my notes.txt')
echo "First line: $first"
echo "Lines: $(wc -l < 'my notes.txt' | tr -d ' ')"
'''),
                         "expect": "`First line: first line` and `Lines: 2`."},
                        {"type": "cmd", "where": "shell", "title": "Add, multiply and divide numbers ($(( )))", "code": C(r'''
a=7; b=3
echo $((a + b)) $((a * b)) $((a / b)) $((a % b))
((a++)); echo $a
echo "scale=2; 7/3" | bc
'''),
                         "expect": "Three lines: `10 21 2 1`, then `8`, then `2.33`. The integer sum, product, quotient and remainder come first, `((a++))` makes 7 into 8, and `bc` gives the decimals."},
                        {"type": "text", "body": "Why does 7 / 3 give 2? `$(( ))` drops the decimals: `7 / 3` is `2`. For decimals pipe the sum to `bc`."},
                        {"type": "cmd", "where": "shell", "title": "Print a tab, pad a number or round decimals (echo, printf)", "code": C(r'''
echo "a\tb"
printf 'a\tb\n'
printf '%s\n' one two three
printf '%05.2f\n' 3.14159
printf '%-6s|%4d\n' ab 7
'''),
                         "expect": "`echo` prints `a\\tb` with the backslash-t as typed. `printf` prints `a` and `b` with a real tab between them. Then `one`, `two`, `three` on separate lines, `03.14`, and `ab    |   7`."},
                    ],
                },
                {
                    "h2": "Check if a command worked (exit codes)",
                    "intro": "Check if the last command worked: every command leaves a number, `0` for success and anything else for failure. `$?` holds the last one.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check if the last command worked ($?)", "code": C(r'''
cd /tmp/tw/vars
ls hello.sh
echo $?
ls nope
echo $?
'''),
                         "expect": "`hello.sh` and `0`, then `ls: nope: No such file or directory` and `1`."},
                        {"type": "text", "body": "Is the exit code the same on Linux? No: GNU `ls` exits with `2` for a missing file where macOS `ls` exits with `1`. Only `0` versus not `0` is portable."},
                        {"type": "cmd", "where": "shell", "title": "End a script with your own exit code, and read true and false", "code": C(r'''
cd /tmp/tw/vars
true; echo $?
false; echo $?
cat > check.sh <<'EOF'
echo "checking"
exit 3
EOF
bash check.sh
echo $?
'''),
                         "expect": "`0` for `true`, `1` for `false`, then `checking` from the script and `3`, the code `exit 3` set."},
                    ],
                },
                {
                    "h2": "Go back to the previous folder, check free disk space and find what uses a port",
                    "intro": "Three everyday shell checks. They also run in zsh.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Go back to the previous folder with cd", "code": C('''
cd /tmp/tw
cd /usr
cd -
pwd
'''),
                         "expect": "`cd -` prints `/tmp/tw`, the folder it takes you back to, and `pwd` prints `/tmp/tw` again. Each `cd` remembers the folder you came from, so a second `cd -` jumps back to `/usr`."},
                        {"type": "cmd", "where": "shell", "title": "Show free disk space (df, du)", "code": C('''
df -h /
du -sh ~/Downloads
'''),
                         "expect": "`df -h /` prints a header (`Filesystem Size Used Avail Capacity ... Mounted on`) and one line for `/`, for example `/dev/disk3s1s1 926Gi 12Gi 350Gi 4%`. `Avail` is the space you can still use. `du -sh ~/Downloads` prints one total and the path, for example `1.3G` then a tab then the folder. Your numbers differ."},
                        {"type": "cmd", "where": "shell", "title": "Which process is using port 3000 (lsof)", "code": C('''
python3 -m http.server 3999 >/dev/null 2>&1 &
sleep 1
lsof -iTCP:3999 -sTCP:LISTEN
kill $(lsof -ti :3999)
'''),
                         "expect": "A job line such as `[1] 69538` from the background start. Then `lsof` prints a header (`COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME`) and one line like `python3.1 69538 you 4u IPv6 ... TCP *:3999 (LISTEN)`; the number under `PID` is the process that holds the port. The PID and the `python3` name differ. The last command stops that process with its PID; the shell may then print `Terminated`. Replace `3999` with your own port, such as `3000`, to find what holds it."},
                    ],
                },
            ],
            "rules": {
                "h2": "Look up how to quote variables, save output and check exit codes",
                "cards": [
                    ("Keep a variable's spaces, or let it split", "Why does an unquoted value break? Bash splits it at spaces, tabs and newlines (IFS), then expands `*` patterns. Quotes stop both.", ["What you want", "Type this"], [
                        ["Keep a value in one piece", "`\"$name\"`: one word, spaces kept. Use this by default."],
                        ["Print the text `$name` as typed", "`'$name'`: nothing expands."],
                        ["See what happens without quotes", "`$name`: split and pattern-expanded, so `my notes.txt` breaks."],
                        ["Add text right after a variable", "`\"${name}s\"`"],
                    ]),
                    ("Save a command's output or add numbers", "Which $ form do I use? Three look alike.", ["What you want", "Type this"], [
                        ["Use a variable's value", "`$name`"],
                        ["Save what a command prints", "`first=$(head -1 file)`"],
                        ["Add or multiply whole numbers", "`$((a + b))`"],
                    ]),
                    ("Check if a command worked", "How do I see if a command worked? Its result is a number.", ["What you want", "Type this"], [
                        ["Read the last command's result", "`echo $?`: 0 is success. Read it before running anything else."],
                        ["End a script with your own code", "`exit 3`"],
                        ["Make a command that always succeeds or fails", "`true` (code 0) or `false` (code 1)"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Count the lines in a file with a space in its name",
                "frame": "How do I print how many lines `my notes.txt` has, in one sentence?",
                "open": "cd /tmp/tw/vars",
                "steps": [
                    (None, "`file='my notes.txt'`", "Quote the name: the space stays inside the value."),
                    (None, "`n=$(wc -l < \"$file\" | tr -d ' ')`", "`wc -l` counts the lines. `tr -d ' '` removes the padding spaces macOS adds."),
                    (None, "`echo \"$file has $n lines\"`", "Double quotes keep the file name whole."),
                ],
                "after": "my notes.txt has 2 lines",
                "meaning": "Keep a file name with spaces whole: quote the variable and it stays one word.",
            },
            "practice": {
                "h2": "Check what you know: quote variables and read exit codes",
                "qs": [
                    ("Mechanism", "Why does `cat $f` fail when `f='my notes.txt'`, while `cat \"$f\"` works?",
                     "How many words does the command get?",
                     ["Without quotes bash cuts the value at the space.", "`cat` then gets two names, `my` and `notes.txt`.", "Quotes keep it as one name."],
                     "Unquoted `$f` splits into two words. `\"$f\"` stays one."),
                    ("Keystrokes", "How do I save today's year in `y` and print `Year: ...`?",
                     "Command substitution, then echo.",
                     ["Write `y=$(date +%Y)`.", "Write `echo \"Year: $y\"`."],
                     "`y=$(date +%Y)` then `echo \"Year: $y\"`."),
                    ("Application", "How do I make a script `fail.sh` that prints `oops` and ends with code 4, then check the code?",
                     "Put exit last, then read the code.",
                     ["Create it with `printf 'echo oops\\nexit 4\\n' > fail.sh`.", "Run `bash fail.sh`.", "Run `echo $?` straight after."],
                     "`bash fail.sh` prints `oops`, then `echo $?` prints `4`."),
                    ("Common mistake", "Why does `count = 5` print `count: command not found`?",
                     "Look at the spaces around the equals sign.",
                     ["Bash reads `count` as a command and `=` and `5` as its arguments.", "An assignment has no spaces around `=`."],
                     "Write `count=5`."),
                ],
            },
        },
        # ============================================================ page 2
        {
            "h1": "Check a file, a number or text, then choose what to run",
            "subtitle": "Check if a file exists, compare two numbers, compare two strings, match a file name pattern, pick a branch with case",
            "idea": (
                "Run a command only if something is true: put the test inside [[ ]] with spaces around everything, and let the exit code pick the branch.",
                [
                    ("Check if a file exists", "[[ -f report.txt ]]", "Also -d, -e, -s and -x."),
                    ("Compare two numbers", "[[ $n -gt 5 ]]", "Or (( n > 5 )) for maths."),
                    ("Match a file name pattern", "[[ $f == *.txt ]]", "No quotes around the pattern."),
                    ("Pick a branch by value", "case $x in a) ... ;; esac", "Use | to join choices."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does `[ $name = Ada ]` error when the name is empty or has a space? Why is `[[ $n=5 ]]` always true?",
                "fix": "Use `[[ ]]` with a space on every side of the operator: `[[ $n = 5 ]]`.",
            },
            "drills": [
                {
                    "h2": "Choose what to run with if, elif and else",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for testing", "code": C(r'''
mkdir -p /tmp/tw/tests/data && cd /tmp/tw/tests
printf 'alpha\nbeta\n' > report.txt
: > empty.txt
printf '#!/bin/bash\necho run\n' > run.sh && chmod +x run.sh
ls
'''),
                         "expect": "`ls` lists `data`, `empty.txt`, `report.txt` and `run.sh`."},
                        {"type": "cmd", "where": "shell", "title": "Run one of three branches (if, elif, else)", "code": C(r'''
n=7
if [[ $n -gt 10 ]]; then
  echo "big"
elif [[ $n -gt 5 ]]; then
  echo "medium"
else
  echo "small"
fi
'''),
                         "expect": "`medium` prints. The first test fails, the `elif` passes, and bash skips the `else`."},
                        {"type": "cmd", "where": "shell", "title": "Check if two strings match, or if a string is empty (= != -z -n)", "code": C(r'''
s=hello
[[ $s == hello ]] && echo "same"
[[ $s != bye ]] && echo "different"
[[ -z "" ]] && echo "empty"
[[ -n $s ]] && echo "not empty"
'''),
                         "expect": "Four lines: `same`, `different`, `empty`, `not empty`."},
                        {"type": "cmd", "where": "shell", "title": "Compare numbers (-eq -lt -gt), and see why < gives the wrong answer", "code": C(r'''
[[ 3 -lt 10 ]] && echo "3 is less than 10"
[[ 5 -eq 5 ]] && echo "equal"
[[ 9 < 10 ]] || echo "as text, 9 sorts after 10"
'''),
                         "expect": "Three lines: `3 is less than 10`, `equal`, `as text, 9 sorts after 10`. Inside `[[ ]]`, `<` compares text, so use `-lt` for numbers."},
                    ],
                },
                {
                    "h2": "Check a file or folder, and combine tests",
                    "intro": "Check a file with one letter after the dash. Join tests with `&&` and `||` inside the brackets.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Check if a file or folder exists, is empty or can run (-f -d -e -s -x)", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && echo "file"
[[ -d data ]] && echo "folder"
[[ -e nope ]] || echo "missing"
[[ -s empty.txt ]] || echo "empty file"
[[ -x run.sh ]] && echo "runnable"
'''),
                         "expect": "Five lines: `file`, `folder`, `missing`, `empty file`, `runnable`."},
                        {"type": "cmd", "where": "shell", "title": "Check two things at once (&& and || inside [[ ]])", "code": C(r'''
cd /tmp/tw/tests
n=12
[[ -f report.txt && -s report.txt ]] && echo "has content"
[[ $n -lt 0 || $n -gt 10 ]] && echo "out of range"
'''),
                         "expect": "Two lines: `has content` and `out of range`."},
                        {"type": "cmd", "where": "shell", "title": "Check if a file name matches a pattern like *.txt", "code": C(r'''
f=notes.txt
[[ $f == *.txt ]] && echo "text file"
[[ $f == n* ]] && echo "starts with n"
[[ $f == "*.txt" ]] || echo "quoted, it is just those characters"
'''),
                         "expect": "Three lines: `text file`, `starts with n`, `quoted, it is just those characters`. A quoted pattern matches only itself."},
                        {"type": "cmd", "where": "shell", "title": "Compare numbers with maths symbols (( ))", "code": C(r'''
n=7
(( n > 5 )) && echo "over 5"
(( n % 2 == 0 )) || echo "odd"
(( n * 2 == 14 )) && echo "double is 14"
'''),
                         "expect": "Three lines: `over 5`, `odd`, `double is 14`."},
                        {"type": "cmd", "where": "shell", "title": "Why is my [[ ]] test always true? Find the missing spaces", "code": C(r'''
n=7
[[ $n=5 ]] && echo "always true"
[[ $n = 5 ]] || echo "really false"
'''),
                         "expect": "`always true` prints because `7=5` is one non-empty word, so the test never compares. The second test, with spaces, is false, so `really false` prints."},
                    ],
                },
                {
                    "h2": "Pick a branch with case, or run a command only if another worked",
                    "intro": "Pick a branch by pattern with `case`. Run the next command on success or on failure with `&&` and `||`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Pick a branch by value (case, patterns and |)", "code": C(r'''
ans=yes
case $ans in
  y|yes) echo "going ahead" ;;
  n|no)  echo "stopping" ;;
  *)     echo "unknown: $ans" ;;
esac
'''),
                         "expect": "`going ahead` prints. `y|yes` matches `yes`, and each branch ends with `;;`."},
                        {"type": "cmd", "where": "shell", "title": "Run a different command for each file type (case)", "code": C(r'''
for f in a.txt b.sh c.md; do
  case $f in
    *.txt|*.md) echo "$f: text" ;;
    *.sh)       echo "$f: script" ;;
  esac
done
'''),
                         "expect": "Three lines: `a.txt: text`, `b.sh: script`, `c.md: text`."},
                        {"type": "cmd", "where": "shell", "title": "Run a command only if another worked (cmd && echo ok || echo fail)", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && echo ok || echo fail
[[ -f nope ]] && echo ok || echo fail
'''),
                         "expect": "`ok` for the file that exists, `fail` for the one that does not."},
                        {"type": "cmd", "where": "shell", "title": "Why does fail print even when the test passed? (the && || trap)", "code": C(r'''
cd /tmp/tw/tests
[[ -f report.txt ]] && false || echo "fail printed anyway"
if [[ -f report.txt ]]; then false; else echo "fail"; fi
echo "if/else done"
'''),
                         "expect": "`fail printed anyway` comes from the `&&` `||` line, because `false` failed. The `if` line prints no `fail`, because `else` runs only when the test fails. Then `if/else done`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Look up a test for a file, a string or a number",
                "cards": [
                    ("Check a file or folder", "Which letter checks what? One letter after the dash.", ["What you want to check", "Type this"], [
                        ["Check a file exists", "`[[ -f x ]]` (a regular file)"],
                        ["Check a folder exists", "`[[ -d x ]]`"],
                        ["Check something exists (a broken symlink counts as missing)", "`[[ -e x ]]`"],
                        ["Check a file is not empty", "`[[ -s x ]]`"],
                        ["Check a file can be run (or a folder entered)", "`[[ -x x ]]`"],
                    ]),
                    ("Compare text and numbers", "How do I match text literally? Quote the right side of `=`. Unquoted, it is a pattern.", ["What you want to check", "Type this"], [
                        ["Check two strings match", "`[[ $a = \"$b\" ]]` (`!=` for different)"],
                        ["Check a string is empty or not", "`[[ -z $a ]]` or `[[ -n $a ]]`"],
                        ["Compare whole numbers", "`[[ $a -lt $b ]]`. Also `-le -gt -ge -eq -ne`."],
                        ["Compare with maths symbols", "`(( a > b ))`"],
                    ]),
                    ("Run a command on pass or fail", "Is `a && b || c` the same as if/else? No.", ["What you want", "Type this"], [
                        ["Run b only when a works", "`a && b`"],
                        ["Run c only when a fails", "`a || c`"],
                        ["Choose between two branches safely", "`if a; then b; else c; fi`"],
                        ["Avoid this trap", "`a && b || c` also runs c when b fails."],
                    ]),
                ],
            },
            "worked": {
                "h2": "Check that a file exists and has content",
                "frame": "How do I make a script read `report.txt` only when it is there and not empty?",
                "open": "cd /tmp/tw/tests",
                "steps": [
                    (None, "`f=report.txt`", "Save the file name once."),
                    (None, "`if [[ -f $f && -s $f ]]; then echo \"$f has data\"; else echo \"$f is missing or empty\"; fi`", "`-f` and `-s` must both pass."),
                    (None, "`f=empty.txt`, then run the `if` line again", "The file exists but `-s` fails."),
                ],
                "after": "report.txt has data\nempty.txt is missing or empty",
                "meaning": "Check a file exists and is not empty in one test: [[ ]] with && checks both facts before the script touches the file.",
            },
            "practice": {
                "h2": "Check what you know: if, case and tests",
                "qs": [
                    ("Mechanism", "Why does `[[ 9 < 10 ]]` come out false?",
                     "Is `<` a number test or a text test?",
                     ["Inside `[[ ]]`, `<` compares text in dictionary order.", "As text, `9` sorts after `10`."],
                     "Use `-lt` for numbers: `[[ 9 -lt 10 ]]`."),
                    ("Keystrokes", "How do I test if `$f` ends in `.log`?",
                     "A pattern on the right, no quotes.",
                     ["Use `==` inside `[[ ]]`.", "Put `*.log` on the right, unquoted."],
                     "`[[ $f == *.log ]]`."),
                    ("Application", "How do I write a case that prints `weekend` for `sat` or `sun` and `weekday` for anything else?",
                     "Join two choices with a pipe.",
                     ["Start with `case $d in`.", "Add `sat|sun) echo weekend ;;`.", "Add `*) echo weekday ;;` and `esac`."],
                     "`case $d in sat|sun) echo weekend ;; *) echo weekday ;; esac`."),
                    ("Common mistake", "Why does `[[ -f report.txt ]] && false || echo fail` print `fail` though the file exists?",
                     "What runs after the middle command fails?",
                     ["`&&` runs `false`, which fails.", "`||` then runs on that failure."],
                     "`a && b || c` also runs `c` when `b` fails. Use `if` and `else`."),
                ],
            },
        },
        # ============================================================ page 3
        {
            "h1": "Loop over files, numbers and lines in bash",
            "subtitle": "Run a command on every file, count from 1 to 5, repeat until something changes, read a file line by line, split a CSV line",
            "idea": (
                "Repeat a command in bash: for walks a list, while repeats until a test fails, and while read walks lines.",
                [
                    ("Loop over files", "for f in *.txt; do ...; done", "Quote \"$f\" inside."),
                    ("Count to five", "for i in {1..5}; do ...; done", "Or for ((i=0; i<5; i++))."),
                    ("Read a file line by line", "while read -r line; do ...; done < file", "Safe with spaces in a line."),
                    ("Split a CSV line into columns", "while IFS=, read -r a b", "IFS is the separator."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does `for x in $(cat file)` cut every line at its spaces? Why does a loop after a pipe lose the variable it set?",
                "fix": "Read lines with `while IFS= read -r line; do ...; done < file`, and quote `\"$f\"` in every loop.",
            },
            "drills": [
                {
                    "h2": "Loop over files, words and numbers (for)",
                    "intro": BASH_FIRST,
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Create the practice files for loops", "code": C(r'''
mkdir -p /tmp/tw/loops && cd /tmp/tw/loops
printf 'one\n' > a.txt
printf 'one\ntwo\n' > b.txt
printf 'one\ntwo\nthree\n' > 'c d.txt'
printf 'red apple\ngreen pear\nblue plum\n' > names.txt
printf 'Ada,36\nBo,41\nCy,29\n' > people.csv
ls
'''),
                         "expect": "`ls` lists `a.txt`, `b.txt`, `c d.txt`, `names.txt` and `people.csv`."},
                        {"type": "cmd", "where": "shell", "title": "Loop over a list of words", "code": C(r'''
for fruit in apple pear plum; do
  echo "fruit: $fruit"
done
'''),
                         "expect": "Three lines: `fruit: apple`, `fruit: pear`, `fruit: plum`."},
                        {"type": "cmd", "where": "shell", "title": "Loop over every .txt file", "code": C(r'''
cd /tmp/tw/loops
for f in *.txt; do
  echo "$f has $(wc -l < "$f" | tr -d ' ') lines"
done
'''),
                         "expect": "Four lines: `a.txt has 1 lines`, `b.txt has 2 lines`, `c d.txt has 3 lines`, `names.txt has 3 lines`. The name with a space stays whole."},
                        {"type": "cmd", "where": "shell", "title": "Stop a loop from running when no file matches *.zip", "code": C(r'''
cd /tmp/tw/loops
for f in *.zip; do echo "got $f"; done
for f in *.zip; do [[ -e $f ]] || continue; echo "got $f"; done
echo "done"
'''),
                         "expect": "The first loop prints `got *.zip`: no file matched, so the pattern itself is the value. The guarded loop prints nothing. Then `done`."},
                        {"type": "cmd", "where": "shell", "title": "Count from 1 to 5 ({1..5})", "code": C(r'''
for i in {1..5}; do printf '%s ' "$i"; done; echo
for c in {a..e}; do printf '%s ' "$c"; done; echo
'''),
                         "expect": "`1 2 3 4 5` on one line, then `a b c d e`."},
                        {"type": "cmd", "where": "shell", "title": "Count with a C-style loop: for ((i=0; i<3; i++))", "code": C(r'''
for ((i=0; i<3; i++)); do
  echo "i=$i"
done
'''),
                         "expect": "Three lines: `i=0`, `i=1`, `i=2`."},
                        {"type": "cmd", "where": "shell", "title": "Count up to a variable, or in steps (seq)", "code": C(r'''
n=3
echo {1..$n}
for i in $(seq 1 $n); do printf '%s ' "$i"; done; echo
seq 1 3 10
'''),
                         "expect": "`{1..3}` prints as typed, because braces do not expand a variable. Then `1 2 3` from `seq`, then `1`, `4`, `7`, `10` on separate lines: start 1, step 3, stop at 10."},
                        {"type": "text", "body": "Why does `{1..$n}` not count to my variable? Braces do not expand a variable. Use `seq`. GNU `seq` works the same on Linux."},
                    ],
                },
                {
                    "h2": "Repeat until something changes (while and until)",
                    "intro": "Repeat as long as a test passes with `while`. Repeat as long as it fails with `until`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Repeat while a counter is small", "code": C(r'''
i=1
while [[ $i -le 3 ]]; do
  echo "round $i"
  i=$((i + 1))
done
'''),
                         "expect": "Three lines: `round 1`, `round 2`, `round 3`."},
                        {"type": "cmd", "where": "shell", "title": "Repeat until a counter passes 3", "code": C(r'''
i=1
until [[ $i -gt 3 ]]; do
  echo "i=$i"
  ((i++))
done
'''),
                         "expect": "Three lines: `i=1`, `i=2`, `i=3`."},
                        {"type": "cmd", "where": "shell", "title": "Stop a loop early (break) or skip one round (continue)", "code": C(r'''
for i in 1 2 3 4 5; do
  [[ $i -eq 2 ]] && continue
  [[ $i -eq 4 ]] && break
  echo "i=$i"
done
'''),
                         "expect": "Two lines: `i=1` and `i=3`. Round 2 is skipped, and round 4 ends the loop."},
                    ],
                },
                {
                    "h2": "Read a file line by line and split columns",
                    "intro": "Read one line at a time with `while read -r`. Feed it a file with `< file`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read a file line by line with while read -r", "code": C(r'''
cd /tmp/tw/loops
while IFS= read -r line || [[ -n $line ]]; do
  echo "> $line"
done < names.txt
'''),
                         "expect": "Each line of `names.txt` with `> ` in front: `> red apple`, `> green pear`, `> blue plum`."},
                        {"type": "text", "body": "How do I keep a last line that has no newline at the end? Add `|| [[ -n $line ]]`: `read` fails on it, but `$line` is still set."},
                        {"type": "cmd", "where": "shell", "title": "Loop over every line of a command's output", "code": C(r'''
cd /tmp/tw/loops
ls *.txt | while IFS= read -r f; do
  echo "got: $f"
done
'''),
                         "expect": "One line per file: `got: a.txt`, `got: b.txt`, `got: c d.txt`, `got: names.txt`."},
                        {"type": "cmd", "where": "shell", "title": "Split simple CSV lines with no quoted fields (while IFS=, read -r)", "code": C(r'''
cd /tmp/tw/loops
while IFS=, read -r name age; do
  echo "$name is $age"
done < people.csv
'''),
                         "expect": "Three lines: `Ada is 36`, `Bo is 41`, `Cy is 29`."},
                        {"type": "cmd", "where": "shell", "title": "Why does my counter stay 0 after a pipe into while?", "code": C(r'''
cd /tmp/tw/loops
count=0
cat names.txt | while read -r x; do count=$((count + 1)); done
echo "after pipe: $count"
while read -r x; do count=$((count + 1)); done < names.txt
echo "after redirect: $count"
'''),
                         "expect": "`after pipe: 0` and `after redirect: 3`. The piped loop ran in a subshell and counted a copy."},
                        {"type": "cmd", "where": "shell", "title": "Loop over lines with spaces safely (not for x in $(cat file))", "code": C(r'''
cd /tmp/tw/loops
for w in $(cat names.txt); do echo "[$w]"; done
while IFS= read -r l || [[ -n $l ]]; do echo "[$l]"; done < names.txt
'''),
                         "expect": "Six lines first, one per word: `[red]`, `[apple]`, `[green]`, `[pear]`, `[blue]`, `[plum]`. Then three whole lines: `[red apple]`, `[green pear]`, `[blue plum]`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Look up which loop to use",
                "cards": [
                    ("Pick a loop for the job", "Choose by what you want to repeat over.", ["What you want to loop over", "Type this"], [
                        ["Loop over every file", "`for f in *.txt; do ...; done`"],
                        ["Repeat a fixed count", "`for i in {1..5}` or `for ((i=0; i<5; i++))`"],
                        ["Repeat a count held in a variable", "`for i in $(seq 1 $n)`"],
                        ["Read every line of a file", "`while IFS= read -r line || [[ -n $line ]]; do ...; done < file`"],
                        ["Split a line into columns", "`while IFS=, read -r a b; do ...; done < file`"],
                    ]),
                    ("Stop a loop, skip a round or repeat", "Which word controls a loop? Four do.", ["What you want", "Type this"], [
                        ["Leave the loop now", "`break`"],
                        ["Skip to the next round", "`continue`"],
                        ["Repeat while a test passes", "`while test; do ...; done`"],
                        ["Repeat until a test passes", "`until test; do ...; done`"],
                    ]),
                    ("Avoid two loop traps that lose data", "Both lose data without showing an error.", ["What you want", "Type this"], [
                        ["Loop over lines that contain spaces", "`while IFS= read -r x; do ...; done < file`, not `for x in $(cat file)`"],
                        ["Keep a variable set inside the loop", "`while read ...; done < file`, not `cmd | while read`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Add up a column of numbers in a CSV file",
                "frame": "`people.csv` has `name,age` on each line. How do I get the total of the ages?",
                "open": "cd /tmp/tw/loops",
                "steps": [
                    (None, "`total=0`", "Start the total at 0."),
                    (None, "`while IFS=, read -r name age; do total=$((total + age)); done < people.csv`", "Each line splits at the comma. The loop reads from the file, so `total` survives."),
                    (None, "`echo \"total age: $total\"`", "Print the total."),
                ],
                "after": "total age: 106",
                "meaning": "Keep a variable set after a loop: redirect the file in, so the loop stays in your shell.",
            },
            "practice": {
                "h2": "Check what you know: loops",
                "qs": [
                    ("Mechanism", "Why is `count` still `0` after `cat f | while read -r x; do count=$((count+1)); done`?",
                     "Where does each side of a pipe run?",
                     ["Each side of a pipe runs in its own subshell.", "The loop changes a copy of `count`.", "The copy disappears when the pipe ends."],
                     "Feed the loop with `< f` instead of a pipe."),
                    ("Keystrokes", "How do I print `a.txt`, `b.txt` and the rest of the `.txt` files in a loop, even when a name has a space?",
                     "A glob, with quotes on the variable.",
                     ["Use `for f in *.txt; do`.", "Write `echo \"$f\"`.", "Close with `done`."],
                     "`for f in *.txt; do echo \"$f\"; done`."),
                    ("Application", "How do I print `Ada`, `Bo` and `Cy` from `people.csv`, one per line?",
                     "Split at the comma and ignore the age.",
                     ["Write `while IFS=, read -r name age; do`.", "Write `echo \"$name\"`.", "End with `done < people.csv`."],
                     "`while IFS=, read -r name age; do echo \"$name\"; done < people.csv`."),
                    ("Common mistake", "Why does `for f in *.zip` print `*.zip` when there are no zip files, and how do I stop that?",
                     "Test that the file exists inside the loop.",
                     ["With no match the pattern stays as text.", "Add `[[ -e $f ]] || continue` as the first line of the loop."],
                     "`for f in *.zip; do [[ -e $f ]] || continue; ...; done`."),
                ],
            },
        },
        # ============================================================ page 4
        {
            "h1": "Make a script read arguments, flags and typed answers",
            "subtitle": "Read the first argument, give an argument a default, read -v and -n NAME flags, ask the user a question, print usage on bad input",
            "idea": (
                "Make a script read input: arguments come from $1, $2 and $@, and flags from a case loop or getopts.",
                [
                    ("Read the first argument", "$1", "$2 is the second, $# is the count."),
                    ("Give an argument a default value", "${1:-world}", "Used when $1 is empty."),
                    ("Read flags like -v and -n NAME", "getopts \"vn:\" opt", "A colon means the flag takes a value."),
                    ("Ask the user a question", "read -p \"Name: \" name", "-s hides it, -t 5 times out."),
                ],
                None,
            ),
            "problem": {
                "fail": "Why does my script break on `bash backup.sh \"my folder\"`? Why does it run with a missing argument and do the wrong thing?",
                "fix": "Quote `\"$@\"` and `\"$1\"`, require what you need with `${1:?usage}`, and print usage and `exit 1` on bad input.",
            },
            "drills": [
                {
                    "h2": "Read the arguments you pass to a script",
                    "intro": "Create each script with a here-doc and run it with `bash name.sh args`, so it works from zsh too.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read each argument, the count and all of them ($0 $1 $2 $# $@)", "code": C(r'''
mkdir -p /tmp/tw/args && cd /tmp/tw/args
cat > show.sh <<'EOF'
echo "script: $0"
echo "first:  $1"
echo "second: $2"
echo "count:  $#"
echo "all:    $@"
EOF
bash show.sh apple "red pear" plum
'''),
                         "expect": "Five lines: `script: show.sh`, `first:  apple`, `second: red pear`, `count:  3`, `all:    apple red pear plum`. The quoted `red pear` is one argument."},
                        {"type": "cmd", "where": "shell", "title": "Keep arguments with spaces whole (\"$@\" versus $* and \"$*\")", "code": C(r'''
cd /tmp/tw/args
cat > each.sh <<'EOF'
for a in "$@"; do echo "[$a]"; done
echo ---
for a in $*; do echo "[$a]"; done
echo ---
for a in "$*"; do echo "[$a]"; done
EOF
bash each.sh one "two words" three
'''),
                         "expect": "Three groups. `\"$@\"` prints `[one]`, `[two words]`, `[three]`. `$*` prints `[one]`, `[two]`, `[words]`, `[three]`. `\"$*\"` prints `[one two words three]`. Each group is separated by `---`."},
                        {"type": "cmd", "where": "shell", "title": "Loop over every argument (shift)", "code": C(r'''
cd /tmp/tw/args
cat > shiftall.sh <<'EOF'
while [[ $# -gt 0 ]]; do
  echo "arg: $1 (left: $#)"
  shift
done
EOF
bash shiftall.sh a b c
'''),
                         "expect": "Three lines: `arg: a (left: 3)`, `arg: b (left: 2)`, `arg: c (left: 1)`. Each `shift` drops `$1` and the rest move up."},
                        {"type": "cmd", "where": "shell", "title": "Take arguments two at a time (shift 2)", "code": C(r'''
cd /tmp/tw/args
cat > pairs.sh <<'EOF'
[[ $(( $# % 2 )) -eq 0 ]] || { echo "usage: pairs.sh KEY VALUE ..." >&2; exit 1; }
while [[ $# -gt 0 ]]; do
  echo "$1 = $2"
  shift 2
done
EOF
bash pairs.sh host web port 80
'''),
                         "expect": "Two lines: `host = web` and `port = 80`. With an odd count, such as `bash pairs.sh host web port`, it prints `usage: pairs.sh KEY VALUE ...` and stops."},
                    ],
                },
                {
                    "h2": "Give an argument a default, require it, or print usage",
                    "intro": "Fall back to `x` with `${1:-x}`. Stop the script with a message when `$1` is missing with `${1:?message}`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Give an argument a default value with ${1:-default}", "code": C(r'''
cd /tmp/tw/args
cat > greet.sh <<'EOF'
name=${1:-world}
echo "Hello, $name"
EOF
bash greet.sh
bash greet.sh Ada
'''),
                         "expect": "`Hello, world` with no argument, then `Hello, Ada`."},
                        {"type": "cmd", "where": "shell", "title": "Require an argument with ${1:?usage}", "code": C(r'''
cd /tmp/tw/args
cat > need.sh <<'EOF'
file=${1:?usage: need.sh FILE}
echo "using $file"
EOF
bash need.sh
echo "exit: $?"
bash need.sh data.csv
'''),
                         "expect": "`need.sh: line 1: 1: usage: need.sh FILE` and `exit: 1`: the script stopped. Then `using data.csv`."},
                        {"type": "cmd", "where": "shell", "title": "Print a usage message and exit 1 on bad input", "code": C(r'''
cd /tmp/tw/args
cat > copy2.sh <<'EOF'
usage() { echo "usage: copy2.sh SRC DEST" >&2; exit 1; }
[[ $# -eq 2 ]] || usage
echo "copying $1 to $2"
EOF
bash copy2.sh a
echo "exit: $?"
bash copy2.sh a b
'''),
                         "expect": "`usage: copy2.sh SRC DEST` and `exit: 1` for one argument. Then `copying a to b`."},
                        {"type": "text", "body": "Where do I learn functions like `usage() { ...; }`? Module 11 covers them."},
                    ],
                },
                {
                    "h2": "Read flags like -v and -n NAME",
                    "intro": "Read flags two ways: a `case` loop with `shift`, or the built-in `getopts`.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Read -n NAME and --name NAME flags with a case loop", "code": C(r'''
cd /tmp/tw/args
cat > parse.sh <<'EOF'
name=world
loud=0
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name) [[ $# -ge 2 && -n $2 ]] || { echo "missing NAME" >&2; exit 1; }; name=$2; shift 2 ;;
    -l|--loud) loud=1; shift ;;
    *) echo "unknown option: $1"; exit 1 ;;
  esac
done
msg="Hello, $name"
[[ $loud -eq 1 ]] && msg=$(echo "$msg" | tr a-z A-Z)
echo "$msg"
EOF
bash parse.sh --name Ada
bash parse.sh -l -n Bo
bash parse.sh --bogus
echo "exit: $?"
'''),
                         "expect": "Four lines: `Hello, Ada`, `HELLO, BO`, `unknown option: --bogus`, `exit: 1`."},
                        {"type": "cmd", "where": "shell", "title": "Read a script's flags with getopts", "code": C(r'''
cd /tmp/tw/args
cat > opts.sh <<'EOF'
verbose=0
name=world
while getopts "vn:" opt; do
  case $opt in
    v) verbose=1 ;;
    n) name=$OPTARG ;;
    *) echo "usage: opts.sh [-v] [-n NAME] [file...]"; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
echo "verbose=$verbose name=$name rest=$*"
EOF
bash opts.sh -v -n Ada one two
bash opts.sh -x
'''),
                         "expect": "`verbose=1 name=Ada rest=one two`. Then for `-x`, getopts prints `opts.sh: illegal option -- x` and the script prints its usage line."},
                        {"type": "text", "body": "What does `getopts \"vn:\"` mean? `v` is a switch and `n:` takes a value, held in `$OPTARG`. `OPTIND` is the index of the next argument, so `shift $((OPTIND - 1))` leaves only the files."},
                    ],
                },
                {
                    "h2": "Ask the user a question and read the answer",
                    "intro": "Wait for a typed line with `read`. These scripts wait for you, so type the answer and press Enter.",
                    "blocks": [
                        {"type": "cmd", "where": "shell", "title": "Ask a question and save the answer (read -p)", "code": C(r'''
cd /tmp/tw/args
cat > ask.sh <<'EOF'
read -p "Your name: " name
echo "Hi $name"
EOF
bash ask.sh
'''),
                         "expect": "`Your name: ` waits. Type `Ada` and press Enter: `Hi Ada` prints."},
                        {"type": "cmd", "where": "shell", "title": "Hide what the user types, like a password (read -s)", "code": C(r'''
cd /tmp/tw/args
cat > secret.sh <<'EOF'
read -s -p "Password: " pw
echo
echo "got ${#pw} characters"
EOF
bash secret.sh
'''),
                         "expect": "`Password: ` waits and shows nothing as you type. After Enter, the cursor moves to a new line and `got 7 characters` prints for a 7-letter password such as `hunter2`."},
                        {"type": "cmd", "where": "shell", "title": "Stop waiting for an answer after 3 seconds (read -t)", "code": C(r'''
cd /tmp/tw/args
cat > quick.sh <<'EOF'
read -t 3 -p "Answer in 3 seconds: " a || echo " too slow"
EOF
bash quick.sh
'''),
                         "expect": "`Answer in 3 seconds: ` waits. With no input, after 3 seconds ` too slow` appears on the same line."},
                        {"type": "cmd", "where": "shell", "title": "Keep backslashes in typed text (read -r)", "code": C(r'''
printf 'C:\\temp\n' | { read line; echo "plain: $line"; }
printf 'C:\\temp\n' | { read -r line; echo "raw:   $line"; }
'''),
                         "expect": "`plain: C:temp`, because plain `read` eats the backslash. Then `raw:   C:\\temp`."},
                    ],
                },
            ],
            "rules": {
                "h2": "Look up how to read arguments, defaults and typed input",
                "cards": [
                    ("Read the arguments", "Where do arguments come from? Bash sets them when the script starts.", ["What you want", "Type this"], [
                        ["Read the first argument", "`$1` (`$2` is the second)"],
                        ["Count the arguments", "`$#`"],
                        ["Pass every argument on, each kept whole", "`\"$@\"`"],
                        ["Print the script name", "`$0`"],
                        ["Avoid this one", "`$*` cuts arguments at spaces"],
                    ]),
                    ("Give a default, require a value or check the count", "What should happen when an argument is missing? Pick one.", ["What you want", "Type this"], [
                        ["Use a default when $1 is empty", "`${1:-world}`"],
                        ["Stop with a message when $1 is empty", "`${1:?usage: x FILE}`"],
                        ["Run your own usage check", "`[[ $# -eq 2 ]] || usage`"],
                    ]),
                    ("Ask the user a question", "Which flag changes how read waits? Pick one.", ["What you want", "Type this"], [
                        ["Show a prompt", "`read -p \"Name: \" name`"],
                        ["Hide what is typed", "`read -s pw`"],
                        ["Give up after 5 seconds", "`read -t 5 a`"],
                        ["Keep backslashes as typed", "`read -r line`"],
                    ]),
                ],
            },
            "worked": {
                "h2": "Greet by name, with a default name and a switch for shouting",
                "frame": "How do I make `parse.sh` greet `world` by default, take `-n NAME`, and shout with `-l`?",
                "open": "cd /tmp/tw/args",
                "steps": [
                    (None, "`bash parse.sh`", "No flags: the default name stays."),
                    (None, "`bash parse.sh -l -n Bo`", "The loop reads `-l`, then `-n` and its value with `shift 2`."),
                ],
                "after": "Hello, world\nHELLO, BO",
                "meaning": "Handle flags in any order: a case loop with shift reads them, and the `*)` branch rejects anything else.",
            },
            "practice": {
                "h2": "Check what you know: arguments, flags and input",
                "qs": [
                    ("Mechanism", "What is the difference between `\"$@\"` and `$*` with `one \"two words\" three`?",
                     "Count the words each one produces.",
                     ["`\"$@\"` gives three words, keeping `two words` together.", "Unquoted `$*` gives four words."],
                     "`\"$@\"` keeps each argument whole. `$*` cuts at spaces."),
                    ("Keystrokes", "How do I set `dir` to the first argument, or to `.` when none is given?",
                     "A default with a colon and a dash.",
                     ["Use `${1:-.}`.", "Assign it with `dir=`."],
                     "`dir=${1:-.}`."),
                    ("Application", "How do I make a script stop with `usage: run.sh FILE` when no file is given?",
                     "A required value with a question mark.",
                     ["Use `${1:?...}`.", "Put the usage text after the question mark."],
                     "`file=${1:?usage: run.sh FILE}`."),
                    ("Common mistake", "Why is `$name` empty when my `getopts \"vn:\"` script sees `-n`? What did I forget?",
                     "Where does getopts put a flag's value?",
                     ["A flag that ends in `:` takes a value.", "The value is in `$OPTARG`, not in `$1`."],
                     "Write `n) name=$OPTARG ;;`."),
                ],
            },
        },
    ],
}
