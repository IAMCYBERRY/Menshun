"""
Menshun Backend - Configuration Management.

This module handles all application configuration including environment variables,
settings validation, and configuration for different deployment environments.
"""

import os
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    This class defines all configuration options for the Menshun backend,
    with automatic loading from environment variables and .env files.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # =============================================================================
    # Application Configuration
    # =============================================================================
    
    ENVIRONMENT: str = Field(default="development", description="Application environment")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    APP_VERSION: str = Field(default="1.0.0-dev", description="Application version")
    
    # =============================================================================
    # API Configuration
    # =============================================================================
    
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="CORS allowed origins"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        description="Allowed hosts"
    )
    
    # =============================================================================
    # Database Configuration
    # =============================================================================
    
    DATABASE_URL: str = Field(
        default="postgresql://pamuser:password@localhost:5432/pamdb",
        description="Database connection URL"
    )
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    DB_POOL_SIZE: int = Field(default=10, description="Database pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    
    # =============================================================================
    # Redis Configuration
    # =============================================================================
    
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    
    # =============================================================================
    # Security Configuration
    # =============================================================================
    
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Application secret key"
    )
    JWT_SECRET_KEY: str = Field(
        default="dev-jwt-secret-change-in-production",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRATION_HOURS: int = Field(default=8, description="JWT expiration hours")
    
    # Password and session configuration
    BCRYPT_ROUNDS: int = Field(default=12, description="Bcrypt rounds")
    SESSION_TIMEOUT_HOURS: int = Field(default=8, description="Session timeout hours")
    MAX_LOGIN_ATTEMPTS: int = Field(default=5, description="Max login attempts")
    
    # =============================================================================
    # Azure AD Configuration
    # =============================================================================
    
    AZURE_CLIENT_ID: Optional[str] = Field(default=None, description="Azure AD client ID")
    AZURE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Azure AD client secret")
    AZURE_TENANT_ID: Optional[str] = Field(default=None, description="Azure AD tenant ID")
    AZURE_AUTHORITY: Optional[str] = Field(default=None, description="Azure AD authority")
    AZURE_SCOPE: str = Field(
        default="https://graph.microsoft.com/.default",
        description="Azure AD scope"
    )
    
    # =============================================================================
    # Vault Configuration
    # =============================================================================
    
    VAULT_TYPE: str = Field(default="file_vault", description="Vault backend type")
    VAULT_ENCRYPTION_KEY: str = Field(
        default="dev-vault-key-change-in-production",
        description="Vault encryption key"
    )
    VAULT_PATH: str = Field(default="/app/vault_data", description="Vault data path")
    
    # Azure Key Vault
    AZURE_KEYVAULT_URL: Optional[str] = Field(default=None, description="Azure Key Vault URL")
    
    # HashiCorp Vault
    VAULT_URL: Optional[str] = Field(default=None, description="HashiCorp Vault URL")
    VAULT_TOKEN: Optional[str] = Field(default=None, description="HashiCorp Vault token")
    
    # =============================================================================
    # Feature Flags
    # =============================================================================
    
    ENABLE_SWAGGER_UI: bool = Field(default=True, description="Enable Swagger UI")
    ENABLE_METRICS: bool = Field(default=True, description="Enable metrics")
    ENABLE_AUDIT_LOGGING: bool = Field(default=True, description="Enable audit logging")
    
    # =============================================================================
    # External Integrations
    # =============================================================================
    
    # Sentry error tracking
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN")
    
    # Email configuration
    SMTP_HOST: Optional[str] = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    SMTP_FROM_EMAIL: Optional[str] = Field(default=None, description="SMTP from email")
    
    # =============================================================================
    # Celery Configuration
    # =============================================================================
    
    CELERY_BROKER_URL: Optional[str] = Field(default=None, description="Celery broker URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, description="Celery result backend")
    CELERY_TIMEZONE: str = Field(default="UTC", description="Celery timezone")
    
    # =============================================================================
    # Performance Configuration
    # =============================================================================
    
    CACHE_TTL_SECONDS: int = Field(default=3600, description="Cache TTL seconds")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Rate limit per minute")
    
    # =============================================================================
    # Compliance Configuration
    # =============================================================================
    
    AUDIT_RETENTION_DAYS: int = Field(default=2555, description="Audit retention days")
    LOG_RETENTION_DAYS: int = Field(default=90, description="Log retention days")
    
    # =============================================================================
    # Validators
    # =============================================================================
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production", "testing"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {allowed}")
        return v.upper()
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    # =============================================================================
    # Property Methods
    # =============================================================================
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.ENVIRONMENT == "testing"
    
    @property
    def celery_broker_url(self) -> str:
        """Get Celery broker URL with Redis fallback."""
        return self.CELERY_BROKER_URL or self.REDIS_URL
    
    @property
    def celery_result_backend(self) -> str:
        """Get Celery result backend with Redis fallback."""
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL
    
    def get_database_url(self) -> str:
        """Get database URL with proper async driver."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL
    
    def get_azure_authority_url(self) -> str:
        """Get Azure AD authority URL."""
        if self.AZURE_AUTHORITY:
            return self.AZURE_AUTHORITY
        if self.AZURE_TENANT_ID:
            return f"https://login.microsoftonline.com/{self.AZURE_TENANT_ID}"
        return "https://login.microsoftonline.com/common"
    
    def is_azure_configured(self) -> bool:
        """Check if Azure AD is properly configured."""
        return all([
            self.AZURE_CLIENT_ID,
            self.AZURE_CLIENT_SECRET,
            self.AZURE_TENANT_ID,
        ])
    
    def is_email_configured(self) -> bool:
        """Check if email is properly configured."""
        return all([
            self.SMTP_HOST,
            self.SMTP_USERNAME,
            self.SMTP_PASSWORD,
            self.SMTP_FROM_EMAIL,
        ])
    
    def get_vault_config(self) -> Dict[str, Any]:
        """Get vault configuration based on vault type."""
        base_config = {
            "type": self.VAULT_TYPE,
            "encryption_key": self.VAULT_ENCRYPTION_KEY,
        }
        
        if self.VAULT_TYPE == "file_vault":
            base_config["path"] = self.VAULT_PATH
        elif self.VAULT_TYPE == "azure_keyvault":
            base_config.update({
                "vault_url": self.AZURE_KEYVAULT_URL,
                "client_id": self.AZURE_CLIENT_ID,
                "client_secret": self.AZURE_CLIENT_SECRET,
                "tenant_id": self.AZURE_TENANT_ID,
            })
        elif self.VAULT_TYPE == "hashicorp_vault":
            base_config.update({
                "vault_url": self.VAULT_URL,
                "token": self.VAULT_TOKEN,
            })
        
        return base_config


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: The global settings instance
    """
    return settings


def validate_required_settings() -> None:
    """
    Validate that all required settings are configured.
    
    Raises:
        ValueError: If required settings are missing
    """
    errors = []
    
    # Check Azure AD configuration in production
    if settings.is_production and not settings.is_azure_configured():
        errors.append("Azure AD configuration is required in production")
    
    # Check database configuration
    if not settings.DATABASE_URL or settings.DATABASE_URL == "postgresql://pamuser:password@localhost:5432/pamdb":
        if settings.is_production:
            errors.append("Production database URL must be configured")
    
    # Check security keys in production
    if settings.is_production:
        if settings.SECRET_KEY == "dev-secret-key-change-in-production":
            errors.append("Production SECRET_KEY must be changed from default")
        
        if settings.JWT_SECRET_KEY == "dev-jwt-secret-change-in-production":
            errors.append("Production JWT_SECRET_KEY must be changed from default")
        
        if settings.VAULT_ENCRYPTION_KEY == "dev-vault-key-change-in-production":
            errors.append("Production VAULT_ENCRYPTION_KEY must be changed from default")
    
    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))


# Validate settings on import
if settings.is_production:
    validate_required_settings()


__all__ = ["Settings", "settings", "get_settings", "validate_required_settings"]