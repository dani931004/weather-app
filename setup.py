from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="weather-app",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'weather=weather_app.cli:cli',
        ],
    },
    python_requires='>=3.8',
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional weather application that fetches and displays weather data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/weather-app",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
