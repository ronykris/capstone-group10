from pydantic import BaseModel
from typing import List

class BoundingBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

class FoodItemClassification(BaseModel):
    id: int
    class_name: str
    confidence: float
    bounding_box: BoundingBox

class ClassificationDataModel(BaseModel):
    id: int
    food_items: List[FoodItemClassification]