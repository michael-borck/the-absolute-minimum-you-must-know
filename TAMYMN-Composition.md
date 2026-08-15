# Composition in Python: The Absolute Minimum You Must Know

Composition is one relationship — *has-a* — and one design rule with a reason behind it:
prefer composition over inheritance. Both fit on this page. The running example is a game
entity, because games make the assembly of small parts visible.

## Has-A: Objects Built From Objects

Instead of one giant `Player` class holding hit points, item lists, and the logic for
each, build small single-purpose objects and *assemble* them:

```python
class Health:
    def __init__(self, points=100):
        self.points = points

    def take_damage(self, amount):
        self.points = max(0, self.points - amount)

    @property
    def alive(self):
        return self.points > 0

class Inventory:
    def __init__(self):
        self.items = []

    def pick_up(self, item):
        self.items.append(item)

    def has(self, item):
        return item in self.items

class Player:
    def __init__(self, name):
        self.name = name
        self.health = Health()          # Player HAS-A Health
        self.inventory = Inventory()    # Player HAS-A Inventory

    def take_damage(self, amount):      # delegation: forward to the part
        self.health.take_damage(amount)

    def status(self):
        state = "alive" if self.health.alive else "down"
        return f"{self.name}: {state}, {self.health.points} hp"
```

```python
>>> hero = Player("Rook")
>>> hero.inventory.pick_up("torch")
>>> hero.take_damage(30)
>>> hero.status()
'Rook: alive, 70 hp'
>>> hero.inventory.has("torch")
True
```

`Player.take_damage` is **delegation**: the whole presents a simple face and forwards the
work to the part that owns it. Each part is small enough to read in one glance and — the
underrated payoff — to test alone: `Health` needs no `Player` to exist.

## Why Composition Over Inheritance

Now add a treasure `Chest`. It needs an inventory too. Inheritance can't help — a chest
*is not a* player, and no honest parent class contains just the overlap. Composition
doesn't care about family trees, only parts:

```python
class Chest:
    def __init__(self, *loot):
        self.inventory = Inventory()
        for item in loot:
            self.inventory.pick_up(item)
```

```python
>>> Chest("gold", "map").inventory.has("map")
True
```

That's the "why" in three points. **Reuse without ancestry** — any object that needs an
inventory takes one; with inheritance, reuse is rationed to descendants. **Swap parts,
even at runtime** — a boss is `Player` plus `self.health = Health(500)`; making bosses,
ghosts (no health), and merchants by *subclassing* forces one class per combination and
the tree explodes. **Loose coupling** — `Player` touches only `Health`'s public methods,
so `Health` can be rewritten freely; a subclass, by contrast, is soldered to its parent's
internals, which is why deep hierarchies rot (see TAMYMN-Inheritance.md).

The rule of thumb: reach for composition first; use inheritance only when the *is-a*
sentence is true in behaviour, not just in English. Most "is-a" ideas are really "has the
abilities of" — and abilities are parts.

## Delegate Deliberately

Expose a forwarding method (like `take_damage`) when the whole should present one simple
face or coordinate several parts; let callers reach the part directly
(`hero.inventory.pick_up(...)`) when the part *is* the interface. What you should not do
is write a forwarding method for every method of every part "for neatness" — that
boilerplate rebuilds the rigid facade composition was meant to avoid. Delegate the calls
that mean something to the whole; leave the rest alone.

## Directing the Machine

Ask an AI for game entities and it will usually reach for a class hierarchy — `Entity`,
`DamageableEntity`, `CollectorEntity`... Name the parts and the relationship instead.

Vague:

```
"Add a merchant character to my game."
```

Informed:

```
"Model characters by composition, not inheritance: a Merchant class that HAS an
Inventory but no Health. Reuse the existing Inventory class unchanged. Don't subclass
Player, and don't create an Entity base class."
```

## Spot the Confabulation

An AI assistant adds that merchant by inheritance:

```
The cleanest reuse is subclassing, since Player already has everything we need:

class Merchant(Player):
    """Merchants trade but never fight."""
    def take_damage(self, amount):
        pass    # merchants are invincible

This way Merchant reuses inventory and status() for free.
```

<details><summary>What's wrong?</summary>

The do-nothing override is the tell. A `Merchant` now *is-a* `Player` that silently
ignores damage — every function written for players ("deal 30 damage, then check
`alive`") still runs but no longer means what it says, which is a Liskov violation (see
TAMYMN-Inheritance.md). Merchant also drags in all of Player whether wanted or not:
`status()` reports hit points the merchant supposedly doesn't have. "Reuses it for free"
is the confabulated benefit — the honest model is composition: `Merchant` *has* an
`Inventory` (reusing that class unchanged) and simply has no `Health` at all, so
"invincible" is true by construction instead of by a method that lies.

</details>

## Where to Practice

- **[python-patterns.guide: Composition Over Inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)** —
  Brandon Rhodes walks a logging design from subclass explosion to composed objects, in
  runnable Python. The single best free read on this page's rule. No signup.
- **[Python Tutor](https://pythontutor.com)** — paste `Player` and watch the object
  diagram: the arrows from `hero` to its `Health` and `Inventory` *are* has-a, drawn.
  No signup.

## Quick Reference

| Idea | One-liner |
|---|---|
| Composition (has-a) | an object holds other objects as attributes |
| Delegation | the whole forwards a call to the part that owns the work |
| Composition over inheritance | reuse by assembly: no ancestry required, parts swappable, coupling loose |
| Swap a part | `self.health = Health(500)` — no new subclass needed |
| Small objects | one job each; testable without the whole |
| Subclass-per-combination | smell: the tree explodes — compose instead |
| Do-nothing override | smell: is-a is false — see TAMYMN-Inheritance.md |
| Forward everything | smell: delegate meaningful calls, not all of them |

That covers the absolute minimum! You can now assemble behaviour from small objects and
justify "composition over inheritance" instead of just reciting it — the other pillars
are mapped in TAMYMN-OOP.md.
