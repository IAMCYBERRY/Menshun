"""
Menshun Backend - Configuration Management Service.

This module provides services for managing system configuration through
the web interface, including setup wizards and dynamic configuration updates.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.configuration import (
    SystemConfiguration,
    SetupProgress,
    ConfigurationTemplate,
    ConfigurationHistory
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class ConfigurationService:
    """Service for managing system configuration and setup process."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def initialize_default_configurations(self) -> None:
        """Initialize default configuration entries for guided setup."""
        default_configs = [
            # Azure AD Configuration
            {
                "config_key": "AZURE_CLIENT_ID",
                "display_name": "Azure AD Client ID",
                "description": "The Application (client) ID from your Azure AD app registration",
                "category": "azure_ad",
                "subcategory": "authentication",
                "config_type": "string",
                "is_required": True,
                "setup_step": "azure_setup",
                "setup_order": 1,
                "validation_regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            },
            {
                "config_key": "AZURE_CLIENT_SECRET",
                "display_name": "Azure AD Client Secret",
                "description": "The client secret value from your Azure AD app registration",
                "category": "azure_ad",
                "subcategory": "authentication",
                "config_type": "string",
                "is_required": True,
                "is_sensitive": True,
                "setup_step": "azure_setup",
                "setup_order": 2
            },
            {
                "config_key": "AZURE_TENANT_ID",
                "display_name": "Azure AD Tenant ID",
                "description": "Your Azure AD tenant (directory) ID",
                "category": "azure_ad",
                "subcategory": "authentication",
                "config_type": "string",
                "is_required": True,
                "setup_step": "azure_setup",
                "setup_order": 3,
                "validation_regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            },
            
            # Organization Configuration
            {
                "config_key": "ORGANIZATION_NAME",
                "display_name": "Organization Name",
                "description": "Your organization's display name",
                "category": "organization",
                "subcategory": "basic",
                "config_type": "string",
                "is_required": True,
                "setup_step": "organization_setup",
                "setup_order": 1
            },
            {
                "config_key": "ORGANIZATION_DOMAIN",
                "display_name": "Organization Domain",
                "description": "Your organization's primary domain (e.g., company.com)",
                "category": "organization",
                "subcategory": "basic",
                "config_type": "string",
                "is_required": True,
                "setup_step": "organization_setup",
                "setup_order": 2,
                "validation_regex": r"^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$"
            },
            {
                "config_key": "PRIMARY_ADMINISTRATOR_EMAIL",
                "display_name": "Primary Administrator Email",
                "description": "Email address of the primary system administrator",
                "category": "organization",
                "subcategory": "admin",
                "config_type": "string",
                "is_required": True,
                "setup_step": "organization_setup",
                "setup_order": 3,
                "validation_regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            },
            
            # Security Configuration
            {
                "config_key": "DEFAULT_SESSION_TIMEOUT",
                "display_name": "Default Session Timeout (minutes)",
                "description": "Default session timeout for user sessions",
                "category": "security",
                "subcategory": "sessions",
                "config_type": "integer",
                "default_value": "30",
                "setup_step": "security_setup",
                "setup_order": 1,
                "validation_regex": r"^[1-9][0-9]*$"
            },
            {
                "config_key": "REQUIRE_MFA_FOR_PRIVILEGED",
                "display_name": "Require MFA for Privileged Users",
                "description": "Require multi-factor authentication for privileged user operations",
                "category": "security",
                "subcategory": "mfa",
                "config_type": "boolean",
                "default_value": "true",
                "setup_step": "security_setup",
                "setup_order": 2
            },
            {
                "config_key": "MAX_ROLE_ASSIGNMENT_DURATION",
                "display_name": "Maximum Role Assignment Duration (days)",
                "description": "Maximum duration for time-limited role assignments",
                "category": "security",
                "subcategory": "roles",
                "config_type": "integer",
                "default_value": "90",
                "setup_step": "security_setup",
                "setup_order": 3
            },
            
            # Compliance Configuration
            {
                "config_key": "ENABLED_COMPLIANCE_FRAMEWORKS",
                "display_name": "Enabled Compliance Frameworks",
                "description": "Select which compliance frameworks to enable",
                "category": "compliance",
                "subcategory": "frameworks",
                "config_type": "json",
                "default_value": '["SOC2"]',
                "possible_values": ["SOX", "SOC2", "ISO27001", "GDPR", "HIPAA"],
                "setup_step": "compliance_setup",
                "setup_order": 1
            },
            {
                "config_key": "AUDIT_LOG_RETENTION_DAYS",
                "display_name": "Audit Log Retention (days)",
                "description": "How long to retain audit logs",
                "category": "compliance",
                "subcategory": "auditing",
                "config_type": "integer",
                "default_value": "2555",  # 7 years for SOX compliance
                "setup_step": "compliance_setup",
                "setup_order": 2
            },
            {
                "config_key": "REQUIRE_JUSTIFICATION_FOR_PRIVILEGED",
                "display_name": "Require Justification for Privileged Access",
                "description": "Require users to provide justification for privileged access requests",
                "category": "compliance",
                "subcategory": "justification",
                "config_type": "boolean",
                "default_value": "true",
                "setup_step": "compliance_setup",
                "setup_order": 3
            },
            
            # Notification Configuration
            {
                "config_key": "SMTP_HOST",
                "display_name": "SMTP Server Host",
                "description": "SMTP server hostname for email notifications",
                "category": "notifications",
                "subcategory": "email",
                "config_type": "string",
                "setup_step": "notifications_setup",
                "setup_order": 1
            },
            {
                "config_key": "SMTP_PORT",
                "display_name": "SMTP Server Port",
                "description": "SMTP server port (usually 587 for TLS)",
                "category": "notifications",
                "subcategory": "email",
                "config_type": "integer",
                "default_value": "587",
                "setup_step": "notifications_setup",
                "setup_order": 2
            },
            {
                "config_key": "SMTP_FROM_EMAIL",
                "display_name": "From Email Address",
                "description": "Email address to use as sender for notifications",
                "category": "notifications",
                "subcategory": "email",
                "config_type": "string",
                "setup_step": "notifications_setup",
                "setup_order": 3,
                "validation_regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            }
        ]
        
        for config_data in default_configs:
            # Check if configuration already exists
            result = await self.db.execute(
                select(SystemConfiguration).where(
                    SystemConfiguration.config_key == config_data["config_key"]
                )
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                config = SystemConfiguration(**config_data)
                self.db.add(config)
        
        await self.db.commit()
        logger.info("Default configurations initialized")
    
    async def initialize_setup_steps(self) -> None:
        """Initialize the setup progress tracking."""
        setup_steps = [
            {
                "setup_step": "welcome",
                "step_name": "Welcome & Prerequisites",
                "step_description": "Welcome to Menshun PAM and system requirements check",
                "step_order": 1
            },
            {
                "setup_step": "azure_setup",
                "step_name": "Azure AD Configuration",
                "step_description": "Configure Azure Active Directory integration",
                "step_order": 2
            },
            {
                "setup_step": "organization_setup",
                "step_name": "Organization Settings",
                "step_description": "Configure your organization details and administrator",
                "step_order": 3
            },
            {
                "setup_step": "security_setup",
                "step_name": "Security Policies",
                "step_description": "Configure security policies and access controls",
                "step_order": 4
            },
            {
                "setup_step": "compliance_setup",
                "step_name": "Compliance Configuration",
                "step_description": "Configure compliance frameworks and audit settings",
                "step_order": 5
            },
            {
                "setup_step": "notifications_setup",
                "step_name": "Notifications",
                "step_description": "Configure email notifications and alerts",
                "step_order": 6
            },
            {
                "setup_step": "review_complete",
                "step_name": "Review & Complete",
                "step_description": "Review configuration and complete setup",
                "step_order": 7
            }
        ]
        
        for step_data in setup_steps:
            # Check if step already exists
            result = await self.db.execute(
                select(SetupProgress).where(
                    SetupProgress.setup_step == step_data["setup_step"]
                )
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                step = SetupProgress(**step_data)
                self.db.add(step)
        
        await self.db.commit()
        logger.info("Setup steps initialized")
    
    async def is_setup_complete(self) -> bool:
        """Check if the initial system setup has been completed."""
        result = await self.db.execute(
            select(SetupProgress).where(
                SetupProgress.setup_step == "review_complete"
            )
        )
        final_step = result.scalar_one_or_none()
        
        if final_step and final_step.is_completed:
            return True
        
        # Also check if all required configurations are set
        result = await self.db.execute(
            select(SystemConfiguration).where(
                SystemConfiguration.is_required == True,
                SystemConfiguration.config_value.is_(None)
            )
        )
        missing_configs = result.scalars().all()
        
        return len(missing_configs) == 0
    
    async def get_setup_progress(self) -> Dict[str, Any]:
        """Get the current setup progress."""
        result = await self.db.execute(
            select(SetupProgress).order_by(SetupProgress.step_order)
        )
        steps = result.scalars().all()
        
        total_steps = len(steps)
        completed_steps = sum(1 for step in steps if step.is_completed)
        
        return {
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "completion_percentage": int((completed_steps / total_steps) * 100) if total_steps > 0 else 0,
            "current_step": next((step.setup_step for step in steps if not step.is_completed), None),
            "is_complete": completed_steps == total_steps,
            "steps": [
                {
                    "step": step.setup_step,
                    "name": step.step_name,
                    "description": step.step_description,
                    "order": step.step_order,
                    "is_completed": step.is_completed,
                    "is_skipped": step.is_skipped,
                    "completion_percentage": step.completion_percentage
                }
                for step in steps
            ]
        }
    
    async def get_configurations_for_step(self, setup_step: str) -> List[Dict[str, Any]]:
        """Get all configurations for a specific setup step."""
        result = await self.db.execute(
            select(SystemConfiguration)
            .where(SystemConfiguration.setup_step == setup_step)
            .order_by(SystemConfiguration.setup_order)
        )
        configs = result.scalars().all()
        
        return [
            {
                "id": str(config.id),
                "key": config.config_key,
                "display_name": config.display_name,
                "description": config.description,
                "type": config.config_type,
                "value": config.config_value if not config.is_sensitive else None,
                "default_value": config.default_value,
                "is_required": config.is_required,
                "is_sensitive": config.is_sensitive,
                "validation_regex": config.validation_regex,
                "possible_values": config.possible_values,
                "setup_order": config.setup_order
            }
            for config in configs
        ]
    
    async def update_configuration(
        self,
        config_key: str,
        value: Any,
        changed_by: str,
        change_reason: Optional[str] = None
    ) -> bool:
        """Update a configuration value."""
        try:
            # Get the configuration
            result = await self.db.execute(
                select(SystemConfiguration).where(
                    SystemConfiguration.config_key == config_key
                )
            )
            config = result.scalar_one_or_none()
            
            if not config:
                logger.error(f"Configuration not found: {config_key}")
                return False
            
            # Store old value for history
            old_value = config.config_value
            
            # Update the configuration
            config.set_value(value)
            config.last_modified_by = changed_by
            config.last_modified_date = datetime.utcnow()
            config.change_reason = change_reason
            
            # Create history record
            history = ConfigurationHistory(
                configuration_key=config_key,
                old_value=old_value,
                new_value=config.config_value,
                change_type="update",
                changed_by=changed_by,
                change_reason=change_reason,
                requires_restart=config.requires_restart
            )
            self.db.add(history)
            
            await self.db.commit()
            logger.info(f"Configuration updated: {config_key}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating configuration {config_key}: {e}")
            return False
    
    async def complete_setup_step(
        self,
        setup_step: str,
        completed_by: str,
        completion_notes: Optional[str] = None
    ) -> bool:
        """Mark a setup step as completed."""
        try:
            # Get the setup step
            result = await self.db.execute(
                select(SetupProgress).where(
                    SetupProgress.setup_step == setup_step
                )
            )
            step = result.scalar_one_or_none()
            
            if not step:
                logger.error(f"Setup step not found: {setup_step}")
                return False
            
            # Mark as completed
            step.is_completed = True
            step.completion_percentage = 100
            step.completed_by = completed_by
            step.completed_date = datetime.utcnow()
            step.completion_notes = completion_notes
            
            await self.db.commit()
            logger.info(f"Setup step completed: {setup_step}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error completing setup step {setup_step}: {e}")
            return False
    
    async def get_configuration_value(self, config_key: str) -> Any:
        """Get a configuration value by key."""
        result = await self.db.execute(
            select(SystemConfiguration).where(
                SystemConfiguration.config_key == config_key
            )
        )
        config = result.scalar_one_or_none()
        
        if config:
            return config.parsed_value
        return None
    
    async def apply_configuration_template(
        self,
        template_name: str,
        applied_by: str
    ) -> bool:
        """Apply a configuration template."""
        try:
            # Get the template
            result = await self.db.execute(
                select(ConfigurationTemplate).where(
                    ConfigurationTemplate.template_name == template_name,
                    ConfigurationTemplate.is_active == True
                )
            )
            template = result.scalar_one_or_none()
            
            if not template:
                logger.error(f"Configuration template not found: {template_name}")
                return False
            
            # Apply each configuration from the template
            for config_key, config_value in template.configuration_data.items():
                await self.update_configuration(
                    config_key=config_key,
                    value=config_value,
                    changed_by=applied_by,
                    change_reason=f"Applied template: {template_name}"
                )
            
            # Update template usage
            template.usage_count += 1
            template.last_used_date = datetime.utcnow()
            
            await self.db.commit()
            logger.info(f"Configuration template applied: {template_name}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error applying template {template_name}: {e}")
            return False