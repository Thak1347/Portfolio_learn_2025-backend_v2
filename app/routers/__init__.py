from .auth import router as auth_router
from .posts import router as posts_router
from .certificates import router as certificates_router
from .skills import router as skills_router

__all__ = ["auth_router", "posts_router", "certificates_router", "skills_router"]