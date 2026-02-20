from flask import jsonify
from flask_login import current_user, login_required, logout_user

from app import db
from app.auth import bp


@bp.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return jsonify({"message": "Account already confirmed."}), 200

    if current_user.confirm(token):
        db.session.commit()
        return jsonify({"message": "You have confirmed your account. Thanks!"}), 200

    return jsonify({"message": "The confirmation link is invalid or has expired."}), 400


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been logged out."}), 200
