#!/usr/bin/env python
import os
import shutil
import json


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def create_file(path, content=""):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created file: {path}")


def init_project():
    """Initialize the project structure."""
    print("Initializing intelligent agent project...")

    # Create base directories
    directories = [
        "model",
        "utils",
        "frontend/static/css",
        "frontend/static/js",
        "data/raw",
        "data/processed"
    ]

    for directory in directories:
        create_directory(directory)

    # Create __init__.py files for Python modules
    module_dirs = ["model", "utils"]
    for module_dir in module_dirs:
        create_file(os.path.join(module_dir, "__init__.py"))

    # Create sample training data
    sample_qa = [
        {
            "question": "What is this intelligent agent?",
            "answer": "This is an AI assistant based on Python with OpenAI-style interfaces and MCP for coherent conversations."
        },
        {
            "question": "How do you process messages?",
            "answer": "I use a Message Coherence Protocol (MCP) to understand intent, determine if web search is needed, and maintain conversation flow."
        },
        {
            "question": "Can you search the web?",
            "answer": "Yes, I can integrate with web search services to provide up-to-date information when needed."
        }
    ]

    create_file("data/raw/sample_qa.json", json.dumps(sample_qa, indent=2))

    print("\nProject structure initialized!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python app.py")
    print("3. Access the web interface: http://localhost:8000")


if __name__ == "__main__":
    init_project()