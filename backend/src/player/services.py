from bson import ObjectId
from fastapi import HTTPException, Path, status
from pymongo import ReturnDocument
from pymongo.collection import Collection
from src.database import db
from src.player.enums import PlayerRoleEnum
from src.player.models import Player
from src.player.schemas import player_list_serial
from src.player.utils import encrypt_password


def get_players_collection() -> Collection:
    return db["players"]


async def find_all_players() -> list[Player]:
    collection = get_players_collection()
    result_list = await collection.find()
    return player_list_serial(result_list)


async def find_player_by_id(player_id: ObjectId) -> Player:
    collection = get_players_collection()
    player: Player = collection.find_one({"_id": player_id})
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found",
        )
    return player


async def create_player(player: Player) -> ObjectId:
    collection = get_players_collection()
    player_dict = player.dict()
    player_name = player_dict["player_name"]
    if collection.find_one({"player_name": player_name}) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"player name {player_name} is taken",
        )
    player_dict["player_password"] = encrypt_password(player_dict["player_password"])
    try:
        return collection.insert_one(player_dict).inserted_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


async def update_player(player_id: ObjectId, data: dict, current_user) -> Player:
    collection = get_players_collection()
    if data["player_name"] is not None:
        validate_no_duplicate_player_name(data["player_name"], collection)

    role = current_user["player_role"]
    # Admins can update any field for any player
    if role == PlayerRoleEnum.admin:
        updated_player = collection.find_one_and_update(
            {"_id": ObjectId(player_id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
    elif role == PlayerRoleEnum.user:
        # Regular users can only update their own username or password
        if current_user["_id"] != player_id:
            raise HTTPException(status_code=403, detail="Operation not permitted")

        allowed_fields = {"player_name", "player_password"}
        update_fields = {
            k: v for k, v in data.items() if k in allowed_fields and v is not None
        }
        if update_fields is None:
            raise HTTPException(status_code=400, detail="Invalid update request")

        updated_player = collection.find_one_and_update(
            {"_id": ObjectId(player_id)},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER,
        )

        if updated_player is None:
            raise HTTPException(status_code=404, detail="Player not found")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown player role"
        )

    return updated_player


async def delete_user(player_id: ObjectId) -> None:
    collection = get_players_collection()
    deleted_player = collection.find_one_and_delete({"_id": ObjectId(player_id)})
    if deleted_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found",
        )


# TODO:
def get_current_user():
    pass


def validate_object_id(player_id: str = Path(...)) -> ObjectId:
    """
    Dependency to validate and convert player_id path parameter into an ObjectId.
    Raises HTTPException if validation fails.
    """
    try:
        return ObjectId(player_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ObjectId, must be a 12-byte input or a 24-character hex string",
        ) from e


def validate_no_duplicate_player_name(player_name: str, collection: Collection) -> None:
    if collection.find_one({"player_name": player_name}) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"player name {player_name} is taken",
        )
