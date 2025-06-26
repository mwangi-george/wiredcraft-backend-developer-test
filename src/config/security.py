import enum
from datetime import timedelta, datetime, timezone

import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger
from src.database import User, get_db
from .env_vars import env_vars

class AccessTokenPurpose(str, enum.Enum):
    """Represent possible access token purposes."""
    LOGIN = "LOGIN"
    REGISTRATION = "REGISTRATION"
    PASSWORD_RESET = "PASSWORD_RESET"


class Security:
    """Main security class providing methods for handling app security function."""

    # OAuth2PasswordBearer is a class provided by FastAPI that facilitates implementing the OAuth 2.0 password flow for token-based authentication, by declaring a security scheme that expects a bearer token in the Authorization header.
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Function to hash a string password."""
        try:
            encoded_password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            return hashed_password.decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to hash password: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to hash password")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Function to verify a string password."""
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception as e:
            logger.error(f"Could not verify credentials: {str(e)}")
            raise HTTPException(status_code=400, detail="Could not verify credentials")

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
        """Function to get a user by id."""
        db_results = await db.execute(select(User).where(User.email == email))
        user=db_results.scalars().one_or_none()
        return user

    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> User | bool:
        """Function to authenticate a user by email and password."""
        user = await self.get_user_by_email(email, db)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, purpose: AccessTokenPurpose):
        """Function to create authentication token based on use"""
        try:
            to_encode = data.copy()
            if purpose == AccessTokenPurpose.LOGIN:
                expires = datetime.now(timezone.utc) + timedelta(minutes=env_vars.access_token_expiry_in_minutes)
            elif purpose == AccessTokenPurpose.PASSWORD_RESET:
                expires = datetime.now(timezone.utc) + timedelta(minutes=env_vars.password_reset_token_expiry_in_minutes)
            else:
                expires = datetime.now(timezone.utc) + timedelta(minutes=30)

            to_encode.update({"exp": expires})
            encoded_jwt = jwt.encode(to_encode, env_vars.JWT_SECRET_KEY, algorithm=env_vars.ALGORITHM)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Failed to create access token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )


    async def get_current_user(
            self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ) -> User:
        """Function to get a user from a token passed in request authorization header."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        try:
            payload = jwt.decode(token=token, key=env_vars.JWT_SECRET_KEY, algorithms=[env_vars.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user: User = await self.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


# instantiate security class
security = Security()