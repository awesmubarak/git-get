from ._base import Base
from importlib import import_module


class Doctor(Base):
    """Doctor.

    Verifies integrity of files and packages. Any errors are then reported
    and need to be fixed.

    Usage: gitget doctor [global options]

    Examples:
        gitget doctor
    """

    def run(self):
        # Core modules required in this script
        try:
            from loguru import logger
            from yaml import safe_load
            from os import path
        except ModuleNotFoundError as ex:
            logger.error(f"Could not import one or more modules: {ex}")
            exit(1)

        # Modules required elsewhere (provides more details when failing)
        failed_modules = []
        for module in ("docopt", "git", "yaml", "tabulate"):
            try:
                import_module(module)
            except ModuleNotFoundError as ex:
                failed_modules.append(str(ex)[17:-1])
        if failed_modules:
            failed_modules_str = ", ".join(failed_modules)
            logger.error(
                f"Could not import the following modules: {failed_modules_str}"
            )

        # Check if package file exists
        logger.debug("Checking if package file exists")
        package_list_path = self.get_package_list_filepath()  # checks automaticcaly
        logger.info("Package file found")

        # Verify that the file is valid yaml
        logger.debug("Verifying that the package file is valid yaml")
        try:
            with open(package_list_path) as file:
                package_list = safe_load(file)
            logger.info("File is valid yaml")
        except ValueError as e:
            logger.error("Package file is invalid yaml")
            exit(1)

        # Check if all packages exist
        logger.debug("Checking each package")
        package_list = self.get_package_list()
        all_packages_valid = True
        for package_name in package_list:
            package_path = package_list[package_name]
            package_path_exists = path.exists(package_path)
            package_path_is_dir = path.isdir(package_path)
            if not package_path_exists:
                logger.warning(f"The path for the package {package_name} was not found")
                all_packages_valid = False
            elif package_path_exists and not package_path_is_dir:
                logger.warning(f"The path for the package {package_name} is a file")
                all_packages_valid = False
            else:
                logger.debug(f"Package {package_name} found")

        if all_packages_valid:
            logger.info("All packages are valid")
        else:
            logger.info("Not all packages are valid")
