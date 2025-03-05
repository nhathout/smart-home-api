# Smart Home API Core

This repository provides a *Python-based* Smart Home API that manages **Users**, **Houses**, **Rooms**, and **Devices**. The primary focus is on **API design** and **robust error handling** &mdash; particularly **input validation**. The project also includes thorough **unit tests** to demonstrate proper functionality for successful operations as well as error cases.

---

## Overview
Initially, this API used **in-memory dictionaries** (`users_db`, `houses_db`, etc.) for demonstration. **Now**, I store all data in **JSON files** (e.g., `users.json`, `houses.json`, etc.). Each CRUD operation loads the JSON, modifies it in memory, and saves it back. No external databases or hardware connections are used.

Key focuses include:
- **Data Models & Classes**: `User`, `House`, `Room`, `Device`.  
- **CRUD Operations**: `Create`, `Read`, `Update`, `Delete` per model.  
- **Validation & Error Handling**: Properly raising exceptions when inputs are invalid.  
- **JSON Storage**: Data is now persisted across runs, unless you delete the JSON files.

---

## FastAPI Implementation

All the core domain logic (CRUD operations, validation, etc.) has been wrapped with FastAPI endpoints in **`main.py`**. You can run the API server locally with:

```uvicorn main:app --reload```<br>

This will launch the FastAPI app at ```http://127.0.0.1:8000```.<br>
- Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the interactive API documentation.

There, you’ll find automatically generated documentation for **Users**, **Houses**, **Rooms**, and **Devices** endpoints, supporting all CRUD operations.

The ```test_api.py``` file contains integration tests for these routes, using ```fastapi.testclient.TestClient```.

---

## API Modules & Data Structures

### Users
- **JSON File**: `users.json`  
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
- **JSON File**: `houses.json`  
- **Fields**:
  - `house_id: str`  
  - `address: str`  
  - `owner: User`  
  - `gps_location: tuple[float, float]`  
  - `num_rooms: int`  
  - `num_baths: int`  

- **API**:
  1. `create_house(house: House) -> House`:  
     - Creates a new house entry.  
     - Raises `ConflictError` if `house_id` already exists.  
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
- **JSON File**: `rooms.json`  
- **Fields**:
  - `name: str`  
  - `floor: int`  
  - `house: House`  

- **API**:
  1. `create_room(room: Room) -> Room`:  
     - Creates a new room entry.  
     - Raises `ConflictError` if the room name already exists.  
  2. `get_room(room_name: str) -> Room`:  
     - Retrieves a room by its name.  
     - Raises `RoomNotFoundError` if not found.  
  3. `update_room(old_room: Room, new_room_name: str) -> Room`:  
     - Renames or otherwise updates a room’s name.  
     - Raises `RoomNotFoundError` if not found.  
  4. `delete_room(room_name: str) -> None`:  
     - Deletes a room by name.  
     - Raises `RoomNotFoundError` if not found.  

### Devices
- **JSON File**: `devices.json`  
- **Fields**:
  - `type: DeviceType` (Enum: `LIGHT`, `THERMOSTAT`, `CAMERA`, `LOCK`, `SENSOR`)  
  - `device_id: str` (non-empty)  
  - `room: Room`  

- **API**:
  1. `create_device(device: Device) -> Device`:  
     - Creates a new device entry.  
     - Raises `ConflictError` if `device_id` already exists.  
     - Raises `ValidationError` if data (type or ID) is invalid.  
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
I focus heavily on **error handling** and **input validation**:

- **ValidationError**: Raised if data (e.g., email format, room name, device ID) is invalid.  
- **NotFoundError** / module-specific “NotFoundError” classes: e.g., `HouseNotFoundError`, `RoomNotFoundError`, `DeviceNotFoundError`. Raised when a requested resource doesn’t exist in the JSON file.  
- **ConflictError**: Raised when creating a resource with an existing unique ID or name.  

Each module’s CRUD function loads data from its JSON, checks for conflicts or invalid data, raises exceptions if needed, and writes changes back to JSON on success.

---

## Unit & Integration Tests
Unit tests (written with **pytest**) verify both **happy-path** (valid) scenarios and various **error scenarios** (invalid inputs, non-existent resources, conflicts). Each module has a corresponding test file:

- **`test_user.py`**: Verifies user creation, retrieval, updates, and deletions, plus invalid data checks.  
- **`test_house.py`**: Validates house CRUD and ensures `HouseNotFoundError` is raised as needed.  
- **`test_room.py`**: Covers rooms with proper references to houses.  
- **`test_device.py`**: Ensures device type, IDs, and references to rooms are validated.  

**(NEW) Intefration Tests**
- Use ```fastapi.testclient.TestClient``` to send real HTTP requests to the in-memory FastAPI app.
- Validate the endpoints (```/users```, ```/houses```, ```/rooms```, ```/devices```) behave as expected, including error cases.

> **Important**: Because JSON files persist data across tests, any test that expects an empty store at the start may remove or reset the corresponding `.json` file before running. Alternatively, each test that requires data can explicitly create it first so the test remains self-contained.

---

## GitHub Actions & Coverage
I use **GitHub Actions** to:
- **Run tests** automatically on every push/pull request  
- **Generate coverage reports**  

You can view test results and coverage details under your repository’s Actions tab.
