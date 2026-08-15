# Abstraction in Python: The Absolute Minimum You Must Know

Abstraction is one habit — depend on *what an object can do*, never on *how it does it* —
plus two Python mechanisms for expressing it: duck typing and `abc.ABC`. All on this
page. The running example is a file-format reader, because swapping formats is where this
habit pays rent.

## Interfaces Over Implementations

Suppose your program summarises records that arrive as CSV today. The naive version bakes
CSV parsing into the summary code; when JSON arrives next month, you're editing summary
logic to accommodate a file format. The abstracted version splits the two along an
**interface**: "a reader is anything with a `read(text)` method returning a list of
dicts". The summary code depends only on that sentence:

```python
def count_records(reader, text):
    return len(reader.read(text))       # knows the interface, not the format
```

`count_records` will work with every reader ever written, including ones that don't exist
yet. That boundary — the agreed method signature between the caller and the
implementations — is called a **seam**, and "program to the seam" is the whole
discipline: callers upstream of the seam never mention CSV, JSON, or anything concrete.

## Duck Typing: The Informal Interface

Python's default is that the interface is *implied*: if it has `read()`, it's a reader
("if it quacks like a duck..."). No declarations, no inheritance:

```python
class CsvReader:
    def read(self, text):
        header, *rows = text.strip().splitlines()
        keys = header.split(",")
        return [dict(zip(keys, row.split(","))) for row in rows]

class JsonReader:
    def read(self, text):
        import json
        return json.loads(text)
```

```python
>>> csv_text = "name,role\nAda,engineer\nGrace,admiral"
>>> CsvReader().read(csv_text)
[{'name': 'Ada', 'role': 'engineer'}, {'name': 'Grace', 'role': 'admiral'}]
>>> count_records(CsvReader(), csv_text)
2
>>> count_records(JsonReader(), '[{"name": "Alan"}]')
1
```

The two classes share no parent — only a shape. Most Python abstraction is exactly this,
and it's enough for most programs.

## `abc.ABC`: The Formal Interface

When the interface deserves to be *written down and enforced* — several implementers,
several authors, or a plug-in seam — make it explicit with an abstract base class:

```python
from abc import ABC, abstractmethod

class RecordReader(ABC):
    @abstractmethod
    def read(self, text):
        """Return a list of record dicts."""

class TsvReader(RecordReader):
    def read(self, text):
        header, *rows = text.strip().splitlines()
        keys = header.split("\t")
        return [dict(zip(keys, row.split("\t"))) for row in rows]
```

```python
>>> count_records(TsvReader(), "name\trole\nAda\tengineer")
1
>>> RecordReader()
Traceback (most recent call last):
    ...
TypeError: Can't instantiate abstract class RecordReader ...
```

Two things the ABC buys you: the interface is now a named, documented thing in the code,
and forgetting to implement `read` fails **at instantiation** — loudly and early —
instead of with an `AttributeError` deep in production. What it does *not* buy: any check
that `read` returns the right thing. An ABC verifies the method exists, not that it
honours the contract.

## Which One, When

Duck typing for interfaces with one or two implementations living near each other; an ABC
when the seam is a public boundary others build against. Either way, the abstraction is
only as good as the seam's discipline — see the confabulation below for the classic way
to ruin it. (For interfaces built by *assembling* small objects rather than subclassing,
see TAMYMN-Composition.md.)

## Directing the Machine

Asked for "flexible" code, an AI will happily generate five formats' worth of `if/elif`
inside one function. The informed prompt names the seam and who's allowed to know what.

Vague:

```
"Make my report code support JSON as well as CSV."
```

Informed:

```
"Define a RecordReader ABC with one abstract method read(text) -> list[dict].
Implement CsvReader and JsonReader against it. count_records() must depend only on
the RecordReader interface — no format names, no isinstance checks at the seam."
```

## Spot the Confabulation

An AI assistant hardens the seam function:

```
For safety, validate the reader before using it:

def count_records(reader, text):
    if not isinstance(reader, RecordReader):
        raise TypeError("reader must inherit from RecordReader")
    return len(reader.read(text))

This guarantees only valid readers are accepted.
```

<details><summary>What's wrong?</summary>

It guarantees the opposite of flexibility and no extra safety. The duck-typed
`CsvReader` and `JsonReader` above worked perfectly at this seam; the isinstance gate now
rejects them for the crime of not inheriting — the check tests *ancestry*, not
*capability*. And it adds no real protection: a subclass of `RecordReader` whose `read`
returns garbage sails straight through. If a wrong object arrives, `reader.read(text)`
already fails with a clear `AttributeError`. Program to the seam: require the method, not
the family tree.

</details>

## Where to Practice

- **[The `abc` module docs](https://docs.python.org/3/library/abc.html)** — short,
  canonical, with runnable examples of `ABC` and `@abstractmethod`. No signup.
- **[Real Python: Implementing an Interface in Python](https://realpython.com/python-interface/)** —
  a free article contrasting informal (duck-typed) and formal (ABC) interfaces with
  worked file-parser examples — the same territory as this page, at article length.

## Quick Reference

| Concept | One-liner |
|---|---|
| Interface | the *what*: methods a caller may rely on |
| Implementation | the *how*: hidden behind the interface |
| Seam | the boundary where implementations are swappable |
| Duck typing | has the method ⇒ is acceptable; no declaration needed |
| `class X(ABC)` | formal, named interface |
| `@abstractmethod` | subclasses must implement this or can't be instantiated |
| `isinstance` at the seam | smell: tests ancestry, not capability |
| "program to the seam" | callers never name concrete implementations |

That covers the absolute minimum! You can now design a seam, choose duck typing or an ABC
deliberately, and swap implementations without touching callers — the other pillars are
mapped in TAMYMN-OOP.md.
