from app.service.schemas import ServiceCreate, ServiceQuery, ServiceRead
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.endpoint}"


class ServiceWrite(ServiceCreate):
    pass


class ServiceRead(ServiceRead):
    pass


class ServiceQuery(ServiceQuery):
    pass
