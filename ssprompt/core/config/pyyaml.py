
from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

import yaml

from ssprompt.core.config import Config

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Mapping, Optional

logger = logging.getLogger(__name__)

class PyYaml:
    def __init__(self, file_path: Optional[Path]=None):
        self.file_path = file_path

    def write_config_to_yaml(self, conf: Config):
        if not self.file_path:
            return 
        with open(self.file_path, 'w+') as file:
            # 按顺序输出 
            yaml.dump({"meta":conf.meta.dict()}, file, default_flow_style=False)
            if conf.text_prompt:
                yaml.dump({"text_prompt":conf.text_prompt}, file, default_flow_style=False)
            if conf.json_prompt:
                yaml.dump({"json_prompt":conf.json_prompt}, file, default_flow_style=False)
            if conf.yaml_prompt:
                yaml.dump({"yaml_prompt":conf.yaml_prompt}, file, default_flow_style=False)
            if conf.python_prompt:
                yaml.dump({"python_prompt":conf.python_prompt}, file, default_flow_style=False)

    def reload_config_to_yaml(self, conf: Config):
        import os 
        os.remove(self.file_path)
        self.write_config_to_yaml(conf)
           

    def read_config_from_yaml(self) -> Config | Any:
        if not self.file_path:
            return 
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                return Config(**data)
        except FileNotFoundError:
            logger.error(f"File '{self.file_path}' not found.")
            return None
    
    @classmethod    
    def read_config_from_str(cls, s: str) -> Config | Any:
        try:
            data = yaml.safe_load(s)
            return Config(**data)
        except Exception:
            logger.error(f"Parse '{s}' to ssprompt config object failed")
            return None
    
    @classmethod      
    def read_from_str(cls, s: str) -> Mapping | None:
        try:
            data = yaml.safe_load(s)
            return data
        except Exception:
            logger.error(f"Parse '{s}' to yaml failed")
            return None
          
    def write_to_yaml(self, data: Mapping):
        if not self.file_path:
            return 
        with open(self.file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def read_from_yaml(self) -> Mapping | None:
        if not self.file_path:
            return 
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError:
            logger.error(f"File '{self.file_path}' not found.")
            return None
       
    def file_exist(self) -> bool:
        return self.file_path.exists() if self.file_path else False

    def is_ssprompt_config(self) -> bool:
        try:
            config = self.read_config_from_yaml()
        except ValueError as e:
            logger.error("The config yaml isn't the ssprompt config file.")
            logger.debug(e)
            return False
        return True


if __name__ == "__main__":
    #Example usage
    data_to_write = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }

    yaml_file = Path("data.yaml")

    # Write data to YAML file
    yaml_writer = PyYaml(yaml_file)
    yaml_writer.write_to_yaml(data_to_write)
    print(f"Data written to {yaml_file}")

    # Read data from YAML file
    yaml_reader = PyYaml(yaml_file)
    read_data = yaml_reader.read_from_yaml()
    if read_data:
        print("Data read from YAML file:")
        print(read_data)

    config = {
        "meta":{
        "name":"test",
        "version":"0.1.2",
        "description":"qwe123",
        "tag":["question"],
        "author":["chenfudong"],
        "llm": ["chatgpt"],
        "readme_format": "md",
        "license" : "MIT"},
        "text_prompt":{
            "dirname":"123",
        },
        "yaml_prompt":{
            "dirname":"123",
            "list":[
                {
                "name": "test",
                "dependencies":[
                {
                    "langchain": "^0.0.267"
                }]}
             ]
        },
        "json_prompt":{
            "dirname":"123",
            "list":[
                {
                "name": "test",
                "dependencies":[
                {
                    "langchain": "^0.0.267"
                }]}
             ]
        },
        "python_prompt":{
            "dirname":"123",
            "list":[
                {
                "name": "test",
                "dependencies":[
                {
                    "langchain": "^0.0.267"
                }]}
             ]
        },
    }   
    conf=Config(**config)

    yaml_conf = PyYaml(yaml_file) 

    yaml_conf.write_config_to_yaml(conf)

    print(yaml_conf.read_config_from_yaml())