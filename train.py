from ultralytics import YOLO

def main():
    # Load pretrained YOLOv8 Nano model
    model = YOLO("yolov8n.pt")

    # Train the model
    from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="data.yaml",
    epochs=5,
    imgsz=320,
    batch=4,
    workers=2,
    device="cpu",
    project="runs",
    name="industrial_defect_detection"
)

if __name__ == "__main__":
    main()