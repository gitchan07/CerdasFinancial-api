
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from db import db
from config.database import connection
from flask_jwt_extended import JWTManager
from controllers.auth_controller import auth_controller
from controllers.watchlist_controller import watchlist_controller
from datetime import timedelta
import os

from models.category import Category
from models.content_course import ContentCourses
from models.subscribe import Subscribe
from models.courses_category import CourseCategory
load_dotenv()

migrate = Migrate()
app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("TOKEN_EXPIRES")))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv("REFRESH_TOKEN_EXPIRES")))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_controller)
app.register_blueprint(watchlist_controller)
@app.route("/")
def index():
    return "API working!"

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return {
        "msg": "Token has expired",
        "status": 401
    }

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return {
        "msg": "Invalid token",
        "status": 401
    }

@jwt.unauthorized_loader
def missing_token_callback(reason):
    return {
        "msg": "Missing token",
        "status": 401
    }


@app.errorhandler(404)
def not_found(error=None):
    return {"message": "Resource not found", "status": 404}, 404

if __name__ == "__main__":
    app.run(debug=True)