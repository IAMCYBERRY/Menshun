"""
Menshun Backend - API Tests for Health Endpoints.

Tests for health check endpoints including liveness and readiness probes.
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient


@pytest.mark.api
@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health check endpoints."""
    
    async def test_health_check(self, async_client: AsyncClient):
        """Test basic health check endpoint."""
        response = await async_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
    
    async def test_health_ready(self, async_client: AsyncClient):
        """Test readiness probe endpoint."""
        response = await async_client.get("/health/ready")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "ready"
        assert "checks" in data
        assert "database" in data["checks"]
        assert "redis" in data["checks"]
    
    async def test_health_live(self, async_client: AsyncClient):
        """Test liveness probe endpoint."""
        response = await async_client.get("/health/live")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "alive"
        assert "uptime" in data
        assert "memory_usage" in data


@pytest.mark.api
def test_health_check_sync(sync_client: TestClient):
    """Test health check with synchronous client."""
    response = sync_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "timestamp" in data


@pytest.mark.api
def test_health_endpoints_no_auth_required(sync_client: TestClient):
    """Test that health endpoints don't require authentication."""
    endpoints = ["/health", "/health/ready", "/health/live"]
    
    for endpoint in endpoints:
        response = sync_client.get(endpoint)
        assert response.status_code == 200
        # Should not return 401 or 403 (authentication/authorization errors)
        assert response.status_code not in [401, 403]