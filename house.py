import json
import os
from typing import Tuple
from user import User, PrivilegeLevel, ValidationError as UserValidationError

HOUSES_JSON_FILE = "houses.json"

class HouseNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

class House:
    def __init__(
        self,
        house_id: str,
        address: str,
        owner: User,
        gps_location: Tuple[float, float],
        num_rooms: int,
        num_baths: int
    ):
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
        return (
            self.house_id == other.house_id and 
            self.address == other.address and 
            self.owner == other.owner and 
            self.gps_location == other.gps_location and
            self.num_rooms == other.num_rooms and 
            self.num_baths == other.num_baths
        )

def load_houses_from_json() -> dict:
    if not os.path.exists(HOUSES_JSON_FILE):
        return {}
    with open(HOUSES_JSON_FILE, "r") as f:
        return json.load(f)

def save_houses_to_json(houses_data: dict) -> None:
    with open(HOUSES_JSON_FILE, "w") as f:
        json.dump(houses_data, f, indent=2)

def house_to_dict(house: House) -> dict:
    return {
        "house_id": house.house_id,
        "address": house.address,
        "owner": {
            "user_id": house.owner.user_id,
            "name": house.owner.name,
            "email": house.owner.email,
            "privilege": house.owner.privilege.value
        },
        "gps_location": house.gps_location,
        "num_rooms": house.num_rooms,
        "num_baths": house.num_baths
    }

def house_from_dict(data: dict) -> House:
    owner_data = data["owner"]
    owner = User(
        user_id=owner_data["user_id"],
        name=owner_data["name"],
        email=owner_data["email"],
        privilege=PrivilegeLevel(owner_data["privilege"])
    )

    return House(
        house_id=data["house_id"],
        address=data["address"],
        owner=owner,
        gps_location=tuple(data["gps_location"]),
        num_rooms=data["num_rooms"],
        num_baths=data["num_baths"]
    )

# C
def create_house(house: House) -> House:
    houses_data = load_houses_from_json()
    
    if house.house_id in houses_data:
        raise ConflictError(f"House ID {house.house_id} already exists")
    
    houses_data[house.house_id] = house_to_dict(house)
    save_houses_to_json(houses_data)
    return house

# R
def get_house(house_id: str) -> House:
    houses_data = load_houses_from_json()
    
    if house_id not in houses_data:
        raise HouseNotFoundError(f"House {house_id} not found")
    
    return house_from_dict(houses_data[house_id])

# U
def update_house(updated_house: House) -> House:
    houses_data = load_houses_from_json()
    
    if updated_house.house_id not in houses_data:
        raise HouseNotFoundError(f"House {updated_house.house_id} not found")
    
    houses_data[updated_house.house_id] = house_to_dict(updated_house)
    save_houses_to_json(houses_data)
    return updated_house

# D
def delete_house(house_id: str) -> None:
    houses_data = load_houses_from_json()
    
    if house_id not in houses_data:
        raise HouseNotFoundError(f"House {house_id} not found")
    
    del houses_data[house_id]
    save_houses_to_json(houses_data)
