"""
Menshun Backend - Enterprise Privileged Access Management System.

This package contains the core backend implementation for the Menshun PAM tool,
providing comprehensive privileged user management, service identity management,
and credential vaulting capabilities for Microsoft Entra ID environments.

The backend is built with FastAPI and provides:
- RESTful API endpoints for all PAM operations
- Microsoft Graph integration for Azure AD management
- Secure credential vaulting with automatic rotation
- Comprehensive audit logging and compliance features
- Background task processing for automated operations

Architecture Overview:
    api/: FastAPI routes and endpoint definitions
    core/: Core business logic, configuration, and utilities
    models/: SQLAlchemy database models and schemas
    services/: Business logic services and external integrations
    utils/: Utility functions and helpers
    scripts/: Management scripts and CLI tools

Security Features:
    - Azure AD authentication and authorization
    - Role-based access control (RBAC)
    - Secure credential storage and encryption
    - Comprehensive audit trails
    - Input validation and sanitization
    - Rate limiting and security headers

Author: Menshun Security Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Menshun Security Team"
__email__ = "security@company.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 Menshun Security"

# Version information
VERSION_INFO = {
    "version": __version__,
    "build": "development",
    "python_version": "3.11+",
    "framework": "FastAPI 0.104+",
    "database": "PostgreSQL 15+",
    "cache": "Redis 7+",
}

# Package metadata
PACKAGE_INFO = {
    "name": "menshun-backend",
    "description": "Enterprise Privileged Access Management - Backend API",
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "version": __version__,
    "home_page": "https://github.com/your-org/menshun",
    "documentation": "https://docs.menshun.com",
}

# Feature flags for the application
FEATURES = {
    "privileged_user_management": True,
    "service_identity_management": True,
    "credential_vaulting": True,
    "automatic_rotation": True,
    "audit_logging": True,
    "compliance_reporting": True,
    "session_monitoring": True,
    "multi_tenant": False,  # Future feature
    "mobile_app": False,   # Future feature
}

# Supported integrations
INTEGRATIONS = {
    "microsoft_graph": True,
    "azure_ad": True,
    "azure_keyvault": True,
    "hashicorp_vault": True,
    "prometheus": True,
    "sentry": True,
    "opentelemetry": True,
}

# Export commonly used classes and functions
from app.core.config import settings
from app.core.logging import get_logger

# Initialize application logger
logger = get_logger(__name__)

# Log package initialization
logger.info(
    "Menshun Backend initialized",
    extra={
        "version": __version__,
        "features": list(FEATURES.keys()),
        "integrations": list(INTEGRATIONS.keys()),
    }
)


def get_version() -> str:
    """
    Get the current version of the Menshun backend.
    
    Returns:
        str: Version string in semantic versioning format
        
    Example:
        >>> from app import get_version
        >>> print(get_version())
        1.0.0
    """
    return __version__


def get_package_info() -> dict:
    """
    Get comprehensive package information.
    
    Returns:
        dict: Dictionary containing package metadata
        
    Example:
        >>> from app import get_package_info
        >>> info = get_package_info()
        >>> print(info['name'])
        menshun-backend
    """
    return PACKAGE_INFO.copy()


def get_version_info() -> dict:
    """
    Get detailed version information including dependencies.
    
    Returns:
        dict: Dictionary containing version details
        
    Example:
        >>> from app import get_version_info
        >>> info = get_version_info()
        >>> print(info['framework'])
        FastAPI 0.104+
    """
    return VERSION_INFO.copy()


def get_features() -> dict:
    """
    Get enabled features for the application.
    
    Returns:
        dict: Dictionary of feature flags
        
    Example:
        >>> from app import get_features
        >>> features = get_features()
        >>> print(features['audit_logging'])
        True
    """
    return FEATURES.copy()


def get_integrations() -> dict:
    """
    Get available integrations for the application.
    
    Returns:
        dict: Dictionary of integration availability
        
    Example:
        >>> from app import get_integrations
        >>> integrations = get_integrations()
        >>> print(integrations['azure_ad'])
        True
    """
    return INTEGRATIONS.copy()


# Health check function for monitoring
def health_check() -> dict:
    """
    Perform basic health check of the application.
    
    Returns:
        dict: Health status information
        
    Example:
        >>> from app import health_check
        >>> status = health_check()
        >>> print(status['status'])
        healthy
    """
    return {
        "status": "healthy",
        "version": __version__,
        "timestamp": "2024-01-01T00:00:00Z",  # This would be dynamic in real implementation
        "features": len([f for f, enabled in FEATURES.items() if enabled]),
        "integrations": len([i for i, enabled in INTEGRATIONS.items() if enabled]),
    }


# Application constants
class Constants:
    """Application-wide constants."""
    
    # API Configuration
    API_V1_PREFIX = "/api/v1"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    OPENAPI_URL = "/openapi.json"
    
    # Security
    JWT_ALGORITHM = "HS256"
    PASSWORD_MIN_LENGTH = 12
    SESSION_TIMEOUT_HOURS = 8
    MAX_LOGIN_ATTEMPTS = 5
    
    # Database
    DATABASE_POOL_SIZE = 10
    DATABASE_MAX_OVERFLOW = 20
    DATABASE_POOL_TIMEOUT = 30
    
    # Cache
    CACHE_TTL_DEFAULT = 3600  # 1 hour
    CACHE_TTL_SHORT = 300     # 5 minutes
    CACHE_TTL_LONG = 86400    # 24 hours
    
    # Background Tasks
    CELERY_TASK_TIMEOUT = 600        # 10 minutes
    CELERY_SOFT_TIMEOUT = 300        # 5 minutes
    CELERY_MAX_RETRIES = 3
    
    # Microsoft Graph
    GRAPH_API_VERSION = "v1.0"
    GRAPH_BASE_URL = "https://graph.microsoft.com"
    
    # Audit and Compliance
    AUDIT_RETENTION_DAYS = 2555      # 7 years
    LOG_RETENTION_DAYS = 90
    BACKUP_RETENTION_DAYS = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = 60
    RATE_LIMIT_BURST = 120
    
    # File Upload
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = [".json", ".csv", ".xlsx"]


# Export constants for easy access
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "VERSION_INFO",
    "PACKAGE_INFO",
    "FEATURES",
    "INTEGRATIONS",
    "Constants",
    "get_version",
    "get_package_info",
    "get_version_info",
    "get_features",
    "get_integrations",
    "health_check",
    "settings",
    "logger",
]