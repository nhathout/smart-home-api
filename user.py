import json
import os
from enum import Enum
import re

USERS_JSON_FILE = "users.json"

def load_users_from_json() -> dict:
    if not os.path.exists(USERS_JSON_FILE):
        return {}
    with open(USERS_JSON_FILE, "r") as f:
        return json.load(f)

def save_users_to_json(users_data: dict) -> None:
    with open(USERS_JSON_FILE, "w") as f:
        json.dump(users_data, f, indent=2)

class PrivilegeLevel(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    RESIDENT = "resident"

class APIError(Exception):
    """Base class for API exceptions"""
    pass

class ValidationError(APIError):
    pass

class NotFoundError(APIError):
    pass

class ConflictError(APIError):
    pass

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

# input validation helper functions
def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email format")

def validate_privilege(privilege: PrivilegeLevel):
    if privilege not in PrivilegeLevel:
        raise ValidationError(f"Invalid privilege level: {privilege}")


# ========== CRUD OPERATIONS ==========

# C
def create_user(user: User) -> User:
    users_data = load_users_from_json()
    if user.user_id in users_data:
        raise ConflictError(f"User ID {user.user_id} exists")
    
    users_data[user.user_id] = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "privilege": user.privilege.value
    }
    save_users_to_json(users_data)
    return user

# R
def get_user(user_id: str) -> User:
    users_data = load_users_from_json()
    if user_id not in users_data:
        raise NotFoundError(f"User {user_id} not found")

    user_dict = users_data[user_id]
    return User(
        user_id=user_dict["user_id"],
        name=user_dict["name"],
        email=user_dict["email"],
        privilege=PrivilegeLevel(user_dict["privilege"])
    )

def get_all_users() -> list[User]:
    """
    Retrieve all users from the JSON store.
    """
    users_data = load_users_from_json()
    user_list = []
    for user_id, user_dict in users_data.items():
        user_obj = User(
            user_id=user_dict["user_id"],
            name=user_dict["name"],
            email=user_dict["email"],
            privilege=PrivilegeLevel(user_dict["privilege"])
        )
        user_list.append(user_obj)
    return user_list

# U
def update_user(updated_user: User) -> User:
    users_data = load_users_from_json()
    if updated_user.user_id not in users_data:
        raise NotFoundError(f"User {updated_user.user_id} not found")
    
    validate_email(updated_user.email)
    validate_privilege(updated_user.privilege)

    users_data[updated_user.user_id] = {
        "user_id": updated_user.user_id,
        "name": updated_user.name,
        "email": updated_user.email,
        "privilege": updated_user.privilege.value
    }
    save_users_to_json(users_data)
    return updated_user

# D
def delete_user(user_id: str) -> None:
    users_data = load_users_from_json()
    if user_id not in users_data:
        raise NotFoundError(f"User {user_id} not found")
    
    del users_data[user_id]
    save_users_to_json(users_data)