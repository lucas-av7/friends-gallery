from flask import Blueprint
from src.middlewares import require_json_request

from src.controllers import user_controller as user_c

user_bp = Blueprint("user", __name__)

user_bp.before_request(require_json_request)

user_bp.add_url_rule("/", "create_user", user_c.create_user, methods=["POST"])
user_bp.add_url_rule("/admin", "create_admin_user", user_c.create_admin_user, methods=["POST"])
user_bp.add_url_rule("/<id>", "get_user", user_c.get_user, methods=["GET"])
user_bp.add_url_rule("/<id>", "delete_user", user_c.delete_user, methods=["DELETE"])
