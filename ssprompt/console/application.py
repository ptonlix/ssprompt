from __future__ import annotations

import logging
import re
from contextlib import suppress
from importlib import import_module
from typing import TYPE_CHECKING, cast

from cleo.application import Application as BaseApplication
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from cleo.exceptions import CleoError
from cleo.formatters.style import Style
from cleo.io.null_io import NullIO

from ssprompt.__version__ import __version__
from ssprompt.console.command_loader import CommandLoader
from ssprompt.console.commands.command import Command
from ssprompt.ssprompt import Ssprompt

if TYPE_CHECKING:
    from collections.abc import Callable

    from cleo.events.event import Event
    from cleo.io.inputs.argv_input import ArgvInput
    from cleo.io.inputs.definition import Definition
    from cleo.io.inputs.input import Input
    from cleo.io.io import IO
    from cleo.io.outputs.output import Output

    from ssprompt.ssprompt import Ssprompt

def load_command(name: str) -> Callable[[], Command]:
    def _load() -> Command:
        words = name.split(" ")
        module = import_module("ssprompt.console.commands." + ".".join(words))
        command_class = getattr(module, "".join(c.title() for c in words) + "Command")
        command: Command = command_class()
        return command

    return _load

COMMANDS = [
    "about",
    "add",
    "init",
    "new",
    "pull",
    "show",
    "version",
]

class Application(BaseApplication):


    def __init__(self) -> None:
        super().__init__("ssprompt", __version__)

        self._ssprompt: Ssprompt | None = None
        self._io: IO | None = None

        dispatcher = EventDispatcher()
        dispatcher.add_listener(str(COMMAND), self.register_command_loggers)
        self.set_event_dispatcher(dispatcher)

        command_loader = CommandLoader({name: load_command(name) for name in COMMANDS})
        self.set_command_loader(command_loader)

    @property
    def ssprompt(self) -> Ssprompt:

        if self._ssprompt is not None:
            return self._ssprompt

        self._ssprompt = Ssprompt()

        return self._ssprompt

    def reset_ssprompt(self) -> None:
        self._ssprompt = None

    def create_io(
        self,
        input: Input | None = None,
        output: Output | None = None,
        error_output: Output | None = None,
    ) -> IO:
        io = super().create_io(input, output, error_output)

        # Set our own CLI styles
        formatter = io.output.formatter
        formatter.set_style("c1", Style("cyan"))
        formatter.set_style("c2", Style("default", options=["bold"]))
        formatter.set_style("info", Style("blue"))
        formatter.set_style("comment", Style("green"))
        formatter.set_style("warning", Style("yellow"))
        formatter.set_style("debug", Style("default", options=["dark"]))
        formatter.set_style("success", Style("green"))

        # Dark variants
        formatter.set_style("c1_dark", Style("cyan", options=["dark"]))
        formatter.set_style("c2_dark", Style("default", options=["bold", "dark"]))
        formatter.set_style("success_dark", Style("green", options=["dark"]))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        self._io = io

        return io
    
    def register_command_loggers(self, event: Event, event_name: str, _: EventDispatcher) -> None:
      
        from ssprompt.console.logging.filters import SSPROMPT_FILTER
        from ssprompt.console.logging.io_formatter import IOFormatter
        from ssprompt.console.logging.io_handler import IOHandler

        assert isinstance(event, ConsoleCommandEvent)
        command = event.command
        if not isinstance(command, Command):
            return

        io = event.io

        # 必须要打印日志的模块   
        loggers = [
            "ssprompt.packages.locker",
        ]

        loggers += command.loggers

        handler = IOHandler(io)
        handler.setFormatter(IOFormatter())

        level = logging.WARNING

        if io.is_debug():
            level = logging.DEBUG
        elif io.is_very_verbose() or io.is_verbose():
            level = logging.INFO

        logging.basicConfig(level=level, handlers=[handler])

        # only log third-party packages when very verbose
        if not io.is_very_verbose():
            handler.addFilter(SSPROMPT_FILTER)

        for name in loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)
    
def main() -> int:
    exit_code: int = Application().run()
    return exit_code


if __name__ == "__main__":
    main()
