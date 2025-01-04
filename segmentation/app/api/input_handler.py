from fastapi import UploadFile, HTTPException
from app.utils.logger import get_logger
from app.schemas.classification_data_model import ClassificationDataModel, FoodItemClassification
import io
from typing import Tuple
# import aiofiles  # For async file operations

logger = get_logger(__name__)

async def get_classification_data(image_id: int) -> Tuple[ClassificationDataModel, io.BytesIO]:
    """
    Retrieve classification data and image for a given ID from data folder.
    
    :param image_id: ID of the image to retrieve
    :return: Tuple of classification data and image buffer
    """
    try:
        if image_id <= 0:
            logger.error(f"Invalid image ID: {image_id}")
            raise HTTPException(
                status_code=404, 
                detail="Image not found"
            )

        # Load classification data from JSON file
        json_path = f"data/classifications/{image_id}.json"
        try:
            with open(json_path, 'r') as f:
                import json
                data = json.load(f)
                classification_data = ClassificationDataModel(**data)
        except FileNotFoundError:
            logger.error(f"Classification data not found for image {image_id}")
            raise HTTPException(
                status_code=404,
                detail="Classification data not found"
            )

        # Load image from file
        image_path = f"data/images/{image_id}.jpg"
        try:
            with open(image_path, 'rb') as f:
                image_buffer = io.BytesIO(f.read())
        except FileNotFoundError:
            logger.error(f"Image file not found for ID {image_id}")
            raise HTTPException(
                status_code=404,
                detail="Image file not found"
            )

        logger.info(f"Retrieved classification data and image for ID {image_id}")
        return classification_data, image_buffer

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving classification data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_input(
    file: UploadFile,
    classification_data: ClassificationDataModel
) -> Tuple[io.BytesIO, ClassificationDataModel]:
    """
    Process the uploaded image file and classification data.
    
    :param file: Uploaded image file
    :param classification_data: Classification data including bounding boxes
    :return: Tuple of processed image buffer and validated classification data
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.jpeg', '.jpg', '.png')):
            logger.error(f"Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail="File must be a JPEG or PNG image")
        
        # Read image content
        content = await file.read()
        buffer = io.BytesIO(content)
        
        # Validate classification data
        if not classification_data.food_items:
            logger.error("No food items found in classification data")
            raise HTTPException(status_code=400, detail="Classification data must contain food items")
        
        logger.info("Input image and classification data processed successfully")
        return buffer, classification_data
        
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_segmentation_request(
    segmentation_id: int
) -> dict:
    """
    Process a segmentation request by ID.
    
    :param segmentation_id: ID of the segmentation to retrieve
    :return: Dictionary containing the segmentation data
    """
    try:
        # Here you would typically fetch the segmentation data from your database
        # This is a placeholder implementation
        logger.info(f"Processing segmentation request for ID: {segmentation_id}")
        
        # Implement your database query here
        # segmentation_data = await db.get_segmentation(segmentation_id)
        
        # For now, return a mock response
        if segmentation_id <= 0:
            raise HTTPException(status_code=404, detail="Segmentation not found")
            
        return {"segmentation_id": segmentation_id}
        
    except Exception as e:
        logger.error(f"Error processing segmentation request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
