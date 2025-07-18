"""
Menshun Backend - Database Configuration and Connection Management.

This module handles database connectivity, session management, and provides
the foundation for SQLAlchemy ORM operations throughout the application.
"""

import asyncio
from typing import AsyncGenerator, Optional

from sqlalchemy import event, pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Base class for all SQLAlchemy models
Base = declarative_base()

# Create async engine with connection pooling
engine = create_async_engine(
    settings.get_database_url(),
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,   # Recycle connections every hour
    future=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session for dependency injection.
    
    This function provides a database session that automatically handles
    cleanup and error rollback for FastAPI dependencies.
    
    Yields:
        AsyncSession: Database session instance
        
    Example:
        ```python
        @app.get("/users/")
        async def get_users(db: AsyncSession = Depends(get_database_session)):
            result = await db.execute(select(User))
            return result.scalars().all()
        ```
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_database_tables() -> None:
    """
    Create all database tables.
    
    This function creates all tables defined by SQLAlchemy models.
    It should only be used for development and testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_database_tables() -> None:
    """
    Drop all database tables.
    
    WARNING: This function destroys all data in the database.
    It should only be used for development and testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped successfully")


async def check_database_connection() -> bool:
    """
    Check if the database connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


# Database event listeners for logging and monitoring
@event.listens_for(engine.sync_engine, "connect")
def on_connect(dbapi_connection, connection_record):
    """Log database connections."""
    logger.debug("Database connection established")


@event.listens_for(engine.sync_engine, "checkout")
def on_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log connection checkout from pool."""
    logger.debug("Database connection checked out from pool")


@event.listens_for(engine.sync_engine, "checkin")
def on_checkin(dbapi_connection, connection_record):
    """Log connection checkin to pool."""
    logger.debug("Database connection returned to pool")


__all__ = [
    "Base",
    "engine",
    "async_session_factory",
    "get_database_session",
    "create_database_tables",
    "drop_database_tables",
    "check_database_connection",
]