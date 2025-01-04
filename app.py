from flask import Flask, render_template, request, redirect, flash
import configparser
import os
import csv
import grpc
from chirpstack_api import api
from createDevice import create_device  # Import create_device function
from activeDevice import activate_device  # Import activate_device function
from deleteDevice import delete_device # Import delete_device function

app = Flask(__name__)
app.secret_key = "your_secret_key"

CONFIG_FILE = "settings.ini"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}

# Default configuration
DEFAULT_CONFIG = {
    "server": "127.0.0.1:8080",
    "api_token": "default_api_token",
    "tenant_id": "default_tenant_id"
}

# Ensure settings.ini exists with default values
if not os.path.exists(CONFIG_FILE):
    config = configparser.ConfigParser()
    config["ChirpStack"] = DEFAULT_CONFIG
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

devices_data = []  # Store uploaded devices

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv(file_path):
    """Read the uploaded CSV file and return its content."""
    devices = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                devices.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return devices

def create_device(client, metadata, device):
    """Create a single device in ChirpStack."""
    try:
        print(f"Creating device with DevEUI: {device['DevEUI']}...")
        device_request = api.CreateDeviceRequest(
            device=api.Device(
                dev_eui=device['DevEUI'],
                name=device['Name'],
                description=device['Desc'],
                application_id=device['AppID'],
                device_profile_id=device['DevProID'],
                is_disabled=False  # Enable the device
            )
        )
        client.Create(device_request, metadata=metadata)
        print(f"Device {device['DevEUI']} created successfully.")
        flash(f"Device {device['DevEUI']} created successfully.", "success")
    except grpc.RpcError as e:
        print(f"Failed to create device {device['DevEUI']}: {e.details()} ({e.code()})")
        flash(f"Failed to create device {device['DevEUI']}: {e.details()} ({e.code()})", "error")

@app.route("/")
def index():
    """Render the index page with current ChirpStack settings."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return render_template(
        "index.html",
        server=config.get("ChirpStack", "server", fallback=DEFAULT_CONFIG["server"]),
        api_token=config.get("ChirpStack", "api_token", fallback=DEFAULT_CONFIG["api_token"]),
        tenant_id=config.get("ChirpStack", "tenant_id", fallback=DEFAULT_CONFIG["tenant_id"]),
        devices=devices_data if devices_data else None  # Show all rows
    )

@app.route("/settings", methods=["POST"])
def save_settings():
    """Save the ChirpStack settings provided by the user."""
    server = request.form.get("server")
    api_token = request.form.get("api_token")
    tenant_id = request.form.get("tenant_id")

    if not server or not api_token or not tenant_id:
        flash("All fields are required!", "error")
        return redirect("/")

    config = configparser.ConfigParser()
    config["ChirpStack"] = {
        "server": server,
        "api_token": api_token,
        "tenant_id": tenant_id
    }
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    flash("Settings saved successfully!", "success")
    return redirect("/")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle the file upload."""
    global devices_data  # Use global to persist devices data across requests
    if "file" not in request.files:
        flash("No file part", "error")
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file", "error")
        return redirect("/")

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Read the file content
        devices_data = read_csv(file_path)

        if devices_data:
            flash(f"{len(devices_data)} devices loaded successfully!", "success")
        else:
            flash("No devices found in the file or file format is invalid.", "error")
            devices_data = []

    else:
        flash("File type not allowed. Please upload a CSV file.", "error")

    return redirect("/")

@app.route("/create_devices", methods=["POST"])
def create_devices():
    """Create devices from the uploaded CSV."""
    if not devices_data:
        flash("No devices to create. Please upload a CSV file first.", "error")
        return redirect("/")

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    server = config.get("ChirpStack", "server", fallback="")
    api_token = config.get("ChirpStack", "api_token", fallback="")
    metadata = [("authorization", f"Bearer {api_token}")]

    # Establish gRPC connection
    try:
        channel = grpc.insecure_channel(server)
        client = api.DeviceServiceStub(channel)

        for device in devices_data:
            create_device(client, metadata, device)
            activate_device(client, metadata, device)  # Activate the device

    except Exception as e:
        flash(f"Failed to create devices: {e}", "error")

    return redirect("/")

@app.route("/delete_devices", methods=["POST"])
def delete_devices():
    """Delete devices listed in the uploaded CSV."""
    if not devices_data:
        flash("No devices to delete. Please upload a CSV file first.", "error")
        return redirect("/")

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    server = config.get("ChirpStack", "server", fallback="")
    api_token = config.get("ChirpStack", "api_token", fallback="")
    metadata = [("authorization", f"Bearer {api_token}")]

    # Establish gRPC connection
    try:
        channel = grpc.insecure_channel(server)
        client = api.DeviceServiceStub(channel)

        for device in devices_data:
            try:
                print(f"Deleting device with DevEUI: {device['DevEUI']}...")
                client.Delete(api.DeleteDeviceRequest(dev_eui=device['DevEUI']), metadata=metadata)
                flash(f"Device {device['DevEUI']} deleted successfully.", "success")
            except grpc.RpcError as e:
                print(f"Failed to delete device {device['DevEUI']}: {e.details()} ({e.code()})")
                flash(f"Failed to delete device {device['DevEUI']}: {e.details()} ({e.code()})", "error")

    except Exception as e:
        flash(f"Failed to delete devices: {e}", "error")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5050)
