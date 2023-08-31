
from __future__ import annotations

from time import sleep
from typing import Any, Dict, List, Mapping, Sequence, Union
from pydantic import BaseModel, Field, validator

PromptTypesList = ["text", "yaml", "json", "python"]
PromptAllTypes = "all"

class MetaConfig(BaseModel):
    name: str = Field(frozen=True)
    version: str = Field(frozen=True, regex=r'^[0-9]\d?(\.([1-9]?\d)){2}$')
    description: str = Field(max_length=255)
    tag: List[str]  =Field(default=[])
    author: List[str] = Field(default=[])
    llm: List[str] =  Field(default=[])
    readme_format: str = Field(default="md")
    license: str | None = Field(default="MIT") 

class Config(BaseModel):

    meta: MetaConfig
    text_prompt: Dict[str, str] | None 
    yaml_prompt: Dict[str, str | List[Dict]] | None 
    json_prompt: Dict[str, str | List[Dict]] | None 
    python_prompt: Dict[str, str | List[Dict]] | None 

    @validator('text_prompt')
    def valid_text_prompt(cls, values: dict) -> dict:
        if not values.get("dirname"):
            raise ValueError("Text Section have not dirname")
        return values

    @validator('yaml_prompt')
    def valid_yaml_prompt(cls, values: dict) -> dict:
        if not values.get("dirname"):
            raise ValueError("Yaml Section have not dirname")
        if (list_value := values.get("list")):
            for idx, value in enumerate(list_value):
                if not value.get("name"):
                    raise ValueError(f"Yaml Section List{idx} have not name")
                if not value.get("dependencies"):
                    raise ValueError(f"Yaml Section List{idx} have not dependencies")
        else :
            raise ValueError("Yaml Section have not list")

        return values

    @validator('json_prompt')
    def valid_json_prompt(cls, values: dict) -> dict:
        if not values.get("dirname"):
            raise ValueError("Json Section have not dirname")
        if (list_value := values.get("list")):
            for idx, value in enumerate(list_value):
                if not value.get("name"):
                    raise ValueError(f"Json Section List{idx} have not name")
                if not value.get("dependencies"):
                    raise ValueError(f"Json Section List{idx} have not dependencies")
        else :
            raise ValueError("Json Section have not list")

        return values

    @validator('python_prompt')
    def valid_python_prompt(cls, values: dict) -> dict:
        if not values.get("dirname"):
            raise ValueError("Python Section have not dirname")
        if (list_value := values.get("list")):
            for idx, value in enumerate(list_value):
                if not value.get("name"):
                    raise ValueError(f"Python Section List{idx} have not name")
                if not value.get("dependencies"):
                    raise ValueError(f"Python Section List{idx} have not dependencies")
        else :
            raise ValueError("Python Section have not list")

        return values
    


if __name__ := "__main__":
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
    conf = Config(**config)