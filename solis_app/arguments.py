# =============================================================================
# Project: SOLIS_APP
#
# Arguments of the command line utility program.
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 20/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from argparse import ArgumentParser
from solis.utils.arguments import ArgumentList, TypedArgument
from solis.app.building import BuildingPipelineArguments


class AppArgs(ArgumentList):
    make = BuildingPipelineArguments()

    log_level = TypedArgument[str](
        "--level",
        "INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"],
    )

    # -------------------------------------------------------------------------
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog="solis")
        return parser

    # -------------------------------------------------------------------------
    def subparser_text(self):
        return "Which command to execute"
