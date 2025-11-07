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
from logging import getLogger
from pathlib import Path
from solis.utils.file_system import local_data_dir
from solis.utils.types.patterns import LazyInit


# =============================================================================
class IndexDatabase:
    """
    File-system index to keep track of the solis projects compiled on the
    computer to allow command line calls flexibility.
    """

    # Path for the solis index database
    INDEX_PATH = local_data_dir().joinpath("solis", "refs")
    LOGGER = LazyInit(lambda: getLogger("IndexDB"))

    # -------------------------------------------------------------------------
    # Package registration manipulation
    # -------------------------------------------------------------------------
    @staticmethod
    def get_package() -> str:
        """ """
        return ""

    # -------------------------------------------------------------------------
    @staticmethod
    def register_package(
        pkg_name: str,
        src_path: Path,
        build_path: Path,
        install_path: Path,
    ) -> None:
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
        """
        # Get package index folder
        pkg_index_path = IndexDatabase.INDEX_PATH.joinpath(pkg_name)
        pkg_index_path.mkdir(parents=True, exist_ok=True)
        IndexDatabase.LOGGER().info("Registering package %s", pkg_name)

        # Save the data
        src_file = pkg_index_path.joinpath("source")
        with src_file.open("w+") as f:
            f.writelines([str(src_path.absolute()), ""])
        build_file = pkg_index_path.joinpath("build")
        with build_file.open("w+") as f:
            f.writelines([str(build_path.absolute()), ""])
        install_file = pkg_index_path.joinpath("install")
        with install_file.open("w+") as f:
            f.writelines([str(install_path.absolute()), ""])

    # -------------------------------------------------------------------------
    # Index database manipulation
    # -------------------------------------------------------------------------
    @staticmethod
    def init_index() -> "IndexDatabase":
        """
        Init the index in the user home directory.
        """
        return IndexDatabase()

    # -------------------------------------------------------------------------
    @staticmethod
    def refresh_index() -> None:
        """"""
