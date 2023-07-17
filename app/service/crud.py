from app.service.models import (
    Service as ServiceModel,
    NovaService as NovaServiceModel,
    MesosService as MesosServiceModel,
    ChronosService as ChronosServiceModel,
    MarathonService as MarathonServiceModel,
    KubernetesService as KubernetesServiceModel,
    RucioService as RucioServiceModel,
    OneDataService as OneDataServiceModel,
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
from app.service.enum import ServiceType
from app.crud import CRUDBase


class CRUDService(CRUDBase[ServiceModel, ServiceCreate, ServiceUpdate]):
    """"""

    def create(
        self, *, obj_in: ServiceCreate, force: bool = False
    ) -> ServiceModel:
        if obj_in.type == ServiceType.openstack_nova.value:
            return nova_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.mesos.value:
            return mesos_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.chronos.value:
            return chronos_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.marathon.value:
            return marathon_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.kubernetes.value:
            return kubernetes_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.rucio.value:
            return rucio_service.create(obj_in=obj_in, force=force)
        elif obj_in.type == ServiceType.onedata.value:
            return onedata_service.create(obj_in=obj_in, force=force)
        return super().create(obj_in=obj_in, force=force)


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
