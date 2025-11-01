# This file makes scripts/utils a Python package
# Expose key modules for import

from .cloud_services import call_cloud_service, CLOUD_SERVICES
from .utils import call_multi_cloud

# Optional: Import and expose other useful functions
# from .config import get_config
# from .debug_env import debug_environment

__all__ = [
    'call_cloud_service',
    'CLOUD_SERVICES',
    'call_multi_cloud'
]
