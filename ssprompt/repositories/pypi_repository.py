from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from importlib import metadata
from typing import TYPE_CHECKING
import logging
import requests
import re

from ssprompt.repositories.abstract_repository import AbstractRepository

if TYPE_CHECKING:
    from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class PyPiRepository(AbstractRepository):
    def __init__(self, 
        url="https://pypi.org/pypi", 
        index="https://pypi.tuna.tsinghua.edu.cn/simple"
    ):
        self._base_url = url
        self._index = index
    def check_package_exists(self,name: str, version:str|None=None) -> bool:
        package =  name + "/json"
        if version:
            package = name + "/" + version + "/json"

        response = requests.get(self._base_url + "/"+ name + "/json")
        if response.status_code == 404:
            return False
        return True

    def install_package(self, name: str, version:str|None=None):
        if version:
            package_identifier = f"{name}=={version}"
        else:
            package_identifier = name

        try:
            subprocess.check_output(["pip", "install", package_identifier, "-i", self._index], stderr=subprocess.STDOUT)
            logger.info(f"Successfully installed package '{package_identifier}'")
        except subprocess.CalledProcessError as e:
            logger.error("Unable to install package.")
            logger.error(e)

    def is_package_installed(self, package_name: str, required_version=None):
        try:
            installed_version = metadata.version(package_name)
            if required_version: 
                return self.check_version_constraint(installed_version, required_version)
            return True
        except metadata.PackageNotFoundError:
            return False


    def check_version_constraint(self, version, constraint):
        if constraint.startswith("^"):
            return self._check_caret_requirement(version, constraint)
        elif constraint.startswith("~"):
            return self._check_tilde_requirement(version, constraint)
        else:
            return self._check_wildcard_requirement(version, constraint)
        

    def _check_caret_requirement(self, version, constraint):
        constraint_version = constraint[1:]
        version_parts = version.split(".")
        constraint_parts = constraint_version.split(".")

        if len(version_parts) != len(constraint_parts):
            return False

        for v, c in zip(version_parts, constraint_parts):
            if v < c:
                return False
            if v > c:
                return True

        return True

    def _check_tilde_requirement(self, version, constraint):
        constraint_version = constraint[1:]
        version_parts = version.split(".")
        constraint_parts = constraint_version.split(".")

        if len(version_parts) != len(constraint_parts):
            return False

        for v, c in zip(version_parts, constraint_parts):
            if v < c:
                return False
            if v > c:
                return True

        return version_parts[-1] >= constraint_parts[-1]

    def _check_wildcard_requirement(self, version, constraint):
        pattern = constraint.replace("*", r"\d+")
        return re.fullmatch(pattern, version) is not None
    
    def get_available_versions(self, package_name):
        url = self._base_url+f"/{package_name}/json"
        response = requests.get(url)
 
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("info", {}).get("version", "")
            releases = data.get("releases", {})
            return latest_version, list(releases.keys())
        else:
            return "", []

    def find_compatible_version(self, package_name, desired_version):
        latest_version, available_versions = self.get_available_versions(package_name)
        if desired_version == "latest":
            return latest_version
        for version in available_versions:
            if self.check_version_constraint(version, desired_version):
                return version
        
        return None
        
if __name__  == "__main__":

    repo = PyPiRepository()

    package_name = "langchain"
    version = "^0.0.99rc"
    find_verison = repo.find_compatible_version(package_name, version)
    print(find_verison)
    # print(repo.check_package_exists(package_name, version))

    # if repo.is_package_installed(package_name):
    #     print(f"包 '{package_name}' 已在本地安装")
    # else:
    #     print(f"包 '{package_name}' 未在本地安装")
    
    # related_packages = repo.get_related_packages("requests")
    # if related_packages:
    #     print(f"与 'requests' 相关的包列表:")
    #     for package in related_packages:
    #         print(package)
    # else:
    #     print("未找到与 'requests' 相关的包列表")