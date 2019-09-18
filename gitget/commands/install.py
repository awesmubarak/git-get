from .base import Base
from loguru import logger
from os import getcwd, path

from git import Repo


class Install(Base):
    """Downloads a repository from github and saves information about it."""

    def run(self):
        package_list = self.get_package_list()
        package_url = self.options["<package_url>"]
        directory_name = ""

        # sort out package name
        if self.options["<package_name>"] is not None:
            logger.debug("Using the name provided as argument")
            package_name = self.options["<package_name>"]
            directory_name = package_name
        else:
            logger.debug("Using the URL to generate a name")
            package_name = "/".join(package_url.split("/")[-2:])

        # check if the package is in the package list already
        if package_name in package_list:
            logger.error(f"Package name {package_name} already exists")
            exit(1)
        logger.info(f"Using package name {package_name}")

        # figure out the package location
        if directory_name == "":
            package_location = f"{getcwd()}/{package_url.split('/')[-1]}"
        else:
            package_location = f"{getcwd()}/{directory_name}"

        # check if directory already exists
        if path.isdir(package_location):
            logger.error(f"Directory already exists: {package_location}")
            exit(1)

        # clone repository
        logger.info(f"Cloning repository {package_name}")
        Repo.clone_from(package_url, package_location)
        logger.debug("Clone successfull")

        # add package to package list
        package_list[package_name] = package_location
        self.write_package_list(package_list)
        logger.info("Saved package information")
