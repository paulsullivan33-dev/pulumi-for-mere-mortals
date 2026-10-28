# Installing Pulumi

This chapter installs the `pulumi`
command and points it at the **local
backend**, so everything that follows
works with no account, no token and no
cloud. You need a terminal and, for the
Python route this guide teaches, Python
3 on the machine — the project creates
its own virtual environment in chapter
4, so nothing about your system Python
is touched.

## The install

Pulumi ships one archive per platform
containing the CLI and its language
hosts. The official routes — an install
script on Linux and macOS, an installer
or a package manager (`brew`, `winget`,
`choco`) on the usual terms — are listed
on the project's download page; all of
them end at the same `pulumi` command.
This guide's lab did it by hand to keep
the whole installation in one folder it
could delete afterwards: it downloaded
the release tarball for its platform
from the project's GitHub releases,
unpacked it, and put the resulting
`pulumi` folder on the `PATH`:

```bash
curl -fsSL -o pulumi.tar.gz \
  https://github.com/pulumi/pulumi/releases/download/v3.272.0/pulumi-v3.272.0-linux-x64.tar.gz
tar xzf pulumi.tar.gz
export PATH=$PWD/pulumi:$PATH
pulumi version
```

Check: the version prints, and the lab's
reading (transcript
`pulumi-lab/transcripts/t00-version.txt`)
is the version this whole guide was
verified against:

```text
$ pulumi version
v3.272.0
```

## Logging in — to your own disk

`pulumi login` normally means Pulumi
Cloud: a token, an account, state stored
on Pulumi's service. For this guide, and
for any private experiment, the local
backend is the better start:

```bash
pulumi login --local
pulumi whoami
```

The lab's transcript
(`pulumi-lab/transcripts/t01-login.txt`):

```text
$ pulumi login --local
Logged in to htch-runtime as root (file://~)
$ pulumi whoami
root
```

Read that answer carefully, because it
is the whole arrangement in one line:
you are logged in *as your own operating
system user*, to a backend whose address
is `file://~` — state will be stored in
files under your home folder (chapter 6
shows exactly where). No credentials
exist because none are needed: whoever
can read those files owns the state,
which is a fact to remember, not a
problem to solve today.

Two consequences worth knowing at the
start:

- **Nothing leaves the machine.** The
  CLI may check for a newer version and
  will download provider plugins the
  first time a program needs them
  (chapter 2); state, config and secrets
  stay local.
- **The arrangement is per machine and
  per folder of state.** Teammates each
  having a local backend have *separate*
  memories of the world; shared work
  wants a shared backend (Pulumi Cloud,
  or a file backend on shared storage —
  documented-only in this guide, chapter
  7). For learning, and for one person
  and their own machines, local is not a
  compromise; it is the honest tool.

## What you have now

A `pulumi` command that answers
`version` and `whoami`, a local backend
with no stacks yet, and no project.
Chapter 4 makes the project; chapter 5
runs it. If `pulumi version` fails with
"command not found", the `pulumi`
folder is not on your `PATH` — that
check, boring as it is, is the fix for
most first-run confusion on every
platform, the installers included.
