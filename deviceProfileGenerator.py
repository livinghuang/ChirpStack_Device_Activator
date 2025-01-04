import grpc
from chirpstack_api import api
from config import server, api_token, tenant_id  # Import configuration from external file

def list_device_profile_templates(client, metadata):
    """List all device profile templates."""
    try:
        print("Fetching device profile templates...")
        response = client.List(
            api.ListDeviceProfileTemplatesRequest(limit=100),
            metadata=metadata,
        )
        print("Raw Response:")
        print(response)  # Debug: Print the raw response for verification

        if not response.result:
            print("No device profile templates found.")
        else:
            print("Device profile templates:")
            for template in response.result:
                print(f"ID: {template.id}, Name: {template.name}")
    except grpc.RpcError as e:
        print(f"Failed to fetch device profile templates: {e.code()} - {e.details()}")

def create_device_profile(client, metadata, tenant_id, profile):
    """Framework for creating a device profile."""
    print(f"Preparing to create device profile: {profile['name']}")
    print(f"Details: MAC Version = {profile['mac_version']}, Activation = {profile['activation']}\n")
    # Framework: Implement actual creation logic here
    try:
        print("Simulating device profile creation...")
        # Placeholder for gRPC CreateDeviceProfile call
        print(f"Device profile {profile['name']} creation simulated successfully.")
    except grpc.RpcError as e:
        print(f"Failed to create device profile {profile['name']}: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Connect to ChirpStack gRPC server
    channel = grpc.insecure_channel(server)
    client = api.DeviceProfileTemplateServiceStub(channel)
    metadata = [("authorization", f"Bearer {api_token}")]

    # Example: Simulate listing device profile templates
    list_device_profile_templates(client, metadata)

    # Example: Simulate creating a device profile
    test_profile = {"name": "TestProfile", "mac_version": "1.0.4", "activation": "OTAA"}
    create_device_profile(client, metadata, tenant_id, test_profile)
