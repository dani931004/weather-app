import os
import re
from pathlib import Path

# Configuration
REPO_OWNER = "dani931004"
REPO_NAME = "weather-app"
AUTHOR_NAME = "dani931004"
AUTHOR_EMAIL = "pythonmaildev@gmail.com"

# Files to update (relative to project root)
FILES_TO_UPDATE = [
    "README.md",
    "CONTRIBUTING.md",
    "pyproject.toml",
    "setup.py",
]

def update_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace repository URLs
        content = re.sub(
            r'github\.com/\w+/weather-app',
            f'github.com/{REPO_OWNER}/{REPO_NAME}',
            content
        )
        
        # Replace author information
        content = content.replace("Your Name", AUTHOR_NAME)
        content = content.replace("your.email@example.com", AUTHOR_EMAIL)
        content = content.replace("yourusername", REPO_OWNER)
        
        # Write changes back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✓ Updated {file_path}")
        
    except Exception as e:
        print(f"✗ Error updating {file_path}: {str(e)}")

def main():
    project_root = Path(__file__).parent
    
    for file_name in FILES_TO_UPDATE:
        file_path = project_root / file_name
        if file_path.exists():
            update_file(file_path)
        else:
            print(f"⚠️  File not found: {file_path}")

if __name__ == "__main__":
    main()
