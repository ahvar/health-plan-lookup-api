from functools import wraps

from flask import current_app, g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from app.api import bp
from app.api.errors import forbidden, unauthorized

auth = HTTPBasicAuth()


class _AnonymousUser:
    is_anonymous = True
    confirmed = True

    def generate_auth_token(self, expiration=3600):
        return ""


def _get_user_model():
    """Return the configured user model class if available."""

    model_cls = current_app.config.get("USER_MODEL")
    if model_cls is not None:
        return model_cls

    model_path = current_app.config.get("USER_MODEL_PATH")
    if not model_path:
        return None

    module_name, _, attr_name = model_path.rpartition(".")
    if not module_name:
        return None

    module = __import__(module_name, fromlist=[attr_name])
    return getattr(module, attr_name, None)


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == "":
        return False

    user_model = _get_user_model()
    if user_model is None:
        g.current_user = _AnonymousUser()
        g.token_used = False
        return False

    if password == "":
        g.current_user = user_model.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = user_model.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized("Invalid credentials")


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


@bp.before_request
@auth.login_required
def before_request():
    current_user = getattr(g, "current_user", _AnonymousUser())
    if not getattr(current_user, "is_anonymous", True) and not getattr(current_user, "confirmed", False):
        return forbidden("Unconfirmed account")
    return None


@bp.route("/tokens/", methods=["POST"])
def get_token():
    current_user = getattr(g, "current_user", _AnonymousUser())
    if getattr(current_user, "is_anonymous", True) or getattr(g, "token_used", False):
        return unauthorized("Invalid credentials")

    token = current_user.generate_auth_token(expiration=3600)
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return jsonify({"token": token, "expiration": 3600})
