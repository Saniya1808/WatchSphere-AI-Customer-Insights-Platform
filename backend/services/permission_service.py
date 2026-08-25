"""
WatchSphere AI v3.0 - Permission & RBAC Governance Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Dict, List, Any


class PermissionService:
    """
    Manages Role-Based Access Control (RBAC) matrix definitions.
    """

    @staticmethod
    def get_permission_matrix() -> Dict[str, Dict[str, bool]]:
        """Returns the system RBAC permission matrix mapping roles to module permissions."""
        return {
            "Admin": {
                "Catalog Access": True, "Commerce Access": True, "AI Engine Access": True,
                "User Management": True, "System Backup": True, "API Key Admin": True
            },
            "Vendor": {
                "Catalog Access": False, "Commerce Access": True, "AI Engine Access": True,
                "User Management": False, "System Backup": False, "API Key Admin": False
            },
            "Manager": {
                "Catalog Access": True, "Commerce Access": True, "AI Engine Access": True,
                "User Management": False, "System Backup": False, "API Key Admin": False
            },
            "Analyst": {
                "Catalog Access": False, "Commerce Access": True, "AI Engine Access": True,
                "User Management": False, "System Backup": False, "API Key Admin": False
            }
        }
