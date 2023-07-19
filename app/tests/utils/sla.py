from app.tests.utils.utils import random_datetime, random_lower_string
from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAUpdate


def create_random_sla() -> SLA:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    item_in = SLACreate(
        description=description, start_date=start_date, end_date=end_date
    )
    return sla.create(obj_in=item_in)


def create_random_update_sla_data() -> SLAUpdate:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    return SLAUpdate(
        description=description, start_date=start_date, end_date=end_date
    )
