import json
import os
from enum import Enum
import re

USERS_JSON_FILE = "users.json"

# Load all users from the JSON file into a dict keyed by user_id.
# If the file doesn't exist or is empty, return an empty dict.
def load_users_from_json() -> dict:
    if not os.path.exists(USERS_JSON_FILE):
        return {}
    with open(USERS_JSON_FILE, "r") as f:
        return json.load(f)

# write given dictionary to the JSON file
def save_users_to_json(users_data: dict) -> None:
    with open(USERS_JSON_FILE, "w") as f:
        json.dump(users_data, f, indent=2)

class PrivilegeLevel(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    RESIDENT = "resident"

class User:
    def __init__(self, user_id: str, name: str, email: str, privilege: PrivilegeLevel):
        if len(name) < 1 or len(name) > 50:
            raise ValidationError("Name must be 1-50 characters")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email format")
        
        if not isinstance(privilege, PrivilegeLevel):
            raise ValidationError("Invalid privilege type")

        self.user_id = user_id
        self.name = name
        self.email = email
        self.privilege = privilege

    def __eq__(self, other):
        return (
            self.user_id == other.user_id and 
            self.name == other.name and 
            self.email == other.email and 
            self.privilege == other.privilege
        )

class APIError(Exception):
    """Base class for API exceptions"""
    pass

class ValidationError(APIError):
    pass

class NotFoundError(APIError):
    pass

class ConflictError(APIError):
    pass

# input validation helper functions
def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email format")

def validate_privilege(privilege: PrivilegeLevel):
    if privilege not in PrivilegeLevel:
        raise ValidationError(f"Invalid privilege level: {privilege}")

## C R U D
# Create
def create_user(user: User) -> User:
    users_data = load_users_from_json()

    # check conflict
    if user.user_id in users_data:
        raise ConflictError(f"User ID {user.user_id} exists")
    
    # convert User object to a dict
    users_data[user.user_id] = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "privilege": user.privilege.value  # store enum as string
    }

    save_users_to_json(users_data)
    return user

# Read
def get_user(user_id: str) -> User:
    users_data = load_users_from_json()

    if user_id not in users_data:
        raise NotFoundError(f"User {user_id} not found")

    # get dict for that user_id
    user_dict = users_data[user_id]
    return User(
        user_id=user_dict["user_id"],
        name=user_dict["name"],
        email=user_dict["email"],
        privilege=PrivilegeLevel(user_dict["privilege"])  # convert back to enum
    )

# Update
def update_user(updated_user: User) -> User:
    users_data = load_users_from_json()

    if updated_user.user_id not in users_data:
        raise NotFoundError(f"User {updated_user.user_id} not found")
    
    # validate updated data
    validate_email(updated_user.email)
    validate_privilege(updated_user.privilege)

    # replace the entry in the JSON dictionary
    users_data[updated_user.user_id] = {
        "user_id": updated_user.user_id,
        "name": updated_user.name,
        "email": updated_user.email,
        "privilege": updated_user.privilege.value
    }

    save_users_to_json(users_data)
    return updated_user

# Delete
def delete_user(user_id: str) -> None:
    users_data = load_users_from_json()

    if user_id not in users_data:
        raise NotFoundError(f"User {user_id} not found")
    
    del users_data[user_id]
    save_users_to_json(users_data)