import json
from typing import Any, Optional
from local_filesystem.files.file import File

JSONModule = type(json)


class JsonFile(File):
    @property
    def json_module(self) -> JSONModule:
        return json

    def set_json(self, obj: Any, indent: Optional[str] = "\t") -> None:
        with open(self.str_path, "w") as writing_file_handler:
            json.dump(obj, writing_file_handler, indent=indent)

    def get_json(self) -> Any:
        with open(self.str_path, "r") as reading_file_handler:
            return json.load(reading_file_handler)


JSON_SUFFIX_MAP = {".json": JsonFile}
