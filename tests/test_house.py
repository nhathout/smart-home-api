import pytest
from user import User, PrivilegeLevel
from house import House, create_house, get_house, update_house, delete_house, HouseNotFoundError

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
        gps_location=(40.7128, -74.0060),  # NYC coordinates
        num_rooms=3,
        num_baths=2
    )

def test_create_and_get_house(sample_house):
    create_house(sample_house)
    retrieved = get_house("house456")
    
    assert retrieved == sample_house
    assert retrieved.address == "123 Pineapple Ave"
    assert retrieved.owner.privilege == PrivilegeLevel.OWNER

def test_get_nonexistent_house():
    with pytest.raises(HouseNotFoundError):
        get_house("non-existent-id")

def test_update_house(sample_owner, sample_house):

    create_house(sample_house)
    
    # create updated version
    updated_house = House(
        house_id="house456",  # Same ID
        address="456 Updated Address Road",
        owner=sample_owner,
        gps_location=(34.0522, -118.2437),  # LA coordinates
        num_rooms=4,
        num_baths=3
    )
    
    update_house(updated_house)
    retrieved = get_house("house456")
    
    assert retrieved.num_rooms == 4
    assert retrieved.num_baths == 3
    assert retrieved.gps_location == (34.0522, -118.2437)

def test_update_nonexistent_house(sample_house):
    with pytest.raises(HouseNotFoundError):
        update_house(sample_house)  # house was never created

def test_delete_house(sample_house):
    create_house(sample_house)
    delete_house("house456")
    
    with pytest.raises(HouseNotFoundError):
        get_house("house456")

def test_delete_nonexistent_house():
    with pytest.raises(HouseNotFoundError):
        delete_house("non-existent-id")