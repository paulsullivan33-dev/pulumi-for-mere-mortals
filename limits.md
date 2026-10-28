# Limits

The plain list of what this tool cannot
do, will not do, or does at a price —
including every limit this guide's lab
met itself, marked as such.

## State is a memory you can lose

Pulumi's knowledge of the world is the
state file (chapter 6). Delete or
corrupt it and the resources still
exist but are unmanaged: previews show
an empty world and offer to create
everything again, which — against a
cloud — means duplicates or collisions,
not a tidy rebuild. Backups sit beside
the local state, and `pulumi import`
can adopt existing resources back into
state; both are seatbelts, not
undo buttons for carelessness. The
local backend makes this *your*
problem in the most literal way: the
memory of what you built is a JSON file
on one disk.

## The plan is only as true as the providers

A preview compares your program with
state. Between state and the world
stands the provider, and providers
differ in what they can observe. The
lab met the sharp end of this: its
command provider **cannot read what it
created**, so a file edited by hand was
invisible to `pulumi refresh` and every
later plan (chapter 9) — drift that
real cloud providers, which implement
reading, would have caught. Even with
reading providers, some drift is
invisible until it matters (a setting
the provider's API does not return),
and some changes are known only at
apply time. Read plans as *the best
available account*, and keep the
outside checks of chapter 12 in your
routine.

## Not everything can be previewed

Values that providers generate —
addresses, IDs, the board's name — are
`[unknown]` until they exist. Programs
that consume them must be written for
that (chapter 11), and a preview can
never show you the finished world in
full, only its shape. Where a value
must be known in advance, someone has
to fix it in advance, in config, and
accept the collisions that fixing
invites (chapter 8's shared folder is
the small print of that bargain).

## A program is code, with code's powers

Your Pulumi program runs, on your
machine, with your credentials, at
`pulumi up`. It can import anything,
read any file, call any API — that is
its virtue as a programming language
and its hazard as an artefact. A
Pulumi program from an untrusted source
is an untrusted program; review one the
way you would review a script a
stranger asked you to run as yourself,
because that is what it is. The
declarations are data to the engine,
but the program that emits them is
alive.

## Secrets: encrypted, not invulnerable

State encrypts secret values (chapter
7), config encrypts secret settings
(chapter 7), and screens mask them by
default. All true, and all bounded:
the state file plus the passphrase
together are the secrets, so the file
belongs under the same discipline as a
keyring — access control, backups that
are themselves protected, and a shared
backend when a team shares the stack.
History and backups retain old secrets
after the values change. And a secret
that a *provider* must hand to a real
service exists in the clear at that end
by necessity. Pulumi keeps secrets out
of your terminal and out of plain text
on disk; it does not abolish them.

## Concurrency and scale are real, and were not tested here

One machine, one stack, one operator:
the lab's whole world. Real use adds a
second operator whose update collides
with yours (backends lock state during
an update; the collision surfaces as a
refusal, not a merge — described from
the documentation), programs with
thousands of resources whose previews
take minutes, and providers whose APIs
rate-limit the engine's enthusiasm.
None of that is a reason to avoid the
tool; all of it is beyond this guide's
evidence, and chapter 11's list of
undemonstrated facilities is the honest
boundary of what was shown.

## The local providers are teachers, not infrastructure

The command and random providers exist
in this guide so the lifecycle can be
learned without an account. Their
limits are the lesson, not the
product: a provider that writes files
cannot see drift, cannot promise the
file survives, and its resources are
exactly as durable as your shell
commands are careful. Do not build
anything you care about on them. The
shape they teach — declare, preview,
apply, reconcile, destroy — is the real
thing; the resources are not.
