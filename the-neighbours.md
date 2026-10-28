# The Neighbours

Pulumi is one answer to "how do we make
infrastructure repeatable". These are
the others you will meet, characterised
fairly — none of them was run for this
chapter, and nothing here is a
benchmark; two of them have full guides
in this series, which say more and say
it from their own labs.

## Terraform

The elder of the family, and the tool
Pulumi is most often compared with —
this series' Terraform guide teaches it
from its own lab. The model is the
same family resemblance: declarations,
a state file, providers, a plan before
an apply (`terraform plan` is the direct
cousin of `pulumi preview`). The
differences are the language and the
centre of gravity. Terraform's
declarations are written in **HCL**, a
configuration language made for the
purpose: very readable for lists of
resources, increasingly awkward as
logic grows, and useless outside
Terraform. Pulumi's bet is that you
would rather bring a language you know,
with its loops, libraries and tests.
Terraform's provider catalogue and
community are the larger and older; if
a thing can be provisioned at all,
someone has usually written the
Terraform provider first. Choose
Terraform for the ecosystem and the
declarative purity; choose Pulumi when
the infrastructure logic itself has
become a program.

## Ansible

Ansible describes the **inside** of
machines: packages installed, files
placed, services running, users present.
Its playbooks are YAML, its unit of work
is the task, and it is normally run
against machines that already exist.
Pulumi describes the machines (and
networks, and buckets) themselves,
existing. The two are complements more
than rivals: a common pattern is Pulumi
or Terraform to create the fleet,
Ansible to dress it. Ansible also has a
guide in this series, built from its
own lab. Where the line blurs — both
can run a command on a host — prefer the
tool whose *state* story you want:
Ansible runs tasks and reports changes
it made; Pulumi remembers resources and
reconciles them, which is why this
guide's command provider is a teaching
device and Ansible is a profession.

## CloudFormation and the AWS CDK

Every cloud has a native tool;
CloudFormation is Amazon's — templates
in JSON or YAML, state kept by the
service, no file of yours to lose.
Its interest here is the **CDK**: AWS's
framework that lets you write TypeScript
or Python which *generates*
CloudFormation templates. That is
Pulumi's idea — real languages for
infrastructure — arriving from inside
one cloud, with the trade stated
plainly: the CDK's world ends at
Amazon's border, while Pulumi's
providers cross clouds and reach
Kubernetes and local tools alike; the
CDK's state, in exchange, is the
cloud's own problem, never a file on
your disk. Similar natives elsewhere
(Azure's Bicep, Google's Deployment
Manager lineage) make the same trade in
their own colours.

## Kubernetes YAML and Helm

If your infrastructure is one
Kubernetes cluster, its own declarative
YAML — or Helm charts packaging it — is
the incumbent tool, and it is genuinely
declarative: the cluster reconciles
continuously, not only when a command
runs. Pulumi reaches Kubernetes through
a provider like any other cloud, and
adds the surrounding world (the cluster
itself, the network under it) to the
same program. The Kubernetes guide in
this series covers the cluster's own
model. The choice is scope: one
cluster's contents, or everything the
cluster stands on, in one state.

## Plain scripts

The oldest neighbour: a shell script
that creates things in order. Scripts
win on transparency — nothing between
you and the commands — and lose on
everything this guide is about: no
state, so no plan, no convergence, no
destroy list, no record of what exists.
Run a script twice and you hold the
consequences yourself. Note the
irony the lab makes visible: Pulumi's
command provider is, deliberately, a
script wrapped in state — the create
and delete commands are yours, and
Pulumi contributes the remembering,
the planning and the ordering. That
wrapping is most of the value of the
whole family; the script alone is the
part you were already able to write.
