from flask import Blueprint, request

auth_controller = Blueprint("auth_controller", __name__)
@auth_controller.route("/api/v1/auth/register", methods=["POST"])
def register():
    try: 
        email = request.form["email"]
        full_name = request.form["full_name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return {
                "message": "Passwords do not match"
            }, 400
        


    except KeyError: 
        return {
            "message": "Invalid request"
        }, 400
    

@auth_controller.route("/api/v1/auth/login", methods=["POST"])
def login():
    try:
        email = request.form["email"]
        password = request.form["password"]

    except KeyError:
        return {
            "message": "Invalid request"
        }, 400