import pytest
from user import User, PrivilegeLevel, create_user, get_user, update_user, delete_user, UserNotFoundError

@pytest.fixture
def sample_user():
    return User(
        user_id="1",
        name="nhathout",
        email="nhathout@example.com",
        privilege=PrivilegeLevel.OWNER
    )

def test_full_user_lifecycle(sample_user):
    # Test create
    create_user(sample_user)
    assert get_user("1") == sample_user

    # Test update
    updated_user = User(
        user_id="1",
        name="nawahathout",
        email="nawa.hathout@example.com",
        privilege=PrivilegeLevel.ADMIN
    )
    update_user(updated_user)
    retrieved = get_user("1")
    assert retrieved.name == "nawahathout"
    assert retrieved.privilege == PrivilegeLevel.ADMIN

    # Test delete
    delete_user("1")
    with pytest.raises(UserNotFoundError):
        get_user("1")

def test_create_invalid_user():
    with pytest.raises(TypeError):
        # Missing privilege parameter
        User("2", "baduser", "bad@example.com")

def test_get_nonexistent_user():
    with pytest.raises(UserNotFoundError):
        get_user("non-existent-id")