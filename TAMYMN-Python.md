# Python: The Absolute Minimum You Must Know

Python looks like a huge language, but effective daily use rests on about eight ideas —
names, core types, truthiness, `for`/`if`, comprehensions, imports, and one famous gotcha
— all on this page. Master these and every library you meet is just more of the same.

## Variables Are Names, Not Boxes

A Python variable is a **name bound to an [object](GLOSSARY.md#object)**, not a box containing a value.
Assignment never copies; it points another name at the same object:

```python
>>> a = [1, 2, 3]
>>> b = a          # b is a second name for the SAME list
>>> b.append(4)
>>> a
[1, 2, 3, 4]
```

That one model explains half of Python's surprises. Want an actual copy? Ask for one:
`b = a.copy()`. Numbers and strings never surprise you this way — they're **immutable**.

## The Core Types

```python
>>> price = 9.99                    # float (42 would be an int)
>>> name = "Ada"                    # str — immutable
>>> tags = ["new", "sale"]          # list — ordered, mutable
>>> point = (3, 4)                  # tuple — ordered, immutable
>>> user = {"name": "Ada", "id": 7} # dict — key -> value lookup
>>> user["name"]
'Ada'
```

Lists hold sequences you'll [loop](GLOSSARY.md#loop) over; dicts hold things you look up by key. Those two plus
strings do 90% of everyday work. `None` is the "no value here" object — test with `is None`.

## f-strings: How You Build Text

Put an `f` before the quote and drop expressions into `{}`:

```python
>>> name, score = "Ada", 97.4567
>>> f"{name} scored {score:.1f}%"
'Ada scored 97.5%'
```

The `:.1f` is a format spec — one decimal place. f-strings replaced every older way of
formatting (`"%s" % name`, `.format()`); if an AI hands you those, ask for f-strings.

## Truthiness

Every object is truthy or falsy: empty things (`""`, `[]`, `{}`, `0`, `None`) are false,
non-empty things are true. So idiomatic Python tests the object itself — you'll rarely see
`if len(tags) == 0:` because `if not tags:` says the same thing:

```python
>>> tags = []
>>> if not tags:
...     print("nothing to show")
nothing to show
```

## for and if: Indentation Is the Syntax

Blocks are defined by indentation — no braces, no `end` — and a `for` loop walks any
collection directly, no index needed:

```python
>>> for word in ["tea", "coffee"]:
...     if len(word) > 3:
...         print(word, "is long")
...     else:
...         print(word, "is short")
tea is short
coffee is long
```

Need positions too? `for i, word in enumerate(words):`. Numbers? `range(5)` gives 0–4.

## Comprehensions: Loops as Expressions

A comprehension builds a new list (or dict) in one readable line — it's the loop above,
folded into the brackets:

```python
>>> nums = [3, 1, 4, 1, 5]
>>> [n * n for n in nums if n > 2]
[9, 16, 25]
>>> {word: len(word) for word in ["tea", "coffee"]}
{'tea': 3, 'coffee': 6}
```

Read it left to right — "n squared, for each n in nums, if n > 2" — and reach for one
whenever you're transforming a collection.

## Importing

```python
>>> import math
>>> math.sqrt(16)
4.0
```

`import math` brings in the [module](GLOSSARY.md#module) and you use `math.sqrt`; `from pathlib import Path`
pulls one name out. Avoid `from module import *` — nobody can tell where names came from.

## Script vs REPL

The `>>>` blocks on this page are **REPL** transcripts — run `python3` alone and you get a
[prompt](GLOSSARY.md#prompt-shell): type an [expression](GLOSSARY.md#expression), see its value. It's your scratchpad. Real programs live in files
— `python3 report.py` runs top to bottom, printing nothing you didn't `print()`. The line
you'll see everywhere:

```
if __name__ == "__main__":   # true only when THIS file is the one being run,
    main()                   # not when it's merely imported by another file
```

## The Gotcha: Mutable Default Arguments

Default values are evaluated **once**, when the [function](GLOSSARY.md#function) is defined — not on every call.
A mutable default is therefore shared between calls:

```python
>>> def add_task(task, tasks=[]):
...     tasks.append(task)
...     return tasks
>>> add_task("write report")
['write report']
>>> add_task("send email")          # a fresh list? No — the SAME list
['write report', 'send email']
```

The standard idiom: default to `None` (`def add_task(task, tasks=None):`) and create the
list inside — `if tasks is None: tasks = []` — so every call gets a fresh one.

## Directing the Machine

An informed prompt names the ideas on this page — the types involved, the shape of the
data, the idiom you want — so the AI writes the code you meant instead of guessing.

Vague:

```
"write python to process my data"
```

Informed:

```
"I have a list of dicts like {'name': 'Ada', 'score': 97.5}. Give me a dict
comprehension mapping name -> score, skipping entries where score is None,
and an f-string that prints each score to one decimal place."
```

## Spot the Confabulation

An AI assistant explains how to customise settings without touching the original:

```
DEFAULT_SETTINGS = {"verbose": False, "retries": 3}

def get_settings():
    settings = DEFAULT_SETTINGS   # take a copy of the defaults
    settings["verbose"] = True    # customise our copy
    return settings
```

<details><summary>What's wrong?</summary>

Assignment doesn't copy — it binds a second name to the **same dict**, so this silently
corrupts the shared defaults for the whole program: `DEFAULT_SETTINGS["verbose"]` is now
`True` everywhere. The fix is an explicit `DEFAULT_SETTINGS.copy()`. Names, not boxes.

</details>

## Where to Practice

- **[futurecoder](https://futurecoder.io)** — free, no-signup course that runs Python in
  your browser, with a debugger that shows what each name points at.
- **[Exercism's Python track](https://exercism.org/tracks/python)** — free small exercises
  with automated tests and human mentoring; ideal once the [syntax](GLOSSARY.md#syntax) feels stable.

## Quick Reference

| Idea | The minimum |
|---|---|
| Assignment | binds a name to an object — never copies (`b = a.copy()` copies) |
| Core types | `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `None` |
| f-string | `f"{name} scored {score:.1f}%"` |
| Truthiness | empty/zero/`None` are false — write `if not tags:` |
| `for` | walks any collection; `enumerate` for indexes, `range(n)` for numbers |
| Comprehension | `[n*n for n in nums if n > 2]` — transform + filter in one line |
| Import | `import math` → `math.sqrt`; `from pathlib import Path` |
| REPL vs script | `python3` to experiment; `python3 file.py` to run a program |
| The gotcha | mutable defaults are shared across calls — default to `None` instead |

That covers the absolute minimum! You can now read and write idiomatic Python, explain its
classic trap, and direct an AI at the rest — everything else is `help(thing)` away.
