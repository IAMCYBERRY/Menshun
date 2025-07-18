"""
Menshun Backend - Credential Model.

This module defines models for credential storage, encryption, and rotation
management. It provides secure storage for passwords, client secrets, and
other sensitive authentication materials with comprehensive audit trails.
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text, 
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class CredentialType(str, Enum):
    """Enumeration of supported credential types."""
    PASSWORD = "password"
    CLIENT_SECRET = "client_secret"
    CERTIFICATE = "certificate"
    API_KEY = "api_key"
    TOKEN = "token"
    SSH_KEY = "ssh_key"


class CredentialStatus(str, Enum):
    """Enumeration of credential status values."""
    ACTIVE = "active"
    EXPIRED = "expired"
    ROTATED = "rotated"
    REVOKED = "revoked"
    PENDING_ROTATION = "pending_rotation"


class RotationStatus(str, Enum):
    """Enumeration of rotation status values."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Credential(FullBaseModel):
    """
    Credential model for secure storage of authentication materials.
    
    This model provides secure storage for various types of credentials
    including passwords, client secrets, certificates, and API keys.
    All credential values are encrypted at rest and access is logged.
    
    Security Features:
    - Encryption at rest for all credential values
    - Comprehensive audit logging for access
    - Automatic rotation scheduling and tracking
    - Version management for credential history
    - Secure metadata storage without exposing values
    
    Supported Credential Types:
    - Passwords (service account passwords)
    - Client Secrets (service principal secrets)
    - Certificates (X.509 certificates and private keys)
    - API Keys (third-party service keys)
    - Tokens (long-lived access tokens)
    - SSH Keys (public/private key pairs)
    """
    
    __tablename__ = "credentials"
    
    # =============================================================================
    # Core Credential Information
    # =============================================================================
    
    credential_type: Mapped[CredentialType] = mapped_column(
        Enum(CredentialType, name="credential_type_enum"),
        nullable=False,
        index=True,
        doc="Type of credential being stored"
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Display name for the credential"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Description of the credential purpose and usage"
    )
    
    # =============================================================================
    # Service Identity Relationship
    # =============================================================================
    
    service_identity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_identities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Service identity that owns this credential"
    )
    
    service_identity: Mapped["ServiceIdentity"] = relationship(
        "ServiceIdentity",
        back_populates="credentials",
        doc="Service identity that owns this credential"
    )
    
    # =============================================================================
    # Encrypted Credential Storage
    # =============================================================================
    
    vault_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        index=True,
        doc="Path to the credential in the vault backend"
    )
    
    vault_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Version identifier in the vault system"
    )
    
    encrypted_metadata: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Encrypted metadata about the credential (non-sensitive)"
    )
    
    # Note: The actual credential value is NOT stored in the database
    # It is stored in the configured vault backend (Azure Key Vault, etc.)
    
    # =============================================================================
    # Credential Lifecycle and Status
    # =============================================================================
    
    status: Mapped[CredentialStatus] = mapped_column(
        Enum(CredentialStatus, name="credential_status_enum"),
        nullable=False,
        default=CredentialStatus.ACTIVE,
        index=True,
        doc="Current status of the credential"
    )
    
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Date when credential was created"
    )
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Expiration date for the credential"
    )
    
    last_used: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp when credential was last accessed"
    )
    
    use_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of times credential has been accessed"
    )
    
    # =============================================================================
    # Rotation Configuration and Tracking
    # =============================================================================
    
    rotation_frequency_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=90,
        doc="Frequency of automatic rotation in days"
    )
    
    next_rotation_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Next scheduled rotation date"
    )
    
    last_rotated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last successful rotation"
    )
    
    rotation_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of times credential has been rotated"
    )
    
    auto_rotation_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether automatic rotation is enabled"
    )
    
    # =============================================================================
    # Security and Compliance
    # =============================================================================
    
    strength_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Strength score of the credential (0-100)"
    )
    
    complexity_requirements: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON object describing complexity requirements"
    )
    
    requires_encryption: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether credential requires encryption at rest"
    )
    
    access_restrictions: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of access restriction rules"
    )
    
    # =============================================================================
    # External System Integration
    # =============================================================================
    
    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="External system identifier for this credential"
    )
    
    external_system: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Name of external system managing this credential"
    )
    
    sync_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether credential is synced with external system"
    )
    
    last_sync: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last synchronization"
    )
    
    # =============================================================================
    # Notification and Alerting
    # =============================================================================
    
    notification_days_before_expiry: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=14,
        doc="Days before expiry to send notifications"
    )
    
    notification_sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether expiry notification has been sent"
    )
    
    emergency_contact: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Emergency contact for credential issues"
    )
    
    # =============================================================================
    # Relationships
    # =============================================================================
    
    # Rotation history for this credential
    rotation_history: Mapped[List["CredentialRotation"]] = relationship(
        "CredentialRotation",
        back_populates="credential",
        cascade="all, delete-orphan",
        order_by="CredentialRotation.created_at.desc()",
        doc="History of rotations for this credential"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Composite indexes for common queries
        Index(
            "ix_credentials_service_type",
            "service_identity_id",
            "credential_type"
        ),
        Index(
            "ix_credentials_status_type",
            "status",
            "credential_type"
        ),
        Index(
            "ix_credentials_rotation_schedule",
            "next_rotation_date",
            "auto_rotation_enabled",
            postgresql_where="next_rotation_date IS NOT NULL AND auto_rotation_enabled = true"
        ),
        Index(
            "ix_credentials_expiry",
            "expires_at",
            "status",
            postgresql_where="expires_at IS NOT NULL AND status = 'active'"
        ),
        Index(
            "ix_credentials_usage",
            "last_used",
            "use_count"
        ),
        
        # Partial index for active credentials
        Index(
            "ix_credentials_active_name",
            "name",
            postgresql_where="status = 'active' AND is_deleted = false"
        ),
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_expired(self) -> bool:
        """
        Check if the credential has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if not self.expires_at:
            return False
        return datetime.utcnow() >= self.expires_at
    
    def needs_rotation(self) -> bool:
        """
        Check if the credential needs rotation.
        
        Returns:
            bool: True if rotation is needed
        """
        if not self.auto_rotation_enabled:
            return False
        
        if not self.next_rotation_date:
            return True
        
        return datetime.utcnow() >= self.next_rotation_date
    
    def days_until_expiry(self) -> Optional[int]:
        """
        Calculate days until credential expires.
        
        Returns:
            Optional[int]: Days until expiry, None if no expiry date
        """
        if not self.expires_at:
            return None
        
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)
    
    def needs_notification(self) -> bool:
        """
        Check if expiry notification should be sent.
        
        Returns:
            bool: True if notification should be sent
        """
        if self.notification_sent or not self.expires_at:
            return False
        
        days_until = self.days_until_expiry()
        if days_until is None:
            return False
        
        return days_until <= self.notification_days_before_expiry
    
    def record_access(self) -> None:
        """Record that the credential was accessed."""
        self.last_used = datetime.utcnow()
        self.use_count += 1
    
    def schedule_rotation(self, days_from_now: Optional[int] = None) -> None:
        """
        Schedule next rotation.
        
        Args:
            days_from_now: Days from now to schedule rotation
        """
        if days_from_now is None:
            days_from_now = self.rotation_frequency_days
        
        self.next_rotation_date = datetime.utcnow() + timedelta(days=days_from_now)
    
    def mark_rotated(self) -> None:
        """Mark credential as successfully rotated."""
        self.last_rotated = datetime.utcnow()
        self.rotation_count += 1
        self.schedule_rotation()
        
        # Reset notification flag
        self.notification_sent = False
    
    def generate_vault_path(self) -> str:
        """
        Generate a unique vault path for this credential.
        
        Returns:
            str: Vault path
        """
        if self.service_identity:
            service_name = self.service_identity.name.lower().replace(" ", "-")
        else:
            service_name = "unknown"
        
        cred_type = self.credential_type.value
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        
        return f"credentials/{service_name}/{cred_type}/{timestamp}/{self.id}"
    
    def get_security_summary(self) -> dict:
        """
        Get security summary for this credential.
        
        Returns:
            dict: Security summary
        """
        return {
            "type": self.credential_type.value,
            "status": self.status.value,
            "is_expired": self.is_expired(),
            "needs_rotation": self.needs_rotation(),
            "days_until_expiry": self.days_until_expiry(),
            "strength_score": self.strength_score,
            "use_count": self.use_count,
            "rotation_count": self.rotation_count,
            "auto_rotation_enabled": self.auto_rotation_enabled,
        }
    
    def __str__(self) -> str:
        """String representation of the credential."""
        return f"Credential({self.name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the credential."""
        return (
            f"<Credential(id={self.id}, name={self.name}, "
            f"type={self.credential_type.value}, status={self.status.value})>"
        )


class CredentialRotation(FullBaseModel):
    """
    Credential Rotation tracking model.
    
    This model tracks the history and status of credential rotation operations,
    providing audit trails and operational insights for credential management.
    """
    
    __tablename__ = "credential_rotations"
    
    # =============================================================================
    # Core Rotation Information
    # =============================================================================
    
    credential_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("credentials.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Credential being rotated"
    )
    
    credential: Mapped["Credential"] = relationship(
        "Credential",
        back_populates="rotation_history",
        doc="Credential being rotated"
    )
    
    # =============================================================================
    # Rotation Status and Timing
    # =============================================================================
    
    status: Mapped[RotationStatus] = mapped_column(
        Enum(RotationStatus, name="rotation_status_enum"),
        nullable=False,
        default=RotationStatus.SCHEDULED,
        index=True,
        doc="Current status of the rotation"
    )
    
    scheduled_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="Date when rotation was scheduled"
    )
    
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when rotation started"
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when rotation completed"
    )
    
    # =============================================================================
    # Rotation Details and Results
    # =============================================================================
    
    rotation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="automatic",
        doc="Type of rotation (automatic, manual, emergency)"
    )
    
    triggered_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="User or system that triggered the rotation"
    )
    
    reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Reason for the rotation"
    )
    
    old_vault_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="Vault path of the old credential"
    )
    
    new_vault_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="Vault path of the new credential"
    )
    
    # =============================================================================
    # Error Handling and Retry Logic
    # =============================================================================
    
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Error message if rotation failed"
    )
    
    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of retry attempts"
    )
    
    max_retries: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
        doc="Maximum number of retry attempts"
    )
    
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp for next retry attempt"
    )
    
    # =============================================================================
    # Verification and Validation
    # =============================================================================
    
    verification_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        doc="Status of credential verification (pending, success, failed)"
    )
    
    verification_details: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Details of verification process"
    )
    
    rollback_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether rollback to old credential is possible"
    )
    
    # =============================================================================
    # Operational Metadata
    # =============================================================================
    
    duration_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Duration of rotation operation in seconds"
    )
    
    systems_updated: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of external systems updated during rotation"
    )
    
    notifications_sent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of notifications sent during rotation"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Composite indexes for queries
        Index(
            "ix_credential_rotations_cred_status",
            "credential_id",
            "status"
        ),
        Index(
            "ix_credential_rotations_scheduled",
            "scheduled_date",
            "status"
        ),
        Index(
            "ix_credential_rotations_retry",
            "next_retry_at",
            postgresql_where="next_retry_at IS NOT NULL AND status = 'failed'"
        ),
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def can_retry(self) -> bool:
        """
        Check if rotation can be retried.
        
        Returns:
            bool: True if retry is possible
        """
        return (
            self.status == RotationStatus.FAILED and
            self.retry_count < self.max_retries
        )
    
    def calculate_duration(self) -> Optional[int]:
        """
        Calculate rotation duration in seconds.
        
        Returns:
            Optional[int]: Duration in seconds, None if not completed
        """
        if not self.started_at or not self.completed_at:
            return None
        
        delta = self.completed_at - self.started_at
        return int(delta.total_seconds())
    
    def mark_started(self) -> None:
        """Mark rotation as started."""
        self.status = RotationStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
    
    def mark_completed(self, new_vault_path: str) -> None:
        """
        Mark rotation as completed successfully.
        
        Args:
            new_vault_path: Path to the new credential in vault
        """
        self.status = RotationStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.new_vault_path = new_vault_path
        self.duration_seconds = self.calculate_duration()
    
    def mark_failed(self, error_message: str) -> None:
        """
        Mark rotation as failed.
        
        Args:
            error_message: Description of the failure
        """
        self.status = RotationStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        self.duration_seconds = self.calculate_duration()
        
        # Schedule retry if possible
        if self.can_retry():
            self.retry_count += 1
            # Exponential backoff: 2^retry_count minutes
            retry_delay = timedelta(minutes=2 ** self.retry_count)
            self.next_retry_at = datetime.utcnow() + retry_delay
    
    def __str__(self) -> str:
        """String representation of the rotation."""
        return f"CredentialRotation({self.credential_id}, {self.status.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the rotation."""
        return (
            f"<CredentialRotation(id={self.id}, credential_id={self.credential_id}, "
            f"status={self.status.value}, scheduled={self.scheduled_date})>"
        )


__all__ = [
    "Credential",
    "CredentialRotation", 
    "CredentialType",
    "CredentialStatus",
    "RotationStatus",
]