import os
import time
import re


class FileSystemDateStats:
    def __init__(self, stat_result: os.stat_result):
        self.str_creation_time = self._fix_st_month_day(time.ctime(stat_result.st_ctime))
        self.str_access_time = self._fix_st_month_day(time.ctime(stat_result.st_atime))
        self.str_modification_time = self._fix_st_month_day(time.ctime(stat_result.st_mtime))

    @staticmethod
    def _fix_st_month_day(str_date: str) -> str:
        re_result = re.findall(r"\w+ \w+ ( \d) \d+:\d+:\d+ \d+", str_date)
        if re_result:
            [month_day] = re_result
            space, day = month_day
            return str_date.replace(month_day, '0' + day)
        else:
            return str_date

    def __str__(self) -> str:
        return f"ComponentStats(creation='{self.str_creation_time}'," \
               f" access='{self.str_access_time}'," \
               f" modification='{self.str_modification_time}')"
