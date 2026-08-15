# File IO in Python: The Absolute Minimum You Must Know

Reading and writing files rests on one non-negotiable habit (`with`), one choice (how to
read: whole, lines, or streaming), one letter (the mode), and one modern API (`pathlib`)
— all on this page. The examples below write into a temporary directory so you can run
them anywhere:

```python
import tempfile
from pathlib import Path

tmp = Path(tempfile.mkdtemp())   # a scratch directory for this page's examples
```

## The Headline Model: with Is Not Optional

A file handle is a borrowed resource: the operating system lends it to you, and it must
be given back — otherwise buffered writes may never reach the disk and long-running
programs leak handles until they crash. `with` is Python's **context manager** syntax:
"borrow this, and no matter what happens — early return, exception, crash — give it back
at the end of the block."

```python
>>> with open(tmp / "notes.txt", "w", encoding="utf-8") as f:
...     _ = f.write("first line\n")    # write returns a count; _ discards it
...     _ = f.write("second line\n")
```

When the block ends, `f` is flushed and closed — guaranteed. The old style
(`f = open(...)` ... `f.close()`) silently skips the `close()` whenever an exception
jumps over it. That's why `with` is non-negotiable: it's not politeness, it's the only
version that's correct when something goes wrong.

## Reading: Whole, Lines, or Streaming

Three ways to get content out, in order of how much memory they hold:

```python
>>> with open(tmp / "notes.txt", encoding="utf-8") as f:
...     whole = f.read()            # the whole file as ONE string
>>> whole
'first line\nsecond line\n'
>>> with open(tmp / "notes.txt", encoding="utf-8") as f:
...     lines = f.readlines()       # a list of lines, newlines included
>>> lines
['first line\n', 'second line\n']
>>> with open(tmp / "notes.txt", encoding="utf-8") as f:
...     for line in f:              # streaming: one line in memory at a time
...         print(line.strip())
first line
second line
```

Default to **iteration**: it works identically on a 1 KB config and a 10 GB log, because
it never loads the whole file. `read()` is for when you genuinely want one string;
`readlines()` is rarely worth it — the file object already iterates by line. Note the
`.strip()`: every line keeps its trailing `\n`, the number-one "why is my output
double-spaced?" surprise.

## Writing and Appending: One Letter Decides

The mode string is small but consequential: `"r"` read (the default), `"w"` write —
**truncates the file to empty the instant it opens** — and `"a"` append, which keeps the
contents and adds to the end:

```python
>>> with open(tmp / "notes.txt", "a", encoding="utf-8") as f:
...     _ = f.write("third line\n")
>>> with open(tmp / "notes.txt", encoding="utf-8") as f:
...     print(len(f.readlines()))
3
```

Reopening a log file with `"w"` when you meant `"a"` deletes the log. If a file
mysteriously ends up empty, suspect a stray `"w"` before anything else.

## Encodings in One Paragraph

A file on disk is bytes; a Python string is text; an **encoding** is the translation
between them, and UTF-8 is the one the modern world agreed on. Python, however, may
default to the operating system's legacy encoding — code that works on your Mac then
mangles `café` into `cafÃ©` on a Windows machine (mojibake) or dies with
`UnicodeDecodeError`. So spell it out, every time, both directions:
`open(path, encoding="utf-8")`. One argument, entire class of bug gone.

## pathlib: The Modern Path API

A `Path` is an object that knows it's a path — no more gluing strings together with
`/` or `os.path.join`. You've been using one all page (`tmp` is a `Path`):

```python
>>> report = tmp / "out" / "report.txt"     # / joins path segments
>>> report.parent.mkdir(parents=True)       # create the directories
>>> report.write_text("done\n", encoding="utf-8")
5
>>> report.read_text(encoding="utf-8")
'done\n'
>>> report.name, report.suffix, report.exists()
('report.txt', '.txt', True)
```

`write_text`/`read_text` are the whole open-with-read-close dance in one call — perfect
for small files (they handle the closing internally). Use `open(path)` with a `with`
block when you need streaming or appending; `Path.glob("*.csv")` finds files by pattern.

## Directing the Machine

The informed prompt names the concepts on this page — `with`, the mode, the encoding,
streaming vs whole-file — because those are exactly the details an AI will otherwise
guess at, and its guesses are where the bugs live.

Vague:

```
"write python code to save my results to a file"
```

Informed:

```
"Using pathlib and a with block, APPEND one line per result to results.log,
UTF-8, creating the file if missing. The input list can be large, so don't
build one giant string — write line by line."
```

## Spot the Confabulation

An AI assistant explains file writing:

```
def save_scores(scores, filename):
    f = open(filename, "w")
    for name, score in scores.items():
        f.write(f"{name},{score}\n")
    # No need to close the file — Python's garbage collector
    # closes it automatically when the function returns.
```

<details><summary>What's wrong?</summary>

The comment is the confabulation — plausible, confident, and only accidentally true.
CPython's reference counting *usually* closes the file promptly, so this "works on my
machine"; on other interpreters (PyPy), or if an exception fires mid-loop, or before an
abrupt exit, the handle can stay open with the last writes **stuck in the buffer** —
a truncated file with no error message. And `"w"` has already emptied any existing file
even if the loop then fails. Correct version: `with open(filename, "w",
encoding="utf-8") as f:` — guaranteed flush and close on every path out of the block.

</details>

## Where to Practice

- **[Advent of Code](https://adventofcode.com)** — hundreds of free puzzles, and every
  single one starts the same way: read an input file, parse it line by line. The most
  natural file-IO drill that exists.
- **[Exercism's Python track](https://exercism.org/tracks/python)** — free, test-driven
  exercises; pair it with rewriting any of your own scripts to use `pathlib` and `with`.

## Quick Reference

| Idea | The minimum |
|---|---|
| Open safely | `with open(path, encoding="utf-8") as f:` — closes on every exit path |
| Read all | `f.read()` → one string (small files only) |
| Read lines | `for line in f:` → streaming, any size; `line.strip()` drops the `\n` |
| Modes | `"r"` read · `"w"` write (**truncates!**) · `"a"` append |
| Encoding | always pass `encoding="utf-8"` — reads and writes |
| Paths | `Path("data") / "in.csv"`; `.exists()`, `.name`, `.suffix`, `.glob("*.csv")` |
| Small files | `path.write_text(s, encoding="utf-8")` / `path.read_text(...)` |
| Scratch space | `tempfile.mkdtemp()` for tests and experiments |

That covers the absolute minimum! You can now read, write, and append any text file
safely on any machine, and spot the two silent killers — a missing `with` and a stray
`"w"` — in anyone's code, including an AI's.
