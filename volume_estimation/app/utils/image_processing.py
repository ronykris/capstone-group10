from typing import Optional, Tuple
from PIL import Image
import io
import logging
from fastapi import UploadFile, HTTPException
from pathlib import Path
from .config import settings

logger = logging.getLogger(__name__)

class ImageProcessor:
    async def process_upload(self, file: UploadFile) -> Image.Image:
        """Process uploaded image file according to configuration settings."""
        try:
            # Validate file format
            ext = Path(file.filename).suffix.lower().lstrip('.')
            if ext not in settings.image.supported_formats:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image format. Supported formats: {settings.image.supported_formats}"
                )

            # Read image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))

            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Resize if necessary
            if self._needs_resize(image.size):
                image = self._resize_image(image)

            return image

        except Exception as e:
            logger.error(f"Image processing error: {e}")
            raise HTTPException(status_code=400, detail="Invalid image file")

    def _needs_resize(self, size: Tuple[int, int]) -> bool:
        """Check if image needs resizing based on config settings."""
        max_width, max_height = settings.image.max_size
        return size[0] > max_width or size[1] > max_height

    def _resize_image(self, image: Image.Image) -> Image.Image:
        """Resize image while maintaining aspect ratio."""
        max_width, max_height = settings.image.max_size
        ratio = min(max_width / image.width, max_height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.LANCZOS)

    def save_processed_image(self, image: Image.Image, path: Path) -> None:
        """Save processed image with configured quality settings."""
        image.save(path, "JPEG", quality=settings.image.quality)