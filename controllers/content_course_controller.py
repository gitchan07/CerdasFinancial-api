from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.courses import Course
from models.content_course import ContentCourses

contents_controller = Blueprint("contents_controller", __name__)
Session = sessionmaker(bind=connection)

@contents_controller.route("/api/v1/content_courses/<string:content_course_id>", methods=["GET"])
@jwt_required()
def get_content_courses(content_course_id):
    session = Session()
    try:
        content_list = session.query(ContentCourses).filter_by(ContentCourses.id==content_course_id).first()
        if content_list is None:
            return jsonify({"msg": "Content not found"}), 404

        # Serialize the content object
        content_dict = {
            "id": content_list.id,
            "name": content_list.name,
            "description": content_list.description,
            # Add other fields here as needed
        }

        return jsonify({"data": content_dict}), 200

    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    finally:
        session.close()
