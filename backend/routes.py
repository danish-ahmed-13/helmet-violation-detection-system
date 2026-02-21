from flask import jsonify, request
from main import run_detection
import os
import json

# Load config to get temp folder path
with open("config.json") as f:
    config = json.load(f)

TEMP_FOLDER = os.path.join(config["media"]["save_folder"], "temp")

def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Helmet Violation Detection Backend Running"})

    @app.route("/detect", methods=["GET", "POST"])
    def detect():
        """
        Detect motorcycles and helmet violations.
        Can accept an image file via POST, otherwise uses default test image.
        """
        # If an image is uploaded via POST
        if request.method == "POST" and "image" in request.files:
            image_file = request.files["image"]
            os.makedirs(TEMP_FOLDER, exist_ok=True)
            file_path = os.path.join(TEMP_FOLDER, image_file.filename)
            image_file.save(file_path)

            result = run_detection(file_path)
            return jsonify(result)

        # If no image uploaded, fallback to default image path from config
        result = run_detection()
        return jsonify(result)
