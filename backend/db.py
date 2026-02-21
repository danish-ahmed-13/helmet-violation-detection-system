import sqlite3
import json
import os


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def init_db():
    config = load_config()
    db_name = config["database"]["name"]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT,
            helmet_detected INTEGER,
            confidence REAL,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print(f"Database '{db_name}' initialized successfully.")


def insert_violation(vehicle_type, helmet_detected, confidence, image_path):
    config = load_config()
    db_name = config["database"]["name"]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO violations (vehicle_type, helmet_detected, confidence, image_path)
        VALUES (?, ?, ?, ?)
    """, (vehicle_type, helmet_detected, confidence, image_path))

    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


    conn.commit()
    conn.close()
