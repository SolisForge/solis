# =============================================================================
#                                Solis | Argument class
#
# This file describes the arguments of the solis command line utility.
#
# Author: Meltwin
# Last modified: 25/08/2025
# Version: 0.0.1
# =============================================================================
from solis_lib.arguments import Argument, ArgumentList

@ArgumentList
class AppArgs:
    test = Argument("-t",default=0.0)
    test2 = Argument("-y",default="hello")
    alpha = Argument("-y",default="hello")

