import grpc
from chirpstack_api import api
from config import server, api_token  # Import configuration

def activate_device(client, metadata, device):
    """Activate an already created device in ChirpStack and update its settings."""
    try:
        print(f"Activating device with DevEUI: {device['DevEUI']}...")

        # Update device settings (enable device and frame-counter validation)
        update_device_request = api.UpdateDeviceRequest(
            device=api.Device(
                dev_eui=device['DevEUI'],
                name=device['Name'],
                description=device['Desc'],
                application_id=device['AppID'],
                device_profile_id=device['DevProID'],
                is_disabled=device['IsDisable'].strip().lower() == 'true',  # Set device enable/disable
                skip_fcnt_check=device['SkipFcntChk'].strip().lower() == 'true'  # Set frame-counter validation
            )
        )
        client.Update(update_device_request, metadata=metadata)
        print(f"Device {device['DevEUI']} settings updated successfully.")

        # Prepare the activation request
        activation_request = api.ActivateDeviceRequest(
            device_activation=api.DeviceActivation(
                dev_eui=device['DevEUI'],
                dev_addr=device['DevAddr'],
                app_s_key=device['AppSKey'],
                nwk_s_enc_key=device['NwkSKey'],
                s_nwk_s_int_key=device.get('SNwkSKey', ''),
                f_nwk_s_int_key=device.get('FNwkSKey', '')
            )
        )

        # Send the activation request
        client.Activate(activation_request, metadata=metadata)
        print(f"Device {device['DevEUI']} activated successfully.")

    except grpc.RpcError as e:
        print(f"Failed to activate device {device['DevEUI']}: {e.details()} ({e.code()})")
    except KeyError as ke:
        print(f"Missing key in device data: {ke}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    metadata = [("authorization", f"Bearer {api_token}")]

    # Example device data for activation
    example_device = {
        'DevEUI': '0004A30B001C9876',
        'Name': 'LightSensor',
        'Desc': 'Light Monitoring',
        'AppID': '1b8bd972-4007-4b8b-a795-9f1856a20513',
        'DevProID': '28c27b72-1860-42af-97f8-aabc69a01281',
        'DevAddr': '01ed8596',
        'NwkSKey': '2ffb137b9176c75ff9d0a5faf8738552',
        'AppSKey': 'dd89e2f64a6af3a90d50f9610a29fd06',
        'SNwkSKey': '',
        'FNwkSKey': '',
        'SkipFcntChk': 'TRUE',
        'IsDisable': 'FALSE'
    }

    activate_device(client, metadata, example_device)
