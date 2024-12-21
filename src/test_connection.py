import grpc
from chirpstack_api import api
from config import server, api_token, tenant_id  # Import configuration from external file

def test_connection_to_chirpstack(server, api_token, tenant_id):
    """
    Test connection to ChirpStack by listing applications for a given tenant.

    Args:
        server (str): ChirpStack gRPC server address
        api_token (str): JWT Token for authentication
        tenant_id (str): Target tenant ID

    Returns:
        None
    """
    print("Connecting to ChirpStack gRPC server...")
    try:
        # Establish gRPC channel
        channel = grpc.insecure_channel(server)
        client = api.ApplicationServiceStub(channel)

        # Set authentication metadata
        metadata = [("authorization", f"Bearer {api_token}")]

        # Create a request to list applications
        request = api.ListApplicationsRequest(tenant_id=tenant_id, limit=10)

        # Call the List method and fetch the response
        response = client.List(request, metadata=metadata)

        print("Connection successful! Listing applications:")
        if not response.result:
            print("No applications found.")
        for app in response.result:
            print(f"ID: {app.id}, Name: {app.name}, Description: {app.description}")
    except grpc.RpcError as e:
        print(f"Failed to connect or retrieve applications: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    test_connection_to_chirpstack(server, api_token, tenant_id)
