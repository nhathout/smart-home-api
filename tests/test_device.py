import pytest
from user import User, PrivilegeLevel
from house import House
from room import Room
from device import Device, DeviceType, create_device, get_device, update_device, delete_device
from device import DeviceNotFoundError, ValidationError, ConflictError

@pytest.fixture
def valid_room():
    owner = User("owner123", "Mo Salad", "mosalad@example.com", PrivilegeLevel.OWNER)
    house = House(
        house_id="house456",
        address="123 Pineapple Ave",
        owner=owner,
        gps_location=(40.7128, -74.0060),
        num_rooms=3,
        num_baths=2
    )
    return Room("Living Room", 1, house)

@pytest.fixture
def valid_device(valid_room):
    return Device(
        type=DeviceType.LIGHT,
        device_id="d1",
        room=valid_room
    )

def test_valid_device_creation(valid_device):
    created = create_device(valid_device)
    assert created == valid_device

def test_invalid_device_type(valid_room):
    with pytest.raises(ValidationError):
        Device("invalid_type", "d2", valid_room)

def test_empty_device_id(valid_room):
    with pytest.raises(ValidationError):
        Device(DeviceType.LOCK, "", valid_room)

def test_invalid_room_type():
    with pytest.raises(ValidationError):
        Device(DeviceType.CAMERA, "d3", "not-a-room")

def test_duplicate_device_id(valid_device):
    duplicate = Device(
        type=DeviceType.THERMOSTAT,
        device_id=valid_device.device_id,
        room=valid_device.room
    )
    
    create_device(valid_device)
    with pytest.raises(ConflictError):
        create_device(duplicate)

def test_update_validation(valid_device):
    create_device(valid_device)
    
    with pytest.raises(ValidationError):
        updated = Device(
            type="invalid_type",
            device_id=valid_device.device_id,
            room=valid_device.room
        )
        update_device(updated)

def test_nonexistent_operations():
    with pytest.raises(DeviceNotFoundError):
        get_device("ghost-device")
    with pytest.raises(DeviceNotFoundError):
        delete_device("ghost-device")