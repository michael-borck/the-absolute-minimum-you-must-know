# Classes in Python: The Absolute Minimum You Must Know

Everything about Python classes follows from one model — a class is a blueprint, an
instance is one [object](GLOSSARY.md#object) built from it — plus about five pieces of mechanics, all on this
page. The running example is a bank account, because it's the smallest thing with both
data and rules.

## The Blueprint and the Built Object

```python
class BankAccount:
    bank_name = "First Doctest Savings"    # class attribute: shared by ALL accounts

    def __init__(self, owner, balance=0):
        self.owner = owner                 # instance attributes: THIS account only
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
```

```python
>>> acct = BankAccount("Amira", 100)
>>> other = BankAccount("Ben")
>>> acct.deposit(50)
150
>>> other.balance                 # untouched — separate instance, separate state
0
```

Calling the class like a [function](GLOSSARY.md#function) (`BankAccount("Amira", 100)`) builds a fresh instance
and runs `__init__` on it. `__init__` does not *create* the object — Python has already
made an empty one — it *initialises* it, stamping on the attributes this instance starts
with.

## `self` Is Not Magic

`self` is just the instance, passed as the first [argument](GLOSSARY.md#argument) automatically:

```python
>>> acct = BankAccount("Amira", 100)
>>> acct.deposit(25)                 # the normal spelling...
125
>>> BankAccount.deposit(acct, 25)    # ...is exactly this, spelled out
150
```

That's the whole trick. `acct.deposit(25)` means "run the blueprint's `deposit` function
*on this object*". It also explains the classic [error message](GLOSSARY.md#error-message)
`deposit() takes 2 positional arguments but 3 were given` — you forgot `self` in the
`def`, so your own arguments shifted into its place.

## Class Attributes vs Instance Attributes

`bank_name` lives on the class — one copy, visible through every instance. `owner` and
`balance` live on each instance. Lookup goes instance first, then class:

```python
>>> BankAccount.bank_name
'First Doctest Savings'
>>> BankAccount("Ben").bank_name  # found on the class, via any instance
'First Doctest Savings'
```

Rule of thumb: constants shared by every instance go on the class; everything that varies
per object gets set on `self` in `__init__`. Never put a **mutable** value (a [list](GLOSSARY.md#list), a
[dict](GLOSSARY.md#dictionary)) on the class "as a default" — every instance would share the same one (see the
[confabulation](GLOSSARY.md#confabulation) below).

## `__repr__`: Make Your Objects Legible

Without `__repr__`, printing an object shows `<__main__.BankAccount object at 0x...>` —
useless in debugging. With it:

```python
>>> BankAccount("Amira", 200)
BankAccount(owner='Amira', balance=200)
```

Convention: `__repr__` returns the code you'd type to rebuild the object. Ten seconds of
effort, repaid every time you look at a stack trace or a list of objects.

## Dataclasses: The Modern Default for Data-Carrying Classes

When a class is mostly "hold these fields", stop writing `__init__` and `__repr__` by
hand — `@dataclass` generates them, plus `==` comparison, from the field list:

```python
from dataclasses import dataclass

@dataclass
class Transaction:
    amount: int
    kind: str
```

```python
>>> t = Transaction(50, "deposit")
>>> t
Transaction(amount=50, kind='deposit')
>>> t == Transaction(50, "deposit")   # plain classes would say False here
True
```

Reach for a dataclass first; fall back to a hand-written class when you need real
behaviour and control, like `BankAccount` above. You can still add methods to a
dataclass.

## Directing the Machine

When you ask an AI for a class, name the parts from this page — which attributes are
per-instance, what the repr should look like, whether a dataclass suffices — or you'll
get generic boilerplate with getters, setters, and [inheritance](GLOSSARY.md#inheritance) you never asked for.

Vague:

```
"Write a bank account class."
```

Informed:

```
"Write a BankAccount class: instance attributes owner and balance (default 0), a
deposit method returning the new balance, and a __repr__ that rebuilds the object.
Also a Transaction dataclass with amount and kind. No getters/setters, no
inheritance."
```

## Spot the Confabulation

An AI assistant adds transaction history to the account:

```python
class LoggedAccount:
    history = []            # keeps a record of every deposit

    def __init__(self, owner):
        self.owner = owner

    def deposit(self, amount):
        self.history.append(amount)
```

<details><summary>What's wrong?</summary>

`history = []` is a **class attribute**, so every account shares one list. Watch:

```python
>>> a, b = LoggedAccount("Amira"), LoggedAccount("Ben")
>>> a.deposit(100)
>>> b.history                     # Ben "has" Amira's deposit
[100]
```

`self.history.append(...)` finds no `history` on the instance, falls through to the
class, and mutates the shared list. Per-instance mutable state must be created in
`__init__`: `self.history = []`. The AI version even *looks* more tidy — which is exactly
why this is the most common class bug LLMs write.

</details>

## Where to Practice

- **[Python Tutor](https://pythontutor.com)** — paste the `BankAccount` code and step
  through it: you'll see the class object, each instance, and which box each attribute
  lives in. The fastest cure for `self` confusion. No signup.
- **[W3Schools Python Classes exercises](https://www.w3schools.com/python/python_classes.asp)** —
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
