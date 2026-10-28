# Preview and Up

Two commands do the building in Pulumi.
`pulumi preview` runs your program,
compares its declarations with state,
and prints what *would* change — touching
nothing. `pulumi up` prints the same plan
and then carries it out. This chapter
runs both against the notice board and
then does the most important thing in
the whole guide: it checks, with
ordinary tools that owe Pulumi nothing,
that what was promised actually exists.

## The first preview

```bash
pulumi preview
```

Expect the first one to be slow. Before
any planning, the language host creates
the project's virtual environment and
installs the packages in
`requirements.txt`, and the engine
downloads the two provider plugins
(chapter 2). Later runs skip all of it.

The plan itself, from the lab's run
(transcript
`pulumi-lab/transcripts/t04-preview.txt`):

```text
Previewing update (dev):

 +  pulumi:pulumi:Stack notice-board-dev create
 +  random:index:RandomPassword lockbox-pin create
 +  random:index:RandomPet board-name create
 +  command:local:Command card-2 create
 +  command:local:Command card-1 create
 +  command:local:Command card-3 create
 +  pulumi:pulumi:Stack notice-board-dev create
Outputs:
    board_name : [unknown]
    board_title: "Village Hall Notice Board"
    lockbox_pin: [secret]
    signing_key: [secret]

Resources:
    + 6 to create
```

How to read it:

- **`+` means create** — every line is a
  resource that does not exist in state
  yet, including, bookending the list,
  the stack itself. Six resources: the
  stack, two random values, three cards.
  If chapter 4's prediction said five,
  the stack is the one most people miss.
- **The order is not a promise.** Cards
  print as 2, 1, 3: the engine plans in
  dependency order and is free to work
  in parallel where nothing depends on
  anything else. Nothing here depends on
  anything, so the engine owes you no
  sequence.
- **Outputs tell you what is knowable.**
  `board_title` is already readable — it
  came from config, not from a provider.
  `board_name` is `[unknown]` until the
  random provider invents it.
  `lockbox_pin` and `signing_key` are
  `[secret]`: Pulumi knows they are
  secret, and will keep them that way in
  state and on screen (chapter 7).

A preview changes nothing. After this
ran, no notice files existed; the state
still held zero resources. That is the
point of it: the plan is a promise you
can read, argue with, and keep — the
recipes chapter suggests saving the
plan alongside the commit that produced
it.

## Applying it: pulumi up

```bash
pulumi up --yes
```

Without `--yes`, `pulumi up` shows the
preview and asks you to confirm
interactively; with it — the form
scripts and this lab use — it applies
the plan it just showed. The lab's run
(transcript
`pulumi-lab/transcripts/t05-up.txt`)
repeats the preview, then:

```text
Updating (dev):
 +  pulumi:pulumi:Stack notice-board-dev created (0.86s)
 ...
Outputs:
    board_name : "finer-earwig"
    board_title: "Village Hall Notice Board"
    lockbox_pin: [secret]
    signing_key: [secret]

Resources:
    + 6 created

Duration: 4s
```

The unknown has resolved: the board is
named **finer-earwig**, chosen by the
random provider during the run and now
written into state, where it will stay
(chapter 9 changes other things and the
name does not move). The secrets are
still shown as `[secret]` — created,
stored, and not printed. That restraint
is the default at every step, not a
setting someone remembered to enable.

## Proving it without Pulumi

The providers promised three files with
specific contents. `pulumi` says they
were created in hundredths of a second.
Both claims are checkable with `ls` and
`cat`, and the lab checked:

```text
$ ls notice-*.txt
notice-1.txt
notice-2.txt
notice-3.txt
$ cat notice-1.txt
Notice 1 of 3: bring a mug, borrow a book. Board: Village Hall Notice Board
```

Make a habit of this shape of check.
A provider is a program, and programs
can be wrong, or can succeed at the
wrong thing — the command provider, for
instance, reports the exit code of your
command, and if your command writes the
file somewhere other than where you
think, Pulumi will faithfully record a
success about a file that is not where
you look for it. The plan is Pulumi's
account of the world; the world is the
authority. Chapters 6 to 11 keep
returning to that gap, because managing
it — knowing what Pulumi knows, what it
cannot know, and what it merely believes
— is most of operating this tool well.

State now remembers six resources and
four outputs. Chapter 6 opens the file
they live in.
