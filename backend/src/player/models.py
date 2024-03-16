from typing import Optional
from pydantic import BaseModel, root_validator, validator
from .enums import PlayerGenderEnum, PlayerStatusEnum, PlayerRoleEnum


class Player(BaseModel):
    player_name: str
    player_gender: PlayerGenderEnum
    player_status: PlayerStatusEnum
    player_role: PlayerRoleEnum
    player_password: str


class PlayerCreateRequest(BaseModel):
    player_name: str
    player_gender: PlayerGenderEnum
    player_status: PlayerStatusEnum
    player_role: PlayerRoleEnum
    player_password: str

    @validator("player_name")
    def validate_player_name(cls, v):
        if not v.isalnum():
            raise ValueError("player name must contain only alphabets")
        if len(v) > 20:
            raise ValueError("player name must be no longer than 20 characters")
        return v.strip()

    @validator("player_password")
    def validate_player_password(cls, v):
        if len(v) > 8:
            raise ValueError("player password must be no longer than 8 characters")
        elif len(v) < 1:
            raise ValueError("player password must be longer than 1 character")
        return v


class PlayerUpdateRequest(BaseModel):
    player_name: Optional[str] = None
    player_gender: Optional[int] = None
    player_status: Optional[int] = None
    player_role: Optional[int] = None
    player_password: Optional[str] = None

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        # Check if all values are None
        if all(value is None for value in values.values()):
            raise ValueError("At least one field must be provided for update")
        return values


class PlayerResponse(BaseModel):
    player_name: str
    player_gender: PlayerGenderEnum
    player_status: PlayerStatusEnum
    player_role: PlayerRoleEnum
