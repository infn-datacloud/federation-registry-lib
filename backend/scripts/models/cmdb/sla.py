from app.provider.schemas_extended import SLACreateExtended
from app.sla.schemas import SLAQuery, SLARead


class SLAWrite(SLACreateExtended):
    ...


class SLARead(SLARead):
    ...


class SLAQuery(SLAQuery):
    ...
