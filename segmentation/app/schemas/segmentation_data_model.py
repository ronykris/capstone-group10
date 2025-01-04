from pydantic import BaseModel

class FoodItemSegmentation(BaseModel):
    id: int
    class_name: str
    masked_image: str  # Path or base64-encoded string
    pixel_area: int
    total_area: int

class SegmentationDataModel(BaseModel):
    id: int
    food_items: list[FoodItemSegmentation]
