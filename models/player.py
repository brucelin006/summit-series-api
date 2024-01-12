from fastapi_utils.api_model import APIModel
from enums.player import PlayerGenderEnum, PlayerStatusEnum, PlayerRoleEnum

class Player(APIModel):
    player_name: str
    player_gender: PlayerGenderEnum
    player_status: PlayerStatusEnum
    player_role: PlayerRoleEnum
