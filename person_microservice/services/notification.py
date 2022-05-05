from models.notification import Notification
from models.patient import Patient
from models.doctor import Doctor
from models.booking.workday import Workday
from services.services import get_object_by_id
from config import db
from constants.messages import (
    get_notification_message_patient_appointment,
    planned_appointment,
    get_notification_message_canceled_appointment,
    cancelled_appointment,
)
from celery_work.tasks import send_message_mail


def send_notification(recipient_id, message):
    new_notification = Notification(recipient_id=recipient_id, message=message)
    db.session.add(new_notification)
    db.session.commit()


def notification_appointment_action(patient_id_prev, appointment):
    message_content = {}
    workday = get_object_by_id(Model=Workday, id=appointment.workday_id)
    doctor = get_object_by_id(Model=Doctor, id=workday.doctor_id)
    message_content["start_time"] = appointment.start_time
    message_content["end_time"] = appointment.end_time
    message_content["doctor_name"] = f"{doctor.first_name} {doctor.surname}"
    message_content["place"] = workday.place

    if not patient_id_prev and appointment.patient_id:
        patient = get_object_by_id(Model=Patient, id=appointment.patient_id)

        message = get_notification_message_patient_appointment(
            start_time=message_content["start_time"],
            end_time=message_content["end_time"],
            doctor_name=message_content["doctor_name"],
            place=message_content["place"],
        )
        send_notification(patient.user.id, message)

        send_message_mail.apply_async(
            kwargs={
                "recipient_email": patient.user.email,
                "message_content": message_content,
                "action_message": planned_appointment,
                "subject_email": planned_appointment,
            }
        )

    elif patient_id_prev and not appointment.patient_id:
        patient = get_object_by_id(Model=Patient, id=patient_id_prev)
        message = get_notification_message_canceled_appointment(
            start_time=message_content["start_time"],
            end_time=message_content["end_time"],
            doctor_name=message_content["doctor_name"],
            place=message_content["place"],
        )
        send_notification(patient.user.id, message)

        send_message_mail.apply_async(
            kwargs={
                "recipient_email": patient.user.email,
                "message_content": message_content,
                "action_message": cancelled_appointment,
                "subject_email": cancelled_appointment,
            }
        )
