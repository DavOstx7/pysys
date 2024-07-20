from platform_independent.shared.base_filter import BaseFilter


class FindStrFilter(BaseFilter):
    def __init__(self, find_str_options: str):
        self.find_str_options = find_str_options.replace(r'"', r'\"')

    def get_filter_command(self) -> str:
        return f"findstr {self.find_str_options}"
