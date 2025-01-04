import grpc
from chirpstack_api import api
from config import server, api_token, tenant_id  # Import configuration from external file
from test_connection import test_connection_to_chirpstack
from input import read_devices_csv
from createDevice import create_device  # Import create_device function
from activeDevice import activate_device  # Import activate_device function
from deleteDevice import delete_device # Import delete_device function

def main():
    """Main function to coordinate all tasks."""
    print("Starting ChirpStack management script...")

    # Test Connection
    print("\nTesting connection to ChirpStack...")
    test_connection_to_chirpstack(server, api_token, tenant_id)

    # Read CSV File
    print("\nReading CSV file...")
    file_path = "src/devices.csv"  # Replace with the actual path to your CSV file
    devices = read_devices_csv(file_path)
    if not devices:
        print("No devices found in the CSV file. Exiting.")
        return

    # Print Loaded Devices
    print("\nLoaded devices:")
    for index, device in enumerate(devices, start=1):
        print(f"Device {index}: {device}")

    # Create and Activate Devices
    print("\nCreating and activating devices...")
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    metadata = [("authorization", f"Bearer {api_token}")]

    for device in devices:
        create_device(client, metadata, device)  # Create the device
        activate_device(client, metadata, device)  # Activate the device
    
    # for device in devices:
    #     delete_device(client, metadata, device['DevEUI'])

if __name__ == "__main__":
    main()
