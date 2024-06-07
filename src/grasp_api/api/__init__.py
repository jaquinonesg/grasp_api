from os import getenv

from dotenv import load_dotenv

from grasp_api.config.main import Settings

load_dotenv(getenv("ENV_FILE"))
settings = Settings()  # type: ignore
