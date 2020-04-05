import datetime
from urlshorten import db


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
