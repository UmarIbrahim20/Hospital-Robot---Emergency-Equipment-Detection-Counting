#!/usr/bin/env python3
"""
Test YOLO model outside of ROS to isolate the issue
"""

import cv2
import numpy as np
from ultralytics import YOLO

print("Testing YOLO with OpenCV compatibility...")
print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")

# Load model
model_path = "/workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_perception/weights/best.pt"
print(f"\nLoading model from: {model_path}")

try:
    model = YOLO(model_path)
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Failed to load model: {e}")
    exit(1)

# Create a test image (simulating what ROS would send)
print("\nCreating test image (640x480, RGB)...")
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

# Ensure it's contiguous
test_image = np.ascontiguousarray(test_image)

print(f"Image shape: {test_image.shape}")
print(f"Image dtype: {test_image.dtype}")
print(f"Image contiguous: {test_image.flags['C_CONTIGUOUS']}")
print(f"Image type: {type(test_image)}")

# Try YOLO inference
print("\nRunning YOLO inference...")
try:
    results = model(test_image, conf=0.5, verbose=False)
    print("✓ YOLO inference successful!")
    print(f"Number of detections: {len(results[0].boxes)}")
except Exception as e:
    print(f"✗ YOLO inference failed: {e}")
    print("\nThis confirms the OpenCV version incompatibility.")
    print("Solution: pip install opencv-python==4.8.1.78")
    exit(1)

# Test with actual image file if available
print("\n" + "="*60)
print("If you have a test image, you can test with:")
print("python3 test_yolo.py --image /path/to/image.jpg")
print("="*60)