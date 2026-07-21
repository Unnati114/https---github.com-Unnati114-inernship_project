from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import shutil
import os
import uuid
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---------------- APP ----------------
app = FastAPI(title="Industrial Defect Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODEL ----------------
# Load the custom trained model instead of default coco model
MODEL_PATH = "runs/detect/runs/industrial_defect_detection/weights/best.pt"
if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
else:
    model = YOLO("yolov8n.pt")

# ---------------- FOLDERS ----------------
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# Serve the results folder statically so the frontend can load annotated images
app.mount("/results", StaticFiles(directory=RESULT_DIR), name="results")

# ---------------- STATS ----------------
stats = {"total": 0, "pass": 0, "fail": 0}

# ---------------- PREDICT ----------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

    # save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # YOLO inference
    results = model(file_path)

    # Save the annotated image with plotted bounding boxes
    result_image_path = os.path.join(RESULT_DIR, f"result_{file_id}.jpg")
    results[0].save(filename=result_image_path)

    defects = []
    confidences = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls.item())
            conf = float(box.conf.item())

            # SAFE LABEL ACCESS
            label = model.names.get(cls, str(cls))

            defects.append(label)
            confidences.append(conf)

    # SAFE AVERAGE
    avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else 0

    # PASS / FAIL
    status = "PASS" if len(defects) == 0 else "FAIL"

    # update stats
    stats["total"] += 1
    stats["pass"] += 1 if status == "PASS" else 0
    stats["fail"] += 1 if status == "FAIL" else 0

    return {
        "status": status,
        "defects": defects,
        "confidence": avg_conf,
        "image_path": file_path,
        "annotated_image_url": f"http://127.0.0.1:8000/results/result_{file_id}.jpg",
        "stats": stats
    }

# ---------------- EXCEL ----------------
@app.get("/export/excel")
def export_excel():
    df = pd.DataFrame([stats])
    path = os.path.join(RESULT_DIR, "report.xlsx")
    df.to_excel(path, index=False)
    return FileResponse(path, filename="report.xlsx")

# ---------------- PDF ----------------
@app.get("/export/pdf")
def export_pdf():
    path = os.path.join(RESULT_DIR, "report.pdf")
    c = canvas.Canvas(path, pagesize=letter)

    c.drawString(100, 750, "Industrial Defect Detection Report")
    c.drawString(100, 720, f"Total: {stats['total']}")
    c.drawString(100, 700, f"PASS: {stats['pass']}")
    c.drawString(100, 680, f"FAIL: {stats['fail']}")

    c.save()

    return FileResponse(path, filename="report.pdf")