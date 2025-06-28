from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from pathlib import Path
from dotenv import load_dotenv
import os

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from .env file
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Clean Architecture"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "url")

    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "url")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # First Superuser
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL", "email")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "password")

    class Config:
        case_sensitive = True
        env_file = str(PROJECT_ROOT / '.env')
        env_file_encoding = 'utf-8'

# Create settings instance
settings = Settings() 