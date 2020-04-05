import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = (1, 0, 0, "dev")

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "urldatabase.db"))

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_file,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    from urlshorten import url

    app.register_blueprint(url.bp)

    return app
