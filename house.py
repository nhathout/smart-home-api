from user import User
from typing import Tuple

class House:
    def __init__(self, house_id: str, address: str, owner: User, 
                 gps_location: Tuple[float, float], num_rooms: int, num_baths: int):

        if not isinstance(owner, User):
            raise ValidationError("Owner must be a valid User")
            
        if not (-90 <= gps_location[0] <= 90) or not (-180 <= gps_location[1] <= 180):
            raise ValidationError("Invalid GPS coordinates")
            
        if num_rooms < 0 or num_baths < 0:
            raise ValidationError("Room and bath counts must be non-negative")
            
        self.house_id = house_id
        self.address = address
        self.owner = owner
        self.gps_location = gps_location
        self.num_rooms = num_rooms
        self.num_baths = num_baths

    def __eq__(self, other):
        return (self.house_id == other.house_id and 
                self.address == other.address and 
                self.owner == other.owner and 
                self.gps_location == other.gps_location and
                self.num_rooms == other.num_rooms and 
                self.num_baths == other.num_baths)

houses_db = {}

class HouseNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

# C
def create_house(house: House) -> House:
    if house.house_id in houses_db:
        raise ConflictError(f"House ID {house.house_id} already exists")
        
    houses_db[house.house_id] = house
    return house

# R
def get_house(house_id: str) -> House:
    if house_id not in houses_db:
        raise HouseNotFoundError(f"House {house_id} not found")
    return houses_db[house_id]

# U
def update_house(updated_house: House) -> House:
    if updated_house.house_id not in houses_db:
        raise HouseNotFoundError(f"House {updated_house.house_id} not found")
    
    houses_db[updated_house.house_id] = updated_house
    return updated_house

# D
def delete_house(house_id: str) -> None:
    if house_id not in houses_db:
        raise HouseNotFoundError(f"House {house_id} not found")
    del houses_db[house_id]