from abc import ABC, abstractmethod
import platform
from time import sleep
from typing import Any, Callable, List, Mapping, Optional, Sequence, Union, Dict
from pathlib import Path

from numpy import savez_compressed
from ssprompt.core.prompthub.abstract_prompthub import AbstractPromptHub
from ssprompt.core.config import PyYaml, Config
import requests
from urllib.parse import urlparse
from pydantic import BaseModel, Field, validator, PrivateAttr
import os
import logging
import time
from tqdm import tqdm

logger = logging.getLogger(__name__)

class GitModel(BaseModel):
    #git_type: str 
    main_project: str
    sub_project: str 
    path: Path
    platform:  Dict[str,Dict[Any, Any]] = {
        "github":{
            "repos": "https://api.github.com/repos/{repo_url}",
            "content": "https://api.github.com/repos/{repo_url}/contents/{file_path}"
        },
        "gitee":{}
    }

    @validator('main_project')
    def valid_main_project(cls, values: str) -> str:

        """eg. ptonlix/PromptHub"""
        count = values.count("/") 
        #  小于1, 说明不是一个主仓库
        if  count != 1 :
            raise ValueError("The name isn't PromptHub project, please check")
        return values

    @validator('path')
    def valid_path(cls, value: Path) ->Path:
        if not value.is_dir():
            raise ValueError("The Path isn't directory")
        return value


class GitPromptHub(AbstractPromptHub):

    _platfrom: Dict =  PrivateAttr()
    _session: Any = PrivateAttr()
    _dir_flag: bool = PrivateAttr()

    platform:  Dict[str,Dict[Any, Any]] = {
        "github":{
            "repos": "https://api.github.com/repos/{repo_url}",
            "content": "https://api.github.com/repos/{repo_url}/contents/{file_path}"
        },
        "gitee":{}
    }

    def __init__(self, git_type:str, main_project:str, sub_project:str, path:Path, dir_flag:bool = True) -> None:
        super().__init__(main_project=main_project, sub_project=sub_project, path=path)
        if not git_type in self.platform.keys():
             raise ValueError("The Git Type is incorrect, [github or gitee]")  
        self._platfrom = self.platform.get(git_type, {})
        self._session = requests.Session()
        self._dir_flag = dir_flag

    @property
    def _save_path(self)->Path:
        save_path = None
        if self._dir_flag:
            if not self.sub_project:
                dir_name = self.main_project.split("/")[1]
            else:
                dir_name = self.sub_project.split("/")[-1] 
            save_path = self.path.joinpath(dir_name)
        else:
            save_path = self.path
        return save_path 

    def check_project_exists(self) -> bool:
        repo_url = self.main_project
        github_api_url = self._platfrom.get("repos", "")

        response = requests.get(github_api_url.format(repo_url=repo_url))
        return response.status_code == 200
    
    def get_project_meta(self)->Config:
        meta_file = ""
        if not self.sub_project:
            meta_file = self.main_project.split("/")[1] + ".yaml"
        else:
            meta_file = self.sub_project.split("/")[-1] + ".yaml"
        meta_file = self._save_path.joinpath(meta_file)
        return PyYaml(meta_file).read_config_from_yaml()
    
    def pull_project(self): 
        if not os.path.exists(self._save_path):
            os.makedirs(self._save_path)
        self._download_github_directory(self.sub_project, self._save_path)
    
    def get_project_dependencies(self) ->List[Dict]:
        depend_list = []
        meta_obj = self.get_project_meta()
        if meta_obj.json_prompt:
            for sub_prompt in meta_obj.json_prompt["list"]:
                depend_list.append(sub_prompt.get("dependencies"))
        if meta_obj.yaml_prompt:
            for sub_prompt in meta_obj. yaml_prompt["list"]:
                depend_list.append(sub_prompt.get("dependencies")) 
        if meta_obj.python_prompt:
            for sub_prompt in meta_obj. python_prompt["list"]:
                depend_list.append(sub_prompt.get("dependencies")) 
        return self._set_dependencies_list(depend_list)

    """
        列表内去重字典
    """                   
    def _set_dependencies_list(self, depend:List[Dict]) -> List[Dict]:
        import json
        unique_data = []
        seen_values = set()

        for item in depend:
            item_str = json.dumps(item, sort_keys=True)
            if item_str not in seen_values:
                unique_data.append(item)
                seen_values.add(item_str) 
        return unique_data

                    
    def _parse_github_response(self, response):
        return response.json()

    def _download_github_directory(self, directory_path: str , save_directory: Path):

        github_api_url = self._platfrom.get("content", "").format(repo_url=self.main_project, file_path=directory_path)
        response = self._session.get(github_api_url)

        if response.status_code == 200:
            content_list = self._parse_github_response(response)
            for item in tqdm(content_list, desc=f"Downloading {directory_path}", unit="file"):
                item_name = item['name']
                item_download_url = item['download_url']
                item_sha = item['sha']
                item_save_path = os.path.join(save_directory, item_name)

                if item['type'] == 'dir':
                    # Recursively download subdirectories
                    subdirectory_path = os.path.join(directory_path, item_name)
                    subdirectory_save_path = save_directory.joinpath(item_name)
                    if not os.path.exists(subdirectory_save_path):
                        os.makedirs(subdirectory_save_path)
                    self._download_github_directory(subdirectory_path, subdirectory_save_path)
                else:
                    self._download_file(item_download_url, item_save_path, item_sha)
        else:
            logger.error(f"Failed to fetch directory content, Status code: {response.status_code}")
            logger.error(f"{response.text}") 

    def _download_file(self, url, save_path, sha, max_retries:int=3, retry_delay: int=200):
        if os.path.exists(save_path):
            if self._check_file_sha(save_path, sha):
                logger.info(f"File '{save_path}' already exists with matching SHA, skipping.")
                return
            else:
                logger.info(f"File '{save_path}' not matching SHA, rm the file.")
                os.remove(save_path)
        
        for attempt in range(max_retries + 1):
            response = self._session.get(url)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                logger.info(f"Downloaded {url} to {save_path}")
                if not self._check_file_sha(save_path, sha):
                    raise ValueError(f"The downloaded {url} file does not match the expected SHA value. \nPlease check and try again")  
            else:
                logger.warning(f"Failed to download {url}, Status code: {response.status_code}")
                if attempt < max_retries:
                    logger.warning(f"Retrying in {retry_delay} millisecond...")
                    time.sleep(retry_delay/1000)
                else:
                    logging.error("Max retry attempts reached.\n Please check and try again")
                    break
    
    def _check_file_sha(self, file_path: Path, sha) -> bool:
        current_sha = self._calculate_sha(file_path)
        return current_sha == sha
   
    def _calculate_sha(self, file_path: Path) -> str:
        from hashlib import sha1
        with open(file_path, "r") as f:
            content = f.read()
            sha1_obj = sha1()
            content = content.encode('ascii')	# 以二进制编码
            content = b'blob %d\0' % len(content) + content
            sha1_obj.update(content)
            return sha1_obj.hexdigest()

if __name__ == "__main__":
   gitprompthub = GitPromptHub("github", "ptonlix/PromptHub", Path("."), sub_project="example") 

   print(gitprompthub.check_project_exists())
   gitprompthub.pull_project()
   print(gitprompthub.get_project_dependencies())