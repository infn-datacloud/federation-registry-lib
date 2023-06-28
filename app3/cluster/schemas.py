from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class ClusterQuery(BaseNodeQuery):
    """Cluster Query Model class.

    Attributes:
        description (str | None): Brief description.
    """


class ClusterCreate(BaseNodeCreate):
    """Cluster Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
    """


class ClusterUpdate(ClusterCreate):
    """Cluster Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
    """


class Cluster(BaseNodeRead, ClusterCreate):
    """Cluster class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
    """
