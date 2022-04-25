from .time_with_adding import get_start_time_appointments
from models.booking.workday import Appointment, Workday
from config import db


def send_message_about_cancelled_appointment(workday_id):
    planned_appointments = Appointment.query.filter((Appointment.workday_id == workday_id) | (Appointment.status == "planned"))
    #TODO send a notification to these users
    
    
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
