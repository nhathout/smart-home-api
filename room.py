from house import House
from typing import Optional

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

rooms_db = {}

class RoomNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

# C
def create_room(room: Room) -> Room:
    if room.name in rooms_db:
        raise ConflictError(f"Room '{room.name}' already exists")
    
    rooms_db[room.name] = room
    return room

# R
def get_room(room_name: str) -> Room:
    if room_name not in rooms_db:
        raise RoomNotFoundError(f"Room '{room_name}' not found")
    return rooms_db[room_name]

# U
def update_room(updated_room: Room) -> Room:
    if updated_room.name not in rooms_db:
        raise RoomNotFoundError(f"Room '{updated_room.name}' not found")
    
    rooms_db[updated_room.name] = updated_room
    return updated_room

# D
def delete_room(room_name: str) -> None:
    if room_name not in rooms_db:
        raise RoomNotFoundError(f"Room '{room_name}' not found")
    del rooms_db[room_name]