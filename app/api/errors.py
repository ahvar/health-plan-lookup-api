from functools import wraps

from flask import jsonify, render_template_string, request

from app.api import bp


def _prefers_json() -> bool:
    return (
        request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
        and request.accept_mimetypes["application/json"] > 0
    )


def api_error_boundary(view_func):
    """Decorator for consistent unexpected-error handling in API views."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValueError as exc:
            return bad_request(str(exc))

    return wrapper


def bad_request(message):
    return jsonify({"error": "bad_request", "message": message}), 400


def unauthorized(message):
    return jsonify({"error": "unauthorized", "message": message}), 401


def forbidden(message):
    return jsonify({"error": "forbidden", "message": message}), 403


def not_found(message):
    return jsonify({"error": "not_found", "message": message}), 404


@bp.app_errorhandler(404)
def handle_404(error):
    if request.path.startswith("/api/v1") and _prefers_json():
        return jsonify({"error": "not_found", "message": "Resource not found."}), 404
    return error


@bp.app_errorhandler(500)
def handle_500(error):
    if request.path.startswith("/api/v1") and _prefers_json():
        return jsonify({"error": "internal_server_error", "message": "Unexpected server error."}), 500
    return (
        render_template_string("<h1>Internal Server Error</h1><p>Please try again later.</p>"),
        500,
    )
