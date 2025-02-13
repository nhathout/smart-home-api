from enum import Enum

class PrivilegeLevel(Enum):
    OWNER = "owner"
    ADMIN = "admin"  
    DEV = "dev"      
    REALTOR = "realtor"
    RESIDENT = "resident" 

class User:
    def __init__(self, user_id: str, name: str, email: str, privilege: PrivilegeLevel):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.privilege = privilege

    # needed for testing
    def __eq__(self, other):
        return (
                self.user_id == other.user_id and 
                self.name == other.name and 
                self.email == other.email and 
                self.privilege == other.privilege
                )

users_db = {} # to store all users

class UserNotFoundError(Exception):
    pass

## C R U D 
# Create
def create_user(user: User) -> User:
    users_db[user.user_id] = user
    return user

# Read/Get
def get_user(user_id: str) -> User:
    if user_id not in users_db:
        raise UserNotFoundError(f"User {user_id} not found")
    return users_db[user_id]

# Update
def update_user(updated_user: User) -> User:
    if update_user.user_id not in users_db:
        raise UserNotFoundError(f"User {updated_user.user_id} not found")
    
    users_db[update_user.user_id] = updated_user
    return updated_user

# Delete
def delete_user(user_id: str) -> None:
    if user_id not in users_db:
        raise UserNotFoundError(f"User {user_id} not found")
    
    del users_db[user_id]