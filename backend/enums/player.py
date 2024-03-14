from enum import IntEnum
# from fastapi_utils.enums import StrEnum


class PlayerGenderEnum(IntEnum):
    male = 0
    female = 1


class PlayerStatusEnum(IntEnum):
    available = 0
    in_progress = 1
    absent = 2


class PlayerRoleEnum(IntEnum):
    admin = 0
    user = 1
