import json

# Function to load JSON data from a file
def load_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to find the name corresponding to the given barcode number
def find_name_by_barcode(barcode_number, data):
    # Flip the keys and values in the dictionary so the barcode numbers become the keys
    barcode_to_name = {value: key for key, value in data.items()}
    # Return the name corresponding to the barcode number, or None if not found
    return barcode_to_name.get(barcode_number, None)

# Example usage:
filepath = 'database.json'  # Replace 'your_file_path.json' with the path to your JSON file
data = load_data(filepath)
barcode_number = '5901234123457'
name = find_name_by_barcode(barcode_number, data)
print(name)
