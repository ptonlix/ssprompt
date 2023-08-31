from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Union

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name
from ssprompt.core.config import Config

from ssprompt.console.commands.command import Command
from ssprompt.repositories import AbstractRepository, PyPiRepository

Requirements = Dict[str, Union[str, Mapping[str, Any]]]

class AddCommand(Command):

    def __init__(self) -> None:
        super().__init__()

        self._repository: AbstractRepository | None = None


    name = "add"
    description = "Add some configurations to <comment>prompt_project.yaml</> file in the current directory."

    options = [
        
        option(
            "types",
             "t", 
            "Specify the Prompt file type, default to all. option: [text,json,yaml,python]",
            flag=False,
            multiple=True,
        ),
        option(
            "dependencies",
            "d",
            "Package to require, with an optional version constraint, "
            "e.g. -d langchain@^0.0.266",
            flag=False,
            multiple=True,
            default=['langchain@^0.0.266']
        ),
    ]

    help = """\
The <c1>add</c1> command add some configurations to <comment>prompt_project.yaml</> file \
in the current directory.
"""
    loggers = ["ssprompt.core.vcs.git"]
    def handle(self) -> int:
        from pathlib import Path
        from ssprompt.core.config import PyYaml
        from ssprompt.layouts import layout
 
        layout_cls = layout("standard")

        project_path = Path.cwd()
        config_file = project_path.name+".yaml"
        yamlconf = project_path.joinpath(config_file)

        types_list = self.option("types")
        depend_list = self.option("dependencies")
        depend_obj = {}
        for depend in depend_list:
            if not depend.find("@"):
                raise ValueError('The input format of dependencies is incorrect. eg. -d langchain@^0.0.266')
            depend_sub_list = depend.split("@")
            depend_obj[depend_sub_list[0]] = depend_sub_list[1]

        layout_ = layout_cls(
            name=project_path.name,
            conf_path=yamlconf
        )

        layout_.add(project_path, types_list, depend_obj)

        return 0

   