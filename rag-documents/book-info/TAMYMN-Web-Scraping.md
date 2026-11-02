> This content is from *TAMYMN-Web-Scraping.md*, part of *The Absolute Minimum You Must Know*.

# Web Scraping: The Absolute Minimum You Must Know

Web scraping is two separate jobs — *fetching* a page and *parsing* it — and beginners
fail by welding them together. Effective scraping rests on one mental model (HTML is a
tree), one library for walking it (BeautifulSoup), and a short code of manners — all on
this page.

## Step Zero: Check for an API First

Before scraping anything, spend five minutes looking for an **API** — many sites offer
their data as clean JSON at a documented URL (look for "API" or "developers" in the
footer, or try the site name + "API" in a search). An API is faster, legal by design,
and doesn't shatter when the site changes its layout. Scraping is the fallback for when
no API exists, not the default.

## The Mental Model: HTML Is a Tree

An HTML page is elements nested inside elements — a tree. Parsing means walking that
tree and plucking out the nodes you want. Everything on this page runs against this
literal string (no network needed — and that's a feature, as we'll see):

Each element has a **tag** (`li`, `a`), **attributes** (`class="book"`, `href=...`), and
**text**. Those three are the coordinates for everything you'll ever extract.

## BeautifulSoup: find and select

`BeautifulSoup` turns the string into a navigable tree:

Now the tree answers questions — dotted access reaches the first element with that tag:

Two ways to hunt. **`find` / `find_all`** take a tag name plus attribute filters
(`class_` has a trailing underscore because `class` is a Python keyword):

**`select` / `select_one`** take CSS selectors — `tag`, `.class`, `#id`, and spaces for
"anywhere inside" — which is usually the shorter spell for anything nested:

The workflow for a real page: open it in the browser, right-click the data you want,
**Inspect**, and read off the tags and classes — then write the selector. A list of
extracted tuples drops straight into a DataFrame (`TAMYMN-Pandas.md`) for the analysis
step.

## Fetching: the Other Half

Downloading the page is one call with the `requests` library — shown here and *not* run,
because live URLs make examples flaky and tests network-dependent:

`response.text` is exactly the kind of string `page` was — from there on, nothing
changes. Which suggests the professional habit: **save the HTML to a file once, then
develop your parser against the saved copy.** You'll re-run the parser fifty times while
you get the selectors right; hitting the server fifty times is slow for you and rude to
them.

## Being Polite (and Legal)

- **Read `robots.txt`** — `https://site.com/robots.txt` says which paths the site asks
  bots not to touch. Respect it.
- **Check the terms of service** — some sites prohibit scraping outright; university and
  workplace rules may add more. "The scraper worked" is not the same as "this was OK".
- **Rate-limit yourself** — one request at a time, with a `time.sleep(1)` or two between
  pages. A tight request loop is indistinguishable from an attack.
- **Identify yourself** — a `User-Agent` with contact info (as above) lets an admin email
  you instead of banning you.

## Directing the Machine

An AI can't see the page you're scraping — so the single highest-value move is pasting a
*sample of the actual HTML* into the prompt and naming the tree coordinates (tags,
classes) you found with Inspect. Otherwise it guesses selectors for a page it imagines.

Vague:

Informed:

## Spot the Confabulation

An AI assistant extracts the listings:

What's wrong?

`find_all('li.book')` mixes the two hunting styles: `find_all` matches **tag names**, and
no tag is literally named `li.book`, so it returns `[]` — no error, no output, the loop
silently does nothing. CSS selectors like `li.book` belong to `select()`. Either
`soup.select('li.book')` or `soup.find_all('li', class_='book')` is correct. The
tell-tale: an empty result from a page where the browser clearly shows the data —
when that happens, suspect your selector's dialect before you suspect the page.

## Where to Practice

- **books.toscrape.com** and
  **quotes.toscrape.com** — sandbox sites built
  *specifically* to be scraped: stable layout, no signup, no legal grey zone. Books has
  1,000 items with pagination; Quotes adds login and JavaScript variants when you're
  ready.
- Your browser's **Inspect** panel on any page — practising "find the selector for this
  element" costs nothing and is half the real skill.

## Quick Reference

| Idiom | What it does |
|---|---|
| check for an API | step zero, before any scraping |
| `BeautifulSoup(html, 'html.parser')` | parse a string into a tree |
| `soup.find('tag', class_='c')` | first matching element (note `class_`) |
| `soup.find_all('tag')` | list of all matches — tag names only! |
| `soup.select('li.book .price')` | CSS selectors: `.class`, `#id`, nesting |
| `el.get_text()` / `el['href']` | element's text / attribute |
| `requests.get(url, headers=...)` | fetch (identify yourself in User-Agent) |
| `response.raise_for_status()` | fail loudly on HTTP errors |
| save HTML, parse the file | develop against a local copy |
| `robots.txt` + ToS + `time.sleep` | the politeness triad |

That covers the absolute minimum! You can now turn any page you're allowed to scrape
into structured data — inspect, select, extract, then analyse it with
`TAMYMN-Pandas.md` — and everything harder (JavaScript pages, logins) is the same tree
model behind more fetching machinery.
