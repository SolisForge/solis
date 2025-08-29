# =============================================================================
#                         Solis executable main program
#
# This file contains the entry point of the solis_lib command line executable.
#
# Author: Meltwin
# Last modified: 29/08/2025
# Version: 0.0.1
# =============================================================================
from arguments import AppArgs

if __name__ == "__main__":
    t = AppArgs().parse_args()

    print(t)

