# =============================================================================
# Project: SOLIS_APP
#
# Common error for scripts usages.
#
# Author    Meltwin (github@meltwin.fr)
# Date      06/11/2025 (created 06/11/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================


# =============================================================================
class CMakeNotFoundError(Exception):
    """
    Could not find the CMake executable
    """
