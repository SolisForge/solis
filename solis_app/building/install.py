# =============================================================================
# Project: SOLIS_APP
#
# Pipeline step: INSTALL (call to the generator to install targets)
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger


# =============================================================================
def step_install() -> None:
    """
    Execute the install step of the given project
    """
    logger = getLogger("install")

    logger.info("Installing project")
