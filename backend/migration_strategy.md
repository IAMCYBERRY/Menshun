# Database Migration Strategy

## Overview

This document outlines the multi-phase migration strategy for the Menshun PAM system database. The approach ensures smooth deployment by separating basic table creation from advanced index creation.

## Phase 1: Initial Migration (Current)

Creates basic table structure with simple indexes only:

### Tables Created:
- `privileged_users`
- `directory_roles`
- `service_identities`
- `credentials`
- `credential_rotations`
- `role_assignments`
- `sessions`
- `audit_logs`

### Index Types Included:
- Basic column indexes (automatically created by SQLAlchemy for indexed columns)
- Simple composite indexes (no WHERE clauses or special operators)
- Unique constraints
- Foreign key constraints

### Index Types Deferred:
- Partial indexes with WHERE clauses
- GIN indexes for full-text search
- Indexes requiring PostgreSQL extensions (pg_trgm)
- Complex conditional indexes

## Phase 2: Advanced Indexes Migration (Future)

### Prerequisites:
1. Ensure PostgreSQL extensions are installed:
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   ```

### Advanced Indexes to Add:

#### Service Identities:
```sql
-- Partial indexes for active identities
CREATE INDEX CONCURRENTLY ix_service_identities_active_name_partial 
ON service_identities (name) 
WHERE is_active = true AND is_deleted = false;

-- Rotation and expiration partial indexes
CREATE INDEX CONCURRENTLY ix_service_identities_rotation_partial 
ON service_identities (next_rotation_date) 
WHERE next_rotation_date IS NOT NULL AND is_active = true;

CREATE INDEX CONCURRENTLY ix_service_identities_expiration_partial 
ON service_identities (expires_at) 
WHERE expires_at IS NOT NULL AND is_active = true;

-- Full-text search index
CREATE INDEX CONCURRENTLY ix_service_identities_search_gin 
ON service_identities USING gin (name gin_trgm_ops, description gin_trgm_ops);
```

#### Directory Roles:
```sql
-- Full-text search for role names and descriptions
CREATE INDEX CONCURRENTLY ix_directory_roles_search_gin 
ON directory_roles USING gin (role_name gin_trgm_ops, description gin_trgm_ops);
```

#### Role Assignments:
```sql
-- Partial indexes for active assignments
CREATE INDEX CONCURRENTLY ix_role_assignments_expiry_partial 
ON role_assignments (expires_at) 
WHERE expires_at IS NOT NULL AND is_active = true;

CREATE INDEX CONCURRENTLY ix_role_assignments_certification_partial 
ON role_assignments (next_certification_date) 
WHERE requires_certification = true AND is_active = true;

CREATE INDEX CONCURRENTLY ix_role_assignments_emergency_partial 
ON role_assignments (is_emergency, assigned_at) 
WHERE is_emergency = true;
```

#### Sessions:
```sql
-- Partial indexes for active sessions
CREATE INDEX CONCURRENTLY ix_sessions_expiry_cleanup_partial 
ON sessions (expires_at, is_active) 
WHERE is_active = true;

CREATE INDEX CONCURRENTLY ix_sessions_active_activity_partial 
ON sessions (last_activity) 
WHERE is_active = true;
```

#### Users:
```sql
-- Partial index for active users
CREATE INDEX CONCURRENTLY ix_privileged_users_active_upn_partial 
ON privileged_users (upn) 
WHERE is_active = true AND is_deleted = false;
```

#### Credentials:
```sql
-- Partial indexes for active credentials
CREATE INDEX CONCURRENTLY ix_credentials_rotation_schedule_partial 
ON credentials (next_rotation_date, auto_rotation_enabled) 
WHERE next_rotation_date IS NOT NULL AND auto_rotation_enabled = true;

CREATE INDEX CONCURRENTLY ix_credentials_expiry_partial 
ON credentials (expires_at, status) 
WHERE expires_at IS NOT NULL AND status = 'active';

CREATE INDEX CONCURRENTLY ix_credentials_active_name_partial 
ON credentials (name) 
WHERE status = 'active' AND is_deleted = false;
```

#### Credential Rotations:
```sql
-- Partial index for failed rotations needing retry
CREATE INDEX CONCURRENTLY ix_credential_rotations_retry_partial 
ON credential_rotations (next_retry_at) 
WHERE next_retry_at IS NOT NULL AND status = 'failed';
```

#### Audit Logs:
```sql
-- GIN index for compliance frameworks
CREATE INDEX CONCURRENTLY ix_audit_logs_compliance_gin 
ON audit_logs USING gin (compliance_frameworks);

-- Full-text search for descriptions and details
CREATE INDEX CONCURRENTLY ix_audit_logs_search_gin 
ON audit_logs USING gin (description gin_trgm_ops, details gin_trgm_ops);
```

## Phase 3: Performance Optimizations (Future)

### Table Partitioning:
- Partition `audit_logs` by timestamp (monthly partitions)
- Partition `sessions` by created_at (monthly partitions)

### Additional Optimizations:
- Analyze table statistics after initial data load
- Adjust work_mem and other PostgreSQL settings
- Consider materialized views for complex reporting queries

## Migration Commands

### For Phase 2 (Advanced Indexes):
```bash
# Create migration file
alembic revision --autogenerate -m "Add advanced indexes and partial indexes"

# Apply migration
alembic upgrade head
```

### Best Practices:
1. Use `CREATE INDEX CONCURRENTLY` to avoid blocking operations
2. Test migrations on staging environment first
3. Monitor index usage with `pg_stat_user_indexes`
4. Drop unused indexes to improve write performance

## Rollback Strategy

Each phase can be rolled back independently:
```bash
# Rollback to previous revision
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

## Monitoring

After each migration phase:
1. Check query performance with `EXPLAIN ANALYZE`
2. Monitor index usage statistics
3. Verify application functionality
4. Check database size and growth patterns