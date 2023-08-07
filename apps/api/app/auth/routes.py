# The route from our auth module
from flask import request, jsonify, make_response
from app.auth import bp, UserSession, generate_token, token_required

# To hash passwords and check
from werkzeug.security import generate_password_hash, check_password_hash

# db and the model user
from app.models import User, BlackListToken
from app.extensions import db

# To debug the code
import pdb

# To check an email
import re
pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@bp.route('/login', methods = ["POST"])
def login():
    data = request.json

    # Verify the data
    if not "passwd" in data.keys():
        return jsonify({ "success" : False, "message" : "Error needs a passwd field" })

    if not "email" in data.keys():
        return jsonify({ "success" : False, "message" : "Error needs a email field" })
    elif not re.match(pattern, data["email"]):
        return make_response(jsonify({ "success" : False, "message" : "Error invalid email" }), 422)

    # check if the users exist
    user_model = User.query.filter_by(email = data["email"]).first()
    if user_model == None:
        return make_response(jsonify({ "success" : False, "message" : "The user doesn't exist" }), 404)

    if not check_password_hash(user_model.passwd, data["passwd"]):
        return make_response(jsonify({ "success" : False, "message" : "Incorrect password" }), 404)
    
    return jsonify({
        "success" : True,
        "message" : "Logged",
        "data" : {
            "token" : generate_token(user_model.id)
        }
    })

@bp.route('/signup', methods = ["POST"])
def signup():
    data = request.json

    # Verify the data
    if not "name" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a name field" }), 422)
    elif data["name"] == "" or len(data["name"]) > User.__table__.columns.name.type.length:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid name" }), 422)

    if not "passwd" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a passwd field" }), 422)
    elif data["passwd"] == "" or len(data["passwd"]) > User.__table__.columns.passwd.type.length:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid passwd" }), 422)
    
    if not "email" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a email field" }), 422)
    elif data["email"] == "" \
         or len(data["email"]) > User.__table__.columns.email.type.length \
         or not re.match(pattern, data["email"]):
        return make_response(jsonify({ "success" : False, "message" : "Error invalid email" }), 422)
    
    if not "schoolname" in data.keys():
        return make_response(jsonify({ "success" : False, "message" : "Error needs a schoolname field" }), 422)
    elif data["schoolname"] == "" or len(data["schoolname"]) > User.__table__.columns.schoolname.type.length:
        return make_response(jsonify({ "success" : False, "message" : "Error invalid schoolname" }), 422)

    # check if the users exist
    user_model = User.query.filter_by(email = data["email"]).first()
    if user_model != None:
        return make_response(jsonify({ "success" : False, "message" : "The user already exist" }), 409)

    user_model = User(data["name"], data["email"], generate_password_hash(data["passwd"]), data["schoolname"])
    db.session.add(user_model)
    db.session.commit()
    
    # Return a success response with a 201 status code
    return make_response(jsonify({
        "success": True,
        "message": "Signed",
        "data" : {
            "token" : generate_token(user_model.id)
        }
    }), 201)

@bp.route("/settings", methods = ["GET"])
@token_required
def fetch_settings(user_session):
    user_model = user_session.query_data()
    return make_response(jsonify({
        "success" : True,
        "message" : "Actual settings",
        "data" : {
            "user" : user_model.to_dict()
        }
    }), 200)

@bp.route("/settings", methods = ["PUT"])
@token_required
def update_settings(user_session):
    user_model = user_session.query_data()
    data = request.json
    
    if not data:
        return make_response(jsonify({
            "success" : False,
            "message" : "Nothing to update, empty body message" }), 422)
    
    if "name" in data.keys():
        if data["name"] == "" or len(data["name"]) > User.__table__.columns.name.type.length:
            return make_response(jsonify({ "success" : False, "message" : "Error invalid name" }), 422)
        user_model.name = data["name"]
        
    if "schoolname" in data.keys():
        if data["schoolname"] == "" or len(data["schoolname"]) > User.__table__.columns.schoolname.type.length:
            return make_response(jsonify({ "success" : False, "message" : "Error invalid schoolname" }), 422)
        user_model.schoolname = data["schoolname"]
        
    if "email" in data.keys():
        if data["email"] == "" \
           or len(data["email"]) > User.__table__.columns.email.type.length \
           or not re.match(pattern, data["email"]):
            return make_response(jsonify({ "success" : False, "message" : "Error invalid email" }), 422)
        user_model.email = data["email"]

    if "passwd" in data.keys():
        if data["passwd"] == "" or len(data["passwd"]) > User.__table__.columns.passwd.type.length:
            return make_response(jsonify({ "success" : False, "message" : "Error invalid password" }), 422)
        user_model.passwd = generate_password_hash(data["passwd"])

    # Update the user
    db.session.commit()
    
    return make_response(jsonify({
        "success" : True,
        "message" : "Updated settings"
    }), 200)

@bp.route("/delete", methods = ["DELETE"])
@token_required
def delete_user(user_session):
    user_model = user_session.query_data()
    
    db.session.delete(user_model)
    db.session.commit()

    return make_response(jsonify({
        "success" : True,
        "message" : "User deleted"
    }), 200)

@bp.route("/logout", methods = ["POST"])
@token_required
def logout_user(user_session):
    black_list_token = BlackListToken(user_session.token, int(user_session.id))

    db.session.add(black_list_token)
    db.session.commit()
    
    return make_response(jsonify({
        "success" : True,
        "message" : "User loged out"
    }), 200)
