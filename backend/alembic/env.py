"""
Menshun Backend - Alembic Environment Configuration.

This module configures the Alembic migration environment for the Menshun PAM system,
providing async support, comprehensive logging, and database configuration management.
"""

import asyncio
import os
from logging.config import fileConfig
from typing import Any

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

# Import models for metadata
from app.core.database import Base
from app.models import *  # Import all models to ensure metadata is available

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# Other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_database_url() -> str:
    """
    Get database URL from environment or config.
    
    Returns:
        str: Database connection URL
    """
    # Try to get from environment first
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Convert to async URL if needed
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return database_url
    
    # Fallback to config
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is also acceptable here. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Custom options for better migration experience
        compare_type=True,
        compare_server_default=True,
        include_schemas=False,
        # Add custom compare functions for better detection
        render_as_batch=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Any) -> None:
    """
    Run migrations with the provided connection.
    
    Args:
        connection: Database connection
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Enhanced migration options
        compare_type=True,
        compare_server_default=True,
        include_schemas=False,
        render_as_batch=False,
        # Custom naming convention for constraints
        render_item=render_item,
        # Transaction per migration for better error handling
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def render_item(type_: str, obj: Any, autogen_context: Any) -> str:
    """
    Custom renderer for migration items.
    
    This function provides custom rendering for specific database objects
    to ensure consistent naming and better migration readability.
    
    Args:
        type_: Type of object being rendered
        obj: The object being rendered
        autogen_context: Autogeneration context
        
    Returns:
        str: Rendered item or None for default rendering
    """
    # Custom rendering for indexes
    if type_ == "index":
        # Ensure consistent index naming
        if hasattr(obj, 'name') and obj.name:
            return f"sa.Index('{obj.name}', {', '.join(repr(c.name) for c in obj.columns)})"
    
    # Custom rendering for foreign keys
    elif type_ == "foreign_key":
        # Add descriptive comments for foreign keys
        if hasattr(obj, 'constraint') and obj.constraint:
            fk = obj.constraint
            return f"sa.ForeignKey('{fk.referred_table.name}.{fk.referred_table.columns.keys()[0]}', ondelete='{fk.ondelete or 'RESTRICT'}')"
    
    # Let Alembic handle default rendering
    return None


async def run_async_migrations() -> None:
    """
    Run migrations in async mode.
    
    This function handles async database connections and ensures
    proper cleanup and error handling.
    """
    # Get database configuration
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    
    # Create async engine
    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            # Additional async configuration
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context. For async engines, we use asyncio to handle the
    async context properly.
    """
    # Check if we're running in async mode
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're already in an async context
            asyncio.create_task(run_async_migrations())
        else:
            # Run in new event loop
            asyncio.run(run_async_migrations())
    except RuntimeError:
        # No event loop, create one
        asyncio.run(run_async_migrations())


# Determine if we're running offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()