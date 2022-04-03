import json
from mongoengine import ValidationError, NotUniqueError
import random
import string


def response(msg, code, data=None, err=None):
    response = {
        "status": "Success" if code < 400 else "Error",
        "status_code": code,
        "message": msg,
    }

    if data is not None:
        string_result = json.dumps(data, default=str)
        dict_result = json.loads(string_result)
        response["data"] = dict_result

    if err:
        if isinstance(err, ValidationError):
            response["err"] = err.to_dict()
        elif isinstance(err, NotUniqueError):
            response["err"] = "Some values are not unique to their fields"
        else:
            response["err"] = str(err)

    return response, code


def random_file_name(size, extension="txt"):
    file_name = "".join(random.choice(string.ascii_lowercase) for i in range(size))
    return f"{file_name}.{extension}"
