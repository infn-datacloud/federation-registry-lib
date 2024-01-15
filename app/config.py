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
    @classmethod
    def get_enum_val(cls, v: Neo4jUriScheme) -> str:
        """Retrive the string from the enum value."""
        return v.value

    @validator("NEOMODEL_DATABASE_URL")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Before checking the DB URL, assemble the target DB uri from single parts."""
        if isinstance(v, AnyUrl):
            s = v
        else:
            s = f"{values.get('NEO4J_URI_SCHEME')}://"
            s += f"{values.get('NEO4J_USER')}:"
            s += f"{values.get('NEO4J_PASSWORD')}@"
            s += f"{values.get('NEO4J_SERVER')}"

        # Set the DB uri for this application
        config.DATABASE_URL = s
        return s

    MAINTAINER_NAME: Optional[str] = None
    MAINTAINER_URL: Optional[AnyHttpUrl] = None
    MAINTAINER_EMAIL: Optional[EmailStr] = None

    ADMIN_EMAIL_LIST: List[EmailStr] = []
    TRUSTED_IDP_LIST: List[AnyHttpUrl] = []

    DOC_V1_URL: Optional[AnyHttpUrl] = None

    @validator("DOC_V1_URL", pre=True)
    @classmethod
    def create_doc_url(cls, v: Optional[AnyHttpUrl], values: Dict[str, Any]) -> str:
        """Build URL for internal documentation."""
        if isinstance(v, AnyUrl):
            return str(v)
        protocol = "http"
        return f"{protocol}://{values.get('DOMAIN')}{values.get('API_V1_STR')}/docs"

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
