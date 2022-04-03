from flask import Blueprint
from src.middlewares import require_json_request

from src.controllers import comment_controller as comment_c

comment_bp = Blueprint("comment", __name__)

comment_bp.before_request(require_json_request)

comment_bp.add_url_rule("/<photo_id>", "create_comment", comment_c.create_comment, methods=["POST"])
comment_bp.add_url_rule("/<id>", "delete_comment", comment_c.delete_comment, methods=["DELETE"])
comment_bp.add_url_rule("/<id>/like", "like_photo", comment_c.like_comment, methods=["POST"])
