> This content is from *TAMYMN-Encapsulation.md*, part of *The Absolute Minimum You Must Know*.

# Encapsulation in Python: The Absolute Minimum You Must Know

Encapsulation is an object keeping its own data valid — and Python's version rests on two
ideas that surprise people coming from Java: privacy is a *convention*, and
getters/setters are replaced by *properties*. Both fit on this page. The running example
is a thermostat, an object with an obvious rule to protect.

## The Point: Invariants, Not Secrecy

An **invariant** is a promise an object makes about its own data — "the set temperature
is always between 5 and 35°C". Encapsulation means the object enforces that promise
itself, so no caller, anywhere, can put it into a nonsense state. That's the value: not
hiding data for its own sake, but making illegal states unrepresentable from outside.

## The `_underscore` Convention

Python has no `private` keyword. Instead, one naming convention carries the meaning:

`_celsius` is perfectly accessible — `t._celsius` works — but the underscore tells every
reader "this is implementation detail; reach in and you're on your own". The language
doesn't stop you; the convention, code review, and linters do. This is deliberate:
"we're all consenting adults here" is the phrase Pythonistas use for it.

(You'll also see `__celsius` with two underscores. That triggers *name mangling* — the
attribute is stored as `_Thermostat__celsius` — which exists to avoid name clashes in
subclasses, **not** to provide security. It's still reachable; it's just renamed.)

## Why Getters and Setters Are Unpythonic

The Java reflex — write `get_celsius()` / `set_celsius(v)` for every field, "in case you
need control later" — is ceremony Python doesn't need, because of one feature: you can
add control *later* without changing callers. So start with a plain attribute:

The reason you *can* start plain is the property.

## Properties: Attribute Syntax, Method Control

A property looks like an attribute to callers but runs your code on read and write:

Three things to notice. The invariant now cannot be broken from outside — every write
path runs the check, including the one inside `__init__`. The real storage is `_celsius`
(underscore), while the public face is `celsius`; a property and its backing field must
have different names or the getter calls itself forever. And `fahrenheit` is **computed,
not stored** — storing both would let them disagree, which is an invariant violation
waiting to happen. Derive, don't duplicate.

The upgrade path is the punchline: version 1 of `Thermostat` could have used a plain
public `self.celsius = 20.0`, and every caller wrote `t.celsius = 25`. Version 2 added
the property. **No caller changed.** That is why Python skips getter/setter boilerplate:
you pay for control only when you need it.

## Directing the Machine

Ask an AI for a class with "private fields" and you'll usually get Java-style
`get_x`/`set_x` pairs, or `__x` mangling misdescribed as security. The informed prompt
uses this page's vocabulary — underscore convention, property, invariant.

Vague:

Informed:

```
"Store the temperature as _celsius and expose it as a `celsius` property whose setter
enforces the 5–35 range (raise ValueError). Add a read-only computed `fahrenheit`
property. No get_/set_ methods."

Use double underscores — Python then makes the attribute truly private and
inaccessible from outside the class:

class Thermostat:
    def __init__(self):
        self.__celsius = 20.0

    def get_celsius(self):
        return self.__celsius

    def set_celsius(self, value):
        self.__celsius = value

Now the temperature can only be changed through the setter, keeping it secure.
```

What's wrong?

Two confident falsehoods. First, `__celsius` is not inaccessible — name mangling just
renames it, and `t._Thermostat__celsius = 999` works fine; mangling exists to prevent
subclass name clashes, not to secure anything. Second, the getter/setter pair enforces
*nothing* — `set_celsius` accepts any value, so there's no invariant, only ceremony that
makes callers uglier. The pythonic version is a plain attribute until you need a rule,
then a `celsius` property whose setter actually validates.

## Where to Practice

- **Real Python: Python's property()** — a
  free, thorough walkthrough of properties, including the getter/setter comparison. No
  signup for the article.
- **Python Tutor** — paste the `Thermostat` class and watch
  reads and writes route through the property methods. No signup.

## Quick Reference

| Tool | Meaning |
|---|---|
| `self.name` | public attribute — the default; start here |
| `self._name` | internal by convention; accessible but hands-off |
| `self.__name` | name-mangled to `_Class__name` — clash protection, not security |
| `@property` | method that runs on attribute *read* |
| `@name.setter` | method that runs on attribute *write* — enforce invariants here |
| property with no setter | read-only / computed attribute |
| `get_x()` / `set_x()` | Java habit — replace with attribute or property |
| invariant | a promise about the data that the object itself enforces |

That covers the absolute minimum! You can now design classes that keep their own promises
and refactor plain attributes into properties without breaking a single caller — the
other pillars are mapped in TAMYMN-OOP.md.
