import requests
from functools import lru_cache
from enum import Enum
from neomodel import config
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, Field, validator
from typing import Any, Dict, List, Optional


class Neo4jUriScheme(Enum):
    NEO4J: str = "neo4j"
    NEO4JS: str = "neo4j+s"
    BOLT: str = "bolt"
    BOLTS: str = "bolt+s"


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"

    NEO4J_SERVER: str = "localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    NEO4J_URI_SCHEME: Neo4jUriScheme = "bolt"
    NEOMODEL_DATABASE_URL: Optional[AnyUrl] = None

    @validator("NEO4J_URI_SCHEME")
    def get_enum_val(cls, v: Neo4jUriScheme) -> str:
        return v.value

    @validator("NEOMODEL_DATABASE_URL", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> AnyUrl:
        if isinstance(v, AnyUrl):
            return v
        s = f"{values.get('NEO4J_URI_SCHEME')}://"
        s += f"{values.get('NEO4J_USER')}:"
        s += f"{values.get('NEO4J_PASSWORD')}@"
        s += f"{values.get('NEO4J_SERVER')}"
        return s

    @validator("NEOMODEL_DATABASE_URL")
    def save_db_url(cls, v: Optional[str]) -> AnyUrl:
        config.DATABASE_URL = v
        return v

    DISCOVERY_URL: Optional[AnyHttpUrl] = None
    CA: Optional[str] = None
    IDP_CONF: Dict[str, Any] = Field(default_factory=dict)
    SCOPES: List[str] = Field(default_factory=list)

    @validator("IDP_CONF", pre=True)
    def get_endpoint(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        if values.get("DISCOVERY_URL") is not None:
            resp = requests.get(
                values.get("DISCOVERY_URL"),
                verify=values.get("CA"),
            )
            return resp.json()
        return {"authorization_endpoint": "", "token_endpoint": ""}

    class Config:
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()
