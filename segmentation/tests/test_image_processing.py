import pytest
from app.utils.image_processing import encode_image_to_base64
import io
from PIL import Image
import base64

@pytest.fixture
def mock_image_buffer():
    """Create a mock image buffer for testing"""
    img = Image.new('RGB', (100, 100), color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def test_encode_image_to_base64(mock_image_buffer):
    """Test base64 encoding of image"""
    data_uri = encode_image_to_base64(mock_image_buffer)
    
    # Verify the data URI format
    assert data_uri.startswith('data:image/jpeg;base64,')
    
    # Verify the base64 content is valid
    base64_content = data_uri.split(',')[1]
    try:
        decoded = base64.b64decode(base64_content)
        assert len(decoded) > 0
    except Exception:
        pytest.fail("Invalid base64 encoding")

def test_encode_image_to_base64_empty_buffer():
    """Test encoding with empty buffer"""
    empty_buffer = io.BytesIO()
    with pytest.raises(ValueError, match="Empty image buffer"):
        encode_image_to_base64(empty_buffer)

def test_encode_image_to_base64_invalid_image():
    """Test encoding with invalid image data"""
    invalid_buffer = io.BytesIO(b"not an image")
    with pytest.raises(ValueError, match="Invalid image data"):
        encode_image_to_base64(invalid_buffer)

def test_encode_image_to_base64_corrupted_image():
    """Test encoding with corrupted image data"""
    # Create a partially valid but corrupted PNG
    corrupted_buffer = io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'corrupted data')
    with pytest.raises(ValueError):
        encode_image_to_base64(corrupted_buffer)
