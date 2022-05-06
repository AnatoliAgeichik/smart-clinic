from flask import Blueprint, request, Response
from datetime import timedelta, time

from models.user import User
from models.booking.workday import Workday, Appointment
from schemas import (
    workdays_schema,
    appointments_schema,
    workday_schema,
    appointment_schema,
)
from services.auth import token_required, get_user_from_request
from services.booking.time_with_adding import get_start_time_appointments, time_adding
from services.booking.workday import (
    send_message_about_cancelled_appointment,
    delete_all_appointment_in_workday,
    validation_access,
)
from services.services import get_object_by_id
from services.notification import notification_appointment_action
from config import db


booking_view = Blueprint("booking", __name__)


@booking_view.route("/workdays", methods=["Get"])
def get_all_workday():
    return workdays_schema.dumps(Workday.query.all())


@booking_view.route("/user/<user_id>/doctor/workdays", methods=["Get"])
def get_workday_by_user_id(user_id):
    user = get_object_by_id(Model=User, id=user_id)
    if not user.doctor:
        return Response(status=404)
    workdays = Workday.query.filter_by(doctor_id=user.doctor.id)
    return Response(
        workdays_schema.dumps(workdays), status=200, mimetype="application/json"
    )


@token_required
@booking_view.route("/user/<user_id>/doctor/workday", methods=["Post"])
def create_workday(user_id):
    user = get_user_from_request(request)
    if not user.id == int(user_id):
        return Response(status=403)
    workday_data = workday_schema.load(request.json)
    new_workday = Workday(**workday_data)
    user.doctor.workday.append(new_workday)
    db.session.add(new_workday)
    db.session.commit()
    create_appointments_for_workday(workday_data, new_workday)
    return Response(
        workday_schema.dumps(new_workday), status=201, mimetype="application/json"
    )


def create_appointments_for_workday(workday_data, workday):
    for start_time in get_start_time_appointments(
        workday_data["start_time"],
        workday_data["end_time"],
        workday_data["appointment_duration"],
    ):
        appointment_data = {
            "start_time": start_time,
            "end_time": time_adding(start_time, workday_data["appointment_duration"]),
            "status": "empty",
        }
        new_appointment = create_appointment(appointment_data, workday)
        db.session.add(new_appointment)
    db.session.commit()


def create_appointment(appointment_data, workday):
    new_appointment = Appointment(**appointment_data)
    workday.appointment.append(new_appointment)
    return new_appointment


@booking_view.route("/user/<user_id>/doctor/workday/<workday_id>", methods=["Get"])
def get_workday_by_id(user_id, workday_id):
    user = get_object_by_id(Model=User, id=user_id)
    if not user.doctor:
        return Response(status=404)

    workday = Workday.query.filter((Workday.id == workday_id)).one()
    return Response(
        workday_schema.dumps(workday), status=200, mimetype="application/json"
    )


@token_required
@booking_view.route("/user/<user_id>/doctor/workday/<workday_id>", methods=["Put"])
def update_workday(user_id, workday_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)
    workday = Workday.query.filter_by(id=workday_id).one()
    workday_data = workday_schema.load(request.json)
    send_message_about_cancelled_appointment(workday_id=workday_id)
    delete_all_appointment_in_workday(workday_id=workday_id)

    Workday.query.filter_by(id=workday_id).update(workday_data)
    db.session.commit()
    create_appointments_for_workday(workday_data, workday)
    return Response(
        workday_schema.dumps(workday), status=200, mimetype="application/json"
    )


@token_required
@booking_view.route("/user/<user_id>/doctor/workday/<workday_id>", methods=["Delete"])
def delete_workday(user_id, workday_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)

    workday = Workday.query.filter_by(id=workday_id).one()
    db.session.delete(workday)
    db.session.commit()
    return Response(status=204)


@booking_view.route(
    "/user/<user_id>/doctor/workday/<workday_id>/appointments", methods=["Get"]
)
def get_appointments(user_id, workday_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)

    appointments = Appointment.query.filter(Appointment.workday_id == workday_id)
    return Response(
        appointments_schema.dumps(appointments), status=200, mimetype="application/json"
    )


@booking_view.route(
    "/user/<user_id>/doctor/workday/<workday_id>/appointments/<appointment_id>",
    methods=["Get"],
)
def get_appoinment_by_id(user_id, workday_id, appointment_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)

    appointment = Appointment.query.filter((Appointment.id == appointment_id)).one()
    return Response(
        appointment_schema.dumps(appointment), status=200, mimetype="application/json"
    )


@booking_view.route(
    "/user/<user_id>/doctor/workday/<workday_id>/appointments/<appointment_id>",
    methods=["Put"],
)
def update_appointment(user_id, workday_id, appointment_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)
    patient_id_prev = Appointment.query.filter_by(id=appointment_id).one().patient_id
    appointment_data = appointment_schema.load(request.json)
    Appointment.query.filter((Appointment.id == appointment_id)).update(
        appointment_data
    )
    db.session.commit()
    appointment_new = Appointment.query.filter_by(id=appointment_id).one()
    notification_appointment_action(patient_id_prev, appointment_new)

    return Response(status=200)


@booking_view.route(
    "/user/<user_id>/doctor/workday/<workday_id>/appointments/<appointment_id>",
    methods=["Delete"],
)
def delete_appointment(user_id, workday_id, appointment_id):
    user = get_user_from_request(request)
    response_status = validation_access(user, user_id, workday_id)
    if response_status:
        return Response(status=response_status)

    appointment = Appointment.query.filter((Appointment.id == appointment_id)).one()
    db.session.delete(appointment)
    db.session.commit()

    return Response(status=204)


@booking_view.route("/appointments", methods=["Get"])
def get_all_appointments():
    filters = dict(request.args)
    start_time_interval = (
        filters["start_time_interval"] if filters["start_time_interval"] else ""
    )
    del filters["start_time_interval"]
    end_time_interval = (
        filters["end_time_interval"] if filters["end_time_interval"] else ""
    )
    del filters["end_time_interval"]
    appoitments = (
        Appointment.query.filter_by(**filters)
        .filter(
            (Appointment.start_time >= start_time_interval)
            & (Appointment.end_time <= end_time_interval)
        )
        .all()
    )

    return Response(
        appointments_schema.dumps(appoitments), status=200, mimetype="application/json"
    )
