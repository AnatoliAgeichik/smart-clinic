def get_notification_message_patient_appointment(
    start_time, end_time, doctor_name, place
):
    return f"уou have made an appointment. Start time:{start_time}, End time: {end_time}. Doctor: {doctor_name} Place: {place}"


def get_notification_message_canceled_appointment(
    start_time, end_time, doctor_name, place
):
    return f"The appointment was canceled. Start time:{start_time}, End time: {end_time}. Doctor: {doctor_name} Place: {place}"


planned_appointment = "you have made an appointment"
cancelled_appointment = "your appointment has been cancelled"
