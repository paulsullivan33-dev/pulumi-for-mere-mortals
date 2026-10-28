# Destroying Things

Everything a stack created, its stack
can take down — in reverse dependency
order, by the same plan-then-act shape
as creation. `pulumi destroy` is the
command, and this chapter runs it on
both of the lab's stacks, reads what it
leaves behind, and finishes the job
properly with `pulumi stack rm`.

## Destroying prod

```bash
pulumi stack select prod
pulumi destroy --yes
```

(transcript
`pulumi-lab/transcripts/t11-destroy-prod.txt`).
The preview inside the destroy reads:

```text
 -  random:index:RandomPet board-name delete
 -  command:local:Command card-2 delete
 -  command:local:Command card-1 delete
 -  random:index:RandomPassword lockbox-pin delete
 -  pulumi:pulumi:Stack notice-board-prod delete
Resources:
    - 5 to delete
```

and the run itself deletes each resource
through its provider: for the cards,
that means running the `delete` command
from the program — `rm -f notice-1.txt`
and `rm -f notice-2.txt`. Five deleted,
and then the message that teaches the
chapter's main distinction:

```text
The resources in the stack have been deleted, but the history
and configuration associated with the stack are still maintained.
If you want to remove the stack completely, run `pulumi stack rm prod`.
```

**Destroy removes resources; it does not
remove the stack.** The state file
remains, now recording an empty world;
the config remains; the history of every
update remains. That is usually what you
want — environments are destroyed and
recreated, and the stack is the
environment's identity — but it means
"we destroyed it" and "it is gone from
Pulumi" are different sentences, and
only the second needs `stack rm`.

## The shared-folder debt comes due

Remember chapter 8's leak: `prod`'s
cards wrote the same `notice-1.txt` and
`notice-2.txt` that `dev` manages. The
check after the destroy:

```text
$ ls notice-*.txt
notice-3.txt
notice-4.txt
notice-5.txt
```

`prod`'s destroy deleted `dev`'s first
two cards, because on disk they were
the *same* files, and nothing in either
state file could say so. `dev`'s state
still lists card-1 and card-2 as
existing resources; the world disagrees;
and because this provider cannot read
(chapter 9), no refresh will ever
reconcile them. On real infrastructure,
recall, each stack's resources are
distinct objects and this cannot
happen; the lab's collision is the
small, survivable version of pointing
two stacks at one shared thing. It is
recorded here rather than tidied away
because it is the most instructive
failure in the whole lab: **stacks
isolate state, not the world.**

## Destroying dev, and removing a stack

The same shape, bigger (transcript
`pulumi-lab/transcripts/t12-destroy-dev.txt`):
`pulumi destroy --yes` on `dev` previews
8 deletions and runs them — the five
cards' `rm` commands (two of them
removing files already gone, which
`rm -f` absorbs silently; destroy does
not fail on a card the world had already
lost), both random resources, and the
stack record. Then the filesystem check:

```text
$ ls notice-*.txt
ls: cannot access 'notice-*.txt': No such file or directory
```

and the tidying pair:

```text
$ pulumi stack rm prod --yes
Stack 'prod' has been removed!
$ pulumi stack ls
NAME  LAST UPDATE  RESOURCE COUNT
dev   now          0
```

`stack rm` deletes the stack itself:
its state file, its history, and its
`Pulumi.<stack>.yaml` config file all go
(`Pulumi.prod.yaml` vanished from the
project folder with it). It refuses to
remove a stack that still has resources
unless you destroy first — the order in
this chapter is the only order there is.
The lab left `dev` standing but empty:
a stack with zero resources, a config
file, and a history — a fair picture of
an environment between deployments, and
the state the lab's machine was left in.

## What destroy cannot do

Three edges, stated plainly here and
again in chapter 14. Destroy deletes
what **state** lists: a resource someone
removed from the program *and* from
state (or a resource created by hand
outside Pulumi) is invisible to it.
Destroy trusts providers: a provider
that reports success without deleting
leaves the world and the records
disagreeing in the dangerous direction.
And destroy is only as reversible as
the resources are: state keeps history,
but the files are gone, the name
finer-earwig is released, and a fresh
`up` would invent a different board.
Deletion in Pulumi is honest, planned
and confirmed — and final.
