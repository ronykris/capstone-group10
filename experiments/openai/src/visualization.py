from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
import logging
from .food_models import ImageAnalysis
from .image_processing import ImageProcessor
from typing import Optional, Tuple

class FoodImageVisualizer:
    @staticmethod
    def draw_bounding_boxes(image_path: str, food_data: ImageAnalysis, resize_target: Tuple[int, int] = (512, 512)) -> Optional[str]:
        """
        Draw bounding boxes and labels on food items, resize image, and encode as base64.

        Args:
            image_path (str): Path to the original image
            food_data (ImageAnalysis): Classified food data with bounding boxes
            resize_target (Tuple[int, int]): Desired dimensions for resizing

        Returns:
            Optional[str]: Base64 encoded image with annotations or None if error occurs
        """
        try:
            # Resize the image
            img = ImageProcessor.resize_image(image_path, resize_target)
            if img is None:
                return None

            draw = ImageDraw.Draw(img)

            # Try to load a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 15)
            except IOError:
                font = ImageFont.load_default()

            original_width, original_height = food_data.image_dimensions
            target_width, target_height = resize_target
            margin_h = 10

            # Draw bounding boxes and labels
            for food_item in food_data.food_items:
                bbox = food_item.bounding_box

                # Scale bounding box to resized dimensions
                scaled_bbox = (
                    bbox.x1 * target_width, bbox.y1 * target_height,
                    bbox.x2 * target_width, bbox.y2 * target_width
                )
                draw.rectangle(
                    [(scaled_bbox[0], scaled_bbox[1]), (scaled_bbox[2], scaled_bbox[3])], 
                    outline="red", 
                    width=2
                )
                label = f"{food_item.name}"
                macros = f"Protein: {food_item.macros.protein}g, Fat: {food_item.macros.fat}g, Carbs: {food_item.macros.carbs}g"

                draw.text(
                    (scaled_bbox[0], scaled_bbox[1] - 20), 
                    label, 
                    fill="red",
                    font=font
                )
                # draw.text(
                #     (scaled_bbox[0], scaled_bbox[1] - 5), 
                #     macros, 
                #     fill="blue",
                #     font=font
                # )
            encoded_image = ImageProcessor.encode_image(img)
            try:
                ImageProcessor.display_encoded_image(encoded_image)
            except Exception as e:
                logging.error(f"Draw image error: {e}")

            # Encode image to base64
            return encoded_image
        except Exception as e:
            logging.error(f"Visualization error: {e}")
            return None
