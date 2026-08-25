"""
WatchSphere AI v3.0 - Authentication & Authorization Routes
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db
from config.constants import ResponseStatus
from backend.schemas.user_schema import UserCreate, UserResponse
from backend.schemas.auth_schema import LoginRequest, Token
from backend.schemas.response_schema import APIResponse
from backend.services.user_service import UserService
from backend.services.auth_service import AuthService
from backend.auth.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])


@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration"
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new system user, vendor, or administrator account.
    """
    user_service = UserService(db)
    created_user = user_service.create(user_in)
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="User registered successfully",
        data=UserResponse.model_validate(created_user)
    )


@router.post(
    "/login",
    response_model=APIResponse[Token],
    status_code=status.HTTP_200_OK,
    summary="User Authentication Login"
)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates user credentials and issues a signed JWT Bearer Token.
    """
    auth_service = AuthService(db)
    token, user = auth_service.login(login_data)
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="Authentication successful",
        data=token
    )


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Current Active Profile"
)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieves the currently authenticated user's profile metadata.
    """
    return APIResponse(
        status=ResponseStatus.SUCCESS,
        message="User profile retrieved successfully",
        data=UserResponse.model_validate(current_user)
    )
