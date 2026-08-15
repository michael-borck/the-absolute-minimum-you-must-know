# Functions in Python: The Absolute Minimum You Must Know

Functions are how you name a piece of work so you can reuse it, test it, and hand it to
someone else — human or AI. Effective use rests on about six ideas: `def`, `return`,
keyword arguments, `*args`/`**kwargs`, scope, and functions-as-values — all on this page.

## def, Parameters, Arguments

```python
>>> def greet(name, punctuation="!"):
...     """Return a greeting for name."""
...     return "Hello, " + name + punctuation
>>> greet("Ada")
'Hello, Ada!'
```

Vocabulary that stops half of all confusion: **parameters** are the names in the `def`
line (`name`, `punctuation`); **arguments** are the values you pass in the call (`"Ada"`).
The triple-quoted line is the **docstring** — one sentence on what the function *returns*,
shown by `help(greet)`.

## return — and the None Trap

`return` hands a value back to the caller and ends the function. A function that never
hits a `return` gives back `None` — silently. The classic beginner trap is printing
instead of returning:

```python
>>> def add(x, y):
...     print(x + y)          # shows the answer... but returns nothing
>>> result = add(2, 3)
5
>>> print(result)
None
```

`add(2, 3) + 10` now crashes with `TypeError: unsupported operand ... 'NoneType'`. The
rule: **functions return values; only the outermost layer of a program prints.** If you
see a `TypeError` mentioning `NoneType`, look for a missing `return` first.

## Keyword Arguments and Defaults

Any argument can be passed by name, in any order — and parameters with defaults become
optional:

```python
>>> def report(name, score, decimals=1):
...     return f"{name}: {round(score, decimals)}"
>>> report("Ada", 97.456)
'Ada: 97.5'
>>> report(score=97.456, name="Ada", decimals=2)
'Ada: 97.46'
```

Calls with keywords read like documentation — `report(score=97.456, ...)` needs no
explaining. One warning inherited from the Python doc: never use a mutable default
(`def f(x, acc=[])`) — the list is created once and shared across calls. Default to
`None` and create it inside.

## *args and **kwargs in One Breath

`*args` scoops up any extra positional arguments into a tuple; `**kwargs` scoops up any
extra keyword arguments into a dict. That's the whole trick:

```python
>>> def summarise(*args, **kwargs):
...     return f"{len(args)} positional, keywords: {sorted(kwargs)}"
>>> summarise(1, 2, 3, mode="fast", debug=True)
"3 positional, keywords: ['debug', 'mode']"
```

You'll *write* these rarely, but you'll *read* them everywhere — they're how wrappers and
frameworks accept "whatever arguments you like and pass them along" (`f(*args, **kwargs)`
forwards them).

## Scope: LEGB in Plain Words

When Python sees a name, it looks in four places, innermost first: **L**ocal (this
function), **E**nclosing (the function this one is nested inside, if any), **G**lobal
(this file), **B**uilt-in (`len`, `print`). First hit wins. And crucially: *assigning* to
a name inside a function makes it local — it never quietly overwrites the global:

```python
>>> greeting = "hi"
>>> def shout():
...     greeting = "HEY"      # a brand-new LOCAL name
...     return greeting
>>> shout()
'HEY'
>>> greeting                  # the global is untouched
'hi'
```

That's a feature: functions can't trample your file's variables by accident. When you
think you need `global`, you almost always actually want to pass the value in as an
argument and `return` the new one out.

## Functions Are Values

A `def` creates an object and binds a name to it — like any other assignment. So
functions can be stored, passed, and returned:

```python
>>> def double(n):
...     return n * 2
>>> twice = double            # no parentheses: the function itself, not a call
>>> twice(5)
10
>>> sorted(["bb", "a", "ccc"], key=len)
['a', 'bb', 'ccc']
```

`key=len` passes the `len` function *itself* into `sorted`. Parentheses are the moment of
calling; a bare function name is a value you can hand around. This one idea unlocks
`sorted(key=...)`, callbacks, and everything in the functional programming doc.

## Directing the Machine

The informed prompt specifies the function's *contract* — parameters, defaults, and what
it returns — using this page's vocabulary. The AI then writes to a spec instead of
inventing one, and you can check the result by calling it.

Vague:

```
"write a function to format scores"
```

Informed:

```
"Write format_score(name, score, decimals=1) that RETURNS a string like 'Ada: 97.5'
(no printing). score may be None — return 'Ada: absent' in that case. Include a
one-line docstring and two doctest examples."
```

## Spot the Confabulation

An AI assistant writes a helper and uses it:

```
def calculate_total(prices):
    total = sum(prices)
    print(f"Total: {total}")

grand_total = calculate_total([9.99, 4.50]) + calculate_total([12.00])
print(f"Grand total: {grand_total}")
```

<details><summary>What's wrong?</summary>

`calculate_total` **prints** the total but never **returns** it, so every call evaluates
to `None` — and `None + None` raises `TypeError: unsupported operand type(s)`. The
output even looks right up to the crash, because the prints still happen. Fix: `return
total`, and let the caller decide what to print. Print-instead-of-return is one of the
most common bugs in AI-generated helper functions — check the `return` line first.

</details>

## Where to Practice

- **[Python Tutor](https://pythontutor.com)** — free, no signup: paste code and step
  through it while it draws each function's frame, its local names, and what they point
  at. The fastest way to *see* scope and call/return happen.
- **[Exercism's Python track](https://exercism.org/tracks/python)** — free exercises
  where every task is "make these tests pass by writing a function with this contract".

## Quick Reference

| Idea | The minimum |
|---|---|
| Define | `def name(params):` + docstring; parameters in the def, arguments in the call |
| Return | `return value`; no return means `None` — print at the edges, return inside |
| Defaults | `def f(x, n=1):` makes `n` optional; never use a mutable default |
| Keywords | `f(score=97, name="Ada")` — any order, self-documenting |
| `*args` / `**kwargs` | extra positionals as a tuple / extra keywords as a dict |
| Scope | LEGB lookup; assignment inside a function creates a *local* name |
| Instead of `global` | pass values in as arguments, return new values out |
| Functions as values | bare name = the function itself; `sorted(words, key=len)` |

That covers the absolute minimum! You can now define a function with a clear contract,
predict what any call returns, and spot the missing-`return` bug on sight — everything
else (decorators, generators, closures) builds on exactly these ideas.
