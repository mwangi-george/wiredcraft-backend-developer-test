import os
from dotenv import load_dotenv
load_dotenv()


class EnvVars:
    """
    Class for managing environment variables.

    Environment variables are classified based on the mode the app will be running - either "dev" or "prod
    """

    def __init__(self, running_in_production: bool = False) -> None:
        """Initialize the class instance in development mode"""
        self.running_in_production = running_in_production

    def _get_env_var(self, production_key: str, development_key: str) -> str:
        """Function to get the relevant environment variable based on the mode the app is running in."""
        return os.getenv(production_key if self.running_in_production else development_key)

    @property
    def db_url(self) -> str:
        return self._get_env_var("DEV_DB_URL", "PROD_DB_URL")


env_vars = EnvVars()