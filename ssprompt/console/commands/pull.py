from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Union, List

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name
from ssprompt.core.config import Config

from ssprompt.console.commands.command import Command
from ssprompt.repositories import AbstractRepository, PyPiRepository
from ssprompt.core.prompthub import AbstractPromptHub, GitPromptHub


class PullCommand(Command):

    def __init__(self) -> None:
        super().__init__()

    name = "pull"
    description = "Pull the prompt engineering project from remote Prompt Hub"
    
    arguments = [
        argument(
            "path", 
            "The path to create the project at.",
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
            "platform",
            None,
            "Choose Prompt Engineering Warehouse Platform. option: [github gitee]",
            flag=False,
            default="github"
        ), 
        option(
            "dirflag",
            None,
            "Switch[on or off]: Create a new project directory and download Prompt project",
            flag=False,
            default="on"
        )
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
        
        main_pro = self.option("project")
        sub_pro = self.option("subproject")
        repo_type = self.option("platform")
        dirswitch = self.option("dirflag")

        dirflag = False if dirswitch == "off" else True
        
        gitprompthub = GitPromptHub(repo_type, main_pro, sub_pro, 
                                    self.ssprompt.github_access_key, path, dirflag)

        depend_list = self.exec_prompt_hub(gitprompthub)

        no_install_depend_list=self.check_no_install_package(depend_list)
        
        if no_install_depend_list:
            self.line(f"<info>{depend_list} are the dependencies of the Project Prompt </info>")
            self.line(f"<info><error>{no_install_depend_list}</error> packages were not downloaded locally</info>")

            question_text = "Would you like to download these dependencies?"
            help_message = """\
    Download these dependency packages locally through pip)
    """     
            if self.confirm(question_text, True):
                if self.io.is_interactive():
                    self.line(help_message)
                    self.install_package(no_install_depend_list) 
                if self.io.is_interactive():
                    self.line("")

        self.add_style('fire', fg='red', bg='blue', options=['bold', 'blink'])
        self.line(f"<info> The <fire>{main_pro} {sub_pro} </fire> Prompt Project pull completed, enjoy AI!</info>") 

        
        return 0


    def exec_prompt_hub(self, prompthub: AbstractPromptHub)->List[Dict]:
        
        prompthub.pull_project()

        return prompthub.get_project_dependencies() 
        
    def check_no_install_package(self, depend_list: List[Dict]) ->List[Dict]:
        repo = PyPiRepository()
        no_install_depend_list=[]
        for depend in depend_list:
            for package_name, version  in depend.items():
                if not repo.is_package_installed(str(package_name),version):
                    no_install_depend_list.append(depend)
        return no_install_depend_list
        

    def install_package(self, depend_list: List[Dict]):
        repo = PyPiRepository()
        for depend in depend_list:
            for package_name, version  in depend.items():
                install_verison =  repo.find_compatible_version(package_name, version)
                repo.install_package(package_name, install_verison)