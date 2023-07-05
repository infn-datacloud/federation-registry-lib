from fastapi import FastAPI, APIRouter
from fastapi import Depends, Request
from fastapi.security import HTTPBasicCredentials
from oldapp.auth import flaat, security
from oldapp import main
from oldapp.dao.providers import ProviderDAO, Provider

router = APIRouter(
    prefix="/providers",
    tags=["providers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
@flaat.is_authenticated()
def getAllProviders(
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
    ) -> list[Provider]:
    user_infos = flaat.get_user_infos_from_request(request)
    dao = ProviderDAO(main.db)
    return dao.all()

@router.get("/{name}", response_model_exclude_unset=True)
@flaat.is_authenticated()
def getProvider(
        name: str,
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
    ) -> Provider:
    #user_infos = flaat.get_user_infos_from_request(request)
    dao = ProviderDAO(main.db)
    return dao.find_by_id(name)

@router.post("/")
@flaat.is_authenticated()
def addProvider(
        provider: Provider,
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
    ):
    user_infos = flaat.get_user_infos_from_request(request)
    dao = ProviderDAO(main.db)
    return dao.add(provider)

@router.delete("/{name}")
@flaat.is_authenticated()
def removeProvider(
        name: str,
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security),
    ):
    user_infos = flaat.get_user_infos_from_request(request)
    dao = ProviderDAO(main.db)
    return dao.remove(name)

