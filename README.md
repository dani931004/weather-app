# Weather App

A simple command-line tool that fetches current weather data for any location and outputs it in JSON format.

## Features

- Get current weather data for any location
- Output data in clean, structured JSON format
- Supports both metric and imperial units
- Save output to a file or print to console
- Lightweight and easy to use

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Create a `.env` file in the project root and add:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENWEATHER_API_KEY=your_api_key_here
     ```

## Usage

```bash
# Get weather for a city
python weather.py "London"

# Get weather with specific units (metric/imperial)
python weather.py "New York" --units imperial

# Specify country code
python weather.py "Paris,fr"

# Pretty-print JSON output
python weather.py "Tokyo" --pretty

# Save output to a JSON file
python weather.py "Berlin" --output weather.json

# Use a specific API key
python weather.py "Madrid" --api-key your_api_key_here
```

## Output Example

```json
{
  "location": {
    "city": "London",
    "country": "GB",
    "coordinates": {
      "lat": 51.5073,
      "lon": -0.1276478
    }
  },
  "weather": {
    "main": "Clouds",
    "description": "overcast clouds",
    "icon": "04d",
    "temperature": {
      "current": 18.5,
      "feels_like": 18.2,
      "min": 17.5,
      "max": 19.5,
      "unit": "°C"
    },
    "pressure": "1012 hPa",
    "humidity": "72%",
    "visibility": "10.0 km",
    "wind": {
      "speed": "3.6 m/s",
      "degree": 200,
      "gust": 7.2
    },
    "clouds": "90%",
    "rain": null,
    "snow": null,
    "sun": {
      "sunrise": 1689999999,
      "sunset": 1690054321
    },
    "timezone": 3600,
    "timestamp": 1690041600
  }
}
```

## Project Structure

```
weather_app/
├── src/
│   └── weather_app/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── weather.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_weather.py
├── docs/
│   └── api.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
