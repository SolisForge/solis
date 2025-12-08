# =============================================================================
# Project: SOLIS_APP
#
# Entrypoint of the steps description module
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from .__args__ import BuildingPipelineArguments
from .build import step_build
from .configure import step_configure
from .install import step_install
from .package import step_package
from .pipeline import PipelineStep

__all__ = [
    "BuildingPipelineArguments",
    "PipelineStep",
    "step_build",
    "step_configure",
    "step_install",
    "step_package",
]
