from enum import IntEnum


class UserRole(IntEnum):
    STUDENT = 1
    EDUCATOR = 2
    ADMIN = 3
    EXTERNAL = 4

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_
