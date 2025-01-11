from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY
from prometheus_client.exposition import basic_auth_handler
from pydantic import BaseModel
from starlette.responses import Response
import requests
import json
import time
import random


app = FastAPI()
# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", ["endpoint", "method"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds", ["endpoint"]
)

MODEL_INFERENCE_TIME = Histogram(
    "model_inference_time_seconds", "Time taken for model inference", ["model"]
)

ERROR_COUNT = Counter("error_count", "Total number of errors", ["endpoint"])

def simulate_model_inference():
    # Simulate the inference time for the AI model (randomized for demonstration)
    inference_time = random.uniform(0.1, 0.5)  # Random time between 0.1 to 0.5 seconds
    time.sleep(inference_time)
    return inference_time

API_URL_1 = "http://classification:8001/detect"
API_URL_2 = "http://segmentation:8002/api/v1/segment"
API_URL_3 = "http://volume_estimation:8003/api/v1/volume-estimate"

# Endpoint to trigger the workflow
@app.post("/workflow")
async def workflow(file: UploadFile = File(...)):
    start_time = time.time()
    # Increment request count
    REQUEST_COUNT.labels(endpoint="/workflow", method="POST").inc()
    try:
        image_path = await file.read()
        files = {"file":(file.filename,image_path,"image/jpeg")}
        model_inference_time = simulate_model_inference()
        out = run_detection(file=files)
        MODEL_INFERENCE_TIME.labels(model="Detection").observe(model_inference_time)
        sout={"id": 1,"food_items":[]}
        model_inference_time = simulate_model_inference()
        for food in out['food_items']:
            fout={}
            fout["id"] = 0
            fout["food_items"] = [food]
            json_str = json.dumps(fout)
            json_bytes = json_str.encode('utf-8')
            out1 = run_segmentation(files, json_bytes)
            sout["food_items"].append(out1)
        MODEL_INFERENCE_TIME.labels(model="Segmentation").observe(model_inference_time)
        dout_bytes = json.dumps(out).encode('utf-8')
        sout_bytes = json.dumps(sout).encode('utf-8')
        model_inference_time = simulate_model_inference()
        oout = run_openai(files, dout_bytes, sout_bytes)
        MODEL_INFERENCE_TIME.labels(model="openai").observe(model_inference_time)
        oout_bytes = json.dumps(oout).encode('utf-8')
    
        # Calculate and record latency
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint="/workflow").observe(latency)
        return json.dumps(dout_bytes.decode()),json.dumps(sout_bytes.decode()),json.dumps(oout_bytes.decode())
    except Exception as e:
        print(e)
        ERROR_COUNT.labels(endpoint="/workflow").inc()
        
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

# Expose metrics to Prometheus
@app.get("/metrics")
async def metrics():
    # Generate metrics in the Prometheus format
    return Response(media_type="text/plain", content=generate_latest())
    #return generate_latest(REGISTRY)

