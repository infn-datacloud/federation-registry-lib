from app.service.models import (
    Service,
    NovaService as NovaService,
    MesosService as MesosService,
    ChronosService as ChronosService,
    MarathonService as MarathonService,
    KubernetesService as KubernetesService,
    RucioService as RucioService,
    OneDataService as OneDataService,
)
from app.service.schemas import (
    ServiceCreate,
    ServiceUpdate,
    NovaServiceCreate,
    NovaServiceUpdate,
    MesosServiceCreate,
    MesosServiceUpdate,
    ChronosServiceCreate,
    ChronosServiceUpdate,
    MarathonServiceCreate,
    MarathonServiceUpdate,
    KubernetesServiceCreate,
    KubernetesServiceUpdate,
    RucioServiceCreate,
    RucioServiceUpdate,
    OneDataServiceCreate,
    OneDataServiceUpdate,
)
from app.crud import CRUDBase


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    """"""


class CRUDNovaService(
    CRUDBase[NovaService, NovaServiceCreate, NovaServiceUpdate]
):
    """"""


class CRUDMesosService(
    CRUDBase[MesosService, MesosServiceCreate, MesosServiceUpdate]
):
    """"""


class CRUDChronosService(
    CRUDBase[ChronosService, ChronosServiceCreate, ChronosServiceUpdate]
):
    """"""


class CRUDMarathonService(
    CRUDBase[MarathonService, MarathonServiceCreate, MarathonServiceUpdate]
):
    """"""


class CRUDKubernetesService(
    CRUDBase[
        KubernetesService,
        KubernetesServiceCreate,
        KubernetesServiceUpdate,
    ]
):
    """"""


class CRUDRucioService(
    CRUDBase[RucioService, RucioServiceCreate, RucioServiceUpdate]
):
    """"""


class CRUDOneDataService(
    CRUDBase[OneDataService, OneDataServiceCreate, OneDataServiceUpdate]
):
    """"""


service = CRUDService(Service, ServiceCreate)
nova_service = CRUDNovaService(NovaService, NovaServiceCreate)
mesos_service = CRUDMesosService(MesosService, MesosServiceCreate)
chronos_service = CRUDChronosService(ChronosService, ChronosServiceCreate)
marathon_service = CRUDMarathonService(MarathonService, MarathonServiceCreate)
kubernetes_service = CRUDKubernetesService(
    KubernetesService, KubernetesServiceCreate
)
rucio_service = CRUDRucioService(RucioService, RucioServiceCreate)
onedata_service = CRUDOneDataService(OneDataService, OneDataServiceCreate)
