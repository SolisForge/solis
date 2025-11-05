# =============================================================================
# Project: SOLIS_APP
#
# Arguments definition for the building pipeline of the solis environment.
#
# Author    Meltwin (github@meltwin.fr)
# Date      05/11/2025 (created 05/11/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from solis.utils.arguments import ArgumentList, TypedArgument


# =============================================================================
class BuildingPipelineArguments(ArgumentList):
    """
    Arguments for the building pipeline
    """

    step = TypedArgument[str](
        "step",
        description="Until which step should we go: %(choices)s",
        choices=["configure", "build", "install", "package"],
    )

    package = TypedArgument[str]("package", description="Package to build")
