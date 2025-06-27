from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from src.config.security import security, AccessTokenPurpose
from src.database import User
from src.schemas.users import NewUser, TextResponse, LoginResponse, UpdateUser, UserInfo


class UserService:
    """Class for user management business logic"""

    @staticmethod
    async def handle_create_user(new_user: NewUser, db: AsyncSession) -> TextResponse:
        """Function to persist new user to database"""

        # step 1: Check if email is already taken
        existing_user = await security.get_user_by_email(new_user.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {new_user.email} already exists",
            )

        try:
            # step 2: Create new user
            new_user = User(**new_user.model_dump())

            # step 3: Hash new user's password
            new_user.password = security.get_password_hash(new_user.password)

            # step 4: Add new users data to db and commit changes to persist
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            # step 5: return formatted confirmation
            return TextResponse(detail=f"User with email {new_user.email} created successfully")
        except SQLAlchemyError as s:
            logger.exception(f"SQLAlchemyError occurred: {str(s)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create new user. Please try again or contact support.")
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create new user. Please try again or contact support.")

    @staticmethod
    async def handle_login_user(email: str, password: str, db: AsyncSession) -> LoginResponse:
        """Function to log in a user"""

        # step 1: authenticate
        user = await security.authenticate_user(email, password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        # step 2: create access token
        access_token = security.create_access_token({"sub": user.email}, purpose=AccessTokenPurpose.LOGIN)

        # step 3: format response
        response = LoginResponse(access_token=access_token, token_type="bearer")
        return response

    @staticmethod
    async def handle_update_user(updated_data: UpdateUser, db: AsyncSession) -> TextResponse:
        """Function to update an existing user's data"""
        # step 1: retrieve user's data
        db_results = await db.execute(select(User).filter_by(id=updated_data.user_id))
        existing_user = db_results.scalars().one_or_none()
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist")

        try:
            # step 2: convert the updated data pydantic model to dict
            data_to_update = updated_data.model_dump(exclude_unset=True)

            # Step 3: Update the user's data based on the new data fields and values
            if data_to_update["field"] in existing_user.__dict__:
                logger.info("Updating existing user")
                setattr(existing_user, data_to_update["field"], data_to_update["value"])

            # step 4: add the data to the database and commit to persist changes
            db.add(existing_user)
            await db.commit()
            await db.refresh(existing_user)

            # step 5: format the confirmation response
            return TextResponse(
                detail=f"{data_to_update['field'].value} updated successfully to "
                       f"{getattr(existing_user, data_to_update['field'])}"
            )
        except SQLAlchemyError as s:
            logger.exception(f"SQLAlchemyError occurred: {str(s)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update user. Please try again or contact support.")
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update user. Please try again or contact support.")

    @staticmethod
    async def handle_remove_user(user_id: str, db: AsyncSession) -> TextResponse:
        """Function to remove a logged-in user"""

        # step 1: Check if user exists
        db_results = await db.execute(select(User).filter_by(id=user_id))
        user = db_results.scalars().one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist")

        # step 2: remove user from db if they exist
        try:
            await db.delete(user)
            await db.commit()

            # step 3: format the confirmation message
            return TextResponse(detail=f"User with id {user_id} removed successfully")
        except SQLAlchemyError as s:
            logger.exception(f"SQLAlchemyError occurred: {str(s)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not remove user. Please try again or contact support."
            )
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not remove user. Please try again or contact support."
            )

    @staticmethod
    async def handle_get_user_by_id(user_id: str, db: AsyncSession) -> UserInfo:
        """Function to fetch a user's information"""

        try:
            # step 1: fetch user from database
            db_results = await db.execute(select(User).filter_by(id=user_id))
            user = db_results.scalars().one_or_none()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist")

            # step 2: return validated user data
            return UserInfo(**user.__dict__)
        except SQLAlchemyError as s:
            logger.exception(f"SQLAlchemyError occurred: {str(s)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not fetch user. Please try again or contact support."
            )
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not fetch user. Please try again or contact support."
            )


user_service = UserService()