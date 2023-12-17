"""Module with the configuration parameters."""
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, List, Optional

from neomodel import config
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, EmailStr, validator


class Neo4jUriScheme(Enum):
    """Enumeration with the accepted neo4j schemas."""

    NEO4J: str = "neo4j"
    NEO4JS: str = "neo4j+s"
    BOLT: str = "bolt"
    BOLTS: str = "bolt+s"


class Settings(BaseSettings):
    """Model with the app settings."""

    PROJECT_NAME: str = "Federation-Registry"
    DOMAIN: str = "localhost:8000"
    API_V1_STR: str = "/api/v1"

    NEO4J_SERVER: str = "localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    NEO4J_URI_SCHEME: Neo4jUriScheme = Neo4jUriScheme.BOLT.value
    NEOMODEL_DATABASE_URL: Optional[AnyUrl] = None

    @validator("NEO4J_URI_SCHEME")
    def get_enum_val(cls, v: Neo4jUriScheme) -> str:
        """Retrive the string from the enum value."""
        return v.value

    @validator("NEOMODEL_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> AnyUrl:
        """Before checking the DB URL, assemble the target DB uri from single parts."""
        if isinstance(v, AnyUrl):
            return v
        s = f"{values.get('NEO4J_URI_SCHEME')}://"
        s += f"{values.get('NEO4J_USER')}:"
        s += f"{values.get('NEO4J_PASSWORD')}@"
        s += f"{values.get('NEO4J_SERVER')}"
        return s

    @validator("NEOMODEL_DATABASE_URL")
    def save_db_url(cls, v: Optional[str]) -> AnyUrl:
        """Set the DB uri for this application."""
        config.DATABASE_URL = v
        return v

    ADMIN_EMAIL_LIST: List[EmailStr] = []
    TRUSTED_IDP_LIST: List[AnyHttpUrl] = []

    # @validator("TRUSTED_IDP_LIST")
    # def validate_list(cls, v: List[AnyHttpUrl], values: Dict[str, Any]) -> AnyHttpUrl:
    #     if values.get("ENABLE_AUTH"):
    #         assert (
    #             len(v) > 0
    #         ), "Empty TRUSTED_IDP_LIST when authentication has been enabled"
    #     return v

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200",
    # "http://localhost:3000", "http://localhost:8080",
    # "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    class Config:
        """Sub class to set attribute as case sensitive."""

        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Retrieve cached settings."""
    return Settings()
