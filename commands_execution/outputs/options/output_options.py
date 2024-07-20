from typing import List
from commands_execution.exceptions import OutputDecodingError

class OutputOptions:
    def __init__(self, stdout: bytes, stderr: bytes):
        self._stdout = stdout
        self._stderr = stderr

    @property
    def stdout_clean(self) -> str:
        try:
            stripped_stdout = self._stdout.strip()
            return stripped_stdout.decode()
        except UnicodeDecodeError as unicode_error:
            raise OutputDecodingError("Cannot decode stdout using utf-8") from unicode_error

    @property
    def stdout_lines(self) -> List[bytes]:
        return self._stdout.splitlines()

    @property
    def stdout_clean_lines(self) -> List[str]:
        return [line.strip() for line in self.stdout_clean.splitlines() if line.strip()]

    @property
    def stderr_clean(self) -> str:
        try:
            stripped_stderr = self._stderr.strip()
            return stripped_stderr.decode()
        except UnicodeDecodeError as unicode_error:
            raise OutputDecodingError("Cannot decode stdout using utf-8") from unicode_error

    @property
    def stderr_lines(self) -> List[bytes]:
        return self._stderr.splitlines()

    @property
    def stderr_clean_lines(self) -> List[str]:
        return [line.strip() for line in self.stderr_clean.splitlines() if line.strip()]