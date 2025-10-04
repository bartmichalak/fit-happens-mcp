from functools import lru_cache

from dotenv import find_dotenv
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(usecwd=True),
        env_file_encoding="utf-8",
        extra="ignore",
        # default env_file solution search .env every time BaseSettings is instantiated
        # dotenv search .env when module is imported, without usecwd it starts from the file it was called
    )

    # API SETTINGS
    api_name: str = f"fit-happens-mcp API"
    api_v1: str = "/api/v1"
    api_latest: str = api_v1
    paging_limit: int = 100



    # MCP SETTINGS
    mcp_server_name: str = f"MCP Server"


    # 0. pytest ini_options
    # 1. environment variables
    # 2. .env
    # 3. default values in pydantic settings


@lru_cache()
def _get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = _get_settings()
