import datetime
import shortuuid
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

# Define base class for which all database models will inherit from
Base = declarative_base()


class User(Base):
    """
    Represents a user in the database.

    This class maps to the 'users' table and stores information about a user.
    """
    __tablename__ = "users"

    id = Column(String(22), primary_key=True, index=True, unique=True, default=shortuuid.uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)  # Extra unique field for use in signing in
    password = Column(String(255), nullable=False)  # Extra field for use in signing
    dob = Column(Date, nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now)
    updated_at = Column(Date, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
