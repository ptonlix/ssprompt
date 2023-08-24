
from __future__ import annotations

import yaml
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Mapping

logger = logging.getLogger(__name__)

class PyYaml:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_to_yaml(self, data: Mapping):
        with open(self.file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def read_from_yaml(self) -> Mapping | None:
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError:
            logger.error(f"File '{self.file_path}' not found.")
            return None
        

if __name__ == "__main__":
    # Example usage
    data_to_write = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }

    yaml_file = "data.yaml"

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
