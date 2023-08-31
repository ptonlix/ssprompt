from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Union

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name

from ssprompt.console.commands.command import Command
from ssprompt.core.config import Config
from ssprompt.core.prompthub import AbstractPromptHub, GitPromptHub
from ssprompt.repositories import AbstractRepository, PyPiRepository


class VersionCommand(Command):
    name = "version"
    description = (
        "Shows the version of the prompt project"
    )

    arguments = [
        argument(
            "version",
            "The version number or the rule to update the version.",
            optional=True,
        )
    ]
    options = [
        option("short", "s", "Output the version number only"),
    ]

    help = """\
The version command shows the current version of the project.
"""

    loggers = ["ssprompt.core.vcs.git"] 

    def handle(self) -> int:

        from pathlib import Path

        from ssprompt.core.config import PyYaml

        path = Path.cwd()
        config_file_name = path.name+".yaml" 
        config_file = path.joinpath(config_file_name)

        yaml = PyYaml(config_file)
        if not yaml.file_exist():
            raise ValueError(f"ssprompt could not find a {config_file_name} file in {path}")
        
        config = yaml.read_config_from_yaml()

        if self.option("short"):
            self.line(config.meta.version)
            return 0

        self.line(f"<comment>{config.meta.name}</comment>  <info>{config.meta.version}</info>")

        return 0