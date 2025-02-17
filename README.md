# Smart Home API Core

This repository provides a *Python-based* Smart Home API that manages **Users**, **Houses**, **Rooms**, and **Devices**. The primary focus is on **API design** and **robust error handling** &mdash; particularly **input validation**. The project also includes thorough **unit tests** to demonstrate proper functionality for successful operations as well as error cases.

---

## Overview
The **Smart Home API** is a collection of Python modules that implement the following:

- **Data Models & Classes**: Definitions of `User`, `House`, `Room`, and `Device` objects.  
- **CRUD Operations**: `Create`, `Read`, `Update`, `Delete` functions for each data model.  
- **Validation & Error Handling**: Ensures data integrity and proper exception raising.  
- **In-Memory Storage**: For demonstration, data is stored in simple dictionaries (e.g., `users_db`, `houses_db`, etc.)—no external database is used.  

We do *not* hook these modules up to external data sources or actual hardware; the emphasis is on **designing the APIs** and **demonstrating error handling** through function-level calls and unit tests.

---

## API Modules & Data Structures

### Users
- **Data Structure**:  
  Each `User` is stored in the in-memory dictionary `users_db`, keyed by `user_id`.  

- **Fields**:
  - `user_id: str`  
  - `name: str` (1–50 characters)  
  - `email: str` (must be valid format)  
  - `privilege: PrivilegeLevel` (Enum: `OWNER`, `ADMIN`, `RESIDENT`)  

- **API**:
  1. `create_user(user: User) -> User`:  
     - Creates a new user.  
     - Raises `ConflictError` if `user_id` already exists.  
     - Raises `ValidationError` if data fails validation.  
  2. `get_user(user_id: str) -> User`:  
     - Retrieves an existing user by ID.  
     - Raises `NotFoundError` if not found.  
  3. `update_user(updated_user: User) -> User`:  
     - Updates an existing user.  
     - Raises `NotFoundError` if the ID does not exist.  
     - Raises `ValidationError` if data is invalid.  
  4. `delete_user(user_id: str) -> None`:  
     - Deletes an existing user by ID.  
     - Raises `NotFoundError` if not found.  

### Houses
- **Data Structure**:  
  Each `House` is stored in the `houses_db` dictionary, keyed by `house_id`.

- **Fields**:
  - `house_id: str`  
  - `address: str`  
  - `owner: User` (should be `PrivilegeLevel.OWNER`)  
  - `gps_location: tuple[float, float]`  
  - `num_rooms: int`  
  - `num_baths: int`  

- **API**:
  1. `create_house(house: House) -> House`:  
     - Creates a new house entry.  
  2. `get_house(house_id: str) -> House`:  
     - Retrieves a house by its ID.  
     - Raises `HouseNotFoundError` if not found.  
  3. `update_house(updated_house: House) -> House`:  
     - Updates house information.  
     - Raises `HouseNotFoundError` if not found.  
  4. `delete_house(house_id: str) -> None`:  
     - Deletes a house by its ID.  
     - Raises `HouseNotFoundError` if not found.  

### Rooms
- **Data Structure**:  
  Each `Room` is stored in `rooms_db`, keyed by the room’s `name`.

- **Fields**:
  - `name: str`  
  - `floor: int`  
  - `house: House`  

- **API**:
  1. `create_room(room: Room) -> Room`:  
     - Creates a new room entry.  
  2. `get_room(room_name: str) -> Room`:  
     - Retrieves a room by its name.  
     - Raises `RoomNotFoundError` if not found.  
  3. `update_room(updated_room: Room) -> Room`:  
     - Updates room details.  
     - Raises `RoomNotFoundError` if not found.  
  4. `delete_room(room_name: str) -> None`:  
     - Deletes a room by name.  
     - Raises `RoomNotFoundError` if not found.  

### Devices
- **Data Structure**:  
  Each `Device` is stored in `devices_db`, keyed by `device_id`.

- **Fields**:
  - `type: DeviceType` (Enum: `LIGHT`, `THERMOSTAT`, `CAMERA`, `LOCK`, `SENSOR`)  
  - `device_id: str` (non-empty)  
  - `room: Room`  

- **API**:
  1. `create_device(device: Device) -> Device`:  
     - Creates a new device entry.  
     - Raises `ConflictError` if `device_id` already exists.  
     - Raises `ValidationError` if device type or ID is invalid.  
  2. `get_device(device_id: str) -> Device`:  
     - Retrieves a device by its ID.  
     - Raises `DeviceNotFoundError` if not found.  
  3. `update_device(updated_device: Device) -> Device`:  
     - Updates existing device details.  
     - Raises `DeviceNotFoundError` if not found.  
  4. `delete_device(device_id: str) -> None`:  
     - Deletes a device by its ID.  
     - Raises `DeviceNotFoundError` if not found.  

---

## Error Handling & Validation
We focus heavily on **error handling** and **input validation**:

- **ValidationError**: Raised if data (e.g., email format, name length, or device ID) is invalid.  
- **NotFoundError** / Custom “NotFoundError”-like classes: Raised when a requested resource does not exist (`HouseNotFoundError`, `RoomNotFoundError`, `DeviceNotFoundError`, etc.).  
- **ConflictError**: Raised when creating a resource with an existing unique ID.  

Each module’s CRUD functions contain the logic to *validate inputs* and raise appropriate exceptions to *signal error states* back to the caller.

---

## Unit Tests
Unit tests (written with **pytest**) verify both **happy-path** (valid) scenarios and various **error scenarios** (invalid inputs, non-existent resources, conflicts). Each module has a corresponding test file:

- **`test_user.py`**: Verifies user creation, retrieval, updates, and deletions, plus invalid data checks.  
- **`test_house.py`**: Validates house CRUD and ensures `HouseNotFoundError` is raised as needed.  
- **`test_room.py`**: Covers rooms with proper references to houses.  
- **`test_device.py`**: Ensures device type, IDs, and references to rooms are validated.  
