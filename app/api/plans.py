from flask import jsonify
import sqlalchemy as sa

from app import db
from app.api import bp
from app.models import Plan, RateArea


@bp.route(
    "/api/v1/plans?state=<state>&rate_area=<rate_area>&metal_level=<metal_level",
    methods=["GET"],
)
def get_plans_st_ra_ml(state, rate_area, metal_level):
    """
    Get the available plans and rates by state, rate area, and metal level

    :param state: state
    :param rate_area: rate area
    :param metal_level: metal level
    :return plans: plan data
    """
    normalized_state = state.strip().upper()
    normalized_metal_level = metal_level.strip().lower()
    stmt = (
        sa.select(Plan)
        .join(RateArea)
        .where(
            RateArea.state_abbreviation == normalized_state,
            RateArea.area_number == rate_area,
            sa.func.lower(Plan.metal_level) == normalized_metal_level,
        )
        .order_by(Plan.plan_id)
    )
    plans = db.session.execute(stmt).scalars().all()
    return jsonify(
        {
            "plans": [
                {
                    "plan_id": plan.plan_id,
                    "state": plan.state_abbreviation,
                    "metal_level": plan.metal_level,
                    "rate": float(plan.rate),
                    "rate_area": plan.rate_area.area_number,
                }
                for plan in plans
            ]
        }
    )


@bp.route("/api/v1/plans?state=<state>", methods=["GET"])
def get_plans_st(state):
    """
    Get available plan IDs, rates, and rate areas for the state.

    :param state: state
    :return plans: plan data
    """
    pass

@bp.route("/api/v1/plans?rate_area=<int:rate_area>", methods=["GET"])
def get_plans_ra(rate_area):
    """
    Get available plan IDs, states, and rates for rate area

    :params rate_area: rate area
    :return plans: plan data
    """


@bp.route("/api/v1/rate_area?state=<state>&zipcode=<zipcode>", methods=["GET"])
def get_rate_area_st_zip(state, zipcode):
    """
    Get rate area(s) for this state and zipcode
    
    :param state: state
    :param zipcode: zipcode
    """


@bp.route("/v1/rate_areas?zipcode=<zipcode>", methods=["GET"])
def get_rate_areas(zipcode):
    pass

@bp.route("/api/v1/zipcodes", methods=["GET"])
def get_zipcodes():
    pass
