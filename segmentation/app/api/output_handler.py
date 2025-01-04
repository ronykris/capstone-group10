from app.schemas.segmentation_data_model import SegmentationDataModel, FoodItemSegmentation
from app.utils.logger import get_logger

logger = get_logger(__name__)

def format_response(segmentation_result: dict) -> SegmentationDataModel:
    """
    Format the segmentation results into the response model.
    
    :param segmentation_result: Dictionary containing segmentation results
    :return: Formatted SegmentationDataModel
    """
    try:
        # Create FoodItemSegmentation instance
        food_item = FoodItemSegmentation(
            id=1,  # You might want to generate this dynamically
            class_name="food_item",  # This could come from a classifier
            masked_image=segmentation_result["segmented_image_url"],
            pixel_area=segmentation_result["pixel_area"],
            total_area=segmentation_result["total_area"]
        )
        
        # Create final response
        response = SegmentationDataModel(
            id=1,  # You might want to generate this dynamically
            food_items=[food_item]
        )
        
        logger.info("Response formatted successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        raise
