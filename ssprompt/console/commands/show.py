from __future__ import annotations

from contextlib import suppress
import platform
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
    
    # arguments = [
    #     argument(
    #         "path", 
    #         "The path to show the project at.",
    #         optional=True,
    #         default=".")
    #     ]
    options = [ 
        option(
            "path",
            "p",
            "The path to show the project at.",
            flag = False
        ),
         option(
            "name",
            None,
            "The prompt project name",
            flag = False
        ),
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
            "platform",
            None,
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

        from pathlib import Path
        from ssprompt.core.config import PyYaml
        path = None
        if self.option("path"):
            path = Path(self.option("path"))
            if not path.is_absolute():
                # we do not use resolve here due to compatibility issues
                # for path.resolve(strict=False)
                path = Path.cwd().joinpath(path)
            if name := self.option("name"):
                path = path.joinpath(name+".yaml")
            else:
                path = path.joinpath(path.name+".yaml")

        if path:
            path_file = path.joinpath(path)
            yaml = PyYaml(path_file)
            if not yaml.file_exist():
                raise ValueError("The configuration file does not exist")
            config = yaml.read_config_from_yaml()
            info = config.json(indent=4)
            self.line("<info>The following is the detailed information of the Prompt project</info>")
            self.line(f"<comment>{info}</comment>")
            return 0
        
        main_pro = self.option("project")
        sub_pro = self.option("subproject")
        repo_type = self.option("platform")

        gitprompthub = GitPromptHub(repo_type, main_pro, sub_pro, self.ssprompt.github_access_key)
        config = self.exec_prompt_hub(gitprompthub)

        if not config:
            self.line("<error>Unable to obtain the Prompt project metadata file. Please check the input parameters</error>")
            return 1

        info = config.json(indent=4)
        self.line("<info>The following is the detailed information of the Prompt project</info>")
        self.line(f"<comment>{info}</comment>")
         
        return 0
        
    def exec_prompt_hub(self, prompthub: AbstractPromptHub):
        self.line("<info>Getting Prompt Project Meta...</info>")   
        return prompthub.get_remote_project_meta() 
    
