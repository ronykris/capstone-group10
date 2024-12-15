import json
import logging
from typing import Optional, Tuple, Dict, Any

import openai
from pydantic import ValidationError, TypeAdapter

from src.image_processing import ImageProcessor
from src.food_models import ImageAnalysis

class FoodClassifier:
    def __init__(self, api_key: str, model: str, prompt_path: str):
        """
        Initialize the food classifier with structured output support.
        
        Args:
            api_key (str): OpenAI API key
            model (str): OpenAI model to use
            prompt_path (str): Path to prompts configuration
        """
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
        with open(prompt_path, 'r') as f:
            self.prompts = json.load(f)
            

    def classify_food(self, image_path: str, target_size: Tuple[int, int] = (512, 512)) -> Optional[ImageAnalysis]:
        """
        Classify food items in an image with structured output.
        
        Args:
            image_path (str): Path to the image
            target_size (Tuple[int, int]): Image resize dimensions
        
        Returns:
            Optional[ImageAnalysis]: Classified food data with structured format
        """
        try:
            # Resize and process image
            image = ImageProcessor.resize_image(image_path, target_size)
            if not image:
                return None

            encoded_image = ImageProcessor.encode_image(image)
            if not encoded_image:
                return None

            # Format prompt with image dimensions
            prompt_template = self.prompts['food_classification']['v1']
            formatted_prompt = prompt_template.format(
                width=target_size[0], 
                height=target_size[1]
            )

            # Prepare messages for API call
            messages = [
                {
                    "role": "system",
                    "content": "You are a precise food detection and nutrition analysis AI. Provide structured, accurate information."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": formatted_prompt
                        },
                        {"type": "image_url", "image_url": {"url": encoded_image}}
                    ]
                }
            ]
            
            # Make API call with JSON output
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=ImageAnalysis
            )

            # Extract and parse the JSON response
            result = response.choices[0].message
            logging.info(f"Raw API Response: {result}")

            try:
                return result.parsed
            except ValidationError as ve:
                logging.error(f"JSON validation error: {ve}")
                return None

        except Exception as e:
            logging.error(f"Food classification error: {e}")
            return None