from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import httpx
from pydantic import BaseModel
import requests
from io import BytesIO
import uvicorn
import json
import urllib.parse
import base64


# Define external API URLs (Example APIs)
API_URL_1 = "http://localhost:8000/detect"
API_URL_2 = "http://localhost:8002/api/v1/segment"
API_URL_3 = "http://localhost:8003/api/v1/volume-estimate"

# Endpoint to trigger the workflow
#@app.post("/workflow")
    
def run_detection(file: UploadFile = File(...)):
    response_service1 = requests.post(API_URL_1, files=file)
    out1 = json.loads(response_service1.content.decode('utf-8'))
    return out1

def run_segmentation(file, out):
    response_service2 = requests.post(API_URL_2, files=file, data={"classification_data":out})
    return response_service2.json()['food_items'][0]

def run_openai(file, dout ,sout):
    response_service3 = requests.post(API_URL_3, files=file, data={"classification_data":dout,"segmentation_data":sout})
    return response_service3.content.decode('utf-8')

if __name__ == "__main__":
    image_path = "1m.jpeg"
    with open(image_path, "rb") as image_file:
        # Create a dictionary to hold the file data
        files = {"file": (image_path, image_file, "image/jpeg")}
        out = run_detection(file=files)
    sout={"id": 1,"food_items":[]}
    for food in out['food_items']:
        fout={}
        fout["id"] =0
        fout["food_items"] = [food]
        json_str = json.dumps(fout)
        json_bytes = json_str.encode('utf-8')
        with open(image_path, "rb") as image_file:
            file = {"file": (image_path, image_file, "image/jpeg")}
            out1 = run_segmentation(file, json_bytes)
            sout["food_items"].append(out1)
    dout_bytes = json.dumps(out).encode('utf-8')
    sout_bytes = json.dumps(sout).encode('utf-8')
    with open(image_path, "rb") as image_file:
        file = {"file": (image_path, image_file, "image/jpeg")}
        oout = run_openai(file, dout_bytes, sout_bytes)
    oout_bytes = json.dumps(oout).encode('utf-8')
    print(dout_bytes,sout_bytes,oout_bytes)