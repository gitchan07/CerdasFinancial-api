from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.courses import Course
from models.content_course import ContentCourses

courses_controller = Blueprint("courses_controller", __name__)
Session = sessionmaker(bind=connection)

@courses_controller.route("/api/v1/courses/<string:course_id>", methods=["GET"])
@jwt_required()
def get_course_by_id(course_id):
    session = Session()
    try:
        course = session.query(Course).filter_by(id=course_id).first()
        if not course:
            return jsonify({"data": "Course Not Found"}), 404

        content_list = session.query(ContentCourses).filter_by(course_id=course.id).all()

        if not content_list:
            return jsonify({
                "course_id": course.id,
                "course_name": course.name,
                "course_description": course.description,
                "content": [],
                "message": "No content available for this course."
            }), 200

        content_data = [
            {
                "content_id": content.id,
                "name": content.name,
                "description": content.description,
                "video_url": content.video_url
            } for content in content_list
        ]

        response = {
            "course_id": course.id,
            "course_name": course.name,
            "course_description": course.description,
            "content": content_data
        }

        return jsonify({"data": response}), 200

    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

    finally:
        session.close()
