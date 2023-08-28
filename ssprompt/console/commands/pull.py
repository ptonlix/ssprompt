from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, Dict, Mapping, Union

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name
from ssprompt.core.config import Config

from ssprompt.console.commands.command import Command
from ssprompt.repositories import AbstractRepository, PyPiRepository

Requirements = Dict[str, Union[str, Mapping[str, Any]]]


class PullCommand(Command):

    def __init__(self) -> None:
        super().__init__()

    name = "pull"
    description = "Pull the prompt engineering project from remote Prompt Hub"
    
    arguments = [
        argument("project", "the prompt engineering project name"),
        argument(
            "path", 
            "The path to create the project at.",
            optional=True,
            default=".")
        ]
    
    help = """\
The <c1> pull</c1> command pull the prompt engineering project from remote Prompt Hub \
in the current directory.
"""
    loggers = ["ssprompt.core.vcs.git"] 

    def handle(self) -> int:
        
        from pathlib import Path

        path = Path(self.argument("path"))
        if not path.is_absolute():
            # we do not use resolve here due to compatibility issues
            # for path.resolve(strict=False)
            path = Path.cwd().joinpath(path)
        
        
        return 0

