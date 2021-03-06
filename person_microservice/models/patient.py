from config import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    surname = db.Column(db.String(32), index=True)
    birthday = db.Column(db.Date)
    user = db.relationship("User", back_populates="patient", uselist=False)
    address = db.relationship("Address", back_populates="patient")
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    phone = db.Column(db.String(14))
    appointment = db.relationship("Appointment")


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(32))
    city = db.Column(db.String(32))
    street = db.Column(db.String(32))
    house_number = db.Column(db.String(16))
    number_flat = db.Column(db.String(16))
    patient = db.relationship("Patient", back_populates="address")
