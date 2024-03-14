from fastapi import APIRouter, status, HTTPException, Body
from models.player import Player, PlayerResponse, players_collection
from bson.objectid import ObjectId
from schemas.player import player_list_serial
from pymongo.errors import DuplicateKeyError
from pymongo.collection import ReturnDocument
from utils.encrypt import encrypt_password

router = APIRouter()


@router.get("/")
async def find_all_players():
    result_list = players_collection.find()
    return player_list_serial(result_list)


@router.get("/{player_id}", response_model=PlayerResponse)
async def find_player_by_id(player_id: str):
    player = players_collection.find_one({"_id": ObjectId(player_id)})
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found",
        )
    return player


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_player(player: Player):
    player_dict = player.dict()
    player_dict["player_password"] = encrypt_password(player_dict["player_password"])
    try:
        inserted_id = players_collection.insert_one(player_dict).inserted_id
        return str(inserted_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="player name must be unique")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: str, player: Player = Body(...)):
    update_data = {k: v for k, v in player.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update.")

    updated_player = players_collection.find_one_and_update(
        {"_id": ObjectId(player_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if not updated_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found",
        )
    return player


# TODO: implement update password only endpoint


@router.delete("/{player_id}")
async def delete_player(player_id: str):
    deleted_player = players_collection.find_one_and_delete(
        {"_id": ObjectId(player_id)}
    )
    if not deleted_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found",
        )
