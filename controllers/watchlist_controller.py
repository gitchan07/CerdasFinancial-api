from flask import Blueprint, request, jsonify
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.watchlist import Watchlist
from models.courses import Course
from models.users import Users
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

watchlist_controller = Blueprint("watchlist_controller", __name__)
Session = sessionmaker(bind=connection)

@watchlist_controller.route("/api/v1/list", methods=["GET"])
@jwt_required()
def get_watchlist():
    try:
        session = Session()
        user_id = get_jwt_identity()
        watchlist_items = session.query(Watchlist).filter_by(user_id=user_id).all()

        if not watchlist_items:
            return jsonify({"message": "No items in watchlist"}), 404
        
        result = [
            {
                "course_id": item.course.id,
                "course_title": item.course.title,
                "description": item.course.description
            } for item in watchlist_items
        ]

        return jsonify({"data": result}), 200

    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    finally:
        session.close()


@watchlist_controller.route("/api/v1/list", methods=["POST"])
@jwt_required()
def add_to_watchlist():
    try:
        session = Session()
        user_id = get_jwt_identity()
        course_id = request.json.get("course_id")

        course = session.query(Course).filter_by(id=course_id).first()
        if not course:
            return jsonify({"message": "Course not found"}), 404

        existing_entry = session.query(Watchlist).filter_by(user_id=user_id, course_id=course_id).first()
        if existing_entry:
            return jsonify({"message": "Course already in watchlist"}), 400

        new_watchlist_item = Watchlist(id=str(uuid.uuid4()), user_id=user_id, course_id=course_id)
        session.add(new_watchlist_item)
        session.commit()

        return jsonify({"message": "Course added to watchlist"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    finally:
        session.close()


@watchlist_controller.route("/api/v1/list/<string:watchlist_id>", methods=["DELETE"])
@jwt_required()
def delete_from_watchlist(watchlist_id):
    try:
        session = Session()
        user_id = get_jwt_identity()

        watchlist_item = session.query(Watchlist).filter_by(id=watchlist_id, user_id=user_id).first()

        if not watchlist_item:
            return jsonify({"message": "Item not found in watchlist"}), 404

        session.delete(watchlist_item)
        session.commit()

        return jsonify({"message": "Course removed from watchlist"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    finally:
        session.close()
