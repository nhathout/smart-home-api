import json
import os
from typing import Optional

from house import House
from user import User, PrivilegeLevel

ROOMS_JSON_FILE = "rooms.json"

class RoomNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

class Room:
    def __init__(self, name: str, floor: int, house: House):
        if not name.strip():
            raise ValidationError("Room name cannot be empty")
        
        if floor < 0:
            raise ValidationError("Floor cannot be negative")
            
        if not isinstance(house, House):
            raise ValidationError("Must provide valid House object")

        self.name = name
        self.floor = floor
        self.house = house

    def __eq__(self, other):
        return (
            self.name == other.name and 
            self.floor == other.floor and 
            self.house == other.house
        )

def load_rooms_from_json() -> dict:
    if not os.path.exists(ROOMS_JSON_FILE):
        return {}
    with open(ROOMS_JSON_FILE, "r") as f:
        return json.load(f)

def save_rooms_to_json(rooms_data: dict) -> None:
    with open(ROOMS_JSON_FILE, "w") as f:
        json.dump(rooms_data, f, indent=2)

def room_to_dict(room: Room) -> dict:
    return {
        "name": room.name,
        "floor": room.floor,
        "house": {
            "house_id": room.house.house_id,
            "address": room.house.address,
            "owner": {
                "user_id": room.house.owner.user_id,
                "name": room.house.owner.name,
                "email": room.house.owner.email,
                "privilege": room.house.owner.privilege.value
            },
            "gps_location": room.house.gps_location,
            "num_rooms": room.house.num_rooms,
            "num_baths": room.house.num_baths
        }
    }

def room_from_dict(data: dict) -> Room:
    house_data = data["house"]
    owner_data = house_data["owner"]

    owner_user = User(
        user_id=owner_data["user_id"],
        name=owner_data["name"],
        email=owner_data["email"],
        privilege=PrivilegeLevel(owner_data["privilege"])
    )
    house_obj = House(
        house_id=house_data["house_id"],
        address=house_data["address"],
        owner=owner_user,
        gps_location=tuple(house_data["gps_location"]),
        num_rooms=house_data["num_rooms"],
        num_baths=house_data["num_baths"]
    )
    return Room(
        name=data["name"],
        floor=data["floor"],
        house=house_obj
    )

# C
def create_room(room: Room) -> Room:
    rooms_data = load_rooms_from_json()

    if room.name in rooms_data:
        raise ConflictError(f"Room '{room.name}' already exists")

    rooms_data[room.name] = room_to_dict(room)
    save_rooms_to_json(rooms_data)
    return room

# R
def get_room(room_name: str) -> Room:
    rooms_data = load_rooms_from_json()

    if room_name not in rooms_data:
        raise RoomNotFoundError(f"Room '{room_name}' not found")
    
    return room_from_dict(rooms_data[room_name])

# U
def update_room(old_room: Room, new_room_name: str) -> Room:
    rooms_data = load_rooms_from_json()

    if old_room.name not in rooms_data:
        raise RoomNotFoundError(f"Room '{old_room.name}' not found")

    existing_room = room_from_dict(rooms_data[old_room.name])
    del rooms_data[old_room.name]

    existing_room.name = new_room_name

    rooms_data[new_room_name] = room_to_dict(existing_room)
    save_rooms_to_json(rooms_data)
    return existing_room

# D
def delete_room(room_name: str) -> None:
    rooms_data = load_rooms_from_json()

    if room_name not in rooms_data:
        raise RoomNotFoundError(f"Room '{room_name}' not found")
    
    del rooms_data[room_name]
    save_rooms_to_json(rooms_data)