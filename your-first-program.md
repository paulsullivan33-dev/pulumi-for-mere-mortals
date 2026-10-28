# Your First Program

By the end of this chapter you have a
project folder, a stack, settings for
that stack, and a program you have read
closely enough to predict — because
chapter 5 will ask you to, before it
shows you the preview. The program is
the lab's notice board, kept at
`pulumi-lab/project/`; everything in it
is invented for the occasion, and
everything it builds lives on your own
machine.

## Starting a project

The usual route is the scaffold:

```bash
pulumi new python
```

which asks a few questions and writes a
starter project. The lab ran it
non-interactively to see exactly what it
generates (transcript
`pulumi-lab/transcripts/t13-pulumi-new.txt`):
a `Pulumi.yaml`, a nearly empty
`__main__.py`, and a `requirements.txt`
naming just the Pulumi package. That is
a fine place to start a real project.
The lab's own project was written by
hand instead — the same three files,
each small enough to explain completely —
because a guide should show you the
whole machine, not the template's
opinion of it.

## Pulumi.yaml: the project's identity

```yaml
name: notice-board
runtime:
  name: python
  options:
    toolchain: pip
    virtualenv: venv
description: A tiny Pulumi program that never leaves this machine. ...
```

Three facts live here. The project's
**name** — config values and state are
namespaced under it, so it matters
beyond politeness. The **runtime**:
Python, installed with pip into a
virtual environment folder called
`venv` inside the project, which the
language host creates on first use and
reuses after. And a description, for
humans. Everything else about the
project is in the program.

## requirements.txt: the shopping list

```text
pulumi>=3.0.0,<4.0.0
pulumi-random>=4.0.0
pulumi-command>=1.0.0
```

One line per Python package the program
imports: the Pulumi SDK itself, and the
two provider packages. The version
ranges are deliberate. A Pulumi program
is ordinary Python, and its dependencies
drift like any others; a fresh machine
rebuilding the venv two years from now
should get packages this program was
written against, not whatever is newest.
The provider *plugins* (chapter 2) are
downloaded by the engine to match these
packages' versions — in the lab, random
4.21.4 and command 1.2.1.

## The program itself

Here is `__main__.py`, in the order it
runs. It is short, and every line earns
its place.

It opens by reading this stack's
**configuration** (chapter 7 is the full
story; here, just notice the shape):

```python
config = Config()
title = config.get("boardTitle") or "Community Notice Board"
pin_count = config.get_int("pinCount") or 3
signing_key = config.get_secret("signingKey")
```

`config.get` reads a setting and returns
`None` if the stack does not set it, so
each line supplies a default — a title, a
count of three — except the secret,
which is allowed to be absent. Nothing
has been built yet; these are just
values.

Then the two random resources:

```python
board_name = random.RandomPet("board-name", length=2)

lockbox_pin = random.RandomPassword(
    "lockbox-pin",
    length=6,
    numeric=True,
    upper=False,
    lower=False,
    special=False,
)
```

Each call declares a resource: a type,
a **logical name** (`"board-name"`,
`"lockbox-pin"` — the name your program
and the state know it by, distinct from
whatever name the outside world sees),
and its inputs. `RandomPassword` with
letters and symbols switched off is a
six-digit PIN; the provider marks its
result secret automatically, which
chapter 7 follows to the state file and
back.

Then the cards — the part that makes
Pulumi feel different from a
configuration file:

```python
for i in range(pin_count):
    command.local.Command(
        f"card-{i + 1}",
        create=f"printf 'Notice {i + 1} of {pin_count}: ...' > notice-{i + 1}.txt",
        delete=f"rm -f notice-{i + 1}.txt",
    )
```

A loop. Because the program is a
program, "one card per pin" is three
lines, and the count is a setting — set
it to five and the program declares five
cards (chapter 9 does exactly that and
reads the plan). Each card is a
`command:local:Command` resource: the
provider will run the `create` command
when the card is created and the
`delete` command when it is destroyed.
The commands are ordinary shell — the
card is a text file with one line in it.

Finally, the exports:

```python
export("board_title", title)
export("board_name", board_name.id)
export("lockbox_pin", lockbox_pin.result)
export("signing_key", signing_key)
```

`export` publishes a value as a **stack
output**. Note `board_name.id` and
`lockbox_pin.result`: those are not
values yet — they are **Outputs**, known
only after the provider runs, and the
preview will show them as `[unknown]` and
`[secret]` respectively. Exporting them
is how they become readable later with
`pulumi stack output`.

## A stack, and its settings

A program with no stack has nowhere to
keep state. The lab created one called
`dev` (transcript
`pulumi-lab/transcripts/t02-stack-init.txt`):

```text
$ pulumi stack init dev
Created stack 'dev'
$ pulumi stack ls
NAME  LAST UPDATE  RESOURCE COUNT
dev*  now          0
```

The star marks the selected stack. Then
two settings — the board's title, and a
secret signing key (chapter 7 returns to
both; the transcript is
`pulumi-lab/transcripts/t03-config.txt`):

```bash
pulumi config set boardTitle "Village Hall Notice Board"
pulumi config set --secret signingKey "oak-tree-42"
```

which land in a new file,
`Pulumi.dev.yaml`, in the project folder,
the secret stored encrypted:

```yaml
config:
  notice-board:boardTitle: Village Hall Notice Board
  notice-board:signingKey:
    secure: v1:efLT3dum3l5QZPY+:dAfLFSrpeXdouMn6bLvk2n3fDQ5tSJAtAhIi
```

Note the keys: `notice-board:boardTitle`
— settings are namespaced by project,
which is why the program's bare
`config.get("boardTitle")` finds them.

## The prediction to make

Before chapter 5: the program declares
two random resources and, with the
defaults and `dev`'s settings in force,
three cards. How many resources should
the first preview offer to create, and
which outputs should be unknown, which
secret, and which already readable? The
preview is the next chapter — check
your prediction against transcript t04
when you get there.
