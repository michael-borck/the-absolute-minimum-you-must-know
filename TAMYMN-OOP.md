# OOP in Python: The Absolute Minimum You Must Know

Object-oriented programming rests on one core idea and four named consequences of it —
all on this page. This doc is the map; each pillar has its own deep-dive
(see TAMYMN-Classes.md, TAMYMN-Encapsulation.md, TAMYMN-Abstraction.md,
TAMYMN-Inheritance.md, TAMYMN-Polymorphism.md, TAMYMN-Composition.md).

## The One Idea: State and Behaviour Travel Together

Without classes, data and the functions that understand it drift apart. A to-do list is a
list of dicts, and `add_task`, `complete_task`, `remaining_tasks` are loose functions that
each must be told (and must trust) what shape that data has:

```python
def complete_task(tasks, name):        # every caller must pass the right structure
    for entry in tasks:
        if entry["task"] == name:
            entry["done"] = True
```

A class staples the data and its functions together into one object, so the knowledge of
"how a to-do list is shaped" lives in exactly one place:

```python
class TodoList:
    def __init__(self):
        self.tasks = []

    def add(self, name):
        self.tasks.append({"task": name, "done": False})

    def complete(self, name):
        for entry in self.tasks:
            if entry["task"] == name:
                entry["done"] = True

    def remaining(self):
        return [e["task"] for e in self.tasks if not e["done"]]
```

```python
>>> todo = TodoList()
>>> todo.add("write report")
>>> todo.add("email Sam")
>>> todo.complete("write report")
>>> todo.remaining()
['email Sam']
```

Callers never touch the dicts inside — they say `todo.complete(...)` and the object does
the right thing to its *own* data. That's the whole sales pitch. Everything else in OOP is
this idea taken further. You've been using it all along: `"abc".upper()` and
`my_list.append(x)` are objects carrying their behaviour with them.

## The Four Pillars, In One Paragraph Each

**Encapsulation** — an object guards its own data and promises to keep it valid. Python
does this by convention (`_name` means "internal") and by properties, not by enforced
`private` keywords. See TAMYMN-Encapsulation.md.

**Abstraction** — callers depend on *what an object can do* (its interface), never on how
it does it. You can swap a CSV reader for a JSON reader if both offer `.read()`. See
TAMYMN-Abstraction.md.

**Inheritance** — one class is a special kind of another (*is-a*) and reuses its code.
Powerful, and the most over-used pillar: deep hierarchies rot. See TAMYMN-Inheritance.md.

**Polymorphism** — the same call, `sender.send(msg)`, does different things depending on
which object receives it, with no `if`-chains at the call site. See
TAMYMN-Polymorphism.md.

And the unofficial fifth pillar that working Python leans on most: **composition** —
building objects that *have* other objects instead of *being* them. See
TAMYMN-Composition.md.

## When NOT to Use OOP

A class earns its keep when there is state that must stay consistent with behaviour. When
there isn't, a class is ceremony:

- **A function that takes input and returns output** — keep it a function. Python is not
  Java; code doesn't have to live in a class.
- **A group of related constants or helpers** — that's a module. Modules already give you
  a namespace for free, without instantiating anything.
- **A bag of data with no behaviour** — a dict, a `namedtuple`, or a `dataclass`
  (see TAMYMN-Classes.md) is lighter and clearer.

The smell to watch for: a class whose methods never touch `self`. It's bundling nothing.

## Directing the Machine

AI assistants over-produce OOP — ask for "a program" and you often get a class explosion.
The informed prompt states which pillar you want and where the boundaries are, in the
vocabulary on this page.

Vague:

```
"Make my to-do code object-oriented."
```

Informed:

```
"Wrap the task list and its functions into a single TodoList class so callers never
touch the internal dicts. No inheritance — one class, plain methods. Keep the
file-saving helpers as module-level functions since they hold no state."
```

## Spot the Confabulation

An AI assistant reviews two helper functions, `slugify(text)` and `word_count(text)`:

```
In professional Python these should be grouped into a class for better
object-oriented design:

class TextUtils:
    def slugify(self, text):
        ...
    def word_count(self, text):
        ...

utils = TextUtils()
utils.slugify("Hello World")

This encapsulates the text behaviour properly.
```

<details><summary>What's wrong?</summary>

Nothing here is encapsulated, because there is no state — neither method reads or writes
`self`. The class bundles data with behaviour, except there is no data, so it buys only
ceremony: you must construct a `TextUtils()` instance just to call a function. A module
named `textutils.py` already provides the namespace. OOP's value is state and behaviour
travelling together; where there's no state, a plain function is the professional choice.

</details>

## Where to Practice

- **[Python Tutor](https://pythontutor.com)** — paste any class-based snippet and step
  through it; you *see* objects as boxes with attribute arrows, which makes `self` and
  instances concrete. No signup.
- **[The official tutorial, chapter 9](https://docs.python.org/3/tutorial/classes.html)** —
  the canonical short read on classes, straight from the source and always current.

## Quick Reference

| Concept | One-liner | Deep dive |
|---|---|---|
| Class / instance | blueprint / one object built from it | TAMYMN-Classes.md |
| Encapsulation | object guards its own data; `_name`, properties | TAMYMN-Encapsulation.md |
| Abstraction | depend on the interface, not the implementation | TAMYMN-Abstraction.md |
| Inheritance | is-a reuse; keep hierarchies shallow | TAMYMN-Inheritance.md |
| Polymorphism | same call, different behaviour per object | TAMYMN-Polymorphism.md |
| Composition | has-a assembly of small objects; usually beats inheritance | TAMYMN-Composition.md |
| When not to | no state to protect → function, module, or dataclass | this page |

That covers the absolute minimum! You now have the map — you can say *which* pillar a
design decision belongs to, and each linked doc takes you the rest of the way.
