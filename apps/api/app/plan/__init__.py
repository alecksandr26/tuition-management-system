from flask import Blueprint

from app.models import PlanOfPayment

bp = Blueprint("plan", __name__, url_prefix = "/api/plan")

from app.plan import routes

