import enum
from datetime import date

from pydantic import BaseModel, EmailStr, Field

class TextResponse(BaseModel):
    """Used for formatting simple text responses."""
    detail: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Response from action"
            }
        }
    }


class UserAddress(BaseModel):
    """Used for formatting user address."""
    name: str
    latitude: float
    longitude: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "123 Main St.",
                "latitude": 40.75,
                "longitude": -73.75,
            }
        }
    }


class NewUser(BaseModel):
    """Class contains information required to create a new user"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)
    name: str = Field(min_length=4, max_length=30)
    dob: date = Field(default=date.today())
    address: UserAddress | None = Field(default=None)
    description: str = Field(max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john_doe@gmail.com",
                "password": "qwerty1234",
                "name": "John Doe",
                "dob": "1970-01-01",
                "address": {
                    "name": "123 Main St.",
                    "latitude": 40.75,
                    "longitude": -73.75,
                },
                "description": "A passionate software engineer",
            }
        }
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "<KEY>",
                "token_type": "Bearer",
            }
        }
    }


class UserFieldsEnum(str, enum.Enum):
    email = "email"
    name = "name"
    dob = "dob"
    description = "description"


class UpdateUser(BaseModel):
    user_id: str  # field to use in updating
    field: UserFieldsEnum
    value: str | date

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "HCxFdfvYCBrK45sFTEo9wH",
                "field": "email",
                "value": "john.doe@gmail.com",
            }
        }
    }


class UserInfo(BaseModel):
    email: str
    name: str
    dob: date
    address: dict
    description: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "<EMAIL>",
                "name": "<NAME>",
                "dob": "1970-01-01",
                "address": {
                    "name": "123 Main St.",
                    "latitude": 40.75,
                    "longitude": -73.75,
                },
                "description": "A passionate software engineer",
            }
        }
    }