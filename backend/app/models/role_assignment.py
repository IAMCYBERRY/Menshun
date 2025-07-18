"""
Menshun Backend - Role Assignment Model.

This module defines the RoleAssignment model for tracking directory role
assignments to users and service identities with comprehensive audit trails
and time-limited assignment support.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Index, String, Text, 
    UniqueConstraint, event
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class RoleAssignment(FullBaseModel):
    """
    Directory Role Assignment model.
    
    This model tracks the assignment of Azure AD directory roles to users
    and service identities, providing comprehensive audit trails, time-limited
    assignments, and assignment lifecycle management.
    
    Key Features:
    - Support for both user and service identity assignments
    - Time-limited assignments with automatic expiration
    - Comprehensive audit trail for compliance
    - Assignment justification and approval workflow
    - Risk assessment for assignment combinations
    - Automatic cleanup of expired assignments
    """
    
    __tablename__ = "role_assignments"
    
    # =============================================================================
    # Core Assignment Information
    # =============================================================================
    
    directory_role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("directory_roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Directory role being assigned"
    )
    
    directory_role: Mapped["DirectoryRole"] = relationship(
        "DirectoryRole",
        back_populates="role_assignments",
        doc="Directory role being assigned"
    )
    
    # =============================================================================
    # Assignment Target (User or Service Identity)
    # =============================================================================
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("privileged_users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="User receiving the role assignment"
    )
    
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="role_assignments",
        doc="User receiving the role assignment"
    )
    
    service_identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_identities.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="Service identity receiving the role assignment"
    )
    
    service_identity: Mapped[Optional["ServiceIdentity"]] = relationship(
        "ServiceIdentity",
        back_populates="role_assignments",
        doc="Service identity receiving the role assignment"
    )
    
    # =============================================================================
    # Assignment Lifecycle
    # =============================================================================
    
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        index=True,
        doc="Timestamp when role was assigned"
    )
    
    assigned_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="UPN of user who made the assignment"
    )
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp when assignment expires (for time-limited roles)"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Whether the assignment is currently active"
    )
    
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when assignment was revoked"
    )
    
    revoked_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="UPN of user who revoked the assignment"
    )
    
    # =============================================================================
    # Justification and Approval
    # =============================================================================
    
    justification: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Business justification for the role assignment"
    )
    
    ticket_number: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Service desk ticket number for the assignment"
    )
    
    approval_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether assignment required approval"
    )
    
    approved_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="UPN of user who approved the assignment"
    )
    
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when assignment was approved"
    )
    
    # =============================================================================
    # Azure AD Integration
    # =============================================================================
    
    azure_assignment_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        doc="Azure AD assignment ID for synchronization"
    )
    
    sync_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        doc="Synchronization status with Azure AD (pending, synced, failed)"
    )
    
    last_sync_attempt: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of last sync attempt with Azure AD"
    )
    
    sync_error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Error message from last sync attempt"
    )
    
    # =============================================================================
    # Risk and Compliance
    # =============================================================================
    
    risk_score: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Risk score for this specific assignment (0-100)"
    )
    
    risk_assessment_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Date when risk was last assessed"
    )
    
    requires_certification: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether assignment requires periodic certification"
    )
    
    last_certified: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Date when assignment was last certified"
    )
    
    certified_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="UPN of user who certified the assignment"
    )
    
    next_certification_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Date when next certification is due"
    )
    
    # =============================================================================
    # Emergency and Break-Glass
    # =============================================================================
    
    is_emergency: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether this was an emergency/break-glass assignment"
    )
    
    emergency_justification: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Justification for emergency assignment"
    )
    
    emergency_approver: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Emergency approver for break-glass assignment"
    )
    
    auto_revoke_hours: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="Hours after which emergency assignment auto-revokes"
    )
    
    # =============================================================================
    # Assignment Source and Context
    # =============================================================================
    
    assignment_source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="manual",
        doc="Source of assignment (manual, automated, imported, emergency)"
    )
    
    source_system: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="External system that created this assignment"
    )
    
    assignment_context: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Additional context about the assignment"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Ensure either user_id or service_identity_id is set, but not both
        # This would be implemented as a check constraint in PostgreSQL
        
        # Unique constraint to prevent duplicate active assignments
        UniqueConstraint(
            "directory_role_id",
            "user_id",
            "service_identity_id",
            name="uq_role_assignments_unique_active"
        ),
        
        # Basic composite indexes for common queries
        Index(
            "ix_role_assignments_user_active",
            "user_id",
            "is_active",
            "expires_at"
        ),
        Index(
            "ix_role_assignments_service_active",
            "service_identity_id", 
            "is_active",
            "expires_at"
        ),
        Index(
            "ix_role_assignments_role_active",
            "directory_role_id",
            "is_active"
        ),
        Index(
            "ix_role_assignments_expiry",
            "expires_at"
        ),
        Index(
            "ix_role_assignments_certification",
            "next_certification_date"
        ),
        Index(
            "ix_role_assignments_emergency",
            "is_emergency",
            "assigned_at"
        ),
        Index(
            "ix_role_assignments_sync_status",
            "sync_status",
            "last_sync_attempt"
        ),
        # Note: Partial indexes with WHERE clauses
        # will be added in separate migrations after basic table structure
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_expired(self) -> bool:
        """
        Check if the assignment has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if not self.expires_at:
            return False
        return datetime.utcnow() >= self.expires_at
    
    def needs_certification(self) -> bool:
        """
        Check if assignment needs certification.
        
        Returns:
            bool: True if certification is required and due
        """
        if not self.requires_certification or not self.is_active:
            return False
        
        if not self.next_certification_date:
            return True
        
        return datetime.utcnow() >= self.next_certification_date
    
    def days_until_expiry(self) -> Optional[int]:
        """
        Calculate days until assignment expires.
        
        Returns:
            Optional[int]: Days until expiry, None if no expiry
        """
        if not self.expires_at:
            return None
        
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)
    
    def get_assignee_name(self) -> str:
        """
        Get the name of the assignment target.
        
        Returns:
            str: Name of user or service identity
        """
        if self.user:
            return self.user.display_name or self.user.upn
        elif self.service_identity:
            return self.service_identity.name
        else:
            return "Unknown"
    
    def get_assignee_type(self) -> str:
        """
        Get the type of assignment target.
        
        Returns:
            str: "user" or "service_identity"
        """
        if self.user_id:
            return "user"
        elif self.service_identity_id:
            return "service_identity"
        else:
            return "unknown"
    
    def calculate_assignment_duration(self) -> Optional[timedelta]:
        """
        Calculate how long the assignment has been active.
        
        Returns:
            Optional[timedelta]: Duration of assignment
        """
        end_time = self.revoked_at or datetime.utcnow()
        return end_time - self.assigned_at
    
    def revoke(self, revoked_by: str, reason: Optional[str] = None) -> None:
        """
        Revoke the role assignment.
        
        Args:
            revoked_by: UPN of user revoking the assignment
            reason: Optional reason for revocation
        """
        self.is_active = False
        self.revoked_at = datetime.utcnow()
        self.revoked_by = revoked_by
        
        if reason:
            if self.assignment_context:
                self.assignment_context += f"\nRevocation reason: {reason}"
            else:
                self.assignment_context = f"Revocation reason: {reason}"
    
    def certify(self, certified_by: str, next_cert_days: int = 90) -> None:
        """
        Certify the role assignment.
        
        Args:
            certified_by: UPN of user certifying the assignment
            next_cert_days: Days until next certification is due
        """
        self.last_certified = datetime.utcnow()
        self.certified_by = certified_by
        self.next_certification_date = datetime.utcnow() + timedelta(days=next_cert_days)
    
    def extend_assignment(self, days: int, extended_by: str) -> None:
        """
        Extend the assignment duration.
        
        Args:
            days: Number of days to extend
            extended_by: UPN of user extending the assignment
        """
        if self.expires_at:
            self.expires_at += timedelta(days=days)
        else:
            self.expires_at = datetime.utcnow() + timedelta(days=days)
        
        # Log the extension
        context = f"Assignment extended by {days} days by {extended_by}"
        if self.assignment_context:
            self.assignment_context += f"\n{context}"
        else:
            self.assignment_context = context
    
    def get_assignment_summary(self) -> dict:
        """
        Get a summary of the assignment.
        
        Returns:
            dict: Assignment summary
        """
        return {
            "id": str(self.id),
            "role_name": self.directory_role.role_name if self.directory_role else "Unknown",
            "assignee_name": self.get_assignee_name(),
            "assignee_type": self.get_assignee_type(),
            "assigned_at": self.assigned_at.isoformat(),
            "assigned_by": self.assigned_by,
            "is_active": self.is_active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired(),
            "needs_certification": self.needs_certification(),
            "is_emergency": self.is_emergency,
            "risk_score": self.risk_score,
        }
    
    def __str__(self) -> str:
        """String representation of the assignment."""
        role_name = self.directory_role.role_name if self.directory_role else "Unknown Role"
        assignee_name = self.get_assignee_name()
        return f"RoleAssignment({role_name} -> {assignee_name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the assignment."""
        return (
            f"<RoleAssignment(id={self.id}, role_id={self.directory_role_id}, "
            f"user_id={self.user_id}, service_id={self.service_identity_id}, "
            f"active={self.is_active})>"
        )


# SQLAlchemy event listeners for business logic
@event.listens_for(RoleAssignment, "before_insert")
def validate_assignment_target(mapper, connection, target):
    """Ensure exactly one of user_id or service_identity_id is set."""
    if not target.user_id and not target.service_identity_id:
        raise ValueError("Assignment must target either a user or service identity")
    
    if target.user_id and target.service_identity_id:
        raise ValueError("Assignment cannot target both user and service identity")


@event.listens_for(RoleAssignment, "after_insert")
def update_role_assignment_count(mapper, connection, target):
    """Update assignment count on the directory role."""
    # This would increment the assignment_count on the DirectoryRole
    # Implementation depends on whether we're in a transaction context
    pass


@event.listens_for(RoleAssignment, "after_update")
def handle_assignment_deactivation(mapper, connection, target):
    """Handle cleanup when assignment is deactivated."""
    # If assignment was deactivated, decrement the role assignment count
    if hasattr(target, '_sa_instance_state'):
        history = target._sa_instance_state.get_history('is_active', True)
        if history.has_changes() and not target.is_active:
            # Decrement assignment count
            pass


__all__ = ["RoleAssignment"]