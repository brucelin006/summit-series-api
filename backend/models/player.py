# from dataclasses import dataclass
# from fastapi_utils.api_model import APIModel
from configs.database import db
from pydantic import BaseModel, validator
from enums.player import PlayerGenderEnum, PlayerStatusEnum, PlayerRoleEnum

players_collection = db["test_players"]
players_collection.create_index("player_name", unique=True)


class Player(BaseModel):
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
        return v


class PlayerResponse(BaseModel):
    player_name: str
    player_gender: PlayerGenderEnum
    player_status: PlayerStatusEnum
    player_role: PlayerRoleEnum
