"""Initial database schema with all core tables

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade the database schema.
    
    Creates all core tables for the Menshun PAM system including:
    - privileged_users: Privileged user accounts
    - directory_roles: Azure AD directory roles
    - service_identities: Service accounts and identities
    - credentials: Encrypted credential storage
    - role_assignments: Role assignment tracking
    - audit_logs: Comprehensive audit trails
    - sessions: User session management
    - credential_rotations: Credential rotation history
    """
    
    # =============================================================================
    # Directory Roles Table
    # =============================================================================
    op.create_table(
        'directory_roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('template_id', sa.String(length=255), nullable=False),
        sa.Column('role_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('subcategory', sa.String(length=100), nullable=True),
        sa.Column('is_privileged', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_built_in', sa.Boolean(), nullable=False, default=True),
        sa.Column('risk_level', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('risk_score', sa.Integer(), nullable=False, default=50),
        sa.Column('requires_justification', sa.Boolean(), nullable=False, default=False),
        sa.Column('requires_approval', sa.Boolean(), nullable=False, default=False),
        sa.Column('max_assignment_duration_days', sa.Integer(), nullable=True),
        sa.Column('permissions', sa.Text(), nullable=True),
        sa.Column('scope', sa.String(length=50), nullable=False, default='directory'),
        sa.Column('can_manage_users', sa.Boolean(), nullable=False, default=False),
        sa.Column('can_manage_groups', sa.Boolean(), nullable=False, default=False),
        sa.Column('can_manage_applications', sa.Boolean(), nullable=False, default=False),
        sa.Column('can_manage_devices', sa.Boolean(), nullable=False, default=False),
        sa.Column('can_read_directory', sa.Boolean(), nullable=False, default=True),
        sa.Column('can_write_directory', sa.Boolean(), nullable=False, default=False),
        sa.Column('graph_permissions_delegated', sa.Text(), nullable=True),
        sa.Column('graph_permissions_application', sa.Text(), nullable=True),
        sa.Column('compliance_frameworks', sa.Text(), nullable=True),
        sa.Column('requires_certification', sa.Boolean(), nullable=False, default=False),
        sa.Column('certification_frequency_days', sa.Integer(), nullable=True),
        sa.Column('segregation_of_duties_conflicts', sa.Text(), nullable=True),
        sa.Column('assignment_count', sa.Integer(), nullable=False, default=0),
        sa.Column('total_assignments', sa.Integer(), nullable=False, default=0),
        sa.Column('last_assigned', sa.DateTime(timezone=True), nullable=True),
        sa.Column('average_assignment_duration_days', sa.Float(), nullable=True),
        sa.Column('azure_role_id', sa.String(length=255), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('role_version', sa.String(length=50), nullable=False, default='1.0'),
        sa.Column('documentation_url', sa.String(length=500), nullable=True),
        sa.Column('training_required', sa.Boolean(), nullable=False, default=False),
        sa.Column('training_url', sa.String(length=500), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('template_id', name='uq_directory_roles_template_id')
    )
    
    # =============================================================================
    # Privileged Users Table
    # =============================================================================
    op.create_table(
        'privileged_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('upn', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('source_user_id', sa.String(length=255), nullable=False),
        sa.Column('source_user_upn', sa.String(length=255), nullable=False),
        sa.Column('source_user_email', sa.String(length=255), nullable=True),
        sa.Column('employee_type', sa.String(length=50), nullable=False, default='Admin'),
        sa.Column('department', sa.String(length=255), nullable=True),
        sa.Column('job_title', sa.String(length=255), nullable=True),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('office_location', sa.String(length=255), nullable=True),
        sa.Column('manager_upn', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('account_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('blocked_sign_in', sa.Boolean(), nullable=False, default=False),
        sa.Column('azure_object_id', sa.String(length=255), nullable=True),
        sa.Column('password_profile', sa.Text(), nullable=True),
        sa.Column('force_change_password', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_tap_generated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tap_count', sa.Integer(), nullable=False, default=0),
        sa.Column('usage_location', sa.String(length=2), nullable=True),
        sa.Column('preferred_language', sa.String(length=10), nullable=True),
        sa.Column('last_sign_in', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sign_in_count', sa.Integer(), nullable=False, default=0),
        sa.Column('failed_sign_in_count', sa.Integer(), nullable=False, default=0),
        sa.Column('risk_level', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('last_risk_assessment', sa.DateTime(timezone=True), nullable=True),
        sa.Column('compliance_status', sa.String(length=50), nullable=False, default='compliant'),
        sa.Column('last_compliance_check', sa.DateTime(timezone=True), nullable=True),
        sa.Column('certification_required', sa.Boolean(), nullable=False, default=False),
        sa.Column('next_certification_date', sa.DateTime(timezone=True), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('upn', name='uq_privileged_users_upn'),
        sa.UniqueConstraint('azure_object_id', name='uq_privileged_users_azure_object_id'),
        sa.UniqueConstraint('source_user_id', name='uq_privileged_users_source_user_id')
    )
    
    # =============================================================================
    # Service Identities Table
    # =============================================================================
    op.create_table(
        'service_identities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('identity_type', sa.Enum('SERVICE_ACCOUNT', 'SERVICE_PRINCIPAL', 'MANAGED_IDENTITY_SYSTEM', 'MANAGED_IDENTITY_USER', 'WORKLOAD_IDENTITY', name='serviceidentitytype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('azure_object_id', sa.String(length=255), nullable=True),
        sa.Column('client_id', sa.String(length=255), nullable=True),
        sa.Column('tenant_id', sa.String(length=255), nullable=True),
        sa.Column('upn', sa.String(length=255), nullable=True),
        sa.Column('department', sa.String(length=255), nullable=True),
        sa.Column('owner_upn', sa.String(length=255), nullable=True),
        sa.Column('business_contact', sa.String(length=255), nullable=True),
        sa.Column('technical_contact', sa.String(length=255), nullable=True),
        sa.Column('cost_center', sa.String(length=100), nullable=True),
        sa.Column('environment', sa.String(length=50), nullable=False, default='production'),
        sa.Column('criticality', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('data_classification', sa.String(length=50), nullable=False, default='internal'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('account_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('status', sa.String(length=50), nullable=False, default='active'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
        sa.Column('application_name', sa.String(length=255), nullable=True),
        sa.Column('application_url', sa.String(length=500), nullable=True),
        sa.Column('resource_group', sa.String(length=255), nullable=True),
        sa.Column('subscription_id', sa.String(length=255), nullable=True),
        sa.Column('kubernetes_namespace', sa.String(length=255), nullable=True),
        sa.Column('kubernetes_service_account', sa.String(length=255), nullable=True),
        sa.Column('cluster_name', sa.String(length=255), nullable=True),
        sa.Column('oidc_issuer_url', sa.String(length=500), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('risk_score', sa.Integer(), nullable=False, default=50),
        sa.Column('requires_mfa', sa.Boolean(), nullable=False, default=False),
        sa.Column('ip_restrictions', sa.Text(), nullable=True),
        sa.Column('has_password', sa.Boolean(), nullable=False, default=False),
        sa.Column('has_client_secret', sa.Boolean(), nullable=False, default=False),
        sa.Column('has_certificate', sa.Boolean(), nullable=False, default=False),
        sa.Column('password_last_changed', sa.DateTime(timezone=True), nullable=True),
        sa.Column('credential_rotation_frequency_days', sa.Integer(), nullable=False, default=90),
        sa.Column('next_rotation_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('compliance_status', sa.String(length=50), nullable=False, default='compliant'),
        sa.Column('last_compliance_check', sa.DateTime(timezone=True), nullable=True),
        sa.Column('requires_approval', sa.Boolean(), nullable=False, default=False),
        sa.Column('usage_count', sa.Integer(), nullable=False, default=0),
        sa.Column('api_calls_last_30_days', sa.Integer(), nullable=False, default=0),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('azure_object_id', name='uq_service_identities_azure_object_id'),
        sa.UniqueConstraint('client_id', name='uq_service_identities_client_id'),
        sa.UniqueConstraint('upn', name='uq_service_identities_upn')
    )
    
    # =============================================================================
    # Credentials Table
    # =============================================================================
    op.create_table(
        'credentials',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('service_identity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('credential_type', sa.Enum('PASSWORD', 'CLIENT_SECRET', 'CERTIFICATE', 'API_KEY', 'TOKEN', 'SSH_KEY', name='credentialtype'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('vault_path', sa.String(length=500), nullable=False),
        sa.Column('vault_version', sa.String(length=50), nullable=True),
        sa.Column('encrypted_metadata', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'EXPIRED', 'ROTATED', 'REVOKED', 'PENDING_ROTATION', name='credentialstatus'), nullable=False, default='ACTIVE'),
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
        sa.Column('use_count', sa.Integer(), nullable=False, default=0),
        sa.Column('rotation_frequency_days', sa.Integer(), nullable=False, default=90),
        sa.Column('next_rotation_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_rotated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('rotation_count', sa.Integer(), nullable=False, default=0),
        sa.Column('auto_rotation_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('strength_score', sa.Integer(), nullable=True),
        sa.Column('complexity_requirements', sa.Text(), nullable=True),
        sa.Column('requires_encryption', sa.Boolean(), nullable=False, default=True),
        sa.Column('access_restrictions', sa.Text(), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('external_system', sa.String(length=100), nullable=True),
        sa.Column('sync_enabled', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_sync', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notification_days_before_expiry', sa.Integer(), nullable=False, default=14),
        sa.Column('notification_sent', sa.Boolean(), nullable=False, default=False),
        sa.Column('emergency_contact', sa.String(length=255), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['service_identity_id'], ['service_identities.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('vault_path', name='uq_credentials_vault_path')
    )
    
    # =============================================================================
    # Role Assignments Table
    # =============================================================================
    op.create_table(
        'role_assignments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('directory_role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('service_identity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('assigned_by', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('revoked_by', sa.String(length=255), nullable=True),
        sa.Column('justification', sa.Text(), nullable=True),
        sa.Column('ticket_number', sa.String(length=100), nullable=True),
        sa.Column('approval_required', sa.Boolean(), nullable=False, default=False),
        sa.Column('approved_by', sa.String(length=255), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('azure_assignment_id', sa.String(length=255), nullable=True),
        sa.Column('sync_status', sa.String(length=50), nullable=False, default='pending'),
        sa.Column('last_sync_attempt', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sync_error', sa.Text(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('risk_assessment_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('requires_certification', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_certified', sa.DateTime(timezone=True), nullable=True),
        sa.Column('certified_by', sa.String(length=255), nullable=True),
        sa.Column('next_certification_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_emergency', sa.Boolean(), nullable=False, default=False),
        sa.Column('emergency_justification', sa.Text(), nullable=True),
        sa.Column('emergency_approver', sa.String(length=255), nullable=True),
        sa.Column('auto_revoke_hours', sa.Integer(), nullable=True),
        sa.Column('assignment_source', sa.String(length=50), nullable=False, default='manual'),
        sa.Column('source_system', sa.String(length=100), nullable=True),
        sa.Column('assignment_context', sa.Text(), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['directory_role_id'], ['directory_roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['privileged_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['service_identity_id'], ['service_identities.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('azure_assignment_id', name='uq_role_assignments_azure_assignment_id')
    )
    
    # =============================================================================
    # Sessions Table
    # =============================================================================
    op.create_table(
        'sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('terminated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('termination_reason', sa.String(length=100), nullable=True),
        sa.Column('authentication_method', sa.String(length=50), nullable=False),
        sa.Column('mfa_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('mfa_methods', sa.Text(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=False, default=50),
        sa.Column('source_ip', sa.String(length=45), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('geographic_location', sa.String(length=255), nullable=True),
        sa.Column('country_code', sa.String(length=2), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('device_fingerprint', sa.String(length=255), nullable=True),
        sa.Column('browser_name', sa.String(length=100), nullable=True),
        sa.Column('browser_version', sa.String(length=50), nullable=True),
        sa.Column('operating_system', sa.String(length=100), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('is_mobile', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_suspicious', sa.Boolean(), nullable=False, default=False),
        sa.Column('anomaly_score', sa.Float(), nullable=True),
        sa.Column('security_flags', sa.Text(), nullable=True),
        sa.Column('concurrent_session_count', sa.Integer(), nullable=False, default=1),
        sa.Column('request_count', sa.Integer(), nullable=False, default=0),
        sa.Column('privileged_operations_count', sa.Integer(), nullable=False, default=0),
        sa.Column('failed_operations_count', sa.Integer(), nullable=False, default=0),
        sa.Column('last_privileged_operation', sa.DateTime(timezone=True), nullable=True),
        sa.Column('session_name', sa.String(length=255), nullable=True),
        sa.Column('application_context', sa.String(length=100), nullable=True),
        sa.Column('client_version', sa.String(length=50), nullable=True),
        sa.Column('audit_trail', sa.Text(), nullable=True),
        sa.Column('compliance_notes', sa.Text(), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['privileged_users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('session_token', name='uq_sessions_session_token')
    )
    
    # =============================================================================
    # Audit Logs Table
    # =============================================================================
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('event_subtype', sa.String(length=100), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('result', sa.String(length=20), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('actor_user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('actor_service_identity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('actor_upn', sa.String(length=255), nullable=True),
        sa.Column('actor_display_name', sa.String(length=255), nullable=True),
        sa.Column('target_user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('target_service_identity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('target_resource_type', sa.String(length=100), nullable=True),
        sa.Column('target_resource_id', sa.String(length=255), nullable=True),
        sa.Column('target_resource_name', sa.String(length=255), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('correlation_id', sa.String(length=255), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('transaction_id', sa.String(length=255), nullable=True),
        sa.Column('source_ip', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('geographic_location', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('previous_values', sa.Text(), nullable=True),
        sa.Column('new_values', sa.Text(), nullable=True),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False, default='info'),
        sa.Column('is_suspicious', sa.Boolean(), nullable=False, default=False),
        sa.Column('anomaly_score', sa.Float(), nullable=True),
        sa.Column('compliance_frameworks', sa.Text(), nullable=True),
        sa.Column('regulatory_classification', sa.String(length=100), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('application', sa.String(length=100), nullable=False, default='menshun-backend'),
        sa.Column('service', sa.String(length=100), nullable=True),
        sa.Column('api_endpoint', sa.String(length=255), nullable=True),
        sa.Column('http_method', sa.String(length=10), nullable=True),
        sa.Column('response_code', sa.Integer(), nullable=True),
        sa.Column('error_code', sa.String(length=100), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('stack_trace', sa.Text(), nullable=True),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('signature', sa.Text(), nullable=True),
        
        # Base model fields (limited for audit logs)
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['actor_user_id'], ['privileged_users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['actor_service_identity_id'], ['service_identities.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['target_user_id'], ['privileged_users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['target_service_identity_id'], ['service_identities.id'], ondelete='SET NULL')
    )
    
    # =============================================================================
    # Credential Rotations Table
    # =============================================================================
    op.create_table(
        'credential_rotations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('gen_random_uuid()')),
        sa.Column('credential_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED', name='rotationstatus'), nullable=False, default='SCHEDULED'),
        sa.Column('scheduled_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('rotation_type', sa.String(length=50), nullable=False, default='automatic'),
        sa.Column('triggered_by', sa.String(length=255), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('old_vault_path', sa.String(length=500), nullable=True),
        sa.Column('new_vault_path', sa.String(length=500), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, default=0),
        sa.Column('max_retries', sa.Integer(), nullable=False, default=3),
        sa.Column('next_retry_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verification_status', sa.String(length=50), nullable=False, default='pending'),
        sa.Column('verification_details', sa.Text(), nullable=True),
        sa.Column('rollback_available', sa.Boolean(), nullable=False, default=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('systems_updated', sa.Text(), nullable=True),
        sa.Column('notifications_sent', sa.Text(), nullable=True),
        
        # Base model fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('updated_by', sa.String(length=255), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('compliance_tags', sa.Text(), nullable=True),
        sa.Column('retention_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('classification', sa.String(length=50), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['credential_id'], ['credentials.id'], ondelete='CASCADE')
    )
    
    # =============================================================================
    # Indexes for Performance
    # =============================================================================
    
    # Directory Roles indexes
    op.create_index('ix_directory_roles_template_id', 'directory_roles', ['template_id'])
    op.create_index('ix_directory_roles_role_name', 'directory_roles', ['role_name'])
    op.create_index('ix_directory_roles_category', 'directory_roles', ['category'])
    op.create_index('ix_directory_roles_is_privileged', 'directory_roles', ['is_privileged'])
    op.create_index('ix_directory_roles_risk_level', 'directory_roles', ['risk_level'])
    op.create_index('ix_directory_roles_is_enabled', 'directory_roles', ['is_enabled'])
    op.create_index('ix_directory_roles_category_privileged', 'directory_roles', ['category', 'is_privileged'])
    op.create_index('ix_directory_roles_risk_level_score', 'directory_roles', ['risk_level', 'risk_score'])
    op.create_index('ix_directory_roles_enabled_category', 'directory_roles', ['is_enabled', 'category'])
    
    # Privileged Users indexes
    op.create_index('ix_privileged_users_upn', 'privileged_users', ['upn'])
    op.create_index('ix_privileged_users_display_name', 'privileged_users', ['display_name'])
    op.create_index('ix_privileged_users_source_user_id', 'privileged_users', ['source_user_id'])
    op.create_index('ix_privileged_users_source_user_upn', 'privileged_users', ['source_user_upn'])
    op.create_index('ix_privileged_users_email', 'privileged_users', ['email'])
    op.create_index('ix_privileged_users_department', 'privileged_users', ['department'])
    op.create_index('ix_privileged_users_is_active', 'privileged_users', ['is_active'])
    op.create_index('ix_privileged_users_manager_upn', 'privileged_users', ['manager_upn'])
    op.create_index('ix_privileged_users_azure_object_id', 'privileged_users', ['azure_object_id'])
    op.create_index('ix_privileged_users_last_sign_in', 'privileged_users', ['last_sign_in'])
    op.create_index('ix_privileged_users_last_activity', 'privileged_users', ['last_activity'])
    op.create_index('ix_privileged_users_is_deleted', 'privileged_users', ['is_deleted'])
    
    # Service Identities indexes
    op.create_index('ix_service_identities_name', 'service_identities', ['name'])
    op.create_index('ix_service_identities_identity_type', 'service_identities', ['identity_type'])
    op.create_index('ix_service_identities_azure_object_id', 'service_identities', ['azure_object_id'])
    op.create_index('ix_service_identities_client_id', 'service_identities', ['client_id'])
    op.create_index('ix_service_identities_tenant_id', 'service_identities', ['tenant_id'])
    op.create_index('ix_service_identities_upn', 'service_identities', ['upn'])
    op.create_index('ix_service_identities_department', 'service_identities', ['department'])
    op.create_index('ix_service_identities_owner_upn', 'service_identities', ['owner_upn'])
    op.create_index('ix_service_identities_environment', 'service_identities', ['environment'])
    op.create_index('ix_service_identities_is_active', 'service_identities', ['is_active'])
    op.create_index('ix_service_identities_status', 'service_identities', ['status'])
    op.create_index('ix_service_identities_expires_at', 'service_identities', ['expires_at'])
    op.create_index('ix_service_identities_last_used', 'service_identities', ['last_used'])
    op.create_index('ix_service_identities_risk_level', 'service_identities', ['risk_level'])
    op.create_index('ix_service_identities_next_rotation_date', 'service_identities', ['next_rotation_date'])
    
    # Credentials indexes
    op.create_index('ix_credentials_service_identity_id', 'credentials', ['service_identity_id'])
    op.create_index('ix_credentials_credential_type', 'credentials', ['credential_type'])
    op.create_index('ix_credentials_name', 'credentials', ['name'])
    op.create_index('ix_credentials_vault_path', 'credentials', ['vault_path'])
    op.create_index('ix_credentials_status', 'credentials', ['status'])
    op.create_index('ix_credentials_expires_at', 'credentials', ['expires_at'])
    op.create_index('ix_credentials_last_used', 'credentials', ['last_used'])
    op.create_index('ix_credentials_next_rotation_date', 'credentials', ['next_rotation_date'])
    op.create_index('ix_credentials_external_id', 'credentials', ['external_id'])
    
    # Role Assignments indexes
    op.create_index('ix_role_assignments_directory_role_id', 'role_assignments', ['directory_role_id'])
    op.create_index('ix_role_assignments_user_id', 'role_assignments', ['user_id'])
    op.create_index('ix_role_assignments_service_identity_id', 'role_assignments', ['service_identity_id'])
    op.create_index('ix_role_assignments_assigned_at', 'role_assignments', ['assigned_at'])
    op.create_index('ix_role_assignments_assigned_by', 'role_assignments', ['assigned_by'])
    op.create_index('ix_role_assignments_expires_at', 'role_assignments', ['expires_at'])
    op.create_index('ix_role_assignments_is_active', 'role_assignments', ['is_active'])
    op.create_index('ix_role_assignments_azure_assignment_id', 'role_assignments', ['azure_assignment_id'])
    op.create_index('ix_role_assignments_next_certification_date', 'role_assignments', ['next_certification_date'])
    op.create_index('ix_role_assignments_is_emergency', 'role_assignments', ['is_emergency'])
    
    # Sessions indexes
    op.create_index('ix_sessions_session_token', 'sessions', ['session_token'])
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'])
    op.create_index('ix_sessions_created_at', 'sessions', ['created_at'])
    op.create_index('ix_sessions_last_activity', 'sessions', ['last_activity'])
    op.create_index('ix_sessions_expires_at', 'sessions', ['expires_at'])
    op.create_index('ix_sessions_is_active', 'sessions', ['is_active'])
    op.create_index('ix_sessions_source_ip', 'sessions', ['source_ip'])
    op.create_index('ix_sessions_country_code', 'sessions', ['country_code'])
    op.create_index('ix_sessions_device_fingerprint', 'sessions', ['device_fingerprint'])
    op.create_index('ix_sessions_is_suspicious', 'sessions', ['is_suspicious'])
    
    # Audit Logs indexes
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_event_subtype', 'audit_logs', ['event_subtype'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_result', 'audit_logs', ['result'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])
    op.create_index('ix_audit_logs_actor_user_id', 'audit_logs', ['actor_user_id'])
    op.create_index('ix_audit_logs_actor_service_identity_id', 'audit_logs', ['actor_service_identity_id'])
    op.create_index('ix_audit_logs_actor_upn', 'audit_logs', ['actor_upn'])
    op.create_index('ix_audit_logs_target_user_id', 'audit_logs', ['target_user_id'])
    op.create_index('ix_audit_logs_target_service_identity_id', 'audit_logs', ['target_service_identity_id'])
    op.create_index('ix_audit_logs_target_resource_type', 'audit_logs', ['target_resource_type'])
    op.create_index('ix_audit_logs_target_resource_id', 'audit_logs', ['target_resource_id'])
    op.create_index('ix_audit_logs_session_id', 'audit_logs', ['session_id'])
    op.create_index('ix_audit_logs_correlation_id', 'audit_logs', ['correlation_id'])
    op.create_index('ix_audit_logs_source_ip', 'audit_logs', ['source_ip'])
    op.create_index('ix_audit_logs_severity', 'audit_logs', ['severity'])
    op.create_index('ix_audit_logs_is_suspicious', 'audit_logs', ['is_suspicious'])
    op.create_index('ix_audit_logs_error_code', 'audit_logs', ['error_code'])
    
    # Credential Rotations indexes
    op.create_index('ix_credential_rotations_credential_id', 'credential_rotations', ['credential_id'])
    op.create_index('ix_credential_rotations_status', 'credential_rotations', ['status'])
    op.create_index('ix_credential_rotations_scheduled_date', 'credential_rotations', ['scheduled_date'])
    op.create_index('ix_credential_rotations_next_retry_at', 'credential_rotations', ['next_retry_at'])


def downgrade() -> None:
    """
    Downgrade the database schema.
    
    WARNING: This will drop all tables and data will be lost.
    """
    # Drop indexes first
    op.drop_index('ix_credential_rotations_next_retry_at', 'credential_rotations')
    op.drop_index('ix_credential_rotations_scheduled_date', 'credential_rotations')
    op.drop_index('ix_credential_rotations_status', 'credential_rotations')
    op.drop_index('ix_credential_rotations_credential_id', 'credential_rotations')
    
    op.drop_index('ix_audit_logs_error_code', 'audit_logs')
    op.drop_index('ix_audit_logs_is_suspicious', 'audit_logs')
    op.drop_index('ix_audit_logs_severity', 'audit_logs')
    op.drop_index('ix_audit_logs_source_ip', 'audit_logs')
    op.drop_index('ix_audit_logs_correlation_id', 'audit_logs')
    op.drop_index('ix_audit_logs_session_id', 'audit_logs')
    op.drop_index('ix_audit_logs_target_resource_id', 'audit_logs')
    op.drop_index('ix_audit_logs_target_resource_type', 'audit_logs')
    op.drop_index('ix_audit_logs_target_service_identity_id', 'audit_logs')
    op.drop_index('ix_audit_logs_target_user_id', 'audit_logs')
    op.drop_index('ix_audit_logs_actor_upn', 'audit_logs')
    op.drop_index('ix_audit_logs_actor_service_identity_id', 'audit_logs')
    op.drop_index('ix_audit_logs_actor_user_id', 'audit_logs')
    op.drop_index('ix_audit_logs_timestamp', 'audit_logs')
    op.drop_index('ix_audit_logs_result', 'audit_logs')
    op.drop_index('ix_audit_logs_action', 'audit_logs')
    op.drop_index('ix_audit_logs_event_subtype', 'audit_logs')
    op.drop_index('ix_audit_logs_event_type', 'audit_logs')
    
    # Drop all other indexes...
    # (Additional index drops would continue here)
    
    # Drop tables in reverse dependency order
    op.drop_table('credential_rotations')
    op.drop_table('audit_logs')
    op.drop_table('sessions')
    op.drop_table('role_assignments')
    op.drop_table('credentials')
    op.drop_table('service_identities')
    op.drop_table('privileged_users')
    op.drop_table('directory_roles')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS rotationstatus')
    op.execute('DROP TYPE IF EXISTS credentialstatus')
    op.execute('DROP TYPE IF EXISTS credentialtype')
    op.execute('DROP TYPE IF EXISTS serviceidentitytype')