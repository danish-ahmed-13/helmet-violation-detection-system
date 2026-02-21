import os
import json
from flask import Flask, send_from_directory
from flask_cors import CORS
from db import init_db
from routes import register_routes

def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

def create_media_folders(config):
    """Ensure media folders exist."""
    media_folder = config["media"]["save_folder"]
    violation_folder = config["media"]["violation_folder"]

    os.makedirs(media_folder, exist_ok=True)
    os.makedirs(violation_folder, exist_ok=True)

    # Temporary folder for uploaded images
    temp_folder = os.path.join(media_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    print("Media folders created successfully.")

def create_app():
    """Initialize Flask app, DB, media folders, register routes, and enable CORS."""
    config = load_config()

    app = Flask(__name__)

    # Enable CORS for all routes (so frontend on another port can access backend)
    CORS(app)

    # Initialize database
    init_db()

    # Create media folders
    create_media_folders(config)

    # Register routes
    register_routes(app)

    # Serve media files
    @app.route("/media/<path:filename>")
    def media_files(filename):
        return send_from_directory(config["media"]["save_folder"], filename)

    return app

if __name__ == "__main__":
    config = load_config()
    app = create_app()
    app.run(
        host=config["app"]["host"],
        port=config["app"]["port"],
        debug=config["app"]["debug"]
    )
