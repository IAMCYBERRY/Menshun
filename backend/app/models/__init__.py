"""
Menshun Backend - Database Models.

This package contains all SQLAlchemy database models for the Menshun PAM system,
including users, service identities, credentials, audit logs, and directory roles.

Models Overview:
    - User: Privileged user accounts created from source users
    - ServiceIdentity: Service accounts, service principals, managed identities
    - Credential: Stored credentials with encryption and rotation tracking
    - DirectoryRole: Azure AD directory roles with permissions and metadata
    - AuditLog: Security and compliance audit events
    - Session: User sessions and authentication tracking
    - RoleAssignment: User-to-role mappings with time tracking
    - CredentialRotation: Credential rotation history and scheduling

Security Features:
    - Encrypted credential storage
    - Audit trails for all operations
    - Soft deletes for compliance
    - Row-level security considerations
    - Immutable audit logs

Performance Features:
    - Proper indexing for frequent queries
    - Optimized foreign key relationships
    - Efficient query patterns
    - Connection pooling support

Author: Menshun Security Team
License: MIT
"""

from app.models.audit import AuditLog
from app.models.base import BaseModel, TimestampMixin
from app.models.credential import Credential, CredentialRotation
from app.models.directory_role import DirectoryRole
from app.models.role_assignment import RoleAssignment
from app.models.service_identity import ServiceIdentity
from app.models.session import Session
from app.models.user import User

# Export all models for easy importing
__all__ = [
    "BaseModel",
    "TimestampMixin",
    "User",
    "ServiceIdentity", 
    "Credential",
    "CredentialRotation",
    "DirectoryRole",
    "RoleAssignment",
    "AuditLog",
    "Session",
]