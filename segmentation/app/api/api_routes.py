from fastapi import APIRouter, UploadFile, File, Body, HTTPException, Form
from app.api.input_handler import process_input, get_classification_data
from app.api.segmentation_processor import process_segmentation
from app.api.output_handler import format_response
from app.utils.logger import get_logger
from app.utils.config import config
from app.schemas.segmentation_data_model import SegmentationDataModel
from app.schemas.classification_data_model import ClassificationDataModel
import io

logger = get_logger(__name__)
router = APIRouter()

@router.get('/healthcheck')
async def get_health_check():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary indicating the service health status.
    """
    return {"status": "ok"}


@router.get("/classification/{image_id}", response_model=ClassificationDataModel)
async def get_classification(image_id: int):
    """
    Get classification data and image for a specific ID.
    
    :param image_id: ID of the image to retrieve
    :return: Classification data including image and bounding boxes
    """
    try:
        # Get classification data and image
        classification_data, image_buffer = await get_classification_data(image_id)
        
        # Return only the classification data
        logger.info(f"Successfully retrieved classification {image_id}")
        return classification_data
        
    except Exception as e:
        logger.error(f"Error retrieving classification: {str(e)}")
        raise

@router.post("/segment", response_model=SegmentationDataModel)
async def segment_image(
    file: UploadFile = File(...),
    classification_data: str = Form(...)
):
    """
    Process and segment an uploaded image with classification data.
    """
    try:
        # Parse classification data from JSON string
        try:
            classification_data = ClassificationDataModel.parse_raw(classification_data)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail="Invalid classification data format"
            )

        # Validate file size
        max_size = config.get("image", "max_size_mb") * 1024 * 1024
        content = await file.read()
        if len(content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {config.get('image', 'max_size_mb')}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
            
        # Validate file extension
        if not any(file.filename.lower().endswith(ext) 
                  for ext in config.get("image", "allowed_extensions")):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {config.get('image', 'allowed_extensions')}"
            )
        
        # Process the input image and classification data
        image_buffer = io.BytesIO(content)
        
        # Perform segmentation using the validated data
        segmentation_result = await process_segmentation(
            image_buffer=image_buffer,
            bounding_boxes=classification_data.food_items
        )
        
        # Format the response
        response = format_response(segmentation_result)
        
        logger.info("Image segmentation completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
