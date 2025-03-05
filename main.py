# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel, EmailStr

from user import (
    User as UserDomain, PrivilegeLevel, ValidationError as UserValidationError,
    NotFoundError as UserNotFoundError, ConflictError as UserConflictError,
    create_user, get_user, get_all_users, update_user, delete_user
)
from house import (
    House as HouseDomain, HouseNotFoundError, ValidationError as HouseValidationError,
    ConflictError as HouseConflictError, create_house, get_house,
    get_all_houses, update_house, delete_house
)
from room import (
    Room as RoomDomain, RoomNotFoundError, ValidationError as RoomValidationError,
    ConflictError as RoomConflictError, create_room, get_room,
    get_all_rooms, update_room, delete_room
)
from device import (
    Device as DeviceDomain, DeviceType, DeviceNotFoundError,
    ValidationError as DeviceValidationError, ConflictError as DeviceConflictError,
    create_device, get_device, get_all_devices, update_device, delete_device
)

app = FastAPI(
    title="Smart Home API",
    description="CRUD operations for Users, Houses, Rooms, and Devices",
    version="1.0.0",
)

# --------------------------
# Pydantic Schemas
# --------------------------
class UserSchema(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    privilege: str

class HouseSchema(BaseModel):
    house_id: str
    address: str
    owner: UserSchema
    gps_location: tuple[float, float]
    num_rooms: int
    num_baths: int

class RoomSchema(BaseModel):
    name: str
    floor: int
    house: HouseSchema

class DeviceSchema(BaseModel):
    device_id: str
    type: str
    room: RoomSchema


# --------------------------
# these convert Pydantic -> domain classes
# --------------------------
def pydantic_user_to_domain(u: UserSchema) -> UserDomain:
    return UserDomain(
        user_id=u.user_id,
        name=u.name,
        email=u.email,
        privilege=PrivilegeLevel(u.privilege)
    )

def pydantic_house_to_domain(h: HouseSchema) -> HouseDomain:
    owner_domain = pydantic_user_to_domain(h.owner)
    return HouseDomain(
        house_id=h.house_id,
        address=h.address,
        owner=owner_domain,
        gps_location=h.gps_location,
        num_rooms=h.num_rooms,
        num_baths=h.num_baths
    )

def pydantic_room_to_domain(r: RoomSchema) -> RoomDomain:
    house_domain = pydantic_house_to_domain(r.house)
    return RoomDomain(name=r.name, floor=r.floor, house=house_domain)

def pydantic_device_to_domain(d: DeviceSchema) -> DeviceDomain:
    room_domain = pydantic_room_to_domain(d.room)
    return DeviceDomain(
        type=DeviceType(d.type),
        device_id=d.device_id,
        room=room_domain
    )

# --------------------------
# Users
# --------------------------
@app.get("/users", response_model=List[UserSchema])
def list_users():
    users = get_all_users()
    return [
        UserSchema(
            user_id=u.user_id,
            name=u.name,
            email=u.email,
            privilege=u.privilege.value
        )
        for u in users
    ]

@app.get("/users/{user_id}", response_model=UserSchema)
def retrieve_user(user_id: str):
    try:
        user_obj = get_user(user_id)
        return UserSchema(
            user_id=user_obj.user_id,
            name=user_obj.name,
            email=user_obj.email,
            privilege=user_obj.privilege.value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/users", response_model=UserSchema, status_code=201)
def create_new_user(user: UserSchema):
    try:
        domain_user = pydantic_user_to_domain(user)
        created_user = create_user(domain_user)
        return UserSchema(
            user_id=created_user.user_id,
            name=created_user.name,
            email=created_user.email,
            privilege=created_user.privilege.value
        )
    except (UserValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.put("/users/{user_id}", response_model=UserSchema)
def update_existing_user(user_id: str, user_update: UserSchema):
    """
    user_id in path must match user_update.user_id for consistency,
    or you can decide how you'd like to handle differences.
    """
    if user_id != user_update.user_id:
        raise HTTPException(
            status_code=400,
            detail="URL user_id and body user_id do not match"
        )

    try:
        domain_user = pydantic_user_to_domain(user_update)
        updated = update_user(domain_user)
        return UserSchema(
            user_id=updated.user_id,
            name=updated.name,
            email=updated.email,
            privilege=updated.privilege.value
        )
    except UserValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/users/{user_id}")
def remove_user(user_id: str):
    try:
        delete_user(user_id)
        return {"detail": f"User {user_id} deleted successfully."}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --------------------------
# Houses 
# --------------------------
@app.get("/houses", response_model=List[HouseSchema])
def list_houses():
    houses = get_all_houses()
    return [
        HouseSchema(
            house_id=h.house_id,
            address=h.address,
            owner=UserSchema(
                user_id=h.owner.user_id,
                name=h.owner.name,
                email=h.owner.email,
                privilege=h.owner.privilege.value
            ),
            gps_location=h.gps_location,
            num_rooms=h.num_rooms,
            num_baths=h.num_baths
        )
        for h in houses
    ]

@app.get("/houses/{house_id}", response_model=HouseSchema)
def retrieve_house(house_id: str):
    try:
        house_obj = get_house(house_id)
        return HouseSchema(
            house_id=house_obj.house_id,
            address=house_obj.address,
            owner=UserSchema(
                user_id=house_obj.owner.user_id,
                name=house_obj.owner.name,
                email=house_obj.owner.email,
                privilege=house_obj.owner.privilege.value
            ),
            gps_location=house_obj.gps_location,
            num_rooms=house_obj.num_rooms,
            num_baths=house_obj.num_baths
        )
    except HouseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/houses", response_model=HouseSchema, status_code=201)
def create_new_house(house: HouseSchema):
    try:
        domain_house = pydantic_house_to_domain(house)
        created_house = create_house(domain_house)
        return house  # or reconstruct from created_house if you like
    except HouseValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HouseConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.put("/houses/{house_id}", response_model=HouseSchema)
def update_existing_house(house_id: str, house_update: HouseSchema):
    if house_id != house_update.house_id:
        raise HTTPException(
            status_code=400,
            detail="URL house_id and body house_id do not match"
        )

    try:
        domain_house = pydantic_house_to_domain(house_update)
        updated = update_house(domain_house)
        return house_update
    except HouseValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HouseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/houses/{house_id}")
def remove_house(house_id: str):
    try:
        delete_house(house_id)
        return {"detail": f"House {house_id} deleted successfully."}
    except HouseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --------------------------
# Rooms 
# --------------------------
@app.get("/rooms", response_model=List[RoomSchema])
def list_rooms():
    rooms = get_all_rooms()
    return [
        RoomSchema(
            name=r.name,
            floor=r.floor,
            house=HouseSchema(
                house_id=r.house.house_id,
                address=r.house.address,
                owner=UserSchema(
                    user_id=r.house.owner.user_id,
                    name=r.house.owner.name,
                    email=r.house.owner.email,
                    privilege=r.house.owner.privilege.value
                ),
                gps_location=r.house.gps_location,
                num_rooms=r.house.num_rooms,
                num_baths=r.house.num_baths
            )
        )
        for r in rooms
    ]

@app.get("/rooms/{room_name}", response_model=RoomSchema)
def retrieve_room(room_name: str):
    try:
        room_obj = get_room(room_name)
        return RoomSchema(
            name=room_obj.name,
            floor=room_obj.floor,
            house=HouseSchema(
                house_id=room_obj.house.house_id,
                address=room_obj.house.address,
                owner=UserSchema(
                    user_id=room_obj.house.owner.user_id,
                    name=room_obj.house.owner.name,
                    email=room_obj.house.owner.email,
                    privilege=room_obj.house.owner.privilege.value
                ),
                gps_location=room_obj.house.gps_location,
                num_rooms=room_obj.house.num_rooms,
                num_baths=room_obj.house.num_baths
            )
        )
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/rooms", response_model=RoomSchema, status_code=201)
def create_new_room(room: RoomSchema):
    try:
        domain_room = pydantic_room_to_domain(room)
        create_room(domain_room)
        return room
    except (RoomValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RoomConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.put("/rooms/{room_name}", response_model=RoomSchema)
def rename_room(room_name: str, new_room_data: RoomSchema):
    """
    This example shows how your current code updates the `Room` name.
    You might choose a different approach in practice.
    """
    try:
        # old room
        old_room_obj = get_room(room_name)
        # We only update the "name" in your existing logic. 
        # new_room_data should contain the new name in new_room_data.name.
        updated = update_room(old_room_obj, new_room_data.name)
        # Return updated data
        return RoomSchema(
            name=updated.name,
            floor=updated.floor,
            house=HouseSchema(
                house_id=updated.house.house_id,
                address=updated.house.address,
                owner=UserSchema(
                    user_id=updated.house.owner.user_id,
                    name=updated.house.owner.name,
                    email=updated.house.owner.email,
                    privilege=updated.house.owner.privilege.value
                ),
                gps_location=updated.house.gps_location,
                num_rooms=updated.house.num_rooms,
                num_baths=updated.house.num_baths
            )
        )
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/rooms/{room_name}")
def remove_room(room_name: str):
    try:
        delete_room(room_name)
        return {"detail": f"Room '{room_name}' deleted successfully."}
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --------------------------
# Devices 
# --------------------------
@app.get("/devices", response_model=List[DeviceSchema])
def list_devices():
    devices = get_all_devices()
    return [
        DeviceSchema(
            device_id=d.device_id,
            type=d.type.value,
            room=RoomSchema(
                name=d.room.name,
                floor=d.room.floor,
                house=HouseSchema(
                    house_id=d.room.house.house_id,
                    address=d.room.house.address,
                    owner=UserSchema(
                        user_id=d.room.house.owner.user_id,
                        name=d.room.house.owner.name,
                        email=d.room.house.owner.email,
                        privilege=d.room.house.owner.privilege.value
                    ),
                    gps_location=d.room.house.gps_location,
                    num_rooms=d.room.house.num_rooms,
                    num_baths=d.room.house.num_baths
                )
            )
        )
        for d in devices
    ]

@app.get("/devices/{device_id}", response_model=DeviceSchema)
def retrieve_device(device_id: str):
    try:
        dev_obj = get_device(device_id)
        return DeviceSchema(
            device_id=dev_obj.device_id,
            type=dev_obj.type.value,
            room=RoomSchema(
                name=dev_obj.room.name,
                floor=dev_obj.room.floor,
                house=HouseSchema(
                    house_id=dev_obj.room.house.house_id,
                    address=dev_obj.room.house.address,
                    owner=UserSchema(
                        user_id=dev_obj.room.house.owner.user_id,
                        name=dev_obj.room.house.owner.name,
                        email=dev_obj.room.house.owner.email,
                        privilege=dev_obj.room.house.owner.privilege.value
                    ),
                    gps_location=dev_obj.room.house.gps_location,
                    num_rooms=dev_obj.room.house.num_rooms,
                    num_baths=dev_obj.room.house.num_baths
                )
            )
        )
    except DeviceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/devices", response_model=DeviceSchema, status_code=201)
def create_new_device(device: DeviceSchema):
    try:
        domain_device = pydantic_device_to_domain(device)
        created_dev = create_device(domain_device)
        return device  # or reconstruct from created_dev
    except (DeviceValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DeviceConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.put("/devices/{device_id}", response_model=DeviceSchema)
def update_existing_device(device_id: str, dev_data: DeviceSchema):
    """
    Device ID in path must match dev_data.device_id, or define your own logic.
    """
    if device_id != dev_data.device_id:
        raise HTTPException(
            status_code=400,
            detail="URL device_id and body device_id do not match"
        )
    try:
        domain_device = pydantic_device_to_domain(dev_data)
        update_device(domain_device)
        return dev_data
    except DeviceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DeviceValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/devices/{device_id}")
def remove_device(device_id: str):
    try:
        delete_device(device_id)
        return {"detail": f"Device '{device_id}' deleted successfully."}
    except DeviceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))