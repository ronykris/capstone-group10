# Food Image Segmentation API

A FastAPI-based service that performs food image segmentation using FAL AI's Segment Anything Model (SAM). The API accepts food images and their bounding box coordinates, processes them through SAM, and returns segmented images with pixel area calculations.

## Features

- Image segmentation using FAL AI's SAM model
- Bounding box-based segmentation
- Pixel area calculations
- Configuration management using YAML
- Environment-based settings
- Docker support
- Comprehensive test suite

## Prerequisites

- Python 3.10 or higher
- Docker (optional)
- FAL AI API key

## Installation

1. Clone the repository:
bash
git clone https://github.com/yourusername/food-segmentation-api.git
cd food-segmentation-api

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
bash
pip install -r requirements.txt

4. Copy the example environment file and set your FAL AI API key:
bash
cp .env.example .env

5. Update `.env` with your FAL AI API key:
plaintext
FAL_KEY=your_fal_key_here
APP_ENV=development

## Configuration

The application uses a YAML-based configuration system (`config/settings.yaml`):

- Application settings (port, host, etc.)
- API configurations
- Image processing parameters
- Logging settings

Environment variables can override configuration values:
- `FAL_KEY`: FAL AI API key
- `APP_PORT`: Application port
- `APP_HOST`: Host address
- `LOG_LEVEL`: Logging level

## Usage

### Running the Application

1. Development mode:
bash
python -m app.main
2. Using helper script:
bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh

### API Endpoints

1. Get Classification Data:
bash
GET /api/v1/classification/{image_id}

2. Segment Image:
bash
POST /api/v1/segment

3. Example Curl Request:
bash
curl -X POST "http://localhost:8002/api/v1/segment" \
-H "Content-Type: multipart/form-data" \
-F "file=@food_image.jpg" \
-F 'classification_data={"id":1,"food_items":[{"id":1,"class_name":"rice","confidence":0.95,"bounding_box":{"x_min":100,"y_min":100,"x_max":200,"y_max":200}}]}'

## Docker Support

### Building the Image

1. Using Docker build:
bash
docker build -t food-segmentation-api .

2. Using helper script:
bash
chmod +x scripts/build_image.sh
./scripts/build_image.sh [version]

### Running with Docker

1. Basic run:
bash
docker run -d \
--name food-segmentation \
-p 8002:8002 \
-e FAL_KEY=your_fal_key_here \
food-segmentation-api

2. Development mode with volume mounts:
bash
docker run -d \
--name food-segmentation-dev \
-p 8002:8002 \
-v "$(pwd)/app:/app/app" \
-v "$(pwd)/config:/app/config" \
--env-file .env \
food-segmentation-api

### Testing

1. Running all tests:
bash
pytest

2. Run specific test files:
bash
pytest tests/test_api.py
pytest tests/test_image_processing.py

3. Run tests with coverage:
bash
pytest --cov=app tests/

4. Run tests without FAL API (mock tests only):
bash
FAL_KEY="" pytest tests/ -v

## Project Structure

food-segmentation-api/
├── app/
│ ├── api/
│ │ ├── api_routes.py
│ │ ├── input_handler.py
│ │ └── segmentation_processor.py
│ ├── utils/
│ │ ├── area_calculation.py
│ │ ├── config.py
│ │ ├── fal_client_utils.py
│ │ ├── image_processing.py
│ │ └── logger.py
│ └── main.py
├── config/
│ └── settings.yaml
├── data/
│ ├── classifications/
│ └── images/
├── scripts/
│ ├── build_image.sh
│ └── run_dev.sh
├── tests/
│ ├── conftest.py
│ ├── test_api.py
│ ├── test_area_calculation.py
│ └── test_image_processing.py
├── .env.example
├── Dockerfile
├── requirements.txt
└── README.md

# to run fastapi server
uvicorn app.main:app --reload

# to run fastapi server with coverage
pytest --cov=app app/main.py

# to run the app with coverage and html report
pytest --cov=app --cov-report=html app/main.py