import os
from dotenv import load_dotenv

load_dotenv()

def load_env_variable(key: str):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Missing environment variable: {key}")
    return value
