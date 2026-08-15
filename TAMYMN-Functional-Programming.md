# Functional Programming in Python: The Absolute Minimum You Must Know

Functional programming sounds academic, but its working core is one habit — write
functions that compute results instead of changing things — plus three tools: `sorted`
with a `key`, comprehensions, and `lambda`. All on this page, and the habit pays off
double in the AI age: pure functions are the easiest code to test, and to delegate.

## The Habit: Functions Without Side Effects

A **pure function** takes inputs and returns a result — nothing else. It doesn't modify
its arguments, touch globals, print, or write files. Same inputs, same answer, every
time:

```python
>>> def total_with_tax(prices, rate):
...     return round(sum(prices) * (1 + rate), 2)
>>> total_with_tax([10.0, 20.0], 0.10)
33.0
>>> total_with_tax([10.0, 20.0], 0.10)      # forever
33.0
```

Everything a function *does* besides returning — mutating a list it was given, updating a
global, printing — is a **side effect**. Side effects aren't evil (a program with none
does nothing you can see), but they're where bugs hide, so the discipline is: compute in
pure functions, and push the printing and file-writing to the thin outer edge of the
program. A useful tell in the standard library: `sorted(nums)` *returns* a new sorted
list (pure); `nums.sort()` *changes* the list and returns `None` (side effect).

## map/filter vs Comprehensions

The classic functional tools exist in Python: `map` applies a function to every element,
`filter` keeps elements passing a test. Both return lazy iterators, so you wrap them in
`list()` to see the values:

```python
>>> nums = [1, 2, 3, 4]
>>> list(map(lambda n: n * n, nums))
[1, 4, 9, 16]
>>> list(filter(lambda n: n % 2 == 0, nums))
[2, 4]
>>> [n * n for n in nums]                   # the same, as comprehensions
[1, 4, 9, 16]
>>> [n * n for n in nums if n % 2 == 0]     # map AND filter in one line
[4, 16]
```

Python prefers the comprehension, and for cause: it reads as English, needs no `lambda`,
no `list()` wrapper, and does map-plus-filter in a single expression. Read `map`/`filter`
fluently — AI-generated and JavaScript-influenced code is full of them — but *write*
comprehensions. Same functional idea (build a new collection, don't mutate the old one),
better clothes.

## sorted(key=...) — the Everyday Higher-Order Function

Functions are values, so you can pass one *into* another function. The place you'll do
this daily is `sorted`: the `key` function is called on each element, and the results
decide the order — the original data is untouched:

```python
>>> words = ["banana", "fig", "apple"]
>>> sorted(words, key=len)
['fig', 'apple', 'banana']
>>> students = [("Ada", 97), ("Cy", 62), ("Bo", 88)]
>>> sorted(students, key=lambda s: s[1], reverse=True)
[('Ada', 97), ('Bo', 88), ('Cy', 62)]
```

The same `key=` idea powers `min`, `max`, and `list.sort` — learn it once, use it
everywhere.

## lambda in One Breath

`lambda s: s[1]` is a nameless one-expression function: parameters before the colon,
returned expression after. That's all it is — `def` without the name or the `return`
keyword. Use it for tiny throwaway keys like the one above; the moment logic needs two
steps or a name would help the reader, promote it to a `def`.

## Why Pure Functions Win in the AI Age

A pure function is a **contract**: inputs in, output back, nothing else touched. That
makes it trivially testable — call it, check the answer, no setup, no cleanup, no
database, no "it depends what ran before":

```python
>>> def slug(title):
...     return title.lower().replace(" ", "-")
>>> slug("File IO Basics")                  # the whole test suite is calls like this
'file-io-basics'
```

The same property makes pure functions the ideal unit to delegate to an AI: the contract
*is* the prompt ("write `slug(title)` that returns..."), and verifying the result is
running the doctests — you never have to trust it, you check it. Code tangled with
globals and hidden state gives you neither the easy prompt nor the easy check.

## Directing the Machine

The informed prompt asks for a *pure* function with a stated contract, and names the
idiom you want back — comprehension, `sorted(key=...)` — so you get testable Python
rather than a script full of side effects.

Vague:

```
"write code to sort my products and update the prices"
```

Informed:

```
"Write a pure function apply_discount(products, rate) — products is a list of
(name, price) tuples. Return a NEW list, prices reduced by rate and rounded to
2 dp, sorted by price ascending with sorted(key=...). Don't mutate the input;
no printing. Include doctests."
```

## Spot the Confabulation

An AI assistant demonstrates `map`:

```
squares = map(lambda n: n * n, [1, 2, 3])
print(list(squares))    # [1, 4, 9]
print(list(squares))    # [1, 4, 9] — reuse it as often as you like
```

<details><summary>What's wrong?</summary>

`map` returns a **lazy iterator**, not a list, and an iterator can be consumed exactly
once. The second `list(squares)` prints `[]` — the values were used up by the first.
(In Python 2 `map` really did return a list, which is exactly why an LLM trained on
decades of both confidently asserts this.) If you need the values more than once,
materialise them — `squares = list(map(...))` — or sidestep the whole issue with the
comprehension `[n * n for n in [1, 2, 3]]`, which builds a real list.

</details>

## Where to Practice

- **[Exercism's Python track](https://exercism.org/tracks/python)** — free; many
  exercises are exactly "transform this collection", and mentors will nudge imperative
  loop solutions toward comprehensions and `sorted(key=...)`.
- **[Project Euler](https://projecteuler.net)** — free maths-flavoured problems that are
  natural pure functions: inputs in, one answer out, perfect for comprehension practice.

## Quick Reference

| Idea | The minimum |
|---|---|
| Pure function | returns a result; doesn't mutate, print, or touch globals |
| Side effects | allowed, but pushed to the program's thin outer edge |
| `sorted(xs)` vs `xs.sort()` | new list (pure) vs in-place mutation returning `None` |
| `map(f, xs)` / `filter(f, xs)` | lazy iterators — read them, but prefer... |
| Comprehension | `[f(x) for x in xs if cond(x)]` — map + filter, readable |
| `sorted(key=...)` | `sorted(students, key=lambda s: s[1], reverse=True)` |
| `lambda` | one-expression nameless function; promote to `def` when it grows |
| Iterator trap | `map`/`filter` results are consumed once — `list()` to keep them |
| AI leverage | a pure function's contract is the prompt; its doctests are the check |

That covers the absolute minimum! You can now compute with pure functions, transform
collections the Pythonic way, and hand an AI a contract it can't weasel out of —
`functools` and `itertools` are just more tools for the same habit.
