"""
Menshun Backend - Session Model.

This module defines the Session model for tracking user authentication sessions,
providing comprehensive session management with security monitoring and
compliance features for the PAM system.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Index, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class Session(FullBaseModel):
    """
    User session model for authentication and activity tracking.
    
    This model tracks user authentication sessions with comprehensive
    security monitoring, geographic tracking, and compliance features.
    It provides detailed session lifecycle management and anomaly detection.
    
    Security Features:
    - Session lifecycle tracking and management
    - Geographic and IP-based monitoring
    - Device fingerprinting and tracking
    - Anomaly detection for suspicious sessions
    - Concurrent session limits and controls
    - Comprehensive audit integration
    """
    
    __tablename__ = "sessions"
    
    # =============================================================================
    # Core Session Information
    # =============================================================================
    
    session_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique session token identifier"
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("privileged_users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="User associated with this session"
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
        doc="User associated with this session"
    )
    
    # =============================================================================
    # Session Lifecycle
    # =============================================================================
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="Timestamp when session was created"
    )
    
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="Timestamp of last session activity"
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        doc="Timestamp when session expires"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Whether the session is currently active"
    )
    
    terminated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when session was terminated"
    )
    
    termination_reason: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Reason for session termination (logout, timeout, admin, security)"
    )
    
    # =============================================================================
    # Authentication Details
    # =============================================================================
    
    authentication_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Authentication method used (password, mfa, sso, certificate)"
    )
    
    mfa_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether MFA was successfully verified for this session"
    )
    
    mfa_methods: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of MFA methods used"
    )
    
    risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=50,
        doc="Risk score for this session (0-100)"
    )
    
    # =============================================================================
    # Network and Geographic Information
    # =============================================================================
    
    source_ip: Mapped[str] = mapped_column(
        String(45),  # IPv6 support
        nullable=False,
        index=True,
        doc="Source IP address of the session"
    )
    
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="User agent string from the browser/client"
    )
    
    geographic_location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Geographic location based on IP (city, country)"
    )
    
    country_code: Mapped[Optional[str]] = mapped_column(
        String(2),
        nullable=True,
        index=True,
        doc="ISO country code based on IP"
    )
    
    timezone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Timezone of the user's location"
    )
    
    # =============================================================================
    # Device and Browser Information
    # =============================================================================
    
    device_fingerprint: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Unique device fingerprint for tracking"
    )
    
    browser_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Browser name (Chrome, Firefox, Safari, etc.)"
    )
    
    browser_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Browser version"
    )
    
    operating_system: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Operating system (Windows, macOS, Linux, etc.)"
    )
    
    device_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Device type (desktop, mobile, tablet)"
    )
    
    is_mobile: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether session is from a mobile device"
    )
    
    # =============================================================================
    # Security and Monitoring
    # =============================================================================
    
    is_suspicious: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Whether session is flagged as suspicious"
    )
    
    anomaly_score: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        doc="Anomaly detection score for behavioral analysis"
    )
    
    security_flags: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of security flags (tor, vpn, proxy, etc.)"
    )
    
    concurrent_session_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Number of concurrent sessions for this user"
    )
    
    # =============================================================================
    # Activity Tracking
    # =============================================================================
    
    request_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of requests made in this session"
    )
    
    privileged_operations_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of privileged operations performed"
    )
    
    failed_operations_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of failed operations in this session"
    )
    
    last_privileged_operation: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last privileged operation"
    )
    
    # =============================================================================
    # Session Metadata
    # =============================================================================
    
    session_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional user-defined session name"
    )
    
    application_context: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Application or service context for the session"
    )
    
    client_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Version of the client application"
    )
    
    # =============================================================================
    # Compliance and Audit
    # =============================================================================
    
    audit_trail: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of key session events for audit"
    )
    
    compliance_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Compliance-related notes for this session"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Composite indexes for common queries
        Index(
            "ix_sessions_user_active",
            "user_id",
            "is_active",
            "last_activity"
        ),
        Index(
            "ix_sessions_ip_created",
            "source_ip",
            "created_at"
        ),
        Index(
            "ix_sessions_suspicious_risk",
            "is_suspicious",
            "risk_score",
            "created_at"
        ),
        Index(
            "ix_sessions_device_fingerprint",
            "device_fingerprint",
            "user_id"
        ),
        Index(
            "ix_sessions_expiry_cleanup",
            "expires_at",
            "is_active",
            # postgresql_where="is_active = true"  # Temporarily commented out for initial migration
        ),
        Index(
            "ix_sessions_geographic",
            "country_code",
            "geographic_location"
        ),
        
        # Partial index for active sessions
        Index(
            "ix_sessions_active_activity",
            "last_activity",
            # postgresql_where="is_active = true"  # Temporarily commented out for initial migration
        ),
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_expired(self) -> bool:
        """
        Check if the session has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        return datetime.utcnow() >= self.expires_at
    
    def is_valid(self) -> bool:
        """
        Check if the session is valid (active and not expired).
        
        Returns:
            bool: True if valid, False otherwise
        """
        return self.is_active and not self.is_expired()
    
    def time_until_expiry(self) -> timedelta:
        """
        Calculate time until session expires.
        
        Returns:
            timedelta: Time until expiry (negative if expired)
        """
        return self.expires_at - datetime.utcnow()
    
    def session_duration(self) -> timedelta:
        """
        Calculate total session duration.
        
        Returns:
            timedelta: Session duration
        """
        end_time = self.terminated_at or datetime.utcnow()
        return end_time - self.created_at
    
    def idle_time(self) -> timedelta:
        """
        Calculate idle time since last activity.
        
        Returns:
            timedelta: Idle time
        """
        return datetime.utcnow() - self.last_activity
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
        self.request_count += 1
    
    def record_privileged_operation(self) -> None:
        """Record a privileged operation in this session."""
        self.privileged_operations_count += 1
        self.last_privileged_operation = datetime.utcnow()
        self.update_activity()
    
    def record_failed_operation(self) -> None:
        """Record a failed operation in this session."""
        self.failed_operations_count += 1
        self.update_activity()
    
    def extend_session(self, hours: int = 8) -> None:
        """
        Extend the session expiry time.
        
        Args:
            hours: Number of hours to extend the session
        """
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def terminate(self, reason: str = "logout") -> None:
        """
        Terminate the session.
        
        Args:
            reason: Reason for termination
        """
        self.is_active = False
        self.terminated_at = datetime.utcnow()
        self.termination_reason = reason
    
    def calculate_risk_score(self) -> int:
        """
        Calculate risk score based on session characteristics.
        
        Returns:
            int: Risk score (0-100)
        """
        score = 20  # Base score
        
        # Geographic risk factors
        if self.country_code and self.country_code not in ["US", "CA", "GB", "AU"]:
            score += 15
        
        # Device and browser factors
        if self.is_mobile:
            score += 5
        
        if not self.device_fingerprint:
            score += 10
        
        # Authentication factors
        if not self.mfa_verified:
            score += 20
        
        # Behavioral factors
        if self.failed_operations_count > 3:
            score += 15
        
        # Time-based factors
        session_hours = self.session_duration().total_seconds() / 3600
        if session_hours > 12:  # Long sessions
            score += 10
        
        # Concurrent sessions
        if self.concurrent_session_count > 2:
            score += 10
        
        return min(100, max(0, score))
    
    def flag_as_suspicious(self, reason: str) -> None:
        """
        Flag session as suspicious.
        
        Args:
            reason: Reason for flagging as suspicious
        """
        self.is_suspicious = True
        self.risk_score = max(self.risk_score, 75)
        
        # Add to compliance notes
        note = f"Flagged as suspicious: {reason} at {datetime.utcnow().isoformat()}"
        if self.compliance_notes:
            self.compliance_notes += f"\n{note}"
        else:
            self.compliance_notes = note
    
    def get_session_summary(self) -> dict:
        """
        Get a summary of the session.
        
        Returns:
            dict: Session summary
        """
        return {
            "session_id": str(self.id),
            "session_token": self.session_token,
            "user_upn": self.user.upn if self.user else None,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "is_active": self.is_active,
            "is_valid": self.is_valid(),
            "source_ip": self.source_ip,
            "geographic_location": self.geographic_location,
            "device_type": self.device_type,
            "browser_name": self.browser_name,
            "mfa_verified": self.mfa_verified,
            "risk_score": self.risk_score,
            "is_suspicious": self.is_suspicious,
            "request_count": self.request_count,
            "privileged_operations_count": self.privileged_operations_count,
            "session_duration_hours": self.session_duration().total_seconds() / 3600,
        }
    
    def __str__(self) -> str:
        """String representation of the session."""
        user_upn = self.user.upn if self.user else "Unknown"
        return f"Session({user_upn}, {self.source_ip})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the session."""
        return (
            f"<Session(id={self.id}, user_id={self.user_id}, "
            f"token={self.session_token[:8]}..., active={self.is_active})>"
        )


__all__ = ["Session"]