# The Moving Parts

Pulumi looks like one command, `pulumi`,
but a run involves several programs
passing work between them. Knowing which
part does what turns most confusion into
a named problem: is this a failure of my
program, of a provider, or of the
engine's memory? This chapter is the map.

## The command-line tool and the engine

The **`pulumi` command** is what you
install and type. Inside it sits the
**engine**: the part that runs your
program, holds the current plan, compares
declarations against **state**, decides
the order of operations (a resource that
another resource depends on is built
first), and records the outcome. When
you read that an update "failed at step
3", the engine is the narrator.

## The language host: how your program runs

Your program is Python, and the engine
is not, so the engine starts a
**language host** for your language —
small bridge programs that ship with the
CLI, one per supported language. The
Python host sets up the project's
**virtual environment** (a private folder
of Python packages, chapter 4), installs
the packages listed in
`requirements.txt` on first use, and runs
`__main__.py`, passing it two internal
addresses: the **resource monitor**,
where the program registers each
declaration it makes, and the **engine**
address, where it sends log messages.
Every `random.RandomPet(...)` line in
your program is, under the covers, a
message to the monitor saying *a resource
of this type, with these inputs, called
by this name*.

That first setup is why the very first
`pulumi preview` takes far longer than
every later one: the lab's first preview
spent most of its time creating the venv
and downloading packages before any
planning happened (the full log is kept
as transcript
`pulumi-lab/transcripts/t90-preview-grpc-proxy-failure.txt`,
kept because of what else it shows —
chapter 15 tells that story).

## Providers and plugins

A **provider** is a separate program —
a plugin the engine downloads on demand
and runs alongside itself — that knows
how to create, read, update and delete
one family of resources. The mapping is
in the resource's type name, which you
can read in every transcript:

```text
random:index:RandomPet
command:local:Command
```

Read it as *package : module : type*.
The random package's provider knows how
to invent names and passwords and —
just as important — how to *remember*
them in state so they do not change on
the next run. The command package's
provider runs shell commands on the
local machine: the `create` command when
a resource is created, the `delete`
command when it is destroyed. Cloud
providers — the packages for Amazon,
Azure, Google Cloud, Kubernetes and
hundreds more — are the same mechanism
with bigger reach: the engine neither
knows nor cares whether creating a
resource means writing a local file or
calling a cloud API across the world.

When a preview needs a provider the
machine has not seen, the engine
downloads the plugin first and says so.
The lab's first preview again:

```text
Downloading plugin random-4.21.4: starting
Downloading plugin command-1.2.1: starting
```

Plugins are kept under the Pulumi home
folder (in the lab,
`pulumi-lab`'s runs stored them under the
folder named by `PULUMI_HOME`), so the
download happens once per provider
version, not once per run.

## The backend: where state lives

The engine's memory — one **state** file
per stack — has to live somewhere, and
the somewhere is the **backend**. Two
kinds matter for this guide:

- The **local backend** (also called the
  file or DIY backend): state as JSON
  files on a disk you control — a folder
  on your machine, or a file URL pointing
  at shared storage. No account, no
  service. This is what the lab used, via
  `pulumi login --local`, and chapter 6
  opens the files.
- **Pulumi Cloud**: the hosted backend,
  which stores state for you and adds
  teams, access control and history on a
  website. It is the default when you
  `pulumi login` with a token. The lab
  did not use it; it is described in
  chapter 6 and labelled documented-only.

Logging in does not move your resources
or your program. It only tells the CLI
which backend's state to read and write.
The same program, the same providers,
either way.

## The project, the program, and the stack

Three nouns the rest of the guide uses
constantly:

- A **project** is a folder with a
  `Pulumi.yaml` in it: a name, a
  language, and the program
  (`__main__.py` for Python). It is the
  unit you put in version control.
- The **program** is the code: the
  declarations, the config lookups, the
  exports.
- A **stack** is one independent copy of
  the project's world: its own state, its
  own configuration values (kept in
  `Pulumi.<stack>.yaml` next to the
  project file), its own outputs. The
  same program run under two stacks
  builds two separate sets of resources —
  `dev` and `prod` in chapter 8 — the way
  the same recipe baked twice makes two
  cakes.

## Who holds what — the summary table

| Part | Holds | If it breaks |
| --- | --- | --- |
| Your program | The declarations — what should exist | Your bug: a Python error, a wrong value |
| Language host | The running of your program, the venv | Install and package problems live here |
| Engine | The plan, the ordering, the comparison with state | The run stops; state keeps the last good record |
| Provider plugin | The know-how for one resource family | Resources of that family cannot be created or read |
| Backend | The state files, one per stack | Pulumi forgets what it built — chapter 14 |
| Config files | Per-stack settings and encrypted secrets | Wrong values flow in; the program does what it was told |

Chapter 15's troubleshooting is mostly
this table read backwards.
