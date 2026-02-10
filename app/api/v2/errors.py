from functools import wraps

from flask import jsonify, render_template_string, request

from app.api.v2 import bp


def _prefers_json() -> bool:
    return (
        request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
        and request.accept_mimetypes["application/json"] > 0
    )


def api_error_boundary(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValueError as exc:
            return bad_request(str(exc))

    return wrapper


def bad_request(detail):
    return jsonify({"error": {"code": "bad_request", "detail": detail}}), 400


def unauthorized(detail):
    return jsonify({"error": {"code": "unauthorized", "detail": detail}}), 401


def not_found(detail):
    return jsonify({"error": {"code": "not_found", "detail": detail}}), 404


@bp.app_errorhandler(404)
def handle_404(error):
    if request.path.startswith("/api/v2") and _prefers_json():
        return jsonify({"error": {"code": "not_found", "detail": "Resource not found."}}), 404
    return error


@bp.app_errorhandler(500)
def handle_500(error):
    if request.path.startswith("/api/v2") and _prefers_json():
        return (
            jsonify(
                {
                    "error": {
                        "code": "internal_server_error",
                        "detail": "Unexpected server error.",
                    }
                }
            ),
            500,
        )
    return (
        render_template_string("<h1>Internal Server Error</h1><p>Please try again later.</p>"),
        500,
    )
