from functools import wraps

from flask import current_app, request

from app.api.v1.errors import unauthorized


def require_api_key(view_func):
    """Require API key when API_KEY is configured."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        configured_key = current_app.config.get("API_KEY")
        if not configured_key:
            return view_func(*args, **kwargs)

        request_key = request.headers.get("X-API-Key")
        if request_key != configured_key:
            return unauthorized("A valid X-API-Key header is required.")

        return view_func(*args, **kwargs)

    return wrapper
