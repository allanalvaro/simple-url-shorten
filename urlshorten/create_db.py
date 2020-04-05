from flask.cli import with_appcontext
from urlshorten import db


@with_appcontext

def init_db():
    db.create_all()


init_db()
