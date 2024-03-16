from fastapi import APIRouter, status, Body, Depends
from src.player.models import (
    Player,
    PlayerCreateRequest,
    PlayerResponse,
    PlayerUpdateRequest,
)
from bson.objectid import ObjectId
import services

router = APIRouter(prefix="/players")


@router.get("/")
async def get_all_players():
    return await services.find_all_players()


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player_by_id(
    player_id: ObjectId = Depends(services.validate_object_id),
):
    return await services.find_player_by_id(player_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_player(player: PlayerCreateRequest):
    inserted_id = await services.create_player(player)
    return str(inserted_id)


@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: ObjectId = Depends(services.validate_object_id),
    data: PlayerUpdateRequest = Body(...),
    current_user: Player = Depends(services.get_current_user),
):
    return await services.update_player(player_id, data.dict())


# TODO: implement update password only endpoint


@router.delete("/{player_id}")
async def delete_player(player_id: ObjectId = Depends(services.validate_object_id)):
    try:
        await services.delete_user(player_id)
    except Exception as e:
        raise e
