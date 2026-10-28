# Changing Things

Infrastructure work is mostly not
creating; it is changing what exists,
safely, and proving the change did what
was intended and nothing else. This
chapter makes the lab's standing change —
three pins become five — reads its plan
closely, applies it, and then runs two
experiments about the limits of
Pulumi's knowledge: an update with
nothing to do, and a change made behind
Pulumi's back.

## The change and its plan

One config value moves:

```bash
pulumi config set pinCount 5
pulumi preview
```

(transcript
`pulumi-lab/transcripts/t07-change-preview.txt`):

```text
 +  command:local:Command card-5 create
 ~  command:local:Command card-1 update [diff: ~create]
 ~  command:local:Command card-3 update [diff: ~create]
 ~  command:local:Command card-2 update [diff: ~create]
 +  command:local:Command card-4 create
Resources:
    + 2 to create
    ~ 3 to update
    5 changes. 3 unchanged
```

The creates are the easy half: cards 4
and 5 are new declarations (the loop now
runs to five), so they will be created.
The updates reward a close read. Why
must cards 1 to 3 change at all? Their
files exist; their commands ran. Look at
the card text: *Notice 1 of 3* — the
total is baked into each card's `create`
command string, and the command string
is the resource's input. Change `3` to
`5` and the input has changed, so the
plan marks the resource `~` **update**,
with the note `[diff: ~create]`: the
property that differs is `create`. For
this provider an update means running
the new command, which rewrites the
file with the corrected total. The plan
is not being fussy; it is showing you,
precisely, that a number embedded in
content propagates exactly as far as
you embedded it. In a cloud program the
same shape appears when a name or a tag
carries a value that later changes —
the preview names every resource that
will feel it, before anything moves.

The unchanged three, meanwhile: the two
random resources and the stack. The
board's name is **not** re-rolled,
because nothing about `board-name`'s
inputs changed — the value in state
stands. This is the quiet superpower of
the state model: randomness is generated
once, at creation, and is stable
thereafter unless the resource is
replaced. A plan that proposed a new
board name here would be a plan to read
very carefully.

## Applying, and the check

`pulumi up --yes` applies it (transcript
`pulumi-lab/transcripts/t08-update-and-noop.txt`):
2 created, 3 updated, and the outside
check agrees — five files now, and the
newest reads *Notice 5 of 5*. The old
cards were rewritten too; `cat
notice-1.txt` now says *of 5*.

## The update that does nothing

Immediately afterwards, the lab ran the
same command again:

```text
$ pulumi up --yes   # a second time, with nothing changed
...
Resources:
    8 unchanged
```

No creates, no updates, no file
rewritten (the command provider does
not re-run commands for unchanged
resources), and the outputs read back
identical — finer-earwig still. This is
chapter 1's **idempotency** with its
boots on, and it is the property to lean
on operationally: `pulumi up` is safe to
re-run after a failure, a doubt, or a
lunch break, because it converges rather
than repeats. If a re-run ever proposes
changes you did not make, that gap
*is* the news — something edited the
program, the config, or (next section)
the world.

## The change Pulumi cannot see

One experiment remains. The lab edited
a card by hand — an extra line appended
to `notice-3.txt`, no Pulumi involved —
then asked Pulumi to reconcile the
world with its records:

```bash
pulumi refresh --yes
pulumi preview
```

**Refresh** is the command for this: it
re-reads every resource through its
provider and updates state to match
reality, so drift — changes made outside
Pulumi — shows up in the next plan. The
result (transcript
`pulumi-lab/transcripts/t10-drift.txt`):

```text
Resources:
    8 unchanged
```

and the preview agreed: nothing to do.
The hand-written line is still in the
file, and Pulumi does not know, because
for *this* provider there is nothing to
know with: the command provider cannot
read a resource back. It knows the
commands it ran and their exit codes;
it has no way to inspect the file they
wrote. Refresh asked, and the provider
could only repeat what state already
said.

Hold the two halves of that result
apart, because both are true and they
are about different things. **Refresh
and drift detection are real** — for
providers that implement reading. A
cloud provider can fetch the actual
server, bucket or rule and compare it
with state, and drift then appears in
the plan as a change to be corrected or
accepted; that is the normal,
documented behaviour this lab could not
demonstrate without an account. And
**a provider that cannot read cannot
detect** — no tool can reconcile what
it cannot observe. When you choose
providers, especially the ones that wrap
scripts and commands, you are choosing
what Pulumi will be able to see. Blind
spots are not a defect in the plan; they
are a property of the provider, and
this guide's small one is labelled in
`criteria.md` so you can calibrate the
rest.
