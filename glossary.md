# Glossary

**Backend** — where stack state is
stored. The local backend keeps JSON
files on disk (`file://~` for the
account's home); Pulumi Cloud is the
hosted backend. Chapter 6.

**Component resource** — a bundle of
resources declared by a class in your
program and treated as one unit.
Described, not demonstrated, in
chapter 11.

**Config** — per-stack settings, stored
in `Pulumi.<stack>.yaml`, read in the
program through the `Config` object.
Secret config values are stored
encrypted. Chapter 7.

**Destroy** — `pulumi destroy`: delete
every resource a stack's state lists,
in reverse dependency order. The stack
itself survives until `pulumi stack
rm`. Chapter 10.

**Drift** — a difference between state
and the real world, caused by changes
made outside Pulumi. Detected by
`pulumi refresh` only for providers
that can read their resources.
Chapter 9.

**Engine** — the part of the CLI that
runs programs, compares declarations
with state, orders the work and records
the result. Chapter 2.

**Export** — to publish a value from a
program as a stack output:
`pulumi.export("name", value)`.

**Idempotency** — running the same
declarations twice converges instead of
repeating: the second `pulumi up`
changes nothing. Chapters 1 and 9.

**Language host** — the bridge program
that runs your code for the engine,
one per supported language; for Python
it manages the project's virtual
environment. Chapter 2.

**Logical name** — the name your
program gives a resource (`"card-3"`),
used in state, plans and URNs, as
opposed to the physical name the real
thing ends up with. Chapter 11.

**Output** — a value that will be known
later: the type of everything a
resource returns, resolved by the
engine during a run, shown as
`[unknown]` in previews until then.

**Plugin** — a provider or language
host as a downloadable program, fetched
by the engine on first need and cached
under the Pulumi home folder.

**Preview** — `pulumi preview`: run the
program, compare with state, print the
plan, change nothing. Also the plan
itself. Chapter 5.

**Program** — your code: the file
(`__main__.py` for Python) whose
declarations describe what should
exist.

**Project** — a folder holding
`Pulumi.yaml`: a name, a runtime, and
the program. The unit kept in version
control.

**Provider** — the plugin that knows
how to create, read, update and delete
one family of resources — random,
command, or a cloud's whole catalogue.
Chapter 2.

**Refresh** — `pulumi refresh`: re-read
every resource through its provider
and bring state in line with the world
before planning. Chapter 9.

**Resource** — one declared thing under
management: a random name, a file, a
server. Identified in state by its
**URN** — stack, project, type and
logical name in one string.

**Resource monitor** — the engine's
inbox, the internal address where a
running program registers each
declaration. Chapter 2; its
unreachability is chapter 15's main
event.

**Secret** — a value marked as
sensitive: encrypted in state and
config, masked on screen, revealed
only by asking explicitly
(`--show-secrets`). Chapters 6 and 7.

**Stack** — one independent copy of a
project's world: its own state, config
and outputs. `dev` and `prod` in this
guide. Chapter 8.

**Stack output** — a value a program
exported, readable afterwards with
`pulumi stack output`.

**State** — the per-stack record of
what exists: every resource, its inputs
and returned values, and the stack
outputs. The engine's memory; the file
you must not lose. Chapter 6.

**Up** — `pulumi up`: show the plan and
carry it out.
