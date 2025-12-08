# =============================================================================
# Project: SOLIS_APP
#
# Entrypoint of the command line executable
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 20/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from .arguments import AppArgs
from .building.main import main as build_main
from logging import config, getLogger
from solis.resources import LOGGER_CONF
from solis.utils.logging import LogLevel

if __name__ == "__main__":
    config.fileConfig(LOGGER_CONF)
    args = AppArgs().parse_args()

    # Set log level
    logger = getLogger()
    logger.setLevel(LogLevel.from_string(args.log_level.value))

    match args.subparser:
        case "make":
            build_main(args.make, args.log_level.value == "DEBUG")
        case _:
            logger.error("How did you get here ?")
