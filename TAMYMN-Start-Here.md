# Start Here: The Absolute Minimum Before the Minimum

Every other page in this book assumes you can read a sentence like "mutable default
argument" without flinching. This page assumes nothing at all. It rests on about six
bootstrap ideas — what code is, the three windows, files and paths, running something,
reading an error, and asking good questions — and by the end you'll have run real Python
and know exactly where to go next.

## What Code Actually Is

A program is a list of instructions for a machine that is unimaginably fast and completely
literal. It does exactly what you wrote — not what you meant, not what any sensible person
would infer — billions of times per second. That literalness is the whole game: every
frustration you'll ever have ("why did it do *that*?") and every power you'll ever gain
("it did precisely what I said") comes from it.

And a program is just a **text file**. Not a special sealed artifact — ordinary text you
could read aloud, saved in an ordinary file, fed to another program (like Python) that
carries out the instructions. Open any `.py` file and you're looking at the whole truth of
what that program does. There is no magic underneath; there is only more text, all the way
down. That's why programming is learnable: everything is inspectable.

## The Three Windows You'll Live In

Programmers keep three kinds of window open, each with one job:

- **The browser** — for reading docs, running this book's [Playground](playground.qmd),
  and asking an AI questions. You already know this one.
- **An editor** — a program for writing code-text, with helpers like coloring and error
  underlines. Think "word processor for code, minus the fonts". The standard one is VS
  Code ([TAMYMN-VSCode.md](TAMYMN-VSCode.md)).
- **The terminal** — a window where you *type* commands instead of clicking buttons:
  `python3 report.py` instead of double-clicking an icon.

The terminal is the one that scares people, so let's defuse it now: it is nothing but a
different way to press buttons. Clicking "rename" and typing `mv draft.txt final.txt` do
the same thing; typed commands are simply more precise, repeatable, and shareable — which
is why every tutorial ever written says "type this" rather than "click here, then here".
It looks hostile because it doesn't advertise its options like menus do. It isn't hostile;
it's just quiet. [TAMYMN-Linux.md](TAMYMN-Linux.md) teaches the twenty commands that
matter — but you don't need any of them to start today.

## Files, Folders, and Where Things Actually Are

Code lives in ordinary files inside ordinary folders — the same files and folders as your
documents and photos. The ending of a filename (the **extension**) is just a label saying
what kind of text is inside: `report.py` is Python code, `notes.md` is Markdown text,
`data.csv` is a table. Changing the extension doesn't convert anything — it's a label, not
a spell.

Here is a secret worth this whole page: roughly half of all beginner problems are some
form of **"the computer can't find my file."** `No such file or directory` almost never
means the file doesn't exist — it means the file isn't where the machine is currently
*looking*. Every program runs "standing in" a particular folder, and a filename like
`data.csv` means "in the folder I'm standing in". The full story — absolute vs relative
paths — is in [TAMYMN-Linux.md](TAMYMN-Linux.md); for now, just knowing that "where is my
file?" is a normal, diagnosable question (not a sign you broke something) puts you ahead.

## Run Your First Python, Right Now

No installing, no setup: this book has a [Playground](playground.qmd) that runs real
Python inside your browser. Open it and type these three lines:

```python
>>> print("Hello — I am giving instructions to a machine")
Hello — I am giving instructions to a machine
>>> hours_per_week = 3
>>> hours_per_week * 52
156
```

That's a real program: an instruction to print text, a name given to a number, and
arithmetic done for you. The `>>>` marks what *you* type — don't type the arrows
themselves, just what follows them; the lines without arrows are the machine's reply.
(You'll see this transcript style throughout the book and everywhere Python is taught.) Everything you will ever build — websites, games, analyses — is this,
compounded: precise instructions, executed literally, one after another.

## Reading an Error Message

Sooner than you'd like, the machine will answer with a wall of red text. This is not a
crash, a verdict, or a sign you're not cut out for this — it is the machine telling you
*exactly* what it needs, in a slightly stilted dialect. Two rules make errors readable:

1. **Read the LAST line first.** Python prints the path it took (the "traceback") and puts
   the actual problem at the bottom: `NameError: name 'prnt' is not defined` means "you
   used the name `prnt` and I've never heard of it" — a typo for `print`.
2. **The last line is a search query, not a judgment.** Paste the error name and message
   into a search engine or an AI chat, along with the line of code it points at. Errors
   are the best-documented texts in all of computing — someone has hit yours before.

Programmers do not read less error text than beginners; they read it *better*, starting
at the bottom.

## The Jargon Strategy

This book uses precise words because precise words are the tools of the trade. When you
hit one you don't know, you have two moves: check [GLOSSARY.md](GLOSSARY.md), where every
term this book relies on is defined in a sentence or two, or ask an AI one precise
question ("In one paragraph: what is a 'variable' in programming?"). Never push on through
a paragraph you couldn't parse — the sentence after it assumes you did.

## Directing the Machine

You'll use AI chat constantly while learning — but at this stage its job is to **explain,
not to do**. A good explaining prompt has three parts: your context (total beginner),
what you already know, and the size of answer you want. That last part matters most —
without it you get a wall of text calibrated for someone else.

Vague:

```
"what is python"
```

Informed:

```
"I've never programmed. In one paragraph, what is Python and what is it for?
Then show me the smallest possible example."
```

One warning before the machine offers to write your code for you: when it writes code you
can't yet read, you can't check it — you can only hope. Learning to read code is exactly
what makes AI assistance safe to use, and that's the whole reason this book exists
([TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md) covers working *with* the machine once you
can check its work).

## Spot the Confabulation

A beginner types `prnt("hello")` into the Playground, gets
`NameError: name 'prnt' is not defined`, pastes it into an AI chat, and receives:

```
This error means your Python installation is missing core components — the print
module failed to load. This usually happens after an incomplete install or a system
update. Uninstall Python completely, restart your computer, and reinstall the
latest version from python.org. The error should then be resolved.
```

<details><summary>What's wrong?</summary>

Everything except the confidence. The error message already says what happened: the name
`prnt` is not defined — because it's a typo for `print`. Nothing is broken, nothing is
missing, and there is no "print module" that fails to load. Reinstalling is almost never
the fix for a Python error, and any explanation that ignores the actual words of the last
line — *name 'prnt' is not defined* — should be discarded. The machine told you exactly
what it needed; the AI answered a different, scarier question.

</details>

## Where to Practice

- **This book's [Playground](playground.qmd)** — real Python in your browser, zero
  install, right next to the chapters. Retype every example you read; typing is how it
  sticks.
- **[futurecoder](https://futurecoder.io)** — a free, no-signup course that runs Python in
  the browser and shows you, step by step, what the machine is doing with each line.
- **[Exercism's Python track](https://exercism.org/tracks/python)** — free small exercises
  with automated tests; ideal a few chapters from now, once the syntax feels stable.

## Quick Reference

| Bootstrap fact | Why it matters |
|---|---|
| A program is a text file | you can read all of it; there is no magic layer |
| The machine is literal | it does what you *wrote*, at billions of steps per second |
| Three windows | browser (read/ask), editor (write), terminal (run) |
| The terminal | typed commands instead of clicks — precise, not hostile |
| `.py` / `.md` / `.csv` | extensions are labels for what text is inside |
| "File not found" | usually means "wrong folder", not "file gone" — see paths |
| Errors | read the **last line first**; it says exactly what's needed |
| Error text | a search/AI query, never a verdict on you |
| Unknown jargon | [GLOSSARY.md](GLOSSARY.md), or one precise AI question |
| Asking AI | context + what you know + size of answer; explain, don't do |
| Running Python | the [Playground](playground.qmd) — in your browser, zero install |

**Where next:** this page → [TAMYMN-Python.md](TAMYMN-Python.md) →
[TAMYMN-Functions.md](TAMYMN-Functions.md), picking up
[TAMYMN-Linux.md](TAMYMN-Linux.md) whenever you're ready to meet the terminal properly.
The trails on the front page map the rest.

That covers the absolute minimum before the minimum! You've run real code, you can read
what the machine says back, and you know how to ask about everything you don't know —
which is now the only skill you actually need.
