import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time
# -----------------------------
#  Initialization
# -----------------------------
print("🚗 Vehicle Distance Measurement System - Starting...")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Using device: {device}")

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # lightweight model
print("✅ YOLOv8 model loaded successfully!")

# -----------------------------
#  Input Source Selection
# -----------------------------
print("\nChoose Input Source:")
print("1. Dashcam video file")
print("2. Laptop/USB webcam")
print("3. IP camera stream\n")

choice = input("Enter your choice (1/2/3): ").strip()

if choice == "1":
    video_path = input("Enter video file path (e.g., dashcam_video.mp4): ").strip()
    cap = cv2.VideoCapture(video_path)
elif choice == "2":
    cap = cv2.VideoCapture(0)
elif choice == "3":
    ip_url = input("Enter IP camera URL (e.g., http://192.168.1.10:8080/video): ").strip()
    cap = cv2.VideoCapture(ip_url)
else:
    print("❌ Invalid choice! Defaulting to webcam...")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("❌ Could not open the video/camera source!")

# -----------------------------
#  Region of Interest (ROI)
# -----------------------------
ROI_ZONES = {
    'LEFT': [[240, 600], [925, 550], [312, 1100], [100, 1100]],
    'MAIN': [[925, 550], [1025, 550], [1712, 1100], [312, 1100]],
    'RIGHT': [[1025, 550], [1802, 600], [1942, 1100], [1712, 1100]]
}

OPTICAL_CENTERS = {
    'LEFT': (500, 800),
    'MAIN': (1025, 900),
    'RIGHT': (1550, 800)
}

WARNING_DISTANCES = {
    'LEFT': 1.0,
    'MAIN': 2.0,
    'RIGHT': 1.0
}

FOCAL_LENGTH = 500
VEHICLE_CONFIDENCE = 0.7

# -----------------------------
#  Processing Loop
# -----------------------------
fps_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print("📹 Stream ended or camera disconnected.")
        break

    # Run YOLO detection
    results = model(frame, conf=VEHICLE_CONFIDENCE, verbose=False)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        label = model.names[cls]

        if label not in ['car', 'truck', 'bus', 'motorbike']:
            continue

        # Approx distance based on bounding box height (simplified)
        box_height = y2 - y1
        distance_m = (FOCAL_LENGTH * 1.6) / (box_height + 1e-6)
        distance_m = np.clip(distance_m, 0.5, 50.0)

        color = (0, 255, 0) if distance_m > 2 else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {distance_m:.1f} m",
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, color, 2)

    # FPS Display
    fps = 1 / (time.time() - fps_time)
    fps_time = time.time()
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Vehicle Distance Measurement", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
