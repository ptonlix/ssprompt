from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Mapping, Optional, Sequence, Union
from pathlib import Path

class AbstractPromptHub(ABC):
    def __init__(self, project: str, sub_project: str, path:Path) -> None:
        self._main_project = project
        self._sub_project = sub_project
        self._path = path 

    @property
    def main_project(self) -> str:
        return self._main_project
    
    @property
    def sub_project(self) -> str:
        return self._sub_project

    @property
    def path(self) -> Path:
        return self._path

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
    def check_dependencies(self, install: Optional[Callable[[Any], Any]]):
        ...

