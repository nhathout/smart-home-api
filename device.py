from room import Room

class Device:
    def __init__(self, type: str, device_id: str, room : Room): # type should be specific set of device types, can add settings, status, battery, etc
        self.type = type
        self.device_id = device_id
        self.room = room

    # needed for testing
    def __eq__(self, other):
        return (
                self.device_id == other.device_id and 
                self.type == other.type and 
                self.room == other.room
                )

devices_db = {} # to store all houses

class DeviceNotFoundError(Exception):
    pass

## C R U D 
# Create
def create_device(device: Device) -> Device:
    devices_db[device.device_id] = device
    return device

# Read/Get
def get_device(device_id: str) -> Device:
    if device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    return devices_db[device_id]

# Update
def update_device(updated_device: Device) -> Device:
    if updated_device.device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {updated_device.device_id} not found")
    
    devices_db[updated_device.device_id] = updated_device
    return updated_device

# Delete
def delete_device(device_id: str) -> None:
    if device_id not in devices_db:
        raise DeviceNotFoundError(f"Device {device_id} not found")
    
    del devices_db[device_id]