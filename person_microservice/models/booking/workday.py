from config import db
from sqlalchemy_utils.types.choice import ChoiceType


class Workday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    appointment_duration = db.Column(db.Time)
    specialization = db.Column(db.String(128))
    description = db.Column(db.Text)
    place = db.Column(db.String(256))
    appointment = db.relationship("Appointment", cascade="all, delete")


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workday_id = db.Column(db.Integer, db.ForeignKey("workday.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    description = db.Column(db.Text)
    STATUS_TYPES = [
       ('empty', 'empty'),
       ('planned', 'planned'),
       ('cancelled_by_doctor', 'cancelled_by_doctor'),
       ('cancelled_by_patient', 'cancelled_by_patient'),
       ('completed', 'completed'),
    ]
    status = db.Column(ChoiceType(STATUS_TYPES, impl=db.String()), default='empty')
