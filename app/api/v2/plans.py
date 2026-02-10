import sqlalchemy as sa
from flask import jsonify, request

from app import db
from app.api.v2 import bp
from app.api.v2.auth import require_api_key
from app.api.v2.errors import api_error_boundary, bad_request
from app.models import Plan, RateArea


@bp.get("/plans")
@require_api_key
@api_error_boundary
def get_plans():
    state = request.args.get("state")
    rate_area = request.args.get("rate_area", type=int)
    metal_level = request.args.get("metal_level")

    stmt = sa.select(Plan).join(RateArea)

    if state:
        stmt = stmt.where(Plan.state_abbreviation == state.strip().upper())
    if rate_area is not None:
        stmt = stmt.where(RateArea.area_number == rate_area)
    if metal_level:
        stmt = stmt.where(sa.func.lower(Plan.metal_level) == metal_level.strip().lower())

    plans = db.session.execute(stmt.order_by(Plan.plan_id)).scalars().all()
    if not plans:
        return bad_request("No plans matched the requested filters.")

    return jsonify(
        {
            "data": [
                {
                    "id": plan.plan_id,
                    "type": "plan",
                    "attributes": {
                        "state": plan.state_abbreviation,
                        "metalLevel": plan.metal_level,
                        "monthlyRate": float(plan.rate),
                    },
                    "relationships": {
                        "rateArea": {
                            "state": plan.rate_area.state_abbreviation,
                            "number": plan.rate_area.area_number,
                        }
                    },
                }
                for plan in plans
            ]
        }
    )
