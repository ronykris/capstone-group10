import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the application root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def pytest_configure(config):
    """Configure test environment"""
    # Load test environment variables
    test_env = root_dir / "tests" / ".env.test"
    if test_env.exists():
        load_dotenv(test_env)
    else:
        # Load default .env file if test env doesn't exist
        load_dotenv(root_dir / ".env")

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    # Use the actual FAL key from .env for integration tests
    if not os.getenv("FAL_KEY"):
        # If no FAL_KEY is set, skip tests that require FAL API
        pytest.skip("FAL_KEY not set")
    
    os.environ["APP_ENV"] = "test"
    
    yield
    
    # Cleanup after tests
    if "APP_ENV" in os.environ:
        del os.environ["APP_ENV"] 