from fastapi import FastAPI, UploadFile, File
from app.services.detector import FoodDetector
import io, os

app = FastAPI()

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#print(f"{BASE_DIR}")
#model_path = os.path.join(BASE_DIR, "models", "trained_model_20241222-221022.pt")
#detector = FoodDetector(model_path)
detector = FoodDetector("models/trained_model_20241222-221022.pt")

@app.post("/detect")
async def detect_food(file: UploadFile = File(...)):
    contents = await file.read()
    results = detector.detect(contents)
    return results