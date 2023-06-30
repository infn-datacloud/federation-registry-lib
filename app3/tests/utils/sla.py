from .utils import random_datetime, random_lower_string
from ...sla.crud import sla
from ...sla.models import SLA
from ...sla.schemas import SLACreate


def create_random_sla() -> SLA:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    item_in = SLACreate(
        description=description, start_date=start_date, end_date=end_date
    )
    return sla.create(obj_in=item_in)
