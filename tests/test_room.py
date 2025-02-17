import pytest
from user import User, PrivilegeLevel
from house import House
from room import Room, create_room, get_room, update_room, delete_room, RoomNotFoundError

# chat-aided test file
@pytest.fixture
def sample_owner():
    return User(
        user_id="owner123",
        name="Mo Salad",
        email="mosalad@example.com",
        privilege=PrivilegeLevel.OWNER
    )

@pytest.fixture
def sample_house(sample_owner):
    return House(
        house_id="house456",
        address="123 Pineapple Ave",
        owner=sample_owner,
        gps_location=(40.7128, -74.0060),
        num_rooms=3,
        num_baths=2
    )

@pytest.fixture
def sample_room(sample_house):
    return Room(
        name="Living Room",
        floor=1,
        house=sample_house
    )

def test_create_and_get_room(sample_room):
    create_room(sample_room)
    retrieved = get_room("Living Room")
    
    assert retrieved == sample_room
    assert retrieved.floor == 1
    assert retrieved.house.house_id == "house456"

def test_get_nonexistent_room():
    with pytest.raises(RoomNotFoundError):
        get_room("Non-existent Room")

def test_update_room(sample_house, sample_room):
    create_room(sample_room)
    
    updated_room = Room(
        name="Living Room",  # Same name required for update
        floor=2,  # Changed floor
        house=sample_house
    )
    
    update_room(updated_room)
    retrieved = get_room("Living Room")
    
    assert retrieved.floor == 2
    assert retrieved.house.address == "123 Pineapple Ave"

def test_update_nonexistent_room(sample_house):
    new_room = Room(
        name="Bedroom",
        floor=1,
        house=sample_house
    )
    with pytest.raises(RoomNotFoundError):
        update_room(new_room)  # Never created

def test_delete_room(sample_room):
    create_room(sample_room)
    delete_room("Living Room")
    
    with pytest.raises(RoomNotFoundError):
        get_room("Living Room")

def test_delete_nonexistent_room():
    with pytest.raises(RoomNotFoundError):
        delete_room("Non-existent Room")