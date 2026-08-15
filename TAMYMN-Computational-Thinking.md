# Computational Thinking: The Absolute Minimum You Must Know

Computational thinking is the craft of turning a fuzzy human problem into precise steps a
machine can execute. It rests on four moves — decompose, spot the pattern, abstract, design
the algorithm — all on this page. In the AI age it is *the* skill that survives: the machine
implements, but someone still has to decide, exactly, what should be implemented.

## The Division of Labour Has Moved

An AI assistant will happily write code for a badly-specified problem — it just writes code
for the *wrong* problem, confidently. The bottleneck is no longer typing the solution; it's
specifying it. Every move on this page is a specification skill, which is why they matter
more now, not less: your decomposition becomes the [prompt](GLOSSARY.md#prompt-ai), and your [test cases](GLOSSARY.md#test) become the
proof the machine did what you meant.

## Move 1: Decomposition

Break the problem into parts small enough that each has an obvious answer. The test of a
good decomposition: every piece is either trivially doable or an already-solved problem.
"Build a grading system" is neither; "read scores from a [CSV](GLOSSARY.md#csv)", "map a score to a letter",
"count letters per class" are all three. Decomposition is also how you [debug](GLOSSARY.md#bug): a program
made of small named steps can be tested one step at a time.

## Move 2: Pattern Recognition

Most "new" problems are old problems wearing a costume. "How many distinct months did each
customer order in?", "how many distinct pages did each IP visit?", and "how many distinct
students submitted per unit?" are the *same* problem: group pairs by key, count distinct
values. Once you name the pattern, you can solve it once and reuse it — and you can ask an
AI for it by name, which gets dramatically better answers than describing it from scratch.

## Move 3: Abstraction

Abstraction is deciding what to ignore. A [function](GLOSSARY.md#function) signature is an abstraction: it promises
*what* comes back and hides *how*. Below, `distinct_per_key` doesn't know or care whether
the pairs are customers-and-months or IPs-and-pages — that irrelevant detail was abstracted
away, which is exactly what makes it reusable.

```python
def distinct_per_key(pairs):
    """Map each key to the number of distinct values paired with it."""
    seen = {}
    for key, value in pairs:
        seen.setdefault(key, set()).add(value)
    return {key: len(values) for key, values in seen.items()}
```

```python
>>> distinct_per_key([("ana", "01"), ("ana", "02"), ("ben", "01")])
{'ana': 2, 'ben': 1}
```

## Move 4: Algorithm Design

An algorithm is the ordered, unambiguous version of your decomposition: each step precise
enough that there is exactly one way to carry it out. "Sort of group them" is not a step;
"for each pair, add the month to that customer's set of months" is. If you can't state a
step that precisely, you haven't finished decomposing — go back to Move 1.

## Worked Example: From Fuzzy to Precise

The boss says: *"find our loyal customers."* That's not a computable statement — nothing in
it says what to [iterate](GLOSSARY.md#iteration) over or compare. Decompose it into decisions and steps:

1. **Define the fuzzy word** (abstraction): *loyal* = ordered in **3 or more distinct
   months**. This is a judgement call — a human one — and it must be made explicitly,
   because the machine will otherwise make it silently.
2. **Name the data shape**: a list of `(customer, month)` pairs, one per order.
3. **Spot the pattern**: "distinct months per customer" is distinct-values-per-key — solved
   above.
4. **Filter and report**: keep names whose count ≥ 3, sorted for a stable report.

Now every step is precise, and the whole thing is four short lines:

```python
>>> orders = [("ana", "2026-01"), ("ben", "2026-01"), ("ana", "2026-02"),
...           ("cli", "2026-02"), ("ana", "2026-03"), ("ben", "2026-01")]
>>> months = distinct_per_key(orders)
>>> sorted(months.items())
[('ana', 3), ('ben', 1), ('cli', 1)]
>>> sorted(name for name, n in months.items() if n >= 3)
['ana']
```

Notice ben ordered twice but in one month — the *definition* decided his fate, not the
code. That's the lesson: the hard part was step 1, and no amount of AI horsepower could
have done it for you, because it's a business decision disguised as a programming task.

## Two Habits That Complete the Loop

- **Evaluate trade-offs.** Most problems have several correct decompositions; prefer the
  one whose steps you can test independently, even if it's a line or two longer.
- **Iterate.** Your first decomposition is a draft. Running it *is* the review: wrong
  output means a wrong step or a wrong definition — refine and re-run. Generalise last:
  only turn a solution into an abstraction (like `distinct_per_key`) once you've met the
  pattern twice.

## Directing the Machine

An informed prompt is a decomposition. Hand the AI your steps and definitions, and it
implements exactly them; hand it the fuzzy version and it invents the missing decisions —
silently, plausibly, and often wrongly.

Vague:

```
"Write code to find our loyal customers from this order data."
```

(What is loyal? What's the data shape? The AI will pick definitions for you and won't
flag that it did.)

Informed:

```
"orders is a list of (customer, month) pairs. 1) Build a dict mapping each customer
to their set of distinct months. 2) A customer is loyal if that set has 3+ months.
3) Return loyal names sorted alphabetically. Include a doctest where a customer
with two orders in one month is NOT loyal."
```

## Spot the Confabulation

You ask an AI: *"flag customers who ordered in three consecutive months"* and it replies:

```python
def flag_loyal(orders):
    months = {}
    for name, month in orders:
        months.setdefault(name, set()).add(month)
    # Three or more months of orders means three consecutive months.
    return sorted(n for n, m in months.items() if len(m) >= 3)
```

<details><summary>What's wrong?</summary>

It solved a *different, easier* problem and asserted the equivalence in a comment. Three
**distinct** months is not three **consecutive** months: a customer who ordered in
January, June, and December has three distinct months and zero consecutive runs. The code
runs, looks professional, and returns plausible names — the error only surfaces if you
test the case the definitions disagree on. This is the classic LLM failure mode: when a
step of the decomposition is hard (detecting consecutive runs), it quietly substitutes a
neighbouring problem it knows how to solve. Your defence is Move 1: decompose first, then
check each step of the answer against *your* steps.

</details>

## Where to Practice

- **[Advent of Code](https://adventofcode.com)** — hundreds of free two-part puzzles
  (every year since 2015 stays open). Each is a fuzzy story you must decompose before any
  code helps, and part two forces you to refine your abstraction — the full loop, daily.
- **[Exercism](https://exercism.org)** — free, with a Python track of small exercises and
  automatic [test suites](GLOSSARY.md#test-suite), so you practise writing the tests-first specification style this
  page preaches.

## Quick Reference

| Move | The question it answers | The smell it fixes |
|---|---|---|
| Decomposition | What are the small, testable parts? | "I don't know where to start" |
| Pattern recognition | What solved problem is this in disguise? | Solving from scratch every time |
| Abstraction | What details can this step ignore? | Code that only works for one dataset |
| Algorithm design | Is every step unambiguous? | "Sort of group them somehow" |
| Trade-offs | Which correct version is easiest to test? | Clever code nobody can verify |
| Iteration | Did the output match the definition? | Shipping the first draft |

That covers the absolute minimum! You can now take a fuzzy request, decompose it into
precise testable steps, and direct either yourself or a machine to implement them — every
other computational skill builds on exactly this loop.
