from flask import Blueprint, request
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.subscribe import Subscribe
from models.users import Users
from datetime import datetime, timezone
import uuid
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


subscribe_controller = Blueprint("subscribe_controller", __name__)
Session = sessionmaker(connection)
@subscribe_controller.route("/api/v1/subscribe", methods=["POST"])
@jwt_required()
def register():
    try: 
        current_user_id = get_jwt_identity()
        session = Session()
        price = request.form.get("price")

        if not price:
            return {
                "message": "Input price"
            }, 400

        current_time = datetime.now(timezone.utc)

        new_subscribe = Subscribe(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            price=price,
            subscribe_date=current_time
        )
        session.add(new_subscribe)

        user = session.query(Users).filter(Users.user_id == current_user_id).first()
        if not user:
            session.rollback()
            return {
                "message": "User not found"
            }, 404

        user.is_subscribe = 1
        user.subscribe_date = current_time

        session.commit()

        return {
            "message": "User Subscribed successfully"
        }, 201

    except KeyError: 
        session.rollback()
        return {
            "message": "Invalid request"
        }, 400
    except Exception as e:
        session.rollback()
        return {
            "message": f"An error occurred: {str(e)}"
        }, 500
    finally:
        session.close()