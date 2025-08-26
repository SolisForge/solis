# =============================================================================
#                            Solis | ArgumentList class
#
# This file describes the ArgumentList object that is a container for arguments.
# It aims to provide a way to simply write argument parser and get a
# corresponding configuration class.
#
# Author: Meltwin
# Last modified: 25/08/2025
# Version: 0.0.1
# =============================================================================
from argparse import ArgumentParser
from typing import Optional, Type, dataclass_transform
from copy import deepcopy

from .Argument import Argument


def __def_init__(self, **kwargs):
    """
    Initialization function of the argument list

    :param self: the instance of the argument list
    :param kwargs: the provided arguments for the init
    :return:
    """
    # Set up the annotation fields if not present
    self.__annotations__ = self.__class__._arg_annotations

    # Initialize fields from the class declaration
    for field in self.__class__._fields:
        setattr(self, field, deepcopy(self.__class__._arg_default[field]))
        self.__annotations__[field] = type(getattr(self, field))
        if field in kwargs.keys():
            if isinstance(getattr(self, field), Argument):
                getattr(self, field).set_value(kwargs[field])
            else:
                setattr(self, field, kwargs[field])


def _generate_parser(self, **kwargs) -> ArgumentParser:
    """
    Generate an argument parser for the given argument list.

    :param self: the argument list instance
    :param kwargs: any arguments that could be needed
    :return: an instantiated and configured argument parser
    """
    parser = ArgumentParser()
    print(self.__dict__)

    return parser


def _argument_list_wrapper(cls, **kwargs):
    """
    Wrapper that actually set up the class.
    It modifies the class declarations to shift all declared class arguments
    as instance fields.
    It also set up annotations.

    :param cls: the class to modify
    :param kwargs: the arguments to use for modifying the class
    :return: a modified class
    """
    # Shift fields to instances
    print(cls.__dict__, end="\n\n")
    cls._arg_default = {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
    for k, _ in cls._arg_default.items():
        delattr(cls, k)
    cls._fields = list(cls._arg_default.keys())

    # Set up the initialization function
    cls.__init__ = __def_init__
    cls.generate_parser = _generate_parser

    # Shift annotation of the fields
    cls._arg_annotations = {}
    for field in cls._fields:
        if field in cls.__annotations__.keys():
            cls._arg_annotations[field] = cls.__annotations__[field]

    return cls


@dataclass_transform()
def ArgumentList(cls: Optional[Type] = None, **kwargs):
    """
    Decorator to use when declaring a new argument list.
    It will take care of making it a dataclass and of the initialization
    of the instance.

    :param cls: the class to modify
    :param kwargs: the arguments that could be used for this decorator
    :return: a modified class
    """
    if cls is None:
        return lambda c: _argument_list_wrapper(c, **kwargs)
    return _argument_list_wrapper(cls, **kwargs)
