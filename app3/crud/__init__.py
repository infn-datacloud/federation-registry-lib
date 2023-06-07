from .flavor import (
    create_flavor,
    connect_flavor_to_project,
    get_flavor,
    get_flavors,
    remove_flavor,
)
from .identity_provider import (
    create_identity_provider,
    get_identity_provider,
    get_identity_providers,
    remove_identity_provider,
)
from .image import (
    create_image,
    get_image,
    connect_image_to_project,
    get_images,
    remove_image,
)
from .project import (
    create_project,
    connect_project_to_user_group,
    get_project,
    get_projects,
    remove_project,
)
from .provider import (
    create_provider,
    get_provider,
    get_providers,
    remove_provider,
)

# from .quota import (
#    create_quota,
#    get_quota,
#    get_quota_by_name,
#    get_quotas,
#    remove_quota,
# )
# from .service import (
#    create_service,
#    get_service,
#    get_service_by_name,
#    get_services,
#    remove_service,
# )
from .sla import (
    create_sla,
    connect_sla_to_project_and_provider,
    get_sla,
    get_slas,
    remove_sla,
)
from .user_group import (
    create_user_group,
    get_user_group,
    get_user_groups,
    remove_user_group,
)

__all__ = [
    "create_flavor",
    "connect_flavor_to_project",
    "get_flavor",
    "get_flavors",
    "get_project_flavors",
    "remove_flavor",
    "create_identity_provider",
    "get_identity_provider",
    "get_identity_providers",
    "remove_identity_provider",
    "create_image",
    "connect_image_to_project",
    "get_image",
    "get_images",
    "remove_image",
    "create_project",
    "connect_project_to_user_group",
    "get_project",
    "get_projects",
    "remove_project",
    "create_provider",
    "get_provider",
    "get_providers",
    "remove_provider",
    "create_quota",
    "get_quota",
    "get_quotas",
    "remove_quota",
    "create_service",
    "get_service",
    "get_services",
    "remove_service",
    "create_sla",
    "connect_sla_to_project_and_provider",
    "get_sla",
    "get_slas",
    "remove_sla",
    "create_user_group",
    "get_user_group",
    "get_user_groups",
    "remove_user_group",
]
