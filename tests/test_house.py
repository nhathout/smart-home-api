import pytest
from user import User, PrivilegeLevel
from house import House, create_house, get_house, update_house, delete_house
from house import HouseNotFoundError, ValidationError, ConflictError
import os

@pytest.fixture(autouse=True)
def clean_houses_file():
    if os.path.exists("houses.json"):
        os.remove("houses.json")
    yield

@pytest.fixture
def sample_owner():
    return User(
        user_id="owner123",
        name="Mo Salad",
        email="mosalad@example.com",
        privilege=PrivilegeLevel.OWNER
    )

@pytest.fixture
def valid_house(sample_owner):
    return House(
        house_id="house456",
        address="123 Pineapple Ave",
        owner=sample_owner,
        gps_location=(40.7128, -74.0060),
        num_rooms=3,
        num_baths=2
    )

def test_create_and_get_house(valid_house):
    create_house(valid_house)
    retrieved = get_house("house456")
    assert retrieved == valid_house

def test_invalid_gps(valid_house):
    with pytest.raises(ValidationError):
        House(
            house_id="bad1",
            address="123 Test",
            owner=valid_house.owner,
            gps_location=(100, 200),
            num_rooms=1,
            num_baths=1
        )

def test_negative_rooms_baths(valid_house):
    with pytest.raises(ValidationError):
        House(
            house_id="bad2",
            address="123 Test",
            owner=valid_house.owner,
            gps_location=(40, -74),
            num_rooms=-1,
            num_baths=1
        )
        
    with pytest.raises(ValidationError):
        House(
            house_id="bad3",
            address="123 Test",
            owner=valid_house.owner,
            gps_location=(40, -74),
            num_rooms=1,
            num_baths=-1
        )

def test_duplicate_house_id(valid_house):
    # First, create the original house
    create_house(valid_house)
    
    # Then create a new house with the same house_id => should conflict
    duplicate = House(
        house_id=valid_house.house_id,
        address="Different Address",
        owner=valid_house.owner,
        gps_location=(0, 0),
        num_rooms=0,
        num_baths=0
    )

    with pytest.raises(ConflictError):
        create_house(duplicate)


def test_update_nonexistent_house(sample_owner):
    house = House(
        house_id="never-added",
        address="123 Test",
        owner=sample_owner,
        gps_location=(0, 0),
        num_rooms=1,
        num_baths=1
    )
    
    with pytest.raises(HouseNotFoundError):
        update_house(house)

def test_delete_nonexistent_house():
    with pytest.raises(HouseNotFoundError):
        delete_house("non-existent-id")