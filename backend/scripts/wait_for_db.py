#!/usr/bin/env python3
"""
Database connection wait script for Menshun PAM backend.
This script waits for the database to be ready before starting the application.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add the app directory to the Python path
app_path = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_path))

import asyncpg
from app.core.config import get_settings


async def wait_for_database(max_retries=30, delay=2):
    """
    Wait for the database to be ready.
    
    Args:
        max_retries: Maximum number of connection attempts
        delay: Delay between attempts in seconds
        
    Returns:
        bool: True if database is ready, False if max retries exceeded
    """
    settings = get_settings()
    db_url = settings.DATABASE_URL
    
    print(f"Waiting for database connection at {db_url.split('@')[1] if '@' in db_url else 'database'}...")
    
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            conn = await asyncpg.connect(db_url)
            
            # Test the connection with a simple query
            await conn.execute("SELECT 1")
            await conn.close()
            
            print(f"✅ Database is ready after {attempt + 1} attempts")
            return True
            
        except (asyncpg.exceptions.CannotConnectNowError, 
                asyncpg.exceptions.ConnectionDoesNotExistError,
                ConnectionRefusedError,
                OSError) as e:
            print(f"⏳ Attempt {attempt + 1}/{max_retries}: Database not ready - {str(e)}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ Database connection failed after maximum retries")
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error connecting to database: {str(e)}")
            return False
    
    return False


async def main():
    """Main function to wait for database."""
    try:
        if await wait_for_database():
            print("🎉 Database is ready!")
            return 0
        else:
            print("💥 Failed to connect to database")
            return 1
    except Exception as e:
        print(f"❌ Script failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)