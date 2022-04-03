from mongoengine import connect
from flask import current_app


def db_init():
    db_uri = current_app.config.get("MONGODB_URI")
    connect(host=db_uri)
