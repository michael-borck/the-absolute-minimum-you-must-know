# Algorithms: The Absolute Minimum You Must Know

An algorithm is a finite, unambiguous recipe: input → steps → output. Effective thinking
about them rests on three ideas — correctness first, scaling second, measurement always —
all on this page. You'll rarely write a classic algorithm from scratch anymore, but you'll
constantly judge the ones an AI hands you, and these three ideas are the criteria.

## Correctness Before Speed

A fast wrong answer is worthless, so correctness comes first — and correctness means
*tested*, not *looks right*. State what the algorithm promises for every input, especially
the awkward ones — empty, one element, target absent, target at each end: that's where
humans and LLMs alike write their bugs. Here's linear search, its promise as doctests —
the tests *are* the specification:

```python
def linear_search(items, target):
    """Return the index of target in items, or -1 — by checking each in turn."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1
```

```python
>>> linear_search([7, 3, 9], 9)
2
>>> linear_search([7, 3, 9], 4)      # absent
-1
>>> linear_search([], 4)             # empty — the classic crash site
-1
```

## Big-O: "How Does It Scale?"

Big-O answers one question: **when the input gets n times bigger, how much slower does
this get?** Ignore constants and small terms; watch the shape:

- **O(1)** — constant: same cost at any size (dict lookup).
- **O(log n)** — halving: doubling the input adds *one* step (binary search).
- **O(n)** — linear: double the input, double the work (a single loop).
- **O(n log n)** — sort territory: what good sorting costs (`sorted()`).
- **O(n²)** — quadratic: double the input, *quadruple* the work (a loop inside a loop).

The tell in code: one pass over the data is O(n); a loop nested inside a loop over the
same data is O(n²). And an innocent-looking `in some_list` or `.index()` *inside* a loop
is a hidden inner loop — that's the most common accidental O(n²) in real code.

## The Canonical Example: Linear vs Binary Search

If the list is **sorted**, you can do enormously better than checking every item: look at
the middle, and half the list is eliminated either way. That's binary search — O(log n).

```python
def binary_search(items, target):
    """Return the index of target in SORTED items, or -1 — by halving the field."""
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

```python
>>> haystack = list(range(0, 2_000_000, 2))    # one million sorted even numbers
>>> linear_search(haystack, 1_999_998)         # worst case: it's the last one
999999
>>> binary_search(haystack, 1_999_998)         # same answer...
999999
>>> binary_search(haystack, 1_999_999)         # odd number: correctly absent
-1
```

Same answers — wildly different work, as the next section shows. The catch: binary search
demands sorted input, and *silently returns garbage on unsorted input*. Sorting first
costs O(n log n), so it only pays off when you'll search the same data many times.

## Measure, Don't Guess

Big-O is the theory; counting actual steps is the experiment. Instrument the loop and the
gap stops being abstract:

```python
def binary_steps(items, target):
    """binary_search, but returning how many items it examined."""
    lo, hi, steps = 0, len(items) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if items[mid] == target:
            return steps
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps
```

```python
>>> haystack = list(range(0, 2_000_000, 2))               # a million items...
>>> binary_steps(haystack, 1_999_998)                     # ...examined: twenty
20
>>> doubled = list(range(0, 4_000_000, 2))                # two million items...
>>> binary_steps(doubled, 3_999_998)                      # ...costs ONE more step
21
```

Linear search examined all one million items to find that last element; binary search
examined **twenty**, and doubling the input cost it exactly one more step. The same habit
applies to wall-clock time: run `python -m timeit` on realistic data before believing any
speed claim — constants, caches, and Python's C-implemented built-ins routinely make the
"slower" big-O the faster program at your actual n.

## When O(n²) Is Perfectly Fine

Big-O only bites when n is big. A double loop over 100 configuration entries is 10,000
steps — microseconds; the same shape over ten million log lines is 10¹⁴ steps — days. So
before optimising, ask: **what is n, today and in a year?** For small, bounded n, the
simple quadratic version that's obviously correct beats the clever one that needs a
comment. Optimise the algorithm when n is large and growing; otherwise, for the reader.

## Directing the Machine

AI assistants produce much better algorithmic code when the prompt states the complexity
requirement and the data's properties — otherwise they default to the first workable loop,
and "workable" at n=10 can be catastrophic at n=10,000,000.

Vague:

```
"Write a function to check which of my ids are in this big list."
```

Informed:

```
"ids has ~50 items; sorted_catalog is a sorted list of ~10 million ints, searched
many times. Don't scan it per lookup — use bisect (or a prebuilt set) so each
membership check is O(log n) or O(1), and include doctests for the empty list
and an absent id."
```

## Spot the Confabulation

An AI "optimises" your slow membership check:

```python
def fast_search(items, target):
    # Optimised from O(n) to O(log n) using binary search.
    items = sorted(items)
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return True
        lo, hi = (mid + 1, hi) if items[mid] < target else (lo, mid - 1)
    return False
```

<details><summary>What's wrong?</summary>

The comment's complexity claim is false. Because the function sorts on **every call**,
each call costs O(n log n) — *worse* than the O(n) linear scan it "optimised". The code
is correct and the claimed speed-up sounds textbook-plausible, which is exactly what
makes it dangerous: the fix (sort once outside, search many times — or just build a set
once) requires seeing the whole call pattern, and the LLM only looked at one function.
Ten seconds with `timeit` on realistic data would have exposed it — measuring beats
guessing.

</details>

## Where to Practice

- **[Advent of Code](https://adventofcode.com)** — free puzzles (all years back to 2015
  stay open) where part one usually rewards a simple O(n²) solution and part two scales n
  up until it hurts — the whole lesson of this page, felt personally.
- **[Project Euler](https://projecteuler.net)** — hundreds of free maths-flavoured
  problems explicitly designed so brute force fails and a better algorithm succeeds.

## Quick Reference

| Idea | The rule |
|---|---|
| Algorithm | Finite, unambiguous steps: input → output |
| Correctness first | Doctests are the spec; test empty / absent / boundary cases |
| O(1), O(log n) | Constant / halving — dict lookup, binary search |
| O(n), O(n log n) | One pass / a good sort |
| O(n²) | Nested loops — fine for small bounded n, deadly at scale |
| Hidden O(n²) | `in list` or `.index()` inside a loop |
| Binary search | O(log n), but input **must be sorted** — sort once, search many times |
| Measure | Count steps or `timeit` on realistic n; never trust a claimed speed-up |

That covers the absolute minimum! You can now read any loop and name how it scales, demand
correctness before speed, and check claimed optimisations with a measurement — which is
exactly the review an algorithm from an AI needs.
