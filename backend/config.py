"""
Configuration management for LiveKit Voice Agent
Handles environment variables, validation, and settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings with validation"""

    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=5001, ge=1, le=65535, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ALLOWED_ORIGINS: str = Field(default="*", description="CORS allowed origins (comma-separated)")

    # LiveKit Configuration
    LIVEKIT_API_KEY: str = Field(..., description="LiveKit API key")
    LIVEKIT_API_SECRET: str = Field(..., description="LiveKit API secret")
    LIVEKIT_URL: str = Field(default="ws://localhost:7880", description="LiveKit server URL")

    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4-realtime-preview", description="OpenAI model")
    OPENAI_TEMPERATURE: float = Field(default=0.8, ge=0.0, le=2.0, description="Model temperature")

    # Database Configuration
    DATABASE_URL: str = Field(default="tutor_db.sqlite", description="Database connection URL")

    # Redis Configuration (optional)
    REDIS_URL: Optional[str] = Field(default=None, description="Redis connection URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")

    # Security
    SECRET_KEY: str = Field(default="change-this-in-production", description="Secret key for sessions")
    JWT_EXPIRATION_HOURS: int = Field(default=2, ge=1, le=24, description="JWT token expiration")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=10, ge=1, le=1000, description="Rate limit per minute")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format: json or text")

    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: Optional[int] = Field(default=None, description="Separate port for metrics")

    # Features
    ENABLE_WEBSOCKET: bool = Field(default=True, description="Enable WebSocket support")
    ENABLE_FILE_UPLOAD: bool = Field(default=True, description="Enable file upload")
    MAX_FILE_SIZE_MB: int = Field(default=10, ge=1, le=100, description="Max file upload size in MB")

    @validator("ALLOWED_ORIGINS")
    def parse_origins(cls, v):
        """Parse comma-separated origins"""
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v

    @validator("LOG_FORMAT")
    def validate_log_format(cls, v):
        """Validate log format"""
        valid_formats = ["json", "text"]
        v = v.lower()
        if v not in valid_formats:
            raise ValueError(f"LOG_FORMAT must be one of {valid_formats}")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings():
    """Reload settings from environment"""
    global _settings
    _settings = Settings()
    return _settings


# Convenience accessors
def get_database_url() -> str:
    """Get database connection URL"""
    return get_settings().DATABASE_URL


def get_livekit_config() -> dict:
    """Get LiveKit configuration"""
    settings = get_settings()
    return {
        "api_key": settings.LIVEKIT_API_KEY,
        "api_secret": settings.LIVEKIT_API_SECRET,
        "url": settings.LIVEKIT_URL
    }


def get_openai_config() -> dict:
    """Get OpenAI configuration"""
    settings = get_settings()
    return {
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.OPENAI_MODEL,
        "temperature": settings.OPENAI_TEMPERATURE
    }


def is_production() -> bool:
    """Check if running in production mode"""
    return not get_settings().DEBUG


def validate_config():
    """Validate all configuration settings"""
    try:
        settings = get_settings()

        # Check required fields
        required_fields = [
            "LIVEKIT_API_KEY",
            "LIVEKIT_API_SECRET",
            "OPENAI_API_KEY"
        ]

        missing = []
        for field in required_fields:
            value = getattr(settings, field, None)
            if not value or value == "":
                missing.append(field)

        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

        # Warn about insecure defaults
        if settings.SECRET_KEY == "change-this-in-production" and is_production():
            raise ValueError("SECRET_KEY must be changed in production!")

        return True

    except Exception as e:
        raise ValueError(f"Configuration validation failed: {str(e)}")


# Export settings instance
settings = get_settings()
