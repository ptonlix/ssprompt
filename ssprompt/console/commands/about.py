from __future__ import annotations

from typing import TYPE_CHECKING

from ssprompt.console.commands.command import Command


if TYPE_CHECKING:
    from collections.abc import Callable


class AboutCommand(Command):
    name = "about"

    description = "Shows information about ssprompt."

    def handle(self) -> int:
        from ssprompt.utils._compat import metadata

        # The metadata.version that we import for Python 3.7 is untyped, work around
        # that.
        version: Callable[[str], str] = metadata.version

        self.line(f"""\
<info>ssprompt - A LLM Prompt distribution tool

Version: {version('ssprompt')}</info>

<comment>Change the world, even a little bit.
See <fg=blue>https://github.com/ptonlix/ssprompt</> for more information.</comment>\
""")

        return 0
