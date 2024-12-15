import json
import logging
from typing import Optional, Dict, List

import openai
from openai.types.chat import ChatCompletion

from src.image_processing import ImageProcessor

class FoodClassifier:
    def __init__(self, api_key: str, model: str, prompt_path: str):
        """
        Initialize the food classifier.
        
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

    def classify_food(self, image_path: str, target_size: tuple[int, int] = (512, 512)) -> Optional[Dict]:
        """
        Classify food items in an image.
        
        Args:
            image_path (str): Path to the image
            target_size (Tuple[int, int]): Image resize dimensions
        
        Returns:
            Optional[Dict]: Classified food data
        """
        try:
            image = ImageProcessor.resize_image(image_path, target_size)
            if not image:
                return None

            encoded_image = ImageProcessor.encode_image(image)
            if not encoded_image:
                return None

            prompt = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.prompts['food_classification']['v1']
                        },
                        {"type": "image_url", "image_url": {"url": encoded_image}}
                    ]
                }
            ]

            response: ChatCompletion = self.client.chat.completions.create(
                model=self.model, 
                messages=prompt, 
                max_tokens=1024,
                response_format={"type": "json_object"}
            )

            result = response.choices[0].message.content.strip()
            return json.loads(result)

        except Exception as e:
            logging.error(f"Food classification error: {e}")
            return None