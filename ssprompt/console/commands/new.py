from __future__ import annotations

from contextlib import suppress

from cleo.helpers import argument
from cleo.helpers import option

from ssprompt.console.commands.command import Command


class NewCommand(Command):
    name = "new"
    description = "Creates a new Prompt project at <path>."

    arguments = [argument("path", "The path to create the project at.")]
    options = [
        option("name", None, "Set the resulting project name.", flag=False),
        option(
            "readme",
            None,
            "Specify the readme file format. One of md (default) or rst",
            flag=False,
        ),
    ]

    loggers = ["ssprompt.core.vcs.git"]
    def handle(self) -> int:
        from pathlib import Path
        from ssprompt.layouts import layout
        from ssprompt.core.vcs.git import GitConfig
      
        layout_cls = layout("standard")

        path = Path(self.argument("path"))
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

        author = git_config.username
        author_email = git_config.email

        author += f" <{author_email}>"

        print(author)



        return 0

