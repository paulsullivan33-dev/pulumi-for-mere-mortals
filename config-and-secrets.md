# Config and Secrets

One program, run for a village hall and
then for a library, should not need two
copies of the code. The differences —
the title on the cards, the number of
pins — are **configuration**: values
that live outside the program, per
stack, in a file you can read. Values
that must not be readable — a signing
key, a password — are configuration too,
with encryption around them. This
chapter covers both, and the outputs
that carry secrets back out.

## Setting and reading config

Configuration lives in
`Pulumi.<stack>.yaml` beside the project
file, and is managed with `pulumi
config`:

```bash
pulumi config set boardTitle "Village Hall Notice Board"
pulumi config
```

The lab's run (transcript
`pulumi-lab/transcripts/t03-config.txt`):

```text
$ pulumi config
KEY         VALUE
boardTitle  Village Hall Notice Board
signingKey  [secret]
```

and the file itself:

```yaml
encryptionsalt: v1:fDGzf/C4Oeg=:v1:w0m1LJ8TLbisZoGq:zS85Kbce3NojeBgqGwah/GBuSgX/Iw==
config:
  notice-board:boardTitle: Village Hall Notice Board
  notice-board:signingKey:
    secure: v1:efLT3dum3l5QZPY+:dAfLFSrpeXdouMn6bLvk2n3fDQ5tSJAtAhIi
```

Three things to notice. Config keys are
namespaced by the project name —
`notice-board:boardTitle` — because a
stack file can also hold other tools'
and providers' settings under their own
namespaces, and nobody's keys may
collide. The program reads its own with
a bare `config.get("boardTitle")`
(chapter 4); the prefix is added for
it. And the file is ordinary YAML you
can diff in version control — including
the parts you cannot read, which brings
us to secrets.

## Secret config

```bash
pulumi config set --secret signingKey "oak-tree-42"
```

One flag changes where the value goes:
not into the YAML as text, but as a
`secure:` blob — ciphertext, produced
with the stack's encryption key (the
`encryptionsalt` at the top of the file,
and a passphrase the CLI asks for, or
takes from `PULUMI_CONFIG_PASSPHRASE`,
when the stack is created). `pulumi
config` shows the key's existence and
hides its value. The program reads it
with `config.get_secret(...)`, which
returns the value wrapped as a secret
Output — so anything derived from it
stays marked secret downstream,
including the stack output the lab
exported it as. That marking, not
anyone's care, is what keeps the value
out of previews, logs and terminals.

Two operational truths about the
passphrase. The lab set it as an
environment variable, which suits
scripts and labs; interactively, the CLI
prompts. And losing it loses the
secrets: the salt and ciphertext can sit
in git forever, and without the
passphrase they are noise. Pulumi Cloud
and the cloud key services can hold this
key instead — described, not run, in
this guide.

## Defaults are part of the program

Config is allowed to be absent. Both of
the lab's stacks set a title; a third,
created only to check, set nothing at
all (transcript
`pulumi-lab/transcripts/t14-defaults.txt`):

```text
Outputs:
    board_name : [unknown]
    board_title: "Community Notice Board"
    lockbox_pin: [secret]

Resources:
    + 6 to create
```

The program's `or "Community Notice
Board"` and `or 3` did their work: title
and card count fell back to the defaults
in the code, and `signing_key` — read
with `get_secret`, given no default, and
exported as `None` — simply does not
appear among the outputs. An unset
optional secret is an absent output, not
an error and not an empty string.
Design for that in your own programs:
decide, per setting, whether absence
means a default, an absence downstream,
or a program that should refuse to run
(`config.require(...)` exists for the
third, and fails the run loudly at
preview time — the right shape for a
setting that has no safe default).

## Reading results back: stack output

Outputs are the program's published
answers, and `pulumi stack output`
reads them from state at any time, with
no run of the program:

```text
$ pulumi stack output
Current stack outputs (4):
    OUTPUT       VALUE
    board_name   finer-earwig
    board_title  Village Hall Notice Board
    lockbox_pin  [secret]
    signing_key  [secret]
```

Secrets stay masked until you say the
words:

```bash
pulumi stack output --show-secrets
pulumi stack output lockbox_pin --show-secrets
```

(transcript
`pulumi-lab/transcripts/t06-outputs.txt`):

```text
    lockbox_pin  502094
    signing_key  oak-tree-42
```

and the second form prints just `502094`
— one value, no table — which is the
form scripts want. Treat it with the
respect the masking implies: a secret
printed into a terminal scrollback, a
log file or a chat transcript is a
secret published. The lab's PIN and
signing key are invented values for a
fictional board, printed in this guide
precisely because they protect nothing;
yours will, so let `--show-secrets` be
rare, deliberate, and never piped
anywhere that keeps records.
