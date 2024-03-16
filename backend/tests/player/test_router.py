from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.database import db


@pytest.fixture(autouse=True)
def use_test_players_collection(monkeypatch):
    def mock_get_players_collection():
        return db["test_players"]  # Adjusted to the correct collection

    # Direct reference to the module where get_players_collection is defined
    monkeypatch.setattr(
        "src.player.router.get_players_collection", mock_get_players_collection
    )


@pytest.fixture(autouse=True, scope="module")
def clean_database():
    # Setup: Clean the database before each test
    db["test_players"].delete_many({})
    # Here, add any other collections you might want to clean

    # This line yields control back to the test function
    yield

    # Teardown: Clean up the database after each test
    db["test_players"].delete_many({})
    # Repeat for any other collections as necessary


# FIXME: mock regular user_id
@pytest.mark.asyncio
async def test_update_player_as_admin(monkeypatch):
    def mock_admin_user():
        """Mock function to simulate an admin user."""
        return {"_id": "admin_user_id", "player_role": 0}

    # Use monkeypatch to simulate an admin user
    monkeypatch.setattr("path.to.your.get_current_user", mock_admin_user)

    # Perform the update operation as an admin
    response = client.put(
        "/players/player_id_to_update",
        json={
            "player_name": "New Name",
            # Include other fields as necessary
        },
    )
    assert response.status_code == 200
    # Add more assertions to verify the response data


# FIXME: mock regular user_id
@pytest.mark.asyncio
async def test_update_player_as_regular_user(monkeypatch):
    def mock_regular_user():
        """Mock function to simulate a regular user."""
        return {"_id": "regular_user_id", "player_role": 1}

    # Use monkeypatch to simulate a regular user
    monkeypatch.setattr("path.to.your.get_current_user", mock_regular_user)

    # Attempt to perform an update operation as a regular user
    response = client.put(
        "/players/player_id_to_update",
        json={
            "player_name": "New Name",
            # Regular user trying to update; adjust as per your logic
        },
    )
    assert response.status_code == 403  # or whatever is appropriate based on your logic


client = TestClient(app)


def test_create_player_success():
    response = client.post(
        "/players/",
        json={
            "player_name": "DuplicateTest",
            "player_gender": 0,
            "player_status": 0,
            "player_role": 0,
            "player_password": "11111111",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, str)


def test_create_player_duplicate_name():
    # Assuming "DuplicatePlayer" already exists
    response = client.post(
        "/players/",
        json={
            "player_name": "DuplicateTest",
            "player_password": "11111111",
            "player_gender": 0,
            "player_status": 0,
            "player_role": 0,
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == f"player name {"DuplicateTest"} is taken"


def test_find_all_players():
    response = client.get("/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure the response is a list


def test_find_player_by_id_success():
    # Assuming a player with ID '65f37d1d4d1666f75a92ee73' exists in test collection
    player_id = client.post(
        "/players/",
        json={
            "player_name": "FindByIdTest",
            "player_password": "11111111",
            "player_gender": 0,
            "player_status": 0,
            "player_role": 0,
        },
    ).json()

    response = client.get(f"/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["player_name"] == "FindByIdTest"
    # Additional assertions to verify the player data


def test_update_player_success():
    # create a player
    player_id = client.post(
        "/players/",
        json={
            "player_name": "UpdateTest",
            "player_password": "11111111",
            "player_gender": 0,
            "player_status": 0,
            "player_role": 0,
        },
    ).json()

    response = client.put(
        f"/players/{player_id}",
        json={
            "player_name": "Updated",
            # Include other fields to be updated
        },
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["player_name"] == "Updated"
    # Additional assertions to verify the update was successful


def test_delete_player_success():
    # Create a player to be deleted, or assume a player with ID 'deletable_id' exists
    player_id = client.post(
        "/players/",
        json={
            "player_name": "DeleteTest",
            "player_gender": 0,
            "player_status": 0,
            "player_role": 0,
            "player_password": "delete",
        },
    ).json()
    # delete
    response = client.delete(f"/players/{player_id}")
    assert response.status_code == 200
    # You can also perform a get request to ensure the player has been deleted
    check_response = client.get(f"/players/{player_id}")
    assert check_response.status_code == 404
