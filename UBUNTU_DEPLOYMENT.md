# 🚀 Ubuntu Server Deployment - Simplified with `make init`

This guide shows how to deploy Menshun PAM to Ubuntu Server using the simplified `make init` command.

## Prerequisites

- Ubuntu Server 20.04 LTS or 22.04 LTS
- 4+ CPU cores, 8GB+ RAM, 50GB+ SSD storage
- Static IP address and domain name
- Root or sudo access

## Quick Start (5 Minutes)

### 1. Install Required Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git make

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for Docker group membership
logout
```

### 2. Clone and Initialize

```bash
# Clone the repository
git clone https://github.com/IAMCYBERRY/Menshun.git
cd Menshun

# Initialize development environment
make init

# OR for production
make init-prod
```

### 3. Configure Azure AD (Required)

Before the application can work, you need to configure Azure AD integration:

#### Create Azure AD App Registration

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create app registration
az ad app create \
  --display-name "Menshun PAM System" \
  --web-redirect-uris "https://your-domain.com" \
  --sign-in-audience "AzureADMyOrg"

# Note the appId from output
```

#### Configure App Permissions

1. Go to **Azure Portal** → **Azure Active Directory** → **App registrations**
2. Find "Menshun PAM System" app
3. **API permissions** → **Add permission** → **Microsoft Graph**
4. Add these **Application permissions**:
   - `Directory.Read.All`
   - `Directory.ReadWrite.All`
   - `User.Read.All`
   - `RoleManagement.Read.All`
   - `RoleManagement.ReadWrite.Directory`
5. **Grant admin consent** for your organization

#### Create Client Secret

```bash
# Create client secret
az ad app credential reset --id <YOUR_APP_ID> --years 2
# Save the password output
```

### 4. Update Configuration

```bash
# Edit the .env file with your Azure AD credentials
nano .env

# Update these values:
# AZURE_CLIENT_ID=your_app_id_here
# AZURE_CLIENT_SECRET=your_client_secret_here
# AZURE_TENANT_ID=your_tenant_id_here
# DOMAIN=your-domain.com (for production)
```

### 5. Access the Application

**Development:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Production:**
- Frontend: https://your-domain.com
- Backend: https://your-domain.com/api
- API Docs: https://your-domain.com/api/docs

### 6. Complete Setup Wizard

1. Open the application in your browser
2. The **guided setup wizard** will automatically appear
3. Follow the step-by-step configuration:
   - **Welcome**: System requirements check
   - **Azure AD**: Test your credentials
   - **Organization**: Company details
   - **Security**: Security policies
   - **Compliance**: Compliance frameworks
   - **Notifications**: Email settings (optional)
   - **Review**: Final configuration review

## Available Commands

```bash
# View all available commands
make help

# Development commands
make init          # Initialize development environment
make dev           # Start with hot reload
make logs          # View application logs
make health        # Check application health
make status        # Show service status
make stop          # Stop all services

# Production commands
make init-prod     # Initialize production environment
make logs-prod     # View production logs
make health-prod   # Check production health
make restart-prod  # Restart production services
make update-prod   # Update production deployment

# Database commands
make backup-db     # Create database backup
make migrate       # Run database migrations
make db-shell      # Access database shell

# Maintenance commands
make update        # Update application
make clean         # Clean up Docker resources
make reset         # Reset everything (destroys data)

# Security commands
make generate-secrets    # Generate secure secrets
make check-security     # Run security checks

# Information commands
make info          # Show deployment information
make version       # Show version information
```

## Production Deployment

### 1. Initialize Production Environment

```bash
# Initialize production environment
make init-prod

# The script will:
# ✅ Check system requirements
# ✅ Create required directories
# ✅ Setup production .env file
# ✅ Build Docker images
# ✅ Start production services
# ✅ Initialize database
# ✅ Setup SSL certificates
# ✅ Show next steps
```

### 2. Configure SSL Certificates

The script creates self-signed certificates for testing. For production:

```bash
# Option 1: Let's Encrypt (recommended)
sudo apt install -y certbot
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to the application
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/certificates/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/certificates/key.pem
sudo chown $USER:$USER ssl/certificates/*.pem

# Option 2: Commercial certificates
# Copy your certificates to:
# ssl/certificates/cert.pem
# ssl/certificates/key.pem
```

### 3. Setup Firewall

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw status
```

### 4. Configure Automatic Backups

```bash
# Create daily database backups
make backup-db

# Schedule automatic backups
(crontab -l 2>/dev/null; echo "0 2 * * * cd /path/to/Menshun && make backup-db") | crontab -
```

## Environment Variables

### Required Variables

```bash
# Azure AD Configuration
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret  
AZURE_TENANT_ID=your_tenant_id

# Application Configuration
DOMAIN=your-domain.com
ENVIRONMENT=production
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# Database Configuration
POSTGRES_PASSWORD=your_db_password
```

### Optional Variables

```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Redis Configuration
REDIS_PASSWORD=your_redis_password
```

### Generate Secure Secrets

```bash
# Generate secure secrets for .env file
make generate-secrets

# Output example:
# SECRET_KEY=a1b2c3d4e5f6...
# ENCRYPTION_KEY=f6e5d4c3b2a1...
# POSTGRES_PASSWORD=randompassword123
# REDIS_PASSWORD=anotherpassword456
```

## Monitoring & Maintenance

### Health Checks

```bash
# Check application health
make health

# Check production health
make health-prod

# View service status
make status
```

### Log Management

```bash
# View application logs
make logs

# View production logs
make logs-prod

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### Updates

```bash
# Update development environment
make update

# Update production environment
make update-prod
```

## Troubleshooting

### Common Issues

1. **Docker permission denied**
   ```bash
   sudo usermod -aG docker $USER
   logout  # Then login again
   ```

2. **Port already in use**
   ```bash
   sudo netstat -tulnp | grep :80
   sudo systemctl stop nginx  # or apache2
   ```

3. **Database connection failed**
   ```bash
   make logs | grep database
   make restart
   ```

4. **Azure AD authentication failed**
   ```bash
   # Check your app registration settings
   # Verify client secret hasn't expired
   # Ensure API permissions are granted
   ```

### Emergency Procedures

```bash
# Emergency stop
make stop

# Reset everything (destroys data)
make reset

# Clean up Docker resources
make clean
```

## Support

- **Documentation**: Check the main [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- **Issues**: Report issues at https://github.com/IAMCYBERRY/Menshun/issues
- **Health Checks**: Use `make health` to diagnose problems
- **Logs**: Use `make logs` to view application logs

## What's Next?

After deployment:

1. **Complete the guided setup wizard** in your browser
2. **Configure your first privileged users**
3. **Set up automated access reviews**
4. **Configure compliance reporting**
5. **Monitor privileged access activities**

The guided setup wizard eliminates the need for manual configuration files - everything is done through the web interface! 🎉