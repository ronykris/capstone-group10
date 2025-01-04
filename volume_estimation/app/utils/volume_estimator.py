from typing import Tuple
import numpy as np
from PIL import Image
import openai

from ..lib.models import (
    ClassificationDataModel, 
    SegmentationDataModel, 
    VolumeEstimationDataModel, 
    FoodItemVolumeEstimation, 
    Macros
    )
from .config import settings

class VolumeEstimator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    async def estimate(
        self,
        image: Image.Image,
        classification: ClassificationDataModel,
        segmentation: SegmentationDataModel
    ) -> VolumeEstimationDataModel:
        # Prepare combined data for OpenAI prompt
        prompt = self._prepare_prompt(classification, segmentation)
        
        # Get volume and nutrition estimates from OpenAI
        response = await self._get_openai_estimation(prompt, image)
        
        # # Process and validate the response
        # result = self._process_response(response, classification, segmentation)
        
        return response

    def _prepare_prompt(
        self,
        classification: ClassificationDataModel,
        segmentation: SegmentationDataModel
    ) -> str:
        prompt = """Analyze the provided image and data to estimate food volumes and nutritional content.
        
        Classification data shows the following items: {class_items}
        
        Segmentation data provides the following pixel areas: {seg_items}
        
        For each food item:
        1. Use the pixel area and total area to estimate the volume
        2. Based on the estimated volume, calculate:
           - Protein, fat, and carbohydrate content in grams
           - Total calories
        
        Provide structured output following the VolumeEstimationDataModel format.
        """
        
        class_items = ", ".join(
            f"{item.class_name} (confidence: {item.confidence})"
            for item in classification.food_items
        )
        
        seg_items = ", ".join(
            f"{item.class_name} (pixel area: {item.pixel_area}, total area: {item.total_area})"
            for item in segmentation.food_items
        )
        
        return prompt.format(class_items=class_items, seg_items=seg_items)

    async def _get_openai_estimation(self, prompt: str, image: Image.Image) -> dict:
        response = self.client.beta.chat.completions.parse(
            model=settings.openai.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in food volume and nutritional content estimation."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": self._encode_image(image)}
                        }
                    ]
                }
            ],
            response_format=VolumeEstimationDataModel
        )
        return response.choices[0].message.parsed

    # Not in use
    def _process_response(
        self,
        response: dict,
        classification: ClassificationDataModel,
        segmentation: SegmentationDataModel
    ) -> VolumeEstimationDataModel:
        # Convert OpenAI response to VolumeEstimationDataModel
        food_items = []
        
        for class_item in classification.food_items:
            # Find matching segmentation data
            seg_item = next(
                (s for s in segmentation.food_items if s.class_name == class_item.class_name),
                None
            )
            
            if seg_item:
                # Create food item with volume-based estimations
                food_item = FoodItemVolumeEstimation(
                    class_name=class_item.class_name,
                    macros=Macros(
                        protein=response['items'][class_item.class_name]['protein'],
                        fat=response['items'][class_item.class_name]['fat'],
                        carbs=response['items'][class_item.class_name]['carbs']
                    ),
                    calories=response['items'][class_item.class_name]['calories'],
                    confidence=class_item.confidence
                )
                food_items.append(food_item)
        
        return VolumeEstimationDataModel(
            food_items=food_items
        )

    def _encode_image(self, image: Image.Image) -> str:
        import base64
        import io
        
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"