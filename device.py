import json
import os
from enum import Enum
from typing import Optional

from room import Room
from house import House
from user import User, PrivilegeLevel

DEVICES_JSON_FILE = "devices.json"

def load_devices_from_json() -> dict:
    if not os.path.exists(DEVICES_JSON_FILE):
        return {}
    with open(DEVICES_JSON_FILE, "r") as f:
        return json.load(f)

def save_devices_to_json(devices_data: dict) -> None:
    with open(DEVICES_JSON_FILE, "w") as f:
        json.dump(devices_data, f, indent=2)

class DeviceType(Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    LOCK = "lock"
    SENSOR = "sensor"

class Device:
    def __init__(self, type: DeviceType, device_id: str, room: Room):
        if not isinstance(type, DeviceType):
            raise ValidationError(f"Invalid device type: {type}")
        if not device_id.strip():
            raise ValidationError("Device ID cannot be empty")
        if not isinstance(room, Room):
            raise ValidationError("Must provide valid Room object")

        self.type = type
        self.device_id = device_id
        self.room = room

    def __eq__(self, other):
        return (
            self.device_id == other.device_id
            and self.type == other.type
            and self.room == other.room
        )

class DeviceNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

def device_to_dict(device: Device) -> dict:
    return {
        "device_id": device.device_id,
        "type": device.type.value,
        "room": {
            "name": device.room.name,
            "floor": device.room.floor,
            "house": {
                "house_id": device.room.house.house_id,
                "address": device.room.house.address,
                "owner": {
                    "user_id": device.room.house.owner.user_id,
                    "name": device.room.house.owner.name,
                    "email": device.room.house.owner.email,
                    "privilege": device.room.house.owner.privilege.value
                },
                "gps_location": device.room.house.gps_location,
                "num_rooms": device.room.house.num_rooms,
                "num_baths": device.room.house.num_baths
            }
        }
    }

def device_from_dict(data: dict) -> Device:
    room_data = data["room"]
    house_data = room_data["house"]
    owner_data = house_data["owner"]

    owner_user = User(
        user_id=owner_data["user_id"],
        name=owner_data["name"],
        email=owner_data["email"],
        privilege=PrivilegeLevel(owner_data["privilege"])
    )

    house_obj = House(
        house_id=house_data["house_id"],
        address=house_data["address"],
        owner=owner_user,
        gps_location=tuple(house_data["gps_location"]),
        num_rooms=house_data["num_rooms"],
        num_baths=house_data["num_baths"]
    )

    room_obj = Room(
        name=room_data["name"],
        floor=room_data["floor"],
        house=house_obj
    )

    return Device(
        type=DeviceType(data["type"]),
        device_id=data["device_id"],
        room=room_obj
    )

# C
def create_device(device: Device) -> Device:
    devices_data = load_devices_from_json()
    
    if device.device_id in devices_data:
        raise ConflictError(f"Device ID {device.device_id} already exists")
    
    devices_data[device.device_id] = device_to_dict(device)
    save_devices_to_json(devices_data)
    return device

# R
def get_device(device_id: str) -> Device:
    devices_data = load_devices_from_json()
    
    if device_id not in devices_data:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    
    return device_from_dict(devices_data[device_id])

# U
def update_device(updated_device: Device) -> Device:
    devices_data = load_devices_from_json()
    
    if updated_device.device_id not in devices_data:
        raise DeviceNotFoundError(f"Device {updated_device.device_id} not found")
    
    devices_data[updated_device.device_id] = device_to_dict(updated_device)
    save_devices_to_json(devices_data)
    return updated_device

# D
def delete_device(device_id: str) -> None:
    devices_data = load_devices_from_json()
    
    if device_id not in devices_data:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    del devices_data[device_id]
    
    save_devices_to_json(devices_data)