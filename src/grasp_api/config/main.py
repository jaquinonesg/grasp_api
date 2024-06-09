from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    grasp_api_db_host: str
    grasp_api_db_port: str
    grasp_api_db_environment: str
    grasp_api_db_local_name: str
    grasp_api_db_name: str
    grasp_api_db_user: str
    grasp_api_db_password: str

    grasp_api_db_ro_host: str
    grasp_api_db_ro_port: str
    grasp_api_db_ro_environment: str
    grasp_api_db_ro_local_name: str
    grasp_api_db_ro_name: str
    grasp_api_db_ro_user: str
    grasp_api_db_ro_password: str

    class Config:
        env_file = "api.env"


settings = Settings()  # type: ignore


def filter_settings(prefix):
    filtered_settings = {
        attr[len(prefix) :]: value
        for attr, value in settings.dict().items()  # type: ignore
        if attr.startswith(prefix)
    }
    return filtered_settings
