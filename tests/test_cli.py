"""Tests for the CLI module."""
import json
import os
from unittest.mock import MagicMock, patch, mock_open
import pytest
from click.testing import CliRunner

from weather_app.cli import cli, format_weather_data
from weather_app.weather import (
    CloudData as Clouds,
    MainWeatherData as Main,
    SystemData as Sys,
    WeatherResponse,
    WindData as Wind,
    WeatherCondition
)


@pytest.fixture
def mock_client_class():
    with patch('weather_app.cli.WeatherClient') as mock_class:
        yield mock_class


def test_cli_help():
    """Test the CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output


def test_format_weather_data():
    """Test the format_weather_data function."""
    # Create a mock WeatherResponse object with all required fields
    coord = {'lon': -0.1257, 'lat': 51.5085}
    weather = [WeatherCondition(
        id=800,
        main='Clear',
        description='clear sky',
        icon='01d'
    )]
    base = 'stations'  # Required field
    visibility = 10000  # Required field
    dt = 1620000000  # Required field
    timezone = 0  # Required field
    id = 2643743  # Required field
    name = 'London'  # Required field
    cod = 200  # Required field
    main = Main(
        temp=15.5,
        feels_like=14.8,
        temp_min=14.0,
        temp_max=16.0,
        pressure=1012,
        humidity=72
    )
    wind = Wind(speed=3.6, deg=200, gust=None)
    clouds = Clouds(all=0)
    sys = Sys(
        type=2,
        id=2019646,
        country='GB',
        sunrise=1619950000,
        sunset=1620000000
    )
    
    # Create a dictionary with all required fields
    weather_data = {
        'coord': coord,
        'weather': weather,
        'base': base,
        'main': main.model_dump(),
        'visibility': visibility,
        'wind': wind.model_dump(),
        'clouds': clouds.model_dump(),
        'dt': dt,
        'sys': sys.model_dump(),
        'timezone': timezone,
        'id': id,
        'name': name,
        'cod': cod
    }
    weather_response = WeatherResponse(**weather_data)
    
    # Test with metric units
    result = format_weather_data(weather_response, 'metric')
    assert result['location']['city'] == 'London'
    assert result['location']['country'] == 'GB'
    assert result['weather']['temperature']['unit'] == '°C'
    assert result['weather']['wind']['speed'] == '3.6 m/s'
    
    # Test with imperial units
    result = format_weather_data(weather_response, 'imperial')
    assert result['weather']['temperature']['unit'] == '°F'
    assert result['weather']['wind']['speed'] == '3.6 mph'

@patch('weather_app.cli.WeatherClient')
def test_cli_get_weather_success(mock_client_class):
    """Test successful weather data retrieval via CLI."""
    # Setup mock
    mock_client = MagicMock()
    # Create a dictionary with all required fields
    weather_data = {
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
        'wind': {'speed': 3.6, 'deg': 200, 'gust': None},
        'clouds': {'all': 0},
        'dt': 1620000000,
        'sys': {
            'type': 2,
            'id': 2019646,
            'country': 'GB',
            'sunrise': 1619950000,
            'sunset': 1620000000
        },
        'timezone': 0,
        'id': 2643743,
        'name': 'London',
        'cod': 200
    }
    mock_client.get_weather_by_city.return_value = WeatherResponse(**weather_data)
    mock_client_class.return_value = mock_client

    # Run CLI command with API key
    runner = CliRunner()
    result = runner.invoke(cli, ['get', 'London'], env={'OPENWEATHER_API_KEY': 'test_key'})
    
    # Verify
    assert result.exit_code == 0
    assert mock_client_class.called
    assert mock_client.get_weather_by_city.called
    mock_client.get_weather_by_city.assert_called_once_with(
        city='London', country_code=None, units='metric'
    )
    data = json.loads(result.output)
    assert data['location']['city'] == 'London'
    assert data['location']['country'] == 'GB'
    assert 'weather' in data


@patch('weather_app.cli.WeatherClient')
def test_cli_get_weather_with_options(mock_client_class):
    """Test CLI with various options."""
    # Setup mock
    mock_client = MagicMock()
    # Create a dictionary with all required fields
    weather_data = {
        'coord': {'lon': -74.006, 'lat': 40.7143},
        'weather': [{
            'id': 800,
            'main': 'Clear',
            'description': 'clear sky',
            'icon': '01d'
        }],
        'base': 'stations',
        'main': {
            'temp': 60.0,
            'feels_like': 59.0,
            'temp_min': 58.0,
            'temp_max': 62.0,
            'pressure': 1012,
            'humidity': 72
        },
        'visibility': 10000,
        'wind': {'speed': 3.6, 'deg': 200, 'gust': None},
        'clouds': {'all': 0},
        'dt': 1620000000,
        'sys': {
            'type': 2,
            'id': 2019646,
            'country': 'US',
            'sunrise': 1619950000,
            'sunset': 1620000000
        },
        'timezone': 0,
        'id': 5128581,
        'name': 'New York',
        'cod': 200
    }
    mock_client.get_weather_by_city.return_value = WeatherResponse(**weather_data)
    mock_client_class.return_value = mock_client

    # Run CLI command with options and API key
    runner = CliRunner()
    result = runner.invoke(cli, [
        'get', 
        'New York',
        '--country', 'us',
        '--units', 'imperial',
        '--pretty'
    ], env={'OPENWEATHER_API_KEY': 'test_key'})
    
    # Verify
    assert result.exit_code == 0
    assert mock_client_class.called
    assert mock_client.get_weather_by_city.called
    mock_client.get_weather_by_city.assert_called_once_with(
        city='New York', country_code='us', units='imperial'
    )
    data = json.loads(result.output)
    assert data['location']['city'] == 'New York'
    assert data['location']['country'] == 'US'
    assert data['weather']['temperature']['unit'] == '°F'


@patch('weather_app.cli.WeatherClient')
def test_cli_get_weather_save_to_file(mock_client_class, tmp_path):
    """Test saving weather data to a file."""
    # Setup mock
    mock_client = MagicMock()
    # Create a dictionary with all required fields
    weather_data = {
        'coord': {'lon': 139.6917, 'lat': 35.6895},
        'weather': [{
            'id': 803,
            'main': 'Clouds',
            'description': 'broken clouds',
            'icon': '04d'
        }],
        'base': 'stations',
        'main': {
            'temp': 22.5,
            'feels_like': 21.8,
            'temp_min': 20.0,
            'temp_max': 25.0,
            'pressure': 1013,
            'humidity': 65
        },
        'visibility': 10000,
        'wind': {'speed': 2.6, 'deg': 180, 'gust': None},
        'clouds': {'all': 20},
        'dt': 1620000000,
        'sys': {
            'type': 2,
            'id': 2019646,
            'country': 'JP',
            'sunrise': 1619940000,
            'sunset': 1619990000
        },
        'timezone': 32400,
        'id': 1850144,
        'name': 'Tokyo',
        'cod': 200
    }
    mock_client.get_weather_by_city.return_value = WeatherResponse(**weather_data)
    mock_client_class.return_value = mock_client

    # Create a temporary file
    output_file = tmp_path / "weather.json"
    
    # Run CLI command with output file
    runner = CliRunner()
    result = runner.invoke(cli, [
        'get', 
        'Tokyo',
        '--output', str(output_file)
    ], env={'OPENWEATHER_API_KEY': 'test_key'})
    
    # Verify
    assert result.exit_code == 0
    assert mock_client_class.called
    assert mock_client.get_weather_by_city.called
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        data = json.load(f)
        assert data['location']['city'] == 'Tokyo'


@patch.dict(os.environ, {}, clear=True)
def test_cli_missing_api_key():
    """Test CLI with missing API key."""
    runner = CliRunner()
    result = runner.invoke(cli, ['get', 'London'])
    
    assert result.exit_code == 1
    assert "Invalid or missing API key" in result.output


@patch('builtins.open', side_effect=PermissionError("Permission denied"))
def test_cli_invalid_output_format(mock_file, mock_client_class):
    """Test CLI with invalid output format."""
    # Setup mock
    mock_client = MagicMock()
    weather_data = {
        'coord': {'lon': -0.1257, 'lat': 51.5085},
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}],
        'base': 'stations',
        'main': {'temp': 15.5, 'feels_like': 14.8, 'temp_min': 14.0, 'temp_max': 16.0, 'pressure': 1012, 'humidity': 72},
        'visibility': 10000,
        'wind': {'speed': 3.6, 'deg': 200, 'gust': None},
        'clouds': {'all': 0},
        'dt': 1620000000,
        'sys': {'type': 2, 'id': 2019646, 'country': 'GB', 'sunrise': 1619950000, 'sunset': 1620000000},
        'timezone': 0,
        'id': 2643743,
        'name': 'London',
        'cod': 200
    }
    mock_client.get_weather_by_city.return_value = WeatherResponse(**weather_data)
    mock_client_class.return_value = mock_client

    # Run CLI command with invalid output format
    runner = CliRunner()
    result = runner.invoke(cli, [
        'get',
        'London',
        '--output', '/invalid/path/weather.json'
    ], env={'OPENWEATHER_API_KEY': 'test_key'})
    
    # Verify
    assert result.exit_code == 1
    assert "Unexpected error: Permission denied" in result.output


@patch('builtins.open', side_effect=OSError("File system error"))
def test_cli_file_write_error(mock_file, mock_client_class, tmp_path):
    """Test error when writing to file fails."""
    # Setup mock
    mock_client = MagicMock()
    weather_data = {
        'coord': {'lon': -0.1257, 'lat': 51.5085},
        'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}],
        'base': 'stations',
        'main': {'temp': 15.5, 'feels_like': 14.8, 'temp_min': 14.0, 'temp_max': 16.0, 'pressure': 1012, 'humidity': 72},
        'visibility': 10000,
        'wind': {'speed': 3.6, 'deg': 200, 'gust': None},
        'clouds': {'all': 0},
        'dt': 1620000000,
        'sys': {'type': 2, 'id': 2019646, 'country': 'GB', 'sunrise': 1619950000, 'sunset': 1620000000},
        'timezone': 0,
        'id': 2643743,
        'name': 'London',
        'cod': 200
    }
    mock_client.get_weather_by_city.return_value = WeatherResponse(**weather_data)
    mock_client_class.return_value = mock_client

    # Create a test file path
    test_file = tmp_path / "test_output.json"
    
    # Run CLI command with file write error
    runner = CliRunner()
    result = runner.invoke(cli, [
        'get', 
        'London',
        '--output', str(test_file)
    ], env={'OPENWEATHER_API_KEY': 'test_key'})
    
    # Verify
    assert result.exit_code == 1
    assert "Unexpected error: File system error" in result.output
