import os
import cv2
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ultralytics import YOLO

from Backend.database import SessionLocal
from Backend.models import Detection
from Backend.yolo_detector import assign_lighting

router = APIRouter(prefix="/detection", tags=["Detection"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Load YOLO model
model = YOLO("runs/detect/train/weights/best.pt")

# Directory setup
upload_dir = "uploads"
output_dir = "outputs"
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


@router.post("/detect")
async def detect_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_id = str(uuid.uuid4())
    class_names = ["Tree", "Fence", "Door", "Shrub", "Pathway", "Window"]
    input_path = f"{upload_dir}/{image_id}_{file.filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = cv2.imread(input_path)
    results = model(image)
    lighting_plan = assign_lighting(results, class_names)
    annotated_image = results[0].plot()
    output_path = f"{output_dir}/{image_id}_{file.filename}"
    cv2.imwrite(output_path, annotated_image)

    for det in lighting_plan:
        db_row = Detection(
            image_name=file.filename,
            object_type=det["object"],
            confidence=det["confidence"],
            suggested_light=det["light"],
            detected_image=output_path
        )
        db.add(db_row)

    db.commit()

    return {
        "image_path": output_path,
        "detections": lighting_plan
    }


@router.get("/detections")
def get_detections(
    id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if id:
        detection = db.query(Detection).filter(Detection.id == id).first()
        if not detection:
            raise HTTPException(status_code=404, detail="Detection not found")
        return detection

    detections = db.query(Detection).all()
    return {
        "count": len(detections),
        "data": detections
    }