# Pulumi for Mere Mortals

Most tools that build infrastructure ask
you to learn a special language for the
job: blocks, attributes, a new syntax for
loops and conditions, invented for one
tool and useful nowhere else. **Pulumi**
takes the opposite bet. You describe what
you want — servers, buckets, files,
settings — in a programming language you
may already know, such as **Python**,
TypeScript, Go or C#. The program says
*there should be a notice board with
these cards on it*; Pulumi works out what
already exists, what must be created,
changed or deleted to make that true, and
shows you the plan before it touches
anything. That showing-before-doing, and
the **state** file that remembers what
was built, are the heart of the tool, and
most of this guide is about them.

This guide explains the model, installs
the command-line tool, and builds one
small Python program end to end: declared,
previewed, created, read back, changed,
copied into a second **stack** with
different settings, and destroyed, with
every step run for real and the
transcripts kept in the repository. The
program uses no cloud account at all. Its
two providers work entirely on the
machine running them — one invents values
and remembers them, the other runs
ordinary shell commands — so the whole
lifecycle can be practised at a kitchen
table, free, with nothing at stake. What
changes when the resources are real cloud
resources is the provider, not the shape
of the work, and the guide says plainly
which parts it verified and which it only
describes.

The lab behind this guide ran the real
thing: **Pulumi 3.272.0**, the official
command-line release, logged in to the
**local backend** — no Pulumi Cloud
account, state kept in files on the lab
machine. The lab program pinned five
notice cards (small text files) to a
fictional village hall's notice board,
generated the board a two-word name and a
secret six-digit PIN, read its settings
from per-stack configuration, and
exported the results as **stack outputs**.
The lab then changed the card count and
watched the plan update three cards and
create two, ran the same update again and
watched it change nothing, gave the
program a second stack with a different
title and fewer cards, edited a card by
hand to see whether Pulumi would notice
(it would not — chapter 9 explains why,
and why real cloud providers differ), and
destroyed everything, stack by stack,
verifying the files were gone.

What the lab could not do, it did not
fake. It had no cloud account, so
creating real servers, buckets or
networks — and the Pulumi Cloud backend,
teams, and hosted secrets — are taught
from the documentation and labelled as
such wherever they appear. One lab note
belongs here rather than in a footnote:
the sandbox the lab ran in silently
resets the internal connections a Python
Pulumi program uses to talk to Pulumi's
engine over IPv4 loopback, so the lab
routed those two connections over IPv6
loopback through a small local relay.
Nothing about Pulumi, its protocol or its
output was changed by that; it is a quirk
of the lab's network, not of the tool,
and chapter 15 and `criteria.md` tell the
whole story. On an ordinary machine, none
of it is needed.

## What this guide covers

- [**What Pulumi is**](what-pulumi-is.md) —
  the model: a program declares what
  should exist, an engine compares it
  with the world and with its memory,
  and providers do the actual building
- [**The moving parts**](the-moving-parts.md) —
  the CLI, the engine, language hosts,
  providers and plugins, the backend,
  and which part holds what
- [**Installing Pulumi**](installing-pulumi.md) —
  the official installer, the version
  check, and logging in to the local
  backend with no account at all
- [**Your first program**](your-first-program.md) —
  the project files, a scaffold from
  `pulumi new`, and the lab's notice
  board program taken apart line by line
- [**Preview and up**](preview-and-up.md) —
  the plan before the act: reading a
  preview, applying it, and proving the
  promised files exist with the promised
  contents
- [**State and backends**](state-and-backends.md) —
  the file that remembers everything:
  where it lives, what is in it, where
  the secrets are inside it, and what a
  backend is for
- [**Config and secrets**](config-and-secrets.md) —
  per-stack settings in a plain YAML
  file, secret values stored encrypted,
  and outputs that stay secret until you
  ask twice
- [**Stacks**](stacks.md) —
  one program, several independent
  worlds: a second stack with its own
  name, PIN and settings, and the day
  the two stacks shared a folder
- [**Changing things**](changing-things.md) —
  growing the board from three cards to
  five, the update that changes nothing,
  and the hand edit Pulumi could not see
- [**Destroying things**](destroying-things.md) —
  taking it all down in the right order,
  what `destroy` leaves behind, and
  removing a stack completely
- [**Writing real programs**](writing-real-programs.md) —
  outputs and the values that are not
  known yet, ordinary Python doing
  ordinary work, and the parts of real
  programs this lab describes rather
  than demonstrates
- [**Recipes**](recipes.md) — practise
  before it matters, keep the plan in
  the commit, one stack per environment,
  and read a secret without printing it
- [**The neighbours**](the-neighbours.md) —
  Terraform, Ansible, CloudFormation and
  the CDK, and plain scripts: what each
  shares with Pulumi and where they part
- [**Limits**](limits.md) — state is a
  file you can lose, not every change
  can be previewed honestly, the program
  is code and can do anything code can,
  and the other edges, stated plainly
- [**Troubleshooting**](troubleshooting.md) —
  the first preview that takes minutes,
  the program that cannot reach its
  engine, and the traps this guide's lab
  fell into so you don't have to
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Real cloud resources. The lifecycle this
guide teaches — declare, preview, apply,
change, destroy — is the same one used
with Amazon, Azure, Google Cloud and
Kubernetes providers, and chapters point
at them, but no cloud account was opened
for this lab and no chapter pretends
otherwise. Pulumi Cloud (the hosted
backend, teams, access control, hosted
deployments) is described, not used.
Policy packs, automation APIs that embed
Pulumi inside other programs, and
converting Terraform projects are named
where they belong and left there. The
other Pulumi languages — TypeScript, Go,
C#, Java, YAML — share the engine and the
model; this guide teaches Python and
says so.

## How to use this guide

Read chapter 1 for the model and chapter
2 before installing anything — knowing
which part holds what turns later
confusion into a named problem. Chapters
4 to 6 take you from an empty folder to
a created, verified set of resources in
one sitting; do that with the local
providers first, where a mistake costs a
text file. Chapters 6 and 7 are not the
optional chapters: understand where state and
secrets live before you trust the tool
with anything real, because the state
file is both the tool's memory and its
biggest liability. The lab's program is
`pulumi-lab/project/`; its transcripts
are `pulumi-lab/transcripts/`; the
numbering matches the chapters
(t00–t14), and t90–t92 keep the
failures the lab diagnosed rather
than hid.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Terraform for Mere Mortals](https://paulsullivan33-dev.github.io/terraform-for-mere-mortals/)
- [Ansible for Mere Mortals](https://paulsullivan33-dev.github.io/ansible-for-mere-mortals/)
- [Kubernetes for Mere Mortals](https://paulsullivan33-dev.github.io/kubernetes-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/pulumi-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/pulumi-for-mere-mortals/blob/main/LICENSE-CODE).
