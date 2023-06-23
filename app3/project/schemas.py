from typing import Optional

from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class ProjectQuery(BaseNodeQuery):
    """Project Query Model class.

    Attributes:
        description (str | None): Brief description.
        public_network_name (str | None): TODO
        private_network_name (str | None): TODO
        private_network_proxy_host (str | None): TODO
        private_network_proxy_user (str | None): TODO
    """

    public_network_name: Optional[str] = None
    private_network_name: Optional[str] = None
    private_network_proxy_host: Optional[str] = None
    private_network_proxy_user: Optional[str] = None


class ProjectPatch(BaseNodeCreate):
    """Project Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        public_network_name (str | None): TODO
        private_network_name (str | None): TODO
        private_network_proxy_host (str | None): TODO
        private_network_proxy_user (str | None): TODO
    """

    public_network_name: Optional[str] = None
    private_network_name: Optional[str] = None
    private_network_proxy_host: Optional[str] = None
    private_network_proxy_user: Optional[str] = None


class ProjectCreate(ProjectPatch):
    """Project Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        public_network_name (str | None): TODO
        private_network_name (str | None): TODO
        private_network_proxy_host (str | None): TODO
        private_network_proxy_user (str | None): TODO
    """


class Project(ProjectCreate, BaseNodeRead):
    """Project class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        public_network_name (str | None): TODO
        private_network_name (str | None): TODO
        private_network_proxy_host (str | None): TODO
        private_network_proxy_user (str | None): TODO
    """
