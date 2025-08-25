# =============================================================================
#                                Solis | Argument class
#
# This file describes the argument object that will be used for argument parser
# automatic building.
#
# Author: Meltwin
# Last modified: 25/08/2025
# Version: 0.0.1
# =============================================================================
from functools import cached_property
from typing import Any, Optional


class Argument:
    """
    Object that stores data about a command line argument.
    """

    def __init__(self,
                 name: str,
                 t: type = str,
                 default: Optional[Any] = None,
                 description: Optional[str] = None,
                 ):
        self._name = name
        self._default = default
        self._desc = description
        self._type = t
        self._value = None
        if default is not None:
            self._type = type(self._default)
            self._value = default

    def set_value(self, v: Any) -> None:
        self._value = v

    @cached_property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    @cached_property
    def type(self) -> type:
        return self._type

    @cached_property
    def default(self) -> Any:
        return self._default

    @cached_property
    def desc(self) -> Optional[str]:
        return self._desc

    def __repr__(self):
        return f"Arg {self.name} ({self.value})"