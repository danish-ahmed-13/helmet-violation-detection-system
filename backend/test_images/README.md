# 🪖 Helmet Violation Detection System

A full-stack AI-based system that detects motorcycle riders and checks whether they are wearing helmets using YOLOv8 models.

This project uses a Flask backend for detection and a React frontend for displaying results.

---

## 🚀 Project Overview

This system performs:

- Motorcycle detection using YOLOv8
- Helmet detection on detected riders
- Confidence-based decision logic
- Cropped image saving for violations
- SQLite database storage
- REST API communication between backend and frontend

Supports:
- Single image detection
- Folder-based batch detection

---

## 🧠 How It Works

1. An image is passed to the vehicle detection model.
2. Motorcycles are detected using bounding boxes.
3. The detected region is cropped.
4. The cropped image is passed to the helmet detection model.
5. If helmet confidence ≥ 0.80 → SAFE  
   Else → VIOLATION
6. Results are stored in database and shown in frontend.

---

## 🛠️ Tech Stack

Backend:
- Python
- Flask
- YOLOv8 (Ultralytics)
- OpenCV
- SQLite

Frontend:
- React.js
- Axios

Tools:
- Git
- GitHub

---

## 📂 Project Structure

helmet_violation_system/

│

├── backend/
│   ├── main.py
│   ├── app.py
│   ├── routes.py
│   ├── db.py
│   ├── config.json
│   ├── requirements.txt
│   └── detection/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md

---

## ⚙️ How To Run Locally

1️⃣ Clone the repository

git clone https://github.com/danish-ahmed-13/helmet-violation-detection-system.git
cd helmet-violation-detection-system


2️⃣ Backend Setup

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Backend runs at:
http://127.0.0.1:5000


3️⃣ Frontend Setup (Open new terminal)

cd frontend
npm install
npm start

Frontend runs at:
http://localhost:3000

---

## 📊 Features

✔ Motorcycle detection  
✔ Helmet detection  
✔ Confidence filtering  
✔ Batch processing  
✔ Cropped violation saving  
✔ Database logging  
✔ Frontend visualization  

---

## 🔮 Future Improvements

- Real-time video detection
- License plate recognition
- Cloud deployment
- Admin dashboard analytics

---

## 👨‍💻 Author

Danish Ahmed  
Jr Software Engineer 

---

