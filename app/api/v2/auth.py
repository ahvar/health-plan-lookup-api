from functools import wraps

from flask import current_app, request

from app.api.v2.errors import unauthorized


def require_api_key(view_func):
    """Require Bearer token when API_KEY is configured."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        configured_key = current_app.config.get("API_KEY")
        if not configured_key:
            return view_func(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        expected = f"Bearer {configured_key}"
        if auth_header != expected:
            return unauthorized("A valid bearer token is required.")

        return view_func(*args, **kwargs)

    return wrapper
