from fastapi import APIRouter
from models.player import Player
from configs.database import client
from bson.objectid import ObjectId
from schemas.player import player_entity, player_entity_list

router = APIRouter()
players_collection = client["summit-series-db"].players

@router.get("/players")
async def find_all_players():
    result_list = players_collection.find()
    return player_entity_list(result_list)

@router.get("/players/{player_id}")
async def find_player_by_id(player_id: str):
    return player_entity(players_collection.find_one({"_id": ObjectId(player_id)}))

@router.post("/players")
async def create_player(player: Player):
    inserted_id = players_collection.insert_one(dict(player)).inserted_id
    db_player = players_collection.find_one({"_id": ObjectId(inserted_id)})
    return player_entity(db_player)