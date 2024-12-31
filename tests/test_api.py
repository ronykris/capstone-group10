import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.utils.config import config
import io
from PIL import Image
import numpy as np
import json
import os
from io import BytesIO

# Create a new app instance for testing
app = create_app()
client = TestClient(app)

@pytest.fixture
def mock_image():
    """Load test image from tests folder"""
    with open('tests/20151127_114556.jpg', 'rb') as f:
        return io.BytesIO(f.read())

@pytest.fixture
def mock_classification_data():
    """Create mock classification data"""
    return {
        "id": 1,
        "food_items": [
            {
                "id": 1,
                "class_name": "test_food",
                "confidence": 0.95,
                "bounding_box": {
                    "x_min": 2000,
                    "y_min": 1220,
                    "x_max": 2680,
                    "y_max": 1950
                }
            }
        ]
    }

def test_get_classification():
    """Test GET /classification/{image_id} endpoint"""
    response = client.get("/api/v1/classification/1")
    assert response.status_code == 200
    data = response.json()
    assert "food_items" in data
    assert isinstance(data["food_items"], list)

def test_get_classification_invalid_id():
    """Test GET with invalid image ID"""
    response = client.get("/api/v1/classification/-1")
    assert response.status_code == 404

# @pytest.mark.skipif(not os.getenv("FAL_KEY"), reason="FAL_KEY not set")
def test_segment_image(mock_image, mock_classification_data):
    """Test POST /segment endpoint with real FAL API"""
    files = {
        "file": ("test.jpg", mock_image, "image/jpeg")
    }
    data = {
        "classification_data": json.dumps(mock_classification_data)
    }
    response = client.post(
        "/api/v1/segment",
        files=files,
        data=data
    )
    assert response.status_code == 200
    data = response.json()
    assert "food_items" in data

def test_segment_image_invalid_file_type(mock_classification_data):
    """Test POST with invalid file type"""
    files = {
        "file": ("test.txt", b"invalid content", "text/plain")
    }
    data = {
        "classification_data": json.dumps(mock_classification_data)
    }
    response = client.post(
        "/api/v1/segment",
        files=files,
        data=data
    )
    assert response.status_code == 400

def test_segment_image_large_file(mock_classification_data):
    """Test POST with file exceeding size limit"""
    # Create a large file
    large_file = io.BytesIO(b"0" * (config.get("image", "max_size_mb") * 1024 * 1024 + 1))
    files = {
        "file": ("large.jpg", large_file, "image/jpeg")
    }
    data = {
        "classification_data": json.dumps(mock_classification_data)
    }
    response = client.post(
        "/api/v1/segment",
        files=files,
        data=data
    )
    assert response.status_code == 400

