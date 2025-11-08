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
from solis.app.common.index import PackageInfo
from subprocess import run
from .build import get_generator


# =============================================================================
def step_install(package: PackageInfo) -> None:
    """
    Execute the install step of the given project
    """
    logger = getLogger("install")

    logger.info("Installing project")
    try:
        make = get_generator(package)
        proc = run(
            [make, "install"],
            check=True,
            cwd=package.build_path,
            capture_output=True,
            encoding="utf-8",
        )
        _make_logger = getLogger(make)
        for line in proc.stdout.split("\n"):
            if line == "":
                continue
            _make_logger.debug(line)
    except Exception as e:
        logger.critical("[%s] %s", e.__class__.__name__, str(e.args))
