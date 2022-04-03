from flask import Blueprint
from src.middlewares import require_json_request

from src.controllers import photo_controller as photo_c

photo_bp = Blueprint("photo", __name__)

photo_bp.before_request(require_json_request)

photo_bp.add_url_rule("/", "create_photo", photo_c.create_photo, methods=["POST"])
photo_bp.add_url_rule("/", "get_photos", photo_c.get_photos, methods=["GET"])
photo_bp.add_url_rule("/pending-photos", "get_pending_photos", photo_c.get_pending_photos, methods=["GET"])
photo_bp.add_url_rule("/<id>", "get_photo", photo_c.get_photo, methods=["GET"])
photo_bp.add_url_rule("/<id>", "delete_photo", photo_c.delete_photo, methods=["DELETE"])
photo_bp.add_url_rule("/<id>/approve", "approve_photo", photo_c.approve_photo, methods=["POST"])
photo_bp.add_url_rule("/<id>/like", "like_photo", photo_c.like_photo, methods=["POST"])
