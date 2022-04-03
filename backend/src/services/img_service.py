import base64
from abc import ABC

import boto3
import requests
from src.utils import random_file_name
from flask import current_app


class StorageProvider(ABC):
    def upload(self, base64_img):
        pass

    def delete(self, delete_key):
        pass


class S3Provider(StorageProvider):
    def __init__(self):
        self.s3_bucket = current_app.config.get("AWS_S3_BUCKET")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=current_app.config.get("AWS_SECRET_KEY"),
        )

    def upload(self, base64_img):
        try:
            file_name = random_file_name(20, "jpg")
            self.s3_client.put_object(Body=base64.b64decode(base64_img), Bucket=self.s3_bucket, Key=file_name)
            object_url = f"https://{self.s3_bucket}.s3.amazonaws.com/{file_name}"
            result = {
                "url": object_url,
                "delete_key": file_name
            }

            return result
        except Exception as err:
            return err

    def delete(self, delete_key):
        try:
            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=delete_key)
            return True
        except Exception:
            return False


class IMGBBProvider(StorageProvider):
    def __init__(self):
        self.api_key = current_app.config.get("IMGBB_API_KEY")

    def upload(self, base64_img):
        payload = {"key": self.api_key}
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params=payload,
            data={"image": base64_img}
        )
        response = response.json()

        if "data" in response:
            result = {
                "url": response["data"]["url"],
                "delete_key": response["data"]["delete_url"]
            }
            return result
        return False

    def delete(self, delete_key):
        payload = {"key": self.api_key}
        requests.delete(delete_key, params=payload)

        # IMGBB doesn't handle deletes well
        return True


class ImgService:
    def __init__(self, service: StorageProvider):
        self.service = service

    def upload(self, base64_img):
        return self.service.upload(base64_img)

    def delete(self, delete_key):
        return self.service.delete(delete_key)
