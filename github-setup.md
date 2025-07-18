# 🚀 GitHub Repository Setup Guide

## Create GitHub Repository

### Option 1: GitHub CLI (Recommended)
```bash
# Install GitHub CLI if not already installed
# macOS: brew install gh
# Windows: winget install --id GitHub.cli
# Linux: https://cli.github.com/manual/installation

# Authenticate with GitHub
gh auth login

# Create repository (choose public or private)
gh repo create menshun-pam --public --description "Enterprise Privileged Access Management for Microsoft Entra ID"

# Add remote and push
git remote add origin https://github.com/yourusername/menshun-pam.git
git branch -M main
git push -u origin main
```

### Option 2: GitHub Web Interface
1. Go to https://github.com/new
2. Repository name: `menshun-pam`
3. Description: `Enterprise Privileged Access Management for Microsoft Entra ID`
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

Then run these commands:
```bash
git remote add origin https://github.com/yourusername/menshun-pam.git
git branch -M main
git push -u origin main
```

## Repository Configuration

After pushing, configure your repository:

### 1. Branch Protection Rules
1. Go to Settings → Branches
2. Add branch protection rule for `main`:
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require review from code owners
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
   - ✅ Include administrators

### 2. Enable Security Features
1. Go to Settings → Security & analysis
2. Enable:
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Code scanning alerts
   - ✅ Secret scanning alerts

### 3. Repository Secrets
1. Go to Settings → Secrets and variables → Actions
2. Add these secrets for CI/CD:

**Repository Secrets:**
```
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AZURE_TENANT_ID=your_azure_tenant_id
DOCKER_HUB_USERNAME=your_dockerhub_username
DOCKER_HUB_TOKEN=your_dockerhub_token
```

### 4. Enable GitHub Pages (Optional)
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs` folder
4. This will host documentation at `https://yourusername.github.io/menshun-pam`

### 5. Repository Topics
Add these topics to help with discoverability:
```
privileged-access-management
azure-ad
enterprise-security
fastapi
react
typescript
docker
kubernetes
compliance
audit-logging
```

## Team Collaboration Setup

### 1. Add Collaborators
1. Go to Settings → Collaborators and teams
2. Add team members with appropriate permissions:
   - **Admin**: Repository owners, DevOps engineers
   - **Write**: Developers, contributors
   - **Read**: Security team, auditors

### 2. Code Owners
The `.github/CODEOWNERS` file is already configured to require reviews from:
- Security team for authentication/authorization changes
- DevOps team for deployment configurations
- Frontend team for UI changes
- Backend team for API changes

### 3. Issue Labels
GitHub will automatically create labels from the issue templates. You can add custom labels:
```
priority: critical
priority: high
priority: medium
priority: low
type: security
type: performance
type: documentation
component: frontend
component: backend
component: database
component: deployment
```

## Development Workflow

### 1. Local Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/menshun-pam.git
cd menshun-pam

# Setup environment
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit .env files with your configuration

# Start development environment
docker-compose up -d
```

### 2. Contributing Process
1. **Create Issue**: Use issue templates for bugs/features
2. **Create Branch**: `git checkout -b feature/description`
3. **Develop**: Make changes following coding standards
4. **Test**: Run tests locally (`make test`)
5. **Commit**: Use conventional commit messages
6. **Push**: `git push origin feature/description`
7. **Pull Request**: Use PR template, request reviews
8. **Merge**: After approval and CI passes

### 3. Release Process
```bash
# Create release branch
git checkout -b release/v1.1.0

# Update version numbers
# - backend/app/__init__.py
# - frontend/package.json
# - README.md

# Commit changes
git commit -m "chore: bump version to v1.1.0"

# Create pull request to main
# After merge, create GitHub release
gh release create v1.1.0 --generate-notes
```

## Deployment Integration

### 1. Docker Hub Integration
The CI/CD pipeline will automatically:
- Build Docker images on every push
- Push to Docker Hub with tags
- Deploy to staging environment

### 2. Azure Container Registry
For Azure deployments:
```bash
# Add Azure secrets to GitHub
az ad sp create-for-rbac --name "github-actions" --sdk-auth
# Add output as AZURE_CREDENTIALS secret
```

### 3. Kubernetes Deployment
```bash
# Add Kubernetes config as secret
cat ~/.kube/config | base64
# Add as K8S_CONFIG secret in GitHub
```

## Monitoring and Maintenance

### 1. Security Monitoring
- Dependabot will create PRs for security updates
- CodeQL scanning will run on every PR
- Secret scanning alerts for exposed credentials

### 2. Performance Monitoring
- GitHub Actions will run performance tests
- Lighthouse CI for frontend performance
- Load testing for API endpoints

### 3. Documentation Updates
- README badges will show build status
- API docs auto-deployed with each release
- Changelog generated from conventional commits

## Getting Started Commands

After creating the repository, run these commands:

```bash
# Navigate to your project
cd /Users/ryanwright/Desktop/Menshun

# Add remote and push (replace with your username)
git remote add origin https://github.com/yourusername/menshun-pam.git
git push -u origin main

# Verify everything is pushed
git status
git log --oneline
```

Your Menshun PAM system is now ready for enterprise development and deployment! 🚀