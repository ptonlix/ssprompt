from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Dict
from pathlib import Path
from pydantic import BaseModel, validator
from ssprompt.core.config import PromptTypesList


class AbstractPromptHub(BaseModel, ABC):
    main_project: str
    sub_project: str
    types: str | None = ""
    typedir: str | None = ""
    path: Path

    @validator("main_project")
    def valid_main_project(cls, values: str) -> str:
        """eg. ptonlix/PromptHub"""
        count = values.count("/")
        #  小于1, 说明不是一个主仓库
        if count != 1:
            raise ValueError("The name isn't PromptHub project, please check")
        return values

    @validator("types")
    def valid_types(cls, value: str) -> str:
        if value and value not in PromptTypesList:
            raise ValueError(
                "types must be the value in the list:[text,json,yaml,python]"
            )
        return value

    @validator("path")
    def valid_path(cls, value: Path) -> Path:
        if not value.is_dir():
            raise ValueError("The Path isn't directory")
        return value

    @abstractmethod
    def check_project_exists(self) -> bool:
        ...

    @abstractmethod
    def get_project_meta(self) -> Any:
        ...

    @abstractmethod
    def get_remote_project_meta(self) -> Any:
        ...

    @abstractmethod
    def pull_project(self):
        ...

    @abstractmethod
    def get_project_dependencies(self) -> List[Dict]:
        ...
