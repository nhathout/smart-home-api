import pytest
from user import (
    User, PrivilegeLevel, 
    create_user, get_user, update_user, delete_user,
    ValidationError, NotFoundError, ConflictError
)

@pytest.fixture
def valid_user():
    return User(
        user_id="u1",
        name="Nawa Hathout",
        email="valid@example.com",
        privilege=PrivilegeLevel.OWNER
    )

def test_successful_lifecycle(valid_user):
    # Test create
    created = create_user(valid_user)
    assert created == valid_user
    
    # Test get
    retrieved = get_user("u1")
    assert retrieved.email == "valid@example.com"
    
    # Test update
    updated = User(
        user_id="u1",
        name="Updated Name",
        email="new@example.com",
        privilege=PrivilegeLevel.ADMIN
    )
    update_user(updated)
    assert get_user("u1").name == "Updated Name"
    
    # Test delete
    delete_user("u1")
    with pytest.raises(NotFoundError):
        get_user("u1")

def test_invalid_emails():
    with pytest.raises(ValidationError):
        User("u2", "Bad Email", "invalid-email", PrivilegeLevel.OWNER)
        
def test_duplicate_user_id(valid_user):
    create_user(valid_user)
    with pytest.raises(ConflictError):
        create_user(valid_user)

def test_invalid_privilege():
    with pytest.raises(ValidationError):
        User("u3", "Test", "test@example.com", "invalid_privilege")

def test_name_length_validation():
    with pytest.raises(ValidationError):
        User("u4", "", "test@example.com", PrivilegeLevel.RESIDENT)

    with pytest.raises(ValidationError):
        User("u5", "A" * 51, "test@example.com", PrivilegeLevel.RESIDENT)

def test_nonexistent_user_operations():
    with pytest.raises(NotFoundError):
        get_user("non-existent")
    with pytest.raises(NotFoundError):
        update_user(User("non-existent", "Test", "test@example.com", PrivilegeLevel.OWNER))
    with pytest.raises(NotFoundError):
        delete_user("non-existent")

def test_create_user_duplicate_id():
    user = User("u6", "Valid", "valid@test.com", PrivilegeLevel.OWNER)
    create_user(user)
    
    with pytest.raises(ConflictError):
        create_user(user)