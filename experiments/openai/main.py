import os
from dotenv import load_dotenv
import logging

from src.food_classifier import FoodClassifier
from src.visualization import FoodImageVisualizer
from utils.logging_config import setup_logging
import json

def main():
    # Load environment and configuration
    load_dotenv()
    setup_logging()

    # Initialize classifier
    classifier = FoodClassifier(
        api_key=os.getenv("OPENAI_KEY"),
        model=os.getenv("MODEL"),
        prompt_path="config/prompts.json"
    )

    # Process image
    image_path = "data/20151221132515.jpg"
    food_data = classifier.classify_food(image_path)

    if food_data:
        logging.info("Food classification successful.")
        print(food_data)
        
        # Visualize results
        FoodImageVisualizer.draw_bounding_boxes(image_path, food_data)
    else:
        logging.error("Food classification failed.")

if __name__ == "__main__":
    main()