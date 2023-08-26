from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def check_package_exists(self, name: str, version:str|None=None) -> bool:
        ...

    @abstractmethod
    def install_package(self, name: str, version:str|None=None):
        ...
