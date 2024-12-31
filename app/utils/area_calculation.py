from PIL import Image
import numpy as np
import requests
from io import BytesIO

def calculate_pixel_area(segmented_image_url: str):
    '''Calculate the pixel area of a segmented image from URL or local path'''
    try:
        # Check if the input is a URL
        if segmented_image_url.startswith(('http://', 'https://')):
            # Download image from URL
            response = requests.get(segmented_image_url)
            response.raise_for_status()  # Raise exception for bad status codes
            image_data = BytesIO(response.content)
            segmented_image = Image.open(image_data).convert("L")
        else:
            # Load local file
            segmented_image = Image.open(segmented_image_url).convert("L")

        # Convert the image to a NumPy array
        image_array = np.array(segmented_image)

        # Define pixel intensity thresholds
        white_threshold = 250  # Adjust for near-white

        # Calculate the area of white pixels
        white_pixel_count = np.sum(image_array >= white_threshold)

        # Get total pixels
        total_pixels = image_array.size

        return white_pixel_count, total_pixels

    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
