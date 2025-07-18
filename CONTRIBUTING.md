# Contributing to Menshun

Thank you for your interest in contributing to Menshun! This document provides guidelines and best practices for contributing to our enterprise PAM solution.

## 🚀 Quick Start for Contributors

1. **Fork the repository** and clone your fork
2. **Set up the development environment** (see [Development Setup](docs/development/development-setup.md))
3. **Create a feature branch** from `develop`
4. **Make your changes** following our code standards
5. **Write tests** for your changes
6. **Submit a pull request**

## 🔄 Development Workflow

### Branch Strategy

We use Git Flow with the following branches:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature development
- `hotfix/*`: Critical production fixes
- `release/*`: Release preparation

### Workflow Steps

```bash
# 1. Clone and setup
git clone https://github.com/your-username/menshun.git
cd menshun
git remote add upstream https://github.com/original-org/menshun.git

# 2. Create feature branch
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature description"

# 4. Push and create PR
git push origin feature/your-feature-name
# Create PR via GitHub UI
```

## 📝 Code Standards

### Python (Backend)

#### Code Formatting
- **Black**: Auto-formatting with line length 88
- **isort**: Import sorting
- **flake8**: Linting with max line length 127
- **mypy**: Type checking (strict mode)

```bash
# Format code
black app/
isort app/
flake8 app/
mypy app/
```

#### Documentation Standards
```python
def create_privileged_user(
    source_user_id: str, 
    selected_roles: List[str],
    tap_settings: TAPSettings
) -> PrivilegedUserResponse:
    """
    Create a privileged user account with specified roles.
    
    This function creates a new privileged user account based on an existing
    source user, assigns the specified directory roles, and generates a 
    Temporary Access Pass (TAP) for initial authentication.
    
    Args:
        source_user_id: UUID of the source user in Azure AD
        selected_roles: List of directory role template IDs to assign
        tap_settings: Configuration for TAP generation (lifetime, usage)
    
    Returns:
        PrivilegedUserResponse containing created user details and TAP
    
    Raises:
        UserNotFoundError: If source user doesn't exist in Azure AD
        RoleAssignmentError: If role assignment fails
        TAPGenerationError: If TAP creation fails
        
    Example:
        >>> user_response = create_privileged_user(
        ...     source_user_id="123e4567-e89b-12d3-a456-426614174000",
        ...     selected_roles=["62e90394-69f5-4237-9190-012177145e10"],
        ...     tap_settings=TAPSettings(lifetime_hours=4, one_time_use=True)
        ... )
        >>> print(user_response.upn)
        smith_john@company.com
    """
```

#### Error Handling
```python
from app.core.exceptions import PAMBaseException

class UserCreationError(PAMBaseException):
    """Raised when privileged user creation fails."""
    
    def __init__(self, message: str, user_id: Optional[str] = None):
        super().__init__(message)
        self.user_id = user_id
        self.error_code = "USER_CREATION_FAILED"
```

### TypeScript (Frontend)

#### Code Formatting
- **ESLint**: Strict TypeScript rules
- **Prettier**: Code formatting
- **TypeScript**: Strict mode enabled

```bash
# Lint and format
npm run lint
npm run format
npm run type-check
```

#### Component Documentation
```tsx
interface PrivilegedUserFormProps {
  /** Source user object from Azure AD search */
  sourceUser: AzureUser;
  /** Available directory roles for assignment */
  availableRoles: DirectoryRole[];
  /** Callback when user creation is initiated */
  onCreateUser: (userData: CreateUserRequest) => void;
  /** Loading state for form submission */
  isLoading?: boolean;
}

/**
 * Form component for creating privileged users.
 * 
 * This component handles the privileged user creation workflow including
 * role selection, TAP configuration, and form validation. It provides
 * a comprehensive interface for administrators to create privileged accounts
 * with appropriate role assignments.
 * 
 * @example
 * ```tsx
 * <PrivilegedUserForm
 *   sourceUser={selectedUser}
 *   availableRoles={directoryRoles}
 *   onCreateUser={handleUserCreation}
 *   isLoading={isCreating}
 * />
 * ```
 */
export const PrivilegedUserForm: React.FC<PrivilegedUserFormProps> = ({
  sourceUser,
  availableRoles,
  onCreateUser,
  isLoading = false
}) => {
  // Component implementation
};
```

## 🧪 Testing Standards

### Test Coverage Requirements
- **Minimum**: 80% overall coverage
- **Critical paths**: 95% coverage required
- **New features**: 90% coverage required

### Backend Testing
```python
# test_user_creation.py
import pytest
from unittest.mock import Mock, patch
from app.services.user_service import UserService
from app.core.exceptions import UserNotFoundError

class TestUserService:
    """Test suite for UserService functionality."""
    
    @pytest.fixture
    def user_service(self):
        """Create UserService instance with mocked dependencies."""
        return UserService()
    
    @pytest.mark.asyncio
    async def test_create_privileged_user_success(self, user_service):
        """Test successful privileged user creation."""
        # Arrange
        source_user_id = "test-user-id"
        selected_roles = ["test-role-id"]
        
        # Act
        result = await user_service.create_privileged_user(
            source_user_id, selected_roles
        )
        
        # Assert
        assert result.user_id is not None
        assert result.upn.endswith("@company.com")
        assert len(result.assigned_roles) == 1
    
    @pytest.mark.asyncio
    async def test_create_privileged_user_not_found(self, user_service):
        """Test user creation with non-existent source user."""
        with pytest.raises(UserNotFoundError):
            await user_service.create_privileged_user(
                "non-existent-id", ["test-role"]
            )
```

### Frontend Testing
```tsx
// PrivilegedUserForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PrivilegedUserForm } from './PrivilegedUserForm';
import { mockAzureUser, mockDirectoryRoles } from '../../../__mocks__';

describe('PrivilegedUserForm', () => {
  const defaultProps = {
    sourceUser: mockAzureUser,
    availableRoles: mockDirectoryRoles,
    onCreateUser: jest.fn(),
  };

  it('should render form with source user information', () => {
    render(<PrivilegedUserForm {...defaultProps} />);
    
    expect(screen.getByText(mockAzureUser.displayName)).toBeInTheDocument();
    expect(screen.getByText('Create Privileged User')).toBeInTheDocument();
  });

  it('should handle role selection correctly', async () => {
    render(<PrivilegedUserForm {...defaultProps} />);
    
    const roleCheckbox = screen.getByRole('checkbox', { 
      name: /Security Administrator/i 
    });
    
    fireEvent.click(roleCheckbox);
    
    await waitFor(() => {
      expect(roleCheckbox).toBeChecked();
    });
  });
});
```

## 🔒 Security Guidelines

### Secure Coding Practices

1. **Input Validation**: Validate all inputs at API boundaries
2. **Authentication**: Use Azure AD tokens for all operations
3. **Authorization**: Implement role-based access control
4. **Secrets**: Never commit secrets or credentials
5. **Logging**: Log security events without sensitive data

### Security Review Checklist

- [ ] Input validation implemented
- [ ] Authentication tokens validated
- [ ] Authorization checks in place
- [ ] No hardcoded secrets
- [ ] Sensitive data properly encrypted
- [ ] Audit logging implemented
- [ ] Error messages don't leak information

## 📊 Performance Guidelines

### Backend Performance
- Database queries must be optimized (no N+1 queries)
- API responses under 200ms for simple operations
- Background tasks for long-running operations
- Proper caching strategies implemented

### Frontend Performance
- Components must be optimized for re-rendering
- API calls should be batched when possible
- Loading states for all async operations
- Lazy loading for large lists

## 🐛 Bug Reports

### Before Submitting
1. Search existing issues
2. Check if it's already fixed in `develop`
3. Reproduce with minimal example
4. Gather debug information

### Bug Report Template
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Browser: [e.g., Chrome 91]
- Version: [e.g., v1.2.3]

## Additional Context
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
## Feature Description
Clear description of the proposed feature

## Problem Statement
What problem does this solve?

## Proposed Solution
Detailed solution description

## Alternatives Considered
Other solutions you've considered

## Additional Context
Use cases, examples, mockups
```

## 📋 Pull Request Process

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)
- [ ] Security considerations addressed
- [ ] Performance impact considered

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Security
- [ ] No security vulnerabilities introduced
- [ ] Security review completed (if applicable)

## Documentation
- [ ] Code documentation updated
- [ ] User documentation updated (if applicable)
```

## 🏷️ Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build process or auxiliary tool changes

### Examples
```bash
feat(user): add privileged user creation endpoint
fix(auth): resolve token refresh issue
docs(api): update authentication documentation
test(user): add unit tests for user service
```

## 🚀 Release Process

### Version Strategy
We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] Change log updated
- [ ] Version bumped
- [ ] Release notes written

## 🆘 Getting Help

### Resources
- [Development Setup](docs/development/development-setup.md)
- [API Documentation](docs/api/api-reference.md)
- [Architecture Guide](docs/development/architecture.md)

### Contact
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Discord**: [Invite link] for real-time chat
- **Email**: opensource@company.com for private inquiries

## 📄 License

By contributing to Menshun, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Menshun! Together, we're building enterprise-grade security tools that make a difference. 🛡️