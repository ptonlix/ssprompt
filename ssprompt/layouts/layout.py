from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from packaging.utils import canonicalize_name

from ssprompt.core.config import Config, PyYaml, PromptTypesList, PromptAllTypes

if TYPE_CHECKING:
    from typing import Dict, List

SSPROMPT_DEFAULT = """\
meta:
  author:
  - ptonlix <baird0917@163.com>
  description: ''
  license: MIT
  llm:
  - gpt-3.5-turbo
  name: open
  readme_format: md
  tag:
  - common
  version: 0.1.0
text_prompt:
  dirname: text
json_prompt:
  dirname: json
  list:
  - dependencies:
      langchain: 0.0.266
    name: example
yaml_prompt:
  dirname: yaml
  list:
  - dependencies:
      langchain: 0.0.266
    name: example
python_prompt:
  dirname: python
  list:
  - dependencies:
      langchain: 0.0.266
    name: example

"""

PROMPT_TEMPLATE = """
## Role : [请填写你想定义的角色名称]

## Background : [请描述角色的背景信息，例如其历史、来源或特定的知识背景]

## Preferences : [请描述角色的偏好或特定风格，例如对某种设计或文化的偏好]

## Profile :

- author: Arthur
- Jike ID: Emacser
- version: 0.2
- language: 中文
- description: [请简短描述该角色的主要功能，50 字以内]

## Goals :
[请列出该角色的主要目标 1]
[请列出该角色的主要目标 2]
...

## Constrains :
[请列出该角色在互动中必须遵循的限制条件 1]
[请列出该角色在互动中必须遵循的限制条件 2]
...

## Skills :

[为了在限制条件下实现目标，该角色需要拥有的技能 1]
[为了在限制条件下实现目标，该角色需要拥有的技能 2]
...

## Examples :

[提供一个输出示例 1，展示角色的可能回答或行为]
[提供一个输出示例 2]
...

## OutputFormat :

[请描述该角色的工作流程的第一步]
[请描述该角色的工作流程的第二步]
...

## Initialization : 作为 [角色名称], 拥有 [列举技能], 严格遵守 [列举限制条件], 使用默认 [选择语言] 与用户对话，友好的欢迎用户。然后介绍自己，并提示用户输入.
"""


class Layout:
    default_config: Config = PyYaml().read_config_from_str(SSPROMPT_DEFAULT)

    def __init__(
        self,
        name: str,
        version: str = "0.1.0",
        description: str = "",
        tag: List[str] = [],
        author: List[str] = [],
        llm: List[str] = [],
        readme_format: str = "md",
        license: str | None = "MIT",
        types_list: List = [],
        dependencies: Dict = {},
        text_prompt: Dict[str, str] | None = None,
        yaml_prompt: Dict[str, str | List[Dict]] | None = None,
        json_prompt: Dict[str, str | List[Dict]] | None = None,
        python_prompt: Dict[str, str | List[Dict]] | None = None,
        conf_path: Path | None = None,
    ) -> None:
        self._name = canonicalize_name(name)
        self._version = version
        self._description = description
        self._tag = tag
        self._author = author if author else ["Your Name <you@example.com>"]
        self._llm = llm
        self._readme_format = readme_format.lower()
        self._license = license

        self._text_prompt = text_prompt or {}
        self._yaml_prompt = yaml_prompt or {}
        self._json_prompt = json_prompt or {}
        self._python_prompt = python_prompt or {}

        self._types_list = types_list
        self._dependencies = dependencies

        self._ssprompt_config = self.default_config.copy(deep=True)
        self._create_ssprompt_config(conf_path)

    def _create_readme(self, path: Path) -> Path:
        readme_file = path.joinpath(f"README.{self._readme_format}")
        readme_file.touch()
        return readme_file

    def _create_ssprompt_config(self, path: Path | Any):
        if path and path.exists():
            self._ssprompt_config = PyYaml(path).read_config_from_yaml()
            return

        self._ssprompt_config.meta.name = self._name
        self._ssprompt_config.meta.author = self._author
        self._ssprompt_config.meta.version = self._version
        if not self._description:
            self._ssprompt_config.meta.description = self._description
        self._ssprompt_config.meta.llm = self._llm
        self._ssprompt_config.meta.readme_format = self._readme_format
        self._ssprompt_config.meta.license = self._license
        self._ssprompt_config.meta.tag = self._tag

        self._set_all_dependencies(self._dependencies)
        self._set_all_list_name(self._name)  # Prompt类型中，默认子默认为工程名字
        self._del_prompt_type(self._types_list)

        return self._ssprompt_config

    def _add_prompt_type(self, types_list: list, dependencies: Dict):
        for prompt_type in types_list:
            match prompt_type:
                case "text":
                    if not self._ssprompt_config.text_prompt:
                        self._ssprompt_config.text_prompt = (
                            self.default_config.text_prompt.copy()
                        )
                case "yaml":
                    if not self._ssprompt_config.yaml_prompt:
                        self._ssprompt_config.yaml_prompt = (
                            self.default_config.yaml_prompt.copy()
                        )
                        self._set_list_name(
                            self._ssprompt_config.meta.name,
                            self._ssprompt_config.yaml_prompt,
                        )
                        self._set_dependencies(
                            dependencies, self._ssprompt_config.yaml_prompt
                        )
                case "json":
                    if not self._ssprompt_config.json_prompt:
                        self._ssprompt_config.json_prompt = (
                            self.default_config.json_prompt.copy()
                        )
                        self._set_list_name(
                            self._ssprompt_config.meta.name,
                            self._ssprompt_config.json_prompt,
                        )
                        self._set_dependencies(
                            dependencies, self._ssprompt_config.json_prompt
                        )
                case "python":
                    if not self._ssprompt_config.python_prompt:
                        self._ssprompt_config.python_prompt = (
                            self.default_config.python_prompt.copy()
                        )
                        self._set_list_name(
                            self._ssprompt_config.meta.name,
                            self._ssprompt_config.python_prompt,
                        )
                        self._set_dependencies(
                            dependencies, self._ssprompt_config.python_prompt
                        )
                case _:
                    raise ValueError(
                        "Incorrect Prompt Type.Optional:[text, json, yaml, python]"
                    )

    def _del_prompt_type(self, types_list: list):
        if PromptAllTypes in types_list:
            return
        del_types_list = set(PromptTypesList) - set(types_list)
        for prompt_type in del_types_list:
            match prompt_type:
                case "text":
                    self._ssprompt_config.text_prompt = None
                case "yaml":
                    self._ssprompt_config.yaml_prompt = None
                case "json":
                    self._ssprompt_config.json_prompt = None
                case "python":
                    self._ssprompt_config.python_prompt = None
                case _:
                    raise ValueError(
                        "Incorrect Prompt Type.Optional:[text, json, yaml, python]"
                    )

    def _set_all_list_name(self, name: str):
        self._set_list_name(name, self._ssprompt_config.json_prompt)
        self._set_list_name(name, self._ssprompt_config.yaml_prompt)
        self._set_list_name(name, self._ssprompt_config.python_prompt)

    def _set_list_name(self, name: str, prompt: Dict[Any, Any] | None):
        if prompt:
            if prompt_list := prompt.get("list"):
                for prompt_list_obj in prompt_list:
                    prompt_list_obj["name"] = name

    def _set_all_dependencies(self, depend: Dict):
        self._set_dependencies(depend, self._ssprompt_config.json_prompt)
        self._set_dependencies(depend, self._ssprompt_config.yaml_prompt)
        self._set_dependencies(depend, self._ssprompt_config.python_prompt)

    def _set_dependencies(self, depend: Dict, prompt: Dict[Any, Any] | None):
        if prompt:
            if prompt_list := prompt.get("list"):
                for prompt_list_obj in prompt_list:
                    prompt_list_obj["dependencies"] = depend

    def _create_prompt_dir(self, path: Path, prompt: Dict[Any, Any] | None):
        if prompt:
            prompt_path = Path(str(prompt["dirname"]))
            prompt_path = path.joinpath(prompt_path)
            prompt_path.mkdir(parents=True, exist_ok=True)
            if prompt_list := prompt.get("list"):
                for prompt_list_obj in prompt_list:
                    prompt_list_path = Path(str(prompt_list_obj["name"]))
                    prompt_list_path = prompt_path.joinpath(prompt_list_path)
                    prompt_list_path.mkdir(parents=True, exist_ok=True)

        if self._ssprompt_config.text_prompt is prompt:
            self.create_prompt_template(path, prompt)

    def _create_all_dir(self, path: Path, with_tests: bool):
        self._create_prompt_dir(path, self._ssprompt_config.text_prompt)
        self._create_prompt_dir(path, self._ssprompt_config.yaml_prompt)
        self._create_prompt_dir(path, self._ssprompt_config.json_prompt)
        self._create_prompt_dir(path, self._ssprompt_config.python_prompt)
        if with_tests:
            self._create_tests(path, self._ssprompt_config.python_prompt)

    def create_config_file(self, path: Path):
        path_file = path.joinpath(self._name + ".yaml")
        yaml = PyYaml(path_file)
        yaml.write_config_to_yaml(self._ssprompt_config)

    def create_prompt_template(self, path: Path, prompt: Dict[Any, Any] | None):
        if prompt:
            prompt_path = Path(str(prompt["dirname"]))
            prompt_file_path = path.joinpath(prompt_path).joinpath(
                self._name + ".prompt"
            )

            with open(prompt_file_path, "w+", encoding="utf-8") as f:
                f.write(PROMPT_TEMPLATE)

    def reload_config_file(self, path: Path):
        path_file = path.joinpath(self._ssprompt_config.meta.name + ".yaml")
        yaml = PyYaml(path_file)
        if not yaml.file_exist():
            raise ValueError(
                "The configuration file does not exist and the project has not been established.\n\
Please use the new or init command to initialize the project"
            )
        yaml.reload_config_to_yaml(self._ssprompt_config)

    def create_types_dir(self, path: Path, types_list: list, with_tests: bool = True):
        path.mkdir(parents=True, exist_ok=True)
        for prompt_type in types_list:
            match prompt_type:
                case "all":
                    self._create_all_dir(path, with_tests)
                case "text":
                    self._create_prompt_dir(path, self._ssprompt_config.text_prompt)
                case "yaml":
                    self._create_prompt_dir(path, self._ssprompt_config.yaml_prompt)
                case "json":
                    self._create_prompt_dir(path, self._ssprompt_config.json_prompt)
                case "python":
                    self._create_prompt_dir(path, self._ssprompt_config.python_prompt)
                    if with_tests:
                        self._create_tests(path, self._ssprompt_config.python_prompt)
                case _:
                    raise ValueError(
                        "Incorrect Prompt Type.Optional:[text, json, yaml, python]"
                    )

    def create(self, path: Path, with_tests: bool = True) -> None:
        path.mkdir(parents=True, exist_ok=True)

        self.create_types_dir(path, self._types_list, with_tests)

        self._create_readme(path)

        self.create_config_file(path)

    def add(
        self, path: Path, types_list: list, dependencies: Dict, with_tests: bool = True
    ):
        path.mkdir(parents=True, exist_ok=True)

        self._add_prompt_type(types_list, dependencies)

        self.create_types_dir(path, types_list, with_tests)

        self.reload_config_file(path)

    @staticmethod
    def _create_tests(path: Path, prompt: Dict[Any, Any] | None):
        if not prompt:
            return
        prompt_path = Path(str(prompt["dirname"]))
        prompt_path = path.joinpath(prompt_path)

        tests = prompt_path / "tests"
        tests.mkdir()

        tests_init = tests / "__init__.py"
        tests_init.touch(exist_ok=False)
