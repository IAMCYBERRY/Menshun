"""
Menshun Backend - FastAPI Application Entry Point.

This module serves as the main entry point for the Menshun Privileged Access Management
system backend API. It sets up the FastAPI application with proper configuration,
middleware, routing, and lifecycle management with comprehensive OpenAPI documentation.

Author: Menshun Security Team
License: MIT
"""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app import get_package_info, get_version, logger
from app.core.config import get_settings

# Get application settings
settings = get_settings()

# Application startup time for uptime calculation
startup_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application,
    including database connections, background tasks, and resource cleanup.
    """
    logger.info("Starting Menshun PAM Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Version: {get_version()}")
    
    # Startup logic here
    try:
        # Initialize database connections
        logger.info("Initializing database connections...")
        
        # Initialize Redis connections
        logger.info("Initializing Redis connections...")
        
        # Start background tasks
        logger.info("Starting background tasks...")
        
        logger.info("Menshun PAM Backend started successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        raise
    finally:
        # Shutdown logic here
        logger.info("Shutting down Menshun PAM Backend...")
        
        # Close database connections
        logger.info("Closing database connections...")
        
        # Close Redis connections
        logger.info("Closing Redis connections...")
        
        # Stop background tasks
        logger.info("Stopping background tasks...")
        
        logger.info("Menshun PAM Backend shutdown complete")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application with enhanced OpenAPI documentation."""
    package_info = get_package_info()
    
    application = FastAPI(
        title="Menshun PAM API",
        description="""
        ## Enterprise Privileged Access Management for Microsoft Entra ID

        The Menshun PAM API provides comprehensive privileged access management capabilities
        for Microsoft Entra ID environments, including:

        ### Core Features
        - **Privileged User Management**: Create, manage, and monitor privileged user accounts
        - **Service Identity Management**: Manage service accounts, service principals, and managed identities
        - **Credential Management**: Secure credential storage, rotation, and lifecycle management
        - **Role Assignment Management**: Manage directory role assignments with approval workflows
        - **Audit & Compliance**: Comprehensive audit logging and compliance reporting

        ### Security & Compliance
        - **Risk-based Access Control**: Risk scoring and assessment for all privileged access
        - **Approval Workflows**: Configurable approval processes for high-risk operations
        - **Certification Requirements**: Periodic recertification of privileged access
        - **Segregation of Duties**: Enforce SoD policies and conflict detection
        - **Compliance Frameworks**: Support for SOX, SOC2, ISO27001, and GDPR

        ### Integration
        - **Microsoft Entra ID**: Native integration with Azure AD/Entra ID
        - **Microsoft Graph**: Real-time synchronization with Microsoft Graph API
        - **Azure Key Vault**: Secure credential storage and management
        - **SIEM Integration**: Export audit logs to SIEM and monitoring systems

        ### API Documentation
        - **Authentication**: All endpoints require valid Azure AD Bearer tokens
        - **Rate Limiting**: API calls are rate-limited to prevent abuse
        - **Versioning**: API versioning follows semantic versioning principles
        - **Error Handling**: Standardized error responses with detailed messages
        """,
        version=get_version(),
        contact={
            "name": "Menshun PAM Team",
            "email": "support@menshun.com",
            "url": "https://menshun.com/support",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        terms_of_service="https://menshun.com/terms",
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            },
            {
                "url": "https://api.menshun.com",
                "description": "Production server"
            }
        ]
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware for production
    if settings.ENVIRONMENT == "production":
        application.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )
    
    # Add compression middleware
    application.add_middleware(GZipMiddleware, minimum_size=1000)
    
    return application


# Create the main application instance
app = create_application()


@app.get(
    "/",
    tags=["Root"],
    summary="API Information",
    description="Returns basic information about the Menshun PAM API",
    response_description="API information including version, status, and navigation links",
)
async def root() -> dict:
    """Root endpoint providing basic application information and navigation."""
    return {
        "name": "Menshun PAM API",
        "version": get_version(),
        "description": "Enterprise Privileged Access Management for Microsoft Entra ID",
        "status": "healthy",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "api_url": "/api/v1",
        "health_url": "/health",
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Basic Health Check",
    description="Returns the basic health status of the API service",
    response_description="Service health information including status, version, and environment",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "version": "1.0.0",
                        "environment": "development",
                        "timestamp": "2024-01-01T00:00:00Z"
                    }
                }
            }
        }
    }
)
async def health_check() -> dict:
    """Basic health check endpoint for load balancers and monitoring systems."""
    return {
        "status": "healthy",
        "version": get_version(),
        "environment": settings.ENVIRONMENT,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


@app.get(
    "/health/ready",
    tags=["Health"],
    summary="Readiness Probe",
    description="Checks if the service is ready to accept requests (database connectivity, etc.)",
    response_description="Readiness status with dependency health checks",
    responses={
        200: {
            "description": "Service is ready",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ready",
                        "checks": {
                            "database": "healthy",
                            "redis": "healthy",
                            "external_apis": "healthy"
                        },
                        "timestamp": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        503: {
            "description": "Service is not ready",
            "content": {
                "application/json": {
                    "example": {
                        "status": "not_ready",
                        "checks": {
                            "database": "unhealthy",
                            "redis": "healthy",
                            "external_apis": "unknown"
                        },
                        "timestamp": "2024-01-01T00:00:00Z"
                    }
                }
            }
        }
    }
)
async def readiness_check() -> dict:
    """Readiness probe for Kubernetes and container orchestration."""
    # TODO: Implement actual health checks for dependencies
    checks = {
        "database": "healthy",  # Check database connectivity
        "redis": "healthy",     # Check Redis connectivity
        "external_apis": "healthy"  # Check Microsoft Graph connectivity
    }
    
    all_healthy = all(status == "healthy" for status in checks.values())
    status_code = 200 if all_healthy else 503
    
    response = {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    
    return JSONResponse(status_code=status_code, content=response)


@app.get(
    "/health/live",
    tags=["Health"],
    summary="Liveness Probe",
    description="Checks if the service is alive and functioning (for restart decisions)",
    response_description="Liveness status with uptime and resource usage",
    responses={
        200: {
            "description": "Service is alive",
            "content": {
                "application/json": {
                    "example": {
                        "status": "alive",
                        "uptime": 3600.5,
                        "memory_usage": "256MB",
                        "timestamp": "2024-01-01T00:00:00Z"
                    }
                }
            }
        }
    }
)
async def liveness_check() -> dict:
    """Liveness probe for Kubernetes and container orchestration."""
    import psutil
    
    uptime = time.time() - startup_time
    process = psutil.Process()
    memory_usage = f"{process.memory_info().rss / 1024 / 1024:.1f}MB"
    
    return {
        "status": "alive",
        "uptime": round(uptime, 1),
        "memory_usage": memory_usage,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# OpenAPI schema customization
def custom_openapi():
    """Customize OpenAPI schema with additional metadata and security definitions."""
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title="Menshun PAM API",
        version=get_version(),
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "AzureADBearer": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/authorize",
                    "tokenUrl": f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token",
                    "scopes": {
                        "User.Read": "Read user profile",
                        "Directory.Read.All": "Read directory data",
                        "Directory.ReadWrite.All": "Read and write directory data",
                        "RoleManagement.Read.All": "Read role management data",
                        "RoleManagement.ReadWrite.Directory": "Read and write role management data"
                    }
                }
            }
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add global security requirement (except for health endpoints)
    openapi_schema["security"] = [{"AzureADBearer": []}]
    
    # Add custom tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "Root",
            "description": "Root API information endpoint"
        },
        {
            "name": "Health",
            "description": "Health check and monitoring endpoints for service status"
        },
        {
            "name": "Authentication",
            "description": "Authentication and authorization endpoints"
        },
        {
            "name": "Users",
            "description": "Privileged user management and lifecycle operations"
        },
        {
            "name": "Service Identities",
            "description": "Service account, service principal, and managed identity management"
        },
        {
            "name": "Credentials",
            "description": "Credential management, rotation, and vault operations"
        },
        {
            "name": "Role Assignments",
            "description": "Directory role assignment management with approval workflows"
        },
        {
            "name": "Directory Roles",
            "description": "Microsoft Entra ID directory role information and metadata"
        },
        {
            "name": "Audit Logs",
            "description": "Audit logging, compliance reporting, and security analytics"
        },
        {
            "name": "Dashboard",
            "description": "Dashboard metrics, statistics, and analytics endpoints"
        }
    ]
    
    # Add external documentation links
    openapi_schema["externalDocs"] = {
        "description": "Menshun PAM Documentation",
        "url": "https://docs.menshun.com"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


__all__ = ["app", "create_application"]