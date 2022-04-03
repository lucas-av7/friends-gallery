from datetime import datetime, timedelta

import jwt
from flask import request, current_app
from src.models import User
from passlib.hash import sha256_crypt
from src.utils import response


def login():
    secret_key = current_app.config.get("SECRET_KEY")

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return response(msg="Incomplete authorization object", code=401)

    try:
        user = User.objects(email=auth.username).first()
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)

    if user and sha256_crypt.verify(auth.password, user["password"]):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=30),
            "iat": datetime.utcnow(),
            "sub": str(user["id"])
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        data = {
            "user": user.to_dict(),
            "token": token,
            "exp": payload["exp"]
        }

        return response(msg="Validated successfuly", code=200, data=data)
    return response(msg="Could not verify", code=401)


def get_user_id_from_token():
    secret_key = current_app.config.get("SECRET_KEY")

    try:
        auth_header = request.headers.get("Authorization")
        pieces = auth_header.split(" ")
        token = pieces[1]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = data["sub"]
        return user_id
    except Exception:
        return None
