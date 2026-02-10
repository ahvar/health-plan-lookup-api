from flask import Blueprint

bp = Blueprint("api_v2", __name__)

from app.api.v2 import auth, errors, counties, zips, plans  # noqa: E402,F401
