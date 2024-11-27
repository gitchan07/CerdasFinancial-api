from flask import Blueprint, request
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.users import Users
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
        user = session.query(Users).filter(email==email).first()

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

@auth_controller.route("/api/v1/me", methods=["POST"])
@jwt_required()
def me():
    try:
        session = Session()
        user_id = get_jwt_identity()
        user = session.query(Users).filter(user_id==user_id).first()
        if not user:
            return {
                "message": "User not found"
                }, 404
        return {
            "users": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }, 200
    except KeyError:
        return {
            
        }