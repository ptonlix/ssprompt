from __future__ import annotations


from cleo.helpers import argument, option

from ssprompt.console.commands.command import Command


class NewCommand(Command):
    name = "new"
    description = "Creates a new prompt engineering project at <path>."

    arguments = [
        argument("path", "The path to create the project at."),
        argument(
            "types", 
            "Specify the Prompt file type, default to all. option: [text,json,yaml,python]",
            optional=True,
            default="all")
        ]
    options = [
        option("name", None, "Set the prompt project name.", flag=False),
        option(
            "readme",
            None,
            "Specify the readme file format. One of md (default) or rst",
            flag=False,
        ),
        option(
            "llm",
            "l",
            "The applicable large model version of Prompt, example: --llm=gpt-3.5-turbo",
            flag=False,
            multiple=True,
            default=["gpt-3.5-turbo"]
        ),
        option(
            "tag",
            "t",
            "The tags of Prompt, example: --tag=common",
            flag=False,
            multiple=True,
            default=["common"]
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

    loggers = ["ssprompt.core.vcs.git"]
    def handle(self) -> int:
        from pathlib import Path

        from ssprompt.core.vcs.git import GitConfig
        from ssprompt.layouts import layout
      
        layout_cls = layout("standard")

        path = Path(self.argument("path"))
        types_list = self.argument("types").split(",")

        if not path.is_absolute():
            # we do not use resolve here due to compatibility issues
            # for path.resolve(strict=False)
            path = Path.cwd().joinpath(path)
        name = self.option("name")
        if not name:
            name = path.name

        if path.exists() and list(path.glob("*")):
            # Directory is not empty. Aborting.
            raise RuntimeError(
                f"Destination <fg=yellow>{path}</> exists and is not empty"
            )
        
        readme_format = self.option("readme") or "md"
        
        # 获取Git配置信息
        git_config = GitConfig()
        author_list = []
        author = git_config.username
        author_email = git_config.email
        if author and author_email:
            author += f" <{author_email}>"
            author_list = [author]
        else:
            author_list = []
        # llm
        llm_list = self.option("llm")
        # tag
        tag_list = self.option("tag")

        # dependencies
        depend_list = self.option("dependencies")
        depend_obj = {}
        for depend in depend_list:
            if not depend.find("@"):
                raise ValueError('The input format of dependencies is incorrect. eg. -d langchain@^0.0.266')
            depend_sub_list = depend.split("@")
            depend_obj[depend_sub_list[0]] = depend_sub_list[1]

        layout_ = layout_cls(
            name,
            "0.1.0",
            author=author_list,
            readme_format=readme_format,
            llm=llm_list,
            tag=tag_list,
            types_list=types_list,
            dependencies=depend_obj
        )

        layout_.create(path)


        return 0

