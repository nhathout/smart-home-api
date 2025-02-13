class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    # needed for testing
    def __eq__(self, other):
        return (self.user_id == other.user_id and self.name == other.name and self.email == other.email)

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
        raise UserNotFoundError(f"User {update_user.user_id} not found")
    
    users_db[update_user.user_id] = updated_user
    return updated_user

# Delete
def delete_user(user_id: str) -> None:
    if user_id not in users_db:
        raise UserNotFoundError(f"User {update_user.user_id} not found")
    
    del users_db[user_id]