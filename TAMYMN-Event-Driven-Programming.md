# Event-Driven Programming: The Absolute Minimum You Must Know

Every GUI, web server, and JavaScript page runs on one idea turned inside-out: your code
stops being the driver and becomes a set of functions waiting to be called. Grasp that
inversion, plus callbacks and a ten-line event loop, and every framework's documentation
starts making sense — all on this page.

## The Inversion: You Don't Call the Framework — It Calls You

A script you've written so far is a **recipe**: it runs top to bottom, in the order you
wrote, and then it ends. An event-driven program is a **reception desk**: it starts, then
*waits*, and things happen in whatever order the outside world decides — a click, a
request, a key press. You don't write the order of events; you write **handlers** (what
to do when each kind of event arrives) and register them. The framework owns the loop and
calls *your* functions. This is literally called *inversion of control*, and it's why
framework code looks so odd at first: there's no visible `main` path, just definitions
hooked onto events.

## Callbacks: Functions Handed Over to Be Called Later

The mechanism is one you already know: functions are values. A **callback** is simply a
function you pass to someone else — *without parentheses*, because you're handing over
the function itself, not the result of calling it now:

```python
>>> def on_login(user):
...     print("welcome,", user)
>>> saved_for_later = on_login       # handing over the function: no ()
>>> saved_for_later("ada")           # the framework calls it when the event fires
welcome, ada
```

`on_login` is the callback; `on_login()` would be the mistake of calling it yourself.
That distinction is the single most common event-handling bug — see the confabulation
below.

## An Event Loop You Can Hold in Your Head

Strip any framework to its skeleton and you find this — a dict mapping event names to
handler lists, and a dispatch function:

```python
handlers = {}                                    # event name -> list of callbacks

def on(event, handler):
    """Register a callback to run when event fires."""
    handlers.setdefault(event, []).append(handler)

def dispatch(event, data=None):
    """The heart of the loop: look up the event's handlers, call each one."""
    for handler in handlers.get(event, []):
        handler(data)
```

A real framework wraps this in `while True: dispatch(next_event())` and feeds it clicks
and network packets, but the shape is exactly this. Using it:

```python
>>> def greet_user(data):
...     print("Welcome,", data)
>>> on("login", greet_user)          # register: greet_user, NOT greet_user()
>>> dispatch("login", "ada")         # the loop calls YOUR function
Welcome, ada
>>> dispatch("logout", "ada")        # no handlers registered: silence, not an error
```

Two properties worth noticing: several handlers can subscribe to one event, and an event
nobody subscribed to simply vanishes — both are deliberate, and both are true of every
real event system you'll meet.

## Where You'll Meet This

Everywhere programs wait on the outside world. **GUIs**: tkinter's
`button.config(command=save_file)` and `window.mainloop()` — that last line *is* the
event loop, which is why code after it never runs. **Web servers**: Flask's
`@app.route("/users")` registers your function as the handler for "a request for /users
arrived". **JavaScript**: `button.addEventListener("click", handleClick)` is `on()` with
different spelling — the browser owns the loop. Same model, three dialects.

## The Trap: Globals Sneak into Handlers

Handlers are called with just the event's data, so where does state between events live
— a click counter, the logged-in user? The lazy answer is module-level `global`
variables, and event code rots exactly this way: every handler reads and writes shared
globals until nothing can be tested or reasoned about alone. The fix is to give state a
home the handler carries with it — a closure (below) or a class with methods as handlers:

```python
>>> def make_click_counter():
...     count = {"clicks": 0}            # state lives HERE, not in a global
...     def on_click(data):
...         count["clicks"] += 1
...         print("clicks so far:", count["clicks"])
...     return on_click
>>> on("click", make_click_counter())
>>> dispatch("click")
clicks so far: 1
>>> dispatch("click")
clicks so far: 2
```

Each call to `make_click_counter()` creates an independent counter — try wiring two
buttons to one global and you'll appreciate the difference.

## Directing the Machine

The informed prompt names the model: which events, which handlers, where state lives.
Frameworks are boilerplate-heavy, so AIs write them well — *if* you specify the wiring
instead of letting the AI guess it (and its guess will use globals).

Vague:

```
"make a python gui with a button that counts clicks"
```

Informed:

```
"tkinter window with a button and a label. Register a handler for the button's
click event that increments a counter and updates the label. Keep the counter in
a class (or closure), not a global. Remind me why nothing after mainloop() runs."
```

## Spot the Confabulation

An AI assistant wires up an event handler:

```
def refresh_view():
    print("view refreshed")

# Register our callback so the view refreshes on every data change:
on("data_changed", refresh_view())
```

<details><summary>What's wrong?</summary>

The parentheses. `refresh_view()` **calls the function immediately** — the view refreshes
once, at registration time — and what actually gets registered is its return value,
`None`. When `data_changed` really fires, dispatch tries to call `None` and crashes with
`TypeError: 'NoneType' object is not callable`. Cruelly, the code *appears* to work when
first run, because the premature call prints the expected message. Register the function
itself: `on("data_changed", refresh_view)`. Callbacks are handed over, never called, by
you.

</details>

## Where to Practice

- **tkinter** — already in your Python installation, no signup, no install: `python3 -m
  tkinter` proves it's there. Build the click-counter above as a real button; the
  [official tutorial at docs.python.org](https://docs.python.org/3/library/tkinter.html)
  has working snippets.
- **Your browser's console** — open developer tools on any page and type
  `document.addEventListener("click", e => console.log(e.target))`. Instant event-driven
  programming; [MDN's "Introduction to events"](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events)
  is the free guided version.

## Quick Reference

| Idea | The minimum |
|---|---|
| The inversion | you register handlers; the framework owns the loop and calls you |
| Callback | a function passed as a value — `handler`, never `handler()` |
| Event loop | `while True:` get event → look up handlers → call each with the data |
| Registration | a dict of event → list of handlers; multiple handlers per event is fine |
| Unhandled event | silently ignored — by design, in every event system |
| State | closures or classes, not globals — each handler carries its own |
| Sightings | tkinter `command=`, Flask `@app.route`, JS `addEventListener` |
| Classic bug | registering `f()` (calls now, registers `None`) instead of `f` |

That covers the absolute minimum! You can now read any framework's event wiring, write
handlers that keep their state to themselves, and spot the called-instead-of-passed bug
before it ships — every GUI toolkit and web framework is this page plus vocabulary.
