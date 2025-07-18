"""
Menshun Backend - Audit Log Model.

This module defines the AuditLog model for comprehensive security and compliance
audit trails throughout the PAM system. It provides immutable logging of all
security-relevant events with detailed context and metadata.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Index, String, Text, 
    event, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel  # Note: Using BaseModel, not FullBaseModel for immutability


class AuditLog(BaseModel):
    """
    Comprehensive audit log model for security and compliance tracking.
    
    This model provides immutable audit trails for all security-relevant
    operations in the PAM system. It supports various event types with
    detailed context and metadata for compliance and forensic analysis.
    
    Key Features:
    - Immutable audit records (no updates allowed)
    - Comprehensive event categorization
    - Detailed context and metadata storage
    - Integration with compliance frameworks
    - Support for correlation IDs and request tracking
    - Geographic and IP-based tracking
    - Risk scoring for audit events
    
    Security Features:
    - Immutable records prevent tampering
    - Cryptographic integrity checking
    - Structured logging with correlation IDs
    - Retention policy enforcement
    - Compliance framework mapping
    """
    
    __tablename__ = "audit_logs"
    
    # =============================================================================
    # Core Event Information
    # =============================================================================
    
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Type of event (authentication, authorization, privileged_operation, etc.)"
    )
    
    event_subtype: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="Subtype for more granular event classification"
    )
    
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Specific action performed (create, update, delete, access, etc.)"
    )
    
    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        doc="Result of the action (success, failure, denied, error)"
    )
    
    # =============================================================================
    # Temporal Information
    # =============================================================================
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="Exact timestamp when event occurred"
    )
    
    duration_ms: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Duration of the operation in milliseconds"
    )
    
    # =============================================================================
    # Actor Information (Who performed the action)
    # =============================================================================
    
    actor_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("privileged_users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="User who performed the action"
    )
    
    actor_user: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[actor_user_id],
        doc="User who performed the action"
    )
    
    actor_service_identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_identities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Service identity that performed the action"
    )
    
    actor_service_identity: Mapped[Optional["ServiceIdentity"]] = relationship(
        "ServiceIdentity",
        foreign_keys=[actor_service_identity_id],
        doc="Service identity that performed the action"
    )
    
    actor_upn: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="UPN of the actor (for cases where actor is not in our database)"
    )
    
    actor_display_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Display name of the actor"
    )
    
    # =============================================================================
    # Target Information (What was acted upon)
    # =============================================================================
    
    target_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("privileged_users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="User that was the target of the action"
    )
    
    target_user: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[target_user_id],
        doc="User that was the target of the action"
    )
    
    target_service_identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_identities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Service identity that was the target of the action"
    )
    
    target_service_identity: Mapped[Optional["ServiceIdentity"]] = relationship(
        "ServiceIdentity",
        foreign_keys=[target_service_identity_id],
        doc="Service identity that was the target of the action"
    )
    
    target_resource_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="Type of resource that was targeted (user, role, credential, etc.)"
    )
    
    target_resource_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="ID of the specific resource that was targeted"
    )
    
    target_resource_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Name of the resource that was targeted"
    )
    
    # =============================================================================
    # Request and Session Context
    # =============================================================================
    
    session_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Session ID associated with the event"
    )
    
    correlation_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Correlation ID for request tracking"
    )
    
    request_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Unique request identifier"
    )
    
    transaction_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Transaction identifier for multi-step operations"
    )
    
    # =============================================================================
    # Network and Geographic Context
    # =============================================================================
    
    source_ip: Mapped[Optional[str]] = mapped_column(
        String(45),  # IPv6 support
        nullable=True,
        index=True,
        doc="Source IP address of the request"
    )
    
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="User agent string from the request"
    )
    
    geographic_location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Geographic location (city, country) based on IP"
    )
    
    # =============================================================================
    # Detailed Event Information
    # =============================================================================
    
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Human-readable description of the event"
    )
    
    details: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed information about the event (JSON format)"
    )
    
    previous_values: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Previous values before change (JSON format)"
    )
    
    new_values: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="New values after change (JSON format)"
    )
    
    # =============================================================================
    # Risk and Security Assessment
    # =============================================================================
    
    risk_score: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Risk score for this event (0-100)"
    )
    
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="info",
        index=True,
        doc="Severity level (low, info, warning, high, critical)"
    )
    
    is_suspicious: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Whether this event is flagged as suspicious"
    )
    
    anomaly_score: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        doc="Anomaly detection score for behavioral analysis"
    )
    
    # =============================================================================
    # Compliance and Regulatory
    # =============================================================================
    
    compliance_frameworks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of relevant compliance frameworks"
    )
    
    regulatory_classification: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Regulatory classification for the event"
    )
    
    retention_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Date when this record can be purged for compliance"
    )
    
    # =============================================================================
    # System and Application Context
    # =============================================================================
    
    application: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="menshun-backend",
        doc="Application that generated the event"
    )
    
    service: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Specific service within the application"
    )
    
    api_endpoint: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="API endpoint that was called"
    )
    
    http_method: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        doc="HTTP method used (GET, POST, etc.)"
    )
    
    response_code: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="HTTP response code"
    )
    
    # =============================================================================
    # Error and Exception Information
    # =============================================================================
    
    error_code: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="Application-specific error code"
    )
    
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Error message if the action failed"
    )
    
    stack_trace: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Stack trace for debugging (sanitized)"
    )
    
    # =============================================================================
    # Data Integrity and Verification
    # =============================================================================
    
    checksum: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        doc="SHA-256 checksum for integrity verification"
    )
    
    signature: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Digital signature for non-repudiation"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Basic indexes for common audit queries
        Index(
            "ix_audit_logs_timestamp_type",
            "timestamp",
            "event_type"
        ),
        Index(
            "ix_audit_logs_actor_timestamp",
            "actor_upn",
            "timestamp"
        ),
        Index(
            "ix_audit_logs_target_timestamp",
            "target_resource_type",
            "target_resource_id",
            "timestamp"
        ),
        Index(
            "ix_audit_logs_session_correlation",
            "session_id",
            "correlation_id"
        ),
        Index(
            "ix_audit_logs_severity_suspicious",
            "severity",
            "is_suspicious",
            "timestamp"
        ),
        Index(
            "ix_audit_logs_source_ip",
            "source_ip",
            "timestamp"
        ),
        Index(
            "ix_audit_logs_retention",
            "retention_date"
        ),
        # Note: Advanced indexes (GIN, full-text search, compliance)
        # will be added in separate migrations after basic table structure
        # and after required extensions are installed
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def get_actor_name(self) -> str:
        """
        Get the name of the actor who performed the action.
        
        Returns:
            str: Actor name or identifier
        """
        if self.actor_user:
            return self.actor_user.display_name or self.actor_user.upn
        elif self.actor_service_identity:
            return self.actor_service_identity.name
        elif self.actor_upn:
            return self.actor_upn
        elif self.actor_display_name:
            return self.actor_display_name
        else:
            return "System"
    
    def get_target_name(self) -> Optional[str]:
        """
        Get the name of the target resource.
        
        Returns:
            Optional[str]: Target name or None if no target
        """
        if self.target_user:
            return self.target_user.display_name or self.target_user.upn
        elif self.target_service_identity:
            return self.target_service_identity.name
        elif self.target_resource_name:
            return self.target_resource_name
        else:
            return None
    
    def is_high_risk(self) -> bool:
        """
        Check if this is a high-risk audit event.
        
        Returns:
            bool: True if high risk
        """
        return (
            self.severity in ["high", "critical"] or
            self.is_suspicious or
            (self.risk_score and self.risk_score >= 75)
        )
    
    def get_retention_period_days(self) -> int:
        """
        Get retention period in days based on event type and compliance.
        
        Returns:
            int: Retention period in days
        """
        # Base retention periods by event type
        retention_map = {
            "authentication": 365,      # 1 year
            "authorization": 365,       # 1 year
            "privileged_operation": 2555,  # 7 years
            "credential_access": 2555,  # 7 years
            "compliance": 2555,         # 7 years
            "security_incident": 2555,  # 7 years
        }
        
        base_retention = retention_map.get(self.event_type, 365)
        
        # Extend for high-risk events
        if self.is_high_risk():
            base_retention = max(base_retention, 2555)
        
        return base_retention
    
    def calculate_checksum(self) -> str:
        """
        Calculate SHA-256 checksum for integrity verification.
        
        Returns:
            str: SHA-256 checksum
        """
        import hashlib
        import json
        
        # Create a deterministic representation of the audit record
        data = {
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "action": self.action,
            "result": self.result,
            "actor_upn": self.actor_upn,
            "target_resource_type": self.target_resource_type,
            "target_resource_id": self.target_resource_id,
            "description": self.description,
            "source_ip": self.source_ip,
        }
        
        # Sort keys for deterministic output
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def to_compliance_record(self) -> dict:
        """
        Convert to compliance record format.
        
        Returns:
            dict: Compliance-formatted audit record
        """
        return {
            "event_id": str(self.id),
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "action": self.action,
            "result": self.result,
            "actor": self.get_actor_name(),
            "target": self.get_target_name(),
            "description": self.description,
            "severity": self.severity,
            "source_ip": self.source_ip,
            "compliance_frameworks": self.compliance_frameworks,
            "retention_date": self.retention_date.isoformat() if self.retention_date else None,
            "checksum": self.checksum,
        }
    
    def __str__(self) -> str:
        """String representation of the audit log."""
        return f"AuditLog({self.event_type}: {self.action} by {self.get_actor_name()})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the audit log."""
        return (
            f"<AuditLog(id={self.id}, type={self.event_type}, "
            f"action={self.action}, result={self.result}, "
            f"timestamp={self.timestamp})>"
        )


# SQLAlchemy event listeners for audit log integrity
@event.listens_for(AuditLog, "before_insert")
def calculate_checksum_before_insert(mapper, connection, target):
    """Calculate checksum before inserting audit record."""
    target.checksum = target.calculate_checksum()


@event.listens_for(AuditLog, "before_update")
def prevent_audit_log_updates(mapper, connection, target):
    """Prevent updates to audit logs for immutability."""
    raise ValueError("Audit logs are immutable and cannot be updated")


@event.listens_for(AuditLog, "before_delete") 
def prevent_audit_log_deletions(mapper, connection, target):
    """Prevent deletion of audit logs except through retention policies."""
    # This could be enhanced to allow deletion only by retention cleanup jobs
    raise ValueError("Audit logs cannot be deleted except through retention policies")


__all__ = ["AuditLog"]