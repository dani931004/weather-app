#!/usr/bin/env python3
"""
Weather App - Simple command-line tool to fetch weather data

Example usage:
    python weather.py "London,uk" --pretty
    python weather.py "New York" --units imperial --output weather.json
"""
import json
import os
import sys
from typing import Optional, Dict, Any

import click
from dotenv import load_dotenv

from src.weather_app.weather import WeatherClient, WeatherResponse
from src.weather_app import exceptions

# Load environment variables from .env file if it exists
load_dotenv()

def format_weather_data(weather_data: Dict[str, Any], units: str) -> Dict[str, Any]:
    """Format weather data into a structured dictionary."""
    temp_unit = '°C' if units == 'metric' else '°F'
    speed_unit = 'm/s' if units == 'metric' else 'mph'
    
    # Safely access nested dictionary keys
    coord = weather_data.get('coord', {})
    main = weather_data.get('main', {})
    weather = weather_data.get('weather', [{}])[0]
    wind = weather_data.get('wind', {})
    sys = weather_data.get('sys', {})
    
    return {
        'location': {
            'city': weather_data.get('name', 'Unknown'),
            'country': sys.get('country', ''),
            'coordinates': {
                'lat': coord.get('lat'),
                'lon': coord.get('lon')
            }
        },
        'weather': {
            'main': weather.get('main', ''),
            'description': weather.get('description', ''),
            'icon': weather.get('icon', ''),
            'temperature': {
                'current': main.get('temp'),
                'feels_like': main.get('feels_like'),
                'min': main.get('temp_min'),
                'max': main.get('temp_max'),
                'unit': temp_unit
            },
            'pressure': f"{main.get('pressure')} hPa" if main.get('pressure') is not None else 'N/A',
            'humidity': f"{main.get('humidity')}%" if main.get('humidity') is not None else 'N/A',
            'visibility': f"{weather_data.get('visibility', 0) / 1000:.1f} km" if weather_data.get('visibility') else 'N/A',
            'wind': {
                'speed': f"{wind.get('speed', 0)} {speed_unit}",
                'degree': wind.get('deg'),
                'gust': wind.get('gust')
            },
            'clouds': f"{weather_data.get('clouds', {}).get('all')}%" if weather_data.get('clouds', {}).get('all') is not None else 'N/A',
            'rain': weather_data.get('rain'),
            'snow': weather_data.get('snow'),
            'sun': {
                'sunrise': sys.get('sunrise'),
                'sunset': sys.get('sunset')
            },
            'timezone': weather_data.get('timezone'),
            'timestamp': weather_data.get('dt')
        }
    }

def get_weather(
    location: str,
    country: Optional[str] = None,
    units: str = 'metric',
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Fetch weather data for a location."""
    if not api_key:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            raise ValueError(
                "API key is required. Set OPENWEATHER_API_KEY environment variable "
                "or pass it with --api-key"
            )
    
    client = WeatherClient(api_key=api_key)
    
    # If location contains a comma, split into city and country
    if ',' in location:
        location_parts = [p.strip() for p in location.split(',')]
        city = location_parts[0]
        country = location_parts[1] if len(location_parts) > 1 else country
    else:
        city = location
    
    try:
        # Get the raw weather data as a dictionary
        weather_data = client.get_weather_by_city(
            city=city,
            country_code=country,
            units=units
        )
        # Convert Pydantic model to dict if needed
        if hasattr(weather_data, 'model_dump'):
            weather_data = weather_data.model_dump()
        return format_weather_data(weather_data, units)
    except exceptions.WeatherAppError as e:
        raise ValueError(f"Failed to fetch weather data: {str(e)}")

def main():
    """Main entry point for the script."""
    try:
        import argparse
        
        parser = argparse.ArgumentParser(description='Get current weather information')
        parser.add_argument('location', help='City name (e.g., "London" or "London,uk")')
        parser.add_argument('--country', '-c', help='Country code (e.g., us, gb, jp)')
        parser.add_argument('--units', '-u', choices=['metric', 'imperial'], 
                          default='metric', help='Units of measurement')
        parser.add_argument('--output', '-o', help='Output file path')
        parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')
        parser.add_argument('--api-key', help='OpenWeatherMap API key')
        
        args = parser.parse_args()
        
        # Get weather data
        weather_data = get_weather(
            location=args.location,
            country=args.country,
            units=args.units,
            api_key=args.api_key
        )
        
        # Format output
        json_output = json.dumps(
            weather_data,
            indent=2 if args.pretty else None,
            ensure_ascii=False
        )
        
        # Output to file or console
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Weather data saved to {args.output}", file=sys.stderr)
        else:
            print(json_output)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
