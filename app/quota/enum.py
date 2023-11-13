from enum import Enum


class QuotaType(Enum):
    """Possibile Quota types."""

    BLOCK_STORAGE: str = "block-storage"
    COMPUTE: str = "compute"
    NETWORK: str = "network"
