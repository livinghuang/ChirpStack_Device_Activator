import csv

def read_devices_csv(file_path):
    """Reads the devices.csv file and returns a list of dictionaries representing each row."""
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        print(f"Successfully read {len(data)} rows from {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {str(e)}")
    return data

if __name__ == "__main__":
    # Example usage
    file_path = "src/devices.csv"  # Replace with your actual CSV file path
    devices_data = read_devices_csv(file_path)
    for index, device in enumerate(devices_data, start=1):
        print(f"Device {index}: {device}")
