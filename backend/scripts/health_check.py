#!/usr/bin/env python3
"""
Health check script for Menshun PAM backend service.
This script is used by Docker healthcheck to verify the service is running properly.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_path = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_path))

import httpx
import asyncpg
from app.core.config import get_settings


async def check_api_health():
    """Check if the API is responding."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                return True, "API is healthy"
            else:
                return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"API health check failed: {str(e)}"


async def check_database_health():
    """Check if the database is accessible."""
    try:
        settings = get_settings()
        # Parse database URL
        db_url = settings.DATABASE_URL
        
        # Simple connection test
        conn = await asyncpg.connect(db_url)
        await conn.execute("SELECT 1")
        await conn.close()
        
        return True, "Database is healthy"
    except Exception as e:
        return False, f"Database health check failed: {str(e)}"


async def main():
    """Run all health checks."""
    print("Running health checks...")
    
    # Check API health
    api_healthy, api_message = await check_api_health()
    print(f"API: {api_message}")
    
    # Check database health
    db_healthy, db_message = await check_database_health()
    print(f"Database: {db_message}")
    
    # Overall health
    if api_healthy and db_healthy:
        print("✅ All health checks passed")
        return 0
    else:
        print("❌ Health checks failed")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Health check script failed: {str(e)}")
        sys.exit(1)