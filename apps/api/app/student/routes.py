# The route from our auth module
from flask import request, jsonify, make_response
from app.student import bp
from app.auth import token_required
from sqlalchemy import and_

from app.models import Student
from app.extensions import db

# To debug the code
import pdb

@bp.route("/", methods = ["POST"])
@token_required
def post_student(user_session):
    data = request.json

    if not isinstance(data, dict) or data.keys() == []:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid input" }), 422)

    if not "name" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a name" }), 422)
    
    if not "phone" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a phone" }), 422)

    if not "plan_name" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a plan_name" }), 422)

    if not "email" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a email" }), 422)

    student_model = Student.query.filter(and_(
            Student.name.like(data["name"]),
            Student.user_id.like(int(user_session.id))
    )).first()
    
    if student_model != None:
        return make_response(jsonify({ "success" : False, "message" : "Student already exist" }), 404)

    data["user_id"] = int(user_session.id)
    
    try:
        student_model = Student(**data)
        db.session.add(student_model)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({
            "success" : False,
            "message" : f"Error: {e}"
        }))
        
    return make_response(jsonify({
        "success" : True,
        "message" : "Student created"
    }), 201)



@bp.route("/<id>", methods = ["GET"])
@token_required
def get_student(user_session, id):
    student_model = Student.query.filter(and_(
        Student.id.like(id),
        Student.user_id.like(int(user_session.id))
    )).first()

    if student_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "Student doesn't exist"
        }), 404)
    
    return make_response(jsonify({
        "success" : True,
        "message" : "Student found it",
        "data" : {
            "student" : student_model.to_dict()
        }
    }), 200)



@bp.route("/<id>", methods = ["DELETE"])
@token_required
def delete_student(user_session, id):
    student_model = Student.query.filter(and_(
        Student.id.like(id),
        Student.user_id.like(int(user_session.id))
    )).first()

    if student_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "Student doesn't exist"
        }), 404)

    db.session.delete(student_model)
    db.session.commit()
    
    return make_response(jsonify({
        "success" : True,
        "message" : "Student deleted it"
    }), 200)


@bp.route("/", methods = ["GET"])
@token_required
def get_students(user_session):
    students = Student.query\
                      .filter_by(user_id = int(user_session.id))\
                      .order_by(Student.enrollment_date)

    page = 1 if not "page" in request.args else int(request.args.get("page"))
    max_per_page = 15 if not "max_per_page" in request.args else int(request.args.get("max_per_page"))

    pagination = students.paginate(page = page, max_per_page = max_per_page)
    
    return make_response(jsonify({
        "success" : True,
        "message" : f"Students from user {user_session.id}",
        "data" : {
            "students" : [s.to_dict() for s in pagination.items]
        }
    }), 200)



@bp.route("/<id>", methods = ["PUT"])
@token_required
def update_student(user_session, id):
    data = request.json
    student_model = Student.query.filter(and_(
        Student.id.like(id),
        Student.user_id.like(int(user_session.id))
    )).first()

    if student_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "Student doesn't exist"
        }), 404)

    if not isinstance(data, dict) or data.keys() == []:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid input" }), 422)

    if "name" in data.keys():
        student_model.name = data["name"]
        
    if "phone" in data.keys():
        student_model.phone = data["phone"]
        
    if "plan_name" in data.keys():
        student_model.plan_name = data["plan_name"]

    if "email" in data.keys():
        student_model.email = data["email"]
        
    try:
        db.session.add(student_model)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({
            "success" : False,
            "message" : f"Error: {e}"
        }))
        
    return make_response(jsonify({
        "success" : True,
        "message" : "Student updated"
    }), 200)



