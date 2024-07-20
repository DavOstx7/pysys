from typing import Union
from pathlib2 import PurePath
from local_filesystem.directories import directory
from local_filesystem.base.filesystem_base_node import FileSystemBaseNode

create_correct_node_type = directory.Directory.create_correct_node_type
select_correct_node_type = directory.Directory.select_correct_node_type


class FileSystemNode:
    def __new__(cls, path: Union[str, PurePath]) -> FileSystemBaseNode:
        return create_correct_node_type(path)
