# =============================================================================
# Project: SOLIS_APP
#
# Main function for the building pipeline of the solis tool.
#
# Author    Meltwin (github@meltwin.fr)
# Date      05/11/2025 (created 05/11/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from solis.app.building import (
    BuildingPipelineArguments,
    PipelineStep,
    step_configure,
    step_build,
    step_install,
    step_package,
)
from solis.utils.types.enum import str_to_enum


def main(args: BuildingPipelineArguments):
    wanted_step = str_to_enum(PipelineStep, args.step.value)

    # Execute steps
    if wanted_step >= PipelineStep.CONFIGURE:
        step_configure()
    if wanted_step >= PipelineStep.BUILD:
        step_build()
    if wanted_step >= PipelineStep.INSTALL:
        step_install()
    if wanted_step >= PipelineStep.PACKAGE:
        step_package()
