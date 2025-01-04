from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
"""
Clasification api response model
"""
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
    
    
"""
Segmentation api response model.
"""
class FoodItemSegmentation(BaseModel):
    id: int
    class_name: str
    masked_image: str  # Path or base64-encoded string
    pixel_area: int
    total_area: int

class SegmentationDataModel(BaseModel):
    id: int
    food_items: list[FoodItemSegmentation]
    
    
"""
Volume estimation api response model
"""
class Macros(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["protein", "fat", "carbs", "fiber"],
            "additionalProperties": False
        }
    )
    protein: float = Field(..., description="Protein content in grams")
    fat: float = Field(..., description="Fat content in grams")
    carbs: float = Field(..., description="Carbohydrate content in grams")
    fiber: float = Field(..., description="Fiber content in grams")
    
class FoodItemVolumeEstimation(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["name", "macros", "calories", "bounding_box"],
            "additionalProperties": False
        }
    )
    class_name: str = Field(..., description="Name of the food item")
    macros: Macros = Field(..., description="Macronutrient breakdown")
    calories: int = Field(..., description="Total calories")
    confidence: Optional[float] = Field(None, description="Confidence score of detection")

class VolumeEstimationDataModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["summary", "food_items"],
            "additionalProperties": False
        }
    )
    food_items: List[FoodItemVolumeEstimation] = Field(
        default_factory=list, 
        description="List of detected food items"
    )
    summary: str = Field(..., description="Short summary about the food conent, and benefits about it")
    