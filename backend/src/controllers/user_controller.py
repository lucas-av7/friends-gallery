from flask import request, current_app
from src.middlewares import require_user
from src.models import User
from passlib.hash import sha256_crypt
from src.utils import response


def create_user():
    try:
        data = request.get_json()
        user = User(**data)
        user.validate()
        user["is_admin"] = False
        user["password"] = sha256_crypt.hash(user["password"])
        user.save()

        return response(msg="Record created successfully", code=201, data=user.to_dict())
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


def create_admin_user():
    secret_key = current_app.config.get("SECRET_KEY")

    try:
        data = request.get_json()

        if "secret_key" not in data or data["secret_key"] != secret_key:
            return response(msg="Could not verify", code=401)

        del data["secret_key"]

        user = User(**data)
        user.validate()
        user["is_admin"] = True
        user["password"] = sha256_crypt.hash(user["password"])
        user.save()

        return response(msg="Record created successfully", code=201, data=user.to_dict())
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def get_user(current_user, id):
    if current_user.is_admin or str(current_user.id) == id:
        try:
            user = User.objects(id=id).first()
            if user:
                return response(msg="Record retrieved successfully", code=200, data=user.to_dict())
            return response(msg="Record not found", code=404)
        except Exception as err:
            return response(msg="Unable to execute", code=400, err=err)
    return response(msg="Could not verify", code=401)


@require_user
def delete_user(current_user, id):
    if current_user.is_admin or str(current_user.id) == id:
        try:
            user = User.objects(id=id).first()
            if user:
                user.delete()
                return response(msg="Record deleted successfully", code=200)
            return response(msg="Record not found", code=404)
        except Exception as err:
            return response(msg="Unable to execute", code=400, err=err)
    return response(msg="Could not verify", code=401)
