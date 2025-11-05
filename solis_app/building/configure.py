# =============================================================================
# Project: SOLIS_APP
#
# Pipeline step: CONFIGURE (call to CMake to define targets)
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger


# =============================================================================
def step_configure() -> None:
    """
    Execute the configure step of the given project
    """
    logger = getLogger("configure")

    logger.info("Configuring project")
