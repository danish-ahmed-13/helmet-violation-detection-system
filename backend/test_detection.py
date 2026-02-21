import cv2
from ultralytics import YOLO
import os

# ----------------------------
# USER CONFIG
# ----------------------------
HELMET_MODEL_PATH = r"C:\Users\USER\Desktop\helmet_violation_system\backend\runs\detect\train\weights\helmet.pt"  # Path to your trained helmet model
IMAGE_PATH = r"C:/Users/USER/Desktop/helmet_violation_system/backend/helmet_test.jpg"  # Image to test
CONF_THRESHOLD = 0.4  # Minimum confidence to consider detection

# ----------------------------
# Load model
# ----------------------------
if not os.path.exists(HELMET_MODEL_PATH):
    print(f"Helmet model not found: {HELMET_MODEL_PATH}")
    exit()

helmet_model = YOLO(HELMET_MODEL_PATH)

# ----------------------------
# Load image
# ----------------------------
if not os.path.exists(IMAGE_PATH):
    print(f"Image not found: {IMAGE_PATH}")
    exit()

img = cv2.imread(IMAGE_PATH)
img_copy = img.copy()

# ----------------------------
# Run helmet detection
# ----------------------------
results = helmet_model(img)
helmet_detected = False

for r in results:
    for box in r.boxes:
        conf = float(box.conf[0])
        if conf >= CONF_THRESHOLD:
            helmet_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Draw box on image
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(img_copy, f"Helmet {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

# ----------------------------
# Output results
# ----------------------------
if helmet_detected:
    print("Helmet detected!")
else:
    print("No helmet detected!")

# Show image with detection boxes
cv2.imshow("Helmet Detection", img_copy)
print("Press any key on the image window to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()
