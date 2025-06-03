"""Configuration settings for the Weather App."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable overrides."""
    
    # API Configuration
    OPENWEATHER_API_KEY: str = Field(
        ...,
        env="OPENWEATHER_API_KEY",
        description="API key for OpenWeatherMap"
    )
    
    OPENWEATHER_BASE_URL: HttpUrl = Field(
        default="https://api.openweathermap.org/data/2.5/weather",
        description="Base URL for OpenWeatherMap API"
    )
    
    # Application Settings
    CACHE_TTL: int = Field(
        default=600,  # 10 minutes in seconds
        description="Time to live for cached weather data in seconds"
    )
    
    REQUEST_TIMEOUT: int = Field(
        default=10,  # seconds
        description="Timeout for API requests in seconds"
    )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


def get_settings() -> Settings:
    """
    Get application settings with environment variable overrides.
    
    Returns:
        Settings: Application settings instance
    
    Raises:
        ValueError: If required environment variables are missing
    """
    try:
        return Settings()
    except Exception as e:
        raise ValueError(
            "Failed to load settings. Please ensure you have set up your .env file "
            "with the required OPENWEATHER_API_KEY."
        ) from e


# Global settings instance
settings = get_settings()
