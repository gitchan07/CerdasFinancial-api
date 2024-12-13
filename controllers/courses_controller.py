from flask import Blueprint, request
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.courses import Course
from models.content_course import ContentCourses
from models.courses_category import CourseCategory
from models.users import Users
from datetime import datetime, timedelta
from minio import Minio
import os
import uuid

minio_client = Minio(
    os.getenv("MINIO_URL"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)
bucket_name = os.getenv("MINIO_BUCKET_NAME")


from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

courses_controller = Blueprint("courses_controller", __name__)
Session = sessionmaker(bind=connection)


@courses_controller.route("/api/v1/courses", methods=["GET"])
@jwt_required()
def get_all_courses():
    current_user = Users.query.filter_by(id=get_jwt_identity()).first()
    if not current_user:
        return {"message": "User not found"}, 404
    session = Session()
    try:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        offset = (page - 1) * limit
        name = request.args.get("name")

        if name:
            courses = session.query(Course).filter(Course.name.like("%"+name+"%")).offset(offset).limit(limit).all()
            total_courses = session.query(Course).filter(Course.name.like("%"+name+"%")).count()
        else:
            courses = session.query(Course).offset(offset).limit(limit).all()
            total_courses = session.query(Course).count()

        if not courses:
            return {"message": "No courses found"}, 404

        courses_json = [
            {
                key: getattr(course, key) if key != "video_url" else minio_client.presigned_get_object(
                    bucket_name,
                    getattr(course, key),
                    expires=timedelta(seconds=3600)
                )
                for key in [
                    "id",
                    "name",
                    "description",
                    "detail",
                    "video_url",
                    "created_at",
                    "created_by",
                ]
            }
            for course in courses
        ]


        for course in courses_json:
            contents = session.query(ContentCourses).filter_by(course_id=course["id"]).all()
            contents_json = [
                {
                    key: getattr(content, key) if key != "video_url" else minio_client.presigned_get_object(
                        bucket_name,
                        getattr(content, key),
                        expires=timedelta(seconds=3600)
                    )
                    for key in [
                        "id",
                        "content_list",
                        "name",
                        "description",
                        "video_url",
                    ]
                }
                for content in contents
            ]
            course["contents"] = contents_json

            categories = session.query(CourseCategory).filter_by(course_id=course["id"]).all()
            categories_json = [
                {
                    "id": category.id,
                    "name": category.category.name
                }
                for category in categories
            ]
            course["categories"] = categories_json

        return {
            "data": courses_json,
            "total": total_courses,
            "page": page,
            "limit": limit
        }, 200

    except Exception as e:
        return {"msg": "Internal Server Error", "error": str(e)}, 500
    finally:
        session.close()

@courses_controller.route("/api/v1/course/<id>", methods=["GET"])
@jwt_required()
def get_courses_by_id(id):
    current_user = Users.query.filter_by(id=get_jwt_identity()).first()
    if not current_user:
        return {"message": "User not found"}, 404
    session = Session()
    try:
        course = session.query(Course).filter_by(id=id).first()
        if not course:
            return {"message": "No courses found"}, 404
        
        course_json = {
            key: getattr(course, key) if key != "video_url" else minio_client.presigned_get_object(
                    bucket_name,
                    getattr(course, key),
                    expires=timedelta(seconds=3600)
                )
            for key in [
                "id",
                "name",
                "description",
                "detail",
                "video_url",
                "created_at",
                "created_by",
            ]
        }

        contents = session.query(ContentCourses).filter_by(course_id=course.id).all()
        contents_json = [
            {
                key: getattr(content, key) if key != "video_url" else minio_client.presigned_get_object(
                    bucket_name,
                    getattr(content, key),
                    expires=timedelta(seconds=3600)
                )
                for key in [
                    "id",
                    "content_list",
                    "name",
                    "description",
                    "video_url",
                ]
            }
            for content in contents
        ]
        course_json["contents"] = contents_json

        categories = session.query(CourseCategory).filter_by(course_id=course.id).all()
        categories_json = [
            {
                "id": category.id,
                "name": category.category.name
            }
            for category in categories
        ]
        course_json["categories"] = categories_json

        print(course_json)
        return {"data": course_json}, 200


        

    except Exception as e:
        return {"msg": "Internal Server Error", "error": str(e)}, 500
    finally:
        session.close()

    
    