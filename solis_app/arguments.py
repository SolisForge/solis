# =============================================================================
#                                Solis | Argument class
#
# This file describes the arguments of the solis command line utility.
#
# Author: Meltwin
# Last modified: 29/08/2025
# Version: 0.0.1
# =============================================================================
from solis.utils.arguments import Argument, ArgumentList, TypedArgument


class InitArgs(ArgumentList):
    test = TypedArgument[bool]("-y")


class AppArgs(ArgumentList):
    test = TypedArgument[str]("-y")
    init = InitArgs()
