from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.security import HTTPBasicCredentials
from app.auth import flaat, security
from app import main
from app.dao.services import ServiceDAO, Service

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@flaat.is_authenticated()
def getAllServices(
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
        ) -> list[Service]:
    user_infos = flaat.get_user_infos_from_request(request)
    dao = ServiceDAO(main.db)
    return dao.all()


@router.post("/")
@flaat.is_authenticated()
def addService(
        service: Service,
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
        ):
    user_infos = flaat.get_user_infos_from_request(request)
    dao = ServiceDAO(main.db)
    return dao.add(service)
