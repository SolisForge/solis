# =============================================================================
# Project: SOLIS_APP
#
# Pipeline step: BUID (call to the generator to compile targets)
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger


# =============================================================================
def step_build() -> None:
    """
    Execute the building step of the given project
    """
    logger = getLogger("build")

    logger.info("Building project")
