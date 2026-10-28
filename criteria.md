# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's notice board belongs to a fictional village hall.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 14 names what the tool
   cannot do: state as a losable memory, providers that cannot
   read and so cannot see drift, values that cannot be known
   before they exist, the program as untrusted code, and
   secrets that are encrypted rather than abolished.
8. **The safety rules are in the text, early.** The state file
   as the keys to the stack (chapter 6), secrets masked by
   default and printed only on explicit request (chapter 7),
   and the wrong-stack check — read the plan's first line —
   all appear before any procedure depends on them.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox.
Pulumi **3.272.0** was installed from the official release
tarball into a scratch folder, logged in to the local backend
only (`pulumi login --local`, file://~) — no Pulumi Cloud or
cloud-provider account exists in this lab. The program
(`pulumi-lab/project/`) uses two providers that work entirely
on the local machine: pulumi-random 4.21.4 and
pulumi-command 1.2.1, with the Python SDK 3.272.0 in the
project's own virtual environment. All transcripts live in
`pulumi-lab/transcripts/`.

Run for real, with transcripts as evidence:

- Install and version (t00); local login and `whoami` showing
  the `file://~` backend and the OS user (t01).
- Stack creation and the stack census (t02); config set, a
  secret config value set with `--secret`, and the resulting
  `Pulumi.dev.yaml` showing the secret as a `secure:` blob
  (t03).
- `pulumi new python --generate-only` and the exact scaffold
  it writes (t13).
- First preview of the lab program: six creates, outputs
  `[unknown]` / `[secret]` / known as predicted in chapter 4
  (t04); `pulumi up --yes` applying it, the generated board
  name (finer-earwig), and the three notice files proven with
  `ls` and `cat` (t05).
- Stack outputs masked, then revealed with `--show-secrets`,
  including a single named output printed bare for scripts
  (t06). The PIN so revealed was then searched for in the
  state file: zero occurrences — secrets are ciphertext in
  state (checked directly against
  `~/.pulumi/stacks/notice-board/dev.json`, which was also
  read to confirm its eight recorded resources: the stack,
  two provider records, five declared resources).
- A config change (pinCount 3 to 5) previewed first: two
  creates and three updates with `[diff: ~create]`, the
  updates traced to the stack total embedded in each card's
  command (t07); applied, five files verified, and a second
  identical `up` reporting 8 unchanged (t08).
- A second stack (prod) with its own config, its own board
  name and PIN, two cards, and no signing-key output (t09);
  the two-stack census (t09, t12).
- Drift: a card edited by hand, followed by
  `pulumi refresh --yes` and `pulumi preview`, both reporting
  8 unchanged — the command provider cannot read, so it
  cannot see the edit (t10).
- `pulumi destroy` on prod (t11) and dev (t12), with the
  files checked gone on disk after each; prod's destroy
  removed two files dev's state still claimed, because both
  stacks' cards shared one folder — kept in the text as the
  lab's most instructive failure. `pulumi stack rm prod`
  removing the stack, its state and its config file (t12).
- A stack with no config at all, previewed to confirm the
  program's built-in defaults and the absent secret output
  (t14).
- Error paths, produced deliberately: a wrong
  `PULUMI_CONFIG_PASSPHRASE` refused with "incorrect
  passphrase" before anything ran (t91), and a program with
  an injected `NameError` reported by Pulumi with the Python
  traceback, file and line (t92).

The sandbox's network quirk, and the lab's cure, in full:
the sandbox silently resets gRPC connections that the
**Python** gRPC client makes over IPv4 loopback, while other
clients — and the same client over IPv6 loopback — pass
untouched. Pulumi's engine hands the Python program its
resource-monitor and engine addresses as 127.0.0.1 arguments,
so no Python Pulumi program could start; the first preview
failed with `StatusCode.UNAVAILABLE ... Connection reset by
peer` and "Resource monitor has terminated" (t90, kept
complete). The diagnosis was by elimination, and each step
was run, not reasoned: the engine, both provider plugins
and a Pulumi YAML program (whose language host is not
Python) all worked over the same addresses; a twenty-line
standalone Python gRPC client and server reproduced the
reset on an unrelated port, and the identical pair succeeded
over `[::1]`. The lab then wrapped `pulumi-language-python-exec`
in its scratch Pulumi install with a small script that starts
two `socat` relays — listening on `[::1]`, forwarding with
ordinary sockets to the engine's 127.0.0.1 listeners — rewrites
the `--monitor` and `--engine` arguments to the relay
endpoints, and runs the real exec script otherwise untouched.
Every transcript above except t90 was produced through that
relay. It is a dumb byte pipe: no Pulumi code, protocol,
state or output was modified, and on an ordinary network
none of it is needed. Chapter 15 tells the story as
troubleshooting, because the error's shape — a program that
cannot reach its engine — is one readers can meet for
ordinary local reasons (proxy variables, firewalls), even
though this lab's cause was exotic.

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- Pulumi Cloud and every hosted feature: accounts, teams,
  access control, hosted history and deployments; likewise
  self-managed backends on cloud object storage.
- All cloud and Kubernetes providers and their resources:
  creating real servers, buckets and networks; drift
  detection and refresh against providers that implement
  reading; update collisions and state locking between
  operators; behaviour at thousands of resources.
- `pulumi import`, saved plans applied with
  `pulumi up --plan`, renaming via aliases, `config.require`,
  secret rotation by replacement.
- Chapter 12's second half: `Output.apply`, component
  resources, `StackReference`, dynamic providers, mock-based
  unit tests of programs, policy packs and transformations.
- Install routes other than the release tarball (the install
  script and the platform package managers), and the
  non-Python languages beyond their existence.
- The comparison tools in chapter 13 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
notice board for a fictional village hall and a fictional
library, invented titles, an invented signing key and a
generated PIN, all printed in the guide precisely because
they protect nothing. No example is modelled on any real
person, network, service or organisation.
