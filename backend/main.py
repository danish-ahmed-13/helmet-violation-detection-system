import os
from datetime import datetime
from ultralytics import YOLO
import cv2
import json
from db import insert_violation

# ----------------------------
# Load config.json
# ----------------------------
with open("config.json") as f:
    config = json.load(f)

VEHICLE_MODEL_PATH = config["model"]["vehicle_model_path"]
HELMET_MODEL_PATH = config["model"]["helmet_model_path"]
CONF_THRESHOLD = config["model"]["confidence_threshold"]

VIOLATION_FOLDER = config["media"]["violation_folder"]
VIDEO_PATH = config["video_path"]

HELMET_THRESHOLD = 0.80  # Separate threshold for helmet

# ----------------------------
# Load models ONCE
# ----------------------------
vehicle_model = YOLO(VEHICLE_MODEL_PATH)
helmet_model = YOLO(HELMET_MODEL_PATH)

os.makedirs(VIOLATION_FOLDER, exist_ok=True)

# ----------------------------
# Vehicle Detection
# ----------------------------
def detect_vehicles(image):
    results = vehicle_model(image)
    vehicles = []

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = vehicle_model.names[cls_id]
            confidence = float(box.conf[0])

            if class_name == "motorcycle" and confidence >= CONF_THRESHOLD:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                vehicles.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence
                })

    return vehicles


# ----------------------------
# Helmet Detection
# ----------------------------
def detect_helmet(crop):
    results = helmet_model(crop)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = helmet_model.names[cls_id]
            conf = float(box.conf[0])

            print("Helmet Model ->", class_name, "Conf:", conf)

            if class_name == "helmet" and conf >= HELMET_THRESHOLD:
                return True

    return False


# ----------------------------
# Coordinator Function
# ----------------------------
def run_detection(image_path=None):

    if image_path is None:
        image_path = VIDEO_PATH

    if not os.path.exists(image_path):
        return {"error": f"{image_path} not found"}

    detections = []

    # ✅ If path is folder → process all images
    if os.path.isdir(image_path):
        image_files = [
            os.path.join(image_path, f)
            for f in os.listdir(image_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]
    else:
        image_files = [image_path]

    # Loop through images
    for img_path in image_files:

        img = cv2.imread(img_path)

        if img is None:
            print(f"Could not read {img_path}")
            continue

        h, w, _ = img.shape
        vehicles = detect_vehicles(img)

        for v in vehicles:
            x1, y1, x2, y2 = v["bbox"]

            # Add padding
            pad_x = int((x2 - x1) * 0.5)
            pad_y = int((y2 - y1) * 1.5)

            x1 = max(0, x1 - pad_x)
            y1 = max(0, y1 - pad_y)
            x2 = min(w, x2 + pad_x)
            y2 = min(h, y2 + pad_y)

            crop = img[y1:y2, x1:x2]

            helmet_present = detect_helmet(crop)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            save_path = os.path.join(
                VIOLATION_FOLDER,
                f"motorcycle_{timestamp}.jpg"
            )

            cv2.imwrite(save_path, crop)

            # Insert into DB
            last_id = insert_violation(
                vehicle_type="motorcycle",
                helmet_detected=int(helmet_present),
                confidence=v["confidence"],
                image_path=save_path
            )

            detections.append({
                "id": last_id,
                "vehicle_type": "motorcycle",
                "helmet_status": "safe" if helmet_present else "violation",
                "confidence": v["confidence"],
                "image_saved": save_path
            })

    if not detections:
        return {"message": "No motorcycles detected"}

    return detections