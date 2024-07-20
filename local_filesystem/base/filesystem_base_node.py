import os
from pathlib2 import PurePath, PureWindowsPath, PurePosixPath
from typing import Union
from local_filesystem.base.filesystem_node_date_stats import FileSystemDateStats
from local_filesystem.exceptions import PathNotFoundError

OSModule = type(os)


class FileSystemBaseNode(PurePath):
    _flavour = PureWindowsPath._flavour if os.name == "nt" else PurePosixPath._flavour

    def __init__(self, path: Union[str, PurePath]):
        if not os.path.exists(path):
            raise PathNotFoundError(f"The path '{path}' does not exist")
        super().__init__()

    @property
    def str_path(self) -> str:
        return PurePath.__str__(self)

    @property
    def date_stats(self) -> FileSystemDateStats:
        return FileSystemDateStats(os.stat(self.str_path))

    @property
    def os_module(self) -> OSModule:
        return os

    def rename(self, new_name: str) -> None:
        os.rename(self.str_path, new_name)

    def delete(self) -> None:
        if os.path.isdir(self.str_path):
            os.rmdir(self.str_path)
        else:
            os.remove(self.str_path)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.str_path})"
