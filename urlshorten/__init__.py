import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

__version__ = (1, 0, 0, "dev")

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "urldatabase.db"))

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=database_file,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    app.cli.add_command(init_db_command)

    from urlshorten.controller.api import url
    from urlshorten.controller import default

    app.register_blueprint(url.bp)
    app.register_blueprint(default.bp)

    return app


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
