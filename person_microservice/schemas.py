from dataclasses import field
import email
from models.doctor import Doctor
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    name = fields.String()
    doctor_id = fields.Integer()
    patient_id = fields.Integer()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class EducationSchema(Schema):
    id = fields.Integer()
    university_name = fields.String()
    specialization = fields.String()
    education_degree = fields.String()
    date_of_graduation = fields.Date()


education_schema = EducationSchema()
educations_schema = EducationSchema(many=True)


class DoctorSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    surname = fields.String()
    birthday = fields.Date()
    education = fields.List(fields.Nested(EducationSchema))


doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)


class AddressSchema(Schema):
    id = fields.Integer()
    country = fields.String()
    city = fields.String()
    street = fields.String()
    house_number = fields.String()
    number_flat = fields.String()


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class PatientSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    surname = fields.String()
    birthday = fields.Date()
    phone = fields.String()
    address_id = fields.Integer()


patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)


class WorkdaySchema(Schema):
    id = fields.Integer()
    doctor_id = fields.Integer()
    date = fields.Date()
    start_time = fields.Time()
    end_time = fields.Time()
    appointment_duration = fields.Time()
    specialization = fields.String()
    description = fields.String()
    place = fields.String()


workday_schema = WorkdaySchema()
workdays_schema = WorkdaySchema(many=True)


class AppointmentSchema(Schema):
    id = fields.Integer()
    workday_id = fields.Integer()
    patient_id = fields.Integer()
    start_time = fields.Time()
    end_time = fields.Time()
    description = fields.String()
    status = fields.String()


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
