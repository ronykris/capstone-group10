from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class Macros(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["protein", "fat", "carbs"],
            "additionalProperties": False
        }
    )
    protein: float = Field(..., description="Protein content in grams")
    fat: float = Field(..., description="Fat content in grams")
    carbs: float = Field(..., description="Carbohydrate content in grams")

class BoundingBox(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["x1", "y1", "x2", "y2"],
            "additionalProperties": False
        }
    )
    x1: float = Field(..., description="Top-left x-coordinate (0-1)")
    y1: float = Field(..., description="Top-left y-coordinate (0-1)")
    x2: float = Field(..., description="Bottom-right x-coordinate (0-1)")
    y2: float = Field(..., description="Bottom-right y-coordinate (0-1)")

class FoodItem(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["name", "macros", "calories", "bounding_box"],
            "additionalProperties": False
        }
    )
    name: str = Field(..., description="Name of the food item")
    macros: Macros = Field(..., description="Macronutrient breakdown")
    calories: int = Field(..., description="Total calories")
    bounding_box: BoundingBox = Field(..., description="Bounding box coordinates")
    confidence: Optional[float] = Field(None, description="Confidence score of detection")

class ImageAnalysis(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "required": ["image_dimensions", "food_items"],
            "additionalProperties": False
        }
    )
    image_dimensions: List[int] = Field(
        ..., 
        description="Original image dimensions as a list [width, height]"
    )
    food_items: List[FoodItem] = Field(
        default_factory=list, 
        description="List of detected food items"
    )