# Food Volume Estimation API

A FastAPI-based microservice for estimating food volume and nutritional content from images, using OpenAI GPT-4 Vision and advanced image processing techniques.

## Features

- Fast and efficient food volume estimation
- Integration with OpenAI GPT-4 Vision for advanced analysis
- Configurable image processing pipeline
- Comprehensive nutritional content estimation
- RESTful API design with FastAPI
- Centralized YAML configuration
- Docker support for easy deployment
- Structured logging with rotation
- Detailed error handling and validation

## Prerequisites

- Python 3.9+
- Docker (optional)
- OpenAI API key

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/volume-estimation-api.git
cd volume-estimation-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create configuration files:
```bash
cp .env.example .env
# Update .env with your OpenAI API key
```

5. Review and update `config/settings.yaml` as needed:
```yaml
# Example configuration structure
app:
  name: "Food Volume Estimation API"
  version: "1.0.0"
  port: 8003
  debug: true

api:
  prefix: "/api/v1"
  allowed_origins: ["*"]

# ... (see full settings.yaml for all options)
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t volume-estimation-api .
```

2. Run the container:
```bash
docker run -d --name volume-estimation-dev -p 8003:8003 -v "$(pwd)/app:/app/app" -v "$(pwd)/config:/app/config" --env-file .env  volume-estimation-api
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `APP_DEBUG`: Override debug mode (true/false)
- `LOG_LEVEL`: Override logging level (INFO/DEBUG/ERROR)

### YAML Configuration (`config/settings.yaml`)

#### Application Settings
```yaml
app:
  name: string
  version: string
  description: string
  host: string
  port: int
  debug: bool
```

#### API Settings
```yaml
api:
  prefix: string
  allowed_origins: list[string]
  timeout: int
  max_request_size: int
```

#### OpenAI Settings
```yaml
openai:
  model: string
  max_tokens: int
  temperature: float
  timeout: int
```

#### Image Processing Settings
```yaml
image:
  max_size: [width, height]
  supported_formats: list[string]
  quality: int
  min_confidence: float
```

#### Logging Settings
```yaml
logging:
  level: string
  format: string
  file:
    enabled: bool
    path: string
    max_size: int
    backup_count: int
  console:
    enabled: bool
```

## API Endpoints

### POST /api/v1/volume-estimate

Estimates food volume and nutritional content from an image.

#### Request

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `file`: Image file (supported formats: jpg, jpeg, png)
  - `classification_data`: JSON string containing classification results
  - `segmentation_data`: JSON string containing segmentation results

Example request using curl:
```bash
curl -X POST "http://localhost:8003/api/v1/volume-estimate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@food_image.jpg" \
  -F "classification_data={\"id\":1,\"food_items\":[...]}" \
  -F "segmentation_data={\"id\":1,\"food_items\":[...]}"
```

#### Response

```json
{
  "food_items": [
    {
      "class_name": "string",
      "macros": {
        "protein": float,
        "fat": float,
        "carbs": float
      },
      "calories": int,
      "confidence": float
    }
  ]
}
```

### GET /api/v1/healthcheck

Returns API health status.

## Development

### Project Structure

```
volume-estimation-api/
├── app/
│   ├── api/
│   │   ├── api_routes.py
│   │   ├── input_handler.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── image_processing.py
│   │   └── logger.py
│   └── main.py
├── config/
│   └── settings.yaml
├── logs/
│   └── .gitkeep
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_image_processing.py
└── [other files]
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py
```

## Logging

The API uses a structured logging system with the following features:

- Log rotation: Configurable file size and backup count
- Separate console and file logging
- Configurable log levels and formats
- Log directory: `logs/app.log`

### Log Levels

- DEBUG: Detailed debug information
- INFO: General operational information
- WARNING: Warning messages for potential issues
- ERROR: Error messages for failed operations
- CRITICAL: Critical errors that require immediate attention

## Performance Considerations

- Image processing:
  - Maximum dimensions: Configurable in settings.yaml
  - Supported formats: JPG, JPEG, PNG
  - Quality optimization: Configurable JPEG quality
  - Automatic resizing for large images

- API performance:
  - Configurable timeouts
  - Request size limits
  - Asynchronous processing
  - CORS configuration

## Error Handling

The API uses standard HTTP status codes with detailed error messages:

- 200: Success
- 400: Bad Request (invalid input)
- 422: Validation Error (invalid data format)
- 500: Internal Server Error

All errors return a JSON response:
```json
{
  "detail": "Error message description"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```bash
git commit -m "Add some feature"
```
4. Push to the branch:
```bash
git push origin feature/your-feature-name
```
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:
- Open an issue in the GitHub repository
- Check the documentation in `/api/docs`
- Contact the development team

## Changelog

See CHANGELOG.md for version history and updates.



## Response example 
```json
{
    "food_items": [
        {
            "class_name": "pasta",
            "macros": {
                "protein": 13.5,
                "fat": 7.0,
                "carbs": 90.0
            },
            "calories": 490,
            "confidence": 0.95
        }
    ]
}
```