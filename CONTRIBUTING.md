# Contributing to Weather App

Thank you for considering contributing to the Weather App! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before making any contributions.

## How to Contribute

### Reporting Bugs

1. **Check Existing Issues**: Before creating a new issue, please check if a similar issue already exists.
2. **Create a Detailed Bug Report**:
   - Use a clear and descriptive title
   - Describe the steps to reproduce the bug
   - Include the expected behavior and actual behavior
   - Add any relevant error messages or screenshots
   - Specify your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. **Check Existing Feature Requests**: Before suggesting a new feature, check if it has already been requested.
2. **Create a Feature Request**:
   - Use a clear and descriptive title
   - Describe the feature and why it would be useful
   - Include any relevant examples or mockups

### Making Code Contributions

1. **Fork the Repository**:
   ```bash
   git clone https://github.com/dani931004/weather-app.git
   cd weather-app
   ```

2. **Set Up Development Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**:
   - Follow the existing code style
   - Write tests for new features
   - Update documentation as needed

5. **Run Tests and Linters**:
   ```bash
   pytest
   black .
   isort .
   mypy src/
   ```

6. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Add your commit message here"
   ```

7. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**:
   - Go to the original repository
   - Click on "New Pull Request"
   - Select your branch
   - Fill in the pull request template
   - Submit the pull request

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dani931004/weather-app.git
   cd weather-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode with all dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=weather_app --cov-report=term-missing
```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **mypy** for static type checking
- **flake8** for linting

Run all code style checks:
```bash
black .
isort .
mypy src/
flake8
```

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
