from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from cleo.commands.command import Command as BaseCommand
from cleo.exceptions import CleoValueError


if TYPE_CHECKING:
    from ssprompt.console.application import Application
    from ssprompt.ssprompt import Ssprompt


class Command(BaseCommand):
    loggers: list[str] = []

    _ssprompt: Ssprompt | None = None

    @property
    def ssprompt(self) -> Ssprompt:
        if self._ssprompt is None:
            return self.get_application().ssprompt

        return self._ssprompt

    def set_ssprompt(self, ssprompt: Ssprompt) -> None:
        self._ssprompt = ssprompt

    def get_application(self) -> Application:
        from ssprompt.console.application import Application

        application = self.application
        assert isinstance(application, Application)
        return application

    def reset_ssprompt(self) -> None:
        self.get_application().reset_ssprompt()

    def option(self, name: str, default: Any = None) -> Any:
        try:
            return super().option(name)
        except CleoValueError:
            return default
