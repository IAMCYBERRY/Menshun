# 🚀 Menshun PAM Deployment Guide

This comprehensive guide covers deploying the Menshun Enterprise Privileged Access Management system across various environments, from local development to enterprise production.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Azure AD Configuration](#azure-ad-configuration)
- [Local Development](#local-development)
- [Production Deployment Options](#production-deployment-options)
  - [Docker Compose (Recommended)](#docker-compose-recommended)
  - [Azure Container Apps](#azure-container-apps)
  - [Kubernetes](#kubernetes)
  - [Manual Installation](#manual-installation)
- [Post-Deployment Configuration](#post-deployment-configuration)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Security Hardening](#security-hardening)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements

**Minimum Hardware:**
- CPU: 4 cores (8 recommended)
- RAM: 8GB (16GB recommended)
- Storage: 50GB SSD (100GB+ recommended)
- Network: 1Gbps connection

**Software Dependencies:**
- Docker 24.0+ and Docker Compose 2.0+
- PostgreSQL 15+ (managed or self-hosted)
- Redis 7+ (for caching and sessions)
- SSL Certificate (Let's Encrypt or commercial)

### Infrastructure Requirements

**Network Configuration:**
- Domain name (e.g., `pam.yourcompany.com`)
- SSL/TLS certificates
- Firewall rules (ports 80, 443)
- DNS configuration

**External Services:**
- Microsoft Entra ID (Azure AD) tenant
- Azure Key Vault (for credential storage)
- SMTP server (for notifications)
- Backup storage (S3, Azure Blob, etc.)

---

## 🔐 Azure AD Configuration

### 1. Create App Registration

```bash
# Install Azure CLI if not already installed
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create the app registration
az ad app create \
  --display-name "Menshun PAM System" \
  --web-redirect-uris "https://pam.yourcompany.com" "http://localhost:3000" \
  --sign-in-audience "AzureADMyOrg"

# Note the appId from the output - this is your AZURE_CLIENT_ID
```

### 2. Configure API Permissions

1. Navigate to **Azure Portal** → **Azure Active Directory** → **App registrations**
2. Find your "Menshun PAM System" app
3. Go to **API permissions** → **Add a permission** → **Microsoft Graph**
4. Add these **Application permissions**:
   - `Directory.Read.All`
   - `Directory.ReadWrite.All`
   - `User.Read.All`
   - `User.ReadWrite.All`
   - `RoleManagement.Read.All`
   - `RoleManagement.ReadWrite.Directory`
   - `AuditLog.Read.All`

5. **Grant admin consent** for your organization

### 3. Create Client Secret

```bash
# Create a client secret (valid for 2 years)
az ad app credential reset --id <YOUR_APP_ID> --years 2

# Note the password from the output - this is your AZURE_CLIENT_SECRET
```

### 4. Configure Authentication

1. In the app registration, go to **Authentication**
2. Add these redirect URIs:
   - `https://pam.yourcompany.com` (production)
   - `http://localhost:3000` (development)
3. Enable **ID tokens** and **Access tokens**
4. Set **Logout URL**: `https://pam.yourcompany.com/logout`

---

## 💻 Local Development

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/menshun.git
cd menshun

# 2. Setup environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Configure Azure AD settings in both .env files
# Edit backend/.env:
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_TENANT_ID=your_tenant_id_here

# Edit frontend/.env:
VITE_AZURE_CLIENT_ID=your_client_id_here
VITE_AZURE_TENANT_ID=your_tenant_id_here

# 4. Start all services
docker-compose up -d

# 5. Initialize database
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.scripts.seed_roles

# 6. Create your first admin user (optional)
docker-compose exec backend python -m app.scripts.create_admin_user
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (user: `pamuser`, password: `password`)
- **Redis**: localhost:6379

### Development Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run tests
docker-compose exec backend pytest
docker-compose exec frontend npm test

# Database operations
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head

# Access database
docker-compose exec database psql -U pamuser -d pamdb

# Stop services
docker-compose down

# Reset everything (⚠️ destroys data)
docker-compose down -v
docker system prune -f
```

---

## 🏢 Production Deployment Options

### Docker Compose (Recommended)

Best for small to medium enterprises with simpler infrastructure needs.

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create deployment directory
sudo mkdir -p /opt/menshun
sudo chown $USER:$USER /opt/menshun
cd /opt/menshun
```

#### 2. Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/menshun.git .

# Setup production environment
cd deploy/production
cp .env.example .env

# Configure environment variables
nano .env
# Update all values, especially:
# - DOMAIN=pam.yourcompany.com
# - All passwords and secrets
# - Azure AD configuration
# - Database settings

# Create required directories
mkdir -p logs traefik/certificates monitoring/grafana/{dashboards,datasources}

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
docker-compose -f docker-compose.prod.yml exec backend python -m app.scripts.seed_roles

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

#### 3. SSL Certificate Setup

```bash
# Option 1: Let's Encrypt (automatic)
# Traefik will automatically obtain certificates if configured

# Option 2: Manual certificate
# Copy your certificates to:
# - traefik/certificates/pam.yourcompany.com.crt
# - traefik/certificates/pam.yourcompany.com.key
```

### Azure Container Apps

Best for Azure-native deployments with automatic scaling and managed services.

#### 1. Prerequisites

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login and set subscription
az login
az account set --subscription "Your Subscription Name"

# Install Container Apps extension
az extension add --name containerapp
```

#### 2. Deploy Infrastructure

```bash
# Clone repository
git clone https://github.com/yourusername/menshun.git
cd menshun/deploy/azure

# Set variables
export RESOURCE_GROUP="menshun-pam-rg"
export LOCATION="eastus"
export ENVIRONMENT_NAME="menshun-prod"
export ACR_NAME="menshunacr$(openssl rand -hex 3)"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy using the provided script
chmod +x deploy.sh
./deploy.sh
```

#### 3. Custom Domain Setup

```bash
# Add custom domain to Container Apps
az containerapp hostname add \
  --hostname pam.yourcompany.com \
  --resource-group $RESOURCE_GROUP \
  --name menshun-frontend

az containerapp hostname add \
  --hostname api.yourcompany.com \
  --resource-group $RESOURCE_GROUP \
  --name menshun-backend
```

### Kubernetes

Best for large enterprises requiring high availability, auto-scaling, and multi-region deployments.

#### 1. Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

#### 2. Deploy to Kubernetes

```bash
# Clone repository
git clone https://github.com/yourusername/menshun.git
cd menshun/deploy/kubernetes

# Update configuration
# Edit secrets.yaml with base64 encoded values:
echo -n "your_password" | base64

# Apply manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Check deployment status
kubectl get pods -n menshun-pam
kubectl get services -n menshun-pam
kubectl get ingress -n menshun-pam
```

#### 3. Initialize Database

```bash
# Run database migrations
kubectl exec -n menshun-pam deployment/menshun-backend -- alembic upgrade head

# Seed directory roles
kubectl exec -n menshun-pam deployment/menshun-backend -- python -m app.scripts.seed_roles

# Create admin user
kubectl exec -n menshun-pam deployment/menshun-backend -- python -m app.scripts.create_admin_user
```

### Manual Installation

For environments where containers are not available.

#### 1. System Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm postgresql-15 redis-server nginx

# CentOS/RHEL
sudo yum install -y python3.11 python3-pip nodejs npm postgresql15-server redis nginx
```

#### 2. Backend Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash menshun
sudo su - menshun

# Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit .env with your configuration

# Initialize database
alembic upgrade head
python -m app.scripts.seed_roles

# Create systemd service
sudo tee /etc/systemd/system/menshun-backend.service << EOF
[Unit]
Description=Menshun PAM Backend
After=network.target

[Service]
Type=exec
User=menshun
Group=menshun
WorkingDirectory=/home/menshun/menshun/backend
Environment=PATH=/home/menshun/menshun/venv/bin
ExecStart=/home/menshun/menshun/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable menshun-backend
sudo systemctl start menshun-backend
```

#### 3. Frontend Setup

```bash
# Build frontend
cd frontend
npm ci
npm run build

# Configure nginx
sudo tee /etc/nginx/sites-available/menshun << EOF
server {
    listen 80;
    server_name pam.yourcompany.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name pam.yourcompany.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    root /home/menshun/menshun/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/menshun /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ⚙️ Post-Deployment Configuration

### 1. Create Administrator Account

```bash
# Docker Compose
docker-compose exec backend python -m app.scripts.create_admin_user

# Kubernetes
kubectl exec -n menshun-pam deployment/menshun-backend -- python -m app.scripts.create_admin_user

# Manual
cd backend && python -m app.scripts.create_admin_user
```

### 2. Configure Notifications

Update your `.env` file with SMTP settings:

```bash
SMTP_HOST=smtp.yourcompany.com
SMTP_PORT=587
SMTP_USER=noreply@yourcompany.com
SMTP_PASSWORD=your_smtp_password
SMTP_FROM="Menshun PAM <noreply@yourcompany.com>"
```

### 3. Setup Backup Strategy

```bash
# Database backup script
cat > /opt/menshun/backup-database.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/menshun/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/pamdb_backup_$DATE.sql"

mkdir -p $BACKUP_DIR
docker-compose exec -T database pg_dump -U pamuser -d pamdb > $BACKUP_FILE
gzip $BACKUP_FILE

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
EOF

chmod +x /opt/menshun/backup-database.sh

# Schedule daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/menshun/backup-database.sh") | crontab -
```

### 4. Configure Log Rotation

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/menshun << EOF
/opt/menshun/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose -f /opt/menshun/docker-compose.prod.yml restart backend frontend
    endscript
}
EOF
```

---

## 📊 Monitoring & Maintenance

### Built-in Monitoring

The deployment includes Prometheus and Grafana for monitoring:

- **Prometheus**: http://your-domain:9090
- **Grafana**: https://monitoring.yourcompany.com
  - Default login: admin / (password from .env)

### Health Checks

```bash
# Check service health
curl https://api.yourcompany.com/health
curl https://api.yourcompany.com/health/ready
curl https://api.yourcompany.com/health/live

# Check all services
docker-compose ps
kubectl get pods -n menshun-pam
```

### Performance Monitoring

```bash
# Database performance
docker-compose exec database psql -U pamuser -d pamdb -c "
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats 
ORDER BY schemaname,tablename,attname;"

# Application metrics
curl https://api.yourcompany.com/metrics

# System resources
docker stats
kubectl top pods -n menshun-pam
```

### Log Management

```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Search logs
docker-compose logs backend | grep ERROR
kubectl logs -n menshun-pam deployment/menshun-backend | grep WARNING

# Export logs to external system
# Configure rsyslog or fluentd for centralized logging
```

---

## 🔒 Security Hardening

### 1. Network Security

```bash
# Configure firewall (UFW example)
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Configure fail2ban
sudo apt install fail2ban
sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
EOF

sudo systemctl restart fail2ban
```

### 2. Application Security

```bash
# Update all dependencies regularly
docker-compose pull
docker-compose up -d

# Run security scans
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image menshun-backend:latest

# Check for vulnerabilities
npm audit --audit-level=high
pip-audit
```

### 3. Database Security

```bash
# Regular security updates
docker-compose exec database psql -U pamuser -d pamdb -c "
UPDATE pg_settings SET setting = 'on' WHERE name = 'log_statement';
UPDATE pg_settings SET setting = 'all' WHERE name = 'log_min_duration_statement';"

# Enable SSL connections only
# Add to postgresql.conf:
# ssl = on
# ssl_cert_file = 'server.crt'
# ssl_key_file = 'server.key'
```

### 4. Backup Security

```bash
# Encrypt backups
gpg --cipher-algo AES256 --compress-algo 1 --s2k-mode 3 \
    --s2k-digest-algo SHA512 --s2k-count 65536 --symmetric \
    --output backup.sql.gpg backup.sql

# Test backup restoration
docker run --rm -v /opt/menshun/backups:/backups postgres:15-alpine \
  psql -h database -U pamuser -d pamdb_test < /backups/latest_backup.sql
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Azure AD Authentication Fails

**Symptoms:** Users can't log in, "Invalid client" errors

**Solutions:**
```bash
# Check app registration settings
az ad app show --id $AZURE_CLIENT_ID

# Verify redirect URIs
# Ensure client secret hasn't expired
# Check API permissions are granted

# Test token acquisition
curl -X POST "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$AZURE_CLIENT_ID&client_secret=$AZURE_CLIENT_SECRET&scope=https://graph.microsoft.com/.default&grant_type=client_credentials"
```

#### 2. Database Connection Issues

**Symptoms:** "Connection refused", "Password authentication failed"

**Solutions:**
```bash
# Check database status
docker-compose ps database
kubectl get pods -n menshun-pam

# Test database connection
docker-compose exec database psql -U pamuser -d pamdb -c "SELECT version();"

# Check logs
docker-compose logs database
kubectl logs -n menshun-pam statefulset/postgresql

# Reset database password
docker-compose exec database psql -U postgres -c "ALTER USER pamuser PASSWORD 'newpassword';"
```

#### 3. Frontend Build Failures

**Symptoms:** White screen, "Failed to fetch" errors

**Solutions:**
```bash
# Check build logs
docker-compose logs frontend

# Verify environment variables
docker-compose exec frontend env | grep VITE_

# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend

# Check API connectivity
curl https://api.yourcompany.com/health
```

#### 4. SSL Certificate Issues

**Symptoms:** "Certificate not trusted", "SSL handshake failed"

**Solutions:**
```bash
# Check certificate validity
openssl x509 -in certificate.crt -text -noout

# Test SSL connection
openssl s_client -connect pam.yourcompany.com:443

# Renew Let's Encrypt certificate
docker-compose exec traefik traefik version
# Check Traefik logs for ACME errors

# Manual certificate renewal
certbot renew --dry-run
```

#### 5. Performance Issues

**Symptoms:** Slow page loads, API timeouts

**Solutions:**
```bash
# Check resource usage
docker stats
kubectl top pods -n menshun-pam

# Database performance
docker-compose exec database psql -U pamuser -d pamdb -c "
SELECT query, mean_time, calls FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;"

# Application profiling
docker-compose exec backend python -m cProfile -o profile.stats app.main

# Scale services
docker-compose up -d --scale backend=3
kubectl scale deployment menshun-backend --replicas=3 -n menshun-pam
```

### Log Locations

```bash
# Docker Compose
/opt/menshun/logs/

# Kubernetes
kubectl logs -n menshun-pam deployment/menshun-backend
kubectl logs -n menshun-pam deployment/menshun-frontend

# Manual installation
/var/log/menshun/
/var/log/nginx/
/var/log/postgresql/
```

### Support Resources

- **Documentation**: https://docs.menshun.com
- **Issue Tracker**: https://github.com/yourusername/menshun/issues
- **Security Issues**: security@menshun.com
- **Community Forum**: https://community.menshun.com

### Emergency Procedures

#### 1. Emergency Shutdown

```bash
# Docker Compose
docker-compose down

# Kubernetes
kubectl scale deployment --replicas=0 -n menshun-pam --all

# Manual
sudo systemctl stop menshun-backend nginx postgresql redis
```

#### 2. Disaster Recovery

```bash
# Restore from backup
gunzip /opt/menshun/backups/latest_backup.sql.gz
docker-compose exec -T database psql -U pamuser -d pamdb < latest_backup.sql

# Rebuild from scratch
git pull origin main
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

#### 3. Security Incident Response

```bash
# Immediate actions
# 1. Isolate affected systems
docker-compose down
kubectl scale deployment --replicas=0 -n menshun-pam --all

# 2. Preserve evidence
docker-compose logs > incident_logs_$(date +%Y%m%d_%H%M%S).txt
kubectl logs -n menshun-pam --all-containers=true > k8s_incident_logs_$(date +%Y%m%d_%H%M%S).txt

# 3. Reset all credentials
# Change all passwords in .env
# Rotate Azure AD client secrets
# Update database passwords
```

---

This deployment guide provides comprehensive instructions for deploying Menshun PAM in various environments. Choose the deployment method that best fits your infrastructure requirements and security policies.