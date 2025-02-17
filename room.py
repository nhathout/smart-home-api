from house import House

class Room:
    def __init__(self, name: str, floor: int, house: House): # can add type, size
        self.name = name
        self.floor = floor
        self.house = house

    # needed for testing
    def __eq__(self, other):
        return (
                self.name == other.name and 
                self.floor == other.floor and 
                self.house == other.house
                )

rooms_db = {} # to store all houses

class RoomNotFoundError(Exception):
    pass

## C R U D 
# Create
def create_room(room: Room) -> Room:
    rooms_db[room.name] = room
    return room

# Read/Get
def get_room(room_name: str) -> Room:
    if room_name not in rooms_db:
        raise RoomNotFoundError(f"Room {room_name} not found")
    return rooms_db[room_name]

# Update
def update_room(updated_room: Room) -> Room:
    if updated_room.name not in rooms_db:
        raise RoomNotFoundError(f"Room {updated_room.name} not found")
    
    rooms_db[updated_room.name] = updated_room
    return updated_room

# Delete
def delete_room(room_name: str) -> None:
    if room_name not in rooms_db:
        raise RoomNotFoundError(f"Room {room_name} not found")
    
    del rooms_db[room_name]