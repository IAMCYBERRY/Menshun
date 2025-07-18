"""
Menshun Backend - Configuration Management Models.

This module contains SQLAlchemy models for storing and managing application
configuration that can be modified through the web interface.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import BaseModel


class SystemConfiguration(BaseModel):
    """
    System-wide configuration settings.
    
    This model stores application configuration that can be modified
    through the web interface, eliminating the need for manual .env file editing.
    """
    
    __tablename__ = "system_configurations"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=True)
    config_type = Column(String(20), nullable=False, default="string")  # string, boolean, integer, json
    
    # Metadata
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(50), nullable=True)
    
    # Validation and constraints
    is_required = Column(Boolean, default=False, nullable=False)
    is_sensitive = Column(Boolean, default=False, nullable=False)  # For passwords, secrets
    validation_regex = Column(String(500), nullable=True)
    default_value = Column(Text, nullable=True)
    possible_values = Column(JSON, nullable=True)  # For enum-like configs
    
    # Setup and management
    setup_step = Column(String(50), nullable=True, index=True)  # Which setup step this belongs to
    setup_order = Column(Integer, default=0)  # Order within the setup step
    is_setup_complete = Column(Boolean, default=False, nullable=False)
    requires_restart = Column(Boolean, default=False, nullable=False)
    
    # Change tracking
    last_modified_by = Column(String(255), nullable=True)
    last_modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    change_reason = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<SystemConfiguration(key='{self.config_key}', category='{self.category}')>"
    
    @property
    def parsed_value(self) -> Any:
        """Parse the configuration value based on its type."""
        if self.config_value is None:
            return None
            
        if self.config_type == "boolean":
            return self.config_value.lower() in ("true", "1", "yes", "on")
        elif self.config_type == "integer":
            try:
                return int(self.config_value)
            except (ValueError, TypeError):
                return None
        elif self.config_type == "json":
            try:
                import json
                return json.loads(self.config_value)
            except (ValueError, TypeError):
                return None
        else:
            return self.config_value
    
    def set_value(self, value: Any) -> None:
        """Set the configuration value with proper type conversion."""
        if value is None:
            self.config_value = None
            return
            
        if self.config_type == "boolean":
            self.config_value = str(bool(value)).lower()
        elif self.config_type == "integer":
            self.config_value = str(int(value))
        elif self.config_type == "json":
            import json
            self.config_value = json.dumps(value)
        else:
            self.config_value = str(value)


class SetupProgress(BaseModel):
    """
    Track the progress of the initial system setup.
    
    This model stores information about which setup steps have been completed
    and the overall setup status.
    """
    
    __tablename__ = "setup_progress"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setup_step = Column(String(50), nullable=False, unique=True, index=True)
    
    # Status tracking
    is_completed = Column(Boolean, default=False, nullable=False)
    is_skipped = Column(Boolean, default=False, nullable=False)
    completion_percentage = Column(Integer, default=0)  # 0-100
    
    # Metadata
    step_name = Column(String(200), nullable=False)
    step_description = Column(Text, nullable=True)
    step_order = Column(Integer, default=0)
    
    # Completion tracking
    completed_by = Column(String(255), nullable=True)
    completed_date = Column(DateTime, nullable=True)
    completion_notes = Column(Text, nullable=True)
    
    # Error tracking
    last_error = Column(Text, nullable=True)
    error_count = Column(Integer, default=0)
    
    def __repr__(self) -> str:
        return f"<SetupProgress(step='{self.setup_step}', completed={self.is_completed})>"


class ConfigurationTemplate(BaseModel):
    """
    Pre-defined configuration templates for different deployment scenarios.
    
    This model stores configuration templates that can be applied during setup
    to quickly configure the system for specific use cases.
    """
    
    __tablename__ = "configuration_templates"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_name = Column(String(100), nullable=False, unique=True)
    template_version = Column(String(20), default="1.0")
    
    # Template metadata
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # development, staging, production, etc.
    
    # Template configuration
    configuration_data = Column(JSON, nullable=False)  # Key-value pairs for configurations
    required_environment = Column(String(50), nullable=True)  # development, production, etc.
    
    # Prerequisites and compatibility
    minimum_version = Column(String(20), nullable=True)
    prerequisites = Column(JSON, nullable=True)  # List of required setup steps or dependencies
    compatibility_notes = Column(Text, nullable=True)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_date = Column(DateTime, nullable=True)
    
    # Template management
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return f"<ConfigurationTemplate(name='{self.template_name}', category='{self.category}')>"


class ConfigurationHistory(BaseModel):
    """
    Track changes to system configuration over time.
    
    This model provides an audit trail of all configuration changes
    for compliance and troubleshooting purposes.
    """
    
    __tablename__ = "configuration_history"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    configuration_key = Column(String(100), nullable=False, index=True)
    
    # Change tracking
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    change_type = Column(String(20), nullable=False)  # create, update, delete
    
    # Change metadata
    changed_by = Column(String(255), nullable=False)
    change_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    change_reason = Column(Text, nullable=True)
    source = Column(String(50), default="web_interface")  # web_interface, api, import, etc.
    
    # Session and context
    session_id = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Impact tracking
    requires_restart = Column(Boolean, default=False, nullable=False)
    restart_completed = Column(Boolean, default=False, nullable=False)
    restart_date = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<ConfigurationHistory(key='{self.configuration_key}', type='{self.change_type}', date='{self.change_date}')>"