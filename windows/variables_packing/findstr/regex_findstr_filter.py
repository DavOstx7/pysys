from platform_independent.shared.base_filter import BaseFilter
from windows.variables_packing.findstr.base.template_findstr_filter import TemplateFindStr


class RegexFindStrFilter(TemplateFindStr, BaseFilter):
    def __init__(self, regex: str, is_case_sensitive: bool = True, is_literal_search: bool = False):
        self.regex = regex.replace(r'"', r'\"')
        super().__init__(is_case_sensitive=is_case_sensitive, is_literal_search=is_literal_search)

    def get_filter_command(self) -> str:
        find_str_command = "findstr /R "
        if not self.is_case_sensitive:
            find_str_command += "/I "

        if self.is_literal_search:
            find_str_command += "/C:"

        find_str_command += f'"{self.regex}"'
        return find_str_command
