import pytest
from user import User, PrivilegeLevel
from house import House, create_house, get_house, update_house, delete_house
from house import HouseNotFoundError, ValidationError, ConflictError

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

def test_invalid_gps():
    with pytest.raises(ValidationError):
        House(
            house_id="bad1",
            address="123 Test",
            owner=sample_owner(),
            gps_location=(100, 200),  # Invalid coordinates
            num_rooms=1,
            num_baths=1
        )

def test_negative_rooms_baths():
    with pytest.raises(ValidationError):
        House(
            house_id="bad2",
            address="123 Test",
            owner=sample_owner(),
            gps_location=(40, -74),
            num_rooms=-1,  # Invalid
            num_baths=1
        )
        
    with pytest.raises(ValidationError):
        House(
            house_id="bad3",
            address="123 Test",
            owner=sample_owner(),
            gps_location=(40, -74),
            num_rooms=1,
            num_baths=-1  # Invalid
        )

def test_duplicate_house_id(valid_house):
    create_house(valid_house)
    with pytest.raises(ConflictError):
        create_house(valid_house)

def test_update_nonexistent_house(valid_house):
    with pytest.raises(HouseNotFoundError):
        update_house(valid_house)

def test_delete_nonexistent_house():
    with pytest.raises(HouseNotFoundError):
        delete_house("non-existent-id")