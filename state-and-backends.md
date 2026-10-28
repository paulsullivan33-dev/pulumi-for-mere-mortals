# State and Backends

After chapter 5's `pulumi up`, Pulumi
knows things: the board is called
finer-earwig, the PIN is a specific
six digits, three specific files were
written by specific commands. Where is
that knowledge kept? In the **state**:
one file per stack, held by the
**backend**, and this chapter opens it.
Of all the chapters, this is the one
whose facts you will use when something
goes wrong at 2 a.m.

## Where the local backend keeps state

The lab logged in with
`pulumi login --local`, backend address
`file://~`. For the local backend, each
stack's state is a JSON file at:

```text
~/.pulumi/stacks/<project>/<stack>.json
```

— in the lab's case
`~/.pulumi/stacks/notice-board/dev.json`,
with a `~/.pulumi/history/` folder
keeping a record of each update beside
it, and `~/.pulumi/backups/` keeping the
previous state file from each run. The
`~` is your operating-system account's
home folder, and that detail is worth
more than it looks: the lab ran as a
different OS user from the one whose
home held its workspace, and its state
landed in *that* user's `.pulumi`, not
in the project folder and not beside the
code. Readers following along as
themselves will simply find it in their
own home. Either way: **state does not
live in the project, and is not part of
the code.** Commit the project to
version control, by all means — chapter
11 recommends it — and you have still
not backed up the state.

A second folder of Pulumi's deserves a
name here, because the lab's account of
itself would be incomplete without it:
the Pulumi home for plugins, logs and
workspace records. By default it is the
same `~/.pulumi`; the lab moved it with
the `PULUMI_HOME` environment variable
so the whole experiment could be deleted
in one gesture — and found that the
*backend's* state files followed the
account's home regardless, exactly as
the `file://~` address says. Two
different ideas share one folder by
default: the tool's own housekeeping,
and the stacks' memories. Keep them
straight and neither will surprise you.

## What is inside the state file

The lab's `dev.json` after the first
`up` is about twelve kilobytes of JSON.
Read with a small script rather than by
eye, it holds a checkpoint whose latest
deployment lists **eight** resources,
not six:

- the stack itself,
- two **provider records** — one for the
  random provider, one for the command
  provider. Providers are themselves
  entries in state, with their own IDs,
  because every other resource must
  record *which provider instance* is
  responsible for it,
- the five resources the program
  declared: the `RandomPet` (its ID is
  the name itself, `finer-earwig`), the
  `RandomPassword`, and the three
  `Command` cards, each with the command
  strings it was created with.

Each entry carries the resource's URN —
its full name inside Pulumi, built from
stack, project, type and logical name —
its inputs, and the outputs the provider
returned. The four stack outputs sit on
the stack's own entry: `board_name`,
`board_title`, `lockbox_pin`,
`signing_key`.

## The secrets inside the file

The PIN is a secret, and the signing key
is a secret, so: are they sitting in
this JSON file in plain text, readable
by anyone who finds it? The lab checked
in the bluntest way — it searched the
state file for the PIN it had revealed
through `pulumi stack output
--show-secrets` (chapter 7):

```text
$ grep -c "502094" ~/.pulumi/stacks/notice-board/dev.json
0
```

Zero. Secret values are stored
**encrypted** in state: in the JSON they
appear as ciphertext in a wrapper that
marks them secret, and the engine
decrypts them only in memory, only when
a run needs them, using the stack's
secrets provider — for the local
backend, a key derived from the
passphrase the lab set when the stack
was created (the lab kept it in the
`PULUMI_CONFIG_PASSPHRASE` environment
variable; the salt for it is the
`encryptionsalt` line at the top of
`Pulumi.dev.yaml`). Forget the
passphrase and the secrets in that stack
are unrecoverable — not locked out by
policy, but mathematically, which is
sterner.

Encryption at rest is not the same as
safety, and chapter 14 is blunt about
it: the state file is the keys to
everything the stack manages, and it
belongs somewhere with backups and
access control, treated like the secret
it collectively is.

## The other backend: Pulumi Cloud

Everything above used files because the
lab had no account and wanted none.
`pulumi login` without `--local` uses
**Pulumi Cloud** instead: state is
stored by the hosted service, each
update's history is kept and viewable,
stacks can be shared with a team, access
is controlled by account rather than by
file permissions, and secrets are
managed by the service. This guide did
not use it, so that paragraph is a
description from the documentation, not
a verification — the mechanics of
programs, previews and providers are the
same, and chapters 5 to 11 work
identically against either backend; what
differs is who holds the memory, and
what happens when the holder is a
service: an account, a login and a
network round trip stand between you
and state, in exchange for sharing and
safekeeping you do not have to build.
Self-managed file backends on shared
storage (an S3, Azure Blob or Google
Cloud Storage URL, or a shared folder)
sit between the two and are likewise
described here rather than run.

The choice, stated plainly: **local
files for learning and for one person;
a shared backend the moment a second
person needs the same world.** A stack
whose state exists on one laptop is a
stack only that laptop can safely
change.
