import pytest
from app.utils.area_calculation import calculate_pixel_area
from PIL import Image
import numpy as np
import io

@pytest.fixture
def mock_segmented_image():
    """Create a mock segmented image for testing"""
    # Create a 100x100 image with known white and black pixels
    img = Image.new('L', (100, 100), color=0)  # Black background
    pixels = np.array(img)
    
    # Create a white square in the middle
    pixels[25:75, 25:75] = 255
    
    img = Image.fromarray(pixels)
    
    # Save to a temporary file
    img_path = "test_segmented.png"
    img.save(img_path)
    return img_path

def test_calculate_pixel_area(mock_segmented_image):
    """Test pixel area calculation"""
    pixel_area, total_area = calculate_pixel_area(mock_segmented_image)
    
    # Expected values based on our mock image
    expected_white_pixels = 50 * 50  # 50x50 white square
    expected_total_pixels = 100 * 100  # 100x100 image
    
    assert pixel_area == expected_white_pixels
    assert total_area == expected_total_pixels

def test_calculate_pixel_area_empty_image():
    """Test with completely black image"""
    # Create black image
    img = Image.new('L', (100, 100), color=0)
    img_path = "test_black.png"
    img.save(img_path)
    
    pixel_area, total_area = calculate_pixel_area(img_path)
    assert pixel_area == 0
    assert total_area == 100 * 100

def test_calculate_pixel_area_full_image():
    """Test with completely white image"""
    # Create white image
    img = Image.new('L', (100, 100), color=255)
    img_path = "test_white.png"
    img.save(img_path)
    
    pixel_area, total_area = calculate_pixel_area(img_path)
    assert pixel_area == 100 * 100
    assert total_area == 100 * 100
