"""
WatchSphere AI v3.0 - Frontend Authentication API Client
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from typing import Optional, Dict, Any, Tuple
import requests
from config.settings import settings
from config.database import SessionLocal
from backend.services.auth_service import AuthService
from backend.schemas.auth_schema import LoginRequest
from config.logging import logger


class AuthClient:
    """
    Frontend authentication client interfacing with backend JWT authentication engine.
    """

    @staticmethod
    def login(email: str, password: str, vendor_company: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]], Optional[str]]:
        """
        Attempts to authenticate user via HTTP REST API endpoint or direct Service fallback.
        Returns: (success: bool, message: str, user_profile: dict, access_token: str)
        """
        api_url = f"http://{settings.HOST}:{settings.PORT}{settings.API_V1_PREFIX}/auth/login"
        payload = {
            "email": email.lower().strip(),
            "password": password,
            "vendor_company": vendor_company.strip() if vendor_company else None
        }

        # 1. Attempt HTTP REST API Call
        try:
            response = requests.post(api_url, json=payload, timeout=3)
            if response.status_code == 200:
                resp_json = response.json()
                token_data = resp_json.get("data", {})
                access_token = token_data.get("access_token")
                user_profile = {
                    "email": token_data.get("email", email),
                    "full_name": token_data.get("full_name", "User"),
                    "role": token_data.get("user_role", "user"),
                    "vendor_company": token_data.get("vendor_company")
                }
                return True, "Authentication successful", user_profile, access_token
        except Exception:
            logger.info("REST API endpoint unavailable; falling back to direct in-process database authentication.")

        # 2. Fallback to direct DB AuthService
        db = SessionLocal()
        try:
            auth_service = AuthService(db)
            login_req = LoginRequest(
                email=email,
                password=password,
                vendor_company=vendor_company
            )
            token, user = auth_service.login(login_req)
            user_profile = {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "vendor_company": user.vendor_company
            }
            return True, "Authentication successful", user_profile, token.access_token
        except Exception as e:
            logger.warning(f"In-process authentication failed: {str(e)}")
            return False, f"Login failed: {str(e)}", None, None
        finally:
            db.close()
