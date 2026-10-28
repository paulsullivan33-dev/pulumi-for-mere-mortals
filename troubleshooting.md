# Troubleshooting

The failures this guide's lab actually
met, plus the two checks that solve most
first-week confusion. Each entry names
its chapter in the moving-parts table
(chapter 2): program, language host,
engine, provider, backend, or config.

## The first preview takes minutes

Symptom: the first `pulumi preview` in a
new project sits for a long time,
printing pip's shopping list. Cause:
the language host creating the virtual
environment and installing
`requirements.txt`, and the engine
downloading provider plugins — once per
project and provider version (chapter
2). The lab's first preview spent over
a minute at this before planning
anything; every later run took seconds.
If a *later* run also crawls, suspect
the network the downloads need, or a
`requirements.txt` change that forced a
reinstall. Not a fault; do not "fix" it
by deleting the venv, which only buys
the same wait again.

## The program cannot reach its engine

Symptom (the lab's transcript
`pulumi-lab/transcripts/t90-preview-grpc-proxy-failure.txt`,
kept in full, pip noise and all):

```text
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses; last error: ... 127.0.0.1: ... Connection reset by peer"
pulumi.errors.RunError: Resource monitor has terminated, shutting down
```

Meaning: your program started, and
could not talk back to the engine that
launched it — the two internal addresses
of chapter 2. Everything else in the
run (install, plugins, login) had
already worked. This is a local
communications failure, and on an
ordinary machine the suspects are the
usual local ones: a proxy in the
environment variables (`http_proxy` and
friends) that should not be consulted
for loopback addresses — the lab's
first attempt was muddied by exactly
this, and the error then was a timeout
waiting for a handshake instead — a
firewall or endpoint-security tool
policing loopback, or a VPN client
with opinions about local traffic.

The lab's sandbox turned out to be the
sterner version: its network layer
resets the Python gRPC client's
connections over IPv4 loopback
specifically, while other programs —
and the same client over IPv6 loopback
(`[::1]`) — pass untouched. The lab
proved the shape by elimination: the
engine, providers and a YAML Pulumi
program ran perfectly; a standalone
Python gRPC client and server,
twenty lines each, failed the same way
the real program had. The cure used
here was local plumbing: two `socat`
relays listening on `[::1]`, forwarding
to the engine's IPv4 addresses, with
the language host's `--monitor` and
`--engine` arguments pointed at the
relays (`criteria.md` describes the
wrapper; no Pulumi component was
modified). You will not need this on a
normal network. Keep the diagnostic
shape, though: **when the error says
the monitor is unreachable, test
whether anything else can make the
same kind of connection, before
suspecting your program.** It is the
chapter 2 table read backwards — an
engine-side failure wearing the
program's clothes.

## Wrong passphrase

Symptom (transcript
`pulumi-lab/transcripts/t91-wrong-passphrase.txt`):

```text
$ PULUMI_CONFIG_PASSPHRASE=wrong-guess pulumi preview
error: getting stack configuration: get stack secrets manager: incorrect passphrase
```

The stack's secrets cannot be
decrypted, so nothing can run — config
is read before everything (chapter 7).
There is no recovery and no back door:
the right passphrase, or the stack's
secrets are gone for good. Check the
environment variable's spelling and
which shell exported it before
concluding the worst; in the lab this
error was produced on purpose, with a
guessed passphrase, to have it on
record.

## A Python error wears Pulumi's clothes, thinly

Symptom (transcript
`pulumi-lab/transcripts/t92-broken-program.txt`):

```text
error: Program failed with an unhandled exception:
  File ".../__main__.py", line 33, in <module>
    this_variable_does_not_exist()
NameError: name 'this_variable_does_not_exist' is not defined
```

This one is what it looks like: your
program is a program, and it crashed.
Pulumi shows the traceback with file
and line; the partial plan above it
(2 to create, 1 errored) is the engine
reporting how far the declarations got.
Fix the Python. A useful discipline:
the resources declared *before* the
crash were registered, so a program
that must fail should fail early —
validate config at the top, before
declaring anything expensive.

## The plan is for the wrong stack

Symptom: a preview proposes destroying
things you love, or creating duplicates
of things that exist. Cause, nine times
in ten: the selected stack is not the
one you think (`pulumi stack ls`, star
marks the spot), and the plan is an
accurate description of a world you did
not mean to edit. The state for the
stack you *did* mean is untouched;
select it and preview again. Chapter 8's
habit — the stack name is the first
line of every plan — exists for this
entry.

## pulumi new refuses: the folder is not empty

`pulumi new` writes into the current
folder and refuses if it finds files
there ("is not empty; use --force to
continue..."). It is protecting the
half-written project you forgot about.
Start in a fresh folder, or use
`--dir`; reach for `--force` only when
you can name every file it will
overwrite. The lab met this by
re-running the scaffold command in the
folder it had already scaffolded —
which is to say, by not reading its own
output. It is kept here because you
will do it too.
