# =============================================================================
# Project: SOLIS_APP
#
# Pipeline step: PACKAGE (call to the generator to packages targets)
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger


# =============================================================================
def step_package() -> None:
    """
    Execute the package step of the given project
    """
    logger = getLogger("package")

    logger.info("Packaging project")
