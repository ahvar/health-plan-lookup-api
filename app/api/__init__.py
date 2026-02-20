from flask import Blueprint

bp = Blueprint("api", __name__)

from app.api import authentication, counties, errors, plans, zips  # noqa: E402,F401
