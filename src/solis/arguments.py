# =============================================================================
#                                Solis | Argument class
#
# This file describes the arguments of the solis command line utility.
#
# Author: Meltwin
# Last modified: 29/08/2025
# Version: 0.0.1
# =============================================================================
from solis_lib.arguments import Argument, ArgumentList,TypedArgument

class InitArgs(ArgumentList):
    test = TypedArgument[bool]("-y")


class AppArgs(ArgumentList):
    init = InitArgs()

    test = TypedArgument[str]("-y")
