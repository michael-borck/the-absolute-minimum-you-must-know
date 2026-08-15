# Data Structures: The Absolute Minimum You Must Know

Choosing a data structure is choosing what your program is fast at — and in Python that
means choosing between four built-in shapes: list, tuple, dict, set. Pick by asking one
question: **how will I look things up?** By position → list. By key → dict. "Have I seen
this?" → set. Fixed record → tuple. That question, and what each shape costs, is this page.

## The One Idea Underneath: O(1) vs O(n)

A list finds things by *scanning* — checking membership means walking every element, O(n).
Dicts and sets find things by *hashing* — the key's hash says exactly where to look, so
lookup, insert, and `in` are O(1): the same cost at ten items or ten million. Every
pick-the-right-shape decision on this page is really this one distinction wearing four
different outfits.

## List: An Ordered Sequence, Fast by Position

Use a list when *order matters* and you access items by position or iterate over all of
them. Append to the end and index anywhere in O(1); but `in`, `.index()`, and
`.insert(0, x)` all scan or shift — O(n).

```python
>>> tasks = ["write", "review"]
>>> tasks.append("ship")          # O(1): the idiomatic way to grow a list
>>> tasks[0], tasks[-1]           # O(1): by position, either end
('write', 'ship')
>>> "review" in tasks             # O(n): scans — fine once, deadly in a loop
True
```

## Tuple: A Frozen Record

A tuple is an immutable sequence — use it when the *positions mean something*: a
coordinate, an (id, name) pair, a function returning two values. Immutability is a
feature twice over: nothing can mutate your record behind your back, and a tuple is
hashable, so it can be a dict key or set member when a list can't.

```python
>>> point = (115.86, -31.95)              # (longitude, latitude): position = meaning
>>> lon, lat = point                      # unpack into names
>>> cities = {point: "Perth"}             # hashable → allowed as a dict key
>>> cities[(115.86, -31.95)]
'Perth'
```

## Dict: Look Things Up by Key

The dict is Python's workhorse: it maps keys to values with O(1) lookup, insert, and
delete, and it remembers insertion order. If you're pairing one thing with another —
name→price, id→record, word→count — it's a dict.

```python
>>> price = {"apple": 3.0, "pear": 4.5}
>>> price["cherry"] = 12.0                # O(1) insert
>>> price["pear"]                         # O(1) lookup — KeyError if missing
4.5
>>> price.get("plum", 0.0)                # lookup with a default instead of an error
0.0
>>> sorted(price)                         # iterating a dict yields its keys
['apple', 'cherry', 'pear']
```

## Set: Membership and Uniqueness

A set is a dict without the values: unordered, unique elements, O(1) membership. Reach for
it whenever the question is "have I seen this before?" or "which items are in A but not
B?" — the set operators answer in one line what loops answer in five.

```python
>>> seen = {"ana", "ben"}
>>> seen.add("ana")                       # already present — sets ignore duplicates
>>> sorted(seen)                          # unordered, so sort before displaying
['ana', 'ben']
>>> paid = {"ben", "cli"}
>>> sorted(seen - paid), sorted(seen & paid)   # difference and intersection
(['ana'], ['ben'])
```

Careful: sets don't promise a printing order — `sorted()` first whenever you show one.
And `{}` is an empty *dict*; an empty set is `set()`.

## The Classic Mistake: Scanning a List a Thousand Times

The single most common performance bug in beginner (and LLM) Python: `in` on a list,
inside a loop. Each check scans the whole list — an accidental O(n²) hiding in one
innocent keyword. The fix is one line: build a set once, then every check is O(1).

```python
>>> subscribers = [f"user{i}@example.com" for i in range(10_000)]
>>> signups = [f"user{i}@example.com" for i in range(9_995, 10_005)]
>>> [s for s in signups if s in subscribers]        # works, but 10 scans x 10,000 items
['user9995@example.com', 'user9996@example.com', 'user9997@example.com', 'user9998@example.com', 'user9999@example.com']
>>> sub_set = set(subscribers)                      # build ONCE, outside any loop...
>>> [s for s in signups if s in sub_set]            # ...then each check is O(1)
['user9995@example.com', 'user9996@example.com', 'user9997@example.com', 'user9998@example.com', 'user9999@example.com']
```

Same answer; at real scale (a million subscribers, a million signups) the first version
does ~10¹² comparisons and the second does ~10⁶ hashes. The symptom to watch for in any
code, yours or an AI's: `x in some_list` or `some_list.index(x)` inside a loop.

## Directing the Machine

AI-generated Python defaults to lists for everything, because lists dominate its training
data. Name the shape and the complexity requirement and you'll get the right structure;
stay vague and you'll get the scan.

Vague:

```
"Write a function that removes customers who unsubscribed from my customer list."
```

Informed:

```
"customers is a list of ~1M (id, email) tuples; unsubscribed is a list of ~100k ids.
Keep customers whose id is not in unsubscribed, preserving order. Convert
unsubscribed to a set first so each check is O(1) — no `in list` inside the loop."
```

## Spot the Confabulation

An AI explains why your lookup code is already fast:

```python
def is_subscriber(email, subscribers):
    # Fast: Python lists are hash-indexed, so `in` is O(1) on average.
    # Converting to a set here would just waste memory.
    return email in subscribers
```

<details><summary>What's wrong?</summary>

The claim is confidently backwards. Python lists are *arrays*, not hash tables — `in` on
a list is O(n), scanning element by element. It's dicts and sets that are hash-indexed
with O(1) membership. The "would just waste memory" advice compounds the error: if this
function is called many times, building `set(subscribers)` **once** (outside the
function) is exactly the right trade — a modest memory cost for turning every lookup
from a full scan into a single hash. This is a textbook LLM confabulation: real
vocabulary ("hash-indexed", "O(1) on average" — true of dicts!) attached to the wrong
noun, stated with total confidence.

</details>

## Where to Practice

- **[Exercism](https://exercism.org)** — free; its Python track has dedicated exercise
  sets on lists, dicts, sets, and tuples, each with a test suite that tells you instantly
  whether your shape choice actually behaves.
- **[Advent of Code](https://adventofcode.com)** — free puzzles (every year since 2015)
  that punish the wrong structure: part two routinely scales n up until list-scanning
  solutions take hours and dict/set solutions take milliseconds.

## Quick Reference

| Shape | Reach for it when | O(1) | O(n) |
|---|---|---|---|
| `list` `[1, 2]` | order matters; access by position | `append`, `lst[i]` | `in`, `.index`, `.insert(0, x)` |
| `tuple` `(1, 2)` | fixed record; needs to be a dict key | indexing, unpacking | `in` |
| `dict` `{"a": 1}` | pair keys with values | `d[k]`, `d.get(k)`, insert, delete | searching by *value* |
| `set` `{1, 2}` | membership, uniqueness, `- & \|` | `in`, `add`, `discard` | — |

One-line conversions: `set(lst)` dedupes, `list(d)` gives keys, `sorted(s)` gives an
ordered list. Empty set is `set()` — `{}` is an empty dict.

That covers the absolute minimum! You can now pick the shape that makes your lookups O(1)
instead of O(n), and spot the scanned-list mistake in any code, human or AI — the rest of
the `collections` module is variations on these four.
