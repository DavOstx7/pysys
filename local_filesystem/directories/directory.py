from __future__ import annotations

import os
from typing import Union, List, ClassVar, Callable
from pathlib2 import PurePath
from local_filesystem.files.file import File
from local_filesystem.files.json_file import JSON_SUFFIX_MAP
from local_filesystem.files.yaml_file import YAML_SUFFIX_MAP
from local_filesystem.base.filesystem_base_node import FileSystemBaseNode
from local_filesystem.exceptions import PathNotFoundError, UnknownPathTypeError

SUFFIX_MAP = {**JSON_SUFFIX_MAP, **YAML_SUFFIX_MAP}


class Directory(FileSystemBaseNode):
    def __init__(self, path: Union[str, PurePath], is_create_dir_if_not_exists: bool = False):
        if not os.path.exists(path) and is_create_dir_if_not_exists:
            try:
                os.mkdir(path)
            except FileNotFoundError as invalid_path_error:
                raise NotADirectoryError(
                    f"Cannot create a file at '{path}', because it is an incorrect path"
                ) from invalid_path_error
        elif not os.path.isdir(path):
            raise NotADirectoryError("The path given exists but does not lead to a directory")
        super().__init__(path)

    def get_directory_nodes(self) -> List[FileSystemBaseNode]:
        listed_fs_nodes = os.listdir(self.str_path)
        return [self.create_correct_node_type(self / fs_node) for fs_node in listed_fs_nodes]

    def get_directory_nodes_by_name(self, filter_function: Callable[[str], bool]):
        return [fs_node for fs_node in self.get_directory_nodes() if filter_function(fs_node.name)]

    @staticmethod
    def create_correct_node_type(path: Union[str, PurePath]) -> FileSystemBaseNode:
        correct_node_type = Directory.select_correct_node_type(path)
        return correct_node_type(path)

    @staticmethod
    def select_correct_node_type(path: Union[str, PurePath]) -> ClassVar:
        if not os.path.exists(path):
            raise PathNotFoundError(f"The path '{path}' does not exist")
        if os.path.isdir(path):
            return Directory
        elif os.path.isfile(path):
            correct_file_node_type = SUFFIX_MAP.get(path.suffix, File)
            return correct_file_node_type
        else:
            raise UnknownPathTypeError(f"The path type of '{path} is unknown")


