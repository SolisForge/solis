# =============================================================================
#                            Solis | ArgumentList class
#
# This file describes the ArgumentList object that is a container for arguments.
# It aims to provide a way to simply write argument parser and get a
# corresponding configuration class.
#
# Author: Meltwin
# Last modified: 29/08/2025
# Version: 0.0.1
# =============================================================================
from argparse import ArgumentParser
from copy import deepcopy
from typing import dataclass_transform, Optional, Self, Dict, Any

from .Argument import TypedArgument


@dataclass_transform()
class MetaArgumentList(type):
    """
    Metaclass to manage argument list back works as a dataclass.
    It manages:
        - setting the class property _fields
        - setting the class property _arg_default
        - setting the class property _arg_annotations
        - removing all fields from the class to later move them in the instance
    """

    def __new__(cls, name, bases, d):
        """
        Generate an ArgumentList class
        """
        # Shift fields to instances
        x = super().__new__(cls, name, bases, d)
        x._IS_ARGUMENT = True
        x._arg_desc = {k: v for k, v in x.__dict__.items() if hasattr(v, "_IS_ARGUMENT")}
        x._fields = list(x._arg_desc.keys())
        for k in x._fields:
            delattr(x, k)

        # Shift annotation of the fields
        x._arg_annotations = {}
        for field in x._fields:
            if field in x.__annotations__.keys():
                x._arg_annotations[field] = x.__annotations__[field]
        return x

    @property
    def arg_desc(self):
        return self._arg_desc


class ArgumentList(metaclass=MetaArgumentList):
    """
    Wrapper class for arguments.
    It helps generate a configured ArgumentParser with several arguments
    and potentially sub-parsers using a tree-scheme.
    """

    _SUBPARSER_KEY = "_subparser"

    # =========================================================================
    # Initialization & quick utils
    # =========================================================================

    def __init__(self, **kwargs):
        """"""
        # Set up the annotation fields if not present
        self.__annotations__ = self.annotations

        # Initialize fields from the class declaration
        for field in self.class_fields:
            setattr(self, field, deepcopy(self.class_fields[field]))
            if field in kwargs.keys():
                if isinstance(getattr(self, field), TypedArgument):
                    getattr(self, field).set_dest(field)
                    getattr(self, field).set_value(kwargs[field])

                else:
                    setattr(self, field, kwargs[field])

        # Subparsers utils
        self._selected_sub: Optional[str] = None

    def __repr__(self) -> str:
        return f"ArgumentList\n{{\n{'\n'.join([k.__repr__() for k in self.fields.values()])}\n}}"

    @property
    def class_fields(self) -> Dict[str, TypedArgument]:
        """
        Return the fields for this class
        """
        return self.__class__._arg_desc

    @property
    def fields(self) -> Dict[str, TypedArgument]:
        """
        Return the fields of this instance
        """
        return {i: getattr(self, i) for i in self.class_fields.keys()}

    @property
    def annotations(self) -> Dict[str, type]:
        return self.__class__._arg_annotations

    @property
    def subparser(self) -> Optional[str]:
        """
        Return the selected subparser
        """
        return self._selected_sub

    # =========================================================================
    # Parser building
    # =========================================================================

    def generate_parser(self, parser: Optional[ArgumentParser] = None, root: str = "") -> ArgumentParser:
        """
        Generate an ArgumentParser instance using a design.
        It supports fields that extends from TypedArgument as well as
        ArgumentList. These will be considered as subparsers.
        :param root: the root namespace used for uniquely saving the argument
        :param parser: the parser instance to configure
        :return:
        """
        _parser = parser if parser is not None else ArgumentParser()
        _subparser = None

        # Go through all arguments to set up the parser
        for field, desc in self.fields.items():
            # Taking care of traditional arguments
            if isinstance(desc, TypedArgument):
                desc.set_root(root)
                desc.set_dest(field)
                desc.generate_parser(_parser)
            # Taking care of subparser
            elif isinstance(desc, ArgumentList):
                if _subparser is None:
                    _subparser = _parser.add_subparsers(dest=f"{root}/{ArgumentList._SUBPARSER_KEY}", required=True)
                _sub = _subparser.add_parser(field)
                desc.generate_parser(_sub, f"{root}/{field}")
            # Else raise an error as we can't support it
            else:
                raise RuntimeError(f"Unsupported argument type {type(desc)} for {field} during parser generation")
        return _parser

    # =========================================================================
    # Argument back propagation
    # =========================================================================

    def parse_args(self) -> Self:
        """
        Parse the args and populate the variables accordingly.
        :return: this instance
        """
        # Parse the arguments
        _parser = self.generate_parser()
        _args = _parser.parse_args()

        # Split by namespace
        _split_args: Dict[str, Dict[str, Any]] = {}
        for k, v in _args.__dict__.items():
            # If None, then skip
            if v is None:
                continue

            # Split on the last / to divide between namespace and name
            start_var_name = len(k) - k[::-1].find("/") - 1
            root = k[:start_var_name]
            name = k[start_var_name+1:]

            # Save it
            if root not in _split_args.keys():
                _split_args[root] = {}
            _split_args[root][name] = v

        # Now populate the fields
        print(_split_args)
        self._populate_arg(_split_args)
        return self

    def _populate_arg(self, args: Dict[str, Dict[str, Any]], root: str = "") -> None:
        """
        Populate the fields of this list with the given arguments
        :param args: the parsed arguments
        """
        _has_fields = root in args.keys()
        print(f"{root}")

        # Populate if a subparser is selected
        if "_subparser" in args[root]:
            self._selected_sub = args[root][ArgumentList._SUBPARSER_KEY]

        # Populate all fields that comes
        for k, v in self.fields.items():
            if isinstance(v, TypedArgument):
                if _has_fields and k in args[root].keys():
                    v.set_value(args[root][k])
            elif isinstance(v, ArgumentList):
                v._populate_arg(args, f"{root}/{k}")
            else:
                raise RuntimeError(f"Encountered unexpected argument type when populating list: argument {k} with type {type(v)} ")