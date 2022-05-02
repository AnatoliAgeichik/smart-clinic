from .time_with_adding import get_start_time_appointments
from models.booking.workday import Appointment, Workday
from models.doctor import Doctor
from models.patient import Patient
from models.notification import Notification
from views.notification import create_notification
from config import db


def get_user_from_workday_id(workday_id):
    doctor_id = Workday.query.filter_by(id=workday_id).one().doctor_id
    return Doctor.query.filter_by(id=doctor_id).one().user.id


def get_user_from_patient_id(patient_id):
    return Patient.query.filter_by(id=patient_id).one().user.id


def send_message_about_cancelled_appointment(workday_id):
    planned_appointments = Appointment.query.filter(
        (Appointment.workday_id == workday_id) & (Appointment.status == "planned")
    )
    for appointment in planned_appointments:

        notification_data = {
            "recipient_id": get_user_from_patient_id(appointment.patient_id),
            "message": "appointment cancelled",
        }
        create_notification(notification_data)

    # TODO send a notification to these users


def delete_all_appointment_in_workday(workday_id=id):
    appointments = Appointment.query.filter((Appointment.workday_id == workday_id))
    for appointment in appointments:
        db.session.delete(appointment)
    db.session.commit()


def validation_access(user, user_id, workday_id):
    if not user.id == int(user_id):
        return 403
    if not (user.doctor or user.doctor.workday):
        return 404


# def change_appointment_status(appointment)
