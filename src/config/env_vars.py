import os
from dotenv import load_dotenv
from loguru import logger

# load environment variables from .env fine
load_dotenv()


class EnvVars:
    """
    Class for managing environment variables.

    Environment variables are classified based on the mode the app is running in- either "dev" or "prod
    """

    # cross-mode variables
    ALGORITHM = os.getenv("ALGORITHM")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    def __init__(self, running_in_production: bool = False) -> None:
        """Initialize the class instance in development mode"""
        self.running_in_production = running_in_production

    def _get_env_var(self, production_key: str, development_key: str) -> str:
        """Function to get the relevant environment variable based on the mode the app is running in."""
        return os.getenv(production_key if self.running_in_production else development_key)

    @property
    def db_url(self) -> str:
        return self._get_env_var("PROD_DB_URL", "DEV_DB_URL")

    @property
    def access_token_expiry_in_minutes(self) -> int:
        return int(self._get_env_var("PROD_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES", "DEV_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES"))

    @property
    def password_reset_token_expiry_in_minutes(self) -> int:
        return int(self._get_env_var("PROD_PASSWORD_RESET_TOKEN_EXPIRY_IN_MINUTES", "DEV_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES"))


env_vars = EnvVars(running_in_production=False)
