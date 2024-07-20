import ruamel_yaml

from typing import Any
from local_filesystem.files.file import File

YAMLModule = type(ruamel_yaml)


class YamlFile(File):
    @property
    def yaml_module(self) -> YAMLModule:
        return ruamel_yaml

    def set_yaml(self, data: Any) -> None:
        with open(self.str_path, "w") as writing_stream:
            ruamel_yaml.safe_dump(data, writing_stream)

    def get_yaml(self) -> Any:
        with open(self.str_path, "r") as reading_stream:
            return ruamel_yaml.safe_load(reading_stream)


YAML_SUFFIX_MAP = {".yaml": YamlFile, ".yml": YAMLModule}
