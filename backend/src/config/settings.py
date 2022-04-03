from os import environ

SECRET_KEY = environ.get("SECRET_KEY")
USE_AWS_S3 = environ.get("USE_AWS_S3")
AWS_S3_BUCKET = environ.get("AWS_S3_BUCKET")
AWS_ACCESS_KEY = environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = environ.get("AWS_SECRET_KEY")
IMGBB_API_KEY = environ.get("IMGBB_API_KEY")
MONGODB_URI = environ.get("MONGODB_URI")
