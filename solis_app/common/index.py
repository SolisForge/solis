# =============================================================================
# Project: SOLIS_APP
#
# Project index for the solis environment.
# This helps resolving the packages paths.
#
# Author    Meltwin (github@meltwin.fr)
# Date      06/11/2025 (created 06/11/2025)
# Version   1.0.0
# Copyright Solis Forge | 2025
#           Distributed under MIT License (https://opensource.org/licenses/MIT)
# =============================================================================
from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from pathlib import Path
from re import match
from solis.app.common.warnings import (
    BuildDirectoryNotFoundWarning,
    InstallDirectoryNotFoundWarning,
)
from solis.utils.file_system import app_data_dir
from solis.utils.types.patterns import LazyInit
from warnings import warn


INDEX_PATH = app_data_dir().joinpath("solis", "index")


# =============================================================================
class IndexType(Enum):
    SOURCE_INFO = "source"
    BUILD_INFO = "build"
    INSTALL_INFO = "install"


IndexInfos = dict[IndexType, str]


# =============================================================================
@dataclass
class PackageInfo:
    """
    Structure to store information about a package
    """

    name: str
    src_path: Path
    build_path: Path
    install_path: Path

    # -------------------------------------------------------------------------
    def get(self, index: IndexType):
        match index:
            case IndexType.SOURCE_INFO:
                return self.src_path.absolute()
            case IndexType.BUILD_INFO:
                return self.build_path.absolute()
            case IndexType.INSTALL_INFO:
                return self.install_path.absolute()

    # -------------------------------------------------------------------------
    @staticmethod
    def from_dict(name: str, d: IndexInfos) -> "PackageInfo":
        """
        Initialize a PackageInfo object from a dictionary
        """
        return PackageInfo(
            name,
            Path(d[IndexType.SOURCE_INFO]),
            Path(d[IndexType.BUILD_INFO]),
            Path(d[IndexType.INSTALL_INFO]),
        )


# =============================================================================
class PackageNotFoundError(Exception):
    """
    When a package could not be found
    """

    def __init__(self, pkg: str) -> None:
        super().__init__(f"Package {pkg} cannot be found")


# =============================================================================
class IndexDatabase:
    """
    File-system index to keep track of the solis projects compiled on the
    computer to allow command line calls flexibility.
    """

    # Path for the solis index database
    LOGGER = LazyInit(lambda: getLogger("IndexDB"))

    # -------------------------------------------------------------------------
    # Package registration
    # -------------------------------------------------------------------------
    @staticmethod
    def find_package(name: str) -> PackageInfo | None:
        """
        Find the package informations from the index

        Parameters
        ----------
        name: str
            The name of the package to find

        Returns
        -------
        PackageInfo
            An instance of a package info created from the information in the
        """
        pkg_index_dir = IndexDatabase._get_package_index_folder(name)

        # Check if project is registered
        if not pkg_index_dir.exists():
            return None

        # Load the project
        project_info: dict[IndexType, str] = {}
        for index in IndexType.__members__.values():
            index_file = IndexDatabase._get_package_index_file(name, index)

            # Check if file exists
            if not index_file.exists():
                return None

            # Read file
            with index_file.open("r") as f:
                project_info[index] = f.readline()

        return PackageInfo.from_dict(name, project_info)

    # -------------------------------------------------------------------------
    @staticmethod
    def register_package(pkg: PackageInfo) -> None:
        """
            Register a package in the solis index

            Parameters
            ----------
            src_path: Path
                Path to the package's sources
            build_path: Path
                Path to the package's build folder
            install_path: Path
                Path to the package's install folder

        # -------------------------------------------------------------------------
        # Indexes architectures
        # -------------------------------------------------------------------------
        @staticmethod
        def _get_p
        """
        # Get package index folder
        IndexDatabase.LOGGER().info("Registering package %s", pkg.name)
        pkg_index_dir = IndexDatabase._get_package_index_folder(pkg.name)
        pkg_index_dir.mkdir(parents=True, exist_ok=True)

        # Save the data
        for index in IndexType.__members__.values():
            with IndexDatabase._get_package_index_file(
                pkg.name,
                index,
            ).open("w+") as file:
                file.writelines([str(pkg.get(index)), ""])

    # -------------------------------------------------------------------------
    # Indexes architectures
    # -------------------------------------------------------------------------
    @staticmethod
    def _get_package_index_folder(pkg_name: str) -> Path:
        """
        Return the index path for the given package
        """
        return INDEX_PATH.joinpath(pkg_name)

    # -------------------------------------------------------------------------
    @classmethod
    def _get_package_index_file(cls, pkg_name: str, index_type: IndexType) -> Path:
        return cls._get_package_index_folder(pkg_name).joinpath(index_type.value)


# =============================================================================
class SolisPackage:
    """
    Package manipulator class
    """

    LOGGER = LazyInit(lambda: getLogger("SolisPackage"))

    # -------------------------------------------------------------------------
    # Resolving packages
    # -------------------------------------------------------------------------
    @classmethod
    def resolve(cls, name: str) -> PackageInfo:
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
        pkg = cls._resolve_search_in_dir(Path.cwd(), name)
        if pkg is not None:
            return cls._resolve_mk_pkg_info(name, pkg)

        # 2/ Search in direct children directories of cwd
        pkg = cls._resolve_search_in_direct_childs(Path.cwd(), name)
        if pkg is not None:
            return cls._resolve_mk_pkg_info(name, pkg)

        # 3/ Look into the index
        pkg = IndexDatabase.find_package(name)
        if pkg is not None:
            return pkg

        # Else, if no other mean could find the function, raise an error
        raise PackageNotFoundError(name)

    # -------------------------------------------------------------------------
    @staticmethod
    def _resolve_mk_pkg_info(name: str, infos: IndexInfos) -> PackageInfo:
        """
        Make a complete package info based on the informations found previously.

        This function need the source files location at minimum.
        """
        if IndexType.SOURCE_INFO not in infos.keys():
            raise RuntimeError(
                "A source location is needed to generate the package info !"
            )
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
                warn(BuildDirectoryNotFoundWarning(name, str(local_build)))
                infos[IndexType.BUILD_INFO] = str(local_build)

        # Install folder information
        if IndexType.INSTALL_INFO not in infos.keys():
            parent_install = source_dir.parent.joinpath("install").absolute()
            # Test common install location
            if parent_install.exists():
                infos[IndexType.INSTALL_INFO] = str(parent_install)
            # Unknown install location, defaulting to parent location
            else:
                warn(InstallDirectoryNotFoundWarning(name, str(parent_install)))
                infos[IndexType.INSTALL_INFO] = str(parent_install)

        # Return the constructed PackageInfo object
        return PackageInfo.from_dict(name, infos)

    # -------------------------------------------------------------------------
    @classmethod
    def _resolve_search_in_dir(cls, directory: Path, name: str) -> IndexInfos | None:
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
        cls.LOGGER().debug("Searching for package in %s", directory)
        if not (cmakelist := directory.joinpath("CMakeLists.txt")).exists():
            return None

        # Look the package name in the file
        cls.LOGGER().debug("Found CMakeLists.txt at %s", cmakelist)
        with cmakelist.open("r") as f:
            for line in f.readlines():
                project_name = match(rf"project\({name}[ \)]", line)

                # If the project name was found, returns a proto package configuration
                if project_name is not None:
                    return {IndexType.SOURCE_INFO: str(directory.absolute())}
        return None

    # -------------------------------------------------------------------------
    @classmethod
    def _resolve_search_in_direct_childs(
        cls, directory: Path, name: str
    ) -> IndexInfos | None:
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
        for dir in directory.iterdir():
            if (
                pkg := cls._resolve_search_in_dir(
                    directory.joinpath(dir),
                    name,
                )
            ) is not None:
                return pkg
        return None
