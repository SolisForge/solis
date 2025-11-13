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
from solis.utils.file_system import app_data_dir
from solis.utils.types.patterns import LazyInit


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
