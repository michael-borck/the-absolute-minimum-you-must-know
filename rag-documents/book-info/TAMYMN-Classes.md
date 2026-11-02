> This content is from *TAMYMN-Classes.md*, part of *The Absolute Minimum You Must Know*.

# Classes in Python: The Absolute Minimum You Must Know

Everything about Python classes follows from one model — a class is a blueprint, an
instance is one object built from it — plus about five pieces of mechanics, all on this
page. The running example is a bank account, because it's the smallest thing with both
data and rules.

## The Blueprint and the Built Object

Calling the class like a function (`BankAccount("Amira", 100)`) builds a fresh instance
and runs `__init__` on it. `__init__` does not *create* the object — Python has already
made an empty one — it *initialises* it, stamping on the attributes this instance starts
with.

## `self` Is Not Magic

`self` is just the instance, passed as the first argument automatically:

That's the whole trick. `acct.deposit(25)` means "run the blueprint's `deposit` function
*on this object*". It also explains the classic error message
`deposit() takes 2 positional arguments but 3 were given` — you forgot `self` in the
`def`, so your own arguments shifted into its place.

## Class Attributes vs Instance Attributes

`bank_name` lives on the class — one copy, visible through every instance. `owner` and
`balance` live on each instance. Lookup goes instance first, then class:

Rule of thumb: constants shared by every instance go on the class; everything that varies
per object gets set on `self` in `__init__`. Never put a **mutable** value (a list, a
dict) on the class "as a default" — every instance would share the same one (see the
confabulation below).

## `__repr__`: Make Your Objects Legible

Without `__repr__`, printing an object shows `` —
useless in debugging. With it:

Convention: `__repr__` returns the code you'd type to rebuild the object. Ten seconds of
effort, repaid every time you look at a stack trace or a list of objects.

## Dataclasses: The Modern Default for Data-Carrying Classes

When a class is mostly "hold these fields", stop writing `__init__` and `__repr__` by
hand — `@dataclass` generates them, plus `==` comparison, from the field list:

Reach for a dataclass first; fall back to a hand-written class when you need real
behaviour and control, like `BankAccount` above. You can still add methods to a
dataclass.

## Directing the Machine

When you ask an AI for a class, name the parts from this page — which attributes are
per-instance, what the repr should look like, whether a dataclass suffices — or you'll
get generic boilerplate with getters, setters, and inheritance you never asked for.

Vague:

Informed:

## Spot the Confabulation

An AI assistant adds transaction history to the account:

What's wrong?

`history = []` is a **class attribute**, so every account shares one list. Watch:

`self.history.append(...)` finds no `history` on the instance, falls through to the
class, and mutates the shared list. Per-instance mutable state must be created in
`__init__`: `self.history = []`. The AI version even *looks* more tidy — which is exactly
why this is the most common class bug LLMs write.

## Where to Practice

- **Python Tutor** — paste the `BankAccount` code and step
  through it: you'll see the class object, each instance, and which box each attribute
  lives in. The fastest cure for `self` confusion. No signup.
- **W3Schools Python Classes exercises** —
  small in-browser fill-in exercises on `__init__`, `self`, and methods. Free, no signup.

## Quick Reference

| Mechanic | What it does |
|---|---|
| `class Name:` | define a blueprint |
| `Name(args)` | build an instance; runs `__init__` |
| `def __init__(self, ...)` | initialise a new instance's attributes |
| `self` | the instance a method was called on (passed automatically) |
| `self.x = value` | instance attribute — this object only |
| `x = value` at class level | class attribute — shared by all instances |
| `def method(self, ...)` | behaviour; call as `obj.method(...)` |
| `def __repr__(self)` | debug string; return rebuild-the-object code |
| `@dataclass` | auto-generate `__init__`, `__repr__`, `==` from fields |
| mutable class attribute | bug: shared state across all instances |

That covers the absolute minimum! You can now define, instantiate, and debug classes and
choose dataclasses when they fit — the rest of OOP (see TAMYMN-OOP.md) builds directly on
these mechanics.
