# Writing Real Programs

The lab's program is forty lines. Real
ones are hundreds, declare dozens of
resource types, and are read by teams.
This chapter covers the step from one
to the other: what the lab's program
already demonstrates about writing
Pulumi in a real language, and the
facilities bigger programs use that this
lab describes from the documentation
instead — labelled as such, per the
rule of the house.

## What the small program already shows

**The language is not a costume.** The
notice board's card loop is a Python
`for` over a number from config;
nothing in it is Pulumi-specific except
the resource constructor it calls. The
same ordinariness scales: a list of
names from a JSON file can drive one
resource per entry; a function can take
settings and declare a standard set of
resources; a `requirements.txt` package
can be imported and used to compute an
input. When a configuration language
would make you learn *its* loop, *its*
functions and *its* string handling,
Pulumi makes you learn none — you
already know Python's, including how to
test them, which is the deeper point:
**the parts of a Pulumi program that do
not declare resources are ordinary code,
and ordinary code can be unit-tested
with ordinary tools** before Pulumi is
involved at all.

**Outputs are values with a fuse on
them.** Chapter 4 exported
`board_name.id` before it existed.
Everything in a Pulumi program that
comes from a resource is an **Output**:
a promise the engine resolves during
the run. Programs mostly pass Outputs
straight into other resources' inputs —
a server's generated address into a
record that must point at it — and the
engine reads those hand-offs as
dependencies, which is how it knows the
order to build in and what must be
rebuilt when something changes. What
you cannot honestly do with an Output is
treat it as a plain value *now*:
print it at preview time, branch on it,
do arithmetic on it in the open. At
preview time it may simply not exist
yet.

**Naming is two decisions.** Every
resource has the **logical name** your
program gives it (`"card-3"`) — the name
in state, in plans, in URNs — and
whatever physical name the provider
gives the real thing (for `RandomPet`,
the name itself; for the cards, the
file name). Logical names are yours to
keep stable: renaming one in code is,
to the engine, a delete and a create,
unless you use the documented renaming
mechanisms (`aliases`) — described here,
not run in the lab. Choose logical
names the way you choose variable
names you will have to live with.

## Described, not demonstrated

The following are standard Pulumi
practice, in the documentation's terms,
and are **not** verified by this guide's
lab. They are named so you know they
exist when a real program needs them,
and so nothing in this chapter pretends
the lab ran them.

- **`Output.apply(...)`** — the way to
  compute with a value once it exists:
  "when this address is known, format it
  like so." The transformation runs
  inside the run, at the right moment,
  and secrecy propagates through it.
- **Component resources** — a class in
  your program that bundles several
  resources into one reusable,
  named unit ("a website" made of a
  bucket, a distribution and a record),
  so big programs are built from
  meaningful pieces rather than long
  lists. The bundle appears in plans
  and state as one parent resource.
- **`StackReference`** — reading another
  stack's outputs from a program, the
  sanctioned way for one stack's world
  to depend on another's (a network
  stack feeding an application stack).
- **Dynamic providers** — writing a
  provider inline, in the program, for
  a resource no existing provider
  covers: a small class implementing
  create/read/update/delete in Python.
  The command provider in this guide is
  the humble pre-built relative of the
  idea.
- **Mocks and unit tests for the
  declarations themselves** — the Python
  SDK can run a program against fake
  providers, so a test can assert "this
  program declares a card per pin"
  without building anything.
- **Policy packs and transformations** —
  organisation rules enforced at preview
  time ("nothing public", "names must
  start so"), and program-wide edits
  applied to every resource of a type.

A reader who needs any of these is past
the mere-mortals stage for this tool,
and the official documentation — which
this chapter follows for everything in
this section — is the right next read.
What the lab *did* establish is the
ground they all stand on: a program
declares, the engine plans against
state, providers act, outputs publish
the results. That much is verified
end to end, and it does not change when
the program grows.
