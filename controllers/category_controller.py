from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import connection
from sqlalchemy.orm import sessionmaker
from models.category import Category
from models.courses_category import CourseCategory

category_controller = Blueprint("category_controller", __name__)
Session = sessionmaker(connection)


@category_controller.route('/api/v1/categories', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        session = Session()
        categories = session.query(Category).all()
        return jsonify({"data": [{"id": category.id, "name": category.name} for category in categories]}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    finally:
        session.close()


@category_controller.route('/api/v1/category/<id>' ,methods=['GET'])
@jwt_required()
def get_category(id):
    try:
        session = Session()
        category = session.query(Category).filter(Category.id==id).first()
        if category is None:
            return jsonify({"msg": "Category not found"}), 404
        
        courses = session.query(CourseCategory).filter_by(Category.category_id==id).all()
        return jsonify({"data": {"id": category.id, "name": category.name, "courses": [{"id": course.course_id, "name": course.course.name} for course in courses]}}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    finally:
        session.close()

