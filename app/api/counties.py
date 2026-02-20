import sqlalchemy as sa
from flask import jsonify, request

from app import db
from app.api import bp
from app.api.authentication import require_api_key
from app.api.errors import api_error_boundary, bad_request
from app.models import County


@bp.get("/counties")
@require_api_key
@api_error_boundary
def get_counties():
    state = request.args.get("state")

    stmt = sa.select(County)
    if state:
        stmt = stmt.where(County.state_abbreviation == state.strip().upper())

    counties = db.session.execute(stmt.order_by(County.name)).scalars().all()
    if not counties:
        return bad_request("No counties matched the requested filters.")

    return jsonify(
        {
            "counties": [
                {
                    "code": county.code,
                    "name": county.name,
                    "state": county.state_abbreviation,
                }
                for county in counties
            ]
        }
    )
