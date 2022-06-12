import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '../../.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Application port
PORT = int(os.environ.get("PORT"))

# Development flag
DEBUG: bool = os.environ.get("DEBUG") == "True"

# Database settings
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")