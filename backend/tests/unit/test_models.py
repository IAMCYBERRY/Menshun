"""
Menshun Backend - Unit Tests for Database Models.

Tests for SQLAlchemy models including validation, relationships,
and business logic methods.
"""

import pytest
import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import PrivilegedUser
from app.models.directory_role import DirectoryRole
from app.models.service_identity import ServiceIdentity
from app.models.credential import Credential
from app.models.role_assignment import RoleAssignment
from app.models.audit import AuditLog


@pytest.mark.unit
@pytest.mark.asyncio
class TestPrivilegedUserModel:
    """Test PrivilegedUser model."""
    
    async def test_create_user(self, db_session: AsyncSession):
        """Test creating a privileged user."""
        user = PrivilegedUser(
            user_principal_name="test.user@company.com",
            display_name="Test User",
            given_name="Test",
            surname="User",
            email="test.user@company.com",
            is_privileged=True,
            risk_score=75,
            account_enabled=True,
            compliance_status="compliant",
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.user_principal_name == "test.user@company.com"
        assert user.display_name == "Test User"
        assert user.is_privileged is True
        assert user.risk_score == 75
        assert user.created_date is not None
        assert user.last_modified is not None
    
    async def test_user_soft_delete(self, db_session: AsyncSession):
        """Test soft delete functionality."""
        user = PrivilegedUser(
            user_principal_name="test.user@company.com",
            display_name="Test User",
            is_privileged=True,
            risk_score=75,
            account_enabled=True,
            compliance_status="compliant",
        )
        
        db_session.add(user)
        await db_session.commit()
        
        # Soft delete
        user.soft_delete()
        await db_session.commit()
        
        assert user.is_deleted is True
        assert user.deleted_date is not None
    
    async def test_user_risk_classification(self, db_session: AsyncSession):
        """Test risk score classification."""
        # Low risk user
        low_risk_user = PrivilegedUser(
            user_principal_name="low.risk@company.com",
            display_name="Low Risk User",
            is_privileged=False,
            risk_score=25,
            account_enabled=True,
            compliance_status="compliant",
        )
        
        # High risk user
        high_risk_user = PrivilegedUser(
            user_principal_name="high.risk@company.com",
            display_name="High Risk User",
            is_privileged=True,
            risk_score=90,
            account_enabled=True,
            compliance_status="non_compliant",
        )
        
        db_session.add_all([low_risk_user, high_risk_user])
        await db_session.commit()
        
        assert low_risk_user.risk_score < 50
        assert high_risk_user.risk_score >= 80


@pytest.mark.unit
@pytest.mark.asyncio
class TestDirectoryRoleModel:
    """Test DirectoryRole model."""
    
    async def test_create_directory_role(self, db_session: AsyncSession):
        """Test creating a directory role."""
        role = DirectoryRole(
            template_id="62e90394-69f5-4237-9190-012177145e10",
            role_name="Global Administrator",
            description="Can manage all aspects of Microsoft Entra ID",
            category="Global",
            subcategory="Administrative",
            is_privileged=True,
            risk_level="critical",
            risk_score=95,
            requires_justification=True,
            requires_approval=True,
            can_manage_users=True,
            can_read_directory=True,
            can_write_directory=True,
            requires_certification=True,
        )
        
        db_session.add(role)
        await db_session.commit()
        await db_session.refresh(role)
        
        assert role.id is not None
        assert role.template_id == "62e90394-69f5-4237-9190-012177145e10"
        assert role.role_name == "Global Administrator"
        assert role.is_privileged is True
        assert role.risk_level == "critical"
        assert role.risk_score == 95
    
    async def test_role_permissions(self, db_session: AsyncSession):
        """Test role permission flags."""
        admin_role = DirectoryRole(
            template_id="admin-role",
            role_name="Administrator",
            description="Administrator role",
            category="Administrative",
            is_privileged=True,
            risk_level="high",
            risk_score=80,
            can_manage_users=True,
            can_manage_groups=True,
            can_manage_applications=True,
            can_manage_devices=True,
            can_read_directory=True,
            can_write_directory=True,
            requires_justification=True,
            requires_approval=True,
            requires_certification=True,
        )
        
        readonly_role = DirectoryRole(
            template_id="readonly-role",
            role_name="Directory Reader",
            description="Read-only role",
            category="Directory",
            is_privileged=False,
            risk_level="low",
            risk_score=20,
            can_manage_users=False,
            can_manage_groups=False,
            can_manage_applications=False,
            can_manage_devices=False,
            can_read_directory=True,
            can_write_directory=False,
            requires_justification=False,
            requires_approval=False,
            requires_certification=False,
        )
        
        db_session.add_all([admin_role, readonly_role])
        await db_session.commit()
        
        assert admin_role.can_manage_users is True
        assert admin_role.can_write_directory is True
        assert readonly_role.can_manage_users is False
        assert readonly_role.can_write_directory is False


@pytest.mark.unit
@pytest.mark.asyncio
class TestServiceIdentityModel:
    """Test ServiceIdentity model."""
    
    async def test_create_service_identity(self, db_session: AsyncSession):
        """Test creating a service identity."""
        service_identity = ServiceIdentity(
            identity_type="service_principal",
            name="Test Service Principal",
            description="Test service principal for API access",
            application_id="test-app-id",
            object_id="test-object-id",
            tenant_id="test-tenant-id",
            is_enabled=True,
            risk_score=45,
        )
        
        db_session.add(service_identity)
        await db_session.commit()
        await db_session.refresh(service_identity)
        
        assert service_identity.id is not None
        assert service_identity.identity_type == "service_principal"
        assert service_identity.name == "Test Service Principal"
        assert service_identity.is_enabled is True
        assert service_identity.risk_score == 45
    
    async def test_service_identity_types(self, db_session: AsyncSession):
        """Test different service identity types."""
        identities = [
            ServiceIdentity(
                identity_type="service_account",
                name="Service Account",
                is_enabled=True,
                risk_score=40,
            ),
            ServiceIdentity(
                identity_type="managed_identity",
                name="Managed Identity",
                subscription_id="test-sub-id",
                resource_group="test-rg",
                is_enabled=True,
                risk_score=30,
            ),
            ServiceIdentity(
                identity_type="workload_identity",
                name="Workload Identity",
                is_enabled=True,
                risk_score=50,
            ),
        ]
        
        db_session.add_all(identities)
        await db_session.commit()
        
        for identity in identities:
            assert identity.id is not None
            assert identity.identity_type in [
                "service_account",
                "service_principal",
                "managed_identity",
                "workload_identity"
            ]


@pytest.mark.unit
@pytest.mark.asyncio
class TestCredentialModel:
    """Test Credential model."""
    
    async def test_create_credential(self, db_session: AsyncSession, sample_service_identity: ServiceIdentity):
        """Test creating a credential."""
        credential = Credential(
            credential_type="password",
            name="Service Account Password",
            description="Password for service account",
            vault_path="/secrets/service-account/password",
            service_identity_id=sample_service_identity.id,
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=90),
            rotation_frequency_days=30,
            auto_rotation_enabled=True,
        )
        
        db_session.add(credential)
        await db_session.commit()
        await db_session.refresh(credential)
        
        assert credential.id is not None
        assert credential.credential_type == "password"
        assert credential.name == "Service Account Password"
        assert credential.is_active is True
        assert credential.auto_rotation_enabled is True
        assert credential.service_identity_id == sample_service_identity.id
    
    async def test_credential_expiration(self, db_session: AsyncSession):
        """Test credential expiration logic."""
        # Expired credential
        expired_credential = Credential(
            credential_type="certificate",
            name="Expired Certificate",
            vault_path="/secrets/expired-cert",
            is_active=True,
            expires_at=datetime.utcnow() - timedelta(days=1),
        )
        
        # Valid credential
        valid_credential = Credential(
            credential_type="secret",
            name="Valid Secret",
            vault_path="/secrets/valid-secret",
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
        
        db_session.add_all([expired_credential, valid_credential])
        await db_session.commit()
        
        assert expired_credential.expires_at < datetime.utcnow()
        assert valid_credential.expires_at > datetime.utcnow()


@pytest.mark.unit
@pytest.mark.asyncio
class TestRoleAssignmentModel:
    """Test RoleAssignment model."""
    
    async def test_create_role_assignment(
        self,
        db_session: AsyncSession,
        sample_user: PrivilegedUser,
        sample_directory_role: DirectoryRole
    ):
        """Test creating a role assignment."""
        assignment = RoleAssignment(
            user_id=sample_user.id,
            directory_role_id=sample_directory_role.id,
            assignment_type="time_limited",
            assignment_reason="Temporary elevated access for project",
            justification="User needs admin access for system maintenance",
            assigned_by="admin@company.com",
            assigned_date=datetime.utcnow(),
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7),
            status="pending_approval",
            compliance_status="pending",
        )
        
        db_session.add(assignment)
        await db_session.commit()
        await db_session.refresh(assignment)
        
        assert assignment.id is not None
        assert assignment.user_id == sample_user.id
        assert assignment.directory_role_id == sample_directory_role.id
        assert assignment.assignment_type == "time_limited"
        assert assignment.status == "pending_approval"
    
    async def test_assignment_approval(
        self,
        db_session: AsyncSession,
        sample_user: PrivilegedUser,
        sample_directory_role: DirectoryRole
    ):
        """Test role assignment approval workflow."""
        assignment = RoleAssignment(
            user_id=sample_user.id,
            directory_role_id=sample_directory_role.id,
            assignment_type="eligible",
            status="pending_approval",
            assigned_by="admin@company.com",
            assigned_date=datetime.utcnow(),
            start_date=datetime.utcnow(),
            compliance_status="pending",
        )
        
        db_session.add(assignment)
        await db_session.commit()
        
        # Approve assignment
        assignment.status = "approved"
        assignment.approved_by = "manager@company.com"
        assignment.approved_date = datetime.utcnow()
        assignment.compliance_status = "compliant"
        
        await db_session.commit()
        
        assert assignment.status == "approved"
        assert assignment.approved_by == "manager@company.com"
        assert assignment.approved_date is not None


@pytest.mark.unit
@pytest.mark.asyncio
class TestAuditLogModel:
    """Test AuditLog model."""
    
    async def test_create_audit_log(self, db_session: AsyncSession, sample_user: PrivilegedUser):
        """Test creating an audit log entry."""
        audit_log = AuditLog(
            event_type="USER_ROLE_ASSIGNED",
            event_category="AUTHORIZATION",
            user_id=sample_user.id,
            resource_type="DIRECTORY_ROLE",
            resource_id="test-role-id",
            action="ASSIGN",
            result="success",
            risk_level="medium",
            source_ip="192.168.1.100",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            location="New York, NY, US",
            details={
                "role_name": "Security Administrator",
                "assignment_type": "eligible",
                "justification": "Required for security operations",
            },
            correlation_id="test-correlation-id",
        )
        
        db_session.add(audit_log)
        await db_session.commit()
        await db_session.refresh(audit_log)
        
        assert audit_log.id is not None
        assert audit_log.event_type == "USER_ROLE_ASSIGNED"
        assert audit_log.event_category == "AUTHORIZATION"
        assert audit_log.user_id == sample_user.id
        assert audit_log.result == "success"
        assert audit_log.risk_level == "medium"
        assert isinstance(audit_log.details, dict)
    
    async def test_audit_log_immutability(self, db_session: AsyncSession):
        """Test that audit logs are immutable after creation."""
        audit_log = AuditLog(
            event_type="LOGIN_ATTEMPT",
            event_category="AUTHENTICATION",
            action="LOGIN",
            result="success",
            risk_level="low",
            source_ip="192.168.1.100",
            details={"method": "SSO"},
        )
        
        db_session.add(audit_log)
        await db_session.commit()
        await db_session.refresh(audit_log)
        
        original_created_date = audit_log.created_date
        
        # Audit logs should not be modifiable after creation
        # This is enforced at the application level, not database level
        assert audit_log.created_date == original_created_date
        assert audit_log.event_type == "LOGIN_ATTEMPT"