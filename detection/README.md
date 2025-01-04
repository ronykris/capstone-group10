# FastAPI Application

## Overview
This is a FastAPI application that provides Classification model using YOLO.

## Prerequisites
Make sure you have the following software installed:

- Python 3.8+
- pip (Python package installer)

## Installation

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the FastAPI application, execute the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- `main` refers to your main Python file (without the `.py` extension).
- `app` refers to the FastAPI instance in your main file.

## Accessing the API

Once the server is running, you can access the API at:

## Api calls
1. */healthcheck*: To check helth of the service. 
2. */detect*: payload is image file.
