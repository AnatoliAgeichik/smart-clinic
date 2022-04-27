import datetime
import sqlalchemy
from config import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient = db.relationship("User")
    datetime = db.Column(db.DateTime(), default=datetime.datetime.now)
    message = db.Column(db.Text())
