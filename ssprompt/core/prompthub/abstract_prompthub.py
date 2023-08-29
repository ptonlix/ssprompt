from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Mapping, Optional, Sequence, Union
from pathlib import Path
from pydantic import BaseModel, Field, validator

class AbstractPromptHub(BaseModel,ABC):
    main_project: str
    sub_project: str 
    path: Path

    # def __init__(self, project: str, sub_project: str, path:Path) -> None:
    #     self._main_project = project
    #     self._sub_project = sub_project
    #     self._path = path  
    
    @validator('main_project')
    def valid_main_project(cls, values: str) -> str:

        """eg. ptonlix/PromptHub"""
        count = values.count("/") 
        #  小于1, 说明不是一个主仓库
        if  count != 1 :
            raise ValueError("The name isn't PromptHub project, please check")
        return values

    @validator('path')
    def valid_path(cls, value: Path) ->Path:
        if not value.is_dir():
            raise ValueError("The Path isn't directory")
        return value

    # @property
    # def main_project(self) -> str:
    #     return self._main_project
    
    # @property
    # def sub_project(self) -> str:
    #     return self._sub_project

    # @property
    # def path(self) -> Path:
    #     return self._path

    @abstractmethod
    def check_project_exists(self) -> bool:
        ...

    @abstractmethod
    def get_project_meta(self)->Any:
        ...

    @abstractmethod
    def pull_project(self):
        ...
    
    @abstractmethod
    def get_project_dependencies(self, install: Optional[Callable[[Any], Any]]):
        ...

