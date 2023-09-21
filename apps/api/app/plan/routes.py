from flask import request, jsonify, make_response
from sqlalchemy import and_

from app.plan import bp
from app.auth import token_required

from app.models import PlanOfPayment, User
from app.extensions import db

import pdb

@bp.route("/", methods = ["POST"])
@token_required
def post_plan(user_session):
    data = request.json
    
    if not isinstance(data, dict) or data.keys() == []:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid input" }), 422)

    if not "name" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a name" }), 422)

    if not "number_of_classes" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a number of classes" }), 422)
    
    if not "price" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a price of the plan" }), 422)

    if not "method" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a method of payment" }), 422)

    plan_model = PlanOfPayment.query.filter(and_(
        PlanOfPayment.name.like(data["name"]),
        PlanOfPayment.user_id.like(int(user_session.id))
    )).first()
    
    if plan_model != None:
        return make_response(jsonify({ "success" : False, "message" : "Plan already exist" }), 404)
    
    data["user_id"] = int(user_session.id)
    try:
        plan_model = PlanOfPayment(**data)
        db.session.add(plan_model)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({ "success" : False, "message" : f"Error: {e}" }), 404)
    
    return make_response(jsonify({
        "success" : True,
        "message" : "Plan of payment created"
    }), 201)



@bp.route("/all", methods = ["GET"])
@token_required
def get_plans(user_session):
    plans = PlanOfPayment.query.filter_by(user_id = int(user_session.id)).all()

    return make_response(jsonify({
        "success" : True,
        "message" : "All the plans",
        "data" : {
            "plans_of_payment" : [plan_model.to_dict() for plan_model in plans]
        }
    }), 200)

@bp.route("/<name>", methods = ["GET"])
@token_required
def get_plan(user_session, name):
    plan_model = PlanOfPayment.query.filter(and_(
        PlanOfPayment.name.like(name),
        PlanOfPayment.user_id.like(int(user_session.id))
    )).first()

    if plan_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "That plan doens't exist"
        }), 422)

    return make_response(jsonify({
        "success" : True,
        "message" : "Plan of payment",
        "data" : {
            "plan_of_payment" : plan_model.to_dict()
        }
    }), 200)

@bp.route("/<name>", methods = ["DELETE"])
@token_required
def delete_plan(user_session, name):
    plan_model = PlanOfPayment.query.filter(and_(
        PlanOfPayment.name.like(name),
        PlanOfPayment.user_id.like(int(user_session.id))
    )).first()

    if plan_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "That plan doens't exist"
        }), 422)
    
    db.session.delete(plan_model)
    db.session.commit()

    return make_response(jsonify({
        "success" : True,
        "message" : "Plan deleted"
    }), 200)



@bp.route("/<name>", methods = ["PUT"])
@token_required
def update_plan(user_session, name):
    data = request.json
    plan_model = PlanOfPayment.query.filter(and_(
        PlanOfPayment.name.like(name),
        PlanOfPayment.user_id.like(int(user_session.id))
    )).first()

    if plan_model == None:
        return make_response(jsonify({
            "success" : False,
            "message" : "That plan doens't exist"
        }), 422)

    if not isinstance(data, dict) or data.keys() == []:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid input" }), 422)

    if "name" in data.keys():
        plan_model.name = data["name"]

    if "desc" in data.keys():
        plan_model.desc = data["desc"]

    if "number_of_classes" in data.keys():
        plan_model.desc = data["number_of_classes"]

    if "price" in data.keys():
        plan_model.price = data["price"]

    if "method" in data.keys():
        plan_model.method = data["method"]

    try:
        db.session.add(plan_model)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({ "success" : False, "message" : f"Error: {e}" }), 404)
    
    return make_response(jsonify({
        "success" : True,
        "message" : "Plan updated"
    }), 200)

