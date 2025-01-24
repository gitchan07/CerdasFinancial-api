from flask import Blueprint, request, jsonify
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.subscribe import Subscribe
from models.subscribe_type import SubscribeType
from models.users import Users
from datetime import datetime, timezone, timedelta
import uuid
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from service.subcription_transaction import create_midtrans_transaction


subscribe_controller = Blueprint("subscribe_controller", __name__)
Session = sessionmaker(connection)
@subscribe_controller.route("/api/v1/subscribe", methods=["POST"])
@jwt_required()
def register():
    try: 
        current_user_id = get_jwt_identity()
        session = Session()
        subscribe_id = request.form.get("subscribe_id")

        if not subscribe_id:
            return {
                "message": "Input price"
            }, 400
        
        check_subscribe = session.query(SubscribeType).filter(SubscribeType.id == subscribe_id).first()
        if not check_subscribe:
            return {
                "message": "Subscribe type not found"
            }, 404
        duration_month = check_subscribe.duration
        current_time = datetime.now(timezone.utc)
        expired_time = current_time + timedelta(days=duration_month * 30)

        new_subscribe = Subscribe(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            subscribe_id=subscribe_id,
            subscribe_date=current_time
        )
        session.add(new_subscribe)

        user = session.query(Users).filter(Users.id == current_user_id).first()
        if not user:
            session.rollback()
            return {
                "message": "User not found"
            }, 404

        user.is_subscribe = 1
        user.subscribe_time = current_time
        user.expired_time = expired_time

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

# subcribe type 
@subscribe_controller.route("/api/v1/subscribe/type", methods=["POST"])
@jwt_required()
def adding_subscribe_type():
    try:
        s = Session()
        id = str(uuid.uuid4())
        duration = request.form.get("duration")
        price = request.form.get("price")

        if not duration or not price:
            return {
                "message": "Input duration and price"
            }, 400
        
        new_subscribe_type = SubscribeType(
            id=id,
            duration=duration,
            price=price
        )
        s.add(new_subscribe_type)
        s.commit()
        return {
            "message": "Subscribe type added successfully"
        }, 201
    except Exception as e:
        return {
            "message": f"An error occurred: {str(e)}"
        }, 500
    finally:
        s.close()

@subscribe_controller.route("/api/v1/subscribe/type", methods=["GET"])
@jwt_required()
def get_all_subscribe_type():
    try:
        s = Session()
        subscribe_type = s.query(SubscribeType).order_by(SubscribeType.duration.asc()).all()
        subscribe_type_list = [
            {
                "id": st.id,
                "duration": st.duration,
                "price": st.price
            } for st in subscribe_type
        ]
        return {
            "data": subscribe_type_list
        }, 200
    except Exception as e:
        return {
            "message": f"An error occurred: {str(e)}"
        }, 500
    finally:
        s.close()

@subscribe_controller.route("/api/v1/subscribe/midtrans", methods=["POST"])
@jwt_required()
def midtrans_payment():
    try:
        user_id = get_jwt_identity()
        subscribe_id = request.form.get("subscribe_id")

        transaction_token = create_midtrans_transaction(user_id, subscribe_id)

        return jsonify({
            "transaction_token": transaction_token
        }), 200

    except ValueError as e:
        return jsonify({
            "message": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500