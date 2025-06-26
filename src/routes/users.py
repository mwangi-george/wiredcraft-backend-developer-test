from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, User
from src.schemas.users import TextResponse, NewUser, LoginResponse, UpdateUser
from src.services.users import user_service
from src.config.security import security


def create_users_router() -> APIRouter:
    """Function to create the user management endpoints"""
    router = APIRouter(prefix="/api/v1/users", tags=["User Management"])

    @router.post("/register", response_model=TextResponse, status_code=status.HTTP_201_CREATED)
    async def register_user(new_user: NewUser, db: AsyncSession = Depends(get_db)) -> TextResponse:
        """Endpoint to register a new user"""
        response = await user_service.create_user(new_user, db)
        return response

    @router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
    async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> LoginResponse:
        """Endpoint to log in a user"""
        response = await user_service.login_user(form_data.username, form_data.password, db)
        return response

    @router.post("/update", response_model=TextResponse, status_code=status.HTTP_200_OK)
    async def update_user(
            updated_data: UpdateUser,
            db: AsyncSession = Depends(get_db),
            user: User = Depends(security.get_current_user),
    ) -> TextResponse:
        """Endpoint to update a user"""
        response = await user_service.update_user(user.email, updated_data, db)
        return response

    return router