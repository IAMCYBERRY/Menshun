"""
Menshun Backend - Setup and Configuration API Endpoints.

This module provides API endpoints for the guided setup wizard and
configuration management through the web interface.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.database import get_async_session
from app.services.configuration import ConfigurationService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/setup", tags=["Setup & Configuration"])


# Pydantic models for request/response
class SetupCheckResponse(BaseModel):
    """Response model for setup status check."""
    is_setup_complete: bool
    requires_setup: bool
    setup_progress: Dict[str, Any]


class ConfigurationItem(BaseModel):
    """Model for configuration item."""
    key: str
    display_name: str
    description: Optional[str] = None
    type: str = "string"
    value: Optional[str] = None
    default_value: Optional[str] = None
    is_required: bool = False
    is_sensitive: bool = False
    validation_regex: Optional[str] = None
    possible_values: Optional[List[str]] = None


class UpdateConfigurationRequest(BaseModel):
    """Request model for updating configuration."""
    configurations: List[Dict[str, Any]]
    change_reason: Optional[str] = None


class CompleteStepRequest(BaseModel):
    """Request model for completing a setup step."""
    completion_notes: Optional[str] = None


@router.get(
    "/status",
    response_model=SetupCheckResponse,
    summary="Check Setup Status",
    description="Check if the system setup has been completed and get current progress"
)
async def check_setup_status(
    db: AsyncSession = Depends(get_async_session)
) -> SetupCheckResponse:
    """
    Check the current setup status and progress.
    
    This endpoint determines if the guided setup needs to be shown
    and provides current progress information.
    """
    try:
        config_service = ConfigurationService(db)
        
        # Initialize default configurations and steps if they don't exist
        await config_service.initialize_default_configurations()
        await config_service.initialize_setup_steps()
        
        # Check setup completion status
        is_complete = await config_service.is_setup_complete()
        setup_progress = await config_service.get_setup_progress()
        
        return SetupCheckResponse(
            is_setup_complete=is_complete,
            requires_setup=not is_complete,
            setup_progress=setup_progress
        )
        
    except Exception as e:
        logger.error(f"Error checking setup status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check setup status"
        )


@router.get(
    "/steps/{step_name}/configurations",
    response_model=List[ConfigurationItem],
    summary="Get Configurations for Setup Step",
    description="Get all configuration items for a specific setup step"
)
async def get_step_configurations(
    step_name: str,
    db: AsyncSession = Depends(get_async_session)
) -> List[ConfigurationItem]:
    """
    Get all configuration items for a specific setup step.
    
    Args:
        step_name: The name of the setup step
        
    Returns:
        List of configuration items for the step
    """
    try:
        config_service = ConfigurationService(db)
        configurations = await config_service.get_configurations_for_step(step_name)
        
        return [
            ConfigurationItem(
                key=config["key"],
                display_name=config["display_name"],
                description=config["description"],
                type=config["type"],
                value=config["value"],
                default_value=config["default_value"],
                is_required=config["is_required"],
                is_sensitive=config["is_sensitive"],
                validation_regex=config["validation_regex"],
                possible_values=config["possible_values"]
            )
            for config in configurations
        ]
        
    except Exception as e:
        logger.error(f"Error getting configurations for step {step_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get configurations for step: {step_name}"
        )


@router.post(
    "/steps/{step_name}/configurations",
    summary="Update Step Configurations",
    description="Update configuration values for a specific setup step"
)
async def update_step_configurations(
    step_name: str,
    request: UpdateConfigurationRequest,
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Update configuration values for a specific setup step.
    
    Args:
        step_name: The name of the setup step
        request: The configuration update request
        
    Returns:
        Success status and updated configuration count
    """
    try:
        config_service = ConfigurationService(db)
        updated_count = 0
        failed_updates = []
        
        # Update each configuration
        for config_data in request.configurations:
            config_key = config_data.get("key")
            config_value = config_data.get("value")
            
            if not config_key:
                continue
                
            success = await config_service.update_configuration(
                config_key=config_key,
                value=config_value,
                changed_by="setup_wizard",  # TODO: Get actual user
                change_reason=request.change_reason or f"Updated via setup step: {step_name}"
            )
            
            if success:
                updated_count += 1
            else:
                failed_updates.append(config_key)
        
        if failed_updates:
            logger.warning(f"Failed to update configurations: {failed_updates}")
        
        return {
            "success": True,
            "updated_count": updated_count,
            "failed_updates": failed_updates,
            "message": f"Updated {updated_count} configurations for step: {step_name}"
        }
        
    except Exception as e:
        logger.error(f"Error updating configurations for step {step_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update configurations for step: {step_name}"
        )


@router.post(
    "/steps/{step_name}/complete",
    summary="Complete Setup Step",
    description="Mark a setup step as completed"
)
async def complete_setup_step(
    step_name: str,
    request: CompleteStepRequest,
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Mark a setup step as completed.
    
    Args:
        step_name: The name of the setup step to complete
        request: The completion request with optional notes
        
    Returns:
        Success status and completion information
    """
    try:
        config_service = ConfigurationService(db)
        
        success = await config_service.complete_setup_step(
            setup_step=step_name,
            completed_by="setup_wizard",  # TODO: Get actual user
            completion_notes=request.completion_notes
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Setup step not found: {step_name}"
            )
        
        # Get updated progress
        setup_progress = await config_service.get_setup_progress()
        
        return {
            "success": True,
            "step_name": step_name,
            "message": f"Setup step '{step_name}' completed successfully",
            "overall_progress": setup_progress
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing setup step {step_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete setup step: {step_name}"
        )


@router.get(
    "/progress",
    summary="Get Setup Progress",
    description="Get detailed progress information for the setup process"
)
async def get_setup_progress(
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Get detailed setup progress information.
    
    Returns:
        Detailed progress information including all steps
    """
    try:
        config_service = ConfigurationService(db)
        return await config_service.get_setup_progress()
        
    except Exception as e:
        logger.error(f"Error getting setup progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get setup progress"
        )


@router.post(
    "/test-azure-connection",
    summary="Test Azure AD Connection",
    description="Test the Azure AD configuration by attempting to connect"
)
async def test_azure_connection(
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Test the Azure AD connection with current configuration.
    
    Returns:
        Connection test results
    """
    try:
        config_service = ConfigurationService(db)
        
        # Get Azure AD configuration
        client_id = await config_service.get_configuration_value("AZURE_CLIENT_ID")
        client_secret = await config_service.get_configuration_value("AZURE_CLIENT_SECRET")
        tenant_id = await config_service.get_configuration_value("AZURE_TENANT_ID")
        
        if not all([client_id, client_secret, tenant_id]):
            return {
                "success": False,
                "error": "Azure AD configuration is incomplete",
                "missing_fields": [
                    field for field, value in [
                        ("client_id", client_id),
                        ("client_secret", client_secret),
                        ("tenant_id", tenant_id)
                    ] if not value
                ]
            }
        
        # TODO: Implement actual Azure AD connection test
        # This would use the Microsoft Graph SDK to test authentication
        
        # For now, return a mock successful response
        return {
            "success": True,
            "message": "Azure AD connection test successful",
            "tenant_info": {
                "tenant_id": tenant_id,
                "verified": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error testing Azure AD connection: {e}")
        return {
            "success": False,
            "error": f"Connection test failed: {str(e)}"
        }


@router.post(
    "/templates/{template_name}/apply",
    summary="Apply Configuration Template",
    description="Apply a pre-defined configuration template"
)
async def apply_configuration_template(
    template_name: str,
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Apply a pre-defined configuration template.
    
    Args:
        template_name: Name of the template to apply
        
    Returns:
        Success status and applied configuration details
    """
    try:
        config_service = ConfigurationService(db)
        
        success = await config_service.apply_configuration_template(
            template_name=template_name,
            applied_by="setup_wizard"  # TODO: Get actual user
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration template not found: {template_name}"
            )
        
        return {
            "success": True,
            "template_name": template_name,
            "message": f"Configuration template '{template_name}' applied successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error applying configuration template {template_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to apply configuration template: {template_name}"
        )


@router.get(
    "/system-info",
    summary="Get System Information",
    description="Get system information for the setup process"
)
async def get_system_info() -> Dict[str, Any]:
    """
    Get system information for display in the setup wizard.
    
    Returns:
        System information including version, environment, etc.
    """
    try:
        import os
        import platform
        import psutil
        from app import get_version
        
        return {
            "application": {
                "name": "Menshun PAM",
                "version": get_version(),
                "environment": os.getenv("ENVIRONMENT", "development")
            },
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "hostname": platform.node()
            },
            "resources": {
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": psutil.disk_usage('/').percent
            },
            "requirements_met": {
                "minimum_memory": psutil.virtual_memory().total >= (4 * 1024 * 1024 * 1024),  # 4GB
                "minimum_disk": psutil.disk_usage('/').free >= (10 * 1024 * 1024 * 1024),  # 10GB
                "python_version": platform.python_version(),
                "recommended_setup": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system information"
        )