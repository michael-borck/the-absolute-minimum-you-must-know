> This content is from *TAMYMN-Inheritance.md*, part of *The Absolute Minimum You Must Know*.

# Inheritance in Python: The Absolute Minimum You Must Know

Inheritance is one relationship — *is-a* — one keyword's worth of mechanics, and two
warnings that most tutorials skip. All on this page. The running example is plotting
shapes, because "a circle is a shape" is true in exactly the way inheritance needs.

## Is-A, and the Mechanics

Write `class Child(Parent)` only when the sentence "every Child *is a* Parent" holds —
and (as you'll see below) holds in behaviour, not just in English. The child inherits
everything the parent has, and may **override** pieces of it:

The payoff is in `describe`: written **once**, on the parent, yet it prints the right
area for every shape, because `self.area()` finds the *child's* override at runtime.
Parent code calling child code — that's the engine inheritance runs on.

## `super()`: Extend, Don't Replace

Defining `__init__` (or any method) in a child **replaces** the parent's version
entirely; nothing runs the parent's automatically. `super().__init__(...)` is how you say
"do the parent's setup, then my extras". Forget it and the instance silently lacks the
parent's attributes — the error surfaces later, far from the cause, as an
`AttributeError` in some unrelated method. The same pattern works in any override:
`super().describe()` calls the parent's version so you can decorate it rather than
re-implement it.

## Liskov in Plain Words: Is-A Means *Behaves-Like*

Here's the famous trap. A square is a rectangle — in English. So:

`stretch` worked on every Rectangle ever — until a Square arrived and broke the unstated
promise that width and height move independently. That's the **Liskov substitution
principle** in plain words: *anywhere the parent works, the child must also work, without
the calling code knowing the difference.* If a child needs the caller to be careful, the
is-a claim is false in code, no matter how true it sounds in English — model it another
way (a `Square` that simply *is its own* `Shape`, or composition).

## Why Deep Hierarchies Rot

`Shape → Rectangle` is one hop, and it's honest. Real codebases sprout
`Shape → Polygon → Rectangle → StyledRectangle → ThemedStyledRectangle`, and then rot
sets in: to understand any method you read five files; a "small" change to a base class
silently changes behaviour in every descendant (the *fragile base class* problem); and
new requirements never fit the tree, so subclasses override methods to do nothing —
Liskov violations institutionalised. Rules of thumb: inherit for genuine
behaves-like-a relationships, keep hierarchies one or two levels deep, and when you're
inheriting just to *reuse* some methods, you want has-a instead — see
TAMYMN-Composition.md.

## Directing the Machine

AI assistants love inventing hierarchies — ask for three related classes and you may get
five, with an abstract base you didn't want. Constrain the tree explicitly, in this
page's terms.

Vague:

Informed:

## Spot the Confabulation

An AI assistant adds a labelled rectangle:

What's wrong?

The comment states a rule from other languages' constructors that Python doesn't have.
Defining `__init__` in the child **replaces** the parent's; nothing calls the parent's
version unless you do. As written, `LabelledRectangle("tile")` has a `label` but no
`width`, `height`, or `name` — and nothing fails until much later, when `.area()` raises
`AttributeError: 'LabelledRectangle' object has no attribute 'width'`. The fix is
explicit: accept `width, height, label`, call `super().__init__(width, height)`, then set
`self.label`.

## Where to Practice

- **Python Tutor** — paste the shapes code and step through
  `Rectangle(3, 4).describe()`; you'll watch the lookup climb from instance to child
  class to parent, which makes overriding and `super()` visible. No signup.
- **python-patterns.guide** —
  Brandon Rhodes' free site; this chapter shows, with runnable Python, exactly how a
  hierarchy rots and what to do instead. No signup.

## Quick Reference

| Mechanic / idea | One-liner |
|---|---|
| `class Child(Parent)` | Child is-a Parent, inherits everything |
| override | redefine a parent method in the child |
| `super().__init__(...)` | run the parent's setup — never automatic |
| `super().method()` | extend a parent method instead of replacing it |
| `issubclass(C, P)` / `isinstance(x, P)` | ask about the tree |
| Liskov, plainly | child must work anywhere the parent does, unnoticed |
| do-nothing override | smell: the is-a claim is false |
| deep hierarchy | smell: fragile base class, five-file reading trips |
| reuse without is-a | use composition — see TAMYMN-Composition.md |

That covers the absolute minimum! You can now build a shallow, honest hierarchy, extend
it with `super()`, and recognise the two ways inheritance goes wrong — the other pillars
are mapped in TAMYMN-OOP.md.
