from pathlib import Path
from typing import List, Dict, Any
import yaml
from pydantic import BaseModel
from dotenv import load_dotenv
import os

class OpenAISettings(BaseModel):
    model: str
    max_tokens: int
    temperature: float
    timeout: int

class ImageSettings(BaseModel):
    max_size: List[int]
    supported_formats: List[str]
    quality: int
    min_confidence: float

class LoggingSettings(BaseModel):
    level: str
    format: str
    file: Dict[str, Any]
    console: Dict[str, Any]

class APISettings(BaseModel):
    prefix: str
    allowed_origins: List[str]
    timeout: int
    max_request_size: int

class AppSettings(BaseModel):
    name: str
    version: str
    description: str
    host: str
    port: int
    debug: bool

class Settings(BaseModel):
    app: AppSettings
    api: APISettings
    openai: OpenAISettings
    image: ImageSettings
    logging: LoggingSettings
    openai_api_key: str

    @classmethod
    def load_config(cls) -> 'Settings':
        # Load environment variables
        load_dotenv()

        # Load YAML config
        config_path = Path("config/settings.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Add environment variables
        config["openai_api_key"] = os.getenv("OPENAI_API_KEY")

        return cls(**config)

# Global settings instance
settings = Settings.load_config()