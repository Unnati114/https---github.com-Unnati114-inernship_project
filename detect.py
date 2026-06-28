from ultralytics import YOLO

model = YOLO("runs/detect/runs/industrial_defect_detection/weights/best.pt")

image_path = "archive/NEU-DET/validation/images/crazing/crazing_241.jpg"

results = model.predict(
    source=image_path,
    conf=0.5,
    save=True,
    show=False
)

print("✅ Detection Completed!")