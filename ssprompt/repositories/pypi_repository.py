from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from importlib import metadata
from typing import TYPE_CHECKING
import logging
import requests
from packaging import version as packaging_version

from ssprompt.repositories.abstract_repository import AbstractRepository

if TYPE_CHECKING:
    from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class PyPiRepository(AbstractRepository):
    def __init__(self, 
        url="https://pypi.org/pypi/", 
        index="https://pypi.tuna.tsinghua.edu.cn/simple"
    ):
        self._base_url = url
        self._index = index
    def check_package_exists(self,name: str, version:str|None=None) -> bool:
        package =  name + "/json"
        if version:
            package = name + "/" + version + "/json"

        response = requests.get(self._base_url + name + "/json")
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
            logger.debug(e)

    def is_package_installed(self, package_name: str, required_version=None):
        try:
            installed_version = metadata.version(package_name)
            if required_version:
                required_version = packaging_version.parse(required_version)
                installed_version = packaging_version.parse(installed_version)
                return installed_version >= required_version
            return True
        except metadata.PackageNotFoundError:
            return False

    def get_related_packages(self, package_name):
        from bs4 import BeautifulSoup
        response = requests.get(self._index +"/"+ package_name + "/")
        if response.status_code == 200:
            packages = []
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            for link in links:
                package_info = link.get("href")
                if package_info.endswith("/"):
                    package_name, package_version = package_info.rstrip("/").rsplit("-", 1)
                    packages.append((package_name, package_version))
            return packages
        else:
            return []

if __name__  == "__main__":

    repo = PyPiRepository()

    package_name = "requests"
    version = "2.26.0"
    print(repo.check_package_exists(package_name, version))

    if repo.is_package_installed(package_name):
        print(f"包 '{package_name}' 已在本地安装")
    else:
        print(f"包 '{package_name}' 未在本地安装")
    
    related_packages = repo.get_related_packages("requests")
    if related_packages:
        print(f"与 'requests' 相关的包列表:")
        for package in related_packages:
            print(package)
    else:
        print("未找到与 'requests' 相关的包列表")