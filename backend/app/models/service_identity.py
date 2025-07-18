"""
Menshun Backend - Service Identity Model.

This module defines the ServiceIdentity model for managing various types of
service identities including Service Accounts, Service Principals, Managed
Identities, and Workload Identities in Azure AD environments.
"""

import uuid
from datetime import datetime
from enum import Enum as PythonEnum
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Enum, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import FullBaseModel


class ServiceIdentityType(str, PythonEnum):
    """Enumeration of supported service identity types."""
    SERVICE_ACCOUNT = "service_account"
    SERVICE_PRINCIPAL = "service_principal"
    MANAGED_IDENTITY_SYSTEM = "managed_identity_system"
    MANAGED_IDENTITY_USER = "managed_identity_user"
    WORKLOAD_IDENTITY = "workload_identity"


class ServiceIdentity(FullBaseModel):
    """
    Service Identity model for Azure AD service entities.
    
    This model represents various types of service identities used for
    automated processes, applications, and workloads. It supports multiple
    identity types with specific configurations and security requirements.
    
    Supported Identity Types:
    - Service Accounts: Traditional user accounts for services
    - Service Principals: Application identities with client secrets
    - Managed Identities: Azure-managed identities for resources
    - Workload Identities: Kubernetes workload identities
    
    Security Features:
    - Identity lifecycle management
    - Credential tracking and rotation
    - Permission and role assignment
    - Comprehensive audit trails
    - Risk assessment and monitoring
    """
    
    __tablename__ = "service_identities"
    
    # =============================================================================
    # Core Identity Information
    # =============================================================================
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Display name for the service identity"
    )
    
    identity_type: Mapped[ServiceIdentityType] = mapped_column(
        Enum(*[e.value for e in ServiceIdentityType], name="service_identity_type_enum"),
        nullable=False,
        index=True,
        doc="Type of service identity"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the service identity purpose"
    )
    
    # =============================================================================
    # Azure AD Identity Information
    # =============================================================================
    
    azure_object_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        doc="Azure AD object ID for the identity"
    )
    
    client_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        doc="Application (client) ID for service principals"
    )
    
    tenant_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Azure AD tenant ID"
    )
    
    # For Service Accounts
    upn: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        doc="User Principal Name for service accounts"
    )
    
    # =============================================================================
    # Organizational and Ownership Information
    # =============================================================================
    
    department: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Department responsible for this identity"
    )
    
    owner_upn: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="UPN of the identity owner/responsible person"
    )
    
    business_contact: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Business contact for this identity"
    )
    
    technical_contact: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Technical contact for this identity"
    )
    
    cost_center: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Cost center for billing and tracking"
    )
    
    # =============================================================================
    # Environment and Classification
    # =============================================================================
    
    environment: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="production",
        index=True,
        doc="Environment (production, staging, development, test)"
    )
    
    criticality: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        doc="Business criticality (low, medium, high, critical)"
    )
    
    data_classification: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="internal",
        doc="Data classification level (public, internal, confidential, restricted)"
    )
    
    # =============================================================================
    # Status and Lifecycle Management
    # =============================================================================
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Whether the identity is active"
    )
    
    account_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether the account is enabled in Azure AD"
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
        doc="Current status (active, inactive, suspended, pending_deletion)"
    )
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Expiration date for the identity"
    )
    
    last_used: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp when identity was last used"
    )
    
    # =============================================================================
    # Application and Resource Information
    # =============================================================================
    
    application_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Name of the application using this identity"
    )
    
    application_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="URL of the application"
    )
    
    resource_group: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Azure resource group (for managed identities)"
    )
    
    subscription_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Azure subscription ID"
    )
    
    # =============================================================================
    # Kubernetes/Workload Identity Specific
    # =============================================================================
    
    kubernetes_namespace: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Kubernetes namespace for workload identities"
    )
    
    kubernetes_service_account: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Kubernetes service account name"
    )
    
    cluster_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Kubernetes cluster name"
    )
    
    oidc_issuer_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="OIDC issuer URL for workload identity federation"
    )
    
    # =============================================================================
    # Security and Risk Assessment
    # =============================================================================
    
    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        index=True,
        doc="Risk level assessment (low, medium, high, critical)"
    )
    
    risk_score: Mapped[int] = mapped_column(
        nullable=False,
        default=50,
        doc="Numeric risk score (0-100)"
    )
    
    requires_mfa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether MFA is required for this identity"
    )
    
    ip_restrictions: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of allowed IP addresses/ranges"
    )
    
    # =============================================================================
    # Credential Management
    # =============================================================================
    
    has_password: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether identity has a password (service accounts)"
    )
    
    has_client_secret: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether identity has client secrets (service principals)"
    )
    
    has_certificate: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether identity uses certificate authentication"
    )
    
    password_last_changed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when password was last changed"
    )
    
    credential_rotation_frequency_days: Mapped[int] = mapped_column(
        nullable=False,
        default=90,
        doc="Frequency for credential rotation in days"
    )
    
    next_rotation_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Next scheduled credential rotation date"
    )
    
    # =============================================================================
    # Compliance and Governance
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
    
    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether changes require approval"
    )
    
    # =============================================================================
    # Usage Analytics
    # =============================================================================
    
    usage_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Number of times identity has been used"
    )
    
    api_calls_last_30_days: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Number of API calls in the last 30 days"
    )
    
    # =============================================================================
    # Relationships
    # =============================================================================
    
    # Credentials associated with this service identity
    credentials: Mapped[List["Credential"]] = relationship(
        "Credential",
        back_populates="service_identity",
        cascade="all, delete-orphan",
        doc="Credentials associated with this service identity"
    )
    
    # Role assignments for this service identity
    role_assignments: Mapped[List["RoleAssignment"]] = relationship(
        "RoleAssignment",
        back_populates="service_identity",
        cascade="all, delete-orphan",
        doc="Directory roles assigned to this service identity"
    )
    
    # Audit logs related to this service identity
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        foreign_keys="AuditLog.target_service_identity_id",
        back_populates="target_service_identity",
        doc="Audit logs where this service identity is the target"
    )
    
    # =============================================================================
    # Database Constraints and Indexes
    # =============================================================================
    
    __table_args__ = (
        # Composite indexes for common queries
        Index(
            "ix_service_identities_type_status",
            "identity_type",
            "status"
        ),
        Index(
            "ix_service_identities_env_dept",
            "environment",
            "department"
        ),
        Index(
            "ix_service_identities_risk_level_score",
            "risk_level",
            "risk_score"
        ),
        Index(
            "ix_service_identities_rotation",
            "next_rotation_date",
            # postgresql_where="next_rotation_date IS NOT NULL AND is_active = true"  # Temporarily commented out for initial migration
        ),
        Index(
            "ix_service_identities_expiration",
            "expires_at",
            # postgresql_where="expires_at IS NOT NULL AND is_active = true"  # Temporarily commented out for initial migration
        ),
        
        # Partial indexes for active identities
        Index(
            "ix_service_identities_active_name",
            "name",
            # postgresql_where="is_active = true AND is_deleted = false"  # Temporarily commented out for initial migration
        ),
        
        # Full-text search index
        Index(
            "ix_service_identities_search",
            "name",
            "description",
            postgresql_using="gin",
            postgresql_ops={
                "name": "gin_trgm_ops",
                "description": "gin_trgm_ops"
            }
        ),
    )
    
    # =============================================================================
    # Model Methods
    # =============================================================================
    
    def is_expired(self) -> bool:
        """
        Check if the service identity has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if not self.expires_at:
            return False
        return datetime.utcnow() >= self.expires_at
    
    def needs_credential_rotation(self) -> bool:
        """
        Check if credentials need rotation.
        
        Returns:
            bool: True if rotation is needed
        """
        if not self.next_rotation_date:
            return True
        return datetime.utcnow() >= self.next_rotation_date
    
    def is_identity_healthy(self) -> bool:
        """
        Check if the identity is in a healthy state.
        
        Returns:
            bool: True if healthy, False otherwise
        """
        return (
            self.is_active and
            self.account_enabled and
            not self.is_expired() and
            not self.is_deleted and
            self.compliance_status == "compliant"
        )
    
    def calculate_risk_score(self) -> int:
        """
        Calculate risk score based on various factors.
        
        Returns:
            int: Risk score from 0-100
        """
        score = 30  # Base score
        
        # Environment factors
        env_scores = {
            "production": 20,
            "staging": 10,
            "development": 5,
            "test": 0
        }
        score += env_scores.get(self.environment, 10)
        
        # Criticality factors
        criticality_scores = {
            "critical": 25,
            "high": 20,
            "medium": 10,
            "low": 5
        }
        score += criticality_scores.get(self.criticality, 10)
        
        # Security factors
        if not self.requires_mfa:
            score += 15
        
        if self.needs_credential_rotation():
            score += 10
        
        if self.is_expired():
            score += 20
        
        # Usage factors
        if not self.last_used:
            score += 15
        elif (datetime.utcnow() - self.last_used).days > 90:
            score += 10
        
        return max(0, min(100, score))
    
    def get_identity_summary(self) -> dict:
        """
        Get a summary of the service identity.
        
        Returns:
            dict: Summary information
        """
        return {
            "name": self.name,
            "type": self.identity_type.value,
            "environment": self.environment,
            "status": self.status,
            "risk_level": self.risk_level,
            "is_healthy": self.is_identity_healthy(),
            "needs_rotation": self.needs_credential_rotation(),
            "is_expired": self.is_expired(),
        }
    
    def update_usage_stats(self, api_calls: int = 1) -> None:
        """
        Update usage statistics.
        
        Args:
            api_calls: Number of API calls to add
        """
        self.usage_count += 1
        self.api_calls_last_30_days += api_calls
        self.last_used = datetime.utcnow()
    
    def schedule_credential_rotation(self, days_from_now: Optional[int] = None) -> None:
        """
        Schedule next credential rotation.
        
        Args:
            days_from_now: Days from now to schedule rotation
        """
        if days_from_now is None:
            days_from_now = self.credential_rotation_frequency_days
        
        from datetime import timedelta
        self.next_rotation_date = datetime.utcnow() + timedelta(days=days_from_now)
    
    def __str__(self) -> str:
        """String representation of the service identity."""
        return f"ServiceIdentity({self.name})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the service identity."""
        return (
            f"<ServiceIdentity(id={self.id}, name={self.name}, "
            f"type={self.identity_type.value}, active={self.is_active})>"
        )


__all__ = ["ServiceIdentity", "ServiceIdentityType"]