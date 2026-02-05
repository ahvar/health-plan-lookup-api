from flask import Flask

from app import db
from app.api.plans import get_plans_st_ra_ml
from app.models import Plan, RateArea, State


def create_test_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=True,
    )
    db.init_app(app)
    return app


def seed_plan_data():
    state = State(abbreviation="MO", name="Missouri")
    rate_area = RateArea(state_abbreviation="MO", area_number=3)
    plans = [
        Plan(
            plan_id="11512345602",
            state_abbreviation="MO",
            metal_level="Silver",
            rate=310.50,
            rate_area=rate_area,
        ),
        Plan(
            plan_id="11512345601",
            state_abbreviation="MO",
            metal_level="Bronze",
            rate=298.62,
            rate_area=rate_area,
        ),
    ]
    db.session.add(state)
    db.session.add(rate_area)
    db.session.add_all(plans)
    db.session.commit()


def test_get_plans_st_ra_ml_filters_by_state_rate_area_and_metal_level():
    app = create_test_app()
    with app.app_context():
        db.create_all()
        seed_plan_data()

        with app.test_request_context():
            response = get_plans_st_ra_ml("mo", 3, "silver")

        payload = response.get_json()

        assert payload["plans"] == [
            {
                "plan_id": "11512345602",
                "state": "MO",
                "metal_level": "Silver",
                "rate": 310.5,
                "rate_area": 3,
            }
        ]

        db.session.remove()
        db.drop_all()
