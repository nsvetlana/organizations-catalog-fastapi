from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str  # Expects a PostgreSQL URL from the .env file.
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    # Use EdDSA for Ed25519:
    JWT_ALGORITHM: str = "EdDSA"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY: str       # The static API key used for token exchange

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
