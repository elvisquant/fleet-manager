# FILE: app/routes/user.py
# Verify this is the new version by seeing this comment.

from fastapi import APIRouter, BackgroundTasks, Depends, status, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import the User model from its correct location in the models directory
from app.models.user import User

from app.config.database import get_session
from app.responses.user import UserResponse, LoginResponse
from app.schemas.user import RegisterUserRequest, ResetRequest, VerifyUserRequest, EmailRequest
from app.services import user
from app.config.security import get_current_user, oauth2_scheme

# Router for public user actions like registration
user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

# Router for protected actions that require a valid token
auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

# Router for authentication actions like login/logout
guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    return await user.create_user_account(data, session, background_tasks)

@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await user.activate_user_account(data, session, background_tasks)
    return JSONResponse(content={"message": "Account is activated successfully."})

# This is the route that was causing the error. It is now fixed.
# It correctly uses the modern Pydantic/FastAPI conventions.
@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return await user.get_login_token(data, session)

@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token: str = Header(), session: Session = Depends(get_session)):
    return await user.get_refresh_token(refresh_token, session)


@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await user.email_forgot_password_link(data, background_tasks, session)
    return JSONResponse(content={"message": "If an account with that email exists, a password reset link has been sent."})

@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
    await user.reset_user_password(data, session)
    return JSONResponse(content={"message": "Your password has been updated successfully."})

@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_info(pk: int, session: Session = Depends(get_session)):
    return await user.fetch_user_detail(pk, session)