---

## Documentation Requirements

### Complete Documentation Structure

```
docs/
├── README.md                     # Main project overview
├── deployment/
│   ├── deployment-guide.md       # Complete deployment instructions
│   ├── docker-setup.md          # Docker-specific deployment
│   ├── cloud-deployment.md      # Azure/AWS/GCP deployment
│   ├── troubleshooting.md       # Common deployment issues
│   └── upgrade-guide.md         # Version upgrade procedures
├── administration/
│   ├── admin-guide.md           # Platform administration guide
│   ├── user-management.md       # User and role management
│   ├── security-configuration.md # Security settings and best practices
│   ├── backup-restore.md        # Backup and recovery procedures
│   └── monitoring-setup.md      # Monitoring and alerting setup
├── user-guides/
│   ├── getting-started.md       # End-user quick start
│   ├── privileged-users.md     # Creating and managing privileged users
│   ├── service-identities.md   # Service identity management
│   ├── credential-management.md # Credential vaulting and rotation
│   └── session-monitoring.md   # Session monitoring features
├── api/
│   ├── api-reference.md         # Complete API documentation
│   ├── authentication.md       # API authentication guide
│   ├── rate-limiting.md         # API usage limits and throttling
│   └── examples/               # API usage examples
├── development/
│   ├── development-setup.md     # Developer environment setup
│   ├── contributing.md          # Contribution guidelines
│   ├── testing.md              # Testing procedures and standards
│   └── architecture.md         # Technical architecture deep-dive
└── compliance/
    ├── security-controls.md     # Security control documentation
    ├── audit-compliance.md     # Compliance and audit procedures
    └── data-protection.md      # Data protection and privacy
```

---

## Project README.md

```markdown
# Menshun - Enterprise Privileged Access Management

<div align="center">
  <img src="docs/assets/menshun-logo.png" alt="Menshun Logo" width="200"/>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
  [![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
</div>

## Overview

**Menshun** is a comprehensive, cloud-native Privileged Access Management tool designed for Microsoft Entra ID environments. Built with Python/FastAPI backend and React frontend, featuring automated privileged user creation, service identity management, and secure credential vaulting with automatic rotation.

*The name "Menshun" reflects our commitment to providing mention-worthy security and access management that enterprises can trust.*

### Key Features

- 🔐 **Privileged User Management**: Automated creation with search-first workflow
- 🤖 **Service Identity Management**: Support for Service Principals, Managed Identities, and Workload Identities
- 🔑 **Credential Vaulting**: Secure storage with automatic rotation
- 👥 **Complete Role Management**: All 130+ Entra ID directory roles
- 📊 **Real-time Monitoring**: Comprehensive audit trails and analytics
- 🎨 **Modern UI**: Solo Leveling-inspired dark theme with glass-morphism effects

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure AD Application Registration
- PostgreSQL 15+ (included in Docker setup)
- Redis 7+ (included in Docker setup)

### 1-Minute Deployment

```bash
# Clone the repository
git clone https://github.com/your-org/menshun.git
cd menshun

# Configure environment
cp .env.example .env
# Edit .env with your Azure AD credentials

# Deploy with Docker Compose
docker-compose up -d

# Access Menshun
open http://localhost:3000
```

## Architecture

### Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18 + TypeScript
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Authentication**: Microsoft Entra ID (Azure AD)
- **Deployment**: Docker + Docker Compose

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB
- **Network**: Internet access for Microsoft Graph API

#### Recommended (Production)
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **Network**: Dedicated connection with monitoring

## Documentation

| Document | Description |
|----------|-------------|
| [Deployment Guide](docs/deployment/deployment-guide.md) | Complete deployment instructions |
| [Admin Guide](docs/administration/admin-guide.md) | Platform administration |
| [User Guide](docs/user-guides/getting-started.md) | End-user documentation |
| [API Reference](docs/api/api-reference.md) | Complete API documentation |
| [Development Setup](docs/development/development-setup.md) | Developer environment |

## Security & Compliance

### Security Features

- ✅ **Zero-Knowledge Access**: Secure credential retrieval patterns
- ✅ **Multi-Factor Authentication**: Required for privileged operations
- ✅ **Audit Logging**: Immutable audit trails with integrity checking
- ✅ **Role-Based Access Control**: Granular permissions
- ✅ **Encryption**: At rest and in transit

### Compliance Standards

- **SOX**: Audit trails and separation of duties
- **SOC 2**: Security controls and monitoring
- **ISO 27001**: Information security management
- **GDPR**: Data protection and privacy controls

## Support

### Getting Help

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-org/menshun/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-org/menshun/discussions)
- 📧 **Enterprise Support**: support@yourcompany.com

### Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development/contributing.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Microsoft Graph SDK team for excellent API support
- Solo Leveling for design inspiration
- FastAPI and React communities for amazing frameworks

---

**Menshun** - Secure. Scalable. Simple. *Mention-worthy.*
```

---

## Deployment Guide (docs/deployment/deployment-guide.md)

```markdown
# Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Azure AD Configuration](#azure-ad-configuration)
4. [Docker Deployment](#docker-deployment)
5. [Database Setup](#database-setup)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Production Considerations](#production-considerations)
8. [Monitoring Setup](#monitoring-setup)
9. [Backup Configuration](#backup-configuration)

## Prerequisites

### System Requirements

#### Minimum System Requirements
```
CPU: 2 cores (x86_64)
RAM: 4GB
Storage: 20GB available space
OS: Linux (Ubuntu 20.04+, CentOS 8+, RHEL 8+)
Docker: 20.10+
Docker Compose: 2.0+
```

#### Recommended Production Requirements
```
CPU: 4 cores (x86_64)
RAM: 8GB
Storage: 100GB SSD
Network: 1Gbps connection
Load Balancer: nginx or cloud LB
Monitoring: Prometheus + Grafana
```

### Network Requirements

#### Outbound Connections Required
```
- graph.microsoft.com:443 (Microsoft Graph API)
- login.microsoftonline.com:443 (Azure AD Authentication)
- your-keyvault.vault.azure.net:443 (Azure Key Vault - if used)
```

#### Inbound Connections
```
- Port 3000: Frontend (React application)
- Port 8000: Backend API (FastAPI)
- Port 5432: PostgreSQL (internal only)
- Port 6379: Redis (internal only)
```

## Environment Setup

### 1. Create Environment File

```bash
# Create .env file from template
cp .env.example .env
```

### 2. Configure Environment Variables

```bash
# .env configuration
# ===================

# Database Configuration
DB_PASSWORD=your_secure_database_password_here
DATABASE_URL=postgresql://pamuser:${DB_PASSWORD}@postgres:5432/pamdb

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Azure AD Configuration
AZURE_CLIENT_ID=your_azure_app_client_id
AZURE_CLIENT_SECRET=your_azure_app_client_secret
AZURE_TENANT_ID=your_azure_tenant_id

# Application Security
SECRET_KEY=your_32_character_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_32_character_encryption_key

# Vault Configuration
VAULT_TYPE=file_vault  # Options: azure_keyvault, hashicorp_vault, file_vault
VAULT_ENCRYPTION_KEY=your_vault_encryption_key

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com

# Email Configuration (Optional)
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
SMTP_FROM_EMAIL=noreply@your-domain.com

# Monitoring (Optional)
SENTRY_DSN=your_sentry_dsn_here
```

### 3. Generate Secure Keys

```bash
# Generate secret keys
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('ENCRYPTION_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('VAULT_ENCRYPTION_KEY=' + secrets.token_urlsafe(32))"
```

## Azure AD Configuration

### 1. Create Azure AD App Registration

```bash
# Using Azure CLI
az login
az ad app create \
  --display-name "PAM Tool" \
  --required-resource-accesses @app-manifest.json \
  --web-redirect-uris "https://your-domain.com/auth/callback"
```

### 2. App Manifest (app-manifest.json)

```json
[
  {
    "resourceAppId": "00000003-0000-0000-c000-000000000000",
    "resourceAccess": [
      {
        "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
        "type": "Scope"
      },
      {
        "id": "06da0dbc-49e2-44d2-8312-53f166ab848a",
        "type": "Role"
      },
      {
        "id": "19dbc75e-c2e2-444c-a770-ec69d8559fc7",
        "type": "Role"
      }
    ]
  }
]
```

### 3. Required API Permissions

#### Delegated Permissions
- `User.ReadWrite.All`
- `Directory.ReadWrite.All`
- `RoleManagement.ReadWrite.Directory`
- `Application.ReadWrite.All`
- `UserAuthenticationMethod.ReadWrite.All`

#### Application Permissions
- `User.ReadWrite.All`
- `Directory.ReadWrite.All`
- `RoleManagement.ReadWrite.Directory`
- `Application.ReadWrite.All`
- `UserAuthenticationMethod.ReadWrite.All`

### 4. Grant Admin Consent

```bash
# Grant admin consent for the application
az ad app permission admin-consent --id YOUR_APP_ID
```

## Docker Deployment

### 1. Download Docker Compose File

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
      - SECRET_KEY=${SECRET_KEY}
      - VAULT_TYPE=${VAULT_TYPE}
      - VAULT_ENCRYPTION_KEY=${VAULT_ENCRYPTION_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./vault_data:/app/vault_data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=pamdb
      - POSTGRES_USER=pamuser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pamuser -d pamdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  celery_worker:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./vault_data:/app/vault_data
      - ./logs:/app/logs
    restart: unless-stopped

  celery_beat:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery beat --loglevel=info
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 2. Deploy the Application

```bash
# Pull the latest images
docker-compose pull

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

### 3. Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed directory roles
docker-compose exec backend python -m app.scripts.seed_roles

# Create initial admin user (optional)
docker-compose exec backend python -m app.scripts.create_admin
```

## Database Setup

### 1. Database Initialization Script (init.sql)

```sql
-- Create database and user
CREATE DATABASE pamdb;
CREATE USER pamuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pamdb TO pamuser;

-- Create extensions
\c pamdb;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO pamuser;
```

### 2. Database Migrations

```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

## SSL/TLS Configuration

### 1. Using Let's Encrypt with nginx

```nginx
# /etc/nginx/sites-available/pam-tool
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Obtain SSL Certificate

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Production Considerations

### 1. Security Hardening

```bash
# Create non-root user
sudo adduser pamuser
sudo usermod -aG docker pamuser

# Set proper file permissions
chmod 600 .env
chown pamuser:pamuser .env

# Configure firewall
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 2. Resource Limits

```yaml
# Add to docker-compose.yml services
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 3. Log Rotation

```bash
# Configure logrotate
sudo nano /etc/logrotate.d/menshun

/var/log/menshun/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 menshun menshun
    postrotate
        docker-compose restart backend
    endscript
}
```

## Monitoring Setup

### 1. Health Check Endpoints

```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# Redis health
curl http://localhost:8000/health/redis
```

### 2. Basic Monitoring Script

```bash
#!/bin/bash
# health-check.sh

BACKEND_URL="http://localhost:8000/health"
FRONTEND_URL="http://localhost:3000"

# Check backend
if curl -f $BACKEND_URL > /dev/null 2>&1; then
    echo "Backend: OK"
else
    echo "Backend: FAILED"
    # Add alert logic here
fi

# Check frontend
if curl -f $FRONTEND_URL > /dev/null 2>&1; then
    echo "Frontend: OK"
else
    echo "Frontend: FAILED"
    # Add alert logic here
fi
```

## Backup Configuration

### 1. Database Backup Script

```bash
#!/bin/bash
# backup-db.sh

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="pamdb"
DB_USER="pamuser"

# Create backup
docker-compose exec -T postgres pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/pamdb_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "pamdb_*.sql.gz" -mtime +30 -delete

echo "Backup completed: pamdb_$DATE.sql.gz"
```

### 2. Full System Backup

```bash
#!/bin/bash
# full-backup.sh

BACKUP_DIR="/backup/full"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR/$DATE

# Backup database
docker-compose exec -T postgres pg_dump -U pamuser pamdb | gzip > $BACKUP_DIR/$DATE/database.sql.gz

# Backup vault data
tar -czf $BACKUP_DIR/$DATE/vault_data.tar.gz ./vault_data/

# Backup configuration
cp .env $BACKUP_DIR/$DATE/
cp docker-compose.yml $BACKUP_DIR/$DATE/

# Backup logs
tar -czf $BACKUP_DIR/$DATE/logs.tar.gz ./logs/

echo "Full backup completed: $BACKUP_DIR/$DATE"
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database logs
docker-compose logs postgres

# Test connection
docker-compose exec backend python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

#### Azure AD Authentication Issues
```bash
# Verify Azure AD configuration
curl -X POST "https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&scope=https://graph.microsoft.com/.default&grant_type=client_credentials"
```

#### Service Startup Issues
```bash
# Check all service statuses
docker-compose ps

# Restart specific service
docker-compose restart backend

# View real-time logs
docker-compose logs -f backend
```

For additional troubleshooting, see [troubleshooting.md](troubleshooting.md).
```

---

## Administrator Guide (docs/administration/admin-guide.md)

```markdown
# Administrator Guide

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [User Management](#user-management)
3. [Security Configuration](#security-configuration)
4. [System Monitoring](#system-monitoring)
5. [Backup and Recovery](#backup-and-recovery)
6. [Troubleshooting](#troubleshooting)

## Initial Setup

### First-Time Login

1. **Access the Application**
   - Navigate to `https://your-domain.com`
   - Click "Sign in with Microsoft"
   - Authenticate with your Azure AD admin account

2. **Initial Configuration**
   - Complete the setup wizard
   - Configure organizational settings
   - Set security policies
   - Review default role assignments

### Administrator Roles

#### Platform Administrators
Users with these roles can manage the PAM tool:

- **Global Administrator**: Full access to all features
- **PAM Administrator**: Manage users, roles, and configurations
- **Security Administrator**: Manage security policies and audit logs
- **Operator**: Day-to-day operations and user support

### System Configuration

#### Basic Settings

Navigate to **Settings > General** to configure:

```
Organization Name: Your Company Name
Domain: company.com
Time Zone: UTC-05:00 (Eastern)
Session Timeout: 8 hours
Audit Retention: 2 years
```

#### Security Policies

Navigate to **Settings > Security**:

```
Multi-Factor Authentication: Required
Password Policy: Complex passwords required
Session Limits: 2 concurrent sessions per user
IP Restrictions: Optional whitelist
Failed Login Threshold: 5 attempts
Account Lockout Duration: 30 minutes
```

## User Management

### Managing Platform Users

#### Adding New Administrators

1. Navigate to **Administration > Platform Users**
2. Click **Add User**
3. Search for user in Azure AD
4. Select appropriate role:
   - **PAM Administrator**: Full management access
   - **Security Administrator**: Security and audit access
   - **Operator**: Operational access only
   - **Viewer**: Read-only access

#### Role Permissions Matrix

| Feature | Global Admin | PAM Admin | Security Admin | Operator | Viewer |
|---------|-------------|-----------|----------------|----------|---------|
| Create Privileged Users | ✅ | ✅ | ❌ | ✅ | ❌ |
| Manage Service Identities | ✅ | ✅ | ❌ | ✅ | ❌ |
| Access Credentials | ✅ | ✅ | ❌ | ✅ | ❌ |
| Manage Platform Settings | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Audit Logs | ✅ | ✅ | ✅ | ✅ | ✅ |
| Security Configuration | ✅ | ❌ | ✅ | ❌ | ❌ |

### Managing Privileged Users

#### Creating Privileged Users

1. Navigate to **Users > Create Privileged User**
2. **Search for Source User**:
   - Enter name, email, or employee ID
   - Select user from search results
   - Review user profile information

3. **Configure Privileged Account**:
   - Verify generated UPN: `lastname_firstname@domain.com`
   - Review copied attributes (department, manager, etc.)
   - Confirm email alias: `originaluser+admin@domain.com`

4. **Assign Directory Roles**:
   - Browse roles by category (Global, Security, Applications)
   - Use search to find specific roles
   - Select appropriate roles for user's responsibilities
   - Review privileged role warnings

5. **Generate TAP**:
   - Configure TAP lifetime (1-24 hours)
   - Set as one-time use
   - Securely share TAP with user

#### Role Assignment Best Practices

**Principle of Least Privilege**:
```
✅ Assign minimum required roles
✅ Use time-limited assignments when possible
✅ Regular access reviews (quarterly)
✅ Document business justification
❌ Avoid permanent Global Administrator assignments
❌ Don't assign multiple high-risk roles unnecessarily
```

**High-Risk Role Combinations to Avoid**:
- Global Administrator + Any other privileged role
- Privileged Role Administrator + User Administrator
- Security Administrator + Application Administrator

#### Monitoring Privileged Users

Navigate to **Users > Privileged Users** for:

- **Active Users**: Currently enabled privileged accounts
- **Inactive Users**: Disabled or suspended accounts
- **Recent Activity**: Last login and actions performed
- **Role Changes**: Recent role assignments/removals
- **TAP Status**: Active and expired temporary access passes

### Disabling Privileged Users

#### Emergency Disable

For immediate security threats:

1. Navigate to **Users > Privileged Users**
2. Find the user account
3. Click **Emergency Disable**
4. Confirm action and provide reason
5. User is immediately disabled in Azure AD

#### Standard Disable Process

For planned account deactivation:

1. Navigate to user profile
2. Click **Disable Account**
3. Select disable reason:
   - User left organization
   - Role no longer required
   - Security concern
   - Temporary suspension
4. Set optional reactivation date
5. Confirm action

## Service Identity Management

### Creating Service Identities

#### Service Principals

1. Navigate to **Identities > Create Service Principal**
2. **Basic Information**:
   ```
   Name: prod-api-service
   Description: Production API service for customer portal
   Environment: Production
   Owner: john.doe@company.com
   ```

3. **Client Secret Configuration**:
   - **Expiration**: 6 months (recommended for production)
   - **Description**: "Production API secret - Jan 2024"
   - **Auto-rotation**: Enable (30 days before expiration)

4. **API Permissions**:
   - **Microsoft Graph**: Select required permissions
   - **Custom APIs**: Add organization-specific APIs
   - **Admin Consent**: Request if required

#### Service Accounts

1. Navigate to **Identities > Create Service Account**
2. **Account Details**:
   ```
   UPN: svc-backup-prod@company.com
   Display Name: Production Backup Service
   Department: IT Operations
   ```

3. **Password Configuration**:
   - **Auto-generated**: 32-character complex password
   - **Rotation Schedule**: 90 days
   - **Vault Storage**: Automatic

4. **Directory Roles**:
   - Assign minimum required roles
   - Avoid privileged roles when possible
   - Document business justification

### Managing Permissions

#### Graph API Permissions

Common permission patterns:

**Read-Only Access**:
```
User.Read.All
Group.Read.All
Application.Read.All
```

**User Management Service**:
```
User.ReadWrite.All
Group.ReadWrite.All
Directory.Read.All
```

**Security Operations**:
```
SecurityEvents.Read.All
IdentityRiskEvent.Read.All
SecurityActions.Read.All
```

#### Directory Role Assignment

Navigate to **Identities > [Service Identity] > Roles**:

1. **View Current Roles**: See all assigned directory roles
2. **Add Roles**: Select from available roles with search/filter
3. **Remove Roles**: Safely remove unnecessary permissions
4. **Role History**: Track all role changes with audit trail

## Credential Management

### Vault Operations

#### Accessing Stored Credentials

1. Navigate to **Credentials > Vault**
2. **Search/Filter**:
   - By service identity name
   - By credential type (password, client secret)
   - By expiration date
   - By last rotation date

3. **Retrieve Credential**:
   - Click on credential entry
   - Provide additional authentication (MFA)
   - Credential displayed for limited time
   - Access logged automatically

#### Manual Credential Rotation

For emergency rotation:

1. Navigate to **Credentials > [Service Identity]**
2. Click **Rotate Now**
3. **Rotation Options**:
   - **Generate New**: Create new random credential
   - **Specify Custom**: Provide specific credential (not recommended)
   - **Update External**: Also update in target systems

4. **Verify Rotation**:
   - Test new credential functionality
   - Confirm old credential is disabled
   - Update any dependent systems

### Rotation Scheduling

#### Automatic Rotation Configuration

Navigate to **Credentials > Rotation Policies**:

**Service Account Passwords**:
```
Default Schedule: Every 90 days
Notification: 14 days before expiration
Auto-Update: Enabled
Retry Policy: 3 attempts with 1-hour intervals
```

**Client Secrets**:
```
Default Schedule: 30 days before expiration
Overlap Period: 48 hours (old and new valid)
Notification: 7 # Enterprise Privileged Access Management (PAM) Tool
## Product Requirements Document

## Executive Summary
A comprehensive cloud-native and self-hostable Privileged Access Management tool built with Python/FastAPI backend and React frontend. The tool provides automated privileged user creation, service identity management, and secure credential vaulting with automatic rotation capabilities.

## Core Features Overview

### 1. Privileged User Management
- **User Search & Creation**: Search existing Entra users and create privileged accounts
- **Role Assignment**: Interactive role selection during user creation
- **Temporary Access Pass**: Passwordless onboarding with TAP generation

### 2. Service Identity Management
- **Multi-Identity Support**: Service Accounts, Service Principals, Managed Identities, Workload Identities
- **Permission Management**: Graph API permissions and directory role assignments
- **Secret Management**: Client secret generation with configurable expiration

### 3. Credential Vaulting & Rotation
- **Automated Vaulting**: Secure storage of passwords and client secrets
- **Automatic Rotation**: Configurable rotation schedules
- **Audit Trail**: Complete credential lifecycle tracking

---

## Technical Architecture

### Technology Stack

#### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ with SQLAlchemy ORM
- **Caching**: Redis 7.0+
- **Background Jobs**: Celery with Redis broker
- **Authentication**: MSAL Python + JWT

#### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: React Query (TanStack Query)
- **Forms**: React Hook Form with Zod validation

#### Microsoft Integration
- **Graph SDK**: Microsoft Graph SDK for Python
- **Authentication**: Azure AD App Registration
- **Permissions**: Graph API delegated and application permissions

#### Security & Deployment
- **Containerization**: Docker + Docker Compose
- **Secrets Management**: Integration with Azure Key Vault, HashiCorp Vault, or file-based
- **Monitoring**: Structured logging + Sentry error tracking
- **Deployment**: Self-hosted Docker, cloud-ready architecture

### Required Microsoft Graph Permissions
```json
{
  "delegated": [
    "User.ReadWrite.All",
    "Directory.ReadWrite.All",
    "RoleManagement.ReadWrite.Directory",
    "Application.ReadWrite.All",
    "UserAuthenticationMethod.ReadWrite.All"
  ],
  "application": [
    "User.ReadWrite.All",
    "Directory.ReadWrite.All",
    "RoleManagement.ReadWrite.Directory",
    "Application.ReadWrite.All",
    "UserAuthenticationMethod.ReadWrite.All"
  ]
}
```

---

## Detailed Feature Specifications

### Feature 1: Privileged User Creation Workflow

#### 1.1 User Search Interface
**Endpoint**: `GET /api/v1/users/search?query={searchTerm}`

**Frontend Components**:
- Search input with debounced API calls
- User result cards displaying: photo, name, email, department, title
- "Select User" action for each result

**Search Capabilities**:
- Search by: Display Name, UPN, Email, Employee ID
- Fuzzy matching with relevance scoring
- Maximum 50 results per search

#### 1.2 User Profile Review
**Endpoint**: `GET /api/v1/users/{userId}/profile`

**Display Information**:
- Basic Info: Name, UPN, Department, Title, Manager
- Employment: Employee Type, Company, Office Location
- Contact: Email, Phone, Mobile
- Preview of proposed privileged account details

**Privileged Account Generation Rules**:
```python
# Naming Convention
privileged_upn = f"{last_name}_{first_name}@{domain}"
privileged_email = f"{original_upn.split('@')[0]}+admin@{domain}"
employee_type = "Admin"

# Copied Attributes
copied_attributes = [
    "department", "job_title", "company_name", 
    "office_location", "manager", "usage_location"
]
```

#### 1.3 Role Selection Interface
**Endpoint**: `GET /api/v1/directory-roles`

**Frontend Features**:
- Searchable/filterable role list
- Checkbox selection with bulk actions
- Role descriptions and permission summaries
- "Select All", "Clear All", "Recommended Roles" quick actions

**Role Categories** (Complete Entra ID Directory Roles):

**Global & Privileged Roles**:
- Global Administrator, Global Reader, Privileged Role Administrator, Privileged Authentication Administrator

**Security & Compliance**:
- Security Administrator, Security Reader, Security Operator, Compliance Administrator, Compliance Data Administrator, Conditional Access Administrator, Authentication Administrator, Authentication Policy Administrator, Authentication Extensibility Administrator

**User & Identity Management**:
- User Administrator, Helpdesk Administrator, Password Administrator, Hybrid Identity Administrator, Identity Governance Administrator, Directory Readers, Directory Writers, Directory Synchronization Accounts

**Application & Service Management**:
- Application Administrator, Application Developer, Cloud Application Administrator, Cloud Device Administrator, External Identity Provider Administrator

**Microsoft 365 Services**:
- Exchange Administrator, Exchange Recipient Administrator, SharePoint Administrator, SharePoint Embedded Administrator, Teams Administrator, Teams Communications Administrator, Teams Communications Support Engineer, Teams Communications Support Specialist, Teams Devices Administrator, Teams Reader, Teams Telephony Administrator

**Azure & Cloud Services**:
- Azure DevOps Administrator, Azure Information Protection Administrator, Intune Administrator, Windows 365 Administrator, Windows Update Deployment Administrator

**Analytics & Insights**:
- Insights Administrator, Insights Analyst, Insights Business Leader, Reports Reader, Usage Summary Reports Reader

**Data & Information Protection**:
- B2C IEF Keyset Administrator, B2C IEF Policy Administrator, Attribute Assignment Administrator, Attribute Assignment Reader, Attribute Definition Administrator, Attribute Definition Reader, Attribute Log Administrator, Attribute Log Reader, Attribute Provisioning Administrator, Attribute Provisioning Reader

**Business Applications**:
- Dynamics 365 Administrator, Dynamics 365 Business Central Administrator, Power Platform Administrator, Fabric Administrator, Yammer Administrator

**Specialized Roles**:
- AI Administrator, Attack Payload Author, Attack Simulation Administrator, Billing Administrator, Cloud App Security Administrator, Customer LockBox Access Approver, Desktop Analytics Administrator, Domain Name Administrator, Edge Administrator, External ID User Flow Administrator, External ID User Flow Attribute Administrator, Global Secure Access Administrator, Global Secure Access Log Reader, Groups Administrator, Guest Inviter, IoT Device Administrator, Kaizala Administrator, Knowledge Administrator, Knowledge Manager, License Administrator, Lifecycle Workflows Administrator, Message Center Privacy Reader, Message Center Reader, Microsoft 365 Backup Administrator, Microsoft 365 Migration Administrator, Microsoft Entra Joined Device Local Administrator, Microsoft Graph Data Connect Administrator, Microsoft Hardware Warranty Administrator, Microsoft Hardware Warranty Specialist, Network Administrator, Office Apps Administrator, Organizational Branding Administrator, Organizational Data Source Administrator, Organizational Messages Approver, Organizational Messages Writer, Partner Tier1 Support, Partner Tier2 Support, People Administrator, Permissions Management Administrator, Printer Administrator, Printer Technician, Search Administrator, Search Editor, Service Support Administrator, Skype for Business Administrator, Tenant Creator, User Experience Success Manager, Virtual Visits Administrator, Viva Glint Tenant Administrator, Viva Goals Administrator, Viva Pulse Administrator

**Total Available Roles**: 130+ Entra ID Directory Roles

#### 1.4 Account Creation & TAP Generation
**Endpoint**: `POST /api/v1/users/privileged`

**Request Payload**:
```json
{
  "source_user_id": "uuid",
  "selected_roles": ["role_id_1", "role_id_2"],
  "tap_settings": {
    "lifetime_hours": 4,
    "one_time_use": true
  }
}
```

**Response**:
```json
{
  "user_id": "uuid",
  "upn": "smith_john@company.com",
  "display_name": "John Smith (Admin)",
  "tap_code": "AB123CD8",
  "tap_expires_at": "2024-07-16T18:00:00Z",
  "assigned_roles": ["Security Administrator", "User Administrator"],
  "audit_id": "uuid"
}
```

### Feature 2: Service Identity Management

#### 2.1 Identity Type Selection
**Main Interface**: Identity creation wizard with type selection:

1. **Service Account** (Azure AD User for services)
2. **Service Principal** (Application identity)
3. **Managed Identity** (Azure resource identity)
4. **Workload Identity** (Kubernetes workload identity)

#### 2.2 Service Account Creation
**Endpoint**: `POST /api/v1/service-accounts`

**Workflow**:
1. **Basic Information**: Name, description, department
2. **Password Settings**: Auto-generated secure password with rotation schedule
3. **Directory Roles**: Select applicable directory roles
4. **Review & Create**: Final confirmation with credential display

**Service Account Naming**: `svc-{purpose}-{environment}@domain.com`

#### 2.3 Service Principal Creation
**Endpoint**: `POST /api/v1/service-principals`

**Workflow**:
1. **Application Registration**: App name, description, redirect URIs
2. **Client Secret**: Generate secret with expiration (3 months, 6 months, 1 year, 2 years)
3. **Graph Permissions**: 
   - **Delegated Permissions**: User interaction required
   - **Application Permissions**: App-only access
4. **API Permissions**: Custom API permissions if needed

**Permission Selection Interface**:
- Categorized permission list (Users, Groups, Mail, Calendar, etc.)
- Search and filter permissions
- Permission description and risk level indicators
- Admin consent requirements clearly marked

#### 2.4 Managed Identity Creation
**Endpoint**: `POST /api/v1/managed-identities`

**Types**:
- **System-Assigned**: Tied to specific Azure resource
- **User-Assigned**: Standalone identity for multiple resources

**Configuration**:
- Azure subscription and resource group selection
- Resource assignments
- Role assignments (Azure RBAC)
- Graph API permissions

#### 2.5 Workload Identity Creation
**Endpoint**: `POST /api/v1/workload-identities`

**Configuration**:
- Kubernetes cluster information
- Service account mapping
- OIDC issuer configuration
- Federated identity credentials

### Feature 3: Credential Vaulting & Rotation

#### 3.1 Vault Integration
**Supported Vault Backends**:
- **Azure Key Vault**: Primary cloud option
- **HashiCorp Vault**: Enterprise on-premises option
- **File-based Vault**: Encrypted JSON for development/small deployments

**Vault Configuration**:
```yaml
vault:
  backend: "azure_keyvault"  # or "hashicorp_vault", "file_vault"
  azure_keyvault:
    vault_url: "https://vault.vault.azure.net/"
    client_id: "${AZURE_CLIENT_ID}"
    client_secret: "${AZURE_CLIENT_SECRET}"
  encryption_key: "${VAULT_ENCRYPTION_KEY}"
```

#### 3.2 Automatic Rotation
**Rotation Schedules**:
- **Service Account Passwords**: 90 days (configurable)
- **Client Secrets**: 180 days before expiration
- **Custom Schedules**: Per-identity configuration

**Rotation Process**:
1. Generate new credential
2. Update in target system (Azure AD)
3. Update vault with new credential
4. Verify new credential works
5. Retire old credential
6. Audit log all steps

**Endpoint**: `POST /api/v1/credentials/{credential_id}/rotate`

#### 3.3 Credential Retrieval
**Secure Access Patterns**:
- Time-limited access tokens
- Just-in-time credential retrieval
- Audit logging of all access
- Role-based access control

**Endpoint**: `GET /api/v1/credentials/{credential_id}/value`
- Requires additional authentication
- Returns credential with access log entry
- Optional time-limited response

---

## Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE privileged_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upn VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    source_user_id VARCHAR(255) NOT NULL,
    source_user_upn VARCHAR(255) NOT NULL,
    employee_type VARCHAR(50) DEFAULT 'Admin',
    department VARCHAR(255),
    job_title VARCHAR(255),
    manager_upn VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    last_tap_generated TIMESTAMP,
    metadata JSONB
);
```

#### Service Identities Table
```sql
CREATE TABLE service_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    identity_type VARCHAR(50) NOT NULL, -- 'service_account', 'service_principal', etc.
    azure_object_id VARCHAR(255) UNIQUE,
    client_id VARCHAR(255),
    description TEXT,
    department VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,
    metadata JSONB
);
```

#### Credentials Table
```sql
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_identity_id UUID REFERENCES service_identities(id),
    credential_type VARCHAR(50) NOT NULL, -- 'password', 'client_secret'
    vault_path VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP,
    rotation_schedule_days INTEGER DEFAULT 90,
    last_rotated TIMESTAMP,
    next_rotation TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Directory Roles Data Model
```sql
CREATE TABLE directory_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id VARCHAR(255) UNIQUE NOT NULL, -- Azure template ID
    role_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_privileged BOOLEAN DEFAULT false,
    category VARCHAR(100), -- 'Global', 'Security', 'User Management', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert all 130+ Entra ID Directory Roles
INSERT INTO directory_roles (template_id, role_name, description, is_privileged, category) VALUES
('62e90394-69f5-4237-9190-012177145e10', 'Global Administrator', 'Can manage all aspects of Microsoft Entra ID and Microsoft services that use Microsoft Entra identities.', true, 'Global'),
('e8611ab8-c189-46e8-94e1-60213ab1f814', 'Privileged Role Administrator', 'Can manage role assignments in Microsoft Entra ID, and all aspects of Privileged Identity Management.', true, 'Global'),
('7be44c8a-adaf-4e2a-84d6-ab2649e08a13', 'Privileged Authentication Administrator', 'Can access to view, set and reset authentication method information for any user (admin or non-admin).', true, 'Security'),
('194ae4cb-b126-40b2-bd5b-6091b380977d', 'Security Administrator', 'Can read security information and reports, and manage configuration in Microsoft Entra ID and Office 365.', true, 'Security'),
('b1be1c3e-b65d-4f19-8427-f6fa0d97feb9', 'Conditional Access Administrator', 'Can manage Conditional Access capabilities.', true, 'Security'),
('fe930be7-5e62-47db-91af-98c3a49a38b1', 'User Administrator', 'Can manage all aspects of users and groups, including resetting passwords for limited admins.', true, 'User Management'),
('9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3', 'Application Administrator', 'Can create and manage all aspects of app registrations and enterprise apps.', true, 'Application'),
-- ... (additional 120+ roles from the provided list)
;
```

---

## API Specification

### Authentication Endpoints
```
POST   /api/v1/auth/login           # Initiate Azure AD login
POST   /api/v1/auth/callback        # Handle Azure AD callback
POST   /api/v1/auth/refresh         # Refresh access token
DELETE /api/v1/auth/logout          # Logout and invalidate session
```

### User Management Endpoints
```
GET    /api/v1/users/search         # Search Entra users
GET    /api/v1/users/{id}/profile   # Get user profile
POST   /api/v1/users/privileged     # Create privileged user
PATCH  /api/v1/users/{id}/disable   # Disable user
GET    /api/v1/users/{id}/roles     # Get user roles
POST   /api/v1/users/{id}/roles     # Assign roles
DELETE /api/v1/users/{id}/roles/{role_id} # Remove role
```

### Service Identity Endpoints
```
GET    /api/v1/service-identities          # List service identities
POST   /api/v1/service-accounts            # Create service account
POST   /api/v1/service-principals          # Create service principal
POST   /api/v1/managed-identities          # Create managed identity
POST   /api/v1/workload-identities         # Create workload identity
GET    /api/v1/service-identities/{id}     # Get identity details
PATCH  /api/v1/service-identities/{id}     # Update identity
DELETE /api/v1/service-identities/{id}     # Delete identity
```

### Permission Management Endpoints
```
GET    /api/v1/directory-roles             # List all 130+ directory roles with filtering
GET    /api/v1/directory-roles/categories  # Get role categories for UI grouping
GET    /api/v1/directory-roles/{id}        # Get specific role details
GET    /api/v1/directory-roles/privileged  # Get only privileged roles
GET    /api/v1/graph-permissions           # List Graph permissions
POST   /api/v1/service-identities/{id}/permissions/graph     # Grant Graph permissions
POST   /api/v1/service-identities/{id}/permissions/directory # Grant directory roles
```

### Credential Management Endpoints
```
GET    /api/v1/credentials                 # List credentials (metadata only)
POST   /api/v1/credentials/{id}/rotate     # Rotate credential
GET    /api/v1/credentials/{id}/value      # Get credential value (secure)
PATCH  /api/v1/credentials/{id}/schedule   # Update rotation schedule
```

### Audit & Reporting Endpoints
```
GET    /api/v1/audit-logs                  # Get audit logs
GET    /api/v1/reports/users               # User management reports
GET    /api/v1/reports/credentials         # Credential reports
GET    /api/v1/reports/permissions         # Permission reports
```

---

## Deployment Architecture

### Self-Hosted Deployment

#### Docker Compose Configuration
```yaml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://pamuser:${DB_PASSWORD}@postgres:5432/pamdb
      - REDIS_URL=redis://redis:6379/0
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
      - SECRET_KEY=${SECRET_KEY}
      - VAULT_TYPE=file_vault
      - VAULT_ENCRYPTION_KEY=${VAULT_ENCRYPTION_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./vault_data:/app/vault_data
      - ./logs:/app/logs

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
    ports:
      - "3000:3000"
    depends_on:
      - backend

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=pamdb
      - POSTGRES_USER=pamuser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery_worker:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://pamuser:${DB_PASSWORD}@postgres:5432/pamdb
      - REDIS_URL=redis://redis:6379/0
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./vault_data:/app/vault_data
      - ./logs:/app/logs

  celery_beat:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://pamuser:${DB_PASSWORD}@postgres:5432/pamdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

#### Environment Configuration
```bash
# .env file
DB_PASSWORD=your_secure_db_password
AZURE_CLIENT_ID=your_azure_app_client_id
AZURE_CLIENT_SECRET=your_azure_app_secret
AZURE_TENANT_ID=your_azure_tenant_id
SECRET_KEY=your_jwt_secret_key
VAULT_ENCRYPTION_KEY=your_vault_encryption_key
```

### Production Considerations

#### Security Hardening
- **HTTPS Only**: TLS termination at load balancer or nginx proxy
- **Network Isolation**: Private subnets for database and Redis
- **Secrets Management**: External secret store integration
- **Access Control**: IP whitelisting and VPN access
- **Monitoring**: Comprehensive logging and alerting

#### Scalability
- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database**: Read replicas for reporting workloads
- **Caching**: Redis Cluster for high availability
- **Background Jobs**: Multiple Celery workers

#### Backup Strategy
- **Database**: Automated daily backups with point-in-time recovery
- **Vault Data**: Encrypted backup of credential store
- **Configuration**: Version-controlled infrastructure as code

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] FastAPI project setup with authentication
- [ ] Database schema and migrations (including all 130+ directory roles)
- [ ] Directory roles seeding script with complete Entra ID role catalog
- [ ] Basic Microsoft Graph integration
- [ ] Docker containerization

### Phase 2: Privileged User Management (Weeks 3-4)
- [ ] User search functionality with Graph API integration
- [ ] Privileged user creation workflow
- [ ] Complete role assignment interface with all 130+ roles
- [ ] Role categorization and filtering (Global, Security, Applications, etc.)
- [ ] TAP generation and management

### Phase 3: Service Identity Management (Weeks 5-7)
- [ ] Service Principal creation and management
- [ ] Service Account creation workflow
- [ ] Permission assignment interfaces (Graph + Directory roles)
- [ ] Client secret generation with configurable expiration
- [ ] Role assignment validation and conflict detection

### Phase 4: Credential Vaulting (Weeks 8-9)
- [ ] Vault backend integration
- [ ] Credential storage and retrieval
- [ ] Basic rotation scheduling
- [ ] Security controls for credential access

### Phase 5: Advanced Features (Weeks 10-12)
- [ ] Automatic credential rotation
- [ ] Managed Identity support
- [ ] Workload Identity integration
- [ ] Advanced reporting and analytics

### Phase 6: Production Readiness (Weeks 13-14)
- [ ] Security hardening and penetration testing
- [ ] Performance optimization and caching strategies
- [ ] Comprehensive testing (unit, integration, e2e)
- [ ] Documentation and deployment guides
- [ ] Solo Leveling design system implementation

### Phase 7: Session Monitoring (Weeks 15-17) - Future Enhancement
- [ ] Real-time session tracking implementation
- [ ] Geographic session visualization dashboard
- [ ] Risk scoring and anomaly detection algorithms
- [ ] Session recording and audit capabilities
- [ ] Advanced security monitoring and alerting

### Phase 8: Advanced Features (Weeks 18-20) - Future Roadmap
- [ ] Advanced reporting and analytics suite
- [ ] Mobile application development
- [ ] Multi-tenant support architecture
- [ ] Custom workflow engine implementation
- [ ] Zero Trust integration features

---

## Security & Compliance

### Data Protection
- **Encryption at Rest**: Database and vault encryption
- **Encryption in Transit**: TLS 1.3 for all communications
- **Credential Security**: Zero-knowledge access patterns
- **Audit Trail**: Immutable audit logs with integrity checking

### Access Controls
- **Role-Based Access**: Granular permissions for tool features
- **Multi-Factor Authentication**: Required for privileged operations
- **Just-in-Time Access**: Time-limited credential retrieval
- **Principle of Least Privilege**: Minimal required permissions

### Compliance Features
- **SOX Compliance**: Audit trails and separation of duties
- **SOC 2**: Security controls and monitoring
- **ISO 27001**: Information security management
- **Custom Compliance**: Configurable audit and reporting

This comprehensive **Menshun** tool provides enterprise-grade privileged access management with modern security practices, flexible deployment options, and extensive Microsoft ecosystem integration.