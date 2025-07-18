"""
Menshun Backend - Logging Configuration.

This module provides structured logging configuration with support for JSON formatting,
correlation IDs, audit trails, and integration with monitoring systems.
"""

import json
import logging
import logging.config
import sys
import time
from typing import Any, Dict, Optional

import structlog
from structlog.stdlib import LoggerFactory

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure structured logging for the application.
    
    Sets up structured logging with JSON formatting, timestamp standardization,
    and appropriate log levels based on the environment configuration.
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL),
    )
    
    # Configure structlog processors
    processors = [
        # Add timestamp
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        # Add custom processors
        add_correlation_id,
        add_service_info,
    ]
    
    # Add JSON formatting for production
    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )


def add_correlation_id(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add correlation ID to log events.
    
    Args:
        logger: The logger instance
        method_name: The method name being called
        event_dict: The event dictionary
        
    Returns:
        Dict[str, Any]: Event dictionary with correlation ID
    """
    # This would typically get the correlation ID from the request context
    # For now, we'll use a placeholder
    event_dict["correlation_id"] = getattr(logger, "_context", {}).get("correlation_id", "unknown")
    return event_dict


def add_service_info(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add service information to log events.
    
    Args:
        logger: The logger instance
        method_name: The method name being called
        event_dict: The event dictionary
        
    Returns:
        Dict[str, Any]: Event dictionary with service info
    """
    event_dict.update({
        "service": "menshun-backend",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    })
    return event_dict


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        structlog.stdlib.BoundLogger: Configured logger instance
    """
    return structlog.get_logger(name)


class AuditLogger:
    """
    Specialized logger for audit events.
    
    This class provides methods for logging security-relevant events
    with standardized formats for compliance and monitoring.
    """
    
    def __init__(self) -> None:
        """Initialize the audit logger."""
        self.logger = get_logger("audit")
    
    def log_authentication(
        self,
        user_id: str,
        action: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log authentication events.
        
        Args:
            user_id: User identifier
            action: Authentication action (login, logout, etc.)
            success: Whether the action succeeded
            ip_address: Client IP address
            user_agent: Client user agent
            additional_data: Additional event data
        """
        event_data = {
            "event_type": "authentication",
            "user_id": user_id,
            "action": action,
            "success": success,
            "timestamp": time.time(),
        }
        
        if ip_address:
            event_data["ip_address"] = ip_address
        
        if user_agent:
            event_data["user_agent"] = user_agent
        
        if additional_data:
            event_data.update(additional_data)
        
        log_method = self.logger.info if success else self.logger.warning
        log_method("Authentication event", **event_data)
    
    def log_authorization(
        self,
        user_id: str,
        resource: str,
        action: str,
        granted: bool,
        reason: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log authorization events.
        
        Args:
            user_id: User identifier
            resource: Resource being accessed
            action: Action being performed
            granted: Whether access was granted
            reason: Reason for the decision
            additional_data: Additional event data
        """
        event_data = {
            "event_type": "authorization",
            "user_id": user_id,
            "resource": resource,
            "action": action,
            "granted": granted,
            "timestamp": time.time(),
        }
        
        if reason:
            event_data["reason"] = reason
        
        if additional_data:
            event_data.update(additional_data)
        
        log_method = self.logger.info if granted else self.logger.warning
        log_method("Authorization event", **event_data)
    
    def log_privileged_operation(
        self,
        user_id: str,
        operation: str,
        target: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log privileged operations.
        
        Args:
            user_id: User performing the operation
            operation: Type of operation
            target: Target of the operation
            success: Whether the operation succeeded
            details: Additional operation details
        """
        event_data = {
            "event_type": "privileged_operation",
            "user_id": user_id,
            "operation": operation,
            "target": target,
            "success": success,
            "timestamp": time.time(),
        }
        
        if details:
            event_data["details"] = details
        
        log_method = self.logger.info if success else self.logger.error
        log_method("Privileged operation", **event_data)
    
    def log_credential_access(
        self,
        user_id: str,
        credential_id: str,
        action: str,
        success: bool,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log credential access events.
        
        Args:
            user_id: User accessing the credential
            credential_id: Credential identifier
            action: Action performed (retrieve, rotate, etc.)
            success: Whether the action succeeded
            additional_data: Additional event data
        """
        event_data = {
            "event_type": "credential_access",
            "user_id": user_id,
            "credential_id": credential_id,
            "action": action,
            "success": success,
            "timestamp": time.time(),
        }
        
        if additional_data:
            event_data.update(additional_data)
        
        log_method = self.logger.info if success else self.logger.warning
        log_method("Credential access", **event_data)
    
    def log_compliance_event(
        self,
        event_type: str,
        description: str,
        compliance_framework: str,
        severity: str = "info",
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log compliance-related events.
        
        Args:
            event_type: Type of compliance event
            description: Event description
            compliance_framework: Relevant compliance framework (SOX, SOC2, etc.)
            severity: Event severity
            additional_data: Additional event data
        """
        event_data = {
            "event_type": "compliance",
            "compliance_event_type": event_type,
            "description": description,
            "compliance_framework": compliance_framework,
            "severity": severity,
            "timestamp": time.time(),
        }
        
        if additional_data:
            event_data.update(additional_data)
        
        # Map severity to log level
        severity_map = {
            "debug": self.logger.debug,
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical,
        }
        
        log_method = severity_map.get(severity.lower(), self.logger.info)
        log_method("Compliance event", **event_data)


# Global audit logger instance
audit_logger = AuditLogger()


def get_audit_logger() -> AuditLogger:
    """
    Get the global audit logger instance.
    
    Returns:
        AuditLogger: The audit logger instance
    """
    return audit_logger


class RequestLogger:
    """
    Logger for HTTP request/response events.
    
    This class provides standardized logging for API requests and responses,
    including timing, status codes, and error information.
    """
    
    def __init__(self) -> None:
        """Initialize the request logger."""
        self.logger = get_logger("requests")
    
    def log_request(
        self,
        method: str,
        path: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> None:
        """
        Log incoming HTTP request.
        
        Args:
            method: HTTP method
            path: Request path
            user_id: Authenticated user ID
            ip_address: Client IP address
            user_agent: Client user agent
            correlation_id: Request correlation ID
        """
        event_data = {
            "event_type": "request_start",
            "method": method,
            "path": path,
            "timestamp": time.time(),
        }
        
        if user_id:
            event_data["user_id"] = user_id
        
        if ip_address:
            event_data["ip_address"] = ip_address
        
        if user_agent:
            event_data["user_agent"] = user_agent
        
        if correlation_id:
            event_data["correlation_id"] = correlation_id
        
        self.logger.info("Request started", **event_data)
    
    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        user_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        """
        Log HTTP response.
        
        Args:
            method: HTTP method
            path: Request path
            status_code: HTTP status code
            duration_ms: Request duration in milliseconds
            user_id: Authenticated user ID
            correlation_id: Request correlation ID
            error: Error message if applicable
        """
        event_data = {
            "event_type": "request_complete",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "timestamp": time.time(),
        }
        
        if user_id:
            event_data["user_id"] = user_id
        
        if correlation_id:
            event_data["correlation_id"] = correlation_id
        
        if error:
            event_data["error"] = error
        
        # Log level based on status code
        if status_code >= 500:
            log_level = self.logger.error
        elif status_code >= 400:
            log_level = self.logger.warning
        else:
            log_level = self.logger.info
        
        log_level("Request completed", **event_data)


# Global request logger instance
request_logger = RequestLogger()


def get_request_logger() -> RequestLogger:
    """
    Get the global request logger instance.
    
    Returns:
        RequestLogger: The request logger instance
    """
    return request_logger


__all__ = [
    "configure_logging",
    "get_logger",
    "AuditLogger",
    "audit_logger",
    "get_audit_logger",
    "RequestLogger",
    "request_logger",
    "get_request_logger",
]