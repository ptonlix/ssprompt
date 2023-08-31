from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Union

from cleo.helpers import argument, option
from packaging.utils import canonicalize_name

from ssprompt.console.commands.command import Command
from ssprompt.repositories import AbstractRepository, PyPiRepository

Requirements = Dict[str, Union[str, Mapping[str, Any]]]

class InitCommand(Command):

    def __init__(self) -> None:
        super().__init__()

        self._repository: AbstractRepository | None = None


    name = "init"
    description = "Creates a basic <comment>prompt_project.yaml</> file in the current directory."

    options = [
        option("name", None, "Set the prompt project name.", flag=False),
        option("description", None, "Description of the prompt project.", flag=False),
        option("author", None, "Author name of the package.", flag=False, multiple=True),
        option("license", None, "Prompt project version number", flag=False),
        
        option(
            "types",
             None, 
            "Specify the Prompt file type, default to all. option: [text,json,yaml,python]",
            flag=False,
            multiple=True,
        ),
        option(
            "llm",
            "l",
            "The applicable large model version of Prompt, example: --llm=gpt-3.5-turbo",
            flag=False,
            multiple=True,
        ),
        option(
            "tag",
            "t",
            "The tags of Prompt, example: --tag=common",
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
        ),
    ]

    help = """\
The <c1>init</c1> command creates a basic <comment>prompt_project.yaml</> file in the\
 current directory.
"""

    loggers = ["ssprompt.core.vcs.git"]
    def handle(self) -> int:
        from pathlib import Path

        from ssprompt.core.config import PyYaml
        from ssprompt.core.vcs.git import GitConfig
        from ssprompt.layouts import layout
        layout_cls = layout("standard")

        project_path = Path.cwd()
        config_file = project_path.name+".yaml"

        yaml = PyYaml(project_path.joinpath(config_file))

        if yaml.file_exist():
            if yaml.is_ssprompt_config():
                self.line_error(
                    f"<error>'A {config_file} file with a prompt section already"
                    " exists.</error>"
                )
                return 1
            else:
                self.line_error(
                    f"<error>'A {config_file} file exist, Please check or delete </error>"
                )
                return 1

        if self.io.is_interactive():
            self.line("")
            self.line(
                "This command will guide you through creating your"
                " <info>pyproject.toml</> config."
            )
            self.line("")

        name = self.option("name")
        if not name:
            name = Path.cwd().name.lower()

            question = self.create_question(
                f"Package name [<comment>{name}</comment>]: ", default=name
            )
            name = self.ask(question)

        description = self.option("description")
        if not description:
            description = self.ask(self.create_question("Description []: ", default=""))
        
        version = "0.1.0"
        question = self.create_question(
            f"Version [<comment>{version}</comment>]: ", default=version
        )
        version = self.ask(question)

        git_config = GitConfig()
        author_list = self.option("author")

        if len(author_list) == 0:
            author = git_config.username
            author_email = git_config.email
            if author and author_email:
                author += f" <{author_email}>"
                author_list = [author]
            else:
                author_list = []

        question = self.create_question(
            f"Author [<comment>{author_list[0]}</comment>, n to skip]: ", default=author_list
        )
        question.set_validator(lambda v: self._validate_author(v))
        author = self.ask(question)
        author_list = [author] if author else author_list
        

        license = self.option("license")
        if not license:
            license = self.ask(self.create_question("License [MIT]: ", default="MIT"))

        if self.io.is_interactive():
            self.line("")
        types_list = self.option("types")
        help_message = """\
Specify the Prompt file type, default to all. option: [all text json yaml python]
- A Prompt project type list (<b>[all] [text python] ...</b>)
"""   
        if not types_list:
            self.line(help_message)
            question = self.create_question("Prompt Project Type []: ", default="all")
            question.set_validator(lambda v: self._validate_list(v))
            types_list = self.ask(question)

        if self.io.is_interactive():
            self.line("")
        llm_list = self.option("llm")
        help_message = """\
The applicable large model version of Prompt
- List of supporting large language models (<b>[gpt-3.5-turbo] [gpt-3.5-turbo chatglm2-6b] ...</b>)
"""   
        if not llm_list:
            self.line(help_message)
            question = self.create_question("Support LLM List []: ", default="gpt-3.5-turbo")
            question.set_validator(lambda v: self._validate_list(v))
            llm_list = self.ask(question)

        if self.io.is_interactive():
            self.line("")
        tag_list = self.option("tag")
        help_message = """\
The tags of Prompt
-List of tags Supported (<b>[common] [common QA] ...</b>)
""" 
        if not tag_list:
            self.line(help_message)
            question = self.create_question("Support Tag List []: ", default="common")
            question.set_validator(lambda v: self._validate_list(v))
            tag_list = self.ask(question)


        if self.io.is_interactive():
            self.line("")

        requirements: Requirements = {}
        question_text = "Would you like to define your main dependencies interactively?"
        help_message = """\
You can specify a package in the following forms:
  - A name and a constraint (<b>langchain@^0.0.266</b>)
"""     
        if self.confirm(question_text, True):
            if self.io.is_interactive():
                self.line(help_message)
                requirements.update(self._determine_requirements(self.option("dependencies"))) 
            if self.io.is_interactive():
                self.line("")


        print(name, version, description, author_list, license, types_list, llm_list, tag_list, requirements)

        layout_ = layout_cls(
            name,
            version,
            author=author_list,
            llm=llm_list,
            tag=tag_list,
            types_list=types_list,
            dependencies=requirements
        )

        layout_.create_config_file(project_path)

        return 0

     

    def _determine_requirements(
        self,
        requires: list[str],
    ) -> Requirements | Any:
        result = {}

        for depend in requires:
            if "@" not in depend:
                raise ValueError('The input format of dependencies is incorrect. eg. -d langchain@^0.0.266')
            depend_sub_list = depend.split("@")
            result[depend_sub_list[0]] = depend_sub_list[1]

        question = self.create_question(
            "Package to add or search for (leave blank to skip):"
        )
        question.set_validator(self._validate_package)

        follow_up_question = self.create_question(
            "\nAdd a package (leave blank to skip):"
        )
        follow_up_question.set_validator(self._validate_package)

        package = self.ask(question)
        while package:
            canonicalized_name = canonicalize_name(package)
            matches = self._get_repository().check_package_exists(canonicalized_name)
            if not matches:
                self.line_error("<error>Unable to find package</error>")
                package = False
            else:
                print(123123)
                question = self.create_question(
                    "Enter the version constraint to require "
                    "(or leave blank to use the latest version):"
                )
                question.set_max_attempts(3)
                question.set_validator(lambda x: (x or "").strip() or None)

                version_constraint = self.ask(question)
                if not version_constraint:
                    version_constraint = "latest" 

                self.line(
                    f"Using version <b>{version_constraint}</b> for"
                    f" <c1>{package}</c1>"
                )

                result[package] = version_constraint

            if self.io.is_interactive():
                package = self.ask(follow_up_question)

        return result

    
    @staticmethod
    def _validate_package(package: str | None) -> str | None:
        if package and len(package.split()) > 2:
            raise ValueError("Invalid package definition.")

        return package

    def _validate_list(self, types: str) -> list[str]:
        return types.split()


    def _validate_author(self, author: str) -> str | None:
        import re

        author_regex = re.compile(r'^[A-Za-z\s]+<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}>$')

        if author in ["n", "no"]:
            return None

        m = author_regex.match(author)
        if not m:
            raise ValueError(
                "Invalid author string. Must be in the format: "
                "John Smith <john@example.com>"
            )

        return author

    def _get_repository(self) -> AbstractRepository:
        
        if self._repository is None:
            self._repository = PyPiRepository()

        return self._repository