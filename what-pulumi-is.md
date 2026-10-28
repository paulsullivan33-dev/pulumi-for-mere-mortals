# What Pulumi Is

Setting up infrastructure by hand goes
like this: you click in a console or type
commands, one resource at a time — a
server here, a storage bucket there, a
setting changed somewhere else — and
three months later nobody can say exactly
what exists, why, or how to build it
again. **Infrastructure as code** is the
fix: you write down what should exist,
in a file, and a tool makes the world
match the writing.

**Pulumi is an infrastructure as code
tool whose writing is an ordinary
program.** Where most tools in this
family invented a configuration language
for the purpose, Pulumi takes programs
written in general-purpose languages —
Python in this guide; TypeScript, Go,
C#, Java and a YAML form also exist —
and treats the program as the description.
A line like

```python
board_name = random.RandomPet("board-name", length=2)
```

does not call a library and get a value
back in the usual way. It *declares*:
there should be a random pet name, two
words long, and I will call it
`board-name`. Pulumi's **engine** reads
the whole program, compares the
declarations with what it built last
time (its **state**, chapter 6), works
out the difference, and asks the right
**provider** — a plugin that knows how
to talk to one kind of system — to create,
change or delete real things until the
world matches the program again.

## The three ideas everything hangs on

**Declaration, not steps.** Your program
says what should exist, not how to build
it in order. If you run it twice, the
second run changes nothing, because the
world already matches — the lab ran
exactly that experiment (transcript
`pulumi-lab/transcripts/t08-update-and-noop.txt`:
the second `pulumi up` reports
*8 unchanged*). This property has a name,
**idempotency**, and it is what separates
this family of tools from a script that
just runs commands top to bottom: a
script run twice creates two of
everything, or fails; a declaration run
twice converges.

**Preview before change.** Before
applying anything, `pulumi preview`
runs the program, compares it with state,
and prints the plan: these resources to
create, these to update, these to
delete, with the same signs the lab's
transcripts use — `+` create, `~`
update, `-` delete. `pulumi up` then
shows the same plan again and does it.
Chapter 5 is built around reading that
plan, because the preview is where
mistakes are cheap.

**State is the memory.** Pulumi does not
rediscover the world from scratch each
run. It keeps a state file per **stack**
(chapter 8) listing every resource it
manages, with the values providers
returned — including, encrypted, the
secret ones. The state is what lets a
two-word random name stay *the same*
name on every run: it was generated once
and remembered. Chapter 6 opens the file
and looks inside. It also follows that
the state file matters: lose it, and
Pulumi forgets what it built; the
resources still exist but are no longer
managed. Chapter 14 returns to that.

## Outputs: the values that are not known yet

A declared resource's real values exist
only after a provider creates it. The
board's name is chosen by the random
provider at apply time; in the preview it
shows as `[unknown]`. Pulumi programs are
built to cope with this: values flow
through the program wrapped in a type
called an **Output**, which means "a
value that will be known later", and a
program's final results are declared
with `pulumi.export(...)`. After
`pulumi up`, those exports are the
**stack outputs** — readable any time
with `pulumi stack output`, chapter 7 —
some of them secret, and shown as
`[secret]` until you explicitly ask to
see them.

## What the lab's program declares

So the whole guide can be followed on
one small example, the lab built a
notice board for a fictional village
hall (`pulumi-lab/project/__main__.py`).
It declares five resources:

- a two-word random name for the board
  (`random:RandomPet`),
- a six-digit PIN for the board's lock
  box (`random:RandomPassword`, whose
  result is automatically secret),
- three notice cards, each a small text
  file written by an ordinary shell
  command (`command:local:Command`) —
  one per pin, and the number of pins is
  a setting.

Neither provider needs an account,
a network service, or anyone's
permission: the random provider invents
values locally, and the command provider
runs commands on the machine itself.
That is a deliberate choice, not a toy.
Every behaviour this guide teaches —
preview, state, secrets, stacks, update,
destroy — is fully exercised by these
two providers, and the day you swap in a
cloud provider, the shape of the work
does not change. What the lab could not
exercise that way, it labels
documented-only; `criteria.md` keeps the
ledger.

Check: after installing (chapter 3) and
creating the first stack, the lab's
first preview of this program reads
(transcript `pulumi-lab/transcripts/t04-preview.txt`):

```text
Resources:
    + 6 to create
```

Six, not five: the stack itself is
counted as a resource too.

## Who it is for

The programmer who already writes Python
(or TypeScript, or Go) and would rather
describe infrastructure with loops,
functions and libraries they know than
learn a single-purpose language. The
team whose infrastructure has grown past
hand-built and needs a written,
reviewable, repeatable description. The
learner who wants the infrastructure as
code model itself — declaration, state,
preview, providers — with the training
wheels of local resources before a cloud
bill is involved. If you have never
met the model at all, the Terraform
guide in this series teaches the same
ideas from the other tradition; the two
tools are compared in chapter 13.

## What it is not

Pulumi is not a configuration manager
for the inside of a machine: it creates
the machine; what runs on it afterwards
is Ansible's country (chapter 13). It is
not a deployment pipeline: it can be run
by one, and hosted automation exists, but
the tool itself is the engine and the
program, not the pipeline around them.
It is not magic about the world: it
knows only what its providers can see,
and chapter 9 shows a change it could
not see at all. And it is not the only
way to hold state or secrets — it keeps
both in files you are responsible for,
which chapter 6 treats with the
seriousness it deserves.
