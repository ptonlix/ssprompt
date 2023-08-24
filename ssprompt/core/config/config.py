
from __future__ import annotations
from ast import pattern

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, root_validator

if TYPE_CHECKING:
    from typing import Sequence, Dict, Any,Union

class Config(BaseModel):

    name: str = Field(frozen=True)
    version: str = Field(frozen=True, pattern= r'^([1-9]\d|[1-9])(\.([0-9]){1,2}){2}$')
    description: str = Field(max_length=255)
    tag: list[str]  =Field(default=[])
    author: list[str] = Field(default=[])
    llm: list[str] =  Field(default=[])
    readme_format: str = Field(default="md")
    license: str | None = Field(default="MIT")
    text_type: Union[Dict[str, Union[str , Dict[str, Any]]] ,None]
    yaml_type: Dict[str, str | Dict[str, Any]] | None = Field(default=None, alias="yaml") 
    json_type: Dict[str, str | Dict[str, Any]] | None = Field(default=None, alias="json")
    python_type: Dict[str, str | Dict[str, Any]] | None = Field(default=None, alias="python")

    @root_validator
    def valid_model(cls, values: dict) -> dict:
        if text_value := values.get("text_type"):
            if not text_value.get("dirname"):
                raise ValueError("Text Section have not dirname")
        return values


if __name__ := "__main__":
    config = {
        "name":"test",
        "version":"0.10.0",
        "description":"qwe123",
        "tag":["question"],
        "author":["chenfudong"],
        "llm": ["chatgpt"],
        "readme_format": "md",
        "license" : "MIT",
        "text_type":{"dirname":"123"}
    }   
    conf = Config(**config)
    print(conf)