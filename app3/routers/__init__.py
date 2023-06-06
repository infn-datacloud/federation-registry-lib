from .flavor import router as flavors_router
from .identity_provider import router as identity_providers_router
from .image import router as images_router
from .project import router as projects_router
from .provider import router as providers_router
#from .quota import router as quotas_router
#from .service import router as services_router
#from .sla import router as slas_router
from .user_group import router as user_groups_router

__all__ = [
    "flavors_router",
    "identity_providers_router",
    "images_router",
    "projects_router",
    "providers_router",
    "quotas_router",
    "services_router",
    "slas_router",
    "user_groups_router",
]
