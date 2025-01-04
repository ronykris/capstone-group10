from PIL import Image
import base64
import io
from app.utils.logger import get_logger

logger = get_logger(__name__)

def encode_image_to_base64(image_buffer: io.BytesIO) -> str:
    """
    Encode an image buffer to base64 data URI.
    
    :param image_buffer: Image buffer to encode
    :return: Base64 encoded data URI
    :raises ValueError: If image buffer is invalid or empty
    """
    try:
        # Verify buffer is not empty
        if image_buffer.getbuffer().nbytes == 0:
            raise ValueError("Empty image buffer")

        # Try to open the image to validate it
        try:
            image = Image.open(image_buffer)
            image.verify()  # Verify it's actually an image
            image_buffer.seek(0)  # Reset buffer position after verify
        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")

        # Convert to JPEG format
        image = Image.open(image_buffer)
        output_buffer = io.BytesIO()
        image.convert('RGB').save(output_buffer, format='JPEG')
        
        # Encode to base64
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        # Create data URI
        data_uri = f"data:image/jpeg;base64,{encoded_image}"
        
        logger.debug("Image successfully encoded to base64")
        return data_uri
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        raise ValueError(f"Failed to encode image: {str(e)}") 