> This content is from *playground.qmd*, part of *The Absolute Minimum You Must Know*.

# Playground 

Every cell on this page is a real Python interpreter running **in your browser** (via
Pyodide / WebAssembly) — nothing to install, nothing sent to a
server. Edit the code and press *Run Code*. Refreshing the page resets everything.

## Scratchpad

Try anything from the chapters here:

## Exercise: catch the confabulation

This function was written by an AI assistant and "works" — until it doesn't. Run it
as-is and look closely at the second call. Then fix it. (The trap is explained in
Python.)

## Exercise: verify like the book does

Every example in this book is a doctest. Here is the same machinery, in your hands:
the docstring below *claims* a behaviour, and `doctest` checks it. One of the claims
is wrong — run the cell, read the failure report, then fix either the code or the
claim (both are legitimate fixes; deciding which is the *point* of verification).

That's the whole loop this book teaches: a precise claim, an automatic check, and a
human deciding what the failure means. Take it with you.
