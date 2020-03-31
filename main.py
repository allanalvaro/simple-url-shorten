import hashlib
import datetime
from base64 import b64encode
from flask import request, render_template, redirect
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "urldatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Url(db.Model):
    url = db.Column(db.String(800), unique=True, nullable=False, primary_key=False)
    hash_url = db.Column(db.String(6), unique=True, nullable=False, primary_key=True)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Url(url='%s', hash_url='%s')>" % (
            self.url, self.hash_url)

    def get_hash(self):
        return str(self.hash_url)

    def get_url(self):
        return str(self.url)


def generate_hash(url):
    hash_url = b64encode(url.encode())
    return hashlib.md5(hash_url).hexdigest()[:6]


@app.route('/geturl', methods=['POST'])
def geturl():
    if request.form:
        _hash = request.form.get('hash_to_url')
        if _hash is None:
            return 'empty hash given', 400

        hash_exists = Url.query.filter_by(hash_url=_hash).first()
        if hash_exists is not None:
            return redirect(hash_exists.get_url())


@app.route('/shorten', methods=['POST'])
def shorten():
    if request.form:
        url = request.form.get('url_to_shorten')

        if url.split("//")[0] not in ("http:", "https:", "sftp:", "ftp:"):
            return 'Wrong url', 400

        try:
            url_exists = Url.query.filter_by(url=url).first()
        except IntegrityError:
            return 'Unable to check if url exist', 500

        if url_exists is None:

            hash_url = generate_hash(url)

            # not good. moving to something like offline Key-DB generator in the future.
            while Url.query.filter_by(hash_url=hash_url).first() is not None:
                print("Re-hashing")
                hash_url = generate_hash(hash_url + str(datetime.datetime.utcnow))

            insert = Url(url=url, hash_url=hash_url)

            try:
                db.session.add(insert)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return 'Unable add a user', 500

            return hash_url

        else:
            print("url exists")
            return url_exists.get_hash()


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port="8080", debug=True)
