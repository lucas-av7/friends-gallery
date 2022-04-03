from .user_routes import user_bp
from .photo_routes import photo_bp
from .comment_routes import comment_bp

__all__ = ["photo_bp", "comment_bp", "user_bp"]
