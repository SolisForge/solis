# =============================================================================
# Project: SOLIS_APP
#
# Package informations resolving functions
#
# Author    Meltwin (github@meltwin.fr)
# Date      07/11/2025 (created 07/11/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from logging import getLogger
from os import walk
from pathlib import Path
from re import match
from solis.app.common.index import IndexDatabase, IndexInfos, IndexType, PackageInfo
from solis.utils.types.patterns import LazyInit

LOGGER = LazyInit(lambda: getLogger("PkgResolve"))


# =============================================================================
def resolve_package(name: str) -> PackageInfo:
    """
    Resolve the information of the package with the given name

    Parameters
    ----------
    name: str
        The name of the package to find

    Returns
    -------
    PackageInfo
        The information of the package that we found
    """
    # 1/ Search in the cwd
    pkg = _search_in_dir(Path.cwd(), name)
    if pkg is not None:
        return _make_pkg_info(name, pkg)

    # 2/ Search in direct children directories of cwd
    pkg = _search_in_direct_child_dirs(Path.cwd(), name)
    if pkg is not None:
        return _make_pkg_info(name, pkg)

    # 3/ Look into the index
    pkg = IndexDatabase.find_package(name)
    if pkg is not None:
        return pkg

    # Else, if no other mean could find the function, raise an error
    raise RuntimeError(f"Could not find package {name}")


# =============================================================================
def _make_pkg_info(name: str, infos: IndexInfos) -> PackageInfo:
    """
    Make a complete package info based on the informations found previously.

    This function need the source files location at minimum.
    """
    if IndexType.SOURCE_INFO not in infos.keys():
        raise RuntimeError("A source location is needed to generate the package info !")
    source_dir = Path(infos[IndexType.SOURCE_INFO])

    # Build folder information
    if IndexType.BUILD_INFO not in infos.keys():
        local_build = source_dir.joinpath("build").absolute()
        parent_build = source_dir.parent.joinpath("build").absolute()
        # Test common build location
        if local_build.exists():
            infos[IndexType.BUILD_INFO] = str(local_build)
        elif parent_build.exists():
            infos[IndexType.BUILD_INFO] = str(parent_build)
        # Unknown build location, defaulting to local build
        else:
            LOGGER().warning(
                "No existing build folder found, default to %s",
                local_build,
            )
            infos[IndexType.BUILD_INFO] = str(local_build)

    # Install folder information
    if IndexType.INSTALL_INFO not in infos.keys():
        parent_install = source_dir.parent.joinpath("install").absolute()
        # Test common install location
        if parent_install.exists():
            infos[IndexType.INSTALL_INFO] = str(parent_install)
        # Unknown install location, defaulting to parent location
        else:
            infos[IndexType.INSTALL_INFO] = str(parent_install)

    # Return the constructed PackageInfo object
    return PackageInfo.from_dict(name, infos)


# =============================================================================
def _search_in_dir(directory: Path, name: str) -> IndexInfos | None:
    """
    Search if the package is defined in the given directory.

    Parameters
    ----------
    directory; Path
        The directory to inspect
    name: str
        The package we are looking for

    Returns
    -------
    PackageInfo | None
        Return the package information if the package is found, else None
    """
    # Look for the CMakeLists.txt file
    LOGGER().debug("Searching for package in %s", directory)
    cmakelist = directory.joinpath("CMakeLists.txt")
    if not cmakelist.exists():
        return None

    # Look the package name in the file
    LOGGER().debug("Found CMakeLists.txt at %s", cmakelist)
    with cmakelist.open("r") as f:
        for line in f.readlines():
            project_name = match(r"project\(" + name, line)

            # If the project name was found, returns a proto package configuration
            if project_name is not None:
                return {IndexType.SOURCE_INFO: str(directory.absolute())}
    return None


# =============================================================================
def _search_in_direct_child_dirs(directory: Path, name: str) -> IndexInfos | None:
    """
    Search if the package is defined in any child directory of the given dir.

    Parameters
    ----------
    directory; Path
        The directory to inspect
    name: str
        The package we are looking for

    Returns
    -------
    PackageInfo | None
        Return the package information if the package is found, else None
    """
    directories = next(walk(directory, True))[1]
    for dir in directories:
        pkg = _search_in_dir(directory.joinpath(dir), name)
        if pkg is not None:
            return pkg
    return None
