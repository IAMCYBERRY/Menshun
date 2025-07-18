"""
Menshun Backend - Directory Role Model.

This module defines the DirectoryRole model for Azure AD directory roles.
It includes all 130+ Entra ID directory roles with their metadata, permissions,
and risk classifications for comprehensive role management.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class DirectoryRole(FullBaseModel):
    """
    Azure AD Directory Role model.
    
    This model represents Azure AD directory roles that can be assigned to
    privileged users. It includes comprehensive metadata about each role
    including permissions, risk level, and compliance information.
    
    The model supports all 130+ Azure AD directory roles with:
    - Role metadata and descriptions
    - Permission and scope information
    - Risk classification and scoring
    - Compliance and audit requirements
    - Assignment tracking and history
    
    Security Features:
    - Risk-based role classification
    - Permission scope validation
    - Compliance framework mapping
    - Audit trail integration
    """
    
    __tablename__ = "directory_roles"
    
    # =============================================================================
    # Core Role Identity
    # =============================================================================
    
    template_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Azure AD role template ID (immutable identifier)"
    )
    
    role_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Display name of the directory role"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the role and its purpose"
    )
    
    # =============================================================================
    # Role Classification and Categorization
    # =============================================================================
    
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Role category (Global, Security, User Management, etc.)"
    )
    
    subcategory: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Role subcategory for more granular classification"
    )
    
    is_privileged: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Whether this is considered a privileged role"
    )
    
    is_built_in: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether this is a built-in Azure AD role"
    )
    
    # =============================================================================
    # Risk Assessment and Security
    # =============================================================================
    
    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        index=True,
        doc="Risk level (low, medium, high, critical)"
    )
    
    risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=50,
        doc="Numeric risk score (0-100)"
    )
    
    requires_justification: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether assignment requires business justification"
    )
    
    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether assignment requires approval workflow"
    )
    
    max_assignment_duration_days: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Maximum assignment duration in days (for time-limited roles)"
    )
    
    # =============================================================================
    # Permissions and Scope
    # =============================================================================
    
    permissions: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of specific permissions granted by this role"
    )
    
    scope: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="directory",
        doc="Scope of the role (directory, tenant, application, etc.)"
    )
    
    can_manage_users: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether role can manage user accounts"
    )
    
    can_manage_groups: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether role can manage groups"
    )
    
    can_manage_applications: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether role can manage applications"
    )
    
    can_manage_devices: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether role can manage devices"
    )
    
    can_read_directory: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether role can read directory information"
    )
    
    can_write_directory: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether role can write directory information"
    )
    
    # =============================================================================
    # Microsoft Graph API Permissions
    # =============================================================================
    
    graph_permissions_delegated: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of delegated Graph API permissions"
    )
    
    graph_permissions_application: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of application Graph API permissions"
    )
    
    # =============================================================================
    # Compliance and Governance
    # =============================================================================
    
    compliance_frameworks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of relevant compliance frameworks (SOX, SOC2, etc.)"
    )
    
    requires_certification: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether assignments require periodic certification"
    )
    
    certification_frequency_days: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Frequency of required certification in days"
    )
    
    segregation_of_duties_conflicts: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of role IDs that conflict with this role (SoD)"
    )
    
    # =============================================================================
    # Usage and Analytics
    # =============================================================================
    
    assignment_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Current number of users assigned to this role"
    )
    
    total_assignments: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Total number of assignments (including historical)"
    )
    
    last_assigned: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        doc="Timestamp when role was last assigned to a user"
    )
    
    average_assignment_duration_days: Mapped[Optional[float]] = mapped_column(
        nullable=True,
        doc="Average duration of role assignments in days"
    )
    
    # =============================================================================
    # Azure AD Metadata
    # =============================================================================
    
    azure_role_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Azure AD role definition ID (for custom roles)"
    )
    
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Whether the role is enabled for assignment"
    )
    
    role_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="1.0",
        doc="Version of the role definition"
    )
    
    # =============================================================================
    # Documentation and Training
    # =============================================================================
    
    documentation_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="URL to official Microsoft documentation for this role"
    )
    
    training_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether training is required before assignment"
    )
    
    training_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="URL to required training materials"
    )
    
    # =============================================================================
    # Relationships
    # =============================================================================
    
    # Role assignments using this role
    role_assignments: Mapped[List["RoleAssignment"]] = relationship(
        "RoleAssignment",
        back_populates="directory_role",
        doc="Users assigned to this directory role"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Ensure template_id uniqueness
        UniqueConstraint(
            "template_id",
            name="uq_directory_roles_template_id"
        ),
        
        # Basic composite indexes for common queries
        Index(
            "ix_directory_roles_category_privileged",
            "category",
            "is_privileged"
        ),
        Index(
            "ix_directory_roles_risk_level_score",
            "risk_level",
            "risk_score"
        ),
        Index(
            "ix_directory_roles_enabled_category",
            "is_enabled",
            "category"
        ),
        Index(
            "ix_directory_roles_assignment_count",
            "assignment_count"
        ),
        # Note: Advanced indexes (GIN, full-text search)
        # will be added in separate migrations after basic table structure
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_high_risk(self) -> bool:
        """
        Check if this is a high-risk role.
        
        Returns:
            bool: True if role is high or critical risk
        """
        return self.risk_level in ["high", "critical"]
    
    def requires_enhanced_monitoring(self) -> bool:
        """
        Check if role requires enhanced monitoring.
        
        Returns:
            bool: True if enhanced monitoring is required
        """
        return (
            self.is_privileged or
            self.is_high_risk() or
            self.requires_approval or
            self.risk_score >= 75
        )
    
    def get_permission_summary(self) -> dict:
        """
        Get a summary of role permissions.
        
        Returns:
            dict: Summary of role permissions
        """
        return {
            "can_manage_users": self.can_manage_users,
            "can_manage_groups": self.can_manage_groups,
            "can_manage_applications": self.can_manage_applications,
            "can_manage_devices": self.can_manage_devices,
            "can_read_directory": self.can_read_directory,
            "can_write_directory": self.can_write_directory,
        }
    
    def calculate_assignment_risk(self, user_risk_score: int) -> int:
        """
        Calculate risk of assigning this role to a user.
        
        Args:
            user_risk_score: Risk score of the user (0-100)
            
        Returns:
            int: Combined risk score for the assignment
        """
        # Weight role risk more heavily
        combined_risk = (self.risk_score * 0.7) + (user_risk_score * 0.3)
        
        # Add penalty for high-risk combinations
        if self.risk_score >= 80 and user_risk_score >= 60:
            combined_risk += 10
        
        return min(100, int(combined_risk))
    
    def get_conflicting_roles(self) -> List[str]:
        """
        Get list of role template IDs that conflict with this role.
        
        Returns:
            List[str]: List of conflicting role template IDs
        """
        import json
        
        if not self.segregation_of_duties_conflicts:
            return []
        
        try:
            return json.loads(self.segregation_of_duties_conflicts)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def increment_assignment_count(self) -> None:
        """Increment the assignment counters."""
        self.assignment_count += 1
        self.total_assignments += 1
        self.last_assigned = datetime.utcnow()
    
    def decrement_assignment_count(self) -> None:
        """Decrement the assignment counter."""
        if self.assignment_count > 0:
            self.assignment_count -= 1
    
    def update_assignment_stats(self, assignment_duration_days: Optional[float] = None) -> None:
        """
        Update assignment statistics.
        
        Args:
            assignment_duration_days: Duration of completed assignment
        """
        if assignment_duration_days is not None:
            if self.average_assignment_duration_days is None:
                self.average_assignment_duration_days = assignment_duration_days
            else:
                # Running average calculation
                total_duration = (self.average_assignment_duration_days * 
                                (self.total_assignments - 1)) + assignment_duration_days
                self.average_assignment_duration_days = total_duration / self.total_assignments
    
    def __str__(self) -> str:
        """String representation of the role."""
        return f"DirectoryRole({self.role_name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the role."""
        return (
            f"<DirectoryRole(id={self.id}, template_id={self.template_id}, "
            f"name={self.role_name}, risk={self.risk_level})>"
        )


__all__ = ["DirectoryRole"]