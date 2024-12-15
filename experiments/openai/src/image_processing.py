import logging
from typing import Optional, Tuple
from PIL import Image
import base64
import io

class ImageProcessor:
    @staticmethod
    def resize_image(image_path: str, target_size: Tuple[int, int] = (512, 512)) -> Optional[Image.Image]:
        """
        Resize an image with high-quality interpolation.
        
        Args:
            image_path (str): Path to the input image
            target_size (Tuple[int, int]): Desired image dimensions
        
        Returns:
            Optional[Image.Image]: Resized image or None if processing fails
        """
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")  # Ensure RGB format
            img = img.resize(target_size, Image.LANCZOS)
            return img
        except FileNotFoundError:
            logging.error(f"Image file '{image_path}' not found.")
            return None
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return None

    @staticmethod
    def encode_image(image: Image.Image) -> Optional[str]:
        """
        Encode a PIL Image to base64.
        
        Args:
            image (Image.Image): PIL Image to encode
        
        Returns:
            Optional[str]: Base64 encoded image or None
        """
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{img_str}"
        except Exception as e:
            logging.error(f"Image encoding error: {e}")
            return None