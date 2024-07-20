from typing import Optional
from commands_execution.outputs.options.output_options import OutputOptions


class Output:
    def __init__(self, stdout: bytes, stderr: bytes, exit_code: Optional[int] = None):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.output_options = OutputOptions(stdout=stdout, stderr=stderr)

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.stdout})"
