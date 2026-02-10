from .auth import router as auth_router
from .detection import router as detection_router

__all__ = ["auth_router", "detection_router"]