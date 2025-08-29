# =============================================================================
#                                Solis | Argument class
#
# This file describes the argument object that will be used for argument parser
# automatic building.
#
# Author: Meltwin
# Last modified: 29/08/2025
# Version: 0.0.1
# =============================================================================
from functools import cached_property, singledispatch
from typing import Any, Optional, TypeVar, Generic, Type
from argparse import ArgumentParser

_T = TypeVar('_T')

class TypedArgument(Generic[_T]):
    """
    Object that stores data about a command line argument.
    """

    _IS_ARGUMENT = True

    def __init__(self,
                 name: str,
                 default: Optional[_T] = None,
                 description: Optional[str] = None,
                 ):
        """
        Constructor of the Argument class.
        :param name: the name of the parameter. Could be either the positional
            parameter name (e.g. file) or the option name (e.g. -i, -o, ...)
        :param default: the default value for this argument
        :param description: the description of this argument. It will be used
            in the help menu
        """
        # Base elements of an argument
        self._name = name
        self._default = default
        self._desc = description
        self._dest = self._name
        self._value: Optional[_T] = None
        self._root = ""
        if default is not None:
            self._value = default

        # Define whether it is a positional or option argument
        self._positional = not self._name.startswith("-")

    def __repr__(self):
        return f"Argument[{self.type.__name__}] {self.root}/{self.dest} ({self.value})"

    # =========================================================================
    #                         Fields Getters / Setters
    # =========================================================================

    @cached_property
    def name(self) -> str:
        return self._name

    def set_value(self, v: Any) -> None:
        self._value = v

    @property
    def value(self) -> _T:
        return self._value

    @cached_property
    def type(self) -> Type[_T]:
        self.type = self.__orig_class__.__args__[0]
        return self.type

    @cached_property
    def default(self) -> _T:
        return self._default

    @cached_property
    def desc(self) -> Optional[str]:
        return self._desc

    def set_dest(self, dest:str) -> None:
        self._dest = dest

    @property
    def dest(self) -> str:
        return self._dest

    def set_root(self, root: str) -> None:
        self._root = root

    @property
    def root(self) -> str:
        return self._root

    @cached_property
    def is_positional(self) -> bool:
        return self._positional

    # =========================================================================
    #                         Argument generation
    # =========================================================================

    def generate_parser(self, parser: ArgumentParser) -> None:
        """
        Configure the ArgumentParser with the given argument.
        :param parser: The ArgumentParser instance.
        :return:
        """
        params = {"type": self.type, "default": self.default, "help": self.desc, "dest": f"{self.root}/{self.dest}"}

        # For boolean, special store true
        if self.type is bool:
            params["action"] = "store_true"
            params["default"] = False
            params.pop("type")

        parser.add_argument(
            self.name,
            **params,
        )


# =============================================================================
#                          Quick writing of arguments
# =============================================================================

# noinspection PyPep8Naming
@singledispatch
def Argument(default, name: str, **kwargs) -> TypedArgument[_T]:
    raise RuntimeError(f"Unsupported type {type(default)} for argument {name}")

@Argument.register(int)
def _(default: int, name:str, **kwargs) -> TypedArgument[_T]:
    return TypedArgument[int](name, default=default, **kwargs)

@Argument.register(float)
def _(default: float, name:str, **kwargs) -> TypedArgument[_T]:
    return TypedArgument[float](name, default=default, **kwargs)

@Argument.register(str)
def _(default: str, name:str, **kwargs) -> TypedArgument[_T]:
    return TypedArgument[str](name, default=default, **kwargs)

@Argument.register(bool)
def _(default: bool, name:str, **kwargs) -> TypedArgument[_T]:
    return TypedArgument[bool](name, default=default, **kwargs)