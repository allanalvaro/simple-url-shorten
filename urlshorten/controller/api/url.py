from urlshorten.helpers.hash import generate_hash
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from sqlalchemy.exc import IntegrityError
from urlshorten import db
from urlshorten.model.url import Url


bp = Blueprint("url", __name__)


@bp.route('/shorten', methods=['POST'])
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

            hash_url = generate_hash()

            # not good. moving to something like offline Key-DB generator in the future.
            while Url.query.filter_by(hash_url=hash_url).first() is not None:
                print("Re-hashing")
                hash_url = generate_hash()

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


@bp.route('/geturl', methods=['POST'])
def geturl():
    if request.form:
        _hash = request.form.get('hash_to_url')
        if _hash is None:
            return 'empty hash given', 400

        hash_exists = Url.query.filter_by(hash_url=_hash).first()
        if hash_exists is not None:
            return redirect(hash_exists.get_url())
