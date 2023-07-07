from .models import (
    Service as ServiceModel,
    NovaService as NovaServiceModel,
    MesosService as MesosServiceModel,
    ChronosService as ChronosServiceModel,
    MarathonService as MarathonServiceModel,
    KubernetesService as KubernetesServiceModel,
    RucioService as RucioServiceModel,
    OneDataService as OneDataServiceModel,
)
from .schemas import (
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
from ..crud import CRUDBase

class CRUDService(
    CRUDBase[ServiceModel, ServiceCreate, ServiceUpdate]
):
    """"""


class CRUDNovaService(
    CRUDBase[NovaServiceModel, NovaServiceCreate, NovaServiceUpdate]
):
    """"""


class CRUDMesosService(
    CRUDBase[MesosServiceModel, MesosServiceCreate, MesosServiceUpdate]
):
    """"""


class CRUDChronosService(
    CRUDBase[ChronosServiceModel, ChronosServiceCreate, ChronosServiceUpdate]
):
    """"""


class CRUDMarathonService(
    CRUDBase[
        MarathonServiceModel, MarathonServiceCreate, MarathonServiceUpdate
    ]
):
    """"""


class CRUDKubernetesService(
    CRUDBase[
        KubernetesServiceModel,
        KubernetesServiceCreate,
        KubernetesServiceUpdate,
    ]
):
    """"""


class CRUDRucioService(
    CRUDBase[RucioServiceModel, RucioServiceCreate, RucioServiceUpdate]
):
    """"""


class CRUDOneDataService(
    CRUDBase[OneDataServiceModel, OneDataServiceCreate, OneDataServiceUpdate]
):
    """"""


service = CRUDService(ServiceModel, ServiceCreate)
nova_service = CRUDNovaService(NovaServiceModel, NovaServiceCreate)
mesos_service = CRUDMesosService(MesosServiceModel, MesosServiceCreate)
chronos_service = CRUDChronosService(ChronosServiceModel, ChronosServiceCreate)
marathon_service = CRUDMarathonService(
    MarathonServiceModel, MarathonServiceCreate
)
kubernetes_service = CRUDKubernetesService(
    KubernetesServiceModel, KubernetesServiceCreate
)
rucio_service = CRUDRucioService(RucioServiceModel, RucioServiceCreate)
onedata_service = CRUDOneDataService(OneDataServiceModel, OneDataServiceCreate)
