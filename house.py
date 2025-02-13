from user import User

class House:
    def __init__(self, house_id: str, address: str, owner: User, gps_location: tuple[float, float], num_rooms: int, num_baths: int):
        self.house_id = house_id
        self.address = address
        self.owner = owner
        self.gps_location = gps_location
        self.num_rooms = num_rooms
        self.num_baths = num_baths

    # needed for testing
    def __eq__(self, other):
        return (self.house_id == other.house_id and 
                self.address == other.address and 
                self.owner == other.owner and 
                self.gps_location == other.gps_location and
                self.num_rooms == other.num_rooms and 
                self.num_baths == other.num_baths
                )

houses_db = {} # to store all houses

class HouseNotFoundError(Exception):
    pass

## C R U D 
# Create
def create_house(house: House) -> House:
    houses_db[house.house_id] = house
    return house

# Read/Get
def get_house(house_id: str) -> House:
    if house_id not in houses_db:
        raise HouseNotFoundError(f"House {house_id} not found")
    return houses_db[house_id]

# Update
def updated_house(updated_house: House) -> House:
    if updated_house.house_id not in houses_db:
        raise HouseNotFoundError(f"House {updated_house.house_id} not found")
    
    houses_db[updated_house.house_id] = updated_house
    return updated_house

# Delete
def delete_house(house_id: str) -> None:
    if house_id not in houses_db:
        raise HouseNotFoundError(f"House {house_id} not found")
    
    del houses_db[house_id]