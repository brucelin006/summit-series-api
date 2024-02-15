from enum import auto
from fastapi_utils.enums import StrEnum

class PlayerGenderEnum(StrEnum):
    male = auto()
    female = auto()

class PlayerStatusEnum(StrEnum):
    available = auto()
    in_progress = auto()
    absent = auto()

class PlayerRoleEnum(StrEnum):
    admin = auto()
    user = auto()
