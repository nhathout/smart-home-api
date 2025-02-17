from enum import Enum
import re

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

users_db = {}

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
    if user.user_id in users_db:
        raise ConflictError(f"User ID {user.user_id} exists")
    
    users_db[user.user_id] = user
    return user

# Read
def get_user(user_id: str) -> User:
    if user_id not in users_db:
        raise NotFoundError(f"User {user_id} not found")
    return users_db[user_id]

# Update
def update_user(updated_user: User) -> User:
    if updated_user.user_id not in users_db:
        raise NotFoundError(f"User {updated_user.user_id} not found")
    
    # Validate updated data
    validate_email(updated_user.email)
    validate_privilege(updated_user.privilege)
    
    users_db[updated_user.user_id] = updated_user
    return updated_user

# Delete
def delete_user(user_id: str) -> None:
    if user_id not in users_db:
        raise NotFoundError(f"User {user_id} not found")
    del users_db[user_id]