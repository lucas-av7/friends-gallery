from functools import wraps
from flask import request
from src.auth import get_user_id_from_token
from src.utils import response
from src.models import User


def require_json_request():
    if request.data and request.method in ["POST", "PUT"] and not request.is_json:
        return response(msg="Payload is not a JSON", code=406)


def require_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_user_id_from_token()
        if not user_id:
            return response(msg="Token is invalid or expired", code=401)

        current_user = User.objects(id=user_id).first()
        if not current_user:
            return response(msg="Could not verify", code=401)

        return f(current_user, *args, **kwargs)
    return decorated
