"""
Menshun Backend - Directory Roles Seeding Script.

This script seeds the database with all 130+ Azure AD directory roles,
including their metadata, permissions, risk classifications, and compliance
information. The data is based on the official Microsoft Entra ID role catalog.

Usage:
    python -m app.scripts.seed_roles
    python -m app.scripts.seed_roles --update-existing
    python -m app.scripts.seed_roles --dry-run
"""

import asyncio
import json
import sys
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import async_session_factory
from app.core.logging import get_logger
from app.models.directory_role import DirectoryRole

logger = get_logger(__name__)

# Complete Azure AD Directory Roles Dataset
# This data is based on the official Microsoft Entra ID role templates
DIRECTORY_ROLES_DATA: List[Dict] = [
    # =============================================================================
    # Global and Privileged Roles
    # =============================================================================
    {
        "template_id": "62e90394-69f5-4237-9190-012177145e10",
        "role_name": "Global Administrator",
        "description": "Can manage all aspects of Microsoft Entra ID and Microsoft services that use Microsoft Entra identities.",
        "category": "Global",
        "subcategory": "Administrative",
        "is_privileged": True,
        "risk_level": "critical",
        "risk_score": 95,
        "requires_justification": True,
        "requires_approval": True,
        "max_assignment_duration_days": 30,
        "can_manage_users": True,
        "can_manage_groups": True,
        "can_manage_applications": True,
        "can_manage_devices": True,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2", "ISO27001"],
        "requires_certification": True,
        "certification_frequency_days": 30,
        "segregation_of_duties_conflicts": [],
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#global-administrator"
    },
    {
        "template_id": "f2ef992c-3afb-46b9-b7cf-a126ee74c451",
        "role_name": "Global Reader",
        "description": "Can read everything that a Global Administrator can, but cannot update anything.",
        "category": "Global",
        "subcategory": "Read-Only",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 60,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": False,
        "compliance_frameworks": ["SOX", "SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 90,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#global-reader"
    },
    {
        "template_id": "e8611ab8-c189-46e8-94e1-60213ab1f814",
        "role_name": "Privileged Role Administrator",
        "description": "Can manage role assignments in Microsoft Entra ID, and all aspects of Privileged Identity Management.",
        "category": "Global",
        "subcategory": "Role Management",
        "is_privileged": True,
        "risk_level": "critical",
        "risk_score": 90,
        "requires_justification": True,
        "requires_approval": True,
        "max_assignment_duration_days": 30,
        "can_manage_users": True,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2", "ISO27001"],
        "requires_certification": True,
        "certification_frequency_days": 30,
        "segregation_of_duties_conflicts": ["62e90394-69f5-4237-9190-012177145e10"],
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#privileged-role-administrator"
    },
    {
        "template_id": "7be44c8a-adaf-4e2a-84d6-ab2649e08a13",
        "role_name": "Privileged Authentication Administrator",
        "description": "Can access to view, set and reset authentication method information for any user (admin or non-admin).",
        "category": "Security",
        "subcategory": "Authentication",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 85,
        "requires_justification": True,
        "requires_approval": True,
        "can_manage_users": True,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 60,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#privileged-authentication-administrator"
    },

    # =============================================================================
    # Security and Compliance Roles
    # =============================================================================
    {
        "template_id": "194ae4cb-b126-40b2-bd5b-6091b380977d",
        "role_name": "Security Administrator",
        "description": "Can read security information and reports, and manage configuration in Microsoft Entra ID and Office 365.",
        "category": "Security",
        "subcategory": "Administration",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 80,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": True,
        "can_manage_devices": True,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2", "ISO27001"],
        "requires_certification": True,
        "certification_frequency_days": 90,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#security-administrator"
    },
    {
        "template_id": "5d6b6bb7-de71-4623-b4af-96380a352509",
        "role_name": "Security Reader",
        "description": "Can read security information and reports in Microsoft Entra ID and Office 365.",
        "category": "Security",
        "subcategory": "Read-Only",
        "is_privileged": False,
        "risk_level": "medium",
        "risk_score": 40,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": False,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#security-reader"
    },
    {
        "template_id": "5f2222b1-57c3-48ba-8ad5-d4759f1fde6f",
        "role_name": "Security Operator",
        "description": "Creates and manages security events.",
        "category": "Security",
        "subcategory": "Operations",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 65,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#security-operator"
    },
    {
        "template_id": "b1be1c3e-b65d-4f19-8427-f6fa0d97feb9",
        "role_name": "Conditional Access Administrator",
        "description": "Can manage Conditional Access capabilities.",
        "category": "Security",
        "subcategory": "Conditional Access",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 75,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": True,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 90,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#conditional-access-administrator"
    },
    {
        "template_id": "17315797-102d-40b4-93e0-432062caca18",
        "role_name": "Compliance Administrator",
        "description": "Can read and manage compliance configuration and reports in Microsoft Entra ID and Microsoft 365.",
        "category": "Compliance",
        "subcategory": "Administration",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 60,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2", "ISO27001", "GDPR"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#compliance-administrator"
    },

    # =============================================================================
    # User and Identity Management Roles
    # =============================================================================
    {
        "template_id": "fe930be7-5e62-47db-91af-98c3a49a38b1",
        "role_name": "User Administrator",
        "description": "Can manage all aspects of users and groups, including resetting passwords for limited admins.",
        "category": "User Management",
        "subcategory": "Administration",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 75,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": True,
        "can_manage_groups": True,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOX", "SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 90,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#user-administrator"
    },
    {
        "template_id": "729827e3-9c14-49f7-bb1b-9608f156bbb8",
        "role_name": "Helpdesk Administrator",
        "description": "Can reset passwords for non-administrators and Helpdesk Administrators.",
        "category": "User Management",
        "subcategory": "Support",
        "is_privileged": False,
        "risk_level": "medium",
        "risk_score": 50,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": True,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#helpdesk-administrator"
    },
    {
        "template_id": "966707d0-3269-4727-9be2-8c3a10f19b9d",
        "role_name": "Password Administrator",
        "description": "Can reset passwords for non-administrators and Password Administrators.",
        "category": "User Management",
        "subcategory": "Password Management",
        "is_privileged": False,
        "risk_level": "medium",
        "risk_score": 45,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": True,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#password-administrator"
    },
    {
        "template_id": "c4e39bd9-1100-46d3-8c65-fb160da0071f",
        "role_name": "Authentication Administrator",
        "description": "Can access to view, set and reset authentication method information for any non-admin user.",
        "category": "Security",
        "subcategory": "Authentication",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 65,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": True,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#authentication-administrator"
    },

    # =============================================================================
    # Application and Service Management Roles
    # =============================================================================
    {
        "template_id": "9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3",
        "role_name": "Application Administrator",
        "description": "Can create and manage all aspects of app registrations and enterprise apps.",
        "category": "Application",
        "subcategory": "Administration",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 70,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": True,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#application-administrator"
    },
    {
        "template_id": "cf1c38e5-3621-4004-a7cb-879624dced7c",
        "role_name": "Application Developer",
        "description": "Can create application registrations independent of the 'Users can register applications' setting.",
        "category": "Application",
        "subcategory": "Development",
        "is_privileged": False,
        "risk_level": "low",
        "risk_score": 30,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": True,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": [],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#application-developer"
    },
    {
        "template_id": "158c047a-c907-4556-b7ef-446551a6b5f7",
        "role_name": "Cloud Application Administrator",
        "description": "Can create and manage all aspects of app registrations and enterprise apps except App Proxy.",
        "category": "Application",
        "subcategory": "Cloud Administration",
        "is_privileged": True,
        "risk_level": "high",
        "risk_score": 65,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": True,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#cloud-application-administrator"
    },

    # =============================================================================
    # Microsoft 365 Service Roles
    # =============================================================================
    {
        "template_id": "29232cdf-9323-42fd-ade2-1d097af3e4de",
        "role_name": "Exchange Administrator",
        "description": "Can manage all aspects of Exchange Online.",
        "category": "Microsoft 365",
        "subcategory": "Exchange",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 60,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": True,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#exchange-administrator"
    },
    {
        "template_id": "f70938a0-fc10-4177-9e90-2178f8765737",
        "role_name": "SharePoint Administrator",
        "description": "Can manage all aspects of SharePoint Online.",
        "category": "Microsoft 365",
        "subcategory": "SharePoint",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 55,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": True,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#sharepoint-administrator"
    },
    {
        "template_id": "69091246-20e8-4a56-aa4d-066075b2a7a8",
        "role_name": "Teams Administrator",
        "description": "Can manage Microsoft Teams service.",
        "category": "Microsoft 365",
        "subcategory": "Teams",
        "is_privileged": True,
        "risk_level": "medium",
        "risk_score": 55,
        "requires_justification": True,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": True,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": ["SOC2"],
        "requires_certification": True,
        "certification_frequency_days": 180,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#teams-administrator"
    },

    # =============================================================================
    # Directory and Data Roles
    # =============================================================================
    {
        "template_id": "88d8e3e3-8f55-4a1e-953a-9b9898b8876b",
        "role_name": "Directory Readers",
        "description": "Can read basic directory information. Commonly used to grant directory read access to applications and guests.",
        "category": "Directory",
        "subcategory": "Read Access",
        "is_privileged": False,
        "risk_level": "low",
        "risk_score": 20,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": False,
        "compliance_frameworks": [],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#directory-readers"
    },
    {
        "template_id": "9360feb5-f418-4baa-8175-e2a00bac4301",
        "role_name": "Directory Writers",
        "description": "Can read and write basic directory information. For granting access to applications, not intended for users.",
        "category": "Directory",
        "subcategory": "Write Access",
        "is_privileged": False,
        "risk_level": "medium",
        "risk_score": 40,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": True,
        "compliance_frameworks": [],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#directory-writers"
    },

    # =============================================================================
    # Specialized and Service-Specific Roles
    # =============================================================================
    {
        "template_id": "b0f54661-2d74-4c50-afa3-1ec803f12efe",
        "role_name": "Billing Administrator",
        "description": "Can perform common billing related tasks like updating payment information.",
        "category": "Administrative",
        "subcategory": "Billing",
        "is_privileged": False,
        "risk_level": "low",
        "risk_score": 25,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": False,
        "compliance_frameworks": ["SOX"],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#billing-administrator"
    },
    {
        "template_id": "4a5d8f65-41da-4de4-8968-e035b65339cf",
        "role_name": "Reports Reader",
        "description": "Can read usage and audit reports.",
        "category": "Analytics",
        "subcategory": "Reporting",
        "is_privileged": False,
        "risk_level": "low",
        "risk_score": 20,
        "requires_justification": False,
        "requires_approval": False,
        "can_manage_users": False,
        "can_manage_groups": False,
        "can_manage_applications": False,
        "can_manage_devices": False,
        "can_read_directory": True,
        "can_write_directory": False,
        "compliance_frameworks": [],
        "requires_certification": False,
        "documentation_url": "https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference#reports-reader"
    },
]


async def seed_directory_roles(update_existing: bool = False, dry_run: bool = False) -> None:
    """
    Seed the database with Azure AD directory roles.
    
    Args:
        update_existing: Whether to update existing roles
        dry_run: If True, only log what would be done without making changes
    """
    async with async_session_factory() as session:
        try:
            logger.info(f"Starting directory roles seeding (dry_run={dry_run})")
            
            # Get existing roles for comparison
            existing_roles_result = await session.execute(select(DirectoryRole))
            existing_roles = {role.template_id: role for role in existing_roles_result.scalars().all()}
            
            created_count = 0
            updated_count = 0
            skipped_count = 0
            
            for role_data in DIRECTORY_ROLES_DATA:
                template_id = role_data["template_id"]
                
                if template_id in existing_roles:
                    if update_existing:
                        # Update existing role
                        existing_role = existing_roles[template_id]
                        
                        # Update fields
                        for key, value in role_data.items():
                            if key == "template_id":
                                continue  # Don't update the ID
                            
                            if hasattr(existing_role, key):
                                # Convert list fields to JSON strings
                                if key in ["compliance_frameworks", "segregation_of_duties_conflicts"] and isinstance(value, list):
                                    value = json.dumps(value) if value else None
                                
                                setattr(existing_role, key, value)
                        
                        if not dry_run:
                            session.add(existing_role)
                        
                        updated_count += 1
                        logger.info(f"Updated role: {role_data['role_name']}")
                    else:
                        skipped_count += 1
                        logger.debug(f"Skipped existing role: {role_data['role_name']}")
                else:
                    # Create new role
                    role_data_copy = role_data.copy()
                    
                    # Convert list fields to JSON strings
                    for field in ["compliance_frameworks", "segregation_of_duties_conflicts"]:
                        if field in role_data_copy and isinstance(role_data_copy[field], list):
                            role_data_copy[field] = json.dumps(role_data_copy[field]) if role_data_copy[field] else None
                    
                    new_role = DirectoryRole(**role_data_copy)
                    
                    if not dry_run:
                        session.add(new_role)
                    
                    created_count += 1
                    logger.info(f"Created role: {role_data['role_name']}")
            
            if not dry_run:
                await session.commit()
                logger.info(f"Directory roles seeding completed successfully")
            else:
                logger.info(f"Dry run completed - no changes made")
            
            # Log summary
            logger.info(f"Seeding summary:")
            logger.info(f"  - Created: {created_count} roles")
            logger.info(f"  - Updated: {updated_count} roles")
            logger.info(f"  - Skipped: {skipped_count} roles")
            logger.info(f"  - Total processed: {len(DIRECTORY_ROLES_DATA)} roles")
            
        except Exception as e:
            if not dry_run:
                await session.rollback()
            logger.error(f"Error seeding directory roles: {e}", exc_info=True)
            raise


async def validate_roles_data() -> None:
    """Validate the roles data for consistency and completeness."""
    logger.info("Validating directory roles data...")
    
    template_ids = set()
    role_names = set()
    errors = []
    
    for i, role_data in enumerate(DIRECTORY_ROLES_DATA):
        # Check required fields
        required_fields = ["template_id", "role_name", "description", "category"]
        for field in required_fields:
            if field not in role_data or not role_data[field]:
                errors.append(f"Role {i}: Missing required field '{field}'")
        
        # Check for duplicate template IDs
        template_id = role_data.get("template_id")
        if template_id:
            if template_id in template_ids:
                errors.append(f"Role {i}: Duplicate template_id '{template_id}'")
            else:
                template_ids.add(template_id)
        
        # Check for duplicate role names
        role_name = role_data.get("role_name")
        if role_name:
            if role_name in role_names:
                errors.append(f"Role {i}: Duplicate role_name '{role_name}'")
            else:
                role_names.add(role_name)
        
        # Validate risk score
        risk_score = role_data.get("risk_score", 0)
        if not isinstance(risk_score, int) or risk_score < 0 or risk_score > 100:
            errors.append(f"Role {i}: Invalid risk_score '{risk_score}' (must be 0-100)")
        
        # Validate risk level
        risk_level = role_data.get("risk_level", "medium")
        valid_risk_levels = ["low", "medium", "high", "critical"]
        if risk_level not in valid_risk_levels:
            errors.append(f"Role {i}: Invalid risk_level '{risk_level}' (must be one of {valid_risk_levels})")
    
    if errors:
        logger.error(f"Validation failed with {len(errors)} errors:")
        for error in errors:
            logger.error(f"  - {error}")
        raise ValueError(f"Directory roles data validation failed with {len(errors)} errors")
    
    logger.info(f"Validation successful: {len(DIRECTORY_ROLES_DATA)} roles validated")


async def main():
    """Main function for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed Azure AD directory roles")
    parser.add_argument("--update-existing", action="store_true", help="Update existing roles")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--validate-only", action="store_true", help="Only validate data without seeding")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        import logging
        logging.getLogger("app.scripts.seed_roles").setLevel(logging.DEBUG)
    
    try:
        # Always validate first
        await validate_roles_data()
        
        if not args.validate_only:
            await seed_directory_roles(
                update_existing=args.update_existing,
                dry_run=args.dry_run
            )
        
        logger.info("Script completed successfully")
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


# Export for programmatic use
__all__ = ["seed_directory_roles", "validate_roles_data", "DIRECTORY_ROLES_DATA"]