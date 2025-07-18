# Menshun - Enterprise Privileged Access Management

<div align="center">
  <img src="docs/assets/menshun-logo.png" alt="Menshun Logo" width="200"/>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
  [![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
  [![CI/CD](https://github.com/your-org/menshun/workflows/CI/badge.svg)](https://github.com/your-org/menshun/actions)
  [![Security Scan](https://github.com/your-org/menshun/workflows/Security%20Scan/badge.svg)](https://github.com/your-org/menshun/actions)
  [![Code Coverage](https://codecov.io/gh/your-org/menshun/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/menshun)
</div>

## Overview

**Menshun** is a comprehensive, cloud-native Privileged Access Management (PAM) solution designed for Microsoft Entra ID environments. Built with modern security practices, it features automated privileged user creation, service identity management, and secure credential vaulting with automatic rotation.

*The name "Menshun" reflects our commitment to providing mention-worthy security and access management that enterprises can trust.*

### 🔑 Key Features

- 🔐 **Privileged User Management**: Automated creation with search-first workflow
- 🤖 **Service Identity Management**: Support for Service Principals, Managed Identities, and Workload Identities  
- 🔑 **Credential Vaulting**: Secure storage with automatic rotation
- 👥 **Complete Role Management**: All 130+ Entra ID directory roles
- 📊 **Real-time Monitoring**: Comprehensive audit trails and analytics
- 🎨 **Modern UI**: Solo Leveling-inspired dark theme with glass-morphism effects
- 🛡️ **Enterprise Security**: SOX, SOC 2, ISO 27001, and GDPR compliance features

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure AD Application Registration with appropriate permissions
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

# Initialize database
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m app.scripts.seed_roles

# Access Menshun
open http://localhost:3000
```

## 🏗️ Architecture

### Technology Stack

**Backend**:
- FastAPI (Python 3.11+) with comprehensive API documentation
- PostgreSQL 15 with SQLAlchemy ORM
- Redis 7 for caching and background jobs
- Celery for async task processing
- Microsoft Graph SDK for Azure AD integration

**Frontend**:
- React 18 + TypeScript with strict type checking
- Vite build tool for optimal performance
- TailwindCSS for responsive design
- React Query for state management
- Comprehensive component documentation with Storybook

**Infrastructure**:
- Docker containers with multi-stage builds
- GitHub Actions CI/CD with security scanning
- Automated testing with coverage reporting
- Pre-commit hooks for code quality

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

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [🚀 Quick Start](docs/quickstart.md) | Get up and running in minutes |
| [🏗️ Development Setup](docs/development/development-setup.md) | Developer environment configuration |
| [🐳 Deployment Guide](docs/deployment/deployment-guide.md) | Production deployment instructions |
| [👤 User Guide](docs/user-guides/getting-started.md) | End-user documentation |
| [⚙️ Admin Guide](docs/administration/admin-guide.md) | Platform administration |
| [🔗 API Reference](docs/api/api-reference.md) | Complete API documentation |
| [🛡️ Security](docs/security/security-controls.md) | Security implementation details |
| [🤝 Contributing](CONTRIBUTING.md) | Development guidelines and contribution process |

## 🔐 Security & Compliance

### Security Features

- ✅ **Zero-Knowledge Access**: Secure credential retrieval patterns
- ✅ **Multi-Factor Authentication**: Required for privileged operations  
- ✅ **Audit Logging**: Immutable audit trails with integrity checking
- ✅ **Role-Based Access Control**: Granular permissions
- ✅ **Encryption**: At rest and in transit (TLS 1.3)
- ✅ **Security Scanning**: Automated vulnerability detection
- ✅ **Supply Chain Security**: Dependency scanning with Dependabot

### Compliance Standards

- **SOX**: Audit trails and separation of duties
- **SOC 2**: Security controls and monitoring  
- **ISO 27001**: Information security management
- **GDPR**: Data protection and privacy controls

## 🛠️ Development

### Getting Started

```bash
# Clone and setup development environment
git clone https://github.com/your-org/menshun.git
cd menshun

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run tests
make test

# Run linting
make lint

# View coverage report
make coverage
```

### Code Quality Standards

- **Python**: Black formatting, flake8 linting, mypy type checking
- **TypeScript**: ESLint with strict rules, Prettier formatting
- **Testing**: 90%+ code coverage requirement
- **Documentation**: Comprehensive docstrings and API docs
- **Security**: Automated security scanning in CI/CD

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development setup and workflow
- Code standards and best practices  
- Testing requirements
- Pull request process
- Security guidelines

## 📈 Project Status

- ✅ **Phase 1**: Core Infrastructure (Complete)
- 🚧 **Phase 2**: Privileged User Management (In Progress)
- ⏳ **Phase 3**: Service Identity Management (Planned)
- ⏳ **Phase 4**: Credential Vaulting (Planned)
- ⏳ **Phase 5**: Advanced Features (Planned)

## 🆘 Support

### Getting Help

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-org/menshun/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-org/menshun/discussions)
- 📧 **Enterprise Support**: support@yourcompany.com

### Community

- 💬 [Discord Server](https://discord.gg/menshun)
- 🐦 [Twitter Updates](https://twitter.com/menshun_pam)
- 📝 [Blog](https://blog.menshun.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Graph SDK team for excellent API support
- Solo Leveling for design inspiration  
- FastAPI and React communities for amazing frameworks
- Open source security tools that make this project possible

---

<div align="center">
  <strong>Menshun</strong> - Secure. Scalable. Simple. <em>Mention-worthy.</em>
  <br><br>
  Made with ❤️ by the Security Engineering Team
</div>