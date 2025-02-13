import pytest
from user import User, PrivilegeLevel
from house import House
from room import Room
from device import Device, create_device, get_device, update_device, delete_device, DeviceNotFoundError

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

@pytest.fixture
def sample_device(sample_room):
    return Device(
        type="light",
        device_id="d1",
        room=sample_room
    )

def test_create_and_get_device(sample_device):
    create_device(sample_device)
    retrieved = get_device("d1")
    
    assert retrieved == sample_device
    assert retrieved.type == "light"
    assert retrieved.room.name == "Living Room"

def test_get_nonexistent_device():
    with pytest.raises(DeviceNotFoundError):
        get_device("non-existent-id")

def test_update_device_type(sample_device):
    create_device(sample_device)
    
    updated = Device(
        type="smart_light",
        device_id="d1",
        room=sample_device.room
    )
    
    update_device(updated)
    retrieved = get_device("d1")
    
    assert retrieved.type == "smart_light"
    assert retrieved.room.floor == 1  # Verify original room remains

def test_update_device_room(sample_room):
    new_room = Room(
        name="Bedroom",
        floor=2,
        house=sample_room.house
    )
    
    device = Device(
        type="thermostat",
        device_id="d2",
        room=sample_room
    )
    
    create_device(device)
    updated = Device(
        type="thermostat",
        device_id="d2",
        room=new_room
    )
    
    update_device(updated)
    retrieved = get_device("d2")
    
    assert retrieved.room.name == "Bedroom"
    assert retrieved.room.floor == 2

def test_update_nonexistent_device():
    fake_device = Device(
        type="camera",
        device_id="fake123",
        room=None
    )
    with pytest.raises(DeviceNotFoundError):
        update_device(fake_device)

def test_delete_device(sample_device):
    create_device(sample_device)
    delete_device("d1")
    
    with pytest.raises(DeviceNotFoundError):
        get_device("d1")

def test_delete_nonexistent_device():
    with pytest.raises(DeviceNotFoundError):
        delete_device("non-existent-id")