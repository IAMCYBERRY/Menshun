"""
Menshun Backend - User Model.

This module defines the User model for privileged user accounts created
from source Azure AD users. It includes all necessary fields for user
management, authentication tracking, and compliance requirements.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class User(FullBaseModel):
    """
    Privileged user model for Azure AD user accounts.
    
    This model represents privileged user accounts created from source Azure AD users.
    It maintains references to the original user and tracks all privileged access
    activities for security and compliance purposes.
    
    Key Features:
    - Links to source Azure AD user
    - Tracks privileged account lifecycle
    - Maintains security and compliance metadata
    - Supports temporary access passes (TAP)
    - Comprehensive audit trail integration
    
    Security Considerations:
    - UPN must be unique across the system
    - Source user tracking for audit trails
    - Employee type classification for access control
    - Active status management for security
    """
    
    __tablename__ = "privileged_users"
    
    # =============================================================================
    # Core User Identity Fields
    # =============================================================================
    
    upn: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="User Principal Name (UPN) for the privileged account"
    )
    
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Display name for the privileged user"
    )
    
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Email address for the privileged account"
    )
    
    # =============================================================================
    # Source User Tracking
    # =============================================================================
    
    source_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Azure AD object ID of the source user"
    )
    
    source_user_upn: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="UPN of the source Azure AD user"
    )
    
    source_user_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Email of the source Azure AD user"
    )
    
    # =============================================================================
    # Organizational Information
    # =============================================================================
    
    employee_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Admin",
        doc="Employee type classification (Admin, Service, etc.)"
    )
    
    department: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Department of the user"
    )
    
    job_title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Job title of the user"
    )
    
    company_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Company or organization name"
    )
    
    office_location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Physical office location"
    )
    
    manager_upn: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="UPN of the user's manager"
    )
    
    # =============================================================================
    # Account Status and Management
    # =============================================================================
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Whether the privileged account is active"
    )
    
    account_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether the account is enabled in Azure AD"
    )
    
    blocked_sign_in: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether sign-in is blocked for this account"
    )
    
    # =============================================================================
    # Authentication and Security
    # =============================================================================
    
    azure_object_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        doc="Azure AD object ID for the privileged account"
    )
    
    password_profile: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Encrypted password profile information"
    )
    
    force_change_password: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether user must change password on next login"
    )
    
    # =============================================================================
    # Temporary Access Pass (TAP) Management
    # =============================================================================
    
    last_tap_generated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when last TAP was generated"
    )
    
    tap_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Number of TAPs generated for this user"
    )
    
    # =============================================================================
    # Usage Location and Licensing
    # =============================================================================
    
    usage_location: Mapped[Optional[str]] = mapped_column(
        String(2),
        nullable=True,
        doc="ISO 3166-1 alpha-2 country code for usage location"
    )
    
    preferred_language: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        doc="Preferred language for the user"
    )
    
    # =============================================================================
    # Activity Tracking
    # =============================================================================
    
    last_sign_in: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp of last successful sign-in"
    )
    
    last_activity: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp of last activity"
    )
    
    sign_in_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Total number of sign-ins"
    )
    
    failed_sign_in_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Total number of failed sign-in attempts"
    )
    
    # =============================================================================
    # Risk and Security Scoring
    # =============================================================================
    
    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        doc="Risk level assessment (low, medium, high, critical)"
    )
    
    risk_score: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Numeric risk score (0-100)"
    )
    
    last_risk_assessment: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last risk assessment"
    )
    
    # =============================================================================
    # Compliance and Audit Fields
    # =============================================================================
    
    compliance_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="compliant",
        doc="Compliance status (compliant, non_compliant, pending_review)"
    )
    
    last_compliance_check: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last compliance check"
    )
    
    certification_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether this account requires periodic certification"
    )
    
    next_certification_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Date when next certification is due"
    )
    
    # =============================================================================
    # Relationships
    # =============================================================================
    
    # Role assignments for this user
    role_assignments: Mapped[List["RoleAssignment"]] = relationship(
        "RoleAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="Directory roles assigned to this user"
    )
    
    # Audit logs related to this user
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        foreign_keys="AuditLog.target_user_id",
        back_populates="target_user",
        doc="Audit logs where this user is the target"
    )
    
    # Sessions for this user
    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="Active and historical sessions for this user"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Unique constraint on source user to prevent duplicate privileged accounts
        UniqueConstraint(
            "source_user_id",
            name="uq_privileged_users_source_user_id"
        ),
        
        # Composite indexes for common queries
        Index(
            "ix_privileged_users_active_department",
            "is_active",
            "department"
        ),
        Index(
            "ix_privileged_users_risk_level_score",
            "risk_level",
            "risk_score"
        ),
        Index(
            "ix_privileged_users_compliance_status",
            "compliance_status",
            "last_compliance_check"
        ),
        Index(
            "ix_privileged_users_activity",
            "last_sign_in",
            "last_activity"
        ),
        
        # Partial index for active users only (performance optimization)
        Index(
            "ix_privileged_users_active_upn",
            "upn",
            postgresql_where="is_active = true AND is_deleted = false"
        ),
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_account_healthy(self) -> bool:
        """
        Check if the account is in a healthy state.
        
        Returns:
            bool: True if account is healthy, False otherwise
        """
        return (
            self.is_active and
            self.account_enabled and
            not self.blocked_sign_in and
            not self.is_deleted and
            self.compliance_status == "compliant"
        )
    
    def needs_certification(self) -> bool:
        """
        Check if the account needs certification.
        
        Returns:
            bool: True if certification is required and due
        """
        if not self.certification_required:
            return False
        
        if not self.next_certification_date:
            return True
        
        return datetime.utcnow() >= self.next_certification_date
    
    def calculate_risk_score(self) -> int:
        """
        Calculate a risk score based on various factors.
        
        Returns:
            int: Risk score from 0-100
        """
        score = 50  # Base score
        
        # Account status factors
        if not self.is_active:
            score += 20
        
        if self.blocked_sign_in:
            score += 15
        
        # Activity factors
        if self.failed_sign_in_count > 5:
            score += 10
        
        if self.last_sign_in:
            days_since_login = (datetime.utcnow() - self.last_sign_in).days
            if days_since_login > 30:
                score += 15
            elif days_since_login > 90:
                score += 25
        
        # Compliance factors
        if self.compliance_status != "compliant":
            score += 20
        
        if self.needs_certification():
            score += 10
        
        # Ensure score is within bounds
        return max(0, min(100, score))
    
    def get_full_name(self) -> str:
        """
        Get the full display name for the user.
        
        Returns:
            str: Full display name
        """
        return self.display_name or self.upn
    
    def generate_privileged_upn(self, domain: str) -> str:
        """
        Generate a privileged UPN from the source user.
        
        Args:
            domain: Domain for the privileged account
            
        Returns:
            str: Generated privileged UPN
        """
        # Extract name parts from source UPN
        if "@" in self.source_user_upn:
            source_name = self.source_user_upn.split("@")[0]
        else:
            source_name = self.source_user_upn
        
        # Generate privileged UPN (assuming lastname_firstname format)
        return f"{source_name}_admin@{domain}"
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
    
    def record_sign_in(self, success: bool = True) -> None:
        """
        Record a sign-in attempt.
        
        Args:
            success: Whether the sign-in was successful
        """
        if success:
            self.last_sign_in = datetime.utcnow()
            self.sign_in_count += 1
            # Reset failed count on successful login
            self.failed_sign_in_count = 0
        else:
            self.failed_sign_in_count += 1
        
        self.update_activity()
    
    def __str__(self) -> str:
        """String representation of the user."""
        return f"PrivilegedUser({self.upn})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the user."""
        return (
            f"<User(id={self.id}, upn={self.upn}, "
            f"active={self.is_active}, source={self.source_user_upn})>"
        )


__all__ = ["User"]