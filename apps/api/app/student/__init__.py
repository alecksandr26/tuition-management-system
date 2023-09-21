from flask import Blueprint

# Import the models
from app.models import Student

bp = Blueprint('student', __name__, url_prefix = '/api/student')

from app.student import routes
