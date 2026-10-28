# Recipes

Short, opinionated answers to the
situations this guide's readers will
actually meet. Each names the chapter
that proves or explains it.

## Practise the whole lifecycle where mistakes are free

Before a program touches a cloud
account, run its shape — declare,
preview, up, change, destroy — against
the local providers, as this guide did
(chapters 5 to 11). The command and
random providers need no account, cost
nothing, and exercise everything except
the cloud provider itself. When the
shape feels boring, swap in the real
provider and re-read chapter 14 first.

## Read the first line of every plan

`Previewing update (prod):` — the stack
name leads every preview, update and
destroy (chapter 8). The cheapest habit
in this guide: never confirm a plan
whose first line names a stack you did
not mean. Add `pulumi stack ls` before
any command you would not want run
against the wrong world.

## Keep the plan with the change

`pulumi preview` can save its plan to a
file, and `pulumi up` can be handed that
exact plan to apply. In team work, this
splits *reviewing* a change from
*applying* it: the plan is produced in
review, attached to the change, and
applied as reviewed. (The mechanism is
documented rather than run in this
guide's lab; the habit is the recipe.
Chapter 5 explains what a plan is and
how to read one.)

## One stack per environment, config doing the differing

`dev`, `staging`, `prod` as stacks;
sizes, counts, titles and endpoints as
config; secrets as secret config
(chapters 7 and 8). If two environments
need different *code*, that is a smell:
reach for a config value, a conditional
around a resource, or a component with
a parameter, in that order.

## Re-run up when in doubt

`up` converges; it does not repeat
(chapter 9). After an interrupted run,
a network failure or a colleague's
interruption, the safe move is to run it
again and read what it proposes. A
proposal of *no changes* is the tool
telling you the world already matches —
believe it, after the outside check
below.

## Verify outside the tool, on a schedule

Pulumi's account of a resource is the
provider's account (chapters 5 and 9).
Now and then, check the world directly:
list the files, call the API, read the
console. Especially after destroys
(chapter 10), and doubly so for anything
a command-style provider manages, where
Pulumi can neither read nor detect
drift.

## Treat the state file like the keys, because it is

Back it up; keep it off laptops that
travel unencrypted; put it on a shared
backend the moment a second person
shares the stack (chapter 6). Losing
state does not delete resources — it
orphans them, unmanaged and still
billing — and recovering starts with
`pulumi import`, the documented route
for adopting existing resources into
state, named here for the day you need
it and otherwise left to chapter 14's
warnings.

## Keep secrets out of terminals

`pulumi stack output` masks by default;
keep it that way (chapter 7). If a
script needs one value, take the single
named output, pass it in an environment
variable, and never let it near a log.
If a secret does get printed somewhere
with records, rotate it — in Pulumi
terms, that means replacing the resource
or value that generated it, and
re-reading chapter 7 on where copies
live: state, history and backups all
remember what terminals forget.

## Choose logical names like you mean it

Logical names live in state and plans
forever, and renaming one is a replace,
not a rename (chapter 11). Short,
stable, boring: `card-3`, not
`card-3-final-v2-really`. The physical
names providers generate can be as
decorative as they like; the logical
ones are the API between your program
and your state.
