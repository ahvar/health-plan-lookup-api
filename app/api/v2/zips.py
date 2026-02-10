import sqlalchemy as sa
from flask import jsonify, request

from app import db
from app.api.v2 import bp
from app.api.v2.auth import require_api_key
from app.api.v2.errors import api_error_boundary, bad_request
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
            "data": [
                {
                    "id": record.zipcode,
                    "type": "zipcode",
                    "attributes": {
                        "state": record.state_abbreviation,
                        "countyId": record.county_id,
                    },
                    "relationships": {
                        "rateArea": {
                            "number": record.rate_area.area_number,
                            "state": record.rate_area.state_abbreviation,
                        }
                    },
                }
                for record in zipcodes
            ]
        }
    )
