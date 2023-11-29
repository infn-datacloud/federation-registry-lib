from tests.utils.crud import TestBaseCRUD


class TestFlavorCRUD(TestBaseCRUD):
    """Class with the basic API calls to Flavor endpoints."""

    __test__ = True
    controller = "flavor_controller"
    db_item1 = "db_flavor"
    db_item2 = "db_flavor2"
    db_parent1 = "db_compute_serv"
    create_key_params = {"db_parent1": "service"}  # noqa: RUF012
