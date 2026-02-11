from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv


load_dotenv()

from Backend.database import init_db
from routers import auth_router, detection_router

app = FastAPI(
    title="LandscapeLight AI",
    description="AI-powered landscape lighting detection and planning API",
    version="1.0.0"
)
origins = os.getenv("CORS_ORIGINS", "").split(",")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(detection_router)

# Serve output images
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "LandscapeLight AI API is running"}