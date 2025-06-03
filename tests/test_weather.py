"""Tests for the weather app."""
import os
import pytest
from unittest.mock import patch, MagicMock

from weather_app.weather import WeatherClient, WeatherResponse
from weather_app.exceptions import LocationNotFoundError, APIError


def test_weather_client_initialization():
    """Test that WeatherClient initializes correctly."""
    client = WeatherClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert "openweathermap.org" in client.base_url


@patch('weather_app.weather.requests.Session.get')
def test_get_weather_by_city_success(mock_get):
    """Test successful weather data retrieval."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'coord': {'lon': -0.1257, 'lat': 51.5085},
        'weather': [{
            'id': 800,
            'main': 'Clear',
            'description': 'clear sky',
            'icon': '01d'
        }],
        'base': 'stations',
        'main': {
            'temp': 15.5,
            'feels_like': 14.8,
            'temp_min': 14.0,
            'temp_max': 16.0,
            'pressure': 1012,
            'humidity': 72
        },
        'visibility': 10000,
        'wind': {
            'speed': 3.6,
            'deg': 200
        },
        'clouds': {'all': 0},
        'dt': 1620000000,
        'sys': {
            'type': 2,
            'id': 2019646,
            'country': 'GB',
            'sunrise': 1619950000,
            'sunset': 1620000000
        },
        'timezone': 3600,
        'id': 2643743,
        'name': 'London',
        'cod': 200
    }
    mock_get.return_value = mock_response

    client = WeatherClient(api_key="test_key")
    weather = client.get_weather_by_city("London")

    assert weather.name == "London"
    assert weather.sys.country == "GB"
    assert weather.weather[0].main == "Clear"
    assert weather.main.temp == 15.5


@patch('weather_app.weather.requests.Session.get')
def test_get_weather_by_city_not_found(mock_get):
    """Test handling of location not found error."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        'cod': '404',
        'message': 'city not found'
    }
    mock_get.return_value = mock_response

    client = WeatherClient(api_key="test_key")
    
    with pytest.raises(LocationNotFoundError):
        client.get_weather_by_city("Nonexistent City")


@patch('weather_app.weather.requests.Session.get')
def test_get_weather_by_city_api_error(mock_get):
    """Test handling of API errors."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        'cod': 401,
        'message': 'Invalid API key'
    }
    mock_get.return_value = mock_response

    client = WeatherClient(api_key="invalid_key")
    
    with pytest.raises(APIError):
        client.get_weather_by_city("London")
