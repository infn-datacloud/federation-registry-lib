from app.service.schemas import ServiceCreate, ServiceQuery, ServiceRead
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.endpoint}"


class ServiceWrite(ServiceCreate, Representation):
    pass


class ServiceRead(ServiceRead, Representation):
    pass


class ServiceQuery(ServiceQuery, Representation):
    pass
