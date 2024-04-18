import streamlit as st
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
import pyrealsense2 as rs
import time

# Load JSON data from file
@st.cache(allow_output_mutation=True)
def load_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to find the name corresponding to the given barcode number
def find_name_by_barcode(barcode_number, data):
    barcode_to_name = {value: key for key, value in data.items()}
    return barcode_to_name.get(barcode_number, None)

# Initialize camera
def init_camera():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline

# Process frames
def process_frames(pipeline, data):
    try:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None, None
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        barcodes = decode(color_image)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            person = find_name_by_barcode(barcode_data, data)
            if person:
                return person, barcode_data
        return None, None
    except Exception as e:
        st.error(f"Error processing frame: {e}")
        return None, None

# Main app
def main():
    st.title("Real-Time Barcode Scanner")
    data_path = 'database.json'
    data = load_data(data_path)
    pipeline = init_camera()
    detected_barcodes = set()
    
    placeholder = st.empty()
    while True:
        person, barcode_data = process_frames(pipeline, data)
        if person and barcode_data not in detected_barcodes:
            detected_barcodes.add(barcode_data)
            placeholder.success(f"Detected: {person}")
        time.sleep(1)  # Sleep to limit the rate of processing (adjust based on your requirements)

if __name__ == "__main__":
    main()
