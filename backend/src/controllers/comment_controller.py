from src.middlewares import require_user
from src.models import Comment, Photo
from flask import request

from src.utils import response


@require_user
def create_comment(current_user, photo_id):
    try:
        if not Photo.objects(id=photo_id, approved=True):
            return response(msg="Photo not found", code=404)

        data = request.get_json()
        data["user"] = current_user
        data["photo"] = photo_id
        comment = Comment(**data)
        comment.save()
        return response(msg="Record created successfully", code=201, data=comment.to_dict())

    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def delete_comment(current_user, id):
    try:
        comment = Comment.objects(id=id).first()
        if comment:
            if current_user.is_admin or current_user.id == comment.user.id:
                comment.delete()
                return response(msg="Record deleted successfully", code=200)
            return response(msg="Could not verify", code=401)
        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def like_comment(current_user, id):
    try:
        user_id = str(current_user.id)
        comment = Comment.objects(id=id).first()
        if comment:
            if user_id in comment.likes:
                comment.update(pull__likes=user_id)
            else:
                comment.update(push__likes=user_id)
            return response(msg="Record updated successfully", code=200)

        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)
