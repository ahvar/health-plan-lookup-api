from . import app


@app.route("/api/v1/plans?state=<state>&rate_area=<rate_area>&metal_level=<metal_level", methods=['GET'])
def get_plans_st_ra_ml(state, rate_area, metal_level):
    """
    Get the available plans and rates by state, rate area, and metal level

    :param state: state
    :param rate_area: rate area
    :param metal_level: metal level
    :return plans: plan data
    """
    pass


@app.route("/api/v1/plans?state=<state>", methods=['GET'])
def get_plans_st(state):
    """
    Get available plan IDs, rates, and rate areas for the state.

    :param state: state
    :return plans: plan data
    """
    pass

@app.route("/api/v1/plans?rate_area=<int:rate_area>", methods=['GET'])
def get_plans_ra(rate_area):
    """
    Get available plan IDs, states, and rates for rate area

    :params rate_area: rate area
    :return plans: plan data
    """


@app.route("/api/v1/rate_area?state=<state>&zipcode=<zipcode>", methods=['GET'])
def get_rate_area_st_zip(state, zipcode):
    """
    Get rate area(s) for this state and zipcode
    
    :param state: state
    :param zipcode: zipcode
    """


@app.route("/v1/rate_areas?zipcode=<zipcode>", methods=['GET'])
def get_rate_areas(zipcode):
    pass

@app.route("/api/v1/zipcodes", methods=['GET'])
def get_zipcodes():
    pass
