from config import db
from models.notification import Notification
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    doctor = db.relationship(
        "Doctor", back_populates="user", cascade="all, delete", uselist=False
    )
    patient = db.relationship(
        "Patient", back_populates="user", cascade="all, delete", uselist=False
    )
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    notifications_received = db.relationship("Notification")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
