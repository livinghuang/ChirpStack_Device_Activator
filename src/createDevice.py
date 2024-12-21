import grpc
from chirpstack_api import api
from config import server, api_token, tenant_id  # Import configuration
from test_connection import test_connection_to_chirpstack

def check_device_data(device):
    """Validate and process the device data before creation and activation."""
    protocol = device.get('Protocol', '').upper()

    if protocol.startswith('ABP10'):
        required_keys = ['DevAddr', 'NwkSKey', 'AppSKey']
    elif protocol.startswith('ABP11'):
        required_keys = ['DevAddr', 'NwkSKey', 'AppSKey', 'SNwkSKey', 'FNwkSKey']
    elif protocol.startswith('OTAA10'):
        required_keys = ['AppKey', 'JoinEUI']
    elif protocol.startswith('OTAA11'):
        required_keys = ['AppKey', 'JoinEUI', 'NwkKey']
    else:
        raise ValueError(f"Invalid protocol specified: {protocol}")

    # Validate required keys
    missing_keys = [key for key in required_keys if not device.get(key)]
    if missing_keys:
        raise KeyError(f"Missing required keys for protocol {protocol}: {', '.join(missing_keys)}")

    print(f"Device data validated for protocol {protocol}.")
    return True

def create_device(client, metadata, device):
    """Create and activate a single device in ChirpStack."""
    try:
        # Validate device data
        check_device_data(device)

        print(f"Creating device with DevEUI: {device['DevEUI']}...")

        # Prepare the device object
        device_request = api.CreateDeviceRequest(
            device=api.Device(
                dev_eui=device['DevEUI'],
                name=device['Name'],
                description=device['Desc'],
                application_id=device['AppID'],
                device_profile_id=device['DevProID'],
            )
        )

        # Add JoinEUI if applicable
        if 'JoinEUI' in device and device['JoinEUI']:
            device_request.device.join_eui = device['JoinEUI']

        # Send the request to create the device
        client.Create(device_request, metadata=metadata)
        print(f"Device {device['Name']} with DevEUI {device['DevEUI']} created successfully.")

    except grpc.RpcError as e:
        print(f"Failed to create or configure device {device['DevEUI']}: {e.details()} ({e.code()})")
    except KeyError as ke:
        print(f"Missing key in device data: {ke}")
    except ValueError as ve:
        print(f"Invalid protocol: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    print("Testing connection to ChirpStack...")
    test_connection_to_chirpstack(server, api_token, tenant_id)

    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    metadata = [("authorization", f"Bearer {api_token}")]

    # Example device data
    example_device = {
        'Name': 'PressureSensor',
        'Desc': 'Pressure Monitoring',
        'Protocol': 'ABP104',
        'AppID': '1b8bd972-4007-4b8b-a795-9f1856a20513',
        'DevProID': '54592572-73fa-4889-b03d-3ab2fb29a19d',
        'DevEUI': '0004A30B001C9876',
        'JoinEUI': '',
        'DevAddr': '01ed8596',
        'NwkSKey': '2ffb137b9176c75ff9d0a5faf8738552',
        'AppSKey': 'dd89e2f64a6af3a90d50f9610a29fd06',
        'SNwkSKey': '',
        'FNwkSKey': '',
        'AppKey': '',
        'NwkKey': '',
        'SkipFcntChk': 'TRUE',
        'IsDisable': 'FALSE'
    }
    create_device(client, metadata, example_device)
