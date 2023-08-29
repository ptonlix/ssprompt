from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, Dict, Mapping, Union, List

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name
from ssprompt.core.config import Config

from ssprompt.console.commands.command import Command
from ssprompt.repositories import AbstractRepository, PyPiRepository
from ssprompt.core.prompthub import AbstractPromptHub, GitPromptHub

class ShowCommand(Command):

    def __init__(self) -> None:
        super().__init__()

    name = "show"
    description = "Show the prompt engineering project meta infomation"
    
    arguments = [
        argument(
            "path", 
            "The path to show the project at.",
            optional=True,
            default=".")
        ]
    options = [ 
        option(
            "project", 
            "m", 
            "Set the prompt main project name. eg. ptonlix/PromptHub", 
            flag=False,
            default="ptonlix/PromptHub",
        ),
        option(
            "subproject", 
            "s", 
            "Set the prompt sub project name. eg. example", 
            flag=False,
            default = ""
        ),
        option(
            "platfrom",
            "p",
            "Choose Prompt Engineering Warehouse Platform. option: [github gitee]",
            flag=False,
            default="github"
        ), 
    ]
    help = """\
The <c1> show </c1> command show the prompt engineering project meta infomation \
including remote or local.
"""

    loggers = ["ssprompt.core.vcs.git"] 

    def handle(self) -> int:

        return 0