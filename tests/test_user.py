import pytest
from user import User, create_user, get_user, update_user, delete_user, UserNotFoundError

def test_full_user_lifecycle():
    # Create
    user = User("1", "nhathout", "nhathout@example.com")
    create_user(user)
    assert get_user("1") == user

    # Update
    updated_user = User("1", "nawahathout", "nawa.hathout@example.com")
    update_user(updated_user)
    assert get_user("1").name == "Noah Hathout"

    # Delete
    delete_user("1")
    with pytest.raises(UserNotFoundError):
        get_user("1")