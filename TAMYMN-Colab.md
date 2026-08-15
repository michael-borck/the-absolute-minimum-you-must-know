# Google Colab: The Absolute Minimum You Must Know

Colab is Jupyter running in your browser on Google's machines — zero install, free GPUs,
shareable like a Google Doc. Everything in `TAMYMN-Jupyter.md` applies unchanged; what's
new is *whose computer the [kernel](GLOSSARY.md#kernel) runs on*, and the handful of consequences of that fact
fill this page.

## The Mental Model: A Borrowed Computer

When you open a [notebook](GLOSSARY.md#notebook) at [colab.research.google.com](https://colab.research.google.com),
Google lends you a fresh virtual machine — the **runtime**. Your notebook file lives in
your Google Drive and is safe; the runtime is a *loaner*, and it is **ephemeral**. When
it's recycled — you close the tab too long, hit a time limit, sit idle — everything on it
vanishes:

- **Files you wrote** to the VM's disk (`/content/...`): gone.
- **Installed packages**: gone.
- **All [variables](GLOSSARY.md#variable)** (the usual Jupyter kernel death, see `TAMYMN-Jupyter.md`): gone.

The notebook's *text and outputs* survive, which fools people into thinking their work is
safe. The rule: **anything you'd cry about losing must leave the VM before the session
ends** — download it, or save it to mounted Drive.

## Getting Files In and Out

```
from google.colab import drive
drive.mount('/content/drive')        # your Google Drive appears as a folder — files
                                     # written there PERSIST across sessions

from google.colab import files
files.download('results.csv')        # push a file to your browser's downloads
files.upload()                       # pick local files to send to the VM
```

Mounting Drive asks for permission once per session. Reading/writing
`/content/drive/MyDrive/...` is slower than VM disk, so a common pattern is: copy data
in, work on `/content`, copy results back out.

## Installing Packages — Every Session

Colab pre-installs the scientific stack (pandas, matplotlib, scikit-learn, torch). For
anything else, a `!` runs a [shell](GLOSSARY.md#shell) command on the VM:

```
!pip install beautifulsoup4      # ! = run in the VM's shell (see TAMYMN-Linux.md)
!ls /content                     # any shell command works the same way
```

Because the runtime is ephemeral, installs don't stick — put every `!pip install` your
notebook needs in the **first cell**, so a fresh runtime can rebuild itself with one run.
That's the Colab flavour of Jupyter's Restart & Run All honesty check: a notebook that
only works because of something you installed by hand last Tuesday is broken.

## The Free GPU

`Runtime > Change runtime type > GPU` attaches a real GPU — the reason Colab is the
default classroom for deep learning. Switching runtime type gives you a *new* VM (state
and files gone — see the model above). Free GPUs are shared and rationed: sessions cap
out at roughly 12 hours, idle notebooks disconnect after a while, and heavy use gets you
temporarily throttled. Don't leave a GPU runtime attached while you're not computing.

## Sharing Like a Doc

The **Share** button works exactly like Google Docs — send a link, add commenters or
editors, collaborate on the same notebook file. One crucial asymmetry: you share the
*document*, not the *computer*. Each person's runtime is their own VM, with its own
variables and files. Two people editing the same notebook are running two separate
kernels — your `df` does not exist on their machine until they run the cells themselves.

## When to Graduate

Colab is the right tool for exploration, coursework, and anything GPU-hungry that fits in
a session. It's the wrong tool the moment you need: work that survives without babysitting
(runtime limits), private data you can't upload to Google, version control that [diffs](GLOSSARY.md#diff)
(notebooks are [JSON](GLOSSARY.md#json)), or code others `import`. That's when you graduate to a real
environment — Python and a [virtual environment](GLOSSARY.md#virtual-environment) on your own machine, VS Code
(`TAMYMN-VSCode.md`), and Git (`TAMYMN-Git.md`) — moving stable code out of the notebook
into `.py` [modules](GLOSSARY.md#module) exactly as `TAMYMN-Jupyter.md` prescribes.

## Directing the Machine

Colab problems are usually *environment* problems, so tell the AI which computer things
happened on — the ephemeral VM or your persistent Drive — and what a fresh runtime
does. Naming the borrowed-computer model turns a haunted-house story into a bug report.

Vague:

```
"colab deleted my trained model, how do I get it back"
```

Informed:

```
"I trained for 3 hours and saved model.pkl to /content, then the runtime disconnected
overnight — I know /content is ephemeral so the file is gone. Rewrite my save cell to
write checkpoints to a mounted Drive folder every epoch, and add a first cell that
reinstalls my pip dependencies so Restart & Run All works on a fresh runtime."
```

## Spot the Confabulation

An AI assistant reassures a worried student:

```
No need to re-run anything tomorrow — Colab autosaves your notebook to Google Drive,
so the model.pkl you wrote today will still be at /content/model.pkl next session.
Files and outputs are all part of the saved notebook.
```

<details><summary>What's wrong?</summary>

It conflates the two computers. Drive autosave preserves the **notebook file** — code,
prose, and displayed outputs. `/content/model.pkl` was written to the **runtime VM's
disk**, which is destroyed when the session ends; it is not "part of the notebook" and
will not exist tomorrow. To keep it: `files.download()` it, or write it into
`/content/drive/MyDrive/...` after `drive.mount()`.

</details>

## Where to Practice

- **[colab.research.google.com](https://colab.research.google.com)** — Colab itself is
  the practice ground: free with any Google account. Open the built-in "Welcome to
  Colab" notebook, then deliberately let a runtime die and reconnect — watching your
  variables and files vanish once teaches the ephemeral model better than any warning.
- **[Kaggle Notebooks](https://www.kaggle.com/code)** — the same hosted-notebook model
  with free GPU quota and public datasets attached; good for seeing that these concepts
  transfer beyond one vendor.

## Quick Reference

| Action / concept | Meaning |
|---|---|
| runtime | a borrowed, **ephemeral** VM — files and installs vanish with it |
| notebook file | lives in your Drive — safe, autosaved (outputs only, not files) |
| `drive.mount('/content/drive')` | attach Drive — files written there persist |
| `files.download('f')` / `files.upload()` | move files to/from your own machine |
| `!command` | run a shell command on the VM |
| `!pip install pkg` | per-session install — put them all in the first cell |
| Runtime > Change runtime type | attach a GPU (new VM: state resets) |
| Share button | shares the document; every collaborator gets their own runtime |
| limits | ~12 h max session, idle disconnects, throttling on heavy GPU use |
| graduate when | long jobs, private data, real diffs, importable code |

That covers the absolute minimum! You can now use free hosted compute without losing
work to a vanished VM — and you know exactly when to move to your own machine;
everything else is inside Colab's own welcome notebooks.
