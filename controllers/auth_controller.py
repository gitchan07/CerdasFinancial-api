from flask import Blueprint, request
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.users import Users
from datetime import datetime, timezone
import uuid
from utils.validators import Validators
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)


auth_controller = Blueprint("auth_controller", __name__)
Session = sessionmaker(connection)
@auth_controller.route("/api/v1/register", methods=["POST"])
def register():
    try: 
        session = Session()
        email = request.form["email"]
        full_name = request.form["full_name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        check_email = session.query(Users).filter(Users.email == email).first()
        if check_email:
            return {
                "message": "Email already exists",
            }, 400

        if not Validators.is_valid(email):
            return {
                "message": "Invalid email"
            }, 400

        if not email or not full_name or not password or not confirm_password:
            return {
                "message": "All fields are required"
            }, 400
        
        if not Validators.is_valid_password(password):
            return {
                "message": "password must min 8 length, have capital word and minimum 1 number"
            }, 400
        
        if password != confirm_password:
            return {
                "message": "Passwords do not match"
            }, 400
        

        
        NewUser = Users(
            id = str(uuid.uuid4()),
            email=email,
            full_name=full_name,
            password=password
        )
        NewUser.set_password(password)
   
        session.add(NewUser)
        session.commit()

        return {
            "message": "User created successfully"
        }, 201
    except KeyError: 
        session.rollback()
        return {
            "message": "Invalid request"
        }, 400
    finally:
        session.close()
    

@auth_controller.route("/api/v1/login", methods=["POST"])
def login():
    try:
        email = request.form["email"]
        password = request.form["password"]

        session = Session()
        user = session.query(Users).filter(Users.email==email).first()

        if not user:
            return {
                "message": "User not found"
                }, 404
        if not user.check_password(password):
            return {
                "message": "Invalid password"
                }, 401
        
        print(user.id)
        
        access_token = create_access_token(identity=user.id, additional_claims={
            "email": user.email,
            "fullname": user.full_name
        })

        refresh_token = create_refresh_token(identity=user.id)
        return {
            "users": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            },
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200

        

    except KeyError:
        return {
            "message": "Invalid request"
        }, 400
    finally:
        session.close()

@auth_controller.route("/api/v1/me", methods=["GET"])
@jwt_required()
def me():
    try:
        session = Session()
        user_id = get_jwt_identity()
        user = session.query(Users).filter(Users.id==user_id).first()
        if not user:
            return {
                "message": "User not found"
                }, 
    
        if user.is_subscribe == 1 and user.subscribe_time is not None:
            today = datetime.now(timezone.utc).astimezone(timezone.utc)
            days = (user.expired_time.astimezone(timezone.utc) - today).days
            
        days_expires = days if user.is_subscribe == 1 else 0
        return {
            "users": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_susbscribe": "Yes" if user.is_subscribe == 1 else "No",
                "day_before_expire": days_expires
            }
        }, 200
    except Exception as e:
        return {
            "msg": "error getting user",
            "error": str(e)
        }

@auth_controller.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {
        "access_token": access_token
    }, 200

@auth_controller.route("/api/v1/change", methods=["POST"])
@jwt_required()
def change_password():
    try:
        session = Session()
        user_id = get_jwt_identity()
        user = session.query(Users).filter(Users.id == user_id).first()
        if not user:
            return {
                "message": "User not found"
            }, 404

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        
        if not user.check_password(old_password):
            return {
                "message": "Old password is incorrect"
            }, 400

        user.set_password(new_password)
        session.commit()

        return {
            "message": "Password changed successfully"
        }, 200
    except Exception as e:
        return {
            "msg": "error changing password",
            "error": str(e)
        }, 500
    


