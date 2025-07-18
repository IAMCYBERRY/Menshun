#!/bin/bash

# Menshun PAM - One-Click Installation Script for Ubuntu Server
# This script automates the installation of Menshun PAM on Ubuntu Server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_NAME="Menshun PAM Installer"
SCRIPT_VERSION="1.0.0"
REPO_URL="https://github.com/IAMCYBERRY/Menshun.git"
INSTALL_DIR="/opt/menshun"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "============================================"
    echo "🚀 $SCRIPT_NAME v$SCRIPT_VERSION"
    echo "============================================"
    echo -e "${NC}"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        echo "Please run as a regular user with sudo privileges"
        exit 1
    fi
}

# Function to check Ubuntu version
check_ubuntu_version() {
    print_status "Checking Ubuntu version..."
    
    if [[ ! -f /etc/lsb-release ]]; then
        print_error "This script only supports Ubuntu"
        exit 1
    fi
    
    source /etc/lsb-release
    
    if [[ "$DISTRIB_ID" != "Ubuntu" ]]; then
        print_error "This script only supports Ubuntu"
        exit 1
    fi
    
    major_version=$(echo "$DISTRIB_RELEASE" | cut -d. -f1)
    
    if [[ $major_version -lt 20 ]]; then
        print_error "Ubuntu 20.04 or later is required"
        exit 1
    fi
    
    print_success "Ubuntu $DISTRIB_RELEASE detected"
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check CPU cores
    cpu_cores=$(nproc)
    if [[ $cpu_cores -lt 2 ]]; then
        print_warning "Only $cpu_cores CPU cores detected. 4+ cores recommended."
    else
        print_success "CPU cores: $cpu_cores"
    fi
    
    # Check RAM
    ram_gb=$(free -g | awk '/^Mem:/{print $2}')
    if [[ $ram_gb -lt 4 ]]; then
        print_warning "Only ${ram_gb}GB RAM detected. 8GB+ recommended."
    else
        print_success "RAM: ${ram_gb}GB"
    fi
    
    # Check disk space
    disk_space=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [[ $disk_space -lt 50 ]]; then
        print_warning "Only ${disk_space}GB disk space available. 50GB+ recommended."
    else
        print_success "Disk space: ${disk_space}GB available"
    fi
}

# Function to update system
update_system() {
    print_status "Updating system packages..."
    sudo apt update -qq
    sudo apt upgrade -y -qq
    print_success "System updated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install essential packages
    sudo apt install -y -qq curl wget git make unzip
    
    # Install Docker
    if ! command -v docker &> /dev/null; then
        print_status "Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        print_success "Docker installed"
    else
        print_success "Docker already installed"
    fi
    
    # Install Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_status "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        print_success "Docker Compose installed"
    else
        print_success "Docker Compose already installed"
    fi
}

# Function to configure firewall
configure_firewall() {
    print_status "Configuring firewall..."
    
    # Install UFW if not present
    if ! command -v ufw &> /dev/null; then
        sudo apt install -y -qq ufw
    fi
    
    # Configure UFW
    sudo ufw --force enable
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    
    print_success "Firewall configured"
}

# Function to clone repository
clone_repository() {
    print_status "Cloning Menshun PAM repository..."
    
    # Create install directory
    sudo mkdir -p $INSTALL_DIR
    sudo chown $USER:$USER $INSTALL_DIR
    
    # Clone repository
    git clone $REPO_URL $INSTALL_DIR
    cd $INSTALL_DIR
    
    print_success "Repository cloned to $INSTALL_DIR"
}

# Function to get deployment type
get_deployment_type() {
    echo -e "${BLUE}Select deployment type:${NC}"
    echo "1) Development (recommended for testing)"
    echo "2) Production (for live environments)"
    echo ""
    
    while true; do
        read -p "Enter your choice (1 or 2): " choice
        case $choice in
            1)
                DEPLOYMENT_TYPE="development"
                break
                ;;
            2)
                DEPLOYMENT_TYPE="production"
                break
                ;;
            *)
                print_error "Invalid choice. Please enter 1 or 2."
                ;;
        esac
    done
    
    print_success "Deployment type: $DEPLOYMENT_TYPE"
}

# Function to collect Azure AD information
collect_azure_info() {
    print_status "Azure AD configuration is required for Menshun PAM"
    echo ""
    echo "You need to create an Azure AD app registration first."
    echo "Visit: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
    echo ""
    
    read -p "Do you have an Azure AD app registration ready? (y/n): " azure_ready
    
    if [[ $azure_ready != "y" && $azure_ready != "Y" ]]; then
        print_warning "Please create an Azure AD app registration first"
        echo ""
        echo "Required steps:"
        echo "1. Go to Azure Portal → Azure Active Directory → App registrations"
        echo "2. Create new registration with name 'Menshun PAM System'"
        echo "3. Add API permissions: Directory.Read.All, Directory.ReadWrite.All, User.Read.All, RoleManagement.Read.All, RoleManagement.ReadWrite.Directory"
        echo "4. Grant admin consent"
        echo "5. Create client secret"
        echo "6. Note down: Client ID, Client Secret, Tenant ID"
        echo ""
        echo "Run this script again when ready."
        exit 0
    fi
    
    echo ""
    print_status "Please provide your Azure AD credentials:"
    
    read -p "Azure Client ID: " AZURE_CLIENT_ID
    read -s -p "Azure Client Secret: " AZURE_CLIENT_SECRET
    echo ""
    read -p "Azure Tenant ID: " AZURE_TENANT_ID
    
    if [[ -z "$AZURE_CLIENT_ID" || -z "$AZURE_CLIENT_SECRET" || -z "$AZURE_TENANT_ID" ]]; then
        print_error "All Azure AD credentials are required"
        exit 1
    fi
    
    print_success "Azure AD credentials collected"
}

# Function to collect domain information
collect_domain_info() {
    if [[ "$DEPLOYMENT_TYPE" == "production" ]]; then
        echo ""
        read -p "Enter your domain name (e.g., pam.yourcompany.com): " DOMAIN_NAME
        
        if [[ -z "$DOMAIN_NAME" ]]; then
            print_error "Domain name is required for production deployment"
            exit 1
        fi
        
        print_success "Domain: $DOMAIN_NAME"
    else
        DOMAIN_NAME="localhost"
    fi
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment configuration..."
    
    # Copy environment template
    cp .env.example .env
    
    # Update environment variables
    if [[ "$DEPLOYMENT_TYPE" == "production" ]]; then
        sed -i "s/ENVIRONMENT=development/ENVIRONMENT=production/" .env
        sed -i "s/DEBUG=true/DEBUG=false/" .env
        sed -i "s/localhost:3000/$DOMAIN_NAME/" .env
        sed -i "s/DOMAIN=localhost/DOMAIN=$DOMAIN_NAME/" .env
    fi
    
    # Update Azure AD configuration
    sed -i "s/AZURE_CLIENT_ID=.*/AZURE_CLIENT_ID=$AZURE_CLIENT_ID/" .env
    sed -i "s/AZURE_CLIENT_SECRET=.*/AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET/" .env
    sed -i "s/AZURE_TENANT_ID=.*/AZURE_TENANT_ID=$AZURE_TENANT_ID/" .env
    
    # Generate secure secrets
    SECRET_KEY=$(openssl rand -hex 32)
    ENCRYPTION_KEY=$(openssl rand -hex 32)
    POSTGRES_PASSWORD=$(openssl rand -base64 32)
    
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    sed -i "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" .env
    sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" .env
    
    # Copy frontend environment
    cp frontend/.env.example frontend/.env
    
    print_success "Environment configured"
}

# Function to deploy application
deploy_application() {
    print_status "Deploying Menshun PAM..."
    
    # Check if user is in docker group
    if ! groups $USER | grep -q docker; then
        print_status "Adding user to docker group..."
        sudo usermod -aG docker $USER
        print_warning "You need to log out and log back in for docker group changes to take effect"
        print_warning "After logging back in, run: cd $INSTALL_DIR && make init"
        exit 0
    fi
    
    # Deploy using Make
    if [[ "$DEPLOYMENT_TYPE" == "production" ]]; then
        make init-prod
    else
        make init
    fi
    
    print_success "Application deployed successfully"
}

# Function to show post-installation information
show_post_install_info() {
    print_success "🎉 Menshun PAM installation completed!"
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}Installation Summary${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
    echo "📍 Installation directory: $INSTALL_DIR"
    echo "🔧 Deployment type: $DEPLOYMENT_TYPE"
    echo "🌐 Domain: $DOMAIN_NAME"
    echo ""
    
    if [[ "$DEPLOYMENT_TYPE" == "production" ]]; then
        echo -e "${BLUE}Access URLs:${NC}"
        echo "• Frontend: https://$DOMAIN_NAME"
        echo "• Backend API: https://$DOMAIN_NAME/api"
        echo "• API Documentation: https://$DOMAIN_NAME/api/docs"
        echo ""
        echo -e "${YELLOW}⚠️  Important Production Notes:${NC}"
        echo "• Configure your domain DNS to point to this server"
        echo "• Replace self-signed SSL certificates with proper certificates"
        echo "• Configure automatic database backups"
        echo "• Set up monitoring and alerting"
    else
        echo -e "${BLUE}Access URLs:${NC}"
        echo "• Frontend: http://localhost:3000"
        echo "• Backend API: http://localhost:8000"
        echo "• API Documentation: http://localhost:8000/docs"
    fi
    
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Open the frontend URL in your browser"
    echo "2. Complete the guided setup wizard"
    echo "3. Configure your Azure AD integration"
    echo "4. Start managing privileged access!"
    echo ""
    echo -e "${BLUE}Useful Commands:${NC}"
    echo "• cd $INSTALL_DIR && make help    - Show all available commands"
    echo "• cd $INSTALL_DIR && make logs    - View application logs"
    echo "• cd $INSTALL_DIR && make status  - Check service status"
    echo "• cd $INSTALL_DIR && make stop    - Stop all services"
    echo ""
    echo -e "${GREEN}🎯 The guided setup wizard will handle all remaining configuration through the web interface!${NC}"
}

# Function to handle script interruption
cleanup() {
    print_warning "Installation interrupted"
    exit 1
}

# Main installation function
main() {
    # Set up signal handlers
    trap cleanup SIGINT SIGTERM
    
    # Print header
    print_header
    
    # Check if running as root
    check_root
    
    # Check Ubuntu version
    check_ubuntu_version
    
    # Check system requirements
    check_requirements
    
    # Get deployment type
    get_deployment_type
    
    # Collect Azure AD information
    collect_azure_info
    
    # Collect domain information
    collect_domain_info
    
    # Confirm installation
    echo ""
    print_status "Ready to install Menshun PAM with the following configuration:"
    echo "• Deployment type: $DEPLOYMENT_TYPE"
    echo "• Domain: $DOMAIN_NAME"
    echo "• Installation directory: $INSTALL_DIR"
    echo ""
    
    read -p "Continue with installation? (y/n): " continue_install
    
    if [[ $continue_install != "y" && $continue_install != "Y" ]]; then
        print_status "Installation cancelled"
        exit 0
    fi
    
    # Start installation
    print_status "Starting installation process..."
    
    # Update system
    update_system
    
    # Install dependencies
    install_dependencies
    
    # Configure firewall
    configure_firewall
    
    # Clone repository
    clone_repository
    
    # Setup environment
    setup_environment
    
    # Deploy application
    deploy_application
    
    # Show post-installation information
    show_post_install_info
}

# Run main function
main "$@"