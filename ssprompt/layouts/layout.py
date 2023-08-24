from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from packaging.utils import canonicalize_name

if TYPE_CHECKING:
    from collections.abc import Mapping,Sequence

SSPROMPT_DEFAULT = """\
meta:
  name: ""
  version: ""
  description: ""
  tag:
    - ""
  authors:
    - ""
  llm:
    - ""
  license: ""
  readme:""

text:
  dirname: "text" 

yaml:
  dirname: "yaml" 
  list:
    -
      name: ""
      dependencies:
        - langchain: ""
        
json:
  dirname: "json" 
  list:
    -
      name: ""
      dependencies:
        - langchain: ""

python:
  dirname: "python" 
  list:
    -
      name: "prompt"
      dependencies:
        - langchain: ""
"""

class Layout:
    def __init__(
        self,
        name: str,
        version: str = "0.1.0",
        description: str = "",
        tag: Sequence[str] = [], 
        author: Sequence[str] = [], 
        llm: Sequence[str] = [], 
        readme_format: str = "md",
        license: str | None = None,
        text: Mapping[str, str | Mapping[str, Any]] | None = None,
        yaml: Mapping[str, str | Mapping[str, Any]] | None = None,
        json: Mapping[str, str | Mapping[str, Any]] | None = None,
        python: Mapping[str, str | Mapping[str, Any]] | None = None, 
    ) -> None:
        self._project = canonicalize_name(name) 
        self._version = version
        self._description = description
        self._tag = tag
        self._author = author if author else "Your Name <you@example.com>" 
        self._llm = llm
        self._readme_format = readme_format.lower()
        self._license = license

        self._text = text or {}
        self._yaml = yaml or {}
        self._json = json or {}
        self._python = python or {}

    def _create_readme(self, path: Path) -> Path:
        readme_file = path.joinpath(f"README.{self._readme_format}")
        readme_file.touch()
        return readme_file


    