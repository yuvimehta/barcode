import pyrealsense2 as rs
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
from owl_client import OwlClient, Joint
import time
client = OwlClient("10.42.0.53")
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m' 

def run_program():
    # Wait for the robot to be available
    while not client.is_running():
        time.sleep(0.5)
        client.send_script("save.xml")

filepath = 'database.json'  # Replace 'your_file_path.json' with the path to your JSON file
print(f"{Colors.YELLOW}List of the people attending::{Colors.RESET}")
print()
print()

# Configure depth and color streams from the RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

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
# Start streaming
pipeline.start(config)
detected_barcodes = set() 
run_program()
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the BGR image to RGB
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Decode the barcodes
        barcodes = decode(color_image)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(color_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            
            if barcode_data not in detected_barcodes:
                detected_barcodes.add(barcode_data)
                data = load_data(filepath)
                person = find_name_by_barcode(barcode_data, data)
                if person:
                    print(f"{Colors.YELLOW}{person}{Colors.RESET}")
                    data = {
                            "name": person
                                }
                    with open("qr_test.json", 'w') as f:
                        json.dump(data, f, indent=4)
                    print()
                    
            # print(f"{Colors.YELLOW}Detected Marker ID:: {markerID}, At pose of x::{pose[0]}, y::{pose[1]}, z::{pose[2]}, orientation::{oreintation}, distance::{distance}{Colors.RESET}")   
        # Display the resulting frame
        cv2.imshow('RealSense', cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
