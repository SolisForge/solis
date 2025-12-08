# =============================================================================
# Project: SOLIS_APP
#
# Description of the building pipeline in the solis development environment.
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from enum import auto, IntEnum


# =============================================================================
class PipelineStep(IntEnum):
    """
    Enumeration of the pipeline steps for the solis environment.
    """

    NONE = 0
    CONFIGURE = auto()
    BUILD = auto()
    INSTALL = auto()
    PACKAGE = auto()
