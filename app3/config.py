from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


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
    NEOMODEL_DATABSE_URL: Optional[str] = None

    @validator("NEO4J_URI_SCHEME")
    def get_enum_val(cls, v: Neo4jUriScheme) -> str:
        return v.value

    @validator("NEOMODEL_DATABSE_URL", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        s = f"{values.get('NEO4J_URI_SCHEME')}://"
        s += f"{values.get('NEO4J_USER')}:"
        s += f"{values.get('NEO4J_PASSWORD')}@"
        s += f"{values.get('NEO4J_SERVER')}"
        return s

    class Config:
        case_sensitive = True


settings = Settings()
