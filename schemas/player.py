# serializes and converts mongodb BSON to JSON

def player_entity(db_item) -> dict:
    return {
        "id": str(db_item["_id"]),
        "name": db_item["player_name"],
        "gender": db_item["player_gender"],
        "status": db_item["player_status"],
        "role": db_item["player_role"] 
    }

def player_entity_list(db_item_list) -> list:
    return [player_entity(db_item) for db_item in db_item_list]