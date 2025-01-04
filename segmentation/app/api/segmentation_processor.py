from app.utils.fal_client_utils import subscribe_to_fal_service
from app.utils.area_calculation import calculate_pixel_area
from app.utils.image_processing import encode_image_to_base64
from app.utils.logger import get_logger
from app.utils.config import config
from app.schemas.classification_data_model import FoodItemClassification
from typing import List
import io
import requests

logger = get_logger(__name__)

async def process_segmentation(
    image_buffer: io.BytesIO,
    bounding_boxes: List[FoodItemClassification]
) -> dict:
    """
    Process image segmentation using FAL AI service.
    
    :param image_buffer: Input image buffer
    :param bounding_boxes: List of food items with bounding boxes
    :return: Dictionary containing segmentation results
    """
    try:
        # Encode image to base64
        data_uri = encode_image_to_base64(image_buffer)        
        # Convert bounding boxes to FAL AI format
        box_prompts = [
            {
                "x_min": item.bounding_box.x_min,
                "y_min": item.bounding_box.y_min,
                "x_max": item.bounding_box.x_max,
                "y_max": item.bounding_box.y_max
            }
            for item in bounding_boxes
        ]
        
        point_prompts = [
            {
                "x": item.bounding_box.x_min + (item.bounding_box.x_max - item.bounding_box.x_min) / 2,
                "y": item.bounding_box.y_min + (item.bounding_box.y_max - item.bounding_box.y_min) / 2,
                "label": item.class_name
            }
            for item in bounding_boxes
        ]

        # Define segmentation arguments using config
        arguments = {
            "image_url": data_uri,
            "output_format": config.get("fal", "output_format"),
            "box_prompts": box_prompts,
            "point_prompts": point_prompts
        }
        
        # Call FAL AI service using service name from config
        result = subscribe_to_fal_service(
            service_name=config.get("fal", "service_name"),
            arguments=arguments
        )
        
        # Process segmentation result
        # segmented_image_url = result.get("image", {}).get("url")
        segmented_image_info = result.get("image", {})
        segmented_image_url = segmented_image_info.get("url")
        if not segmented_image_url:
            raise ValueError("Segmentation failed: No output URL returned")
            
        # Verify the URL is accessible and is a PNG image
        try:
            response = requests.get(segmented_image_url, stream=True)
            content_type = response.headers.get('content-type', '')
            if 'image/' not in content_type:
                raise ValueError(f"Invalid content type: {content_type}. Expected image")
            # Read first few bytes to verify it's accessible without downloading whole image
            response.raw.read(1024)
        except requests.RequestException as e:
            raise ValueError(f"Could not access segmented image URL: {str(e)}")
        # Calculate pixel areas
        pixel_area, total_area = calculate_pixel_area(segmented_image_url)
        
        return {
            "segmented_image_url": segmented_image_url,
            "pixel_area": pixel_area,
            "total_area": total_area
        }
        
    except Exception as e:
        logger.error(f"Error in segmentation processing: {str(e)}")
        raise