import fal_client
from app.utils.logger import get_logger
from app.utils.config import config

logger = get_logger(__name__)

def initialize_fal_client():
    """Initialize FAL client with API key from config"""
    api_key = config.get("fal", "api_key")
    if not api_key:
        logger.error("FAL API key not configured")
        raise ValueError("FAL API key is required")
    
    fal_client.api_key = api_key

def subscribe_to_fal_service(service_name: str, arguments: dict):
    """Subscribe to a FAL service"""
    try:
        # Ensure client is initialized
        initialize_fal_client()
        
        result = fal_client.subscribe(
            service_name,
            arguments=arguments,
            with_logs=True
        )
        return result
    except Exception as e:
        logger.error(f"Failed to subscribe to service {service_name}: {str(e)}")
        raise
