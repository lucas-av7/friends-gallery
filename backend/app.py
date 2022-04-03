import os

from flask import Flask
from flask_cors import CORS

from src.auth import login
from src.config.db_config import db_init
from src.routes import comment_bp, photo_bp, user_bp
from src.utils import response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_pyfile("src/config/settings.py")

with app.app_context():
    db_init()

app.url_map.strict_slashes = False

app.add_url_rule("/api/auth/login", "login", login, methods=["POST"])

app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(photo_bp, url_prefix="/api/photos")
app.register_blueprint(comment_bp, url_prefix="/api/comments")


# Custom error response for all api endpoints
@app.errorhandler(405)
def not_allowed(e):
    return response(msg="Method not allowed", code=405)


@app.errorhandler(404)
def not_found(e):
    return response(msg="API endpoint not found", code=404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
