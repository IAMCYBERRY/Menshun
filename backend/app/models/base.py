"""
Menshun Backend - Base Database Models.

This module provides base classes and mixins for all database models,
including common fields, methods, and behaviors shared across entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BaseModel(Base):
    """
    Abstract base model for all database entities.
    
    This class provides common functionality including:
    - UUID primary keys
    - Soft delete capability
    - Common query methods
    - Serialization support
    
    All models should inherit from this base class to ensure
    consistent behavior and maintainability.
    """
    
    __abstract__ = True
    
    # Primary key using UUID for security and distribution
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Unique identifier for the entity"
    )
    
    # Soft delete support for compliance and audit requirements
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Soft delete flag for audit compliance"
    )
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when entity was soft deleted"
    )
    
    # Metadata for extensibility
    metadata_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON metadata for extensible attributes"
    )
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        
        Converts CamelCase class names to snake_case table names.
        Example: PrivilegedUser -> privileged_users
        """
        import re
        # Convert CamelCase to snake_case and pluralize
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        
        # Add 's' for pluralization (simple approach)
        if not name.endswith('s'):
            name += 's'
        
        return name
    
    def soft_delete(self) -> None:
        """
        Perform soft delete on the entity.
        
        This method marks the entity as deleted without removing it
        from the database, maintaining audit trails and compliance.
        """
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """
        Restore a soft-deleted entity.
        
        This method reverses a soft delete operation by clearing
        the deletion flags and timestamp.
        """
        self.is_deleted = False
        self.deleted_at = None
    
    def to_dict(self, exclude_deleted: bool = True) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Args:
            exclude_deleted: Whether to exclude soft-deleted entities
            
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        if exclude_deleted and self.is_deleted:
            return {}
        
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            
            # Handle UUID serialization
            if isinstance(value, uuid.UUID):
                value = str(value)
            
            # Handle datetime serialization
            elif isinstance(value, datetime):
                value = value.isoformat()
            
            result[column.name] = value
        
        return result
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update model instance from dictionary.
        
        Args:
            data: Dictionary of attributes to update
            
        Note:
            This method only updates attributes that exist as columns
            in the database table for security.
        """
        for key, value in data.items():
            if hasattr(self, key) and key in [c.name for c in self.__table__.columns]:
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """
        String representation of the model instance.
        
        Returns:
            str: Human-readable representation
        """
        class_name = self.__class__.__name__
        return f"<{class_name}(id={self.id})>"


class TimestampMixin:
    """
    Mixin class providing created_at and updated_at timestamps.
    
    This mixin automatically manages creation and update timestamps
    for entities that need temporal tracking.
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="Timestamp when entity was created"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when entity was last updated"
    )


class AuditMixin:
    """
    Mixin class providing audit fields for tracking changes.
    
    This mixin tracks who created and last modified an entity,
    essential for compliance and security auditing.
    """
    
    created_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="User who created this entity"
    )
    
    updated_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="User who last updated this entity"
    )


class VersionMixin:
    """
    Mixin class providing optimistic locking through version control.
    
    This mixin implements version-based optimistic locking to prevent
    concurrent modification conflicts in multi-user scenarios.
    """
    
    version: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Version number for optimistic locking"
    )
    
    def increment_version(self) -> None:
        """Increment the version number."""
        self.version += 1


class ComplianceMixin:
    """
    Mixin class providing compliance-related fields.
    
    This mixin adds fields commonly required for regulatory
    compliance and audit requirements.
    """
    
    compliance_tags: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON array of compliance framework tags"
    )
    
    retention_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Date when this record can be permanently deleted"
    )
    
    classification: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Data classification level (public, internal, confidential, restricted)"
    )


# Common base class combining all mixins
class FullBaseModel(BaseModel, TimestampMixin, AuditMixin, VersionMixin, ComplianceMixin):
    """
    Complete base model with all common functionality.
    
    This class combines the base model with all available mixins,
    providing a comprehensive foundation for entities requiring
    full audit, compliance, and versioning capabilities.
    """
    
    __abstract__ = True


__all__ = [
    "BaseModel",
    "TimestampMixin", 
    "AuditMixin",
    "VersionMixin",
    "ComplianceMixin",
    "FullBaseModel",
]