"""A notice board that exists only on this machine.

Pulumi programs describe things and let providers make them real.
The two providers used here need no cloud account at all:

- pulumi-random invents values (names, passwords) and remembers
  them in state, so they stay the same on every later run.
- pulumi-command runs ordinary shell commands on this machine,
  so a "resource" here is a text file written by printf.

Everything else in the file is plain Python: a loop, a config
lookup, string formatting. That is the point of Pulumi - the
infrastructure is described in a real programming language.
"""

import pulumi
from pulumi import Config, export
import pulumi_random as random
import pulumi_command as command

# Settings for this stack, read from Pulumi.<stack>.yaml.
# `pulumi config set boardTitle "..."` changes them per stack.
config = Config()
title = config.get("boardTitle") or "Community Notice Board"
pin_count = config.get_int("pinCount") or 3
signing_key = config.get_secret("signingKey")

# A friendly two-word name for the board. The random provider
# generates it once; the value is stored in the stack's state,
# so preview and up agree about it and it never changes
# unless this resource is replaced or deleted.
board_name = random.RandomPet("board-name", length=2)

# The PIN for the board's lock box. RandomPassword marks its
# result secret, and the secret stays encrypted in state:
# `pulumi stack output` shows [secret] unless asked not to.
lockbox_pin = random.RandomPassword(
    "lockbox-pin",
    length=6,
    numeric=True,
    upper=False,
    lower=False,
    special=False,
)

# One notice card per pin. Each card is a small text file in
# the project folder, written by the command provider. The
# delete command is what `pulumi destroy` will run later.
for i in range(pin_count):
    command.local.Command(
        f"card-{i + 1}",
        create=f"printf 'Notice {i + 1} of {pin_count}: bring a mug, borrow a book. Board: {title}\\n' > notice-{i + 1}.txt",
        delete=f"rm -f notice-{i + 1}.txt",
    )

# Stack outputs: the values someone running this program
# probably wants to read back. The PIN is exported straight
# from the secret value, so the output is secret too.
export("board_title", title)
export("board_name", board_name.id)
export("lockbox_pin", lockbox_pin.result)
export("signing_key", signing_key)
