# test_api.py
import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_json_files():
    """
    Ensures any leftover JSON files are removed so each test starts fresh.
    Adjust as needed if you want data to persist between tests.
    """
    for filename in ["users.json", "houses.json", "rooms.json", "devices.json"]:
        if os.path.exists(filename):
            os.remove(filename)
    yield

# -----------------------------
# USERS
# -----------------------------
def test_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    payload = {
        "user_id": "u1",
        "name": "Test User",
        "email": "test@example.com",
        "privilege": "owner"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user_id"] == "u1"
    assert data["privilege"] == "owner"

def test_create_duplicate_user():
    user = {
        "user_id": "u2",
        "name": "Dup",
        "email": "dup@example.com",
        "privilege": "admin"
    }
    # First time
    resp1 = client.post("/users", json=user)
    assert resp1.status_code == 201

    # Second time => 409
    resp2 = client.post("/users", json=user)
    assert resp2.status_code == 409

def test_update_nonexistent_user():
    updated_data = {
        "user_id": "ghost",
        "name": "Ghost Updated",
        "email": "ghost@domain.com",
        "privilege": "resident"
    }
    resp = client.put("/users/ghost", json=updated_data)
    assert resp.status_code == 404

def test_user_crud_cycle():
    """
    Demonstrate creating, retrieving, updating, and deleting a user in one flow.
    """
    # Create
    payload = {
        "user_id": "u100",
        "name": "Cycle Test",
        "email": "cycle@example.com",
        "privilege": "owner"
    }
    create_resp = client.post("/users", json=payload)
    assert create_resp.status_code == 201

    # Retrieve
    get_resp = client.get("/users/u100")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Cycle Test"

    # Update
    updated_data = {
        "user_id": "u100",
        "name": "Cycle Test - Updated",
        "email": "updated@example.com",
        "privilege": "admin"
    }
    put_resp = client.put("/users/u100", json=updated_data)
    assert put_resp.status_code == 200
    assert put_resp.json()["email"] == "updated@example.com"

    # Delete
    del_resp = client.delete("/users/u100")
    assert del_resp.status_code == 200

    # Confirm deleted
    get_deleted = client.get("/users/u100")
    assert get_deleted.status_code == 404


# -----------------------------
# HOUSES
# -----------------------------
def test_houses_empty():
    resp = client.get("/houses")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_house_requires_valid_owner():
    """
    A House schema must include a valid User schema as 'owner'.
    We'll create a user first, then reference it in the house.
    """
    # Create a user
    user_payload = {
        "user_id": "owner1",
        "name": "House Owner",
        "email": "owner@example.com",
        "privilege": "owner"
    }
    user_resp = client.post("/users", json=user_payload)
    assert user_resp.status_code == 201

    # Create a house referencing this user
    house_payload = {
        "house_id": "house1",
        "address": "123 Main St",
        "owner": user_payload,  # nest the user info here
        "gps_location": [40.7128, -74.0060],
        "num_rooms": 2,
        "num_baths": 1
    }
    house_resp = client.post("/houses", json=house_payload)
    assert house_resp.status_code == 201
    data = house_resp.json()
    assert data["house_id"] == "house1"
    assert data["owner"]["user_id"] == "owner1"

def test_delete_nonexistent_house():
    resp = client.delete("/houses/ghost-house")
    assert resp.status_code == 404

def test_house_crud_cycle():
    # First, create user who will own the house
    user = {
        "user_id": "howner",
        "name": "House Master",
        "email": "howner@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user)

    # Create the house
    house_payload = {
        "house_id": "h123",
        "address": "111 Pineapple Ave",
        "owner": user,
        "gps_location": [40.7128, -74.0060],
        "num_rooms": 3,
        "num_baths": 2
    }
    create_resp = client.post("/houses", json=house_payload)
    assert create_resp.status_code == 201

    # Retrieve
    get_resp = client.get("/houses/h123")
    assert get_resp.status_code == 200
    assert get_resp.json()["address"] == "111 Pineapple Ave"

    # Update
    updated_payload = {
        "house_id": "h123",
        "address": "999 Updated Lane",
        "owner": user,
        "gps_location": [40.7128, -74.0060],
        "num_rooms": 5,
        "num_baths": 3
    }
    put_resp = client.put("/houses/h123", json=updated_payload)
    assert put_resp.status_code == 200
    assert put_resp.json()["address"] == "999 Updated Lane"

    # Delete
    del_resp = client.delete("/houses/h123")
    assert del_resp.status_code == 200

    # Confirm gone
    gone_resp = client.get("/houses/h123")
    assert gone_resp.status_code == 404


# -----------------------------
# ROOMS
# -----------------------------
def test_rooms_empty():
    resp = client.get("/rooms")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_room():
    """
    A Room references a House (which references a User).
    So we must create a User, then a House, then a Room.
    """
    # Create user
    user_payload = {
        "user_id": "room-owner",
        "name": "Room Owner",
        "email": "room_owner@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user_payload)

    # Create house
    house_payload = {
        "house_id": "room-house1",
        "address": "Room Address",
        "owner": user_payload,
        "gps_location": [30.0, 50.0],
        "num_rooms": 4,
        "num_baths": 2
    }
    client.post("/houses", json=house_payload)

    # Create room referencing the house
    room_payload = {
        "name": "Living Room",
        "floor": 1,
        "house": house_payload
    }
    resp = client.post("/rooms", json=room_payload)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Living Room"

def test_rename_room():
    # Create user, house, room
    user = {
        "user_id": "renamer",
        "name": "Renamer Bob",
        "email": "renamer@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user)
    house = {
        "house_id": "rename-house",
        "address": "123 Renamer Lane",
        "owner": user,
        "gps_location": [33.0, -70.0],
        "num_rooms": 3,
        "num_baths": 2
    }
    client.post("/houses", json=house)
    room = {
        "name": "Old Room Name",
        "floor": 1,
        "house": house
    }
    client.post("/rooms", json=room)

    # Rename the room using PUT
    new_data = {
        "name": "New Room Name",
        "floor": 1,
        "house": house
    }
    put_resp = client.put("/rooms/Old Room Name", json=new_data)
    assert put_resp.status_code == 200
    assert put_resp.json()["name"] == "New Room Name"

    # Confirm old name is gone, new name is present
    old_check = client.get("/rooms/Old Room Name")
    assert old_check.status_code == 404

    new_check = client.get("/rooms/New Room Name")
    assert new_check.status_code == 200
    assert new_check.json()["name"] == "New Room Name"

def test_delete_nonexistent_room():
    del_resp = client.delete("/rooms/MissingRoom")
    assert del_resp.status_code == 404


# -----------------------------
# DEVICES
# -----------------------------
def test_devices_empty():
    resp = client.get("/devices")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_device():
    """
    A Device references a Room (which references a House -> User).
    So we must create a user, house, room, then device.
    """
    # 1. Create user
    user = {
        "user_id": "dev-owner",
        "name": "Device Owner",
        "email": "dev_owner@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user)

    # 2. Create house
    house = {
        "house_id": "dev-house1",
        "address": "Device House Lane",
        "owner": user,
        "gps_location": [45.0, -120.0],
        "num_rooms": 2,
        "num_baths": 1
    }
    client.post("/houses", json=house)

    # 3. Create room
    room = {
        "name": "Device Room",
        "floor": 1,
        "house": house
    }
    client.post("/rooms", json=room)

    # 4. Create device
    device_payload = {
        "device_id": "d100",
        "type": "light",
        "room": room
    }
    dev_resp = client.post("/devices", json=device_payload)
    assert dev_resp.status_code == 201
    assert dev_resp.json()["device_id"] == "d100"

    # Retrieve
    get_resp = client.get("/devices/d100")
    assert get_resp.status_code == 200
    assert get_resp.json()["type"] == "light"

def test_create_duplicate_device():
    # set up user, house, room
    user_payload = {
        "user_id": "dup-dev-owner",
        "name": "Dup Dev Owner",
        "email": "dup_dev@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user_payload)
    house_payload = {
        "house_id": "dup-dev-house",
        "address": "Dup Dev St",
        "owner": user_payload,
        "gps_location": [10.0, 10.0],
        "num_rooms": 1,
        "num_baths": 1
    }
    client.post("/houses", json=house_payload)
    room_payload = {
        "name": "Dup Dev Room",
        "floor": 1,
        "house": house_payload
    }
    client.post("/rooms", json=room_payload)

    device_payload = {
        "device_id": "dup-dev1",
        "type": "thermostat",
        "room": room_payload
    }
    # First creation => 201
    first = client.post("/devices", json=device_payload)
    assert first.status_code == 201

    # Duplicate creation => 409
    second = client.post("/devices", json=device_payload)
    assert second.status_code == 409

def test_update_nonexistent_device():
    dev_data = {
        "device_id": "ghost",
        "type": "camera",
        "room": {
            "name": "NoRoom",
            "floor": 1,
            "house": {
                "house_id": "NoHouse",
                "address": "No Address",
                "owner": {
                    "user_id": "NoUser",
                    "name": "Nobody",
                    "email": "nobody@example.com",
                    "privilege": "owner"
                },
                "gps_location": [0, 0],
                "num_rooms": 0,
                "num_baths": 0
            }
        }
    }
    resp = client.put("/devices/ghost", json=dev_data)
    assert resp.status_code == 404

def test_delete_device():
    # set up everything
    user = {
        "user_id": "del-dev-user",
        "name": "Del Dev",
        "email": "del@example.com",
        "privilege": "owner"
    }
    client.post("/users", json=user)

    house = {
        "house_id": "del-house",
        "address": "Del House Rd",
        "owner": user,
        "gps_location": [33, -80],
        "num_rooms": 1,
        "num_baths": 1
    }
    client.post("/houses", json=house)

    room = {
        "name": "Del Room",
        "floor": 1,
        "house": house
    }
    client.post("/rooms", json=room)

    device = {
        "device_id": "del-dev1",
        "type": "sensor",
        "room": room
    }
    client.post("/devices", json=device)

    # now delete it
    del_resp = client.delete("/devices/del-dev1")
    assert del_resp.status_code == 200

    # confirm it's gone
    gone_resp = client.get("/devices/del-dev1")
    assert gone_resp.status_code == 404