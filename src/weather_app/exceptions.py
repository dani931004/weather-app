"""Custom exceptions for the Weather App."""

class WeatherAppError(Exception):
    """Base exception for all Weather App related errors."""
    pass

class APIError(WeatherAppError):
    """Raised when there's an error with the weather API."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class InvalidAPIKeyError(APIError):
    """Raised when the provided API key is invalid."""
    def __init__(self, message: str):
        super().__init__(status_code=401, message=message)

class LocationNotFoundError(WeatherAppError):
    """Raised when the requested location is not found."""
    pass

class RateLimitExceededError(APIError):
    """Raised when the API rate limit is exceeded."""
    pass

class ConfigurationError(WeatherAppError):
    """Raised when there's an error in the application configuration."""
    pass
