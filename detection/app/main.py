from fastapi import FastAPI, UploadFile, File
from app.services.detector import FoodDetector
import io

app = FastAPI()
detector = FoodDetector("models/trained_model.pt")

@app.post("/detect")
async def detect_food(file: UploadFile = File(...)):
    contents = await file.read()
    results = detector.detect(contents)
    return results