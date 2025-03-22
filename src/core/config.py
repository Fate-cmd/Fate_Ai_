from pydantic import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "Fate AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fate_db")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))

    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Blockchain Settings
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    SOLANA_NETWORK: str = os.getenv("SOLANA_NETWORK", "mainnet-beta")

    # AI Model Settings
    AI_MODEL_PATH: str = os.getenv("AI_MODEL_PATH", "models/fate_model")
    AI_MODEL_VERSION: str = os.getenv("AI_MODEL_VERSION", "1.0.0")

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ETHERSCAN_API_KEY: str = os.getenv("ETHERSCAN_API_KEY", "")

    # Security Settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://fate-ai.com").split(",")
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "fate.log")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    class Config:
        case_sensitive = True

settings = Settings() 