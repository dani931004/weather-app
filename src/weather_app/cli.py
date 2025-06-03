"""
Weather App - Command Line Interface

A simple CLI to fetch weather data from OpenWeatherMap API.
"""
from datetime import datetime
import json
import sys
from typing import Any, Dict, Optional

import click
from dotenv import load_dotenv

from . import __version__, exceptions
from .weather import WeatherClient, WeatherResponse

# Load environment variables
load_dotenv()

def format_weather_data(weather_data: WeatherResponse, units: str) -> Dict[str, Any]:
    """Format weather data into a structured dictionary."""
    temp_unit = '°C' if units == 'metric' else '°F'
    speed_unit = 'm/s' if units == 'metric' else 'mph'
    
    return {
        'location': {
            'city': weather_data.name,
            'country': weather_data.sys.country,
            'coordinates': {
                'lat': weather_data.coord['lat'],
                'lon': weather_data.coord['lon']
            }
        },
        'weather': {
            'main': weather_data.weather[0].main,
            'description': weather_data.weather[0].description,
            'icon': weather_data.weather[0].icon,
            'temperature': {
                'current': weather_data.main.temp,
                'feels_like': weather_data.main.feels_like,
                'min': weather_data.main.temp_min,
                'max': weather_data.main.temp_max,
                'unit': temp_unit
            },
            'pressure': f"{weather_data.main.pressure} hPa",
            'humidity': f"{weather_data.main.humidity}%",
            'visibility': f"{weather_data.visibility / 1000:.1f} km" if weather_data.visibility else 'N/A',
            'wind': {
                'speed': f"{weather_data.wind.speed} {speed_unit}",
                'degree': weather_data.wind.deg if hasattr(weather_data.wind, 'deg') else None,
                'gust': weather_data.wind.gust if hasattr(weather_data.wind, 'gust') else None
            },
            'clouds': f"{weather_data.clouds.all}%" if hasattr(weather_data, 'clouds') else 'N/A',
            'rain': weather_data.rain if hasattr(weather_data, 'rain') else None,
            'snow': weather_data.snow if hasattr(weather_data, 'snow') else None,
            'sun': {
                'sunrise': datetime.fromtimestamp(weather_data.sys.sunrise).isoformat(),
                'sunset': datetime.fromtimestamp(weather_data.sys.sunset).isoformat()
            },
            'timezone': weather_data.timezone if hasattr(weather_data, 'timezone') else None,
            'timestamp': datetime.now().isoformat()
        }
    }

@click.group()
@click.version_option(version=__version__)
def cli():
    """Weather App - Fetch current weather data for any location."""
    pass

@cli.command()
@click.argument('location')
@click.option('--country', '-c', help='Country code (e.g., us, gb, jp)')
@click.option('--units', '-u', type=click.Choice(['metric', 'imperial']), 
              default='metric', help='Units of measurement (metric/imperial)')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--pretty/--no-pretty', default=True, help='Pretty-print JSON output')
@click.option('--api-key', envvar='OPENWEATHER_API_KEY', 
              help='OpenWeatherMap API key (can also be set via OPENWEATHER_API_KEY env var)')
def get(location: str, country: Optional[str], units: str, 
       output: Optional[str], pretty: bool, api_key: Optional[str]):
    """Get current weather for a location.
    
    LOCATION can be a city name (e.g., 'London'), or a city name with country code 
    (e.g., 'London,uk').
    """
    try:
        if not api_key:
            raise exceptions.InvalidAPIKeyError("API key is required")
            
        client = WeatherClient(api_key=api_key)
        
        # If location contains a comma, split into city and country
        if ',' in location:
            location_parts = [p.strip() for p in location.split(',')]
            city = location_parts[0]
            country = location_parts[1] if len(location_parts) > 1 else country
        else:
            city = location
        
        weather_data = client.get_weather_by_city(
            city=city,
            country_code=country,
            units=units
        )
        
        # Format the output
        formatted_data = format_weather_data(weather_data, units)
        json_output = json.dumps(
            formatted_data, 
            indent=2 if pretty else None,
            ensure_ascii=False
        )
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            click.echo(f"Weather data saved to {output}", err=True)
        else:
            click.echo(json_output)
                
    except exceptions.WeatherAppError as e:
        error_msg = str(e)
        if isinstance(e, exceptions.InvalidAPIKeyError):
            error_msg = (
                "Invalid or missing API key. Please set the OPENWEATHER_API_KEY "
                "environment variable or use the --api-key option."
            )
        click.secho(f"Error: {error_msg}", fg='red', err=True)
        sys.exit(1)
    except Exception as e:
        click.secho(f"Unexpected error: {str(e)}", fg='red', err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
