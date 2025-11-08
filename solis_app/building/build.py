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
from solis.app.common.errors.scripts import GeneratorNotFoundError
from solis.app.common.index import PackageInfo
from subprocess import run


# =============================================================================
def step_build(package: PackageInfo) -> None:
    """
    Execute the building step of the given project
    """
    logger = getLogger("build")
    try:
        make = get_generator(package)
        logger.info('Building project with generator "%s"', make)
        run([make], check=True, cwd=package.build_path)
    except Exception as e:
        logger.critical("[%s] %s", e.__class__.__name__, str(e.args))


# =============================================================================
def get_generator(package: PackageInfo) -> str:
    """
    Get the generator for the given package (as defined in the CMakeCache.txt
    file as the CMAKE_MAKE_PROGRAM variable)
    """
    # CMakeCache file
    cmake_cache = package.build_path.joinpath("CMakeCache.txt")
    if not cmake_cache.exists():
        raise RuntimeError("CMakeCache.txt file does not exist ")

    # Read the CMAKE_MAKE_PROGRAM variable
    with cmake_cache.open("r") as _cache:
        for line in _cache.readlines():
            # Look for the MAKE_PROGRAM cache value
            if not line.startswith(r"CMAKE_MAKE_PROGRAM"):
                continue

            # Get make program
            return line.split("=")[1].strip()
    raise GeneratorNotFoundError()
