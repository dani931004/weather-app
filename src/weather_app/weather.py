"""Core functionality for fetching and processing weather data."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Optional, Union, Any

import requests
from pydantic import BaseModel, Field, validator

from . import exceptions
from .config import settings


class WeatherCondition(BaseModel):
    """Represents weather condition details."""
    id: int
    main: str
    description: str
    icon: str


class MainWeatherData(BaseModel):
    """Main weather data fields."""
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class WindData(BaseModel):
    """Wind data fields."""
    speed: float
    deg: int
    gust: Optional[float] = None


class CloudData(BaseModel):
    """Cloud coverage data."""
    all: int


class SystemData(BaseModel):
    """System data from the API response."""
    type: Optional[int] = None
    id: Optional[int] = None
    country: str
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    """Complete weather data response model."""
    coord: Dict[str, float]
    weather: list[WeatherCondition]
    base: str
    main: MainWeatherData
    visibility: int
    wind: WindData
    clouds: CloudData
    dt: int
    sys: SystemData
    timezone: int
    id: int
    name: str
    cod: int

    @property
    def condition(self) -> WeatherCondition:
        """Get the primary weather condition."""
        return self.weather[0] if self.weather else None


class WeatherClient:
    """Client for interacting with the OpenWeatherMap API."""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the weather client.
        
        Args:
            api_key: OpenWeatherMap API key
            base_url: Base URL for the API
        """
        self.api_key = api_key or settings.OPENWEATHER_API_KEY
        self.base_url = base_url or str(settings.OPENWEATHER_BASE_URL)
        self.session = requests.Session()
        
    def get_weather_by_city(
        self,
        city: str,
        country_code: str = None,
        units: str = 'metric',
        lang: str = 'en'
    ) -> WeatherResponse:
        """Get current weather data for a city.
        
        Args:
            city: City name
            country_code: Optional country code (e.g., 'us', 'uk')
            units: Units of measurement ('metric' or 'imperial')
            lang: Language for weather descriptions
            
        Returns:
            WeatherResponse object containing weather data
            
        Raises:
            LocationNotFoundError: If the location is not found
            APIError: For other API-related errors
        """
        params = {
            'q': f"{city},{country_code}" if country_code else city,
            'appid': self.api_key,
            'units': units,
            'lang': lang
        }
        
        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('cod') != 200:
                self._handle_api_error(data.get('cod', 500), data.get('message', 'Unknown error'))
                
            return WeatherResponse(**data)
            
        except requests.exceptions.RequestException as e:
            raise exceptions.APIError(
                status_code=getattr(e.response, 'status_code', 500),
                message=str(e)
            ) from e
    
    def _handle_api_error(self, status_code: int, message: str) -> None:
        """Handle API errors based on status code."""
        # Convert status_code to int if it's a string
        status_code_int = int(status_code) if isinstance(status_code, str) else status_code
        
        if status_code_int == 401:
            raise exceptions.InvalidAPIKeyError(status_code_int, message)
        elif status_code_int == 404:
            raise exceptions.LocationNotFoundError(f"Location not found: {message}")
        elif status_code_int == 429:
            raise exceptions.RateLimitExceededError(status_code_int, message)
        else:
            raise exceptions.APIError(status_code_int, message)
    
    def format_weather_output(
        self,
        weather_data: WeatherResponse,
        output_format: str = 'json'
    ) -> str:
        """Format weather data for output.
        
        Args:
            weather_data: Weather data to format
            output_format: Output format ('json' or 'text')
            
        Returns:
            Formatted weather data as string
        """
        if output_format.lower() == 'json':
            return weather_data.json(indent=2, exclude_none=True)
        else:
            # Simple text format
            data = weather_data.dict()
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']
            
            return (
                f"Weather in {data['name']}, {data['sys']['country']}:\n"
                f"{weather['main']} ({weather['description']})\n"
                f"Temperature: {main['temp']}°C (feels like {main['feels_like']}°C)\n"
                f"Humidity: {main['humidity']}%\n"
                f"Wind: {wind['speed']} m/s, {wind['deg']}°\n"
                f"Pressure: {main['pressure']} hPa"
            )
