from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
import logging

class FoodImageVisualizer:
    @staticmethod
    def draw_bounding_boxes(image_path: str, food_data: Dict[str, List[Dict]]) -> None:
        """
        Draw bounding boxes and labels on food items.
        
        Args:
            image_path (str): Path to the original image
            food_data (Dict): Classified food data with bounding boxes
        """
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 10)
            except IOError:
                font = ImageDraw.truetype(ImageDraw.core.font_path, 10)

            for food_item in food_data.get('food_items', []):
                bbox = food_item.get('bounding_box', {})
                if bbox:
                    draw.rectangle(
                        [(bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2'])], 
                        outline="red", 
                        width=2
                    )
                    label = f"{food_item.get('name', 'Unknown')}"
                    draw.text(
                        (bbox['x1'], bbox['y1'] - 15), 
                        label, 
                        fill="red",
                        font=font
                    )

            img.show()
        except Exception as e:
            logging.error(f"Visualization error: {e}")