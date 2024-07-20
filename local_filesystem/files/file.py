import os

from typing import Union, Optional
from commands_execution import Executor, Output

from pathlib2 import PurePath
from local_filesystem.base.filesystem_base_node import FileSystemBaseNode

EXECUTOR = Executor()


class File(FileSystemBaseNode):
    def __init__(self, path: Union[str, PurePath], is_create_file_if_not_exists: bool = False):
        if not os.path.exists(path) and is_create_file_if_not_exists:
            try:
                self.create_file(path)
            except FileNotFoundError as invalid_path_error:
                raise NotADirectoryError(
                    f"Cannot create a file at '{path}', because it is an incorrect path"
                ) from invalid_path_error
        elif not os.path.isfile(path):
            raise NotADirectoryError("The path given exists but does not lead to a file")
        super().__init__(path)

    @staticmethod
    def create_file(path: Union[str, PurePath]) -> None:
        file = open(path, mode="x")
        file.close()

    def get_content(self) -> bytes:
        with open(self, "rb") as reading_file_handler:
            return reading_file_handler.read()

    def get_str_content(self, decoding_type: Optional[str] = None) -> str:
        bytes_content = self.get_content()
        if decoding_type:
            return bytes_content.decode(decoding_type)
        else:
            return bytes_content.decode()

    def set_content(self, content: bytes) -> None:
        with open(self, "wb") as writing_file_handler:
            writing_file_handler.write(content)

    def set_str_content(self, content: str, encoding: Optional[str] = None) -> None:
        if encoding:
            self.set_content(content.encode(encoding))
        else:
            self.set_content(content.encode())

    def add_content(self, content: bytes) -> None:
        with open(self, "ab") as writing_file_handler:
            writing_file_handler.write(content)

    def add_str_content(self, content: str, encoding: Optional[str] = None) -> None:
        if encoding:
            self.add_content(content.encode(encoding))
        else:
            self.add_content(content.encode())

    def execute_file(self,
                     stdin: Optional[str] = None, timeout: Optional[int] = None,
                     is_full_output: Optional[bool] = False) -> Output:
        return EXECUTOR.execute_command_simply(
            self.str_path, stdin=stdin, timeout=timeout, is_full_output=is_full_output
        )

    @property
    def run_file(self) -> execute_file:
        return self.execute_file
