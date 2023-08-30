from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Dict
from pathlib import Path
from pydantic import BaseModel, Field, validator

class AbstractPromptHub(BaseModel,ABC):

    main_project: str
    sub_project: str 
    path: Path
    
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

    @abstractmethod
    def check_project_exists(self) -> bool:
        ...

    @abstractmethod
    def get_project_meta(self)->Any:
        ...
    
    @abstractmethod
    def get_remote_project_meta(self) -> Any: 
        ...

    @abstractmethod
    def pull_project(self):
        ...
    
    @abstractmethod
    def get_project_dependencies(self)->List[Dict]:
        ...

