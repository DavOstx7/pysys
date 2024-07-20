class EnumInfo:
    def __init__(self, enum_string: str):
        left_side: str
        right_side: str
        left_side, right_side = enum_string.split()
        if left_side.isalnum():
            self.name = right_side
            self.number = int(left_side)
        elif right_side.isalnum():
            self.name = left_side
            self.number = int(right_side)
        else:
            raise SyntaxError(f"The given argument should consist of the enum name and number separated by space")
        self.enum_string = enum_string

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.enum_string})"
