from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.services.detector import FoodDetector
import io, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
detector = FoodDetector("models/trained_model_20241222-221022.pt")

@app.post("/detect")
async def detect_food(file: UploadFile = File(...)):
    contents = await file.read()
    results = detector.detect(contents)
    return results

@app.get('/healthcheck')
async def get_health_check():
    return {"status": "ok"}
