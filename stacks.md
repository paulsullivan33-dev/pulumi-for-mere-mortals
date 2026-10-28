# Stacks

A **stack** is one managed copy of a
project's world: its own state file, its
own config, its own outputs, its own
resources. The program is shared; the
worlds are not. This chapter gives the
notice board a second stack — the
library's — and watches what is shared,
what is separate, and one place where
the separation leaks, in a way that
teaches more than the tidy parts do.

## The second stack

```bash
pulumi stack init prod
pulumi config set boardTitle "Library Notice Board"
pulumi config set pinCount 2
pulumi up --yes
```

Note what just happened mechanically:
`stack init` made a new state
(`~/.pulumi/stacks/notice-board/prod.json`)
and selecting it made the following
`config set` commands write to
`Pulumi.prod.yaml`, not `dev`'s file.
The lab's run (transcript
`pulumi-lab/transcripts/t09-second-stack.txt`):

```text
Outputs:
    board_name : "mint-kitten"
    board_title: "Library Notice Board"
    lockbox_pin: [secret]

Resources:
    + 5 created
```

Everything separate, as promised. The
board got its **own** random name —
mint-kitten, not finer-earwig — because
`prod`'s state had no name in it, so the
provider invented one and `prod`'s state
now remembers it. Its **own** PIN,
which the lab did not print, because one
printed lab secret per chapter is
enough. **Two** cards, because its
`pinCount` says so. And **three**
outputs, not four: `prod` sets no
`signingKey`, so the export is absent,
exactly as chapter 7 described. Five
resources created, not six-plus-stack —
the arithmetic of a smaller config.

`pulumi stack ls` keeps the census:

```text
NAME  LAST UPDATE     RESOURCE COUNT
dev*  17 seconds ago  10
prod  now             7
```

Resource counts here include the stack,
its providers and — for `dev`, which had
been through an update by then — the
full set state knows about; the point of
the listing is the two independent
counts, not the bookkeeping. The star
marks the selected stack: the one
`preview`, `up`, `config` and `output`
will act on until you `pulumi stack
select` the other. Most stack accidents
in real teams are selection accidents —
the right command against the wrong
stack — and the habit that prevents
them is reading the stack name in every
plan's first line: `Previewing update
(prod):` says where the plan applies
before it says anything else.

## What stacks are for

The pattern above is the standard one:
one stack per **environment** — `dev`,
`staging`, `prod` — differing in config:
sizes, counts, titles, endpoints, which
secrets. The code, reviewed once, runs
everywhere; the config, small enough to
read in one screen, carries the
differences. Teams also use stacks for
one world per developer, per customer,
or per region. All of those are the same
mechanism: separate state, separate
config, same declarations.

## The leak: two stacks, one folder

Now the honest complication, which this
lab is unusually well placed to show.
The cards are **files in the project
folder** — the working directory both
stacks' programs ran in. So when `prod`
was created, its card-1 and card-2
commands wrote `notice-1.txt` and
`notice-2.txt` — the very files `dev`'s
state believes it manages, now
containing the library's title. Neither
stack is wrong in its own terms: each
ran its commands, each state recorded
success. The *files* cannot serve two
masters.

On real infrastructure this collision
mostly cannot happen: a server or bucket
created for `prod` is a distinct object
from `dev`'s, with its own name in the
cloud, and one stack's destroy cannot
reach the other's resources. It *can*
happen wherever two stacks are pointed
at one shared thing by hand — a fixed
name chosen in code rather than
generated, a shared folder, a singleton
service — and Pulumi will not warn you,
because as far as state can tell,
nothing is shared. The lab's version is
the harmless end of that spectrum, and
chapter 10 will cash it in: watch what
`prod`'s destroy does to files `dev`
still claims.

The lesson to keep: a stack isolates
**state**, not the world. Where the
world itself is shared, you share it on
purpose, in the open — or not at all.
