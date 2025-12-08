# =============================================================================
# Project: SOLIS_APP
#
# Warnings for the solis console app.
#
# Author    Meltwin (github@meltwin.fr)
# Date      05/12/2025 (created 05/12/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from pathlib import Path


# =============================================================================
class BuildDirectoryNotFoundWarning(Warning):
    """
    When build directory does not exist
    """

    def __init__(self, pkg: str, default: str | Path = "build"):
        super().__init__(
            f"No build directory was found for package {pkg}, defaulting to {default}"
        )


# =============================================================================
class InstallDirectoryNotFoundWarning(Warning):
    """
    When install directory does not exist
    """

    def __init__(self, pkg: str, default: str | Path = "build"):
        super().__init__(
            f"No install directory was found for package {pkg}, defaulting to {default}"
        )
