from src.services.img_service import ImgService, IMGBBProvider, S3Provider
from src.middlewares import require_user
from src.models import Photo, Comment
from flask import request, current_app

from src.utils import response


@require_user
def create_photo(current_user):
    USE_AWS_S3 = current_app.config.get("USE_AWS_S3")

    img_provider = S3Provider if USE_AWS_S3 == "1" else IMGBBProvider
    img_service = ImgService(img_provider())

    try:
        data = request.get_json()
        data["approved"] = False
        data["user"] = current_user

        if "base64_img" in data:
            result = img_service.upload(data["base64_img"])
            if result:
                data["url"] = result["url"]
                data["delete_key"] = result["delete_key"]
                del data["base64_img"]
                photo = Photo(**data)
                photo.save()
                return response(msg="Record created successfully", code=201, data=photo.to_dict())
        return response(msg="Unable to upload the photo", code=400)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


def get_photo(id):
    try:
        photo = Photo.objects(id=id, approved=True).first()
        if photo:
            comments = [comment.to_dict() for comment in Comment.objects(photo=id)]
            photo = photo.to_dict()
            photo["comments"] = comments
            return response(msg="Records retrieved successfully", code=200, data=photo)
        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


def get_photos():
    try:
        photos = [photo.to_dict() for photo in Photo.objects(approved=True)]

        for photo in photos:
            comments = [comment.to_dict() for comment in Comment.objects(photo=photo["_id"])]
            photo["comments"] = comments

        return response(msg="Records retrieved successfully", code=200, data=photos)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def get_pending_photos(current_user):
    if not current_user.is_admin:
        return response(msg="Could not verify", code=401)
    try:
        photos = [photo.to_dict() for photo in Photo.objects(approved=False)]

        for photo in photos:
            comments = [comment.to_dict() for comment in Comment.objects(photo=photo["_id"])]
            photo["comments"] = comments

        return response(msg="Records retrieved successfully", code=200, data=photos)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def delete_photo(current_user, id):
    USE_AWS_S3 = current_app.config.get("USE_AWS_S3")

    img_provider = S3Provider if USE_AWS_S3 == "1" else IMGBBProvider
    img_service = ImgService(img_provider())

    try:
        photo = Photo.objects(id=id).first()
        if photo:
            if current_user.is_admin or str(current_user.id) == str(photo.user.id):
                result = img_service.delete(photo["delete_key"])
                if result:
                    photo.delete()
                    return response(msg="Record deleted successfully", code=200)
                return response(msg="Unable to delete the photo on the storage service", code=400)
            return response(msg="Could not verify", code=401)
        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def approve_photo(current_user, id):
    if not current_user.is_admin:
        return response(msg="Could not verify", code=401)

    try:
        photo = Photo.objects(id=id).first()
        if photo:
            photo.update(approved=True)
            return response(msg="Record updated successfully", code=200)
        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)


@require_user
def like_photo(current_user, id):
    try:
        user_id = str(current_user.id)
        photo = Photo.objects(id=id).first()
        if photo:
            if user_id in photo.likes:
                photo.update(pull__likes=user_id)
            else:
                photo.update(push__likes=user_id)
            return response(msg="Record updated successfully", code=200)
        return response(msg="Record not found", code=404)
    except Exception as err:
        return response(msg="Unable to execute", code=400, err=err)
