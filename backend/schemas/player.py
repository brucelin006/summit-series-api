"""
serializes and converts the mongodb BSON to JSON
"""


def player_serial(db_item) -> dict:
    return {
        "id": str(db_item["_id"]),
        "name": db_item["player_name"],
        "gender": db_item["player_gender"],
        "status": db_item["player_status"],
        "role": db_item["player_role"],
    }


def player_list_serial(db_items) -> list:
    return [player_serial(db_item) for db_item in db_items]
