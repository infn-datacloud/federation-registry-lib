from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAUpdate
from app.tests.utils.project import create_random_project
from app.tests.utils.user_group import create_random_user_group
from app.tests.utils.utils import random_datetime, random_lower_string


def create_random_sla() -> SLA:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    item_in = SLACreate(
        description=description, start_date=start_date, end_date=end_date
    )
    return sla.create(
        obj_in=item_in,
        project=create_random_project(),
        user_group=create_random_user_group(),
    )


def create_random_update_sla_data() -> SLAUpdate:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    return SLAUpdate(
        description=description, start_date=start_date, end_date=end_date
    )
