from room import Room
from enum import Enum
from typing import Optional

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
            self.device_id == other.device_id and 
            self.type == other.type and 
            self.room == other.room
        )

devices_db = {}

class DeviceNotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

# C
def create_device(device: Device) -> Device:
    if device.device_id in devices_db:
        raise ConflictError(f"Device ID {device.device_id} already exists")
    
    devices_db[device.device_id] = device
    return device

# R
def get_device(device_id: str) -> Device:
    if device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    return devices_db[device_id]

# U
def update_device(updated_device: Device) -> Device:
    if updated_device.device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {updated_device.device_id} not found")
    
    devices_db[updated_device.device_id] = updated_device
    return updated_device

# D
def delete_device(device_id: str) -> None:
    if device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    del devices_db[device_id]