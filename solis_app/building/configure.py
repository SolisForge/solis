# =============================================================================
# Project: SOLIS_APP
#
# Pipeline step: CONFIGURE (call to CMake to define targets)
#
# Author    Meltwin (github@meltwin.fr)
# Date      28/10/2025 (created 28/10/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger
from re import match
from solis.app.common.errors.scripts import CMakeNotFoundError
from subprocess import check_output


# =============================================================================
def get_cmake_executable() -> tuple[str, str]:
    """
    Get the CMake executable to use

    Returns
    -------
    cmake_exe, cmake_version: str, str
        The command line executable to call CMake and its version

    Raises
    ------
    CMakeNotFoundError
        If a cmake executable could not found
    """
    cmake_exe = "cmake"

    # Try to call "cmake --version" to check if present
    stdout = check_output([cmake_exe, "--version"], encoding="utf-8").strip()
    cmake_version = match("^cmake version ([0-9]+\.[0-9]+\.[0-9]+)", stdout)
    if cmake_version is None:
        raise CMakeNotFoundError("could not find CMake as `cmake`")
    return cmake_exe, cmake_version.group(1)


# =============================================================================
def step_configure() -> None:
    """
    Execute the configure step of the given project
    """
    logger = getLogger("configure")

    try:
        cmake_exe, cmake_version = get_cmake_executable()
        logger.info("Using CMake v%s", cmake_version)
    except Exception as e:
        logger.critical("[%s] %s", e.__class__.__name__, str(e.args))
