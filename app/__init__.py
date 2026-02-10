from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.db import Model

db = SQLAlchemy(model_class=Model, metadata=Model.metadata)
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.v1 import bp as api_v1_bp
    from app.api.v2 import bp as api_v2_bp

    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
    app.register_blueprint(api_v2_bp, url_prefix="/api/v2")
    return app
