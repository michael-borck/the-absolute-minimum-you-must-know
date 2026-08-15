# Glossary {.unnumbered}

These are the terms the chapters use without stopping to define — each entry is one to
three sentences: what the thing is, and why you care. Chapters link here the first time
a term appears; follow the link, read the entry, go back. Where a chapter goes deep, the
entry points you to it.

**Term not here? Ask an AI — precisely.** The prompt shape that works:

> "In the context of Git, what does 'staging' mean? I understand files and folders but
> not version control. Two sentences and a tiny example."

Three ingredients: the *context* (Git, not English), *what you already know* (so the
answer builds on it), and the *size of answer* you want (so you get two sentences, not
an essay). Then sanity-check the answer against the chapter you're reading —
explanations can be confabulated too
([TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md)).

## A

### AGENTS.md

A file in your repo root that coding agents read at the start of every session — your
standing instructions ("run tests with pytest", "never touch migrations/"). When an
agent keeps making the same mistake, the fix is a line here, not a longer prompt.
See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### AI agent

An LLM put in a loop and handed tools: it reads your files, runs commands, edits code,
sees what happened, and goes again. Powerful precisely because every action really
happens — which is why you commit first and read the diff after.
See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### API

An Application Programming Interface: the set of calls a piece of software promises to
answer, so your code can use it without knowing its insides. A web API is the same idea
over the network — you send a URL, you get back data (usually JSON).

### Argument

The actual value you pass when calling a function — in `greet("Alice")`, `"Alice"` is
the argument. The parameter is the name in the definition; the argument is what fills it
at call time. See [TAMYMN-Functions.md](TAMYMN-Functions.md).

### Assertion

A statement that a specific thing must be true right now — `assert total == 42` — which
fails loudly if it isn't. Tests are built from assertions: each one is a claim your code
must keep honouring. See [TAMYMN-Testing.md](TAMYMN-Testing.md).

### Attribute

A variable attached to an object — `car.colour`, `df.shape`. Attributes are the
object's state; methods are what it can do with that state.
See [TAMYMN-Classes.md](TAMYMN-Classes.md).

### Axis

One direction of a plot (the x-axis and y-axis) — and, confusingly, also what pandas
calls its two directions (`axis=0` is down the rows, `axis=1` is across the columns).
When a pandas call does the opposite of what you expected, check the axis first.
See [TAMYMN-Matplotlib.md](TAMYMN-Matplotlib.md).

## B

### Boolean

A value that is either `True` or `False` — the entire currency of decision-making.
Every `if` and every `while` boils its condition down to one boolean.

### Branch

A movable label pointing at a commit, letting you work on something new while `main`
stays safe and working. Creating one costs nothing, which is the point: branch freely,
merge when it's ready. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Bug

A gap between what you told the computer to do and what you meant it to do. The
computer is never wrong about which of those it executed — debugging is finding where
your mental model and the code diverge.

## C

### Cell

One block of a notebook, holding either code or Markdown. Cells run individually, in
whatever order you click — which is flexible for exploring and a classic source of
"works for me, breaks on restart" bugs. See [TAMYMN-Jupyter.md](TAMYMN-Jupyter.md).

### CI (continuous integration)

A robot that runs your test suite automatically on every push, so a broken change is
caught in minutes instead of discovered by a teammate next week. If the tests only run
when someone remembers to run them, they will eventually not run.

### Class

A blueprint that defines what a kind of object knows (attributes) and can do (methods).
`Dog` is the class; your actual dog `rex` is an instance made from it.
See [TAMYMN-Classes.md](TAMYMN-Classes.md).

### Clone

Copying an entire repository — every file *and* its whole history — from a remote to
your machine with `git clone <url>`. You now have a complete, independent copy, not a
window onto someone else's. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Command line

The text interface where you type commands and read their output — the native language
of Git, pip, pytest, and every AI coding agent. Fluency here is leverage everywhere
else in this book. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Comment

A note in the code that the interpreter ignores (`# like this` in Python). Good
comments say *why* the code does something; the code itself already says what.

### Commit

A permanent snapshot of your staged changes, with a message saying why. Committed work
is essentially impossible to lose — which is why "commit before you experiment" is the
habit that makes everything else low-stakes. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Composition

Building an object *out of* other objects — a `Car` *has an* `Engine` — instead of
inheriting from them. Usually the more flexible choice: parts can be swapped;
ancestry can't. See [TAMYMN-Composition.md](TAMYMN-Composition.md).

### Condition

An expression that evaluates to `True` or `False`, deciding which way an `if` goes or
whether a `while` keeps looping. Most subtle bugs in conditions are boundary cases:
`<` where you meant `<=`.

### Confabulation

When an AI states falsehoods fluently and confidently. It isn't lying — it has no
ground truth to lie about; it produces plausible text, and plausible is not the same as
true. Also marketed as "hallucination"; every chapter's "Spot the Confabulation"
section trains you for it. See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Constructor (`__init__`)

The method that runs when an object is created — `__init__` in Python — where you set
up its starting attributes. `Dog("Rex")` calls it for you; you never call `__init__`
directly. See [TAMYMN-Classes.md](TAMYMN-Classes.md).

### Context (AI)

Everything the model can currently see: your prompt, the conversation so far, the files
it has opened. An AI acts only on its context — missing context doesn't stop it, it
fills the gap with a plausible guess. See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### CSV

Comma-Separated Values: a plain-text table, one row per line, commas between columns.
The lingua franca of data exchange — every spreadsheet exports it, and
`pd.read_csv` is how most pandas work begins. See [TAMYMN-Pandas.md](TAMYMN-Pandas.md).

## D

### Database

Software whose whole job is storing data safely and answering questions about it fast —
surviving crashes, concurrent users, and datasets too big for memory. When your data
outgrows a CSV, this is where it goes. See [TAMYMN-SQLite.md](TAMYMN-SQLite.md).

### DataFrame

The central object of pandas: a table with labelled rows and columns, where operations
apply to whole columns at once instead of one value at a time. Learn to think in
columns and most pandas code writes itself. See [TAMYMN-Pandas.md](TAMYMN-Pandas.md).

### Dependency

Code your code needs but you didn't write — every library you `pip install`. Each one
is borrowed power and borrowed risk, which is why agents adding dependencies casually
is on the watch-list. See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Dictionary

Python's key–value store: `{"name": "Alice", "role": "admin"}`. You look things up by
key, not position, and lookup is fast no matter how big it gets — the answer to "I need
to find things by name". See [TAMYMN-Data-Structures.md](TAMYMN-Data-Structures.md).

### Diff

The exact line-by-line difference between two versions of your files. `git diff` is how
you review what actually changed — your work or an AI's — because the report is a
claim and the diff is the fact. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Directory

A folder. Directories nest into a tree, and a path is the route through that tree to a
file — the single idea that makes the command line make sense.
See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Doctest

A test written as an interpreter transcript inside a docstring — `>>>` line, expected
output — so your documentation *is* your test. Every Python example in this book is
one, and CI proves they all pass. See [TAMYMN-Doctest.md](TAMYMN-Doctest.md).

### Duck typing

Python's stance that an object's abilities matter more than its ancestry: if it has a
`.quack()` method, it can be used wherever quacking is needed, whatever class it is.
This is why Python code asks "can it?" instead of "is it?".
See [TAMYMN-Polymorphism.md](TAMYMN-Polymorphism.md).

## E

### Editor

The program you write code in. Any one will do; what matters is knowing yours well
enough that the mechanics of editing never interrupt the thinking.
See [TAMYMN-VSCode.md](TAMYMN-VSCode.md).

### Error message

The computer telling you *exactly* what went wrong and where — read it bottom-up: the
last line names the problem, the lines above trace where. Pasting one verbatim is also
the single most effective AI prompt there is.

### Exception

Python's mechanism for "something went wrong here, someone else deal with it": the
error travels up through the callers until code catches it or the program stops with a
traceback. Catching one you can't actually handle just hides the crash for later.

### Expression

Code that produces a value: `2 + 3`, `len(name)`, `x > 0`. Expressions go anywhere a
value goes; statements (assignments, `if`, `return`) don't — that's why
`x = (y = 5)` is a syntax error.

## F

### File extension

The suffix after the dot — `.py`, `.csv`, `.md` — a naming convention that tells humans
and programs what's inside. It's only convention: renaming `.txt` to `.py` changes
nothing about the contents.

### Float

A number with a decimal point, stored in binary approximation — which is why
`0.1 + 0.2` is very slightly not `0.3`. Never compare floats with `==`; ask if they're
*close*.

### Function

A named, reusable block of code: inputs in (parameters), work happens, value out
(`return`). The fundamental unit of "solve it once, use it everywhere" — and the unit
tests are built around. See [TAMYMN-Functions.md](TAMYMN-Functions.md).

## G

### Git

The version control system this whole book leans on: it snapshots your project so any
state can be recovered and any change reviewed. In the AI age it matters more, not
less — a commit is what makes an agent's work safe to undo.
See [TAMYMN-Git.md](TAMYMN-Git.md).

## H

### Hidden file

A file whose name starts with a dot — `.git`, `.env` — which `ls` doesn't show by
default (`ls -a` does). Much of your configuration, and your entire Git history, lives
in files you can't see until you ask. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### HTML

The markup language of every web page: content wrapped in nested tags like
`<p>` and `<a>`. Web scraping is just parsing that tree to pull out the parts you
want. See [TAMYMN-Web-Scraping.md](TAMYMN-Web-Scraping.md).

## I

### IDE

An Integrated Development Environment: an editor with the rest of the workflow —
running, debugging, Git, terminal — built in. VS Code is the one this book uses.
See [TAMYMN-VSCode.md](TAMYMN-VSCode.md).

### Import

How one Python file uses another's code: `import pandas` loads the module and gives you
a name to reach its contents through. Everything beyond the built-ins arrives this way.

### Index

A position in a sequence — and in Python, counting starts at 0, so `items[1]` is the
*second* item. Off-by-one errors around indexes are the most common bug in
programming; assume you've made one until proven otherwise.

### Inheritance

Defining a class as a specialised version of another — `Poodle(Dog)` gets everything
`Dog` has and overrides what differs. Use it for genuine "is-a" relationships; reach
for composition otherwise. See [TAMYMN-Inheritance.md](TAMYMN-Inheritance.md).

### Instance

One concrete object made from a class: the class is the blueprint, the instance is the
house. Each instance has its own attribute values — two `Dog`s, two names.
See [TAMYMN-Classes.md](TAMYMN-Classes.md).

### Integer

A whole number, positive or negative. In Python they're exact at any size — it's
floats, not ints, that carry rounding surprises.

### Interface

The set of methods an object promises to answer — the *what*, deliberately hiding the
*how*. Code written against an interface doesn't care which object shows up, which is
what makes parts swappable. See [TAMYMN-Encapsulation.md](TAMYMN-Encapsulation.md).

### Interpreter

The program that reads your Python source and executes it line by line — `python` on
the command line *is* the interpreter. No separate compile step: run it, and errors
appear when the offending line is reached.

### Iteration

One pass through a loop, and the general act of visiting each item of a collection in
turn. Most real programs are 10% clever ideas and 90% iterating over things.

## J

### JSON

JavaScript Object Notation: nested dictionaries and lists written as text —
`{"name": "Alice", "tags": ["admin"]}`. The format web APIs speak, and it maps
directly onto Python's dicts and lists. See [TAMYMN-FileIO.md](TAMYMN-FileIO.md).

## K

### Kernel

The live Python process behind a notebook, holding every variable you've defined this
session. "Restart kernel and run all" is the honesty test: if your notebook only works
because of leftover state, this is how you find out.
See [TAMYMN-Jupyter.md](TAMYMN-Jupyter.md).

## L

### Library

A collection of ready-made code you import instead of writing — pandas, matplotlib.
The skill isn't memorising libraries; it's knowing one exists, reading enough of its
docs to start, and testing what you build on it.

### List

Python's ordered, changeable sequence: `[1, 2, 3]`. Use it when order matters and
you'll be adding, removing, or walking through items — which is most of the time.
See [TAMYMN-Data-Structures.md](TAMYMN-Data-Structures.md).

### LLM

A Large Language Model — the engine inside ChatGPT, Claude, Copilot — trained on vast
text to predict what comes next, which turns out to produce remarkably useful prose and
code. It has no ground truth, only plausibility: hence confabulation, and hence the
verify habit. See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Loop

Code that repeats: `for` when you're visiting each item of something, `while` when
you're repeating until a condition changes. If your `while` condition can never become
false, that's an infinite loop — Ctrl+C gets you out.

## M

### Markdown

Plain text with light conventions — `# heading`, `**bold**`, backticks for code — that
renders as formatted documents. READMEs, notebooks, and this entire book are written in
it; ten minutes of learning covers years of use.
See [TAMYMN-Markdown.md](TAMYMN-Markdown.md).

### Merge

Bringing one branch's commits into another — `git merge fix-login` while on `main`.
Where both branches changed the same lines, Git stops and asks you to decide: that's a
merge conflict, not a disaster. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Merge conflict

Git found the same lines changed in both branches and refuses to guess. It marks the
clash in the file with `<<<<<<<` / `=======` / `>>>>>>>`; you keep what you want,
delete the markers, `git add`, `git commit`. That's the whole procedure.
See [TAMYMN-Git.md](TAMYMN-Git.md).

### Method

A function that lives on an object and works with its data — `name.upper()`,
`df.head()`. The dot means "ask this object to do something with what it knows".
See [TAMYMN-Classes.md](TAMYMN-Classes.md).

### Module

A single Python file that can be imported — `math`, or your own `utils.py`. The unit
of code organisation one level up from the function.

## N

### Namespace

The mapping from names to objects that determines what `x` means *here* — each module,
function, and class gets its own. Namespaces are why your `count` and pandas' `count`
can coexist without a fight.

### Notebook

A document mixing runnable code cells, their output, and Markdown prose — the standard
tool for data exploration, where seeing each step's result shapes the next step.
See [TAMYMN-Jupyter.md](TAMYMN-Jupyter.md).

## O

### Object

A bundle of data (attributes) and behaviour (methods) travelling together. In Python
*everything* is one — numbers, strings, functions, DataFrames — which is why the dot
works on all of them. See [TAMYMN-OOP.md](TAMYMN-OOP.md).

### Open source

Software whose source code is public to use, read, and modify — Python, Git, pandas,
Linux: your entire toolchain. Freedom to read the source is also a debugging superpower
you'll eventually use.

## P

### Package

A distributable bundle of modules — what you actually `pip install`. Also, more
narrowly, a directory of Python modules with an `__init__.py`.

### Parameter

A named input in a function's definition — `def greet(name):` declares the parameter
`name`. It's the labelled slot; the argument is what you drop into it when calling.
See [TAMYMN-Functions.md](TAMYMN-Functions.md).

### Path

The address of a file in the directory tree — absolute (`/home/alice/report.py`, from
the root) or relative (`data/sales.csv`, from where you are now). Half of all
"file not found" errors are a relative path resolved from a different directory than
you assumed. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Permissions

Per-file rules for who may read, write, or execute it. The reason `./script.sh` says
"permission denied" until you `chmod +x` it — the file exists; you just haven't marked
it runnable. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### pip

Python's package installer: `pip install pandas` fetches a library and its dependencies
from the Python Package Index. Run it inside a virtual environment, or every project on
your machine shares one tangled pile of packages.

### Plot

A visual encoding of data — positions, lengths, colours standing in for numbers — built
so a human can see the pattern a table hides. The chart type is a choice about what
comparison you want the eye to make.
See [TAMYMN-Visualisation.md](TAMYMN-Visualisation.md).

### Process

One running program, with its own memory and an ID the system tracks. Your notebook
kernel, your shell, and the server that won't release port 8000 are each a process —
and `kill` is how you end one that's misbehaving.
See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Prompt (AI)

What you send an LLM — and the quality lever you actually control. A good one supplies
context, states what you already know or constrain, and defines the size and shape of
answer you want. See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Prompt (shell)

The `$` (or `%`, or `>`) the terminal prints when it's ready for your next command.
No prompt showing means something is still running — or waiting for input you didn't
know it wanted. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Prompt engineering

The craft of writing prompts that leave the model as little guesswork as possible:
name the files, state the constraints, give acceptance criteria. Less magic
incantation, more clear specification — computational thinking applied to delegation.
See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Pull

`git pull`: fetch the remote's new commits and merge them into your branch — how you
catch up with work that happened elsewhere. Push rejected? Pull first, resolve, push
again. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Push

`git push`: send your local commits to the remote so they're backed up and visible to
others. Until you push, your commits exist only on your machine.
See [TAMYMN-Git.md](TAMYMN-Git.md).

## Q

### Query

A question you ask a database, written in SQL: `SELECT name FROM users WHERE age > 30`.
You describe *what* you want; the database figures out *how* to get it.
See [TAMYMN-SQLite.md](TAMYMN-SQLite.md).

## R

### README

The file at a project's root that tells a newcomer what this is, why it exists, and how
to run it — the front door of the repository, written in Markdown. If a project has
exactly one document, it's this one.

### Regression

A thing that used to work and now doesn't, broken by a later change. Test suites exist
mainly to catch regressions the moment they're introduced — including a "regression
test" you add for every bug you fix, so it can never sneak back.
See [TAMYMN-Testing.md](TAMYMN-Testing.md).

### Remote

A copy of your repository living elsewhere — usually GitHub — that you push to and pull
from. `origin` is just the default nickname for the one you cloned from.
See [TAMYMN-Git.md](TAMYMN-Git.md).

### REPL

The Read-Eval-Print Loop: type `python`, get `>>>`, and every expression you enter is
evaluated immediately. The cheapest experiment bench you own — three seconds to check
what a function actually returns beats three minutes of guessing.

### Repository

A project directory whose entire history Git tracks — the hidden `.git/` folder *is*
the repository. Delete that folder and the history is gone; copy the directory and it
all comes along. See [TAMYMN-Git.md](TAMYMN-Git.md).

### Return value

What a function hands back to its caller — the whole point of calling it. A function
with no `return` gives you `None`, which is the story behind half of all
"'NoneType' object has no attribute..." errors.
See [TAMYMN-Functions.md](TAMYMN-Functions.md).

### Root

Two meanings: the top of the filesystem tree (`/`), and the all-powerful admin account
that `sudo` briefly lets you borrow — which can delete anything, and will, without
asking twice. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

## S

### Scope

The region of code where a name is visible. A variable assigned inside a function
exists only there — which is a feature: functions that don't leak or grab surrounding
state are the ones you can reason about and test.
See [TAMYMN-Functions.md](TAMYMN-Functions.md).

### Script

A file of code meant to be run top to bottom — `python analyse.py` — as opposed to a
notebook you poke at interactively. When an analysis needs to run reliably, on a
schedule, or by someone else, it becomes a script.

### Series

One labelled column of data — what you get when you select a single column from a
DataFrame. Most pandas operations flow through it, so recognising "this is a Series
now" explains a lot of behaviour. See [TAMYMN-Pandas.md](TAMYMN-Pandas.md).

### Server

A program (or the machine running it) that waits for requests and answers them — web
pages, API responses, database results. Every URL you visit is a conversation with one.

### Set

Python's unordered collection of unique values: `{1, 2, 3}`. Duplicates vanish on
entry, and membership checks are fast — the tool for "have I seen this before?".
See [TAMYMN-Data-Structures.md](TAMYMN-Data-Structures.md).

### Shell

The program that reads your typed commands, runs them, and shows the results — bash and
zsh are the common ones. The terminal is the window; the shell is the interpreter
living inside it. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### SQL

Structured Query Language, the standard language of databases — and unusually for this
industry, a skill from the 1970s that's still everywhere. You declare what data you
want; the database works out how. See [TAMYMN-SQLite.md](TAMYMN-SQLite.md).

### SSH

Secure Shell: an encrypted connection giving you a command line on a distant machine,
plus the key-pair authentication Git hosts use instead of passwords. How you'll reach
every server you ever administer. See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Staging area

Git's middle place between your edited files and history — `git add` puts changes here,
composing exactly what the next commit will contain. It's why you can edit five files
and commit two: the snapshot is composed, not automatic.
See [TAMYMN-Git.md](TAMYMN-Git.md).

### Statement

A complete instruction that *does* something — an assignment, an `if`, a `return` — as
opposed to an expression, which *is* something (a value). A program is statements;
statements are built from expressions.

### String

Text as a value: `"hello"`. Immutable in Python — every `.upper()`, `.strip()`,
`.replace()` returns a *new* string, which is why `name.upper()` alone changes
nothing until you assign the result.

### Syntax

The grammar of the language — the colons, indentation, and brackets Python demands
before it will even try to run your code. Syntax errors are the friendly ones: caught
immediately, at the exact line, before any damage.

## T

### TDD

Test-Driven Development: write a failing test *first*, write the minimum code to pass
it, clean up, repeat. The failing test proves the test can fail — and "write the test,
let the AI make it pass" is one of the strongest agent workflows there is.
See [TAMYMN-TDD.md](TAMYMN-TDD.md).

### Terminal

The window your shell runs in — where you type commands and read output. Living here
comfortably is the gateway skill: Git, pip, pytest, and AI agents all speak terminal.
See [TAMYMN-Linux.md](TAMYMN-Linux.md).

### Test

Code that runs your code and asserts the result is right — an executable, re-runnable
claim about behaviour. Tests are what let you change things without fear, and the
machine that verifies AI-written work at scale.
See [TAMYMN-Testing.md](TAMYMN-Testing.md).

### Test suite

All your tests, run as one command (`pytest`). Its value is the binary verdict: green
means every claim still holds; one red means stop and look. Guard it — an agent that
"fixes" a failure by editing the test has moved your finish line.
See [TAMYMN-Testing.md](TAMYMN-Testing.md).

### Token

The chunk of text — roughly three-quarters of a word — that LLMs actually read and
write. Models have a limited token window, which is why long conversations "forget"
their beginnings and why context is a budget you spend deliberately.
See [TAMYMN-AI-Agents.md](TAMYMN-AI-Agents.md).

### Tuple

Python's immutable sequence: `(lat, lon)`. Use it for fixed-shape bundles that
shouldn't change — and note that functions returning "two values" are really returning
one tuple. See [TAMYMN-Data-Structures.md](TAMYMN-Data-Structures.md).

### Type

What kind of value something is — `int`, `str`, `list`, `DataFrame` — which determines
what you can do with it. Half of all beginner errors are type mismatches, like the
classic `"5" + 3`; `type(x)` answers the question directly.

## U

### URL

A web address: `https://example.com/search?q=pandas` is a protocol, a server, a path
on that server, and query parameters. APIs and web scraping both start with
constructing the right one.

## V

### Value

The actual piece of data — `42`, `"hello"`, `[1, 2]` — as distinct from any variable
naming it. Several variables can name one value, which is why mutating a list through
one name surprises you through the other.

### Variable

A name bound to a value: `count = 3` doesn't put 3 in a box, it sticks the label
`count` on the value 3. Names-pointing-at-values is the model that later explains why
two variables can share one list. See [TAMYMN-Python.md](TAMYMN-Python.md).

### Virtual environment

A private, per-project set of installed packages (`python -m venv .venv`, then
activate), so project A's pandas upgrade can't break project B. Non-negotiable
hygiene: one project, one environment, always.

## W

### Working directory

Two related meanings: the directory your shell is currently *in* (relative paths
resolve from here), and in Git, the files as you see them now — the editable place, as
opposed to the staging area and history. See [TAMYMN-Git.md](TAMYMN-Git.md).

---

That covers the vocabulary! Anything not here follows the same pattern: context, what
you already know, size of answer — ask precisely, verify against the chapter.
