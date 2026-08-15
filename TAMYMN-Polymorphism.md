# Polymorphism in Python: The Absolute Minimum You Must Know

Polymorphism is one sentence — *the same call, different behaviour depending on the
object* — and the rest of this page is what that buys you and the smell that tells you
you're doing it by hand. The running example is a notification sender, because "send this
alert somehow" is polymorphism's natural habitat.

## Same Call, Different Behaviour

Three unrelated classes, one shared method shape:

```python
class EmailSender:
    def send(self, to, message):
        return f"email to {to}: {message}"

class SmsSender:
    def send(self, to, message):
        return f"sms to {to}: {message[:20]}"      # SMS truncates

class SlackSender:
    def send(self, to, message):
        return f"slack DM to @{to}: {message}"
```

```python
>>> def alert(sender, to, message):
...     return sender.send(to, message)            # ONE call site, no ifs
>>> for sender in [EmailSender(), SmsSender(), SlackSender()]:
...     print(alert(sender, "sam", "server is down in eu-west-1"))
email to sam: server is down in eu-west-1
sms to sam: server is down in eu
slack DM to @sam: server is down in eu-west-1
```

`alert` contains no channel logic at all, yet each channel behaves correctly — Python
looks up `send` **on the object it receives**, at runtime, and each object carries its
own version. New channel next month? Write one class with a `send` method; `alert` and
every other call site work with it *unchanged*. The dispatch table you'd otherwise
maintain by hand is method lookup, and it's free.

In Python this needs no common parent: matching method shapes are enough (**duck
typing** — if it has `send`, it's a sender). When you want the shape written down and
enforced, give the senders an ABC — that trade-off is TAMYMN-Abstraction.md's territory.

## You Already Use It Everywhere

`len("abc")`, `len([1, 2])`, `for x in anything`, `a + b` on ints or strings — the
built-ins are polymorphic across types via dunder methods (`__len__`, `__iter__`,
`__add__`). Your classes join in the same way:

```python
class Broadcast:
    def __init__(self, *senders):
        self.senders = senders

    def __len__(self):
        return len(self.senders)
```

```python
>>> len(Broadcast(EmailSender(), SmsSender()))
2
```

## The Smell: `isinstance` Chains

Here's the same `alert` written by someone who has the classes but not the idea:

```
def alert(sender, to, message):
    if isinstance(sender, EmailSender):
        return f"email to {to}: {message}"
    elif isinstance(sender, SmsSender):
        return f"sms to {to}: {message[:20]}"
    elif isinstance(sender, SlackSender):
        return f"slack DM to @{to}: {message}"
```

This *runs*, but it has moved every class's behaviour out of the classes and into one
brittle function: adding a channel now means editing `alert` (and every other
isinstance-chain in the codebase — they breed), the truncation rule lives far from
`SmsSender`, and any sender the chain doesn't list falls off the end and returns `None`
silently. An isinstance chain over your own classes is the machine telling you a method
is missing: the branches *are* the method bodies, filed in the wrong place. Move each
branch into its class as `send`, and the chain collapses into `sender.send(to, message)`.
(Occasional `isinstance` on *foreign* types at a system boundary is fine; chains over
types you control are the smell.)

## Directing the Machine

LLMs produce isinstance chains readily — they're the locally-obvious completion. Name the
polymorphic design you want and forbid the smell.

Vague:

```
"Make the alert function also handle Slack."
```

Informed:

```
"Each channel class owns its formatting in a send(to, message) method with the same
signature. alert() must call sender.send() and contain no isinstance checks or
channel names. Add SlackSender as a new class; don't touch alert()."
```

## Spot the Confabulation

An AI assistant offers a sender that accepts two calling styles:

```
class EmailSender:
    def send(self, to):
        return self.send(to, "ping")

    def send(self, to, message):
        return f"email to {to}: {message}"

Python method overloading: the interpreter picks the right send() based on the
number of arguments you pass.
```

<details><summary>What's wrong?</summary>

Python has no overloading by signature — a class body is just executed top to bottom, so
the second `def send` silently **replaces** the first, the same way `x = 1; x = 2` leaves
`x == 2`. Only the two-argument version survives, and `sender.send("sam")` raises
`TypeError: send() missing 1 required positional argument`. The pythonic spellings are a
default (`def send(self, to, message="ping")`) or, for dispatch by *type*,
`functools.singledispatchmethod`. This one is worth internalising: it looks like Java,
compiles like Python, and LLMs trained on both write it constantly.

</details>

## Where to Practice

- **[learnpython.org — Classes and Objects](https://www.learnpython.org/en/Classes_and_Objects)** —
  an in-browser interactive chapter; extend its exercises by giving two classes the same
  method and looping over them. Free, no signup.
- **[Python Tutor](https://pythontutor.com)** — paste the senders and step the loop; you
  can watch each iteration dispatch `send` to a different class. No signup.

## Quick Reference

| Idea | One-liner |
|---|---|
| Polymorphism | same call, behaviour chosen by the receiving object |
| Method lookup | Python finds the method on the object, at runtime |
| Duck typing | matching method shape is enough — no shared parent needed |
| Override-based | subclasses redefine a parent method — see TAMYMN-Inheritance.md |
| Dunder methods | make your objects work with `len()`, `+`, `for`, `print` |
| isinstance chain | smell: method bodies filed in the wrong place |
| Signature overloading | doesn't exist — last `def` wins; use defaults |
| `functools.singledispatch` | stdlib tool when you truly must dispatch on type |

That covers the absolute minimum! You can now collapse if-chains into methods and add new
behaviours without touching call sites — the other pillars are mapped in TAMYMN-OOP.md.
