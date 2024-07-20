import re
import functools
from typing import Optional, Container, Any
from typing import Callable, TypeVar, ParamSpec
from platform_independent.shared.base_filter import BaseFilter
from platform_independent.shared.consts import DATE_VALUES_REGEX

T = TypeVar('T')
P = ParamSpec('P')


def retry(times: int = 1, exceptions: Optional[Container[Exception]] = None):
    if not exceptions:
        exceptions = {Exception}

    def retry_decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        @functools.wraps(func)
        def func_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as caught_exception:
                    print(f"[-] Caught exception {caught_exception} when calling {func}")
                    for exception in exceptions:
                        if isinstance(caught_exception, exception):
                            continue
                    raise
            return func(*args, **kwargs)

        return func_wrapper

    return retry_decorator


def pipe_filter_to_command(command: str, piped_filter_command: Optional[BaseFilter]) -> str:
    if piped_filter_command:
        return f"{command} | {piped_filter_command.get_filter_command()}"
    return command


def append_filter_to_command(command: str, filter_command: Optional[BaseFilter], in_between: str = '') -> str:
    full_command = command
    if in_between:
        full_command += f" {in_between}"
    if filter_command:
        full_command += f" {filter_command.get_filter_command()}"
    return full_command


def parse_date_time_to_str(date_time: str) -> str:
    [(year, month, day, hour, minutes, seconds)] = re.findall(DATE_VALUES_REGEX, date_time)
    return f"{day}/{month}/{year} {hour}:{minutes}:{seconds}"


def convert_100_nanoseconds_time_to_seconds_time(time: int) -> int:
    return time * (10 ** -7)
