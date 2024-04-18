#!/bin/bash

cd ~/hackathon/barcode
echo "Starting Owl Robot GPT"

# Base directory
base_dir=$(pwd)


echo "Path to run.py: ${base_dir}/detect.py"

# Terminal 2: launch script
echo "Running launch.py script..."
gnome-terminal -- bash -c "python3 ${base_dir}/detect.py"

  