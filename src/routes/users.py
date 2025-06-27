from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, User
from src.schemas.users import TextResponse, NewUser, LoginResponse, UpdateUser, UserInfo
from src.services.users import user_service
from src.config.security import security


def create_users_router() -> APIRouter:
    """Function to create the user management endpoints"""
    router = APIRouter(prefix="/api/v1/users", tags=["User Management"])

    @router.post("/register", response_model=TextResponse, status_code=status.HTTP_201_CREATED)
    async def register_user(new_user: NewUser, db: AsyncSession = Depends(get_db)) -> TextResponse:
        """Endpoint to register a new user"""
        response = await user_service.handle_create_user(new_user, db)
        return response

    @router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
    async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> LoginResponse:
        """Endpoint to log in a user"""
        response = await user_service.handle_login_user(form_data.username, form_data.password, db)
        return response

    @router.patch("/update", response_model=TextResponse, status_code=status.HTTP_200_OK)
    async def update_user(data: UpdateUser, db: AsyncSession = Depends(get_db)) -> TextResponse:
        """Endpoint to update a logged-in user"""
        response = await user_service.handle_update_user(data, db)
        return response

    @router.delete("/{user_id}", response_model=TextResponse, status_code=status.HTTP_200_OK)
    async def remove_user(user_id: str, db: AsyncSession = Depends(get_db)) -> TextResponse:
        """Endpoint to remove a logged-in user"""
        response = await user_service.handle_remove_user(user_id, db)
        return response

    @router.get("/{user_id}", response_model=UserInfo, status_code=status.HTTP_200_OK)
    async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> UserInfo:
        """Endpoint to retrieve a user's information"""
        response = await user_service.handle_get_user_by_id(user_id, db)
        return response

    @router.get("/all", response_model=list[UserInfo], status_code=status.HTTP_200_OK)
    async def get_all_users(start: int, limit: int, db: AsyncSession = Depends(get_db)) -> list[UserInfo]:
        """Endpoint to retrieve all users - paginated"""
        response = await user_service.handle_get_all_users(start, limit, db)
        return response


    return router