# 🏭 AI Industrial Defect Detection System

An AI-powered defect detection system using **YOLOv8 and FastAPI** that detects defects in industrial images and classifies them as **PASS / FAIL** with confidence scores and analytics dashboard.

---

## 🚀 Features

-  Upload industrial images
-  YOLOv8-based object detection
-  PASS / FAIL classification
-  Confidence score display
-  Analytics dashboard (Total, Pass, Fail)
-  Export reports in PDF format
-  Export reports in Excel format
-  FastAPI backend for real-time processing

---

## Tech Stack

- Python 
- FastAPI 
- YOLOv8 (Ultralytics) 
- Pandas 
- ReportLab 
- HTML, CSS, JavaScript 🌐

---

## 📁 Project Structure
Industrial_Defect_Detection/
│
├── api/
│ └── main.py
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── uploads/
├── results/
├── models/
│ └── best.pt
│
├── requirements.txt
└── README.md

## How It Works
User uploads image
Image sent to FastAPI backend
YOLOv8 detects objects/defects
System calculates confidence score
Output: PASS / FAIL result
Analytics & reports generated
