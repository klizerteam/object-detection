import cv2
import uuid
import shutil
from sqlalchemy.orm import Session
from fastapi import FastAPI,UploadFile,File,Depends,HTTPException
from pydantic import BaseModel, EmailStr
from ultralytics import YOLO
from typing import Optional
from yolo_detector import assign_lighting
from database import init_db
from models import Detection
from database import SessionLocal
from models import User
from auth import hash_password, verify_password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

web = FastAPI()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

@web.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@web.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email
    }


@web.on_event("startup")
def startup():
    init_db()
model = YOLO("runs/detect/train/weights/best.pt")

upload_dir = "uploads"
output_dir = "outputs"
import os
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)



@web.post("/detect")
async def detect_image(file:UploadFile=File(...),db: Session = Depends(get_db)):
    image_id = str(uuid.uuid4())
    class_names = ["Tree", "Fence", "Door", "Shrub", "Pathway", "Window"]
    input_path = f"{upload_dir}/{image_id}_{file.filename}"
    with open(input_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    image = cv2.imread(input_path)
    results=model(image)
    lighting_plan = assign_lighting(results,class_names)
    annotated_image = results[0].plot()
    output_path = f"{output_dir}/{image_id}_{file.filename}"
    cv2.imwrite(output_path,annotated_image)
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

    return{
        "image_path":output_path,
        "detections":lighting_plan
    }



@web.get("/detections/")
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
