from platform_independent.shared.base_filter import BaseFilter
from typing import Optional, Dict, List
from windows.local.svcs.consts import SC_FILTER_OPTIONS

SC_FILTER_OPTIONS: Dict[str, List[str]] = SC_FILTER_OPTIONS


class ScQueryFilter(BaseFilter):
    def __init__(self, service_type: Optional[str] = None, service_state: Optional[str] = None,
                 buffer_size_bytes: Optional[int] = None, resume_index: Optional[int] = None,
                 service_group: Optional[str] = None):
        self.service_type = service_type
        self.service_state = service_state
        self.buffer_size_bytes = buffer_size_bytes
        self.resume_index = resume_index
        self.service_group = service_group

    def get_filter_command(self) -> str:
        sc_filter = " "
        if self.service_type:
            sc_filter = f"type={self.service_type} "
        if self.service_state:
            sc_filter += f"state={self.service_state} "
        if self.buffer_size_bytes:
            sc_filter += f"bufize={self.buffer_size_bytes} "
        if self.resume_index:
            sc_filter += f"ri={self.resume_index} "
        if self.service_group:
            sc_filter += f"group={self.service_group} "
        return sc_filter.strip()
