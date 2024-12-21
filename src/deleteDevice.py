import grpc
from chirpstack_api import api
from config import server, api_token, tenant_id  # Import configuration
from test_connection import test_connection_to_chirpstack

def delete_device(client, metadata, dev_eui):
    """Delete a device from ChirpStack by DevEUI."""
    try:
        print(f"Deleting device with DevEUI: {dev_eui}...")

        # Prepare the delete device request
        delete_request = api.DeleteDeviceRequest(dev_eui=dev_eui)

        # Send the delete request
        client.Delete(delete_request, metadata=metadata)
        print(f"Device with DevEUI {dev_eui} deleted successfully.")
    except grpc.RpcError as e:
        print(f"Failed to delete device {dev_eui}: {e.details()} ({e.code()})")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    print("Testing connection to ChirpStack...")
    test_connection_to_chirpstack(server, api_token, tenant_id)

    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    metadata = [("authorization", f"Bearer {api_token}")]

    # Example DevEUI
    dev_eui = "0004A30B001C1234"  # Replace with the actual DevEUI of the device to delete

    delete_device(client, metadata, dev_eui)
