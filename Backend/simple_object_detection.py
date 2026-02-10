from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="datasets/data.yaml",
    epochs=60,
    imgsz=512,
    batch=8
)