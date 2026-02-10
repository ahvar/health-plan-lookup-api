import sqlalchemy as sa
from flask import jsonify, request

from app import db
from app.api import bp
from app.api.authentication import require_api_key
from app.api.errors import api_error_boundary, bad_request
from app.models import ZipCode


@bp.get("/zipcodes")
@require_api_key
@api_error_boundary
def get_zipcodes():
    zipcode = request.args.get("zipcode")
    state = request.args.get("state")

    stmt = sa.select(ZipCode)
    if zipcode:
        stmt = stmt.where(ZipCode.zipcode == zipcode)
    if state:
        stmt = stmt.where(ZipCode.state_abbreviation == state.strip().upper())

    zipcodes = db.session.execute(stmt.order_by(ZipCode.zipcode)).scalars().all()
    if not zipcodes:
        return bad_request("No zip codes matched the requested filters.")

    return jsonify(
        {
            "zipcodes": [
                {
                    "zipcode": record.zipcode,
                    "state": record.state_abbreviation,
                    "county_id": record.county_id,
                    "rate_area": record.rate_area.area_number,
                }
                for record in zipcodes
            ]
        }
    )
