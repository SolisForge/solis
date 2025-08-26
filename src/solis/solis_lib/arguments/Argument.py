# =============================================================================
#                                Solis | Argument class
#
# This file describes the argument object that will be used for argument parser
# automatic building.
#
# Author: Meltwin
# Last modified: 26/08/2025
# Version: 0.0.1
# =============================================================================
from functools import cached_property
from typing import Any, Optional
from argparse import ArgumentParser


class Argument:
    """
    Object that stores data about a command line argument.
    """

    def __init__(self,
                 name: str,
                 t: Optional[type] = None,
                 default: Optional[Any] = None,
                 description: Optional[str] = None,
             ):
        """
        Constructor of the Argument class.
        :param name: the name of the parameter. Could be either the positional
            parameter name (e.g. file) or the option name (e.g. -i, -o, ...)
        :param t: the type of the argument, if none is provided it will use
            the one of the default value, else str
        :param default: the default value for this argument
        :param description: the description of this argument. It will be used
            in the help menu
        """
        self._name = name
        self._default = default
        self._desc = description
        self._type = t
        self._value = None
        if default is not None:
            self._type = type(self._default)
            self._value = default

    def __repr__(self):
        return f"Arg {self.name} ({self.value})"

    # =========================================================================
    #                         Fields Getters / Setters
    # =========================================================================

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

    # =========================================================================
    #                         Argument generation
    # =========================================================================

    def generate_parser(self, parser: ArgumentParser) -> None:
        """
        Configure the ArgumentParser with the given argument.
        :param parser: The ArgumentParser instance.
        :return:
        """
        parser.add_argument(
            self.name,
            dest=self.name,
            type=self.type,
            default=self.default,
            help=self.desc
        )