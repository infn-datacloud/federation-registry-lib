from typing import Any, Dict, Optional, Union

from app.crud import CRUDBase
from app.provider.models import Provider
from app.quota.crud import quota
from app.service.models import KubernetesService, NovaService, Service
from app.service.schemas import (
    KubernetesServiceCreate,
    KubernetesServiceRead,
    KubernetesServiceReadPublic,
    KubernetesServiceReadShort,
    KubernetesServiceUpdate,
    NovaServiceCreate,
    NovaServiceRead,
    NovaServiceReadPublic,
    NovaServiceReadShort,
    NovaServiceUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceReadPublic,
    ServiceReadShort,
    ServiceUpdate,
)
from app.service.schemas_extended import (
    KubernetesServiceReadExtended,
    NovaServiceReadExtended,
)


class CRUDService(
    CRUDBase[
        Service,
        ServiceCreate,
        ServiceUpdate,
        ServiceRead,
        ServiceReadPublic,
        ServiceReadShort,
        None,
    ]
):
    """"""

    def create(
        self, *, obj_in: ServiceCreate, provider: Provider, force: bool = False
    ) -> Service:
        if isinstance(obj_in, NovaServiceCreate):
            db_obj = nova_service.create(obj_in=obj_in, force=force)
        # elif isinstance(obj_in, MesosServiceCreate):
        #    db_obj = mesos_service.create(obj_in=obj_in, force=force)
        # elif isinstance(obj_in, ChronosServiceCreate):
        #    db_obj = chronos_service.create(obj_in=obj_in, force=force)
        # elif isinstance(obj_in, MarathonServiceCreate):
        #    db_obj = marathon_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, KubernetesServiceCreate):
            db_obj = kubernetes_service.create(obj_in=obj_in, force=force)
        # elif isinstance(obj_in, RucioServiceCreate):
        #    db_obj = rucio_service.create(obj_in=obj_in, force=force)
        # elif isinstance(obj_in, OneDataServiceCreate):
        #    db_obj = onedata_service.create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Service) -> bool:
        if isinstance(db_obj, NovaService):
            return nova_service.remove(db_obj=db_obj)
        # elif isinstance(db_obj, MesosService):
        #    return mesos_service.remove(db_obj=db_obj)
        # elif isinstance(db_obj, ChronosService):
        #    return chronos_service.remove(db_obj=db_obj)
        # elif isinstance(db_obj, MarathonService):
        #    return marathon_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, KubernetesService):
            return kubernetes_service.remove(db_obj=db_obj)
        # elif isinstance(db_obj, RucioService):
        #    return rucio_service.remove(db_obj=db_obj)
        # elif isinstance(db_obj, OneDataService):
        #    return onedata_service.remove(db_obj=db_obj)

    def update(
        self, *, db_obj: Service, obj_in: Union[ServiceUpdate, Dict[str, Any]]
    ) -> Optional[Service]:
        if isinstance(db_obj, NovaService):
            return nova_service.update(db_obj=db_obj, obj_in=obj_in)
        # elif isinstance(db_obj, MesosService):
        #    return mesos_service.update(db_obj=db_obj, obj_in=obj_in)
        # elif isinstance(db_obj, ChronosService):
        #    return chronos_service.update(db_obj=db_obj, obj_in=obj_in)
        # elif isinstance(db_obj, MarathonService):
        #    return marathon_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, KubernetesService):
            return kubernetes_service.update(db_obj=db_obj, obj_in=obj_in)
        # elif isinstance(db_obj, RucioService):
        #    return rucio_service.update(db_obj=db_obj, obj_in=obj_in)
        # elif isinstance(db_obj, OneDataService):
        #    return onedata_service.update(db_obj=db_obj, obj_in=obj_in)


class CRUDNovaService(
    CRUDBase[
        NovaService,
        NovaServiceCreate,
        NovaServiceUpdate,
        NovaServiceRead,
        NovaServiceReadPublic,
        NovaServiceReadShort,
        NovaServiceReadExtended,
    ]
):
    """"""

    def remove(self, *, db_obj: NovaService) -> bool:
        for item in db_obj.num_cpu_quotas.all():
            quota.remove(item)
        for item in db_obj.ram_quotas.all():
            quota.remove(item)
        return super().remove(db_obj=db_obj)


# class CRUDMesosService(
#    CRUDBase[MesosService, MesosServiceCreate, MesosServiceUpdate]
# ):
#    """"""


# class CRUDChronosService(
#    CRUDBase[ChronosService, ChronosServiceCreate, ChronosServiceUpdate]
# ):
#    """"""


# class CRUDMarathonService(
#    CRUDBase[MarathonService, MarathonServiceCreate, MarathonServiceUpdate]
# ):
#    """"""


class CRUDKubernetesService(
    CRUDBase[
        KubernetesService,
        KubernetesServiceCreate,
        KubernetesServiceUpdate,
        KubernetesServiceRead,
        KubernetesServiceReadPublic,
        KubernetesServiceReadShort,
        KubernetesServiceReadExtended,
    ]
):
    """"""

    def remove(self, *, db_obj: KubernetesService) -> bool:
        for item in db_obj.num_cpu_quotas.all():
            quota.remove(item)
        for item in db_obj.ram_quotas.all():
            quota.remove(item)
        return super().remove(db_obj=db_obj)


# class CRUDRucioService(
#    CRUDBase[RucioService, RucioServiceCreate, RucioServiceUpdate]
# ):
#    """"""


# class CRUDOneDataService(
#    CRUDBase[OneDataService, OneDataServiceCreate, OneDataServiceUpdate]
# ):
#    """"""


service = CRUDService(
    model=Service,
    create_schema=ServiceCreate,
    read_schema=ServiceRead,
    read_public_schema=ServiceReadPublic,
    read_short_schema=ServiceReadShort,
    read_extended_schema=None,
)
nova_service = CRUDNovaService(
    model=NovaService,
    create_schema=NovaServiceCreate,
    read_schema=NovaServiceRead,
    read_public_schema=NovaServiceReadPublic,
    read_short_schema=NovaServiceReadShort,
    read_extended_schema=NovaServiceReadExtended,
)
# mesos_service = CRUDMesosService(MesosService, MesosServiceCreate)
# chronos_service = CRUDChronosService(ChronosService, ChronosServiceCreate)
# marathon_service = CRUDMarathonService(MarathonService, MarathonServiceCreate)
kubernetes_service = CRUDKubernetesService(
    model=KubernetesService,
    create_schema=KubernetesServiceCreate,
    read_schema=KubernetesServiceRead,
    read_public_schema=KubernetesServiceReadPublic,
    read_short_schema=KubernetesServiceReadShort,
    read_extended_schema=KubernetesServiceReadExtended,
)
# rucio_service = CRUDRucioService(RucioService, RucioServiceCreate)
# onedata_service = CRUDOneDataService(OneDataService, OneDataServiceCreate)
