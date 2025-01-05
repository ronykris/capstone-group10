from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import httpx
from pydantic import BaseModel
import requests
from io import BytesIO
import json


app = FastAPI()

API_URL_1 = "http://localhost:8000/detect"
API_URL_2 = "http://localhost:8002/api/v1/segment"
API_URL_3 = "http://localhost:8003/api/v1/volume-estimate"

# Endpoint to trigger the workflow
@app.post("/workflow")
async def workflow(file: UploadFile = File(...)):
    image_path = await file.read()
    files = {"file":(file.filename,image_path,"image/jpeg")}
    out = run_detection(file=files)
    sout={"id": 1,"food_items":[]}
    for food in out['food_items']:
        fout={}
        fout["id"] = 0
        fout["food_items"] = [food]
        json_str = json.dumps(fout)
        json_bytes = json_str.encode('utf-8')
        out1 = run_segmentation(files, json_bytes)
        sout["food_items"].append(out1)
    dout_bytes = json.dumps(out).encode('utf-8')
    sout_bytes = json.dumps(sout).encode('utf-8')
    oout = run_openai(files, dout_bytes, sout_bytes)
    oout_bytes = json.dumps(oout).encode('utf-8')
    return json.dumps(dout_bytes),json.dumps(sout_bytes),json.dumps(oout_bytes)
    
def run_detection(file: UploadFile = File(...)):
    response_service1 = requests.post(API_URL_1, files=file)
    out1 = json.loads(response_service1.content.decode('utf-8'))
    return out1

def run_segmentation(file, out):
    response_service2 = requests.post(API_URL_2, files=file, data={"classification_data":out})
    print(response_service2.json())
    return response_service2.json()['food_items'][0]

def run_openai(file, dout ,sout):
    response_service3 = requests.post(API_URL_3, files=file, data={"classification_data":dout,"segmentation_data":sout})
    return response_service3.content.decode('utf-8')
    
@app.get('/healthcheck')
async def get_health_check():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary indicating the service health status.
    """
    return {"status": "ok"}