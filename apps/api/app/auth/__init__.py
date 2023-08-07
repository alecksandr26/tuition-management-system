from flask import Blueprint, make_response, request, jsonify

# Import the models
from app.models import User, BlackListToken

# Import the jwt to decode the token
import jwt
import datetime
from functools import wraps

# import the app for the configs
from app.config import Config

bp = Blueprint('auth', __name__, url_prefix = '/api/auth')

def generate_token(id : int):
    assert isinstance(id, int)
    
    payload = {
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(days = 1),  # Token expiration time
        "iat" : datetime.datetime.utcnow(),
        "id" : id
    }
    
    return jwt.encode(payload, Config.SECRET_KEY, algorithm = "HS256")

def validate_token(token : str):
    data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    return data

# The UserSession class
class UserSession:
    def __init__(self, user_model : User, token : str = None):
        assert isinstance(user_model, User)
        self.id = str(user_model.id) # Create the string from integer
        self.token = token

    # To fetch the data from the user
    def query_data(self):
        return User.query.filter_by(id = int(self.id)).first()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            
        if not token:
            return make_response(jsonify({ "success" : False, "message" : "a valid token is missing" }), 401)

        model_token = BlackListToken.query.filter_by(token = token).first()
        if model_token != None:
            return make_response(jsonify({ "success" : False, "message" : "token is invalid" }), 401)
        
        try:
            data = validate_token(token)
            user_session = UserSession(User.query.filter_by(id = data['id']).first(), token)
        except:
            return make_response(jsonify({ "success" : False, "message" : "token is invalid" }), 401)

        return f(user_session, *args, **kwargs)
    return decorator

from app.auth import routes
