from __future__ import annotations

import logging
import subprocess
from operator import gt
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

class GitConfig:

    def __init__(self):
        self._config_data = self._get_git_config()

    @property
    def username(self) -> str:
        return self._config_data["user"]["name"]
    
    @property
    def email(self) -> str:
        return  self._config_data["user"]["email"] 
    
    def _git_installed(self):
        try:
            subprocess.call(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except OSError:
            return False
        
    def _get_git_config(self):
        config_data = {}
        if self._git_installed():
            try:
                # Get user.name and user.email
                user_name = self._get_git_config_value("user.name")
                user_email = self._get_git_config_value("user.email")
                config_data["user"] = {"name": user_name, "email": user_email}

                # Get other configuration values
                # Add more keys as needed
                config_data["core"] = {"editor": self._get_git_config_value("core.editor")}

            except Exception as e:
                logger.error("Error fetching Git config, please check Git")
        else:
            logger.warning("Warning: Git not installed!")
            config_data["user"] = {"name": "", "email": ""}

        return config_data

    def _get_git_config_value(self, config_key: str):
        try:
            config_value = subprocess.check_output(["git", "config", "--get", config_key]).decode().strip()
            return config_value
        except subprocess.CalledProcessError:
            return None

    def get_config(self):
        return self._config_data

if __name__ == "__main__":
    git_config = GitConfig()
    config_data = git_config.get_config()
    print("Git Configuration:")
    print(config_data)
    print(git_config.username, git_config.email)
