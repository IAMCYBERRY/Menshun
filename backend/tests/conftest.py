"""
Menshun Backend - Test Configuration and Fixtures.

This module provides shared fixtures and configuration for all tests,
including database setup, authentication mocking, and test clients.
"""

import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_async_session
from app.core.config import get_settings
from app.models.user import PrivilegedUser
from app.models.directory_role import DirectoryRole
from app.models.service_identity import ServiceIdentity

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def override_get_async_session(db_session: AsyncSession):
    """Override the database session dependency."""
    async def _override_get_async_session():
        yield db_session
    
    app.dependency_overrides[get_async_session] = _override_get_async_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(override_get_async_session) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def sync_client(override_get_async_session) -> Generator[TestClient, None, None]:
    """Create a sync HTTP client for testing."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_settings():
    """Override settings for testing."""
    settings = get_settings()
    settings.DATABASE_URL = TEST_DATABASE_URL
    settings.TESTING = True
    settings.SECRET_KEY = "test-secret-key-for-testing-only"
    return settings


@pytest_asyncio.fixture
async def sample_directory_role(db_session: AsyncSession) -> DirectoryRole:
    """Create a sample directory role for testing."""
    role = DirectoryRole(
        template_id="62e90394-69f5-4237-9190-012177145e10",
        role_name="Global Administrator",
        description="Can manage all aspects of Microsoft Entra ID and Microsoft services.",
        category="Global",
        subcategory="Administrative",
        is_privileged=True,
        risk_level="critical",
        risk_score=95,
        requires_justification=True,
        requires_approval=True,
        max_assignment_duration_days=30,
        can_manage_users=True,
        can_manage_groups=True,
        can_manage_applications=True,
        can_manage_devices=True,
        can_read_directory=True,
        can_write_directory=True,
        compliance_frameworks='["SOX", "SOC2", "ISO27001"]',
        requires_certification=True,
        certification_frequency_days=30,
    )
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role


@pytest_asyncio.fixture
async def sample_user(db_session: AsyncSession) -> PrivilegedUser:
    """Create a sample privileged user for testing."""
    user = PrivilegedUser(
        user_principal_name="test.user@company.com",
        display_name="Test User",
        given_name="Test",
        surname="User",
        email="test.user@company.com",
        department="IT Security",
        job_title="Security Administrator",
        is_privileged=True,
        risk_score=75,
        account_enabled=True,
        compliance_status="compliant",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def sample_service_identity(db_session: AsyncSession) -> ServiceIdentity:
    """Create a sample service identity for testing."""
    service_identity = ServiceIdentity(
        identity_type="service_principal",
        name="Test Service Principal",
        description="Test service principal for automated testing",
        application_id="test-app-id",
        object_id="test-object-id",
        tenant_id="test-tenant-id",
        is_enabled=True,
        risk_score=45,
    )
    db_session.add(service_identity)
    await db_session.commit()
    await db_session.refresh(service_identity)
    return service_identity


@pytest.fixture
def mock_azure_token():
    """Mock Azure AD token for authentication testing."""
    return {
        "access_token": "mock-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "User.Read Directory.Read.All",
        "id_token": "mock-id-token",
    }


@pytest.fixture
def mock_graph_user():
    """Mock Microsoft Graph user data."""
    return {
        "id": "test-user-id",
        "userPrincipalName": "test.user@company.com",
        "displayName": "Test User",
        "givenName": "Test",
        "surname": "User",
        "mail": "test.user@company.com",
        "department": "IT Security",
        "jobTitle": "Security Administrator",
        "accountEnabled": True,
    }


@pytest.fixture
def mock_graph_role():
    """Mock Microsoft Graph directory role data."""
    return {
        "id": "test-role-id",
        "roleTemplateId": "62e90394-69f5-4237-9190-012177145e10",
        "displayName": "Global Administrator",
        "description": "Can manage all aspects of Microsoft Entra ID and Microsoft services.",
        "isBuiltIn": True,
        "isEnabled": True,
    }


# Test data factories
class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user_data(**kwargs):
        """Create user test data."""
        default_data = {
            "user_principal_name": "test.user@company.com",
            "display_name": "Test User",
            "given_name": "Test",
            "surname": "User",
            "email": "test.user@company.com",
            "department": "IT Security",
            "job_title": "Security Administrator",
            "is_privileged": True,
            "risk_score": 75,
            "account_enabled": True,
            "compliance_status": "compliant",
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_role_data(**kwargs):
        """Create directory role test data."""
        default_data = {
            "template_id": "test-template-id",
            "role_name": "Test Role",
            "description": "Test role description",
            "category": "Test",
            "is_privileged": True,
            "risk_level": "medium",
            "risk_score": 50,
            "requires_justification": True,
            "requires_approval": False,
            "can_manage_users": False,
            "can_manage_groups": False,
            "can_manage_applications": False,
            "can_manage_devices": False,
            "can_read_directory": True,
            "can_write_directory": False,
            "requires_certification": False,
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_service_identity_data(**kwargs):
        """Create service identity test data."""
        default_data = {
            "identity_type": "service_principal",
            "name": "Test Service Identity",
            "description": "Test service identity description",
            "application_id": "test-app-id",
            "object_id": "test-object-id",
            "tenant_id": "test-tenant-id",
            "is_enabled": True,
            "risk_score": 45,
        }
        default_data.update(kwargs)
        return default_data


@pytest.fixture
def test_data_factory():
    """Provide test data factory."""
    return TestDataFactory


# Pytest markers for test categorization
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "database: Database tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "security: Security tests")
    config.addinivalue_line("markers", "compliance: Compliance tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add markers based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        
        # Add slow marker for tests that take longer
        if hasattr(item, "fixturenames") and "slow" in item.fixturenames:
            item.add_marker(pytest.mark.slow)


# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    yield
    # Cleanup is handled by pytest automatically